import os
import json
import time
import argparse
import google.generativeai as genai
from pathlib import Path

# Configuration (Keep your existing GEMINI_API_KEY, GEMINI_MODEL_NAME, rate limits)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
# ### UPDATED ### - Specific model as requested by user
GEMINI_MODEL_NAME = "gemini-2.5-flash-preview-05-20"
# ### NEW ### - Rate limits based on user's model documentation
# 10 RPM, 250k TPM, 500 RPD
# Script primarily manages RPM. TPM/RPD are operational considerations.
REQUESTS_PER_MINUTE_LIMIT = 9.5
SLEEP_INTERVAL = 60.0 / REQUESTS_PER_MINUTE_LIMIT

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    print("ERROR: GEMINI_API_KEY environment variable not set.")
    exit(1)

generation_config = {
    "temperature": 0.7,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 8192, 
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
    # (Keep your existing call_gemini_api function - it already expects JSON)
    try:
        model = genai.GenerativeModel(
            model_name=GEMINI_MODEL_NAME,
            generation_config=generation_config,
            safety_settings=safety_settings
        )
        print(f"Sending request to Gemini model: {GEMINI_MODEL_NAME}")
        response = model.generate_content(prompt_text)
        
        raw_json_text = None
        if hasattr(response, 'text') and response.text:
            raw_json_text = response.text
        elif response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
            raw_json_text = "".join([part.text for part in response.candidates[0].content.parts if hasattr(part, 'text')])
        
        if raw_json_text:
            return json.loads(raw_json_text)
        else:
            print("ERROR: No text content found in Gemini response.")
            print(f"Full Gemini Response object: {response}")
            return None
    except json.JSONDecodeError as e:
        print(f"ERROR: Failed to decode JSON from Gemini response: {e}")
        if 'raw_json_text' in locals() and raw_json_text:
             print(f"Raw Text that failed JSON parsing: {raw_json_text}")
        else:
             print(f"Full Gemini Response (if available): {response if 'response' in locals() else 'N/A'}")
        return None
    except Exception as e:
        print(f"ERROR: An error occurred while calling Gemini API: {type(e).__name__} - {e}")
        if hasattr(e, 'message'): print(f"Error Message: {e.message}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Generate Guild Op brief proposals for review.")
    parser.add_argument("--ops_file", required=True, help="Path to the JSON file containing Guild Ops.")
    parser.add_argument("--project_id", required=True, help="Project ID.")
    parser.add_argument("--context_label", required=True, help="Context label.")
    parser.add_argument("--assignee", default="Kin-Caid", help="Default assignee.")
    # --- UPDATED DEFAULT PROMPT TEMPLATE PATH ---
    parser.add_argument("--prompt_template_path", 
                        default=".github/scripts/prompts/review_generation_prompt_template.txt", 
                        help="Path to prompt template for review generation, relative to repository root.")
    parser.add_argument("--output_json_file", default="_generated_briefs_to_create.json", help="Output JSON file for machine processing.")
    parser.add_argument("--output_md_file", default="_generated_briefs_for_review.md", help="Output Markdown file for human review.")
    
    args = parser.parse_args()

    # ... (API Key check, ops_file loading - same as your provided script) ...
    if not GEMINI_API_KEY: # Duplicating check just in case
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

    prompt_template_full_path = Path(args.prompt_template_path)
    prompt_template = load_prompt_template(prompt_template_full_path)
    
    op_type_counters = {}
    all_generated_briefs_json = [] # This will now store the richer JSON
    all_generated_briefs_md_parts = [] # Store parts of MD for final assembly

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
        
        llm_response_data = call_gemini_api(current_prompt)

        # Store the raw LLM response along with original details for the JSON output
        json_entry_for_output = {
            "original_op_input_details": op_details, # Original input for this Op
            "llm_generated_data": llm_response_data, # The full JSON returned by LLM
            "generation_status": "success" if llm_response_data else "failure"
        }
        all_generated_briefs_json.append(json_entry_for_output) # Add to our list for _generated_briefs_to_create.json

        md_entry = f"## PROPOSED BRIEF FOR: {op_details.get('op_title', 'N/A')} (Input)\n\n"
        if llm_response_data and isinstance(llm_response_data, dict):
            # Extract fields for Markdown formatting
            title = llm_response_data.get("issue_title", "[MISSING TITLE FROM LLM]")
            labels = llm_response_data.get("issue_labels", [])
            assignee = llm_response_data.get("assignee", args.assignee) # Fallback to arg
            full_markdown_body = llm_response_data.get("full_markdown_body", "[MISSING MARKDOWN BODY FROM LLM]")
            scribes_notes = llm_response_data.get("scribes_generation_notes", "N/A")

            md_entry += f"### GitHub Issue Frontmatter (Proposed):\n"
            md_entry += f"```yaml\n"
            md_entry += f"title: \"{title}\"\n"
            md_entry += f"labels:\n"
            for label in labels:
                md_entry += f"  - \"{label}\"\n"
            md_entry += f"assignees:\n  - \"{assignee}\"\n"
            md_entry += f"```\n\n"
            
            md_entry += f"### Full Guild Op Brief Body (Proposed):\n"
            md_entry += f"```markdown\n"
            md_entry += f"{full_markdown_body}\n"
            md_entry += f"```\n\n"
            md_entry += f"**Scribe's Generation Notes (from LLM):** {scribes_notes}\n"
            print(f"Successfully processed and formatted brief for: {title}")

        else:
            md_entry += f"**ERROR:** Failed to generate valid brief content from LLM for this Op. Please check logs.\n"
            print(f"Skipping detailed Markdown for Op '{op_details.get('op_title', 'N/A')}' due to LLM error or invalid response.")
        
        md_entry += "---\n"
        all_generated_briefs_md_parts.append(md_entry)

        if i < len(guild_ops_list) - 1:
            print(f"Sleeping for {SLEEP_INTERVAL:.2f} seconds to respect RPM limit...")
            time.sleep(SLEEP_INTERVAL)

    # Write the JSON output file which contains the direct LLM responses
    output_json_path = Path(args.output_json_file)
    with open(output_json_path, 'w') as f_json:
        json.dump(all_generated_briefs_json, f_json, indent=2)
    print(f"\nGenerated JSON (containing LLM outputs) written to: {output_json_path.resolve()}")

    # Write the Markdown review file
    output_md_path = Path(args.output_md_file)
    with open(output_md_path, 'w') as f_md:
        f_md.write(f"# Guild Op Briefs - For Review\n\n")
        f_md.write(f"**Project ID (User Input):** `{args.project_id}` | **Context Label (User Input):** `{args.context_label}`\n\n")
        f_md.write("Review the following proposed GitHub Issues. The content below is generated by the LLM based on the `review_generation_prompt_template.txt`.\n")
        f_md.write("The accompanying `_generated_briefs_to_create.json` file contains the raw JSON structured data from the LLM.\n\n---\n\n")
        for entry in all_generated_briefs_md_parts:
            f_md.write(entry)
    print(f"Generated Markdown review file written to: {output_md_path.resolve()}")

    print(f"\n--- Brief Generation For Review Complete ---")

if __name__ == "__main__":
    main()

