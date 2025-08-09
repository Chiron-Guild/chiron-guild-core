import re
import subprocess
import json

def get_logged_commits(registry_file="registry.md"):
    """
    Reads the registry file and extracts all logged commit SHAs.
    The SHA is expected to be the text of a markdown link pointing to the commit.
    e.g., [abc1234](https://github.com/...)
    """
    logged_shas = set()
    try:
        with open(registry_file, "r", encoding="utf-8") as f:
            content = f.read()
        # This regex finds markdown links where the link text is a 7-character hex string
        # and the URL contains '/commit/'.
        pattern = r"\[([0-9a-f]{7})\]\(https://github.com/.*/commit/\1[0-9a-f]*\)"
        matches = re.findall(pattern, content)
        logged_shas.update(matches)
    except FileNotFoundError:
        print(f"Registry file '{registry_file}' not found. Assuming no commits are logged.")
    return logged_shas

def get_recent_commits(branch="main", limit=50):
    """
    Gets a list of recent commit SHAs from the specified branch.
    Returns the short SHA (7 characters).
    """
    try:
        # Get the last 'limit' commits, formatted to just the short SHA
        result = subprocess.run(
            ["git", "log", f"--pretty=format:%h", "-n", str(limit), branch],
            capture_output=True,
            text=True,
            check=True,
        )
        return set(result.stdout.strip().split("\n"))
    except subprocess.CalledProcessError as e:
        print(f"Error getting git log: {e}")
        return set()

def main():
    """
    Compares recent commits to logged commits and prints the list of
    un-logged commits as a JSON array.
    """
    logged_commits = get_logged_commits()
    print(f"Found {len(logged_commits)} logged commits: {logged_commits}")

    recent_commits = get_recent_commits()
    print(f"Found {len(recent_commits)} recent commits: {recent_commits}")

    unlogged_commits = list(recent_commits - logged_commits)
    print(f"Found {len(unlogged_commits)} unlogged commits: {unlogged_commits}")

    # Output the list of unlogged commits as a JSON string for the GitHub Action
    print(f"::set-output name=commits::{json.dumps(unlogged_commits)}")

if __name__ == "__main__":
    main()
