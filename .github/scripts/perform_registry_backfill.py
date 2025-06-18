"""
This script performs a one-time backfill of the operative registry by
iterating through the Git history, enriching each new commit with AI-generated
data, and compiling a new registry file.
"""
import json
import os
import time
import subprocess
import argparse
import sys

# We import the functions from our now-standardized enrichment script.
from enrich_task_entry import initialize_model, get_enrichment_data
from google.api_core import exceptions as api_exceptions

def main():
    """Main function to orchestrate the backfill process."""
    parser = argparse.ArgumentParser(
        description="Backfill the operative registry from Git history."
    )
    parser.add_argument(
        "--operative-name",
        required=True,
        help="The Git author name to filter commits by."
    )
    parser.add_argument(
        "--repo-url",
        required=True,
        help="The full URL of the GitHub repository."
    )
    parser.add_argument(
        "--registry-file",
        required=True,
        help="Path to the operative registry JSON file."
    )
    parser.add_argument(
        "--model-name",
        default='gemini-2.0-flash',
        help="The Gemini model to use for enrichment."
    )
    args = parser.parse_args()

    sleep_interval = 5

    # --- 1. Load existing registry ---
    if os.path.exists(args.registry_file) and os.path.getsize(args.registry_file) > 0:
        try:
            with open(args.registry_file, 'r', encoding='utf-8') as f:
                registry_data = json.load(f)
            if 'tasks' not in registry_data:
                registry_data['tasks'] = []
        except json.JSONDecodeError:
            print(f"Warning: Could not decode {args.registry_file}. Starting fresh.")
            registry_data = {"tasks": []}
    else:
        registry_data = {"tasks": []}

    existing_ids = {task['task_id'] for task in registry_data.get('tasks', [])}
    print(f"Found {len(existing_ids)} existing tasks.")

    # --- 2. Get all commits ---
    git_log_command = [
        'git', 'log', f'--author={args.operative_name}',
        '--pretty=format:%H||%s||%b', '--reverse'
    ]
    result = subprocess.run(
        git_log_command, capture_output=True, text=True, check=True
    )
    commits = result.stdout.strip().split('\n')
    print(f"Found {len(commits)} total commits by {args.operative_name}.")

    # --- 3. Initialize model ---
    model = initialize_model(args.model_name)
    if not model:
        sys.exit(1)

    # --- 4. Process each commit ---
    new_tasks_added = 0
    for commit_line in commits:
        if new_tasks_added > 0:  # Don't sleep on the first iteration
            print(f"Sleeping for {sleep_interval}s...")
            time.sleep(sleep_interval)
        try:
            sha, subject, body = commit_line.split('||', 2)
            commit_message = f"{subject}\n\n{body}".strip()
            commit_id_short = sha[:8]

            if commit_id_short in existing_ids:
                continue

            print(f"\n--- Processing new commit: {commit_id_short} ---")
            commit_url = f"{args.repo_url}/commit/{sha}"

            enrichment = get_enrichment_data(model, commit_url, commit_message)
            if not enrichment:
                print(f"Skipping commit {commit_id_short} due to enrichment failure.")
                continue

            commit_datetime = subprocess.check_output(
                ['git', 'show', '-s', '--format=%cI', sha], text=True
            ).strip()

            new_task = {
                "task_id": commit_id_short,
                "task_title": subject,
                "completion_date": commit_datetime,
                "operative": args.operative_name,
                "deliverable_url": commit_url,
                "provenance_type": enrichment.get("provenance_type"),
                "objective": enrichment.get('objective'),
                "summary_of_changes": enrichment.get('summary_of_changes'),
                "critique": (enrichment.get('annotations', [{}])[0].get('comment')),
                "task_category": enrichment.get('task_category'),
                "task_type": enrichment.get('task_type'),
                "skills_demonstrated": enrichment.get('skills_demonstrated')
            }
            registry_data['tasks'].append(new_task)
            existing_ids.add(commit_id_short)
            new_tasks_added += 1
            print(f"Successfully enriched and added task {commit_id_short}.")

        except (subprocess.CalledProcessError, ValueError, api_exceptions.GoogleAPICallError) as e:
            print(f"Skipping commit line due to processing error: {e}")
            continue

    # --- 5. Write final registry ---
    if new_tasks_added > 0:
        with open(args.registry_file, 'w', encoding='utf-8') as f:
            json.dump(registry_data, f, indent=2)
        print(f"\nSUCCESS: Added {new_tasks_added} new tasks to the registry.")
    else:
        print("\nSUCCESS: No new tasks found to add.")


if __name__ == "__main__":
    main()