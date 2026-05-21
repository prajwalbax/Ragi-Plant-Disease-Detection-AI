from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class Settings(BaseSettings):

    # App

    app_name: str = (
        "Ragi Disease Detection API"
    )

    log_level: str = "INFO"

    host: str = "0.0.0.0"

    port: int = 8000


    # Model

    load_model_on_startup: bool = True

    model_dir: Path = Field(
        default=Path(
            "../my_model"
        )
    )

    class_indices_path: Path = Field(
        default=Path(
            "../class_indices.json"
        )
    )

    image_size: int = 224

    prediction_timeout_seconds: float = 30.0


    # LLM

    groq_api_key: str = ""

    llm_model: str = (
        "llama-3.3-70b-versatile"
    )

    llm_timeout_seconds: float = 20.0


    # Future deployment

    frontend_url: str = (
        "http://localhost:3000"
    )


    # CORS

    cors_origins: list[str] = [

        "http://localhost:3000",

        "http://127.0.0.1:3000",

        "https://*.vercel.app",

    ]


    model_config = SettingsConfigDict(

        env_file=".env",

        env_prefix="RAGI_",

        case_sensitive=False,

        extra="ignore"

    )


    @property
    def backend_root(self) -> Path:

        return (
            Path(__file__)
            .resolve()
            .parents[2]
        )


    @property
    def resolved_model_dir(
        self
    ) -> Path:

        return self._resolve_path(
            self.model_dir
        )


    @property
    def resolved_class_indices_path(
        self
    ) -> Path:

        return self._resolve_path(
            self.class_indices_path
        )


    def _resolve_path(
        self,
        path: Path
    ) -> Path:

        if path.is_absolute():

            return path

        return (

            self.backend_root
            / path

        ).resolve()


@lru_cache
def get_settings():

    return Settings()


settings = get_settings()