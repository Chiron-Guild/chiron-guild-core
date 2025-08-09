"""
This script provides functionalities to enrich a task entry by analyzing a
Git commit using the Google Gemini API.
"""
import os
import sys
import json
import google.generativeai as genai
from google.api_core import exceptions as api_exceptions

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

def initialize_model(model_name='gemini-1.5-flash'):
    """
    Initializes and configures the Gemini client for a specific model.
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
    """
    if "Human-authored-by:" in commit_message:
        print("Human-authored commit detected. Skipping AI enrichment.")
        return None

    prompt = f"""
    You are an expert AI code reviewer and technical writer for the Chiron Guild.
    Your task is to analyze a Git commit and generate a structured JSON analysis.

    Analyze the code changes found at the following URL:
    {commit_url}

    Now, generate a JSON object with the following three keys, strictly adhering
    to the format and instructions:

    1. "summary_of_changes": A brief, plain-language summary of what was
       technically done in the commit.
    2. "constructive_critique": A brief, objective critique of the code,
       focusing on potential improvements or alternative approaches.
    3. "skills_demonstrated": Generate a JSON list of 3-5 specific technical
       skills or concepts shown in this commit.

    Return ONLY the raw JSON object.
    """
    try:
        response = model.generate_content(
            [prompt],
            generation_config={"response_mime_type": "application/json"}
        )
        return json.loads(response.text)

    except (api_exceptions.GoogleAPICallError, json.JSONDecodeError) as e:
        print(f"ERROR: API call/JSON parse failed for {commit_url}. Reason: {e}")
        return None


def main():
    """
    Main function to read env vars and orchestrate the enrichment process.
    """
    commit_url = os.environ.get("COMMIT_URL")
    commit_message = os.environ.get("COMMIT_MESSAGE")

    if not commit_url or not commit_message:
        print("ERROR: COMMIT_URL or COMMIT_MESSAGE environment variables not set.")
        sys.exit(1)

    model = initialize_model()
    if not model:
        sys.exit(1)

    enrichment_data = get_enrichment_data(
        model, commit_url, commit_message
    )

    if enrichment_data:
        with open('enrichment.json', 'w', encoding='utf-8') as f:
            json.dump(enrichment_data, f, indent=2)
        print(f"Successfully generated enrichment data for {commit_url}")
    else:
        print(f"Failed to generate enrichment data for {commit_url}")
        # We don't exit with 1 here, because a failed enrichment is not a failed workflow
        sys.exit(0)


if __name__ == "__main__":
    main()
