import argparse
import json
import os
from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument('--issue-number', required=True)
parser.add_argument('--issue-title', required=True)
parser.add_argument('--assignees', required=True)
parser.add_argument('--labels', required=True)
parser.add_argument('--issue-url', required=True)
parser.add_argument('--closed-at', required=True)
args = parser.parse_args()

registry_path = 'registry/operative_registry.json'

try:
    with open(registry_path, 'r') as f:
        registry = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    registry = []

assignees = json.loads(args.assignees)
labels = [lbl['name'] for lbl in json.loads(args.labels)]

# For demo, using only basic fields. Map these as you wish to your registry structure.
for assignee in assignees:
    entry = {
        "associated_guild_op_id": assignee['login'],
        "date_issued": args.closed_at[:10],
        "skills_demonstrated": [l for l in labels if l not in ["guild-seal"]],
        "contribution_summary": args.issue_title,
        "github_issue_url": args.issue_url,
        "deliverable_links": [],  # Could add logic to collect from issue body/comments
        "compiled_context_link": "",
        "verification_status": "verified"
    }
    registry.append(entry)

with open(registry_path, 'w') as f:
    json.dump(registry, f, indent=2)
