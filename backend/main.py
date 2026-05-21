import sys
from pathlib import Path

sys.path.insert(
    0,
    str(
        Path(__file__)
        .resolve()
        .parent
    )
)

from fastapi import FastAPI
from fastapi.middleware.cors import (
    CORSMiddleware
)

from app.api.routes import router

from app.core.config import (
    settings
)

from app.core.logging import (
    configure_logging,
    logger
)

from app.services.model_service import (
    model_service
)


configure_logging(
    settings.log_level
)


app = FastAPI(

    title=
    settings.app_name,

    version="2.0.0",

    description=(

        "Finger Millet disease "
        "detection API with "
        "TensorFlow inference "
        "and multilingual AI advisory"

    )

)


app.add_middleware(

    CORSMiddleware,

    allow_origins=
    settings.cors_origins,

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]

)


app.include_router(
    router
)


@app.on_event(
    "startup"
)
def startup():

    logger.info(

        "Starting %s",

        settings.app_name

    )

    model_service.validate_assets()

    if (

        settings
        .load_model_on_startup

    ):

        model_service.load()

        logger.info(
            "Model loaded"
        )

    logger.info(

        "Startup complete"

    )


@app.on_event(
    "shutdown"
)
def shutdown():

    logger.info(

        "Shutting down API"

    )