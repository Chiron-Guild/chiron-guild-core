import os
import re
import json
from datetime import datetime

def parse_issue_body(body):
    """
    Parses the body of a GitHub issue created from a YAML form.
    The body is a mix of markdown headers and key-value pairs.
    """
    data = {}

    # This regex is designed to find sections starting with '###'
    # and capture the text until the next '###' or the end of the string.
    sections = re.split(r'\n### ', body)

    for section in sections:
        # Split each section into a title and a body
        parts = section.split('\n\n', 1)
        if len(parts) == 2:
            key = parts[0].strip()
            value = parts[1].strip()
            data[key] = value

    return data

def format_entry(data):
    """Formats the parsed data into a markdown block."""

    title = os.getenv("ISSUE_TITLE", "")
    issue_url = os.getenv("ISSUE_URL", "")
    commit_url = os.getenv("COMMIT_URL", "")
    closed_at_str = os.getenv("CLOSED_AT", "")
    ai_summary_json = os.getenv("AI_SUMMARY", "")

    if closed_at_str:
        closed_at_dt = datetime.fromisoformat(closed_at_str.replace("Z", "+00:00"))
        closed_at_formatted = closed_at_dt.strftime("%Y-%m-%d")
    else:
        closed_at_formatted = "N/A"

    objective = data.get("Objective(s)", "Not specified")
    guild_seal = data.get("Awarded Guild Seal", "Not specified")

    entry = f"""
---
### [{title}]({issue_url})

- **Status:** Completed on {closed_at_formatted}
- **Guild Seal:** {guild_seal}
- **Objective:** {objective}
"""

    if commit_url:
        entry += f"- **Associated Commit:** [{commit_url.split('/')[-1][:7]}]({commit_url})\n"

    if ai_summary_json:
        try:
            ai_data = json.loads(ai_summary_json)
            summary = ai_data.get("summary_of_changes", "N/A")
            critique = ai_data.get("constructive_critique", "N/A")
            skills = ai_data.get("skills_demonstrated", [])

            entry += f"""
#### AI-Generated Summary of Changes
{summary}

- **Constructive Critique:** {critique}
- **Skills Demonstrated (AI):** {', '.join(skills) if skills else 'N/A'}
"""
        except json.JSONDecodeError:
            entry += "\n*AI summary was not valid JSON and could not be included.*"

    return entry + "\n"

def main():
    issue_body = os.getenv("ISSUE_BODY")
    if not issue_body:
        print("No issue body provided. Exiting.")
        return

    parsed_data = parse_issue_body(issue_body)
    markdown_entry = format_entry(parsed_data)

    registry_file = "registry.md"

    with open(registry_file, "a", encoding="utf-8") as f:
        f.write(markdown_entry)

    print(f"Successfully appended entry for issue #{os.getenv('ISSUE_NUMBER')} to {registry_file}")

if __name__ == "__main__":
    main()
