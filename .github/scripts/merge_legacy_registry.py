#!/usr/bin/env python3
"""
Merge Legacy Registry Script

This script intelligently merges unique, non-commit-based tasks from a legacy
operative registry into the new, standardized operative history format. It
transforms the data into the new schema and ensures the final log is complete
and chronologically sorted.

The script is idempotent and can be safely re-run.
"""

import json
import os
import sys
import re
import argparse  # Refinement: Use argparse for robust argument handling
from typing import Dict, List, Any, Optional

def load_json_file(file_path: str) -> Any:
    """Loads and parses a JSON file with error handling."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Input file '{file_path}' not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in '{file_path}': {e}")
        sys.exit(1)

def save_json_file(data: Any, file_path: str) -> None:
    """Saves data to a JSON file with pretty-printing."""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        print(f"\nSUCCESS: Merged data saved to '{file_path}'")
    except IOError as e:
        print(f"Error saving file '{file_path}': {e}")
        sys.exit(1)

def has_commit_deliverable(deliverables: List[str]) -> bool:
    """Checks if any deliverable string is a GitHub commit URL."""
    commit_pattern = r'github\.com/.+/commit/'
    return any(re.search(commit_pattern, str(d)) for d in deliverables)

def transform_legacy_task(legacy_task: Dict[str, Any]) -> Dict[str, Any]:
    """Transforms a legacy task dictionary into the new standardized schema."""
    issue_number = legacy_task.get('issue_number')
    task_id = f"issue-{issue_number}" if issue_number else "legacy-task"

    title = legacy_task.get('issue_title', 'Legacy Task')
    
    # Refinement: Handle missing category/type with defaults
    category_match = re.search(r'\[CHIRON-(\w+)', title)
    type_match = re.search(r'-\w+-(\w+)\]', title)
    category = category_match.group(1).upper() if category_match else "LEGACY"
    task_type = type_match.group(1).upper() if type_match else "PROJ"
    
    # Refinement: Create a more descriptive summary
    deliverables = legacy_task.get('Deliverables', [])
    if deliverables:
        summary = f"Completed deliverables include: {', '.join(map(str, deliverables))}."
    else:
        summary = "Legacy task completed as per issue description."

    return {
        "task_id": task_id,
        "task_title": title,
        "completion_date": legacy_task.get('closed_at'),
        "operative": "Kin-Caid",
        "deliverable_url": legacy_task.get('issue_url'),
        "provenance_type": "human_authored",
        "objective": legacy_task.get('Objective'),
        "summary_of_changes": summary,
        "critique": None,
        "task_category": category,
        "task_type": task_type,
        "skills_demonstrated": legacy_task.get('skills', [])
    }

def merge_registries(legacy_file: str, new_file: str, output_file: str) -> None:
    """Main function to merge legacy registry into new history format."""
    print("Loading data...")
    legacy_data = load_json_file(legacy_file)
    new_data = load_json_file(new_file)

    if 'tasks' not in new_data or not isinstance(new_data['tasks'], list):
        print(f"Error: New history file '{new_file}' must contain a 'tasks' list.")
        sys.exit(1)

    existing_tasks = new_data['tasks']
    # Create a set of existing task IDs for efficient lookup
    existing_ids = {task.get('task_id') for task in existing_tasks}
    
    print(f"Found {len(existing_tasks)} tasks in new history.")
    print(f"Found {len(legacy_data)} tasks in legacy registry.")
    print("-" * 40)

    merged_count = 0
    for task in legacy_data:
        # Skip tasks that are commit-based
        if has_commit_deliverable(task.get('Deliverables', [])):
            continue

        transformed = transform_legacy_task(task)
        
        # Idempotency check: skip if already merged
        if transformed['task_id'] in existing_ids:
            continue

        print(f"Merging unique legacy task: {transformed['task_id']} - {transformed['task_title']}")
        existing_tasks.append(transformed)
        existing_ids.add(transformed['task_id'])
        merged_count += 1
    
    # Refinement: Sort the final merged list by completion date
    # Handles cases where completion_date might be None or an empty string
    existing_tasks.sort(key=lambda x: x.get('completion_date') or '', reverse=True)
    
    new_data['tasks'] = existing_tasks
    save_json_file(new_data, output_file)

    print("-" * 40)
    print(f"Merge complete. Merged {merged_count} new legacy tasks.")
    print(f"Total tasks in final registry: {len(existing_tasks)}")

def main():
    """Main entry point and argument parsing for the script."""
    # Refinement: Use argparse for robust and documented arguments
    parser = argparse.ArgumentParser(
        description="Merge unique legacy tasks into a new operative history file.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        '--legacy-file',
        default='operative_registry_legacy.json',
        help='Path to the legacy (issue-based) JSON registry file.'
    )
    parser.add_argument(
        '--new-file',
        default='operative_history.json',
        help='Path to the new (commit-based) JSON history file.'
    )
    parser.add_argument(
        '--output-file',
        default='operative_history_FINAL.json',
        help='Path for the final merged JSON output file.'
    )
    args = parser.parse_args()

    print("Chiron Guild Legacy Registry Merger")
    print("=" * 40)
    
    merge_registries(args.legacy_file, args.new_file, args.output_file)

if __name__ == "__main__":
    main()