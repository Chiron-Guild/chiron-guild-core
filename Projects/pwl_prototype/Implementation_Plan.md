# Implementation Plan: Personal Work Ledger (PWL) Prototype
**Document Version:** 1.0
**Manager Agent:** Manager Agent Instance 1
**Project Principal (User):** Kin-Caid

## 1. Project Summary & Objectives

This project aims to develop a functional prototype of the Personal Work Ledger (PWL), serving as the "Phase 0: Foundation" deliverable for the Chiron Guild. The PWL will be a private, AI-powered "digital lab notebook" for a single user on a Windows machine.

The primary objectives are:
1.  Develop an event-driven tracker for key applications (VS Code, Chrome, Office, Terminal).
2.  Build an analysis engine to contextualize events and distinguish human vs. AI provenance.
3.  Create a functional desktop dashboard (PySide) for reviewing the work history.
4.  Prototype real-time contextual AI assistance using the Google Gemini API.
5.  Demonstrate credential generation via an SPDX-compliant JSON export.

The project must adhere to strict user sovereignty and local-first data privacy.

## 2. Memory Bank Configuration

- **Structure Type:** Directory-Based (Multi-File)
- **Location:** `/Memory/` at the project root.
- **Rationale:** The project's complexity, with distinct modules for event tracking, data analysis, and UI, necessitates a modular logging system. A multi-file approach allows for focused, organized logs for each major phase and task, preventing a single monolithic file from becoming unmanageable. This decision was made in accordance with `prompts/01_Manager_Agent_Core_Guides/02_Memory_Bank_Guide.md`.
- **Naming Convention:** Log files should be named descriptively and placed in phase-specific subdirectories, e.g., `Memory/Phase_1_Infrastructure/T01_Database_Schema_Log.md`.

---

## 3. Phased Implementation Breakdown

### Phase 1: Core Infrastructure & Setup
*Objective: Establish the foundational project structure and data storage.*
| Task ID | Description | Status | Agent Notes |
| :--- | :--- | :--- | :--- |
| **T01** | **Initialize Project Structure & Database:** Create directory layout, `requirements.txt`, and define the SQLite database schema in a setup script. | `Complete` | Foundational first step. |
| **T02** | **Develop Core Logging Module:** Create a simple, robust Python logging module to standardize how all other components will write status updates and errors to the console and/or a file. | `Complete` | Essential for debugging all subsequent phases. |

### Phase 2: Event Tracker Development (Windows)
*Objective: Build the background service to monitor user activity.*
| Task ID | Description | Status | Agent Notes |
| :--- | :--- | :--- | :--- |
| **T03** | **Global Input Monitoring:** Implement basic keyboard and mouse event monitoring using a library like `pynput` to capture raw input activity. | `Pending` | This will be the base layer for the heuristic engine. |
| **T04** | **Active Window & Application Tracking:** Implement logic to identify the active foreground application (e.g., `Code.exe`, `chrome.exe`). | `Pending` | Crucial for attributing events to the correct application. |
| **T05** | **VS Code Integration:** Develop specific hooks or monitoring techniques for VS Code events (e.g., file save, find/replace). | `Pending` | May require inspecting accessibility APIs or logs. |
| **T06** | **Chrome Browser Integration:** Develop logic to track significant web events like form submissions and URL changes. | `Pending` | Complex; will likely involve Windows UI Automation APIs. |
| **T07** | **Microsoft Office (Word/Excel) Integration:** Develop logic to track file save events for Word and Excel. | `Pending` | COM automation or UI Automation may be viable paths. |
| **T08** | **System Terminal Integration:** Monitor a running PowerShell/CMD process for command executions, especially `git` commands. | `Pending` | Involves process monitoring and potentially stdout capture. |

### Phase 3: Analysis Engine & AI Enrichment
*Objective: Process raw events into meaningful, enriched log entries.*
| Task ID | Description | Status | Agent Notes |
| :--- | :--- | :--- | :--- |
| **T09** | **Event Stream Processor:** Develop a script that reads raw events from the SQLite DB and groups them into logical sessions or actions. | `Pending` | The first step in turning noise into signal. |
| **T10** | **Human vs. AI Heuristic Engine:** Implement the initial logic to distinguish provenance based on event patterns (e.g., paste events followed by minimal typing). | `Pending` | Highly experimental. Will require significant iteration. |
| **T11** | **Google Gemini API Integration:** Create a module to send contextual data to the Gemini API for enrichment (e.g., summarizing a task, suggesting skills). | `Pending` | Requires secure API key management. |

### Phase 4: User Dashboard (UI)
*Objective: Create the user-facing application to view and manage the ledger.*
| Task ID | Description | Status | Agent Notes |
| :--- | :--- | :--- | :--- |
| **T12** | **Design UI Layout with Qt Designer:** Create the `.ui` file for the main dashboard window, including a list/table view for events, a detail pane, and search/filter controls. | `Pending` | Visual design step. |
| **T13** | **Develop PySide Application Logic:** Write the Python code to load the `.ui` file, connect UI elements to functions, and populate the view with data from the SQLite database. | `Pending` | The bulk of the UI development work. |
| **T14** | **Implement Annotation/Management Features:** Add functionality for the user to add notes to, categorize, or delete log entries from the dashboard. | `Pending` | Gives the user sovereign control over their record. |

### Phase 5: Credential Generation
*Objective: Implement the final export functionality.*
| Task ID | Description | Status | Agent Notes |
| :--- | :--- | :--- | :--- |
| **T15** | **Implement Data Exporter:** Create a function that takes a selection of log entries and formats them into the target SPDX-compliant JSON structure. | `Pending` | The final deliverable of the project's data pipeline. |

### Phase 6: Finalization & Optimization
*Objective: Polish the prototype for usability and performance.*
| Task ID | Description | Status | Agent Notes |
| :--- | :--- | :--- | :--- |
| **T16** | **Performance Tuning:** Analyze and optimize the background tracker for low CPU and memory overhead. | `Pending` | Critical for user acceptance. |
| **T17** | **Packaging & Installation:** Create a simple installation script or `README.md` guide for setting up and running the prototype. | `Pending` | Ensures the project is usable and repeatable. |