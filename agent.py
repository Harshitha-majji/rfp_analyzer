import json
import os

from dotenv import load_dotenv
from google import genai

from prompts import ORCHESTRATOR_PROMPT

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


def generate_memory_queries(rfp_analysis):
    prompt = ORCHESTRATOR_PROMPT.format(
        rfp_analysis=rfp_analysis
    )

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt
    )

    text = response.text.strip()

    # Remove markdown code fences if Gemini returns them
    if text.startswith("```"):
        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()

    return json.loads(text)