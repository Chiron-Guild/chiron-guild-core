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

def get_commit_datetime(sha):
    """
    Safely get commit datetime with error handling.
    
    Args:
        sha (str): The commit SHA hash
        
    Returns:
        str: ISO format datetime string, or None if failed
    """
    try:
        result = subprocess.run(
            ['git', 'show', '-s', '--format=%cI', sha],
            capture_output=True,
            text=True,
            check=True,
            timeout=30
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        print(f"Warning: Could not get datetime for commit {sha}: {e}")
        # Try alternative approach
        try:
            result = subprocess.run(
                ['git', 'log', '-1', '--format=%cI', sha],
                capture_output=True,
                text=True,
                check=True,
                timeout=30
            )
            return result.stdout.strip()
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
            return None

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

    # --- 2. Get all commits with better error handling ---
    git_log_command = [
        'git', 'log', f'--author={args.operative_name}',
        '--pretty=format:%H||%s||%b%x00', '--reverse'
    ]
    
    try:
        result = subprocess.run(
            git_log_command, 
            capture_output=True, 
            text=True, 
            check=True,
            timeout=60
        )
        commits = [line for line in result.stdout.strip().split('\x00') if line.strip()]
        print(f"Found {len(commits)} total commits by {args.operative_name}.")
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        print(f"ERROR: Failed to get git log: {e}")
        sys.exit(1)

    # --- 3. Initialize model (removed duplicate) ---
    model = initialize_model(args.model_name)
    if not model:
        sys.exit(1)

    # --- 4. Process each commit ---
    new_tasks_added = 0
    skipped_commits = 0
    
    for i, commit_line in enumerate(commits):
        if new_tasks_added > 0:
            print(f"Sleeping for {sleep_interval}s...")
            time.sleep(sleep_interval)
            
        try:
            commit_line = commit_line.strip()
            if not commit_line:
                continue
                
            parts = commit_line.split('||', 2)
            if len(parts) >= 2:
                sha = parts[0].strip()
                subject = parts[1].strip()
                body = parts[2].strip() if len(parts) > 2 else ""
            else:
                print(f"Warning: Malformed commit line: {commit_line[:100]}...")
                skipped_commits += 1
                continue

            # Validate SHA format
            if not sha or len(sha) < 8:
                print(f"Warning: Invalid SHA format: {sha}")
                skipped_commits += 1
                continue

            commit_message = f"{subject}\n\n{body}".strip()
            commit_id_short = sha[:8]

            if commit_id_short in existing_ids:
                print(f"Skipping existing commit: {commit_id_short}")
                continue

            print(f"\n--- Processing commit {i+1}/{len(commits)}: {commit_id_short} ---")
            commit_url = f"{args.repo_url}/commit/{sha}"

            # Get commit datetime with error handling
            commit_datetime = get_commit_datetime(sha)
            if not commit_datetime:
                print(f"Warning: Could not get datetime for {commit_id_short}, using current time")
                from datetime import datetime
                commit_datetime = datetime.now().isoformat()

            # Get enrichment data
            enrichment = get_enrichment_data(model, commit_url, commit_message)
            if not enrichment:
                print(f"Skipping commit {commit_id_short} due to enrichment failure.")
                skipped_commits += 1
                continue

            new_task = {
                "task_id": commit_id_short,
                "task_title": subject,
                "completion_date": commit_datetime,
                "operative": args.operative_name,
                "deliverable_url": commit_url,
                "provenance_type": enrichment.get("provenance_type"),
                "objective": enrichment.get('objective'),
                "summary_of_changes": enrichment.get('summary_of_changes'),
                "critique": (
                    enrichment.get('annotations', [{}])[0].get('comment') if 
                    enrichment.get('annotations') else enrichment.get('constructive_critique')
                ),
                "task_category": enrichment.get('task_category'),
                "task_type": enrichment.get('task_type'),
                "skills_demonstrated": enrichment.get('skills_demonstrated')
            }
            
            registry_data['tasks'].append(new_task)
            existing_ids.add(commit_id_short)
            new_tasks_added += 1
            print(f"Successfully enriched and added task {commit_id_short}.")

        except (ValueError, api_exceptions.GoogleAPICallError) as e:
            print(f"Skipping commit due to processing error: {e}")
            skipped_commits += 1
            continue
        except Exception as e:
            print(f"Unexpected error processing commit: {e}")
            skipped_commits += 1
            continue

    # --- 5. Write final registry ---
    if new_tasks_added > 0:
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(args.registry_file), exist_ok=True)
            
            with open(args.registry_file, 'w', encoding='utf-8') as f:
                json.dump(registry_data, f, indent=2)
            print(f"\nSUCCESS: Added {new_tasks_added} new tasks to the registry.")
        except IOError as e:
            print(f"ERROR: Failed to write registry file: {e}")
            sys.exit(1)
    else:
        print("\nSUCCESS: No new tasks found to add.")
    
    if skipped_commits > 0:
        print(f"INFO: Skipped {skipped_commits} commits due to errors.")


if __name__ == "__main__":
    main()