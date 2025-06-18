"""
This script performs a targeted A/B test on a small, specific sample of
tasks from an existing registry file to compare LLM performance.
"""
import json
import time
import argparse
import sys

# We import the functions from our now-standardized enrichment script.
from enrich_task_entry import initialize_model, get_enrichment_data


def main():
    """Main function to orchestrate the targeted A/B test."""
    parser = argparse.ArgumentParser(
        description="Run a targeted A/B test on specific tasks."
    )
    parser.add_argument(
        "--source-registry",
        required=True,
        help="Path to the source operative_registry.json file."
    )
    parser.add_argument(
        "--output-file",
        required=True,
        help="Path for the new JSON file to save test results."
    )
    parser.add_argument(
        "--model-name",
        required=True,
        help="The Gemini model to test."
    )
    parser.add_argument(
        '--task-ids',
        nargs='+',
        required=True,
        help='A space-separated list of task_ids to test (e.g., d73868a7 14251f6f).'
    )
    args = parser.parse_args()

    # --- CONFIG ---
    sleep_interval = 5

    # --- 1. Load the source registry and handle both old/new formats ---
    try:
        with open(args.source_registry, 'r', encoding='utf-8') as f:
            loaded_json = json.load(f)

        source_tasks = []
        # --- THIS IS THE FIX ---
        # Check if the loaded data is a list (old format) or a dict (new format)
        if isinstance(loaded_json, list):
            print("Old registry format (list) detected.")
            source_tasks = loaded_json
        elif isinstance(loaded_json, dict) and 'tasks' in loaded_json:
            print("New registry format (dict) detected.")
            source_tasks = loaded_json.get("tasks", [])
        # --- END OF FIX ---
        
        # Create a dictionary for fast lookups
        source_tasks_dict = {
            task['task_id']: task for task in source_tasks if 'task_id' in task
        }
        print(f"Loaded {len(source_tasks_dict)} tasks from {args.source_registry}.")

    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading source registry: {e}")
        sys.exit(1)

    # --- The rest of the script is identical ---
    model = initialize_model(args.model_name)
    if not model:
        print("Failed to initialize Gemini model. Exiting.")
        sys.exit(1)

    new_enriched_tasks = []
    tasks_to_process = args.task_ids
    total_tasks = len(tasks_to_process)

    for i, task_id in enumerate(tasks_to_process):
        print(f"\n--- Processing task {i+1}/{total_tasks}: {task_id} ---")
        
        task = source_tasks_dict.get(task_id)
        if not task:
            print(f"WARNING: Task ID {task_id} not found in source registry. Skipping.")
            continue

        commit_message = task.get('task_title', '')
        commit_url = task.get('deliverable_url')

        if not commit_url:
            print(f"Skipping task {task_id} due to missing deliverable URL.")
            continue
            
        enrichment = get_enrichment_data(model, commit_url, commit_message)
        
        if enrichment:
            new_task = task.copy()
            new_task.update({
                "ai_model_used_for_enrichment": args.model_name,
                "provenance_type": enrichment.get("provenance_type"),
                "ai_generated_objective": enrichment.get('objective'),
                "ai_summary_of_changes": enrichment.get('summary_of_changes'),
                "ai_inferred_category": enrichment.get('task_category'),
                "ai_inferred_type": enrichment.get('task_type'),
                "ai_suggested_skills": enrichment.get('skills_demonstrated'),
                "ai_critique": (enrichment.get('annotations', [{}])[0].get('comment'))
            })
            new_enriched_tasks.append(new_task)
            print(f"Successfully enriched task {task_id}.")
        else:
            print(f"Failed to enrich task {task_id}.")
        
        if i < total_tasks - 1:
            print(f"Sleeping for {sleep_interval}s...")
            time.sleep(sleep_interval)

    final_output = {"tasks": new_enriched_tasks}
    with open(args.output_file, 'w', encoding='utf-8') as f:
        json.dump(final_output, f, indent=2)

    print(f"\nSUCCESS: Targeted A/B Test complete.")
    print(f"Wrote {len(new_enriched_tasks)} enriched tasks to {args.output_file}.")

if __name__ == "__main__":
    main()