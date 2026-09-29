import json
import os
import re
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
# Clean model response
# ---------------------------------------------------------

def clean_json_response(text):
    """
    Clean an LLM response before JSON parsing.

    Handles:
    - empty responses
    - ```json ... ``` code fences
    - ``` ... ``` code fences
    - surrounding whitespace
    """

    if text is None:
        raise ValueError("Model returned an empty response.")

    text = str(text).strip()

    if not text:
        raise ValueError("Model returned an empty response.")

    # Remove opening Markdown code fence.
    text = re.sub(
        r"^\s*```(?:json)?\s*",
        "",
        text,
        flags=re.IGNORECASE
    )

    # Remove closing Markdown code fence.
    text = re.sub(
        r"\s*```\s*$",
        "",
        text
    )

    return text.strip()


# ---------------------------------------------------------
# Extract JSON array
# ---------------------------------------------------------

def extract_json_array(text):
    """
    Extract a JSON array from an LLM response.

    Examples of accepted responses:

    ["query one", "query two"]

    ```json
    ["query one", "query two"]
    ```

    Here are the queries:
    ["query one", "query two"]
    """

    cleaned = clean_json_response(text)

    # -----------------------------------------------------
    # Attempt 1: entire response is JSON
    # -----------------------------------------------------

    try:
        parsed = json.loads(cleaned)

        if isinstance(parsed, list):
            return parsed

    except json.JSONDecodeError:
        pass

    # -----------------------------------------------------
    # Attempt 2: find JSON array inside extra text
    # -----------------------------------------------------

    start = cleaned.find("[")

    if start != -1:
        # Try progressively smaller endings.
        for end in range(len(cleaned), start, -1):
            candidate = cleaned[start:end].strip()

            if not candidate.endswith("]"):
                continue

            try:
                parsed = json.loads(candidate)

                if isinstance(parsed, list):
                    return parsed

            except json.JSONDecodeError:
                continue

    # -----------------------------------------------------
    # Failed
    # -----------------------------------------------------

    raise ValueError(
        "Could not extract a valid JSON array from model response.\n\n"
        f"Raw model response:\n{cleaned}"
    )


# ---------------------------------------------------------
# Extract JSON object
# ---------------------------------------------------------

def extract_json_object(text):
    """
    Extract a JSON object from an LLM response.

    Examples:

    {"key": "value"}

    ```json
    {"key": "value"}
    ```

    Here is the result:
    {"key": "value"}
    """

    cleaned = clean_json_response(text)

    # -----------------------------------------------------
    # Attempt 1: entire response is JSON
    # -----------------------------------------------------

    try:
        parsed = json.loads(cleaned)

        if isinstance(parsed, dict):
            return parsed

    except json.JSONDecodeError:
        pass

    # -----------------------------------------------------
    # Attempt 2: find JSON object inside extra text
    # -----------------------------------------------------

    start = cleaned.find("{")

    if start != -1:
        # Try progressively smaller endings.
        for end in range(len(cleaned), start, -1):
            candidate = cleaned[start:end].strip()

            if not candidate.endswith("}"):
                continue

            try:
                parsed = json.loads(candidate)

                if isinstance(parsed, dict):
                    return parsed

            except json.JSONDecodeError:
                continue

    # -----------------------------------------------------
    # Failed
    # -----------------------------------------------------

    raise ValueError(
        "Could not extract a valid JSON object from model response.\n\n"
        f"Raw model response:\n{cleaned}"
    )


# ---------------------------------------------------------
# Call OpenRouter
# ---------------------------------------------------------

def call_openrouter(prompt, max_attempts=3):
    """
    Send a prompt to OpenRouter with retry handling.
    """

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

            # -------------------------------------------------
            # Validate response
            # -------------------------------------------------

            if not response.choices:
                raise ValueError(
                    "OpenRouter returned no choices."
                )

            content = response.choices[0].message.content

            if content is None:
                raise ValueError(
                    "OpenRouter returned an empty response."
                )

            content = str(content).strip()

            if not content:
                raise ValueError(
                    "OpenRouter returned an empty response."
                )

            return content

        except Exception as e:

            if attempt == max_attempts - 1:
                raise

            print(
                f"\nOpenRouter request failed: {e}\n"
                f"Retrying in 5 seconds "
                f"({attempt + 1}/{max_attempts})..."
            )

            time.sleep(5)


# ---------------------------------------------------------
# Fallback memory queries
# ---------------------------------------------------------

def get_fallback_memory_queries():

    return [
        "previous proposals for the same client",
        "successful proposals for similar projects",
        "unsuccessful proposals and lessons learned",
        "similar technical requirements and implementation approaches"
    ]


# ---------------------------------------------------------
# Generate memory-search queries
# ---------------------------------------------------------

def generate_memory_queries(rfp_analysis):

    prompt = ORCHESTRATOR_PROMPT.format(
        rfp_analysis=rfp_analysis
    )

    response_text = call_openrouter(prompt)

    print("\n===== MEMORY QUERY MODEL RESPONSE =====")
    print(response_text)
    print("=======================================\n")

    try:

        queries = extract_json_array(response_text)

    except ValueError as e:

        print("\nModel returned invalid JSON.")
        print(f"Reason: {e}")

        print("\nUsing fallback memory queries.")

        queries = get_fallback_memory_queries()

    # -----------------------------------------------------
    # Keep only non-empty strings
    # -----------------------------------------------------

    cleaned_queries = []

    for query in queries:

        if isinstance(query, str):

            query = query.strip()

            if query:
                cleaned_queries.append(query)

    # -----------------------------------------------------
    # If model returned an empty array
    # -----------------------------------------------------

    if not cleaned_queries:

        print(
            "Model returned no usable memory queries."
        )

        cleaned_queries = get_fallback_memory_queries()

    return cleaned_queries


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

    print("\n===== RECOMMENDATION MODEL RESPONSE =====")
    print(response_text)
    print("=========================================\n")

    try:

        recommendations = extract_json_object(
            response_text
        )

    except ValueError as e:

        print("\nModel returned invalid JSON.")
        print(f"Reason: {e}")

        raise ValueError(
            "Could not parse recommendations as JSON."
        ) from e

    if not isinstance(recommendations, dict):

        raise ValueError(
            "Recommendations response must be a JSON object."
        )

    return recommendations