# Chiron Guild: Guild Op Protocols

**Version: 1.0**
**Date: [Current Date]**
**Status: Ratified**

## 1. Introduction: The Fundamental Unit of Work

This document defines the protocols governing the **Guild Op**, the fundamental, atomic unit of work within the Chiron Guild. Adherence to these protocols ensures that all work is transparent, auditable, and contributes directly to an Operative's `Reputation Matrix`.

A Guild Op represents a discrete, actionable task with a clear objective and verifiable deliverables. It is the mechanism through which the Guild self-assembles, projects are executed, and value is created.

---

## 2. Anatomy of a Guild Op

Every Guild Op, whether created via Full Decomposition or Rapid Instantiation, is defined by a core set of attributes, typically captured in its Guild Op Brief on the Guild Board (GitHub Issue).

*   **Guild Op ID:** The unique, human-readable identifier for the Op (e.g., `CHIRON-GOV-002`).
*   **Objective:** A concise statement defining the "why" of the task.
*   **Deliverables:** A clear, verifiable list of the "what" that will be produced.
*   **Skills Required/Demonstrated:** A list of competencies utilized to complete the Op.
*   **Estimated Effort:** A t-shirt size estimate (Small, Medium, Large) to gauge complexity.
*   **Acceptance Criteria:** A checklist of conditions that must be met for the Op to be considered complete.
*   **Awarded Guild Seal:** The specific digital credential awarded upon successful completion and verification.

---

## 3. The Guild Op ID System

The Guild Op ID provides immediate context about an Op's purpose and origin. It follows a rigid `[PROJECT]-[TYPE]-[SEQUENCE]` structure.

**Format:** `[PROJECT_PREFIX]-[OP_TYPE]-[SEQUENCE_ID]`

*   **`[PROJECT_PREFIX]`:** A 2-4 letter code identifying the parent project. The canonical list of prefixes is managed in the root `project_mappings.json` file.
    *   Examples: `CHIRON` (Guild Infrastructure), `CCG` (Creek Connections), `PERS` (Personal).
*   **`[OP_TYPE]`:** A three-letter code defining the category of work. See Section 4 for a full list of official Op Types.
    *   Examples: `DEV`, `DOC`, `GOV`.
*   **`[SEQUENCE_ID]`:** A three-digit number, padded with leading zeros, that is sequential *within its own project and type*.
    *   Examples: `CHIRON-DEV-001`, `CHIRON-DEV-002`, `CCG-DEV-001`.

---

## 4. Official Op Type Definitions

Categorizing Ops by type is critical for filtering the Guild Board and for analyzing an Operative's skills within the `Reputation Matrix`.

| Type  | Name                  | Definition                                                                  |
| ----- | --------------------- | --------------------------------------------------------------------------- |
| `DEV` | Development           | Writing or modifying code; software implementation.                         |
| `DSN` | Design                | UI/UX design, graphic design, system architecture, or conceptual modeling.  |
| `DOC` | Documentation         | Writing or updating protocols, guides, briefs, or `Context Compilations`.   |
| `GOV` | Governance            | Defining or refining Guild rules, protocols, or decision-making processes.  |
| `STR` | Strategy              | High-level planning, research, analysis, and decision-making.               |
| `QAT` | Quality & Testing     | Testing, quality assurance, bug hunting, and verification tasks.            |
| `COM` | Communications        | External or internal communications, community management, or marketing.    |
| `LRN` | Learning              | Dedicated effort to learn a new skill required for future Ops.              |
| `PROJ`| Project Management    | Meta-Op for managing a collection of other Guild Ops (e.g., an Epic).       |
| `PRAC`| Practice              | Skill practice to maintain proficiency.                                     |
| `CRAFT`| Crafting              | The creation of a physical object.                                          |


---

## 5. Guild Op Lifecycle & Status Labels

Every Guild Op progresses through a defined lifecycle, tracked on the Guild Board using standardized `status:` labels.

*   **`status:open`:** The Op has been created and is available for an Operative to begin work. This is the default state.
*   **`status:in-progress`:** The Op has been claimed and is actively being worked on by an Operative.
*   **`status:in-review`:** The work has been completed and submitted for verification (e.g., via a Pull Request).
*   **`status:blocked`:** The Op cannot be progressed due to an external dependency or obstacle.
*   **`status:closed`:** The Op has been successfully completed, verified, and its awarded Guild Seal has been logged to the `Reputation Matrix`.

---

## 6. Operational Cadence: Full Decomposition vs. Rapid Instantiation

The Chiron Guild employs two distinct protocols for the creation of Guild Ops, each designed for a specific operational context. Choosing the correct protocol is essential for maintaining a balance between deep, strategic planning and swift, tactical execution.

### The Full Decomposition Protocol

This is the Guild's primary ceremony for strategic foresight. It is a comprehensive, multi-stage process designed to transform a large, complex, or ambiguous project concept into a network of interconnected, well-defined Guild Ops.

**Use this protocol when:**

*   Initiating a new major project (a `PROJ` Op).
*   The path forward is unclear and requires systematic breakdown and analysis.
*   The goal is to generate a complete backlog of tasks for a multi-week or multi-month endeavor.
*   You need to align a series of tasks with high-level `meta_objectives` and `project_sectors`.

> **Guiding Principle:** Use Full Decomposition when the map needs to be drawn before the journey can begin. It prioritizes clarity and strategic alignment over speed. Refer to `project_decomposition.md` for the complete procedure.

### The Rapid Instantiation Protocol (Quick Op)

This is the Guild's fast lane for tactical velocity. It utilizes a standardized GitHub Issue Template (`quick_op.yml`) to capture discrete, well-understood tasks with minimal friction.

**Use this protocol when:**

*   The task is already clearly defined and can be completed in a single work session (typically less than 8 hours).
*   Capturing emergent work from a meeting or ongoing project.
*   Logging daily tasks to ensure they are contributed to the `Reputation Matrix`.
*   Creating a specific bug fix, a small documentation update, or a single feature enhancement.

> **Guiding Principle:** Use Rapid Instantiation when the next step on the path is clear. It prioritizes speed and efficiency for known work units.

### At a Glance: Which Protocol to Use?

| Attribute          | Full Decomposition Protocol                                   | Rapid Instantiation (Quick Op)                                |
| ------------------ | ------------------------------------------------------------ | ------------------------------------------------------------- |
| **Primary Use**    | New, complex, or ambiguous projects                          | Known, discrete, or in-progress tasks                         |
| **Input**          | A high-level project concept or idea                         | A clearly defined task                                        |
| **Output**         | A full `input_ops.json` and a batch of generated brief proposals | A single, well-defined Guild Op on the board                  |
| **Overhead**       | Medium (requires interactive LLM sessions and review)        | Very Low (a single form submission)                           |
| **Core Principle** | **Foresight**                                                | **Velocity**                                                  |
