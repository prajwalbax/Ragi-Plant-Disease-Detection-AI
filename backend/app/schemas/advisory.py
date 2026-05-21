from pydantic import BaseModel
from typing import List


class Recommendation(
    BaseModel
):

    chemical_name: str

    dosage: str

    application_method: str


class AdvisoryResponse(
    BaseModel
):

    english_explanation: List[str]

    kannada_explanation: List[str]

    recommendation: Recommendation