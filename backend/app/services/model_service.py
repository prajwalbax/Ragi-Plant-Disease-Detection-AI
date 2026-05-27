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

        self._interpreter = None

        self._input_details = None

        self._output_details = None

        self._classes = []

        self._lock = Lock()

        self._model_path = (

            settings
            .resolved_model_dir
            / "model.tflite"

        )


    @property
    def is_loaded(self):

        return (

            self._interpreter
            is not None

            and

            bool(
                self._classes
            )

        )


    def validate_assets(
        self
    ):

        model_file = (

            self._model_path

        )

        class_file = (

            settings
            .resolved_class_indices_path

        )

        if not model_file.exists():

            raise ModelNotReadyError(

                f"Model missing: "

                f"{model_file}"

            )

        if not class_file.exists():

            raise ModelNotReadyError(

                f"Missing class file: "

                f"{class_file}"

            )


    def load(self):

        with self._lock:

            if self.is_loaded:

                return

            self.validate_assets()

            logger.info(

                "Loading TFLite model..."

            )

            with open(

                self._model_path,

                "rb"

            ) as file:

                model_bytes = (

                    file.read()

                )

            self._interpreter = (

                tf.lite.Interpreter(

                    model_content=
                    model_bytes,

                    num_threads=1

                )

            )

            self._interpreter.allocate_tensors()

            self._input_details = (

                self
                ._interpreter
                .get_input_details()

            )

            self._output_details = (

                self
                ._interpreter
                .get_output_details()

            )

            self._classes = (

                self._load_classes(

                    settings
                    .resolved_class_indices_path

                )

            )

            logger.info(

                "TFLite model ready"

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

            self._interpreter.set_tensor(

                self
                ._input_details[0]["index"],

                image.astype(
                    np.float32
                )

            )

            self._interpreter.invoke()

            preds = (

                self
                ._interpreter
                .get_tensor(

                    self
                    ._output_details[0]["index"]

                )

            )

        except Exception as exc:

            logger.exception(

                f"Inference failed: {str(exc)}"

            )

            raise PredictionError(

                f"Prediction failed: {str(exc)}"

            ) from exc

        duration = (

            time.perf_counter()

            - start

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

            "confidence=%.4f "

            "duration=%.4fs",

            filename,

            disease,

            confidence,

            duration

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

                "english_explanation":[],

                "kannada_explanation":[],

                "recommendation":{

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

            encoding="utf-8"

        ) as file:

            raw = json.load(
                file
            )

        return [

            name

            for _, name

            in sorted(

                raw.items(),

                key=lambda x:

                int(x[0])

            )

        ]


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