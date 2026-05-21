import io
import json
import logging
import time

from pathlib import Path
from threading import Lock

import numpy as np
import tensorflow as tf

from PIL import (
    Image,
    UnidentifiedImageError
)

from app.core.config import settings

from app.schemas.prediction import (
    PredictionResponse
)

logger = logging.getLogger(
    "ragi-api.model"
)


DISEASE_DESCRIPTIONS = {

    "downy":
    "Downy mildew symptoms detected.",

    "healthy":
    "Leaf appears healthy.",

    "mottle":
    "Mottle symptoms detected.",

    "seedling":
    "Seedling disease symptoms detected.",

    "smut":
    "Smut symptoms detected.",

    "wilt":
    "Wilt symptoms detected."
}


class ModelNotReadyError(
    RuntimeError
):

    pass


class PredictionError(
    RuntimeError
):

    pass


class ModelService:

    def __init__(self):

        self._model = None

        self._classes = []

        self._lock = Lock()


    @property
    def is_loaded(self):

        return (

            self._model
            is not None

            and

            bool(
                self._classes
            )

        )


    def validate_assets(
        self
    ):

        model_dir = (
            settings
            .resolved_model_dir
        )

        class_file = (

            settings
            .resolved_class_indices_path

        )

        if not model_dir.exists():

            raise ModelNotReadyError(

                f"Missing model: "
                f"{model_dir}"

            )

        if not (

            model_dir /
            "saved_model.pb"

        ).exists():

            raise ModelNotReadyError(

                "SavedModel missing"

            )

        if not class_file.exists():

            raise ModelNotReadyError(

                "class_indices.json missing"

            )


    def load(self):

        with self._lock:

            if self.is_loaded:

                return

            self.validate_assets()

            logger.info(
                "Loading TensorFlow model..."
            )

            self._model = (

                tf.keras.layers
                .TFSMLayer(

                    str(
                        settings
                        .resolved_model_dir
                    ),

                    call_endpoint=
                    "serving_default"

                )

            )

            self._classes = (

                self._load_classes(

                    settings
                    .resolved_class_indices_path

                )

            )

            logger.info(
                "Model ready"
            )


    def predict(
        self,
        contents: bytes,
        filename: str
    ):

        if not self.is_loaded:

            self.load()

        image = (

            self
            ._preprocess_image(
                contents
            )

        )

        start = time.perf_counter()

        try:

            outputs = (

                self._model(
                    image
                )

            )

            preds = (

                list(
                    outputs.values()
                )[0]
                .numpy()
            )

        except Exception as exc:

            logger.exception(
                "Inference failed"
            )

            raise PredictionError(

                "Prediction failed"

            ) from exc

        duration = (

            time.perf_counter()
            - start
        )

        if (

            duration >

            settings
            .prediction_timeout_seconds

        ):

            raise PredictionError(

                "Prediction timeout"

            )

        idx = int(

            np.argmax(
                preds[0]
            )

        )

        confidence = float(

            preds[0][idx]

        )

        disease = (

            self._classes[idx]

        )

        logger.info(

            "Prediction "

            "file=%s "

            "disease=%s "

            "confidence=%.4f",

            filename,

            disease,

            confidence

        )

        return PredictionResponse(

            disease_class=
            disease,

            confidence=
            confidence,

            confidence_percent=
            round(
                confidence * 100,
                2
            ),

            description=

            DISEASE_DESCRIPTIONS.get(

                disease,

                "Disease detected."

            ),

            filename=
            filename,

            advisory={

                "english_explanation": [],

                "kannada_explanation": [],

                "recommendation": {

                    "chemical_name":"",

                    "dosage":"",

                    "application_method":""

                }

            }

        )


    def _load_classes(
        self,
        path: Path
    ):

        with path.open(

            "r",

            encoding=
            "utf-8"

        ) as file:

            raw = json.load(
                file
            )

        classes = [

            name

            for _, name

            in sorted(

                raw.items(),

                key=lambda x:

                int(x[0])

            )

        ]

        return classes


    def _preprocess_image(

        self,
        contents: bytes

    ):

        try:

            image = Image.open(

                io.BytesIO(
                    contents
                )

            ).convert(

                "RGB"

            )

        except (

            UnidentifiedImageError

        ):

            raise PredictionError(

                "Invalid image"

            )

        image = image.resize(

            (

                settings.image_size,

                settings.image_size

            )

        )

        array = (

            np.asarray(

                image,

                dtype=np.float32

            )

            / 255.0

        )

        return np.expand_dims(

            array,

            axis=0

        )


model_service = ModelService()