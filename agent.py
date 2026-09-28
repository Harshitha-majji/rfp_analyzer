import json
import os
import time

from dotenv import load_dotenv
from openai import OpenAI

from prompts import ORCHESTRATOR_PROMPT, RECOMMENDATION_PROMPT


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
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)

MODEL_NAME = "openrouter/free"


# ---------------------------------------------------------
# Clean JSON response
# ---------------------------------------------------------

def clean_json_response(text):
    """Remove markdown code fences from the model response."""

    if not text:
        raise ValueError("Model returned an empty response.")

    text = text.strip()

    if text.startswith("```json"):
        text = text[len("```json"):].strip()

    elif text.startswith("```"):
        text = text[len("```"):].strip()

    if text.endswith("```"):
        text = text[:-3].strip()

    return text


# ---------------------------------------------------------
# Call OpenRouter
# ---------------------------------------------------------

def call_openrouter(prompt, max_attempts=3):
    """Send a prompt to OpenRouter with simple retry handling."""

    for attempt in range(max_attempts):

        try:

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

            if not response.choices:
                raise ValueError("OpenRouter returned no choices.")

            content = response.choices[0].message.content

            if not content:
                raise ValueError(
                    "OpenRouter returned an empty response."
                )

            return content

        except Exception as e:

            if attempt == max_attempts - 1:
                raise

            print(
                f"OpenRouter request failed. "
                f"Retrying in 5 seconds ({attempt + 1}/{max_attempts})..."
            )

            time.sleep(5)


# ---------------------------------------------------------
# Generate memory-search queries
# ---------------------------------------------------------

def generate_memory_queries(rfp_analysis):

    prompt = ORCHESTRATOR_PROMPT.format(
        rfp_analysis=rfp_analysis
    )

    response_text = call_openrouter(prompt)

    cleaned_text = clean_json_response(response_text)

    try:

        queries = json.loads(cleaned_text)

    except json.JSONDecodeError as e:

        print("\nModel returned invalid JSON:")
        print(cleaned_text)

        raise ValueError(
            "Could not parse memory queries as JSON."
        ) from e

    if not isinstance(queries, list):

        raise ValueError(
            "Memory queries response must be a JSON array."
        )

    return queries


# ---------------------------------------------------------
# Generate recommendations
# ---------------------------------------------------------

def generate_recommendations(rfp_analysis, memories):

    prompt = RECOMMENDATION_PROMPT.format(
        rfp_analysis=rfp_analysis,
        memories=json.dumps(
            memories,
            indent=2,
            ensure_ascii=False
        )
    )

    response_text = call_openrouter(prompt)

    cleaned_text = clean_json_response(response_text)

    try:

        recommendations = json.loads(cleaned_text)

    except json.JSONDecodeError as e:

        print("\nModel returned invalid JSON:")
        print(cleaned_text)

        raise ValueError(
            "Could not parse recommendations as JSON."
        ) from e

    if not isinstance(recommendations, dict):

        raise ValueError(
            "Recommendations response must be a JSON object."
        )

    return recommendations