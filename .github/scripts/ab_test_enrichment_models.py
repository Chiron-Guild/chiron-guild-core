"""
This script performs an A/B test between different Gemini models by
re-enriching a pre-filtered list of tasks from an existing registry file.
"""

import os
import json
import time
import argparse
from datetime import timezone

# Assuming enrich_task_entry is in the same directory or accessible
# We need to modify enrich_task_entry.py to accept a model name parameter
from enrich_task_entry import initialize_model, get_enrichment_data

def main():
    """Main function to orchestrate the A/B test."""
    parser = argparse.ArgumentParser(description="A/B test enrichment models.")
    parser.add_argument("--source-registry", required=True, help="Path to the source operative_registry.json file.")
    parser.add_argument("--output-file", required=True, help="Path for the new JSON file to save test results.")
    parser.add_argument("--model-name", required=True, help="The Gemini model to test (e.g., 'gemini-2.5-flash-lite-preview-06-17').")
    args = parser.parse_args()

    # --- CONFIG ---
    # We can use a slightly faster interval for the lite model's higher RPM
    sleep_interval = 4 # (60 seconds / 15 RPM)
    
    # --- 1. Load the source registry ---
    try:
        with open(args.source_registry, 'r', encoding='utf-8') as f:
            source_registry = json.load(f)
        source_tasks = source_registry.get("tasks", [])
        print(f"Loaded {len(source_tasks)} tasks from {args.source_registry}.")
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading source registry: {e}")
        exit(1)

    # --- 2. Initialize the specified model ---
    # We will need to update `initialize_model` to accept the model name
    model = initialize_model(args.model_name)
    if not model:
        print("Failed to initialize Gemini model. Exiting.")
        exit(1)

    # --- 3. Process each task from the source list ---
    new_enriched_tasks = []
    for i, task in enumerate(source_tasks):
        print(f"\n--- Processing task {i+1}/{len(source_tasks)}: {task['task_id']} ---")
        
        # We need the full commit message for the best results, which isn't in the registry.
        # For this test, we can simulate it using the title. For production, the live
        # workflow has the full message.
        commit_message = task.get('task_title', '')
        commit_url = task.get('deliverable_url')

        if not commit_url:
            print(f"Skipping task {task['task_id']} due to missing deliverable URL.")
            continue
            
        enrichment = get_enrichment_data(model, commit_url, commit_message)
        
        if enrichment:
            # Create a new, enriched task object
            new_task = task.copy() # Start with the original task data
            new_task.update({
                "ai_model_used": args.model_name,
                "ai_generated_objective": enrichment.get('objective'),
                "ai_summary_of_changes": enrichment.get('summary_of_changes'),
                "ai_critique": enrichment.get('constructive_critique')
            })
            new_enriched_tasks.append(new_task)
            print(f"Successfully enriched task {task['task_id']}. Sleeping for {sleep_interval}s...")
        else:
            print(f"Failed to enrich task {task['task_id']}. It will be excluded from the output.")
        
        time.sleep(sleep_interval)

    # --- 4. Write final results ---
    final_output = {"tasks": new_enriched_tasks}
    with open(args.output_file, 'w', encoding='utf-8') as f:
        json.dump(final_output, f, indent=2)
    print(f"\nSUCCESS: A/B Test complete. Wrote {len(new_enriched_tasks)} enriched tasks to {args.output_file}.")


if __name__ == "__main__":
    main()