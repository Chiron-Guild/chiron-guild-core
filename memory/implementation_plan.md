# Implementation Plan: Chiron Guild - Phase 0 System Finalization

**Project:** Chiron Guild - Phase 0 System Finalization
**Manager Agent:** Manager Agent v1
**User:** Kin-Caid
**Date:** 2024-05-24
**Status:** In Progress

---

## 1. Project Objective

The primary objective of this project is to finalize the initial operational system for the Chiron Guild, as defined in **Phase 0: Foundation**. The goal is to create a robust, low-friction, and structured system for decomposing projects and automating the creation of an LLM-enriched log of work.

**Success Metric:** The system is fully operational and valuable for a single user, enabling them to manage all personal and professional projects within the framework. The final output of work logs will be stored in `operative_registry.md`.

---

## 2. Memory Bank Configuration

**Chosen Structure:** Directory-based, Multi-file System (`/Memory/`).

**Justification:** Based on the analysis in `prompts/01_Manager_Agent_Core_Guides/02_Memory_Bank_Guide.md`, the project's complexity, involving distinct workstreams (System Refinement, Decomposition Tooling, Documentation), warrants a multi-file structure for organizational clarity, scalability, and ease of context retrieval. Logs will be organized into subdirectories corresponding to the major workstreams defined in this plan.

---

## 3. Implementation Workstreams & Tasks

The project is broken down into three primary workstreams. Tasks will be assigned to Implementation Agents sequentially unless otherwise noted.

### Workstream 1: System Stabilization & Refinement

*Focus: Make the existing GitHub Actions workflow robust, reliable, and produce the correct output format.*

*   **Task 1.1: Enhance `enrich_task_entry.py` Robustness**
    *   **Sub-task 1.1.1:** Implement more specific error handling for Gemini API calls (e.g., catch specific exceptions like `DeadlineExceeded`, `ResourceExhausted`).
    *   **Sub-task 1.1.2:** Implement a simple retry mechanism (e.g., retry once after a short delay on failure).
    *   **Sub-task 1.1.3:** Add schema validation for the JSON returned by the AI. If the JSON is malformed or missing keys, the script should handle it gracefully (e.g., log an error and exit, rather than crashing).
*   **Task 1.2: Implement JSON to Markdown Conversion**
    *   **Sub-task 1.2.1:** Design a standardized Markdown format for a single entry in `operative_registry.md`. This format should be clear, readable, and contain all the enriched data fields.
    *   **Sub-task 1.2.2:** Modify the `enrich-task-registry.yml` workflow to add a new step that takes `enrichment_output.json` as input and converts it into the standardized Markdown format.
    *   **Sub-task 1.2.3:** Modify the workflow's final step to append the generated Markdown to `operative_registry.md` instead of updating a JSON file.
*   **Task 1.3: Workflow Review and Cleanup**
    *   **Sub-task 1.3.1:** Review both `log-task-to-registry.yml` and `enrich-task-registry.yml` for any potential race conditions or logic gaps.
    *   **Sub-task 1.3.2:** Ensure the placeholder creation and enrichment update mechanism works reliably.

### Workstream 2: Project Decomposition Tooling

*Focus: Build a low-friction process for decomposing complex projects into actionable deliverables.*

*   **Task 2.1: Define Project Decomposition Requirements**
    *   **Sub-task 2.1.1:** Define the core components of a "complex project" in the context of the Guild (e.g., High-Level Goal, Key Deliverables, Epics, Tasks).
*   **Task 2.2: Design and Implement GitHub Issue Template for Decomposition**
    *   **Sub-task 2.2.1:** Create a new GitHub Issue Form (`.github/ISSUE_TEMPLATE/project_decomposition.yml`) that guides a user through the decomposition process.
    *   **Sub-task 2.2.2:** The form should include fields for Project Title, Objective, Key Deliverables, and a structured way to list initial tasks. Use labels to automatically tag these issues (e.g., `project-brief`, `status:planning`).

### Workstream 3: Documentation & Usability

*Focus: Create clear documentation to make the system fully operational and valuable for a single user.*

*   **Task 3.1: Create Core System Documentation**
    *   **Sub-task 3.1.1:** Create a comprehensive `README.md` at the project root that explains the purpose of the Chiron Guild Core repository and the function of the automated work-logging system.
    *   **Sub-task 3.1.2:** Add a `docs/workflow_guide.md` file that visually and textually explains the end-to-end process from `git commit` to the final entry in `operative_registry.md`.
*   **Task 3.2: Create User-Facing Guides**
    *   **Sub-task 3.2.1:** Write a guide on "How to Decompose a Project" using the new issue template.
    *   **Sub-task 3.2.2:** Write a guide on "Making a Commit" that explains how to format commit messages and use the `Human-authored-by:` trailer.
*   **Task 3.3: Document the `operative_registry.md` Standard**
    *   **Sub-task 3.3.1:** Formally document the standard Markdown format for a log entry, as designed in Task 1.2.1.

---

## 4. Next Steps

The immediate next step is to begin execution of **Workstream 1**, starting with **Task 1.1**. I will prepare the first task assignment prompt for your review.
