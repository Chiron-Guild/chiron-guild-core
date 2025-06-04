import os
import json
import time
import argparse
import google.generativeai as genai # ### UPDATED ### - Assuming the new 'google-genai' lib keeps this import convention
from pathlib import Path

# Configuration
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
# ### UPDATED ### - Specific model as requested by user
GEMINI_MODEL_NAME = "models/gemini-1.5-flash-preview-05-20"
# ### NEW ### - Rate limits based on user's model documentation
# 10 RPM, 250k TPM, 500 RPD
# Script primarily manages RPM. TPM/RPD are operational considerations.
REQUESTS_PER_MINUTE_LIMIT = 10
SLEEP_INTERVAL = 60.0 / REQUESTS_PER_MINUTE_LIMIT

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    print("ERROR: GEMINI_API_KEY environment variable not set.")
    exit(1)

# ### UPDATED ### - Generation config might need slight tweaks if the new SDK changes defaults
# Keeping it similar for now, response_mime_type is key.
generation_config = {
    "temperature": 0.7,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 8192, # Max for 1.5 Flash is 8192 output tokens, but user's screenshot shows 65,536. Let's use 8192 as per common flash model.
    "response_mime_type": "application/json",
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

def load_prompt_template(template_path):
    try:
        with open(template_path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        print(f"ERROR: Prompt template not found at {template_path}")
        exit(1)

def call_gemini_api(prompt_text):
    try:
        model = genai.GenerativeModel(
            model_name=GEMINI_MODEL_NAME,
            generation_config=generation_config,
            safety_settings=safety_settings
        )
        print(f"Sending request to Gemini model: {GEMINI_MODEL_NAME}")
        response = model.generate_content(prompt_text)
        
        # ### UPDATED ### - Robust handling for response structure
        # The new SDK with response_mime_type="application/json" should ideally
        # make response.text directly the JSON string.
        # We retain checks for different ways the text might be structured in the response.
        raw_json_text = None
        if hasattr(response, 'text') and response.text:
            raw_json_text = response.text
        elif response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
            # Concatenate parts if response.text is not directly available
            raw_json_text = "".join([part.text for part in response.candidates[0].content.parts if hasattr(part, 'text')])
        
        if raw_json_text:
            # print(f"Raw JSON response from Gemini: {raw_json_text[:500]}...") # For debugging
            return json.loads(raw_json_text)
        else:
            print("ERROR: No text content found in Gemini response.")
            print(f"Full Gemini Response object: {response}") # Log the whole object for inspection
            return None

    except json.JSONDecodeError as e:
        print(f"ERROR: Failed to decode JSON from Gemini response: {e}")
        # Log the raw text again if it was available before JSON parsing failed
        if 'raw_json_text' in locals() and raw_json_text:
             print(f"Raw Text that failed JSON parsing: {raw_json_text}")
        else:
             print(f"Full Gemini Response (if available): {response if 'response' in locals() else 'N/A'}")
        return None
    except Exception as e:
        # Catching google.api_core.exceptions.PermissionDenied or other API errors
        print(f"ERROR: An error occurred while calling Gemini API: {type(e).__name__} - {e}")
        if hasattr(e, 'message'): print(f"Error Message: {e.message}")
        # print(f"Full Gemini Response (if available): {response if 'response' in locals() else 'N/A'}") # Might be too verbose
        return None

# --- main function remains largely the same as in the previous version ---
# It iterates, calls the updated call_gemini_api, and writes to output files.
def main():
    parser = argparse.ArgumentParser(description="Generate Guild Op brief proposals for review.")
    parser.add_argument("--ops_file", required=True, help="Path to the JSON file containing Guild Ops.")
    parser.add_argument("--project_id", required=True, help="Project ID.")
    parser.add_argument("--context_label", required=True, help="Context label.")
    parser.add_argument("--assignee", default="Kin-Caid", help="Default assignee.")
    parser.add_argument("--prompt_template_path", default="scripts/prompts/issue_creation_prompt_template.txt", help="Path to prompt template.")
    parser.add_argument("--output_json_file", default="_generated_briefs_to_create.json", help="Output JSON file for machine processing.")
    parser.add_argument("--output_md_file", default="_generated_briefs_for_review.md", help="Output Markdown file for human review.")
    
    args = parser.parse_args()

    if not GEMINI_API_KEY:
        print("ERROR: GEMINI_API_KEY environment variable is not set. Exiting.")
        return

    try:
        with open(args.ops_file, 'r') as f:
            guild_ops_list = json.load(f)
    except FileNotFoundError:
        print(f"ERROR: Ops file not found at {args.ops_file}")
        return
    except json.JSONDecodeError:
        print(f"ERROR: Could not decode JSON from {args.ops_file}")
        return

    script_dir = Path(__file__).parent
    prompt_template = load_prompt_template(script_dir / args.prompt_template_path)
    
    op_type_counters = {}
    all_generated_briefs_json = []
    all_generated_briefs_md = []

    print(f"Processing {len(guild_ops_list)} Guild Ops from {args.ops_file} for review generation using model {GEMINI_MODEL_NAME}...")

    for i, op_details in enumerate(guild_ops_list):
        print(f"\n--- Generating brief for Op {i+1}/{len(guild_ops_list)}: {op_details.get('op_title', 'N/A')} ---")

        op_type = op_details.get("op_type", "UNKNOWN").upper()
        op_type_counters[op_type] = op_type_counters.get(op_type, 0) + 1
        num_id = f"{op_type_counters[op_type]:03d}"

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
        
        # print(f"Constructed prompt:\n{current_prompt[:500]}...\n") # For debugging prompt
        llm_response_data = call_gemini_api(current_prompt)

        if llm_response_data and isinstance(llm_response_data, dict):
            generated_title = llm_response_data.get("issue_title")
            generated_labels = llm_response_data.get("issue_labels", [])
            generated_body = llm_response_data.get("issue_body")

            if not all([generated_title, generated_body]): # Labels can be empty
                print("ERROR: LLM response missing required fields (issue_title or issue_body). Skipping this Op.")
                # Create an error entry for JSON output
                error_entry = {
                    "original_op_details": op_details,
                    "llm_error": "Missing title or body from LLM response",
                    "generated_issue_title": None,
                    "generated_issue_labels": [],
                    "generated_issue_body": None,
                    "assignee": args.assignee
                }
                all_generated_briefs_json.append(error_entry)
                md_error_entry = f"## ERROR Generating Brief for: {op_details.get('op_title', 'N/A')}\n\n"
                md_error_entry += f"LLM API call returned invalid data (missing title/body). Please review logs.\n---\n"
                all_generated_briefs_md.append(md_error_entry)

            else:
                generated_brief_json_entry = {
                    "original_op_details": op_details,
                    "generated_issue_title": generated_title,
                    "generated_issue_labels": generated_labels,
                    "generated_issue_body": generated_body,
                    "assignee": args.assignee
                }
                all_generated_briefs_json.append(generated_brief_json_entry)

                md_entry = f"## Proposed Issue: {generated_title}\n\n"
                md_entry += f"**Labels:** `{', '.join(generated_labels)}`\n\n"
                md_entry += f"**Assignee:** `{args.assignee}`\n\n"
                md_entry += f"**Original Op Title:** {op_details.get('op_title', 'N/A')}\n"
                md_entry += f"**Original Deliverable:** {op_details.get('primary_deliverable', 'N/A')}\n\n"
                md_entry += "### Generated Brief Body:\n"
                md_entry += "```markdown\n"
                md_entry += f"{generated_body}\n"
                md_entry += "```\n---\n"
                all_generated_briefs_md.append(md_entry)
                print(f"Successfully generated brief for: {generated_title}")

        else:
            print(f"Skipping brief generation for Op '{op_details.get('op_title', 'N/A')}' due to LLM error or invalid response.")
            error_entry = { # Create an error entry for JSON output
                "original_op_details": op_details,
                "llm_error": "Failed to get valid response from LLM or API error",
                "generated_issue_title": None,
                "generated_issue_labels": [],
                "generated_issue_body": None,
                "assignee": args.assignee
            }
            all_generated_briefs_json.append(error_entry)
            md_error_entry = f"## ERROR Generating Brief for: {op_details.get('op_title', 'N/A')}\n\n"
            md_error_entry += f"LLM API call failed or returned invalid data. Please review logs.\n---\n"
            all_generated_briefs_md.append(md_error_entry)


        if i < len(guild_ops_list) - 1:
            print(f"Sleeping for {SLEEP_INTERVAL:.2f} seconds to respect RPM limit...")
            time.sleep(SLEEP_INTERVAL)

    output_json_path = Path(args.output_json_file)
    with open(output_json_path, 'w') as f_json:
        json.dump(all_generated_briefs_json, f_json, indent=2)
    print(f"\nGenerated JSON briefs written to: {output_json_path.resolve()}")

    output_md_path = Path(args.output_md_file)
    with open(output_md_path, 'w') as f_md:
        f_md.write(f"# Guild Op Briefs - For Review\n\nProject ID: `{args.project_id}` | Context: `{args.context_label}`\n\n")
        f_md.write("Review the following proposed GitHub Issues. If edits are needed, modify the corresponding entries in `_generated_briefs_to_create.json` before running the issue creation workflow.\n\n---\n\n")
        for entry in all_generated_briefs_md:
            f_md.write(entry)
    print(f"Generated Markdown review file written to: {output_md_path.resolve()}")

    print(f"\n--- Brief Generation Complete ---")

if __name__ == "__main__":
    main()