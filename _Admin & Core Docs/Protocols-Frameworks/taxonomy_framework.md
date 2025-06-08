# Chiron Guild: Operational Taxonomy Framework

**Version:** 1.1
**Objective:** To define a clear and comprehensive taxonomy for all types of operations undertaken within the Chiron Guild. This framework will guide the creation of `Guild Op IDs`, labeling on the `Guild Board`, and the overall organization of work.

---

## 1. The Universal Unit: The `Guild Op`

At the heart of all activity within the Chiron Guild is the **`Guild Op`**.

* **Definition:** A `Guild Op` is the fundamental, discrete, actionable task or directive managed through the Guild's systems (primarily the `Guild Board` on GitHub Issues). Each `Guild Op` has a defined objective, deliverables, and associated `Guild Seals` upon completion.

---

## 2. Primary Guild Op Categories (Context & Origin)

While "Guild Op" is the universal term, Ops are further categorized by their primary context, origin, or overarching purpose. This is typically reflected in the `[PROJECT_ID]` segment of a `Guild Op ID`.

### A. `CORE` - Core Guild Operations

* **Purpose:** These Ops are dedicated to the **self-assembly, maintenance, governance, and evolution of the Chiron Guild itself.** This includes building and refining its infrastructure, core protocols, internal tools, community initiatives, and foundational documentation. These are the tasks that directly forge the Guild.
* **`PROJECT_ID` Prefix Examples:** `CHIRON`, `GUILD`, `INFRA`, `PROTOCOL`
* **Repository Path:** Projects/chiron/Guild Ops/[project-slug]/ (e.g. Projects/chiron/Guild Ops/[CHIRON-DEV-001])
* **Example `Guild Ops`:**
    * `CHRN-DEV-001: Implement Automated Laurel Award System`
    * `PROTOCOL-DOC-003: Draft and Ratify Membership Onboarding Protocol`
    * `GUILD-GOV-002: Establish Initial Guild Treasury Management Strategy`

### B. `PERS` - Personal Development & Professional Operations

* **Purpose:** Initiated by an individual **Operative for their personal skill development, learning endeavors, creative projects, or for managing and documenting their professional work-related projects** (e.g., tasks from external employment or freelance engagements). These Ops utilize Guild methodologies (decomposition, `Context Compilations`, `Guild Seals`) to structure and validate personal and professional growth, achievement, and contribution. This creates a verifiable record that can be leveraged for portfolio building, performance reviews (e.g., generating summaries for annual reviews), and showcasing a holistic skill set.
* **`PROJECT_ID` Prefix Examples:** Operative's unique alias (e.g., `KCAD` for Kin-Caid, `OP007`)
* **Repository Path:** Projects/personal/[project-slug]/ (e.g. Projects/personal/creek_connections)
* **Example `Guild Ops`:**
    * `KCAD-CRAFT-001: Master Basic Pottery Wheel Centering Techniques`
    * `OP007-LRN-002: Complete Advanced Course in AI Ethics and Application`
    * `KCAD-DEV-003: Build Personal Portfolio Website Showcasing Guild Seals`
    * `KCAD-STR-004: Develop and Execute Q3 Marketing Strategy (External Client Project Alpha)`
    * `OP007-DOC-005: Produce Technical Documentation Suite for [Work Project Name] (Professional Task)`

### C. `BNTY` - Bounty Board Operations

* **Purpose:** These Ops arise from the **Chiron Guild `Bounty Board`**. They typically involve the collaborative development of innovative products, services, tools, or protocols proposed by Operatives, often with the goal of external monetization and equitable reward distribution among contributors and the Guild.
* **`PROJECT_ID` Prefix Examples:** A unique identifier for the specific Bounty (e.g., `AIDM` for "AI Dungeon Master," `SOLARPNK`)
* **Repository Path:** Projects/bounty/[project-slug]/ (e.g. Projects/county/BOUNTY-GAME-ALPHA)
* **Example `Guild Ops`:**
    * `AIDM-DSN-001: Design UI/UX Mockups for AI Dungeon Master MVP`
    * `SOLARPNK-STR-002: Research Market Viability for Decentralized Energy Protocol`
    * `AIDM-GOV-003: Define IP Ownership and Revenue Share Model for Bounty Projects`

