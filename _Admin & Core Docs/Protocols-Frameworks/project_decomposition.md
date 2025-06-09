# Protocol: LLM-Assisted Project Decomposition for the Chiron Guild

**Operative:** Kin-Caid
**Version: 1.2** # UPDATED VERSION
**Date: 2025-06-06** # UPDATED DATE
**Objective:** To provide a standardized, LLM-augmented process for decomposing complex projects into a structured JSON format (input_ops.json). This JSON will define meta-objectives, project sectors, and discrete `Guild Ops`, suitable for input into automated brief generation systems. This protocol leverages a "Mythic Core, Precision Shell" approach.

---
## Stage 0. Overview of the Project Decomposition & Guild Op Lifecycle

This protocol outlines a multi-stage process, combining Operative strategy with LLM assistance and GitHub Actions automation, to transform a high-level project concept into actionable Guild Ops managed on the Guild Board. 

This structured lifecycle ensures clarity, provides opportunities for review, and leverages automation for efficiency. The following sections detail the prompts and procedures for each stage.

**The lifecycle consists of the following key stages:**

*   **Stage 1: LLM Priming (Operative & LLM)**
    *   Establish foundational context for the LLM regarding Chiron Guild terminology and ethos.
*   **Stage 2: Project Definition & High-Level Structuring (Operative & LLM)**
    *   **Task 2.1. Meta-Objective Definition:** Distill the project's core purpose into 3-5 Meta-Objectives (output: JSON snippet). **(Utilize `decomposition_stage_2.1_meta_objectives.ipynb`)**
    *   **Task 2.2. Strategic Chunking & Sector Definition:** Break down the project into 3-5 major Project Sectors, aligning them with Meta-Objectives (output: JSON snippet). **(Utilize `decomposition_stage_2.2_chunking_and_sectors.ipynb`)**
*   **Stage 3: Granular Guild Op Identification (Operative & LLM - Iterative per Sector)**
    *   For each defined Project Sector, generate a list of 5-10 discrete Guild Ops (output: JSON snippet per sector). **(Utilize `decomp_task_3_granular_op_id.ipynb`)**
*   **Stage 4: Assembling the `input_ops.json` File (Operative Task)**
    *   Consolidate the project name, project metadata, and the JSON outputs from Tasks 2.1, 2.2, and 3.1 into a single, canonical `Projects/input_ops.json` file. This file serves as the master input for automated brief generation.
*   **Stage 5: Automated Brief Generation for Review (Operative Task & GitHub Action)**
    *   The Operative pushes the `Projects/input_ops.json` file to the repository.
    *   This triggers the `Generate Guild Op Briefs for Review` GitHub Action (`generate_briefs.yml`).
    *   The Action uses an LLM to generate detailed brief proposals for each Op in `input_ops.json`.
    *   The Action **automatically commits** the generated briefs (e.g., `_generated_briefs_for_review.md` and `_generated_briefs_to_create.json`) to the specific project's `generated_briefs` directory (e.g., `Projects/personal/creek_connections/generated_briefs/`).
    *   The Operative reviews these generated files directly in the repository and refines `_generated_briefs_to_create.json` if necessary.
    *   The Operative cleans the processed Ops from `Projects/input_ops.json`.
