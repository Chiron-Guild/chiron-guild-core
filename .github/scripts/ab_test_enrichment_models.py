"""
This script performs an A/B test between different Gemini models by
re-enriching a pre-filtered list of tasks from an existing registry file.
"""
import json
import time
import argparse
import sys

# We import the functions from our now-standardized enrichment script.
from enrich_task_entry import initialize_model, get_enrichment_data


def main():
    """Main function to orchestrate the A/B test."""
    parser = argparse.ArgumentParser(
        description="A/B test enrichment models on an existing registry."
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
        help="The Gemini model to test (e.g., 'gemini-2.5-flash-lite-preview-06-17')."
    )
    args = parser.parse_args()

    # --- CONFIG ---
    # A 4-second sleep is safe for 15 RPM, 5-6s for 10 RPM models.
    sleep_interval = 5

    # --- 1. Load the source registry ---
    try:
        with open(args.source_registry, 'r', encoding='utf-8') as f:
            source_registry = json.load(f)
        source_tasks = source_registry.get("tasks", [])
        if not isinstance(source_tasks, list): # Handle old list-only format
             source_tasks = source_registry
        print(f"Loaded {len(source_tasks)} tasks from {args.source_registry}.")
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading source registry: {e}")
        sys.exit(1)

    # --- 2. Initialize the specified model ---
    # The initialize_model function in the other script now accepts this.
    model = initialize_model(args.model_name)
    if not model:
        print("Failed to initialize Gemini model. Exiting.")
        sys.exit(1)

    # --- 3. Process each task from the source list ---
    new_enriched_tasks = []
    for i, task in enumerate(source_tasks):
        print(f"\n--- Processing task {i+1}/{len(source_tasks)}: {task.get('task_id', 'N/A')} ---")

        # For this test, we simulate the commit message from the task title.
        commit_message = task.get('task_title', '')
        commit_url = task.get('deliverable_url')

        if not commit_url:
            print(f"Skipping task {task.get('task_id', 'N/A')} due to missing deliverable URL.")
            continue

        enrichment = get_enrichment_data(model, commit_url, commit_message)

        if enrichment:
            # Create a new, enriched task object
            new_task = task.copy()  # Start with the original task data
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
            print(f"Successfully enriched task {task.get('task_id', 'N/A')}.")
        else:
            print(f"Failed to enrich task {task.get('task_id', 'N/A')}.")

        print(f"Sleeping for {sleep_interval}s...")
        time.sleep(sleep_interval)

    # --- 4. Write final results ---
    final_output = {"tasks": new_enriched_tasks}
    with open(args.output_file, 'w', encoding='utf-8') as f:
        json.dump(final_output, f, indent=2)

    print(f"\nSUCCESS: A/B Test complete.")
    print(f"Wrote {len(new_enriched_tasks)} enriched tasks to {args.output_file}.")


if __name__ == "__main__":
    main()