### D. `CLIENT` - External Client Operations (Guild-Contracted)

* **Purpose:** These Ops represent **work undertaken by the Chiron Guild as a collective (often by self-organizing `Shadowrunner` teams of Operatives) for external clients, partners, or organizations.** This category covers consultancy, project development, or services rendered under a Guild contract, generating revenue or strategic value for the Guild and participating Operatives. This is distinct from `PERS` Ops where an individual manages their own external work through the Guild system for personal tracking.
* **`PROJECT_ID` Prefix Examples:** A code for the external client or project (e.g., `ACMECO`, `NGOINIT`)
* **Repository Path:** Projects/client/[project-slug]/ (e.g. Projects/client/Guild Ops/CLIENT-ACME-PROJECT_X)
* **Example `Guild Ops`:**
    * `ACMECO-DEV-001: Develop Custom Data Analytics Dashboard for Acme Corp (Guild Contract)`
    * `NGOINIT-STR-002: Provide Strategic Consultation on AI Integration for Non-Profit Initiative (Guild Contract)`
    * `ACMECO-QAT-003: Conduct Comprehensive Security Audit for Acme Corp's Web Platform (Guild Contract)`

Note on Automation: The canonical mapping between a PROJECT_ID prefix and its specific Repository Path is maintained in the root project_mappings.json file. This file serves as the single source of truth for all automated Guild workflows that need to locate project-specific directories.
---

## 3. Work Type Designators (`OP_TYPE`)

Within each Primary Guild Op Category, the specific *nature of the work* being performed is defined by an `OP_TYPE`. This is the second segment of a standard `Guild Op ID` (e.g., `[PROJECT_ID]-[OP_TYPE]-[NUM_ID]`).

The established `OP_TYPE`s are:

* **`DEV`**: Development (software, systems, tools, technical implementation)
* **`DSN`**: Design (UI/UX, graphic, system architecture, product design)
* **`DOC`**: Documentation (writing, editing, research, protocol creation, `Context Compilations`)
* **`GOV`**: Governance (policy making, legal frameworks, decision processes, community standards)
* **`STR`**: Strategy (planning, market analysis, vision setting, roadmap development)
* **`QAT`**: Quality Assurance & Testing (software testing, process auditing, validation)
* **`COM`**: Communication & Marketing (outreach, content creation for promotion, community engagement strategy)

**Potential `OP_TYPE` Additions for Consideration (especially for `PERS` Ops):**

* **`LRN`**: Learning (focused acquisition of new knowledge or theoretical understanding – distinct if the primary output isn't just documentation)
* **`CRAFT`**: Craftsmanship (physical creation, making, artistry – for projects like ceramics, woodworking, etc.)
* **`PRAC`**: Practice (dedicated practice of a specific skill, physical or digital, where the act of practice and its logged reflection is the core)
* **`PROJ`**: Project Management (specifically for Ops focused on the coordination, planning, and delivery of a larger initiative, often seen in professional work)

The decision to add these new `OP_TYPE`s would depend on the frequency and distinct nature of such Personal Development Ops. For now, many learning, craft, and project management activities can be framed using existing types. Adding `PROJ` might be particularly useful for distinguishing `PERS` ops that are about managing external work projects.

---

## 4. Implications for Guild Systems

* **`Guild Op ID` Structure:** The `[PROJECT_ID]` will clearly indicate the Op's category (e.g., `CHRN-DEV-001`, `KCAD-CRAFT-002`, `KCAD-PROJ-001`).
* **`Guild Board` Labeling:** GitHub Issues representing `Guild Ops` should be labeled with:
    * A primary category label (e.g., `Context:CORE`, `Context:PERS`, `Context:BNTY`, `Context:EXTN`).
    * A work type label (e.g., `Work:DEV`, `Work:DOC`, `Work:PROJ`).
* **`Guild Seal` & `Chironic Laurel` Logic:** The categorization can inform the types of Seals awarded and the criteria for certain Laurels.

This taxonomy aims to provide a robust and flexible framework for organizing all Guild activities, ensuring clarity for current and future Operatives.
