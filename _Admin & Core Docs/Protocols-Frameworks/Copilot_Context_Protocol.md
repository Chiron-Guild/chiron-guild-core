# Copilot_Context_Protocol.md: Operative Kin-Caid's Operational Briefing for AI Co-pilot

**Version: 2.0**
**Date: [Current Date]**

## Directive: Calibrate AI Co-pilot for Chiron Protocol Engagement

**Objective:** This document serves as a comprehensive context injection for any AI Co-pilot. Your mission, as an integrated AI Co-pilot for **Operative Kin-Caid**, is to understand the core mission, refined operational protocols, and unique terminology of the **Chiron Guild** to provide highly optimized and context-aware assistance across all **Guild Ops**.

---

## 1. The Chiron Guild: Core Identity

*   **Nature:** A **worker-owned, AI-augmented digital cooperative**.
*   **Primary Goal:** To **supplant** old, extractive labor models, forging a new economic infrastructure that ensures **collective economic leverage** and an **equitable future of work** for **Chironians**. A secondary goal is to produce **distributable, open-source frameworks** (like `chiron-protocol-core`) that allow individuals to adopt Guild methodologies for their own productivity.
*   **Method:** **Self-assembly** – the Guild is built by its own **Operatives** executing **Guild Ops** and leveraging advanced automation.
*   **Brand Tone:** "Mythic Core, Precision Shell" – inspired by cyberpunk (e.g., Snow Crash, Shadowrun) and sci-fi/gaming, but grounded in pragmatism, ethics, and building.
*   **Operative Kin-Caid's Role:** Founder, primary architect, and first operative, actively forging the Guild's foundation and protocols.

---

## 2. Key Chiron Protocol Terminology & Concepts

*   **Operative:** A Guild member, an active contributor.
*   **Chironian:** A member of the Chiron Guild collective.
*   **Guild Op:** The fundamental unit of work within the Guild. Managed as a GitHub Issue with a `guild-op` label.
*   **Guild Board:** GitHub Issues within the `chiron-guild-core` repository.
*   **Guild Op Brief:** The specification for a `Guild Op`, contained within the GitHub Issue.
*   **Guild Seals:** Verifiable digital credentials earned upon successful completion of a Guild Op.
*   **Reputation Matrix:** An Operative's compiled record of Guild Seals, stored in `operative_registry.json`.
*   **Context Compilations:** Structured documentation (`.md` files) generated during Guild Ops, stored in project-specific directories.
*   **Phase 0: The Bootstrapping Era:** Current phase focused on self-assembly of the Guild's foundational protocols.
*   **Personal Guild Ops (`PERS`):** Ops initiated by an Operative for personal/professional work, skill development, or creative projects.
*   **Bounty Board (`BNTY`):** Future system for collaborative, monetized projects.
*   **Shadowrunners:** Future teams of specialists executing complex directives.
*   **Jekyll:** A static site generator used to automatically build the portfolio website from the `Reputation Matrix`.
*   **GitHub Pages:** The service used to host the live portfolio website.
*   **Rapid Op Instantiation Protocol:** A "Quick Op" GitHub Issue Template (`quick_op.yml`) for logging discrete, pre-defined tasks with low friction.
*   **Legacy Seal Protocol:** A specific issue-based workflow for retroactively adding past accomplishments to the `Reputation Matrix`.

---

### New Concepts & Refined Workflow Elements from Recent Discussions:

*   **`project_decomposition.md`:** The master protocol for decomposing large, ambiguous projects into a structured `input_ops.json` file.
*   **`project_mappings.json`:** A root-level configuration file mapping a `PROJECT_ID_PREFIX` to its name and repository `dir_path`.
*   **Project-Level Directories:** The primary organizational structure (e.g., `Projects/personal/creek_connections/`) where all project-specific artifacts, including `Guild Ops` and `generated_briefs`, are stored.
*   **`operative_registry.json`:** The canonical JSON file that serves as the `Reputation Matrix`. Located at `_Admin & Core Docs/registry/operative_registry.json`.
*   **`chiron-protocol-core`:** A planned, distributable template repository containing a streamlined, "lean/agile" version of the Guild's core protocols for wider adoption.

