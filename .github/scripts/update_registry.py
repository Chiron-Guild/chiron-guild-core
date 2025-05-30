import argparse
import json
import os
from datetime import datetime

def get_issue_body_excerpt(issue_body, max_length=160):
    if not issue_body:
        return ""
    return (issue_body[:max_length] + "...") if len(issue_body) > max_length else issue_body

parser = argparse.ArgumentParser()
parser.add_argument('--issue-number', required=True)
parser.add_argument('--issue-title', required=True)
parser.add_argument('--issue-body', required=False, default="")
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
skills = [l for l in labels if l not in ["guild-seal"]]

# Attempt to extract deliverable links from the issue body (naive approach)
import re
def extract_links(text):
    if not text:
        return []
    # Find Markdown-style and plain URLs
    md_links = re.findall(r'\[.*?\]\((https?://[^\s)]+)\)', text)
    plain_links = re.findall(r'(https?://[^\s)]+)', text)
    # Remove duplicates and md_links already in plain_links
    all_links = list({*md_links, *plain_links})
    return all_links

deliverable_links = extract_links(args.issue_body)

for assignee in assignees:
    entry = {
        "associated_guild_op_id": assignee.get('login', ''),
        "operative_display_name": assignee.get('login', ''),
        "operative_github_profile": f"https://github.com/{assignee.get('login','')}",
        "date_issued": args.closed_at[:10],
        "project_name": "",  # To be filled manually or via convention
        "role": "",          # To be filled manually or via convention
        "skills_demonstrated": skills,
        "contribution_summary": args.issue_title,
        "issue_title": args.issue_title,
        "issue_body_excerpt": get_issue_body_excerpt(args.issue_body),
        "github_issue_url": args.issue_url,
        "pull_request_urls": [],  # Enhancement: parse PR references from body/comments
        "deliverable_links": deliverable_links,
        "compiled_context_link": "",  # Could be filled in later
        "reviewer_ids": [],           # Enhancement: fetch from API if desired
        "verification_status": "verified",
        "verification_method": "Guild Seal label, issue closed",
        "tags": skills,
        "time_spent": ""              # Could be filled in manually if tracked
    }
    registry.append(entry)

with open(registry_path, 'w') as f:
    json.dump(registry, f, indent=2)
