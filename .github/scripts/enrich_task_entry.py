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
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

def initialize_model():
    """Initializes and configures the Gemini client."""
    if not GEMINI_API_KEY:
        print("ERROR: GEMINI_API_KEY environment variable not set.")
        return None
    genai.configure(api_key=GEMINI_API_KEY)
    # Use the 2.0 Flash model for its higher rate limits during this large backfill.
    return genai.GenerativeModel('gemini-2.0-flash')

def get_enrichment_data(model, commit_url, commit_message):
    """
    Calls the Gemini API to get an AI-generated analysis of a commit.
    """
    prompt = f"""
    You are an expert AI code reviewer and technical writer for the Chiron Guild.
    Your task is to analyze a Git commit and provide a structured summary.
    Analyze the code changes found at the following URL. The original commit
    message was:

    --- COMMIT MESSAGE ---
    {commit_message}
    --- END COMMIT MESSAGE ---

    Based on your analysis of the code changes (the 'diff') and the commit
    message, provide a JSON object with the following three keys:
    1. "objective": A concise, one-sentence statement describing the primary
       goal or purpose of this commit.
    2. "summary_of_changes": A brief, plain-language summary of what was
       technically done.
    3. "constructive_critique": A brief, objective critique of the code changes.

    Return ONLY the raw JSON object, with no other text or markdown formatting.
    """
    try:
        # --- THIS IS THE FIX ---
        # The `thinking_config` parameter has been removed, as it is not
        # compatible with the 'gemini-2.0-flash' model.
        response = model.generate_content(
            [prompt, commit_url],
            generation_config=genai.types.GenerationConfig(
                response_mime_type="application/json"
            )
        )
        return json.loads(response.text)
    except (api_exceptions.GoogleAPICallError, json.JSONDecodeError) as e:
        print(f"ERROR: Gemini API call or JSON parsing failed for {commit_url}. Reason: {e}")
        return None

def main():
    """
    Main function to parse arguments and orchestrate the enrichment process.
    """
    parser = argparse.ArgumentParser(description="Enrich a task entry using AI.")
    parser.add_argument("--commit-url", required=True, help="The URL of the commit to analyze.")
    parser.add_argument("--commit-message", required=True, help="The full message of the commit.")
    args = parser.parse_args()

    model = initialize_model()
    if not model:
        sys.exit(1)

    enrichment_data = get_enrichment_data(model, args.commit_url, args.commit_message)

    if enrichment_data:
        with open('enrichment_output.json', 'w', encoding='utf-8') as f:
            json.dump(enrichment_data, f, indent=2)
        print(f"Successfully generated enrichment data for {args.commit_url}")
    else:
        print(f"Failed to generate enrichment data for {args.commit_url}")
        sys.exit(1)

if __name__ == "__main__":
    main()