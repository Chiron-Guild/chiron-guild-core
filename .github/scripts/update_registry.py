# .github/scripts/update_registry.py

import json
import os
import re
from datetime import datetime
from shutil import copyfile

def extract_section(issue_body, section_name, is_single_line=False):
    """
    Extracts content from a specific markdown section.
    This version uses a more flexible and robust regex pattern.
    """
    if not issue_body:
        return "" if is_single_line else []
        
    # --- THE DEFINITIVE REGEX FIX ---
    # This pattern is much more flexible:
    #   - `##+`: Matches two or more '#' characters.
    #   - `\s*`: Matches any whitespace.
    #   - `\n?`: Makes the newline after the header optional.
    #   - `(?=\n##+|\Z)`: Stops at the next header or the end of the string.
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
    # Read all data from environment variables
    issue_number = os.getenv("ISSUE_NUMBER")
    issue_title = os.getenv("ISSUE_TITLE")
    issue_body = os.getenv("ISSUE_BODY", "")
    assignees_json_str = os.getenv("ASSIGNEES_JSON")
    issue_url = os.getenv("ISSUE_URL")
    closed_at = os.getenv("CLOSED_AT")

    if not issue_number:
        print("Error: ISSUE_NUMBER environment variable not set.")
        return

    try:
        assignees_json = json.loads(assignees_json_str) if assignees_json_str else []
        assignees = [a.get("login", "") for a in assignees_json if "login" in a]
    except Exception as e:
        print(f"Error loading assignees: {e}")
        assignees = []

    # Extract sections from the issue body using the robust function
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
