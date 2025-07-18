"""
This script provides functionalities to enrich a task entry by analyzing a
Git commit using the Google Gemini API.
"""
import os
import sys
import json
import argparse
import google.generativeai as genai
from google.api_core import exceptions as api_exceptions

# pylint: disable=invalid-name
# We use UPPER_SNAKE_CASE for constants, a standard Python convention.
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

def initialize_model(model_name='gemini-2.0-flash'):
    """
    Initializes and configures the Gemini client for a specific model.

    Args:
        model_name (str): The name of the Gemini model to use.

    Returns:
        An initialized GenerativeModel client, or None on failure.
    """
    if not GEMINI_API_KEY:
        print("ERROR: GEMINI_API_KEY environment variable not set.")
        return None
    genai.configure(api_key=GEMINI_API_KEY)
    print(f"Initializing model: {model_name}")
    return genai.GenerativeModel(model_name=model_name)


def get_enrichment_data(model, commit_url, commit_message):
    """
    Calls the Gemini API to get an AI-generated analysis of a commit.
    Also checks for the 'Human-authored-by' trailer to bypass the API call.

    Args:
        model: The initialized GenerativeModel client.
        commit_url (str): The URL of the commit to analyze.
        commit_message (str): The full message of the commit.

    Returns:
        A dictionary with the enrichment data, or None on failure.
    """
    if "Human-authored-by:" in commit_message:
        print("Human-authored commit detected. Skipping AI enrichment.")
        return {
            "provenance_type": "human_authored",
            "objective": "Task completed via direct human authorship.",
            "summary_of_changes": commit_message.split('\n', 1)[0],
            "constructive_critique": None,
            "task_category": "CORE",
            "task_type": "DEV",
            "skills_demonstrated": ["Human-Only Authorship"]
        }

    prompt = f"""
    You are an expert AI code reviewer and technical writer for the Chiron Guild,
    specializing in creating SPDX-compliant metadata. Your task is to analyze
    a Git commit and generate a structured JSON analysis.

    First, analyze the provided commit message for structured data:
    --- COMMIT MESSAGE ---
    {commit_message}
    --- END COMMIT MESSAGE ---

    Next, analyze the code changes found at the following URL:
    {commit_url}

    Now, generate a JSON object with the following six keys, strictly adhering
    to the format and instructions:

    1. "objective": A concise, one-sentence statement describing the primary
       goal of this commit.
    2. "summary_of_changes": A brief, plain-language summary of what was
       technically done.
    3. "constructive_critique": A brief, objective critique of the code.
    4. "task_category": Infer the BEST matching category from ["CORE", "PERS",
       "PROD", "CLIENT"].
    5. "task_type": Infer the BEST matching type from ["DEV", "DSN", "DOC",
       "GOV", "STR", "QAT", "COM", "LRN", "PROJ"].
    6. "skills_demonstrated": Generate a JSON list of 3-5 specific technical
       skills or concepts shown in this commit.

    Return ONLY the raw JSON object.
    """
    try:
        response = model.generate_content(
            [prompt, commit_url],
            generation_config=genai.types.GenerationConfig(
                response_mime_type="application/json"
            )
        )
        parsed_json = json.loads(response.text)

        # --- THIS IS THE FIX ---
        # Gracefully handle if the AI returns a list containing one dict
        if isinstance(parsed_json, list) and parsed_json:
            enrichment = parsed_json[0]
        else:
            enrichment = parsed_json

        # Now, safely check if the result is a dictionary before proceeding
        if not isinstance(enrichment, dict):
            print(f"ERROR: AI returned an unexpected data type: {type(enrichment)}.")
            return None

        enrichment["provenance_type"] = "ai_assisted"
        return enrichment

    except (api_exceptions.GoogleAPICallError, json.JSONDecodeError) as e:
        print(f"ERROR: API call/JSON parse failed for {commit_url}. Reason: {e}")
        return None


def main():
    """
    Main function to parse arguments and orchestrate the enrichment process.
    """
    parser = argparse.ArgumentParser(description="Enrich a task entry using AI.")
    parser.add_argument(
        "--commit-url", required=True, help="The URL of the commit to analyze."
    )
    parser.add_argument(
        "--commit-message", required=True, help="The full message of the commit."
    )
    parser.add_argument(
        "--model-name", default='gemini-2.0-flash', help="The Gemini model to use."
    )
    args = parser.parse_args()

    model = initialize_model(args.model_name)
    if not model:
        sys.exit(1)

    enrichment_data = get_enrichment_data(
        model, args.commit_url, args.commit_message
    )

    if enrichment_data:
        with open('enrichment_output.json', 'w', encoding='utf-8') as f:
            json.dump(enrichment_data, f, indent=2)
        print(f"Successfully generated enrichment data for {args.commit_url}")
    else:
        print(f"Failed to generate enrichment data for {args.commit_url}")
        sys.exit(1)


if __name__ == "__main__":
    main()