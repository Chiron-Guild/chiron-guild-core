# .github/scripts/rapid_log_processor.py
#
# Chiron Guild: Rapid Log Processor
# Version: 1.1 (Gemini Integration)
#
# This script is the "brain" of the Rapid Logging Protocol. It is triggered by a GitHub Action
# when a "Rapid Log" issue is created. It uses Google Gemini via LangChain for classification.

import os
import json
import re
from datetime import datetime, timezone

# --- MODIFICATION: Import the correct LangChain integration ---
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser

# --- Configuration: File Paths (Unchanged) ---
REGISTRY_PATH = "_Admin & Core Docs/registry/operative_registry.json"
TAXONOMY_PATH = "taxonomy_framework.md"
MAPPINGS_PATH = "project_mappings.json"
NEW_OP_ID_PATH = "new_op_id.txt"

# --- Pydantic Model for Structured LLM Output (Unchanged) ---
class TaskClassification(BaseModel):
    """Defines the structured output for the LLM's classification."""
    project_id_prefix: str = Field(description="The most appropriate Project Prefix from the provided list.")
    op_type: str = Field(description="The most appropriate Operation Type from the provided list.")

# --- Helper Functions (Unchanged) ---
def parse_issue_body(body: str) -> tuple[str, str]:
    """
    Extracts the task description and deliverable URL from the GitHub issue body.
    """
    try:
        description_match = re.search(r"### Task Description\s*\n\n(.*?)\s*\n\n### Deliverable URL", body, re.DOTALL)
        url_match = re.search(r"### Deliverable URL\s*\n\n(.*?)$", body, re.DOTALL)
        description = description_match.group(1).strip() if description_match else ""
        url = url_match.group(1).strip() if url_match else ""
        if not description or not url:
            raise ValueError("Could not parse description or URL from issue body.")
        return description, url
    except Exception as e:
        print(f"Error parsing issue body: {e}")
        exit(1)

def load_context_files() -> tuple[str, list[str]]:
    """
    Loads the taxonomy framework for context and project prefixes for validation.
    """
    try:
        with open(TAXONOMY_PATH, 'r', encoding='utf-8') as f:
            taxonomy_context = f.read()
        with open(MAPPINGS_PATH, 'r', encoding='utf-8') as f:
            project_mappings = json.load(f)
            project_prefixes = list(project_mappings.keys())
        return taxonomy_context, project_prefixes
    except FileNotFoundError as e:
        print(f"Error: Required context file not found: {e.filename}")
        exit(1)

def generate_new_op_id(registry_data: list, prefix: str) -> tuple[int, str]:
    """
    Generates the next sequential numeric ID for a given project prefix.
    """
    id_pattern = re.compile(rf"\[{re.escape(prefix)}-[A-Z]+-(\d+)\]")
    max_id = 0
    for entry in registry_data:
        title = entry.get("issue_title", "")
        match = id_pattern.match(title)
        if match:
            current_id = int(match.group(1))
            if current_id > max_id:
                max_id = current_id
    new_numeric_id = max_id + 1
    formatted_id = f"{new_numeric_id:03d}"
    return new_numeric_id, formatted_id


