# .github/scripts/update_registry.py

import json
import os
import re
from datetime import datetime
from shutil import copyfile

def extract_section(issue_body, section_name, is_single_line=False):
    if not issue_body:
        return "" if is_single_line else []
    
    pattern = re.compile(
        rf"^##+\s*{section_name}[:\s]*\n?(.*?)(?=\n##+|\Z)",
        re.DOTALL | re.IGNORECASE | re.MULTILINE
    )
    match = pattern.search(issue_body)

    if not match:
        return "" if is_single_line else []

    block = match.group(1).strip()
    
    if is_single_line:
        return " ".join([line.lstrip("-•* ").strip() for line in block.splitlines() if line.strip()])
    
    return [line.lstrip("-•* ").strip() for line in block.splitlines() if line.strip()]

def main():
    # Read the entire issue payload from a single environment variable
    payload_str = os.getenv("ISSUE_PAYLOAD")
    if not payload_str:
        print("Error: ISSUE_PAYLOAD environment variable not set.")
        return
    
    try:
        issue = json.loads(payload_str)
    except json.JSONDecodeError:
        print("Error: Could not decode ISSUE_PAYLOAD JSON.")
        return

    # Extract all data from the parsed issue object
    issue_number = issue.get("number")
    issue_title = issue.get("title", "")
    issue_body = issue.get("body", "")
    assignees_list = issue.get("assignees", [])
    issue_url = issue.get("html_url", "")
    closed_at = issue.get("closed_at", "")

        # --- START OF DIAGNOSTIC PRINT ---
    print("--- GROUND TRUTH: Raw 'issue_body' variable ---")
    print(repr(issue_body))
    print("--- END OF GROUND TRUTH ---")
    # --- END OF DIAGNOSTIC PRINT ---
    
    assignees = [a.get("login", "") for a in assignees_list if a]

    # Extract sections from the issue body
    skills = extract_section(issue_body, "Skills Required|Skills Demonstrated|Associated Skills")
    objective = extract_section(issue_body, "Objective", is_single_line=True)
    deliverables = extract_section(issue_body, "Deliverables")
    awarded_guild_seal = extract_section(issue_body, "Awarded Guild Seal", is_single_line=True)
    estimated_effort = extract_section(issue_body, "Estimated Effort", is_single_line=True)
    acceptance_criteria = extract_section(issue_body, "Acceptance Criteria|Verification/Acceptance Criteria")

    # Prepare the registry entry
    entry = {
        "issue_number": int(issue_number),
        "issue_title": issue_title,
        "issue_url": issue_url,
        "assignees": assignees,
        "Objective": objective,
        "Deliverables": deliverables,
        "skills": skills,
        "Estimated Effort": estimated_effort,
        "Acceptance Criteria": acceptance_criteria,
        "Awarded Guild Seal": awarded_guild_seal,
        "closed_at": closed_at or datetime.utcnow().isoformat() + "Z",
    }

    registry_path = os.path.join("_Admin & Core Docs", "registry", "operative_registry.json")
    registry_dir = os.path.dirname(registry_path)
    if not os.path.exists(registry_dir):
        os.makedirs(registry_dir)

    # Load existing registry
    registry = []
    if os.path.isfile(registry_path):
        with open(registry_path, "r", encoding="utf-8") as f:
            try:
                registry = json.load(f)
            except json.JSONDecodeError:
                print(f"Warning: Could not decode JSON from {registry_path}. Starting fresh.")
                registry = []

    # Update or add the entry
    registry = [e for e in registry if e.get("issue_number") != entry["issue_number"]]
    registry.append(entry)
    registry.sort(key=lambda x: x["issue_number"], reverse=True)

    # Write back to the file
    with open(registry_path, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2, ensure_ascii=False)
    
    print(f"Registry successfully updated for issue #{issue_number}")

if __name__ == "__main__":
    main()
