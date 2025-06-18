"""
This script provides functionalities to enrich a task entry by analyzing a
Git commit using the Google Gemini API.

It is designed to be called from a workflow, taking a commit URL, message, and
model name as input, and writing a JSON file with the AI-generated analysis.
It respects a 'Human-authored-by:' trailer to bypass AI enrichment.
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

def initialize_model(model_name='gemini-2.5-flash-lite-preview-06-17'):
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
    return genai.GenerativeModel(model_name)

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
    # 1. Check for the human-authored trailer first.
    if "Human-authored-by:" in commit_message:
        print("Human-authored commit detected. Skipping AI enrichment.")
        return {
            "provenance_type": "human_authored",
            "objective": "Task completed via direct human authorship.",
            "summary_of_changes": commit_message.split('\n', 1)[0],
            "constructive_critique": None,
            "task_category": "CORE",  # Default for human-only tasks
            "task_type": "DEV",     # Default for human-only tasks
            "skills_demonstrated": ["Human-Only Authorship"]
        }

    # 2. If no trailer, proceed with AI enrichment.
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

    Now, generate a JSON object with the following keys, strictly adhering to
    the format and instructions.

    **Instructions for JSON Fields:**

    1.  "creators": Create a JSON list of strings. The primary human author
        is found in the commit data. The AI tool used for this analysis is
        "gemini-2.0-flash". Example: ["Person: Kin-Caid", "Tool: gemini-2.0-flash"].

    2.  "objective": A concise, one-sentence statement describing the primary
        goal of this commit. If the commit message body provides a good
        explanation, synthesize it. If the message is generic (e.g., "updates"),
        you MUST infer the purpose directly from analyzing the code changes.

    3.  "summary_of_changes": A brief, plain-language summary of what was
        technically done. Mention files changed and the nature of the changes.

    4.  "task_category":
        - **First, TRY to parse** the category from a `Task-Category:` tag in the commit message.
        - **If the tag is NOT PRESENT,** you MUST infer the BEST matching
          category from this list: ["CORE", "PERS", "PROD", "CLIENT"].
          - CORE: Building the Guild itself (infrastructure, governance).
          - PERS: Personal skill development or projects.
          - PROD: Building a new, shared asset for the Guild.
          - CLIENT: Work for an external client.

    5.  "task_type":
        - **First, TRY to parse** the type from a `Task-Type:` tag in the commit message.
        - **If the tag is NOT PRESENT,** you MUST infer the BEST matching
          type from this list: ["DEV", "DSN", "DOC", "GOV", "STR", "QAT", "COM", "LRN", "PROJ"].
          - DEV: Development, coding, scripting.
          - DSN: Design (UI/UX, architecture).
          - DOC: Documentation writing.

    6.  "skills_demonstrated": A JSON list of 3-5 specific technical skills
        or concepts demonstrated in this commit (e.g., ["Python", "GitHub Actions", "API Design"]).

    7.  "annotations": A JSON list containing one or more annotation objects.
        Create at least one annotation object with the following structure:
        {{
          "annotationType": "REVIEW",
          "annotationDate": "YYYY-MM-DDTHH:MM:SSZ",
          "comment": "[Your constructive critique of the code changes. If the message is generic, your critique should note the lack of a descriptive message as a point for improvement.]",
          "annotator": "Tool: chiron-guild-bot-v1.1"
        }}

    Return ONLY the raw JSON object.
    """
    try:
        response = model.generate_content(
            [prompt, commit_url],
            generation_config=genai.types.GenerationConfig(
                response_mime_type="application/json"
            )
        )
        enrichment = json.loads(response.text)

        if not isinstance(enrichment, dict):
            print(f"ERROR: AI returned an unexpected data type (expected dict, got {type(enrichment)}).")
            print(f"Raw AI Response: {enrichment}")
            return None # Return None to indicate failure

        # If the check passes, we can safely proceed.
        enrichment["provenance_type"] = "ai_assisted"
        return enrichment

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
    parser.add_argument("--model-name", default='gemini-2.0-flash', help="The Gemini model to use.")
    args = parser.parse_args()

    model = initialize_model(args.model_name)
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