# --- Main Execution Logic ---
def main():
    """Main script execution."""
    print("--- Starting Rapid Log Protocol Processor (Gemini Engine) ---")

    # 1. Ingest Data from Environment Variables
    issue_title = os.environ.get("ISSUE_TITLE")
    issue_body = os.environ.get("ISSUE_BODY")
    issue_url = os.environ.get("ISSUE_URL")
    # --- MODIFICATION: Use the new secret ---
    google_api_key = os.environ.get("GEMINI_API_KEY")

    if not all([issue_title, issue_body, issue_url, google_api_key]):
        print("Error: Missing one or more required environment variables.")
        exit(1)

    op_name_cleaned = re.sub(r"\[RAPID LOG\]\s*", "", issue_title, flags=re.IGNORECASE).strip()
    print(f"Processing Task: {op_name_cleaned}")

    # 2. Parse Inputs
    task_description, deliverable_url = parse_issue_body(issue_body)
    print("Successfully parsed task description and deliverable URL.")

    # 3. Load Guild Context
    taxonomy_context, project_prefixes = load_context_files()
    print(f"Loaded Guild Context. Valid prefixes: {project_prefixes}")

    # 4. Build and Execute LangChain Classification Chain with Gemini
    print("Initiating Gemini LLM classification...")
    parser = JsonOutputParser(pydantic_object=TaskClassification)

    prompt = ChatPromptTemplate.from_messages([
        # Gemini handles system prompts differently. We combine it into the human message.
        ("human", """
        You are a hyper-competent AI assistant for the Chiron Guild, tasked with classifying completed work.
        Your job is to analyze a task description and determine its Project Prefix and Operation Type based on the Guild's official taxonomy and project list.
        You MUST choose from the provided lists. Do not invent new categories.

        **Taxonomy & Project Context:**
        ---
        {taxonomy_context}
        ---

        **Valid Project Prefixes:**
        {project_prefixes}

        **Instructions:**
        Analyze the following task description and respond ONLY with a valid JSON object matching the requested format.

        **Task Description:**
        ---
        {task_description}
        ---

        **JSON Output Format:**
        {format_instructions}
        """)
    ])
    
    # --- MODIFICATION: Instantiate ChatGoogleGenerativeAI instead of ChatOpenAI ---
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-preview-05-20",  
        google_api_key=google_api_key,
        temperature=0,
        convert_system_message_to_human=True # Important for models that don't have a native system role
    )
    
    chain = prompt | llm | parser

    try:
        classification = chain.invoke({
            "taxonomy_context": taxonomy_context,
            "project_prefixes": ", ".join(project_prefixes),
            "task_description": task_description,
            "format_instructions": parser.get_format_instructions(),
        })
        prefix = classification['project_id_prefix']
        op_type = classification['op_type']
        print(f"Gemini Classification successful: Prefix='{prefix}', Type='{op_type}'")
    except Exception as e:
        print(f"Error during Gemini LLM classification: {e}")
        exit(1)

    # 5. Load Registry and Generate New Op ID (Unchanged)
    try:
        with open(REGISTRY_PATH, 'r', encoding='utf-8') as f:
            registry_data = json.load(f)
    except FileNotFoundError:
        registry_data = []
    
    _, numeric_id_str = generate_new_op_id(registry_data, prefix)
    op_id = f"{prefix}-{op_type}-{numeric_id_str}"
    full_op_title = f"[{op_id}] {op_name_cleaned}"
    print(f"Generated new Guild Op ID: {op_id}")

    # 6. Assemble Full Registry Entry (Unchanged)
    new_entry = {
        "issue_number": int(issue_url.split('/')[-1]),
        "issue_title": full_op_title,
        "issue_url": issue_url,
        "assignees": ["Kin-Caid"],
        "Objective": task_description,
        "Deliverables": [deliverable_url],
        "skills": [],
        "Estimated Effort": "N/A (Rapid Log)",
        "Acceptance Criteria": [],
        "Awarded Guild Seal": "",
        "closed_at": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
    }
    print("Assembled new registry entry.")

    # 7. Update the Registry File (Unchanged)
    registry_data.insert(0, new_entry)
    try:
        with open(REGISTRY_PATH, 'w', encoding='utf-8') as f:
            json.dump(registry_data, f, indent=2)
        print(f"Successfully updated '{REGISTRY_PATH}'.")
    except Exception as e:
        print(f"Error writing to registry file: {e}")
        exit(1)

    # 8. Write the new Op ID for the GitHub Action to use (Unchanged)
    with open(NEW_OP_ID_PATH, 'w') as f:
        f.write(op_id)
    print(f"Wrote new Op ID to '{NEW_OP_ID_PATH}' for workflow handoff.")
    
    print("--- Rapid Log Protocol Processor Finished ---")

if __name__ == "__main__":
    main()