*   **Stage 6: Guild Op Brief Instantiation on GitHub Board (Issue Creation & Automated Archival)**
    *   The Operative uses the finalized data from `_generated_briefs_to_create.json` (from the project's `generated_briefs` directory) to create new GitHub Issues (manually or via a future local script).
    *   The creation of each GitHub Issue automatically triggers the `Create Guild Op Directory and Log` GitHub Action (`create-op-directory-log.yml`).
    *   This second Action scaffolds the `Projects/[ProjectID-Slug]/Guild Ops/[GUILD_OP_ID]/` directory and initial log file on a new feature branch for that Guild Op.
---

## Stage 1. LLM Priming Protocol (Execute Once Per Session or As Needed)

**Purpose:** To establish foundational context for the LLM, ensuring its responses align with Chiron Guild terminology, objectives, and operational ethos.

**LLM Prompt:**

```text
You are an expert project decomposition assistant and strategic analyst for Operative Kin-Caid of the Chiron Guild.

**Core Mission & Ethos:**
The Chiron Guild is a worker-owned, AI-augmented digital cooperative. Our ethos is 'Mythic Core, Precision Shell,' focused on supplanting old labor models with equitable and efficient systems. We value clarity, actionability, and meticulous planning.

**Key Terminology (You MUST understand and use these correctly):**
*   **Project Brief:** The initial high-level description of the project provided by the Operative.
*   **Meta-Objective:** A high-level strategic goal for the project.
*   **Project Sector:** A major logical phase or component of the project. Each has a unique `sector_id`.
*   **Guild Op:** A granular, actionable task within a Project Sector. Each Op is designed to be a discrete unit of work.
*   **`op_title`:** The concise, action-oriented title of a Guild Op.
*   **`op_type`:** The category of work for a Guild Op. The official types are DEV, DSN, DOC, GOV, STR, QAT, COM, and for PERS Ops, we also use LRN, CRAFT, PRAC, and PROJ.
*   **`primary_deliverable`:** The main verifiable outcome of a Guild Op.
*   **`input_ops.json`:** The target structured JSON file this decomposition process aims to create.
*   **Chironian:** A member of the Chiron Guild.
*   **Guild Board:** The platform (e.g., GitHub Issues) where Guild Ops are managed.
*   **Guild Seal:** A verifiable credential awarded upon successful completion of a Guild Op.
*   **Context Compilations:** Structured documentation supporting Guild operations.

**Your Role:**
Your primary function is to assist Operative Kin-Caid in breaking down complex Project Briefs into a structured JSON format. You will guide the definition of meta-objectives, the identification of project sectors, and the granulation of work into Guild Ops for each sector. Your responses must be structured as requested (often JSON), precise, and focused on verifiable outcomes, embodying the 'Precision Shell.'

**Operational Context / Tone:**
Your responses must adapt to the context provided by the Operative. If the context is "Mythic Core," use Guild-specific lore and tone. If the context is "Professional/Agile," use standard industry terminology (e.g., "Tasks" instead of "Guild Ops," "Backlog" instead of "Guild Board"). You will be given this context with the initial project brief.
```

## Stage 2. LLM-Assisted Meta-Objective Definition

**Purpose:** To prime the LLM to act as a project analyst helping define core project objectives.

## Task 2.1. LLM-Assisted Meta-Objective Definition

**Purpose:** To assist the Operative in distilling a project's core purpose into a set of compelling Meta-Objective statements, formatted for easy inclusion in input_ops.json.

**User Inputs to LLM:**
* Project Name/Concept
* Raw Project Description

**LLM Prompt:**

```text
You are an expert project analyst working with Operative Kin-Caid of the Chiron Guild.

**Your Current Task:** Meta-Objective Definition.
Your goal is to assist Operative Kin-Caid in drafting 3-5 concise, compelling Meta-Objective statements based on the provided project information.

**Process:**
1.  You will be provided with a Project Name/Concept and a Raw Project Description.
2.  Based on this input, draft 3-5 Meta-Objective statements.
3.  Each statement should be a single sentence capturing the absolute core purpose and primary value proposition of the project for the Chiron Guild or the specific Operative endeavor.
4.  Focus on the ultimate 'win' or desired future state.
5.  **Output Format:** Structure your response as a **JSON array**. Each object in the array should represent one Meta-Objective and MUST contain the following keys:
    *   `"id"` (string): A short identifier (e.g., "M1", "M2", "M3").
    *   `"text"` (string): The concise Meta-Objective statement.

Reminder: Adhere to the specified Operational Context / Tone ("Mythic Core" or "Professional/Agile") for this project in all your generated text.
```

**Example User Input for Task 2.1:**

```text
Project Name/Concept: Chiron Guild Internal Communications Hub

Raw Project Description:
The Chiron Guild currently uses a mix of Discord, email, and shared documents for internal communication. This is becoming fragmented and inefficient as we grow. We need a centralized, self-hosted platform that integrates chat, knowledge base, and announcements. The platform should be secure, extensible, and align with our values of data sovereignty and transparency. The goal is to improve information flow, reduce time spent searching for information, and foster a stronger sense of community among Chironians. This will ultimately make our cooperative more effective and resilient.

Task: Generate the JSON array of Meta-Objectives.
```

**Example LLM Output for Task 2.1:**

```text
[
  {
    "id": "M1",
    "text": "To establish a secure, integrated, and self-hosted Chiron Guild Communications Hub that centralizes information flow, enhancing collaboration and reinforcing operational sovereignty."
  },
  {
    "id": "M2",
    "text": "To streamline internal communications and knowledge sharing within the Chiron Guild, fostering a more cohesive, efficient, and resilient cooperative."
  },
  {
    "id": "M3",
    "text": "To empower Chironians with a unified and transparent communication platform that minimizes information fragmentation and maximizes collective intelligence."
  }
]
```


**Operative Action for Task 2.1:** 
1. Review the LLM's suggestions.
2. Select, refine, or combine them to finalize the list of Meta-Objectives. (Note: This JSON array will form the meta_objectives part of input_ops.json.)
---

## Task 2.2 LLM-Assisted Strategic Chunking & Sector Definition

**Purpose:** To assist the Operative in breaking down the project (based on its finalized Meta-Objectives) into major, distinct Project Sectors, formatted for easy inclusion in input_ops.json.

**User Inputs to LLM:**
* Finalized Project Meta-Objectives (text or the JSON array from Task 2.1).
* Overall Project Name/Concept.
* Optional: Additional project context or constraints.

**LLM Prompt:**

```text
You are an expert systems architect and strategic planner for Operative Kin-Caid of the Chiron Guild.

**Your Current Task:** Strategic Chunking & Project Sector Definition.
Your goal is to assist Operative Kin-Caid in breaking down the project into 3-5 major, distinct Project Sectors (logical phases or key components) required to achieve its Meta-Objectives.

**Process:**
1.  You will be provided with the finalized Project Meta-Objectives and the Overall Project Name/Concept.
2.  Based on this input, propose 3-5 major, distinct Project Sectors.
3.  **Output Format:** Structure your response as a **JSON array**. Each object in the array should represent one Project Sector and MUST contain the following keys:
    *   `"sector_id"` (integer): Assign a sequential ID, starting from 1.
    *   `"sector_name"` (string): A short, descriptive name for the Sector (e.g., "Core Infrastructure Setup," "User Interface Development").
    *   `"sector_summary"` (string): A 1-2 sentence summary of the Sector's primary focus and objectives.
    *   `"alignment_with_meta_objectives"` (string): Briefly explain how this Sector contributes to achieving one or more of the overall Project Meta-Objectives.

Reminder: Adhere to the specified Operational Context / Tone ("Mythic Core" or "Professional/Agile") for this project in all your generated text.
```
**Example User Input for Task 2.2:**

```text
Overall Project Name: Chiron Guild Internal Communications Hub

Finalized Meta-Objectives:
[
  {
    "id": "M1",
    "text": "To establish a secure, integrated, and self-hosted Chiron Guild Communications Hub that centralizes information flow, enhancing collaboration and reinforcing operational sovereignty."
  },
  {
    "id": "M2",
    "text": "To streamline internal communications and knowledge sharing within the Chiron Guild, fostering a more cohesive, efficient, and resilient cooperative."
  }
]

Additional Context: The solution will likely involve selecting and deploying a self-hosted open-source software package and integrating it with our existing identity management system (if feasible).

Task: Generate the JSON array of Project Sectors.
```

**Example LLM Output for Task 2.2:**

```text
[
  {
    "sector_id": 1,
    "sector_name": "Platform Research, Selection & Initial Setup",
    "sector_summary": "Thoroughly research, evaluate, and select a suitable self-hosted communication platform, then perform initial server provisioning and software installation.",
    "alignment_with_meta_objectives": "Directly supports M1 by identifying and establishing the foundational 'self-hosted platform' and prepares for M2 by selecting a tool to 'streamline communications'."
  },
  {
    "sector_id": 2,
    "sector_name": "Core Feature Configuration & Customization",
    "sector_summary": "Configure essential communication features (chat, forums, announcements, knowledge base) and apply necessary Guild branding or light customization.",
    "alignment_with_meta_objectives": "Achieves the 'integrated' and 'centralized information flow' aspects of M1, directly enabling features for M2."
  },
  {
    "sector_id": 3,
    "sector_name": "Security, Integration & Protocol Definition",
    "sector_summary": "Implement security best practices, explore integration with existing Guild identity systems, and define operational protocols for platform usage and moderation.",
    "alignment_with_meta_objectives": "Addresses the 'secure' and 'operational sovereignty' aspects of M1, and establishes guidelines for an 'efficient cooperative' (M2)."
  },
  {
    "sector_id": 4,
    "sector_name": "User Onboarding, Documentation & Launch",
    "sector_summary": "Develop user guides, conduct pilot testing with a core group of Chironians, gather feedback, and prepare for a Guild-wide launch.",
    "alignment_with_meta_objectives": "Ensures the platform 'enhances collaboration' (M1) effectively and 'fosters a stronger community' (M2) by preparing users for adoption."
  }
]
```

**Operative Action for Stage 2.2:** 

Review the LLM's suggestions. Refine sector names, summaries, and alignments as needed. This JSON array will form the project_sectors part of input_ops.json.

## Task 2.3 Generate Project Requirements Document (PRD)

**Purpose:** To assist the Operative in breaking down the project (based on its finalized Meta-Objectives) into major, distinct Project Sectors, formatted for easy inclusion in input_ops.json.

**User Inputs to LLM:**
* Overall Project Name/Concept.
* Finalized Project Meta-Objectives (text or the JSON array from Task 2.1).
* Finalized Project Sectors (text or the JSON array from Task 2.2).
* Optional: Additional project context or constraints.

**LLM Prompt:**

```text
## Persona & Tone
You are an expert Senior Project Manager and Business Analyst. Your communication style is clear, concise, and professional, adhering strictly to standard agile and lean project management principles. Avoid jargon, but use industry-standard terminology where appropriate (e.g., "scope," "KPIs," "stakeholders"). Your entire output must be grounded in business value and user needs.

## Task
Your task is to synthesize the provided project inputs into a comprehensive, professional Project Requirements Document (PRD). The output must be a single, complete Markdown document suitable for review by technical and non-technical stakeholders.

## Inputs You Will Receive
1.  **Project Name:** The official name of the project.
2.  **Raw Project Description:** The initial, high-level brief from the project owner.
3.  **Strategic Objectives (JSON):** A JSON array of the project's high-level goals.
4.  **Project Sectors (JSON):** A JSON array of the major functional areas or phases of the project.
5.  **project_prd_template.md** A markdown document that defines the PRD template.

## Process
1.  **Analyze all inputs** to gain a holistic understanding of the project's purpose and structure.
2.  **Synthesize an Executive Summary and Problem Statement** based on the raw description and objectives. Do not simply copy; interpret and summarize.
3.  **Populate the PRD structure**, mapping the provided "Strategic Objectives" and "Project Components" to the appropriate sections.
4.  **Infer and Propose** additional critical sections based on your expertise:
    *   **User Stories / Key Features:** Propose 3-5 high-level user stories that capture the essence of the project's functionality.
    *   **Out of Scope:** Suggest 2-3 reasonable items that should be explicitly excluded to maintain focus.
    *   **Success Metrics / KPIs:** Propose 2-3 measurable KPIs that directly relate to the Strategic Objectives.
    *   **Assumptions and Dependencies:** Infer at least one reasonable assumption and one potential dependency.
5.  **Format the entire output** as a clean, professional Markdown document. Use headers, lists, and tables appropriately for maximum clarity.

## Output Format
* Your final output MUST be a single, complete Markdown document.
* Do not include any commentary outside of the document itself. Structure your response according to the provided PRD template format.

**Begin generating the PRD now.**
```

**Operative Action for Stage 2.2:** 

Review the LLM's output, refine as needed and save to the Project directory.
---

## Stage 3. LLM-Assisted Granular Op Identification (Task 3.1 - Run for EACH Sector)

**Purpose:** To assist the Operative in generating a list of 5-10 discrete, actionable Guild Ops for each defined Project Sector, formatted for easy inclusion in input_ops.json.

**User Input to LLM (for each sector):**
*Overall Project Meta-Objective(s) (for context).
*The specific sector_id of the current sector being decomposed.
*The sector_name of the current sector.
*The sector_summary of the current sector.

**LLM Prompt for Task 3.1:**

```text
# System Instruction (for AI Studio Preamble/Tuning - Task 3.1: Granular Guild Op Identification for Project Decomposition)

You are an expert task analyst and project deconstruction specialist for the Chiron Guild, working with Operative Kin-Caid. Your responses must embody the Guild's "Mythic Core, Precision Shell" ethos – visionary in scope, meticulous in detail.

**Your Current Task:** Granular Guild Op Identification for a specific Project Sector.
Your goal is to assist Operative Kin-Caid by generating a list of 5-10 potential, discrete, and actionable Guild Ops required to complete the objectives of a given Sector.

**Process:**
1.  You will be provided with:
    *   The overall **Project Meta-Objective(s)** (for broader context).
    *   The **Current Sector ID** (integer).
    *   The **Current Sector Name**.
    *   The **Current Sector Summary**.(edited)
2.  For the specified Sector, generate a list of 5-10 potential granular Guild Ops.
3.  **Output Format:** Generate your response as a **JSON array**. Each object in the array should represent a single Guild Op and MUST contain the following keys:
    *   `"sector_id"` (integer): The **Current Sector ID** provided in the input. This links the Op to its parent sector.
    *   `"op_title"` (string): A clear, action-oriented title for the Guild Op.
    *   `"op_type"` (string): Its likely **Op Type**. Choose from: `DEV`, `DSN`, `DOC`, `GOV`, `STR`, `QAT`, `COM`, `LRN`, `CRAFT`, `PRAC`, `PROJ`.
    *   `"primary_deliverable"` (string): A brief, verifiable statement of the primary outcome or artifact produced by completing the Op.

Reminder: Adhere to the specified Operational Context / Tone ("Mythic Core" or "Professional/Agile") for this project in all your generated text.
```

**Example User Input for Task 3.1 (for a single sector):**

```text
Project Meta-Objective(s):
M1: To establish a secure, integrated, and self-hosted Chiron Guild Communications Hub...
M2: To streamline internal communications and knowledge sharing...

Current Sector ID: 1
Current Sector Name: Platform Research, Selection & Initial Setup
Current Sector Summary: Thoroughly research, evaluate, and select a suitable self-hosted communication platform, then perform initial server provisioning and software installation.

Task: Generate the JSON array of Guild Ops for this sector.
```

**Example LLM Output for Task 3.1 (for a single sector):**

```text
[
  {
    "sector_id": 1,
    "op_title": "Research & Document Top 5 Self-Hosted Communication Platforms",
    "op_type": "DOC",
    "primary_deliverable": "A comparative report detailing features, pros/cons, security aspects, and Guild alignment for 5 candidate platforms."
  },
  {
    "sector_id": 1,
    "op_title": "Define Selection Criteria & Scorecard for Communication Platform",
    "op_type": "GOV",
    "primary_deliverable": "A finalized scorecard with weighted criteria for platform selection, approved by relevant stakeholders."
  },
  {
    "sector_id": 1,
    "op_title": "Select Final Communication Platform based on Research & Criteria",
    "op_type": "STR",
    "primary_deliverable": "A decision log documenting the final platform choice and rationale."
  },
  {
    "sector_id": 1,
    "op_title": "Provision Development Server for Selected Platform",
    "op_type": "DEV",
    "primary_deliverable": "A provisioned server (virtual or physical) with OS, basic security hardening, and network access, ready for platform installation."
  },
  {
    "sector_id": 1,
    "op_title": "Install and Perform Initial Configuration of Selected Platform",
    "op_type": "DEV",
    "primary_deliverable": "The selected communication platform installed on the development server with default admin account setup and basic operational status confirmed."
  }
]
```

**Operative Action for Stage 3:** 

1. Run Task 3.1 for each Project Sector defined in Task 2.2.
2. Collect all the JSON arrays of Guild Ops.
3. Utilize notebooks/decomp_task_3_granular_op_id.ipynb for interactive execution and review of this task.

## 4. Assembling the Final input_ops.json (Operative Task)

**Purpose:** To consolidate the outputs from Tasks 2.1, 2.2, and 3.1 into a single input_ops.json file, saved within the specific project's directory (e.g., Projects/personal/creek_connections/input_ops.json).

**Process:**
1. Create input_ops.json: Start a new JSON file.
2. Add project_metadata: Include the top-level project_metadata object (e.g., project_id_prefix, context_label, default_assignee, version). This is the configuration for this project.
3. Add project_name: Define the top-level project_name string.
4. Add meta_objectives: Copy the finalized JSON array of meta-objective objects from Task 2.1 and place it as the value for the meta_objectives key.
5. Add project_sectors: Copy the finalized JSON array of project sector objects from Task 2.2 and place it as the value for the project_sectors key.
6. Add guild_ops:
7. Create an empty array as the value for the guild_ops key.
8. Take all the individual JSON arrays of Guild Op objects generated from Task 3.1 (one array per sector).
9. Concatenate these arrays into a single, flat list of Guild Op objects. This combined list becomes the value for the top-level guild_ops key.

**Target input_ops.json Schema:**

```text
{
  "project_metadata": {
    "project_id_prefix": "string (e.g., CCG)",
    "context_label": "string (e.g., Context:PERS, Context:CORE). This MUST align with the Primary Guild Op Categories defined in taxonomy_framework.md.",
    "default_assignee": "string (e.g., Kin-Caid)",
    "version": "string (e.g., 1.0.0)"
  },
  "project_name": "string (e.g., Creek Connections - JavaScript Game Development)",
  "meta_objectives": [
    {
      "id": "string (e.g., M1)",
      "text": "string (Meta-Objective statement)"
    }
    // ... more meta-objectives
  ],
  "project_sectors": [
    {
      "sector_id": "integer (e.g., 1)",
      "sector_name": "string",
      "sector_summary": "string",
      "alignment_with_meta_objectives": "string"
    }
    // ... more project sectors
  ],
  "guild_ops": [ // This is a FLAT LIST of ALL ops from ALL sectors
    {
      "sector_id": "integer (links to project_sectors)",
      "op_title": "string",
      "op_type": "string (DEV, DOC, etc.)",
      "primary_deliverable": "string"
    }
    // ... many more guild_ops
  ]
}
```

**Example Final input_ops.json (Conceptual Snippet):**

```text
{
  "project_metadata": {
    "project_id_prefix": "CHRN",
    "context_label": "Context:CORE",
    "default_assignee": "Kin-Caid",
    "version": "1.0.0"
  },
  "project_name": "Chiron Guild Internal Communications Hub - CHRN_COMMS_HUB",
  "meta_objectives": [
    { "id": "M1", "text": "To establish a secure, integrated..." }
    // ...
  ],
  "project_sectors": [
    { "sector_id": 1, "sector_name": "Platform Research, Selection & Initial Setup", "sector_summary": "...", "alignment_with_meta_objectives": "..." },
    { "sector_id": 2, "sector_name": "Core Feature Configuration & Customization", "sector_summary": "...", "alignment_with_meta_objectives": "..." }
    // ...
  ],
  "guild_ops": [
    // Ops from Sector 1
    { "sector_id": 1, "op_title": "Research & Document Top 5 Platforms", "op_type": "DOC", "primary_deliverable": "Comparative report..." },
    { "sector_id": 1, "op_title": "Define Selection Criteria", "op_type": "GOV", "primary_deliverable": "Finalized scorecard..." },
    // Ops from Sector 2
    { "sector_id": 2, "op_title": "Configure Chat Channels", "op_type": "DEV", "primary_deliverable": "Chat channels configured..." },
    { "sector_id": 2, "op_title": "Draft Knowledge Base Structure", "op_type": "DOC", "primary_deliverable": "KB structure document..." }
    // ... and so on for all ops from all sectors
  ]
}
```

**This project-specific input_ops.json file is now ready to be used by the generate_briefs_for_review.py script.**








