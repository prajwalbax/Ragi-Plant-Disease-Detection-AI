import json
import logging

from groq import Groq

from app.core.config import settings
from app.services.prompt_service import build_prompt

logger = logging.getLogger(
    "ragi-api.llm"
)

client = Groq(
    api_key=settings.groq_api_key
)


def fallback():

    return {

        "english_explanation":[

            "Disease explanation unavailable.",

            "Please retry.",

            ""

        ],

        "kannada_explanation":[

            "ಮಾಹಿತಿ ಲಭ್ಯವಿಲ್ಲ.",

            "ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ.",

            ""

        ],

        "recommendation":{

            "chemical_name":

            "Unavailable",

            "dosage":

            "Unavailable",

            "application_method":

            "Unavailable"

        }

    }


def get_disease_advisory(

    disease:str,

    confidence:float

):

    try:

        prompt = build_prompt(

            disease,

            confidence

        )

        response = client.chat.completions.create(

        model=settings.llm_model,

        messages=[

                {

                    "role":"system",

                    "content":"""

        Return STRICT JSON ONLY.

        Never truncate output.

        Never add markdown.

        Never use ```json

        Always finish JSON.

        """

                },

            {

                "role":"user",

                "content":prompt

            }

            ],

            temperature=0.1,

            max_tokens=700

        )

        

        content = (

            response
            .choices[0]
            .message
            .content
        )

        if not content:

            logger.error(

                "Groq empty response"

            )

            return fallback()

        try:

            return json.loads(

                content

            )

        except Exception:

            logger.exception(

                "Invalid JSON from LLM"

            )

            logger.error(

                content

            )

            return fallback()

    except Exception:

        logger.exception(

            "Groq request failed"

        )

        return fallback()