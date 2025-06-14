# .github/scripts/rapid_log_processor.py
#
# Chiron Guild: Rapid Log Processor
# Version: 1.2 (AI-Augmented)
#
# This hybrid script uses deterministic user input for classification (Prefix, Type)
# and a generative LLM (Gemini) to expand a simple description into a rich,
# structured entry for the Reputation Matrix.

import os
import json
import re
from datetime import datetime, timezone

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser
from typing import List

# --- Configuration: File Paths ---
REGISTRY_PATH = "_Admin & Core Docs/registry/operative_registry.json"
NEW_OP_ID_PATH = "new_op_id.txt"

# --- Pydantic Model for Structured LLM Generation ---
class InferredOpDetails(BaseModel):
    """Defines the structured output for the LLM's generation task."""
    objective: str = Field(description="A formal, single-paragraph objective statement rewritten from the user's task description.")
    deliverables: List[str] = Field(description="A list of 1-3 specific, tangible outputs or results. The provided Deliverable URL should be the primary deliverable.")
    skills: List[str] = Field(description="A list of 3-5 professional skills demonstrated by completing this task.")
    estimated_effort: str = Field(description="An estimate of the effort using a T-shirt size scale: X-Small (<1 hour), Small (1-3 hours), Medium (4-8 hours), Large (8-16 hours), X-Large (16+ hours).")
    acceptance_criteria: List[str] = Field(description="A list of 2-4 verifiable criteria that prove the task is complete, written in the format '[ ] A task is complete when...'.")

# --- Helper Functions (parse_issue_body and generate_new_op_id are from previous version) ---
def parse_issue_body_with_dropdowns(body: str) -> dict:
    parsed_data = {}
    pattern = re.compile(r"###\s*(?P<key>.*?)\s*\n\n(?P<value>.*?)(?=\n###|\Z)", re.DOTALL)
    for match in pattern.finditer(body):
        key = match.group('key').strip().lower().replace(' ', '_')
        value = match.group('value').strip()
        parsed_data[key] = value
    key_mapping = {'project_prefix': 'project_prefix', 'operation_type': 'op_type', 'task_description': 'task_description', 'deliverable_url': 'deliverable_url'}
    standardized_data = {}
    for raw_key, value in parsed_data.items():
        for standard_key, map_val in key_mapping.items():
             if standard_key in raw_key:
                  standardized_data[map_val] = value
                  break
    return standardized_data

def generate_new_op_id(registry_data: list, prefix: str) -> tuple[int, str]:
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
    print("--- Starting Rapid Log Protocol Processor (v1.2 AI-Augmented) ---")

    # 1. Ingest and Parse Deterministic Data
    issue_title = os.environ.get("ISSUE_TITLE")
    issue_body = os.environ.get("ISSUE_BODY")
    issue_url = os.environ.get("ISSUE_URL")
    google_api_key = os.environ.get("GOOGLE_API_KEY")

    if not all([issue_title, issue_body, issue_url, google_api_key]):
        print("Error: Missing one or more required environment variables.")
        exit(1)

    op_name_cleaned = re.sub(r"\[RAPID LOG\]\s*", "", issue_title, flags=re.IGNORECASE).strip()
    form_data = parse_issue_body_with_dropdowns(issue_body)
    prefix = form_data.get('project_prefix')
    op_type = form_data.get('op_type')
    task_description = form_data.get('task_description')
    deliverable_url = form_data.get('deliverable_url')

    if not all([prefix, op_type, task_description, deliverable_url]):
        print(f"Error: Could not parse all required fields from issue body. Data: {form_data}")
        exit(1)
        
    print(f"Parsed data successfully: Prefix='{prefix}', Type='{op_type}'")

    # 2. Generate New Op ID (Done early for use in commit message)
    try:
        with open(REGISTRY_PATH, 'r', encoding='utf-8') as f:
            registry_data = json.load(f)
    except FileNotFoundError:
        registry_data = []
    
    _, numeric_id_str = generate_new_op_id(registry_data, prefix)
    op_id = f"{prefix}-{op_type}-{numeric_id_str}"
    full_op_title = f"[{op_id}] {op_name_cleaned}"
    print(f"Generated new Guild Op ID: {op_id}")

    # 3. Use LLM to Generate Rich Details
    print("Initiating Gemini LLM to generate rich details...")
    parser = JsonOutputParser(pydantic_object=InferredOpDetails)

    prompt = ChatPromptTemplate.from_messages([
        ("human", """
        You are a meticulous Guild Scribe AI. Your task is to expand a brief task description from an Operative into a formal, structured entry for our Reputation Matrix.
        Use the provided information to generate a comprehensive JSON object.

        **Operative's Input:**
        - Task Description: "{task_description}"
        - Primary Deliverable URL: "{deliverable_url}"

        **Your Instructions:**
        1.  **Objective:** Rewrite the user's description into a formal, single-paragraph objective statement.
        2.  **Deliverables:** List the specific, tangible outputs. The provided URL is always the primary deliverable. Infer any others from the description.
        3.  **Skills:** Infer a list of 3-5 professional skills demonstrated by this work.
        4.  **Estimated Effort:** Estimate the effort using this T-shirt scale: X-Small, Small, Medium, Large, X-Large.
        5.  **Acceptance Criteria:** Create a list of verifiable criteria that prove the task is complete.

        Respond ONLY with a valid JSON object matching the requested format.
        **JSON Output Format:**
        {format_instructions}
        """)
    ])
    
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-preview-05-20", google_api_key=google_api_key, temperature=0.5, convert_system_message_to_human=True)
    chain = prompt | llm | parser

    try:
        inferred_details = chain.invoke({
            "task_description": task_description,
            "deliverable_url": deliverable_url,
            "format_instructions": parser.get_format_instructions(),
        })
        print("Gemini successfully generated rich details.")
    except Exception as e:
        print(f"Error during Gemini LLM generation: {e}")
        # Fallback to a basic entry if AI fails
        inferred_details = {
            "objective": task_description,
            "deliverables": [deliverable_url],
            "skills": ["Error: AI generation failed"],
            "estimated_effort": "N/A",
            "acceptance_criteria": ["[ ] Task is logged."]
        }

    # 4. Assemble Final Registry Entry
    new_entry = {
        "issue_number": int(issue_url.split('/')[-1]),
        "issue_title": full_op_title,
        "issue_url": issue_url,
        "assignees": ["Kin-Caid"],
        "Objective": inferred_details['objective'],
        "Deliverables": inferred_details['deliverables'],
        "skills": inferred_details['skills'],
        "Estimated Effort": inferred_details['estimated_effort'],
        "Acceptance Criteria": inferred_details['acceptance_criteria'],
        "Awarded Guild Seal": "",
        "closed_at": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
    }
    print("Assembled new registry entry with AI-augmented details.")

    # 5. Update the Registry File and Handoff File
    registry_data.insert(0, new_entry)
    with open(REGISTRY_PATH, 'w', encoding='utf-8') as f:
        json.dump(registry_data, f, indent=2)
    print(f"Successfully updated '{REGISTRY_PATH}'.")

    with open(NEW_OP_ID_PATH, 'w') as f:
        f.write(op_id)
    print(f"Wrote new Op ID to '{NEW_OP_ID_PATH}' for workflow handoff.")
    
    print("--- Rapid Log Protocol Processor Finished ---")

if __name__ == "__main__":
    main()
