import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key=os.getenv("GEMINI_API_KEY")

client=genai.Client(api_key=api_key)


def analyze_rfp(rfp_text):

    prompt=f"""
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

RFP DOCUMENT:

{rfp_text}
"""

    response=client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt
    )

    return response.text