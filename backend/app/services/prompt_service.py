def build_prompt(
    disease: str,
    confidence: float
):

    return f"""
You are an agricultural expert specialized in Finger Millet diseases.

Disease detected:
{disease}

Prediction confidence:
{confidence:.2f}

Tasks:

1. Explain the disease in exactly 3 simple English lines.

2. Explain the disease in exactly 3 simple Kannada lines.

3. Recommend the best pesticide/fungicide.

4. Provide dosage.

5. Provide application method.

Rules:

- Use farmer friendly language.
- Kannada should be simple Karnataka Kannada.
- Return ONLY valid JSON.
- Do not use markdown.

Output format:

{{
  "english_explanation":[
    "",
    "",
    ""
  ],

  "kannada_explanation":[
    "",
    "",
    ""
  ],

  "recommendation":{{

    "chemical_name":"",

    "dosage":"",

    "application_method":""

  }}
}}
"""