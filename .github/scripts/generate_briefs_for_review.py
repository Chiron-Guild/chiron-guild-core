import os
import json
import time
import argparse
import google.generativeai as genai
from pathlib import Path

# --- Configuration ---
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
REQUESTS_PER_MINUTE_LIMIT = 9.5 
SLEEP_INTERVAL = 60.0 / REQUESTS_PER_MINUTE_LIMIT

# --- Initialize Gemini Client ---
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    print("ERROR: GEMINI_API_KEY environment variable not set. Please set it in your GitHub Repository Secrets.")
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

# --- Helper Functions ---
def load_prompt_template(template_path):
    """Loads the prompt template from the specified file path."""
    try:
        with open(template_path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        print(f"ERROR: Prompt template not found at {template_path}. Please ensure the path is correct.")
        exit(1)

def call_gemini_api(prompt_text, model_name):
    """Calls the Gemini API with the given prompt text and returns parsed JSON response."""
    try:
        model = genai.GenerativeModel(
            model_name=model_name,
            generation_config=generation_config,
            safety_settings=safety_settings
        )
        print(f"Sending request to Gemini model: {model_name}")
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

# --- Main Processing Logic ---
def main():
    parser = argparse.ArgumentParser(description="Generate Guild Op brief proposals for review.")
    parser.add_argument("--ops_file", required=True, help="Path to the JSON file containing Guild Ops (e.g., archives/input_ops.json).")
    parser.add_argument("--project_id_cli_arg", required=True, help="Overall Project ID Prefix (e.g., CCG) to use for Op IDs.")
    parser.add_argument("--context_label", required=True, help="Context label (e.g., Context:PERS).")
    parser.add_argument("--assignee", default="Kin-Caid", help="Default assignee.")
    parser.add_argument("--prompt_template_path", 
                        default=".github/scripts/prompts/review_generation_prompt_template.txt", 
                        help="Path to prompt template for review generation, relative to repository root.")
    parser.add_argument("--output_json_file", default="_generated_briefs_to_create.json", help="Output JSON file for machine processing.")
    parser.add_argument("--output_md_file", default="_generated_briefs_for_review.md", help="Output Markdown file for human review.")
    parser.add_argument("--project_mappings_file", default="project_mappings.json", help="Path to the project_mappings.json file, relative to repo root.")
    parser.add_argument("--model_name", required=True, help="The Gemini model name to use for generation.")

    args = parser.parse_args()

    if not GEMINI_API_KEY:
        print("ERROR: GEMINI_API_KEY environment variable is not set. Exiting.")
        return

    try:
        with open(args.ops_file, 'r') as f:
            project_data_from_input_ops = json.load(f) 
    except FileNotFoundError:
        print(f"ERROR: Ops file not found at {args.ops_file}")
        return
    except json.JSONDecodeError:
        print(f"ERROR: Could not decode JSON from {args.ops_file}")
        return

    project_mappings = {}
    try:
        # Construct absolute path if needed, or assume it's relative to repo root
        mappings_file_path = Path(args.project_mappings_file)
        if not mappings_file_path.is_absolute() and not Path.cwd().joinpath(mappings_file_path).exists():
             # Try relative to script if not found at repo root (for local dev flexibility)
             script_dir_path = Path(__file__).resolve().parent
             if script_dir_path.joinpath(mappings_file_path).exists():
                  mappings_file_path = script_dir_path.joinpath(mappings_file_path)
        
        if mappings_file_path.exists():
            with open(mappings_file_path, 'r') as f_map:
                project_mappings = json.load(f_map)
        else:
            print(f"WARNING: Project mappings file not found at '{args.project_mappings_file}' or alternate paths. Mappings will not be used.")
    except json.JSONDecodeError:
        print(f"WARNING: Could not decode JSON from '{args.project_mappings_file}'. Mappings will not be used.")
    except Exception as e:
        print(f"WARNING: Could not load project mappings file '{args.project_mappings_file}': {e}")


    overall_project_name_for_briefs = project_data_from_input_ops.get("project_name")
    
    # FIX #3: Correctly parse the new project_mappings.json structure
    if not overall_project_name_for_briefs:
        # Get the mapping object for the project ID, default to empty dict if not found
        project_mapping_object = project_mappings.get(args.project_id_cli_arg, {})
        # Get the 'name' from that object
        overall_project_name_for_briefs = project_mapping_object.get("name")

    if not overall_project_name_for_briefs:
        overall_project_name_for_briefs = f"Project: {args.project_id_cli_arg}"
        print(f"WARNING: Using fallback Parent Project name: '{overall_project_name_for_briefs}'. Define 'project_name' in '{args.ops_file}' or map '{args.project_id_cli_arg}' in '{args.project_mappings_file}'.")
    
    print(f"Using Overall Parent Project Name for briefs: '{overall_project_name_for_briefs}'")

    
    sector_name_lookup = {}
    if "project_sectors" in project_data_from_input_ops and isinstance(project_data_from_input_ops["project_sectors"], list):
        for sector in project_data_from_input_ops["project_sectors"]:
            if "sector_id" in sector and "sector_name" in sector:
                sector_name_lookup[sector["sector_id"]] = sector["sector_name"]
            else:
                print(f"WARNING: Sector object missing 'sector_id' or 'sector_name': {sector}")

    all_individual_ops_with_context = []
    if "guild_ops" in project_data_from_input_ops and isinstance(project_data_from_input_ops["guild_ops"], list):
        for op_detail in project_data_from_input_ops["guild_ops"]:
            op_copy = op_detail.copy()
            sector_id_from_op = op_detail.get("sector_id")
            
            if "sector_name" in op_detail:
                op_copy["sector_name_for_prompt"] = op_detail["sector_name"]
            elif sector_id_from_op is not None and sector_id_from_op in sector_name_lookup:
                op_copy["sector_name_for_prompt"] = sector_name_lookup[sector_id_from_op]
            else:
                op_copy["sector_name_for_prompt"] = "Unknown Sector (ID not found or missing)"
            
            all_individual_ops_with_context.append(op_copy)
    else:
        print(f"ERROR: The input JSON file '{args.ops_file}' does not contain a top-level 'guild_ops' list or it's not a list.")
        return
    
    if not all_individual_ops_with_context:
        print("No Guild Ops found to process in the 'guild_ops' list of the input file.")
        return

    prompt_template_full_path = Path(args.prompt_template_path)
    if not prompt_template_full_path.is_absolute() and not Path.cwd().joinpath(prompt_template_full_path).exists():
        script_dir_path = Path(__file__).resolve().parent
        if script_dir_path.joinpath(prompt_template_full_path).exists():
            prompt_template_full_path = script_dir_path.joinpath(prompt_template_full_path)

    prompt_template = load_prompt_template(prompt_template_full_path)
    
    op_type_counters = {}
    all_generated_briefs_json = []
    all_generated_briefs_md_parts = []

    print(f"Processing {len(all_individual_ops_with_context)} individual Guild Ops for review generation using model {args.model_name}...")

    for i, op_details in enumerate(all_individual_ops_with_context):
        print(f"\n--- Generating brief for Op {i+1}/{len(all_individual_ops_with_context)}: {op_details.get('op_title', 'N/A')} ---")

        op_type = op_details.get("op_type", "UNKNOWN").upper()
        op_type_counters[op_type] = op_type_counters.get(op_type, 0) + 1
        num_id = f"{op_type_counters[op_type]:03d}"

        current_prompt = prompt_template.replace("{{OVERALL_PROJECT_NAME}}", overall_project_name_for_briefs) \
                                        .replace("{{PROJECT_ID}}", args.project_id_cli_arg) \
                                        .replace("{{OP_TYPE}}", op_details.get("op_type", "N/A")) \
                                        .replace("{{OP_TYPE_UPPERCASE}}", op_details.get("op_type", "N/A").upper()) \
                                        .replace("{{OP_TYPE_LOWERCASE}}", op_details.get("op_type", "N/A").lower()) \
                                        .replace("{{OP_TITLE}}", op_details.get("op_title", "N/A")) \
                                        .replace("{{PRIMARY_DELIVERABLE}}", op_details.get("primary_deliverable", "N/A")) \
                                        .replace("{{SECTOR_NAME}}", op_details.get("sector_name_for_prompt", "N/A")) \
                                        .replace("{{CONTEXT_LABEL}}", args.context_label) \
                                        .replace("{{ASSIGNEE}}", args.assignee) \
                                        .replace("{{NUM_ID}}", num_id)
        
        llm_response_data = call_gemini_api(current_prompt, args.model_name)

        json_entry_for_output = {
            "original_op_input_details": op_details,
            "llm_generated_data": llm_response_data,
            "generation_status": "success" if llm_response_data else "failure"
        }
        all_generated_briefs_json.append(json_entry_for_output) 

        md_entry = f"## PROPOSED BRIEF FOR: {op_details.get('op_title', 'N/A')} (From Sector: {op_details.get('sector_name_for_prompt')})\n\n"
        if llm_response_data and isinstance(llm_response_data, dict):
            title = llm_response_data.get("issue_title", "[MISSING TITLE FROM LLM]")
            labels = llm_response_data.get("issue_labels", [])
            assignee = llm_response_data.get("assignee", args.assignee) 
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

        if i < len(all_individual_ops_with_context) - 1:
            print(f"Sleeping for {SLEEP_INTERVAL:.2f} seconds to respect RPM limit...")
            time.sleep(SLEEP_INTERVAL)

    output_json_path = Path(args.output_json_file)
    with open(output_json_path, 'w') as f_json:
        json.dump(all_generated_briefs_json, f_json, indent=2)
    print(f"\nGenerated JSON (containing LLM outputs) written to: {output_json_path.resolve()}")

    output_md_path = Path(args.output_md_file)
    with open(output_md_path, 'w') as f_md:
        f_md.write(f"# Guild Op Briefs - For Review\n\n")
        # --- MODIFIED: Display the overall_project_name_for_briefs ---
        f_md.write(f"**Overall Parent Project for this Batch:** `{overall_project_name_for_briefs}`\n\n")
        f_md.write(f"**Input Project ID Prefix (for Op IDs):** `{args.project_id_cli_arg}` | **Input Context Label:** `{args.context_label}`\n\n")
        f_md.write("Review the following proposed GitHub Issues. The content below is generated by the LLM based on the `review_generation_prompt_template.txt`.\n")
        f_md.write("The accompanying `_generated_briefs_to_create.json` file contains the raw JSON structured data from the LLM.\n\n---\n\n")
        for entry in all_generated_briefs_md_parts:
            f_md.write(entry)
    print(f"Generated Markdown review file written to: {output_md_path.resolve()}")

    print(f"\n--- Brief Generation For Review Complete ---")

if __name__ == "__main__":
    main()
