import os

from dotenv import load_dotenv
from openai import OpenAI


# ---------------------------------------------------------
# Load environment variables
# ---------------------------------------------------------

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    raise ValueError(
        "OPENROUTER_API_KEY is missing. "
        "Please check your .env file."
    )


# ---------------------------------------------------------
# OpenRouter client
# ---------------------------------------------------------

client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)


# ---------------------------------------------------------
# Model
# ---------------------------------------------------------

MODEL_NAME = "openai/gpt-4o-mini"


# ---------------------------------------------------------
# Analyze RFP
# ---------------------------------------------------------

def analyze_rfp(rfp_text):

    prompt = f"""
You are an RFP Analyzer.

Analyze the following RFP document carefully.

Extract the following information:

1. Client
2. Project
3. Project Description
4. Requirements
5. Technical Requirements
6. Deliverables
7. Timeline
8. Budget
9. Eligibility Criteria
10. Evaluation Criteria
11. Constraints

If information is not present in the RFP, write "Not specified".

Do not invent information.

Return the analysis in a clear, structured format.

RFP DOCUMENT:

{rfp_text}
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content

