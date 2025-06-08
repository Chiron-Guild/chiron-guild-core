# .github/scripts/update_registry.py

import json
import os
import re
from datetime import datetime
from shutil import copyfile

def extract_section(issue_body, section_name, is_single_line=False):
    """
    Extracts content from a specific markdown section.
    This version uses a flexible regex that accounts for optional markdown bolding.
    """
    if not issue_body:
        return "" if is_single_line else []
        
    # --- THE DEFINITIVE REGEX FIX ---
    # This pattern now handles optional bolding (e.g., **Skills Required**) around the section name.
    # `(?:\*\*)?` is a non-capturing group for an optional, escaped `**`.
    pattern = re.compile(
        rf"^##+\s*(?:\*\*)?({section_name})(?:\*\*)?[:\s]*\n?(.*?)(?=\n##+|\Z)",
        re.DOTALL | re.IGNORECASE | re.MULTILINE
    )
    # --- END OF FIX ---

    match = pattern.search(issue_body)

    if not match:
        return "" if is_single_line else []

    # We now use group(2) because the section_name itself is in the first capture group
    block = match.group(2).strip()
    
    if is_single_line:
        return " ".join([line.lstrip("-•* ").strip() for line in block.splitlines() if line.strip()])
    
    return [line.lstrip("-•* ").strip() for line in block.splitlines() if line.strip()]

def main():
    payload_str = os.getenv("ISSUE_PAYLOAD")
    if not payload_str:
        print("Error: ISSUE_PAYLOAD environment variable not set.")
        return
    
    try:
        issue = json.loads(payload_str)
    except json.JSONDecodeError:
        print("Error: Could not decode ISSUE_PAYLOAD JSON.")
        return

    issue_number = issue.get("number")
    issue_title = issue.get("title", "")
    issue_body = issue.get("body", "")
    assignees_list = issue.get("assignees", [])
    issue_url = issue.get("html_url", "")
    closed_at = issue.get("closed_at", "")

    assignees = [a.get("login", "") for a in assignees_list if a]

    # The issue_body is now parsed correctly by the robust extract_section function
    skills = extract_section(issue_body, "Skills|Skills Required|Skills Demonstrated|Associated Skills")
    objective = extract_section(issue_body, "Objective", is_single_line=True)
    deliverables = extract_section(issue_body, "Deliverables")
    awarded_guild_seal = extract_section(issue_body, "Awarded Guild Seal", is_single_line=True)
    estimated_effort = extract_section(issue_body, "Estimated Effort", is_single_line=True)
    acceptance_criteria = extract_section(issue_body, "Acceptance Criteria|Verification/Acceptance Criteria")

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

    registry = []
    if os.path.isfile(registry_path):
        with open(registry_path, "r", encoding="utf-8") as f:
            try:
                registry = json.load(f)
            except json.JSONDecodeError:
                print(f"Warning: Could not decode JSON from {registry_path}. Starting fresh.")
                registry = []

    registry = [e for e in registry if e.get("issue_number") != entry["issue_number"]]
    registry.append(entry)
    registry.sort(key=lambda x: x["issue_number"], reverse=True)

    with open(registry_path, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2, ensure_ascii=False)
    
    print(f"Registry successfully updated for issue #{issue_number}")

if __name__ == "__main__":
    main()
