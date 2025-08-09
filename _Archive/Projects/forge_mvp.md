# Guild System MVP: Core Components

This document outlines the Minimum Viable Products (MVPs) for the core components of the Guild system: Curriculum ("Genesis Path"), AI Mentor ("Oracle"), and Seal Verification ("Peer Review Council").

## 1. Curriculum MVP: The "Genesis Path"

**Goal:** To guide an apprentice from zero knowledge to being "Bounty-ready" on a single, well-defined track. Specialized tracks will be deferred for V2.

**Focus:** Linear sequence of 5-7 core Guild Operations (Guild Ops) focusing on LLM-assisted back-end development.

**The "Genesis Path" Guild Ops:**

*   **Op 001: The Prompt Brief**
    *   **Task:** Apprentice is given a simple problem (e.g., "create a function that sorts a list of users by age"). They must write a detailed, structured prompt specification for an LLM to solve it.
    *   **Core Skill:** Problem Decomposition
*   **Op 002: Generation & First Review**
    *   **Task:** Apprentice feeds their Op 001 brief into the chosen LLM. They then review the generated code, annotating it line-by-line to explain what each part does.
    *   **Core Skill:** Code Comprehension and AI Output Analysis
*   **Op 003: The Debugging Loop**
    *   **Task:** Apprentice is provided with AI-generated code that has a subtle, known bug. They must use the AI Mentor (see below) to diagnose and fix the problem.
    *   **Core Skill:** Human-in-the-Loop Verification
*   **Op 004: Refactoring for Clarity**
    *   **Task:** Apprentice takes a piece of functional but messy code and uses the AI Mentor to refactor it for readability and efficiency, adhering to Guild protocol.
    *   **Core Skill:** Quality Assurance and Protocol Adherence
*   **Op 005: Simple Integration**
    *   **Task:** Apprentice is given two separate, functional code modules (e.g., a "user creation" function and a "database entry" function) and must write the "glue" code to make them work together.
    *   **Core Skill:** Basic Systems Integration

**Outcome:** A direct, practical path to creating a worker who can be a useful junior member of a Forge Team.

## 2. AI Mentor MVP: The "Oracle"

**Goal:** Provide a powerful, constrained assistant to answer questions and automate tasks. Not a fully sentient tutor; focused on functionality, not conversation.

**Core Features:**

*   **Error Message Explainer:**
    *   Apprentice highlights an error message and asks, "Explain this."
    *   The AI provides a simple, plain-language explanation and suggests 2-3 common causes.
*   **Context-Aware Q&A:**
    *   The Oracle is fed all Guild documentation, protocols, and details of the current Guild Op.
    *   Apprentice can ask direct questions (e.g., "What is the Guild's preferred method for authenticating a user?").
    *   Answers are based solely on curated knowledge.
*   **On-Demand Code Generation:**
    *   Apprentice writes a comment (e.g., `// create a python class for a User with name and email`) and asks the Oracle to generate the code block.
    *   Offloads syntax memorization.

**What's Not Included (for the MVP):** Proactive suggestions, conversational dialogue, or performance tracking. The Oracle is a tool, not a teacher; teaching comes through the Guild Ops structure.

## 3. Seal Verification MVP: The "Peer Review Council"

**Goal:** To ensure that a Guild Seal is "proof that can't be faked." Prioritizes quality over complexity, deferring automated systems.

**Process:**

*   **Submission:**
    *   Apprentice completes a Guild Op and submits it for verification.
    *   Submission includes the final product (e.g., the code) and a brief write-up of their process.
*   **Council Review:**
    *   Submission is randomly assigned to a "Peer Review Council" of three certified Operatives who have already passed that Op.
*   **Checklist-Based Adjudication:**
    *   Reviewers use a simple, objective checklist defined in the Op Brief (e.g., "Does the code run without errors? Y/N").
    *   Reviewers verify compliance, not providing subjective feedback.
*   **Issuance or Rejection:**
    *   If at least two out of the three reviewers approve the submission, the apprentice is automatically and cryptographically issued their Guild Seal for that Op.
    *   If not, they receive anonymized checklist feedback and must revise and resubmit their work.
