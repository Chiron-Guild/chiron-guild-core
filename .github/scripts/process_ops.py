import os
import json
import subprocess
import time
import argparse
import google.generativeai as genai
from pathlib import Path

# Configuration
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

# User specified "gemini-1.5-flash-preview-05-20", using 'gemini-1.5-flash-latest' for broader compatibility and updates.
# If you have specific access to the preview model and prefer it, you can change this back.
GEMINI_MODEL_NAME = "gemini-1.5-flash-latest" 
REQUESTS_PER_MINUTE_LIMIT = 10
SLEEP_INTERVAL = 60.0 / REQUESTS_PER_MINUTE_LIMIT

# Configure the Gemini client
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    print("ERROR: GEMINI_API_KEY environment variable not set. Please set it in your GitHub Repository Secrets.")
    exit(1)

# Generation configuration for the LLM.
# temperature: Lower values (closer to 0) make the output more deterministic.
# top_p/top_k: Control diversity. Set to 1 for maximum predictability.
# response_mime_type: Crucial for ensuring the model attempts to output valid JSON.
generation_config = {
    "temperature": 0.7, 
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 4096, 
    "response_mime_type": "application/json", 
}

# Safety settings to prevent generation of harmful content.
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

def load_prompt_template(template_path):
    """Loads the prompt template from the specified file path."""
    try:
        with open(template_path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        print(f"ERROR: Prompt template not found at {template_path}. Please ensure the path is correct.")
        exit(1)

def call_gemini_api(prompt_text):
    """Calls the Gemini API with the given prompt text and returns parsed JSON response."""
    try:
        model = genai.GenerativeModel(
            model_name=GEMINI_MODEL_NAME,
            generation_config=generation_config,
            safety_settings=safety_settings
        )
        response = model.generate_content(prompt_text)
        
        # Check if the response contains any text content, which should be our JSON.
        if response.text:
            return json.loads(response.text)
        else:
            print("WARNING: Gemini API response was empty or did not contain text content.")
            # Print full response for debugging if it's not text
            # if response.candidates and response.candidates[0].content:
            #     print(f"Full Gemini Response Content: {response.candidates[0].content}")
            return None

    except json.JSONDecodeError as e:
        print(f"ERROR: Failed to decode JSON from Gemini response: {e}")
        print(f"Raw Gemini Response Text (first 500 chars): {response.text[:500] if hasattr(response, 'text') else 'N/A'}")
        return None
    except Exception as e:
        print(f"ERROR: An error occurred while calling Gemini API: {e}")
        # Attempt to print response content for more context
        if 'response' in locals() and hasattr(response, 'text'):
            print(f"Partial Gemini Response Text: {response.text[:500]}")
        elif 'response' in locals() and hasattr(response, 'prompt_feedback') and response.prompt_feedback.block_reason:
            print(f"Gemini API blocked response due to: {response.prompt_feedback.block_reason}")
        return None

def create_github_issue(title, body, labels, assignee, repo_name):
    """Creates a GitHub issue using the gh CLI tool."""
    labels_str = ",".join(labels)
    # The --body-file approach is more robust for longer content, but direct --body works for most cases
    # For very long bodies, consider writing to a temp file and using --body-file @temp_file
    cmd = [
        "gh", "issue", "create",
        "--title", title,
        "--body", body,
        "--label", labels_str,
        "--assignee", assignee,
        "--repo", repo_name
    ]
    try:
        print(f"Attempting to create issue: '{title}' in repository: '{repo_name}'")
        
        # Ensure GITHUB_TOKEN is available to the gh CLI command
        env_with_token = os.environ.copy()
        env_with_token["GITHUB_TOKEN"] = GITHUB_TOKEN

        process = subprocess.run(cmd, capture_output=True, text=True, check=True, env=env_with_token)
        print(f"Successfully created issue: {process.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Failed to create GitHub issue for '{title}'.")
        print(f"  Return code: {e.returncode}")
        print(f"  Stdout: {e.stdout}")
        print(f"  Stderr: {e.stderr}")
        return False
    except Exception as e:
        print(f"ERROR: An unexpected error occurred during GitHub issue creation: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Process Guild Ops and create GitHub Issues using Gemini.")
    parser.add_argument("--ops_file", required=True, help="Path to the JSON file containing Guild Ops.")
    parser.add_argument("--project_id", required=True, help="Project ID for the Guild Ops (e.g., CCG).")
    parser.add_argument("--context_label", required=True, help="Context label for the Guild Ops (e.g., Context:PERS).")
    parser.add_argument("--assignee", default="Kin-Caid", help="Default assignee for the issues.")
    parser.add_argument("--repo_name", required=True, help="GitHub repository name (e.g., owner/repo).")
    parser.add_argument("--prompt_template_path", default="scripts/prompts/issue_creation_prompt_template.txt", help="Path to the prompt template file.")
    
    args = parser.parse_args()

    # Pre-check for API keys
    if not GEMINI_API_KEY:
        print("ERROR: GEMINI_API_KEY environment variable is not set. Please configure it in your GitHub Repository Secrets.")
        return
    if not GITHUB_TOKEN:
        print("ERROR: GITHUB_TOKEN environment variable is not set. This is usually set automatically by GitHub Actions.")
        return

    try:
        with open(args.ops_file, 'r') as f:
            guild_ops_list = json.load(f)
    except FileNotFoundError:
        print(f"ERROR: Ops file not found at '{args.ops_file}'. Please ensure the path is correct and the file exists.")
        return
    except json.JSONDecodeError:
        print(f"ERROR: Could not decode JSON from '{args.ops_file}'. Please ensure it's valid JSON.")
        return

    # Construct the absolute path to the prompt template
    script_dir = Path(__file__).parent
    prompt_template_full_path = script_dir / args.prompt_template_path
    prompt_template = load_prompt_template(prompt_template_full_path)
    
    # Counter for NUM_ID generation (resets per op_type for THIS batch)
    op_type_counters = {}
    total_ops = len(guild_ops_list)
    created_count = 0

    print(f"Starting to process {total_ops} Guild Ops from {args.ops_file}...")
    print(f"Issues will be created in repository: {args.repo_name}")
    print(f"Default Assignee: {args.assignee}")
    print(f"Project ID: {args.project_id}")
    print(f"Context Label: {args.context_label}")

    # Iteratively process each Guild Op
    for i, op_details in enumerate(guild_ops_list):
        print(f"\n--- Processing Op {i+1}/{total_ops}: {op_details.get('op_title', 'N/A')} ---")

        op_type = op_details.get("op_type", "UNKNOWN").upper()
        # Increment counter for the current OP_TYPE
        op_type_counters[op_type] = op_type_counters.get(op_type, 0) + 1
        num_id = f"{op_type_counters[op_type]:03d}" # Format as 3-digit string (e.g., "001")

        # Populate the prompt template with dynamic Guild Op details
        current_prompt = prompt_template.replace("{{PROJECT_ID}}", args.project_id) \
                                        .replace("{{OP_TYPE}}", op_details.get("op_type", "N/A")) \
                                        .replace("{{OP_TYPE_UPPERCASE}}", op_details.get("op_type", "N/A").upper()) \
                                        .replace("{{OP_TYPE_LOWERCASE}}", op_details.get("op_type", "N/A").lower()) \
                                        .replace("{{OP_TITLE}}", op_details.get("op_title", "N/A")) \
                                        .replace("{{PRIMARY_DELIVERABLE}}", op_details.get("primary_deliverable", "N/A")) \
                                        .replace("{{SECTOR_NAME}}", op_details.get("sector_name", "N/A")) \
                                        .replace("{{CONTEXT_LABEL}}", args.context_label) \
                                        .replace("{{ASSIGNEE}}", args.assignee) \
                                        .replace("{{NUM_ID}}", num_id)
        
        print(f"Calling Gemini API for Op {num_id}...")
        llm_response_data = call_gemini_api(current_prompt)

        if llm_response_data and isinstance(llm_response_data, dict):
            issue_title = llm_response_data.get("issue_title")
            issue_labels = llm_response_data.get("issue_labels", [])
            issue_body = llm_response_data.get("issue_body")

            if not all([issue_title, issue_body]):
                print(f"ERROR: LLM response for '{op_details.get('op_title', 'N/A')}' was missing required fields (issue_title or issue_body). Skipping issue creation.")
                print(f"Received LLM Response Data: {llm_response_data}")
            else:
                if create_github_issue(issue_title, issue_body, issue_labels, args.assignee, args.repo_name):
                    created_count += 1
        else:
            print(f"Skipping issue creation for Op '{op_details.get('op_title', 'N/A')}' due to an invalid or empty LLM response.")

        # Respect rate limit for consecutive API calls
        if i < total_ops - 1: # Don't sleep after the last item
            print(f"Sleeping for {SLEEP_INTERVAL:.2f} seconds to respect API rate limit...")
            time.sleep(SLEEP_INTERVAL)

    print(f"\n--- Guild Op Creation Process Complete ---")
    print(f"Total Guild Ops requested: {total_ops}")
    print(f"Successfully created GitHub Issues: {created_count}")
    if created_count < total_ops:
        print(f"WARNING: Failed to create issues for {total_ops - created_count} Ops. Check logs above for specific errors.")
        print("Remember to remove successfully processed Ops from 'guild_ops_input.json' before running again to avoid duplicates.")


if __name__ == "__main__":
    main()