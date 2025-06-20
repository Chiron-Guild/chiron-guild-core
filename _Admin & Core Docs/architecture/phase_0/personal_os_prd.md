# Product Requirements Document (PRD): The Personal Operating System

This PRD details the features and functionalities of the Phase 0 product.

### **1. Introduction**
This document defines the requirements for the Chiron Guild's Phase 0 product: a "Personal Operating System" (POS). The POS is a GitHub-based framework designed to help a solo knowledge worker define, execute, and track their work with extreme clarity and verifiable proof of completion. This product is the foundational step in our **Mission** to build a new system for work, directly embodying our core values of **Precision & Clarity** and **Sovereignty & Agency**.

### **2. Goals and Objectives**
*   **Product Goal:** To provide immediate, tangible value to an individual knowledge worker by giving them a superior system for personal project management and a permanent, auditable record of their accomplishments.
*   **Business Objective:** To create a stable, desirable, and open-source foundation that will attract the first wave of community members in Phase 1.

### **3. Target Audience**
*   **Primary User:** Solo knowledge workers (developers, researchers, writers, strategists) who are familiar with the GitHub ecosystem and value structured, deep work.
*   **Characteristics:** Organized, methodical, interested in personal productivity systems, and aligned with the principles of open source and verifiable work.

### **4. User Stories & Features**

| Priority | User Story                                                                                                                                                                       | Feature Name                 | Strategic Link                                                                   |
| :------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------- | :------------------------------------------------------------------------------- |
| **P0**   | As a user, I want to define a new task using a structured template, so that my objectives, context, and success criteria are captured with maximum clarity.                          | Structured Task Creation     | `Value: Precision & Clarity`                                                     |
| **P0**   | As a user, when I close a task in GitHub, I want the system to **automatically** log it to my permanent record, so that I have verifiable provenance without tedious manual work.    | Automated Contribution Logging | `Article III: Right to Verifiable Provenance`, `Value: Augmentation, Not Replacement` |
| **P0**   | As a user, I want to view my entire work history in a single, human-readable Markdown file, so that I can easily review and share my accomplishments.                               | Human-Readable Registry      | `Value: Precision & Clarity`                                                     |
| **P1**   | As a user, I want to easily set up this system for myself by forking a repository and setting one secret, so that I can get started quickly.                                     | "One-Fork" Installation    | `Mission: Grow` (Foundation for it)                                              |
| **P1**   | As a user, I want to categorize my tasks using labels, so that the automated log entry reflects the nature and context of the work.                                              | Task Categorization          | `Guild Charter: Task Taxonomy Protocol` (Foundation for it)                    |

### **5. Functional Requirements**
*   **FR-1 (Templates):** The system MUST provide at least one GitHub Issue template in the `.github/ISSUE_TEMPLATE` directory. The template MUST prompt the user for a clear title, description, and acceptance criteria.
*   **FR-2 (Automation Trigger):** The system MUST include a GitHub Actions workflow that triggers on the `issues` event with `type: closed`.
*   **FR-3 (Data Parsing):** The workflow MUST successfully extract the following data from the closed issue payload: issue number, issue title, closing user's GitHub handle, and all assigned labels.
*   **FR-4 (Registry Writing):** The workflow MUST append a new, formatted Markdown table row to the `data/registry.md` file. The format should be: `| YYYY-MM-DD | [#IssueNum](link) Title | @username | [Label1] [Label2] |`
*   **FR-5 (Idempotency):** The workflow MUST NOT create duplicate entries if it is accidentally run more than once for the same issue.

### **6. Non-Functional Requirements**
*   **NFR-1 (Usability):** The core loop (create issue -> close issue -> see log) MUST not require any command-line interaction or local scripts. It must function entirely within the GitHub web UI.
*   **NFR-2 (Reliability):** The GitHub Action workflow must be resilient and include error handling for common failure modes (e.g., missing secrets).
*   **NFR-3 (Documentation):** The `README.md` must contain clear, step-by-step instructions for forking, configuration, and basic use.

### **7. Success Metrics**
*   **Activation Rate:** % of users who fork the repo and successfully log their first task.
*   **Task Throughput:** A single user can successfully log >20 tasks in a week without system failure.
*   **System Integrity:** 0 manual edits are required to the `registry.md` file during normal operation.

### **8. Assumptions & Dependencies**
*   The system is dependent on the GitHub platform, specifically GitHub Actions and Issues.
*   We assume users have a GitHub account and basic familiarity with its concepts (repositories, issues, forking).

### **9. Out of Scope**
*   Any form of payment processing or financial calculation.
*   Database integration (e.g., Postgres, MySQL).
*   User management beyond a single user's GitHub identity.
*   Any features related to the Project Asset Lifecycle (Prime Earning Period, etc.).
