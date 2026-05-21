from pydantic import BaseModel, Field


class HealthResponse(BaseModel):

    status: str = "running"

    model_loaded: bool = False


class Recommendation(BaseModel):

    chemical_name: str

    dosage: str

    application_method: str


class AdvisoryResponse(BaseModel):

    english_explanation: list[str]

    kannada_explanation: list[str]

    recommendation: Recommendation


class PredictionResponse(BaseModel):

    disease_class: str = Field(
        ...,
        alias="class"
    )

    confidence: float

    confidence_percent: float

    description: str

    filename: str

    advisory: AdvisoryResponse

    model_config = {

        "populate_by_name": True

    }