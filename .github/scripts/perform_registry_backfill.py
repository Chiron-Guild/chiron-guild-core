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
from datetime import timezone

# Assuming enrich_task_entry is in the same directory or accessible
from enrich_task_entry import initialize_model, get_enrichment_data

def main():
    """Main function to orchestrate the backfill process."""
    parser = argparse.ArgumentParser(description="Backfill the operative registry from Git history.")
    parser.add_argument("--operative-name", required=True, help="The Git author name to filter commits by.")
    parser.add_argument("--repo-url", required=True, help="The full URL of the GitHub repository.")
    parser.add_argument("--registry-file", required=True, help="Path to the operative registry JSON file.")
    args = parser.parse_args()

    # --- CONFIG ---
    sleep_interval = 5  # Safe sleep for 15 RPM limit of Gemini 2.0 Flash

    # --- 1. Load existing registry ---
    if os.path.exists(args.registry_file):
        with open(args.registry_file, 'r', encoding='utf-8') as f:
            registry_data = json.load(f)
    else:
        registry_data = {"tasks": []}
    
    existing_ids = {task['task_id'] for task in registry_data.get('tasks', [])}
    print(f"Found {len(existing_ids)} existing tasks.")

    # --- 2. Get all commits by the target operative ---
    git_log_command = [
        'git', 'log',
        f'--author={args.operative_name}',
        '--pretty=format:%H||%s||%b', # SHA||subject||body
        '--reverse' # Start from the oldest commit
    ]
    result = subprocess.run(git_log_command, capture_output=True, text=True, check=True)
    commits = result.stdout.strip().split('\n')
    print(f"Found {len(commits)} total commits by {args.operative_name}. Processing new ones...")

    # --- 3. Initialize model ---
    model = initialize_model()
    if not model:
        print("Failed to initialize Gemini model. Exiting.")
        exit(1)

    # --- 4. Process each commit ---
    new_tasks_added = 0
    for commit_line in commits:
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

            # Create the new task entry
            commit_datetime = subprocess.check_output(
                ['git', 'show', '-s', '--format=%cI', sha]
            ).decode('utf-8').strip()

            new_task = {
                "task_id": commit_id_short,
                "task_title": subject,
                "task_category": "CORE", # Default category for backfill
                "task_type": "DEV",    # Default type for backfill
                "status": "Completed",
                "operative": args.operative_name,
                "completion_date": commit_datetime,
                "deliverable_url": commit_url,
                "ai_generated_objective": enrichment.get('objective'),
                "ai_summary_of_changes": enrichment.get('summary_of_changes'),
                "ai_critique": enrichment.get('constructive_critique')
            }
            registry_data['tasks'].append(new_task)
            existing_ids.add(commit_id_short)
            new_tasks_added += 1

            print(f"Enriched and added task {commit_id_short}. Sleeping for {sleep_interval}s...")
            time.sleep(sleep_interval)

        except Exception as e:
            print(f"Skipping commit line '{commit_line[:50]}...' due to processing error: {e}")
            continue

    # --- 5. Write final registry ---
    if new_tasks_added > 0:
        with open(args.registry_file, 'w', encoding='utf-8') as f:
            json.dump(registry_data, f, indent=2)
        print(f"\nSUCCESS: Added {new_tasks_added} new, enriched tasks to the registry.")
    else:
        print("\nSUCCESS: No new tasks found to add.")

if __name__ == "__main__":
    main()