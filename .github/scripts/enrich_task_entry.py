"""
This script provides functionalities to enrich a task entry by analyzing a
Git commit using the Google Gemini API.

It is designed to be called from a GitHub Actions workflow, taking a commit URL
and message as input, and writing a JSON file with the AI-generated analysis.
"""

import os
import sys
import json
import argparse
import google.generativeai as genai
from google.api_core import exceptions as api_exceptions

# pylint: disable=invalid-name
# We use UPPER_SNAKE_CASE for constants, which is a standard Python convention.
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

def initialize_model():
    """Initializes and configures the Gemini client."""
    if not GEMINI_API_KEY:
        print("ERROR: GEMINI_API_KEY environment variable not set.")
        return None
    genai.configure(api_key=GEMINI_API_KEY)
    return genai.GenerativeModel('gemini-2.5-flash-preview-05-20')

def get_enrichment_data(model, commit_url, commit_message):
    """
    Calls the Gemini API to get an AI-generated analysis of a commit.

    Args:
        model: The initialized GenerativeModel client.
        commit_url (str): The URL of the commit to analyze.
        commit_message (str): The full message of the commit.

    Returns:
        A dictionary with the enrichment data, or None on failure.
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
       goal or purpose of this commit. Infer the 'why' behind the changes.
    2. "summary_of_changes": A brief, plain-language summary of what was
       technically done. Mention the files changed and the nature of the changes
       (e.g., 'added a function', 'refactored a class', 'fixed a bug').
    3. "constructive_critique": A brief, objective critique of the code changes.
       If the code is excellent, state that. If there are potential improvements
       (e.g., 'a variable could be named more clearly', 'this function could
       benefit from more comments'), mention them constructively. If the commit
       is too simple for a critique (e.g., a typo fix), state that.

    Return ONLY the raw JSON object, with no other text or markdown formatting.
    """
    try:
        # Configuration is passed directly into the generate_content call.
        response = model.generate_content(
            [prompt, commit_url],
            generation_config=genai.types.GenerationConfig(
                response_mime_type="application/json"
            ),
            # Explicitly disable thinking for cost control in automated tasks.
            thinking_config={"thinking_budget": 0}
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
        # Write the JSON response to a file with specified encoding.
        with open('enrichment_output.json', 'w', encoding='utf-8') as f:
            json.dump(enrichment_data, f, indent=2)
        print(f"Successfully generated enrichment data for {args.commit_url}")
    else:
        print(f"Failed to generate enrichment data for {args.commit_url}")
        sys.exit(1)

if __name__ == "__main__":
    main()