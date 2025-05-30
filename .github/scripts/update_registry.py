import argparse
import json
import os
import re
from datetime import datetime

def parse_args():
    parser = argparse.ArgumentParser(description="Update the operative registry from a closed issue.")
    parser.add_argument("--issue-number", required=True)
    parser.add_argument("--issue-title", required=True)
    parser.add_argument("--issue-body", required=True)
    parser.add_argument("--assignees", required=False, default="[]")
    parser.add_argument("--labels", required=False, default="[]")
    parser.add_argument("--issue-url", required=True)
    parser.add_argument("--closed-at", required=False, default="")
    return parser.parse_args()

def extract_skills_from_body(issue_body):
    # Tries to extract skills from the "Skills Demonstrated" or "Associated Skills" section
    pattern = re.compile(
        r"## (Skills Demonstrated|Associated Skills)(.*?)(?:\n## |\Z)", re.DOTALL | re.IGNORECASE
    )
    match = pattern.search(issue_body)
    skills = []
    if match:
        block = match.group(2)
        for line in block.splitlines():
            skill = line.lstrip("-•* ").strip()
            # Filter out empty lines and section dividers
            if skill and not skill.startswith("#"):
                skills.append(skill)
    return skills

def main():
    args = parse_args()

    # Parse assignees and labels safely
    try:
        assignees_json = json.loads(args.assignees) if args.assignees else []
        assignees = [a.get("login", "") for a in assignees_json if "login" in a]
    except Exception as e:
        print(f"Error loading assignees: {e}")
        assignees = []

    try:
        labels_json = json.loads(args.labels) if args.labels else []
        labels = [l.get("name", "") for l in labels_json if "name" in l]
    except Exception as e:
        print(f"Error loading labels: {e}")
        labels = []

    # Skills: extract only from issue body, not from labels
    skills = extract_skills_from_body(args.issue_body)

    # Prepare the registry entry
    entry = {
        "issue_number": int(args.issue_number),
        "issue_title": args.issue_title,
        "issue_url": args.issue_url,
        "assignees": assignees,
        "labels": labels,
        "skills": skills,
        "closed_at": args.closed_at or datetime.utcnow().isoformat() + "Z",
    }

    registry_path = os.path.join("registry", "operative_registry.json")
    if not os.path.exists("registry"):
        os.makedirs("registry")

    # Load existing registry or create new
    if os.path.isfile(registry_path):
        with open(registry_path, "r", encoding="utf-8") as f:
            try:
                registry = json.load(f)
            except Exception:
                registry = []
    else:
        registry = []

    # Remove any previous entry for this issue
    registry = [e for e in registry if e.get("issue_number") != entry["issue_number"]]
    registry.append(entry)

    # Write back
    with open(registry_path, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2, ensure_ascii=False)
    print(f"Registry updated with issue #{args.issue_number}")

if __name__ == "__main__":
    main()
