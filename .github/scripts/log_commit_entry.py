import os
import json
from datetime import datetime

def format_commit_entry():
    """Formats the commit data into a markdown block."""

    commit_sha = os.environ.get("COMMIT_SHA", "")
    commit_url = os.environ.get("COMMIT_URL", "")
    commit_message = os.environ.get("COMMIT_MESSAGE", "No commit message found.")
    ai_summary_json = os.environ.get("AI_SUMMARY", "")

    # Use the first line of the commit message as the title
    title = commit_message.splitlines()[0]

    entry = f"""
---
### Commit: [{title}]({commit_url})

- **Status:** Logged on {datetime.now().strftime("%Y-%m-%d")}
- **Commit:** [{commit_sha}]({commit_url})
"""

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
    """
    Appends the formatted commit entry to the registry file.
    """
    markdown_entry = format_commit_entry()
    registry_file = "registry.md"

    with open(registry_file, "a", encoding="utf-8") as f:
        f.write(markdown_entry)

    print(f"Successfully appended entry for commit {os.environ.get('COMMIT_SHA')} to {registry_file}")

if __name__ == "__main__":
    main()
