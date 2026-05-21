from fastapi import (
    APIRouter,
    File,
    HTTPException,
    UploadFile,
    status,
)

import logging
import traceback

from app.schemas.prediction import (
    HealthResponse,
    PredictionResponse,
)

from app.services.model_service import (
    ModelNotReadyError,
    PredictionError,
    model_service,
)

from app.services.llm_service import (
    get_disease_advisory,
)

logger = logging.getLogger(
    "ragi-api.routes"
)

router = APIRouter()


@router.get(
    "/",
    response_model=HealthResponse
)
@router.get(
    "/health",
    response_model=HealthResponse
)
def health():

    return HealthResponse(

        status="running",

        model_loaded=
        model_service.is_loaded

    )


@router.post(

    "/predict",

    response_model=
    PredictionResponse

)
async def predict(

    file: UploadFile = File(...)

):

    allowed = {

        "image/jpeg",

        "image/jpg",

        "image/png",

        "image/webp",

    }

    if (

        not file.content_type

        or

        file.content_type
        not in allowed

    ):

        raise HTTPException(

            status_code=

            status
            .HTTP_415_UNSUPPORTED_MEDIA_TYPE,

            detail=

            "Upload JPG, PNG or WEBP."

        )

    contents = await file.read()

    if not contents:

        raise HTTPException(

            status_code=

            status
            .HTTP_400_BAD_REQUEST,

            detail=

            "Image empty."

        )

    try:

        prediction = (

            model_service.predict(

                contents,

                file.filename
                or
                "upload"

            )

        )

        logger.info(

            "Prediction success "

            "disease=%s "

            "confidence=%.4f",

            prediction
            .disease_class,

            prediction
            .confidence

        )

        advisory = (

            get_disease_advisory(

                prediction
                .disease_class,

                prediction
                .confidence

            )

        )

        prediction.advisory = advisory

        return prediction

    except (

        ModelNotReadyError

    ) as exc:

        logger.exception(

            "Model load failure: %s",

            str(exc)

        )

        raise HTTPException(

            status_code=

            status
            .HTTP_503_SERVICE_UNAVAILABLE,

            detail=str(exc)

        ) from exc

    except (

        PredictionError

    ) as exc:

        logger.exception(

            "Prediction failure: %s",

            str(exc)

        )

        raise HTTPException(

            status_code=

            status
            .HTTP_422_UNPROCESSABLE_ENTITY,

            detail=str(exc)

        ) from exc

    except Exception as exc:

        logger.exception(

            "Unhandled backend failure"

        )

        traceback.print_exc()

        raise HTTPException(

            status_code=

            status
            .HTTP_500_INTERNAL_SERVER_ERROR,

            detail=

            str(exc)

        ) from exc