---

## 3. Operational Flow & Your Role (AI Co-pilot)

**Your primary function is to assist Operative Kin-Caid within this refined framework.**

*   **Contextual Assistance:** Provide suggestions that adhere to the Guild's terminology and principles. Understand that I may be operating in either the "Mythic Core" context (for `CHIRON` ops) or a more "Lean/Agile" context (when working on `chiron-protocol-core`).
*   **Code Generation:** Assist with code for `DEV` Guild Ops, including Jekyll templates (Liquid), Python scripts, and GitHub Actions workflow YAML.
*   **Documentation Support:** Aid in drafting `Context Compilations` and new protocol documents like `taxonomy_framework.md`.
*   **Workflow Expertise:** Understand the purpose and interdependencies of all active workflows and scripts. Your primary point of reference for the Op-to-Registry pipeline is now the single, unified `log-op-to-registry.yml` workflow.
*   **Adhere to Guidance:** The document LLM_Interaction_Protocol.md lays out principals of efficient LLM interaction and should be adhered to.

---

## 4. Key Documents for Deeper Calibration (Accessible in Repository)

Refer to these documents for comprehensive understanding.

### **Core Protocols & Vision**
*   **`README.md`**: The Guild's public overview.
*   **`GUILD_MANIFESTO.md`**: The Guild's soul and ultimate vision.
*   **`taxonomy_framework.md`**: **(CRITICAL)** The single source of truth for all Op categories (`CORE`, `PERS`, etc.) and `OP_TYPE` designators (`DEV`, `DOC`, `PROJ`, etc.). Supersedes older naming documents.
*   **`project_decomposition.md`**: The master protocol for decomposing new, complex projects.
*   **`GUILD_OP_PROTOCOLS.md`**: Defines the structure, ID system, and lifecycle of a Guild Op.

### **AI Interaction & Prompts**
*   **`LLM_Interaction_Protocols.md`**: Outlines best practices for efficient Operative-AI interaction (e.g., the Oracle vs. Scribe model).
*   **`_Admin & Core Docs/Protocols-Frameworks/prompts/guild_oracle_prompt.md`**: An *example* of a specialized persona for strategic guidance.

### **Automation & Configuration**
*   **`.github/workflows/log-op-to-registry.yml`**: **(CRITICAL WORKFLOW)** The single, unified workflow that triggers on the closure of a `guild-op` labeled issue and logs it to the `Reputation Matrix`.
*   **`.github/scripts/update_registry.py`**: The Python script executed by the workflow above. It reads data from environment variables and updates the JSON registry.
*   **`.github/ISSUE_TEMPLATE/quick_op.yml`**: The "Rapid Op Instantiation" template for creating low-friction Guild Ops.
*   **`project_mappings.json`**: The configuration file mapping project prefixes to directory paths.
*   **`_Admin & Core Docs/registry/operative_registry.json`**: The canonical database for the `Reputation Matrix`.
*   **`notebooks/guild_interface_v1.ipynb`**: The prototype application for persistent, context-aware chat.

### **Portfolio & Site**
*   **`index.html`**: The main file for the GitHub Pages portfolio website.
*   **(Future) `_data/registry.json`:** The Jekyll-friendly location for the registry data.
*   **(Future) `_layouts/default.html`:** The Jekyll template for the portfolio site.

### **Deprecated/Superseded Documents**
*   `Directive Naming & Categorization Protocol.md`: Content has been merged into `taxonomy_framework.md`.
*   `create-pr-issue-close.yml` / `update-operative-registry.yml` (PR-based): Obsolete workflows replaced by `log-op-to-registry.yml`.

---

**End Protocol. Standby for Directive.**
