# Chiron Guild: Neutral Canon Architecture

**Version: 1.0**
**Status: Draft**
**Objective:** This document defines the canonical architecture for the Guild's knowledge base. It establishes a "Neutral Core" of style-agnostic source documents from which all public-facing and internal-facing documents ("shells") are synthesized. This ensures a single source of truth, simplifies maintenance, and enables scalable, automated content generation.

---

## 1. The Four Pillars of the Neutral Canon

The Neutral Canon is organized into four distinct pillars, representing a complete separation of the Guild's foundational concepts.

### I. Identity (`_identity/`)
*   **Purpose:** To define the immutable "Why" of the Guild. This is its soul and unchanging core.
*   **Atomic Documents:**
    *   `vision.md`: Defines the ultimate, aspirational future state the Guild works toward.
    *   `mission.md`: Defines the Guild's active purpose and what it does to achieve the vision.
    *   `values.md`: Lists and explains the core principles that guide all actions (e.g., Equity, Sovereignty, Precision).

### II. Strategy (`_strategy/`)
*   **Purpose:** To define the high-level "What" and "When." This is the operational roadmap and business logic.
*   **Atomic Documents:**
    *   `economic_model.md`: Describes the mechanics of value creation and distribution (worker-owned, Bounties, Seals).
    *   `strategic_phases.md`: Outlines the multi-phase roadmap for Guild development (Phase 0, Phase 1, etc.).

### III. Protocols (`_protocols/`)
*   **Purpose:** To define the granular "How." These are the repeatable, style-agnostic procedures for executing work.
*   **Atomic Documents:**
    *   `work_breakdown_protocol.md`: The process for decomposing a project into tasks.
    *   `task_lifecycle_protocol.md`: The rules for a task's journey from creation to completion.
    *   *(Future protocols will be added here)*

### IV. Data (`_data/`)
*   **Purpose:** To provide the structured data and definitions that drive the synthesis engine. This is the "dictionary" for the system.
*   **Atomic Documents:**
    *   `taxonomy.json`: A structured file defining all task categories and types (e.g., `DEV`, `DOC`).
    *   `style_lexicons.json`: A structured file containing the key-value terminology mappings for each output "shell" (e.g., Mythic, Professional).

---

## 2. Canonical Directory Structure

To implement this architecture, all neutral source files will be housed within a top-level `_neutral_source` directory. The structure is as follows:
```
/_Admin & Core Docs/
└── architecture/
    ├── neutral_canon_architecture.md  # The blueprint itself
    ├── identity/
    │   ├── vision.md
    │   ├── mission.md
    │   └── values.md
    ├── strategy/
    │   ├── economic_model.md
    │   └── strategic_phases.md
    ├── protocols/
    │   ├── work_breakdown_protocol.md
    │   └── task_lifecycle_protocol.md
    └── data/
        ├── taxonomy.json
        └── style_lexicons.json
```
---

## 3. Specification for `style_lexicons.json`

The `style_lexicons.json` file is the heart of the synthesis engine. It is not merely a glossary; it is the direct configuration input for the LLM that performs the translation. It provides the structured data needed to transform neutral content into a specific stylistic "shell."

### 3.1. Top-Level Structure

The file will be a JSON object where each top-level key represents a distinct output "shell" (e.g., `mythic`, `professional`).

```json
{
  "mythic": {
    "prompt_persona": "You are the Chiron Oracle, a wise and strategic guide for the Chiron Guild. Your language is insightful, strategic, and occasionally evocative, drawing from the Guild's 'Mythic Core' lore. You think in terms of forging, protocols, and directives.",
    "lexicon": {
      "neutral document": "Canonical Protocol",
      "style shell": "Operational Shell",
      "system": "Protocol",
      "process": "Workflow",
      "document": "Context Compilation",
      "task": "Guild Op",
      "contributor": "Operative",
      "group of contributors": "Chironians",
      "project phase": "Project Sector",
      "work board": "Guild Board",
      "proof of work": "Guild Seal",
      "skills registry": "Reputation Matrix",
      "task specification": "Guild Op Brief",
      "business logic": "Economic Engine",
      "roadmap": "Strategic Forging Path"
    }
  },
  "professional": {
    "prompt_persona": "You are a Senior Project Manager and Business Analyst. Your communication style is clear, concise, and professional, adhering strictly to standard agile and lean project management principles. Your output must be grounded in business value and user needs.",
    "lexicon": {
      "neutral document": "Source Document",
      "style shell": "Output Format",
      "system": "System",
      "process": "Process",
      "document": "Document",
      "task": "Task",
      "contributor": "Team Member",
      "group of contributors": "The Team",
      "project phase": "Project Phase",
      "work board": "Kanban Board",
      "proof of work": "Verified Deliverable",
      "skills registry": "Accomplishments Registry",
      "task specification": "Task Specification",
      "business logic": "Business Model",
      "roadmap": "Roadmap"
    }
  }
}
```

### 3.2. Shell Object Structure

* Each shell object will contain two primary key-value pairs: prompt_persona and lexicon.
prompt_persona (string): This is a concise instruction that primes the LLM with the required persona for the synthesis task. It sets the tone and voice.
* lexicon (object): This is an object containing key-value pairs for direct terminology substitution. The key is the neutral term (e.g., "task"), and the value is the shell-specific term (e.g., "Guild Op").

```

