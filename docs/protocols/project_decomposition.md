# Protocol: LLM-Assisted Project Decomposition for the Chiron Guild

**Operative:** Kin-Caid
**Version:** 1.0
**Date:** {{DATE}}
**Objective:** To provide a standardized, LLM-augmented process for decomposing complex projects into discrete, actionable `Guild Ops` suitable for the `Guild Board`. This protocol leverages a "Mythic Core, Precision Shell" approach, combining strategic oversight with AI-driven efficiency.

---

## 0. LLM Priming Protocol (Execute Once Per Session or As Needed)

**Purpose:** To establish foundational context for the LLM, ensuring its responses align with Chiron Guild terminology, objectives, and operational ethos.

**Prompt:**
```text
You are an expert project decomposition assistant for Operative Kin-Caid of the Chiron Guild. The Guild is a worker-owned, AI-augmented digital cooperative with a 'Mythic Core, Precision Shell' ethos, focused on supplanting old labor models. Key terms: 'Guild Op' (a granular task), 'Guild Seal' (verifiable credential for Op completion), 'Chironian' (Guild member), 'Guild Board' (GitHub Issues for Ops), 'Context Compilations' (structured documentation). Your goal is to help break down complex projects into clear, actionable Guild Ops. Be concise, structured, and focus on verifiable outcomes.

Phase 1: Decompiling the Monolith
1.1 LLM-Assisted Meta-Objective Definition
 * Goal: To distill the project's core purpose into a single, potent Meta-Objective statement.
 * Operative Input: A raw description of the project, its intended value, any initial thoughts or goals.
 * LLM Prompt Framework:
   System: You are an expert project analyst.
User:
Project Title/Concept: [Your Project Title/Concept Here]

Raw Project Description:
[Paste your detailed project description, goals, pain points it solves, desired future state for the Chiron Guild.]

Task:
Based on the project description for the Chiron Guild, draft 3-5 concise, compelling Meta-Objective statements. Each statement should be a single sentence capturing the absolute core purpose and primary value proposition of this project. Focus on the ultimate 'win.' Label them M1, M2, M3, etc.

 * Expected LLM Output: 3-5 potential Meta-Objective sentences.
 * Operative Action (Human Filter): Review LLM suggestions. Select the most resonant Meta-Objective or synthesize a new one. This choice is strategic and aligns with the Guild's core mission.
1.2 LLM-Assisted Strategic Chunking (Sector Identification)
 * Goal: To break down the chosen Meta-Objective into 3-5 major logical phases or components (Sectors).
 * Operative Input: The finalized Meta-Objective from step 1.1. Optional: 1-2 sentences of additional high-level project context.
 * LLM Prompt Framework:
   System: You are an expert systems architect.
User:
Meta-Objective: [Your Finalized Meta-Objective from step 1.1]
Project Context: [Optional: 1-2 sentences of additional context, e.g., "This is for the Chiron Guild, a digital cooperative. The solution will likely involve X and integrate with Y."]

Task:
Based on the Meta-Objective, propose 3-5 major, distinct Sectors (logical phases or key components) required to achieve it. For each Sector, provide a short descriptive name and a 1-sentence summary of its focus. Structure the output as a numbered list.
Example Sector Format:
1.  **Sector Name:** [e.g., Core Infrastructure Setup]
    * Summary: [e.g., Establish the foundational platform and server environment.]

 * Expected LLM Output: A list of 3-5 named and summarized Sectors.
 * Operative Action: Evaluate the proposed Sectors for logical flow, comprehensiveness, and distinction. Adjust, merge, or add Sectors as necessary to define the high-level project architecture.
1.3 LLM-Assisted Granular Op Identification (Per Sector)
 * Goal: For each Sector identified in step 1.2, brainstorm a list of potential, discrete, actionable Guild Ops.
 * Operative Input: One specific Sector Name and its Summary (from step 1.2). The overall Meta-Objective for context.
 * LLM Prompt Framework (Execute for each Sector):
   System: You are an expert task analyst for the Chiron Guild.
User:
Meta-Objective (Overall Project): [Your Finalized Meta-Objective]
Current Sector for Decomposition:
* Sector Name: [Name of the Sector from step 1.2]
* Sector Summary: [Summary of the Sector from step 1.2]

Task:
For the Sector named "[Sector Name]," generate a list of 5-10 potential granular Guild Ops needed to complete its objectives. For each Guild Op:
1.  Suggest a clear, action-oriented **Op Title**.
2.  Indicate its likely **Op Type** (`DEV` for development/technical tasks, `DOC` for documentation/research, `GOV` for governance/decision-making).
3.  Briefly state the **Primary Deliverable** or verifiable outcome (this will inform the Guild Seal).

Structure the output as a bulleted list for each Guild Op. Ensure Ops are discrete and actionable.

Example Output Format:
* Op Title: Research & Select Self-Hosted Chat Platform
    * Op Type: DOC
    * Primary Deliverable: Recommendation report with top 3 platforms, pros/cons.
* Op Title: Provision Server for Chat Platform
    * Op Type: DEV
    * Primary Deliverable: Server provisioned and accessible with basic security hardening.

 * Expected LLM Output: A list of candidate Guild Ops for the specified Sector.
 * Operative Action (Critical Human Oversight):
   * Filter: Discard irrelevant or poorly defined Op suggestions.
   * Refine: Sharpen Op Titles and clarify Primary Deliverables. Ensure atomicity and verifiability for Guild Seal issuance.
   * Add: Identify and include any missing Ops. Consider dependencies between Ops.
   * Consolidate: Merge Ops if they are too fragmented or overly granular.
2. Hiro's Pro-Tips for LLM Interaction (Precision Shell Tactics)
 * Iterate on Prompts: If initial LLM outputs are suboptimal, refine your prompt. Add more context, specify the desired format, or adjust constraints. Treat prompt engineering as a debugging process.
 * Maintain Session Continuity: For some LLMs, periodically restating key context (e.g., the Meta-Objective or the LLM Priming Protocol) can improve the relevance and consistency of responses throughout a longer interaction.
 * Leverage "Temperature" Controls (If available):
   * For brainstorming tasks (e.g., Granular Op Identification), a slightly higher temperature setting can encourage more diverse and creative suggestions.
   * For refinement or definition tasks (e.g., Meta-Objective Definition), a lower temperature setting promotes more focused and deterministic output.
 * System Prompts are Key: Use the "System" role in your prompts to define the LLM's persona and task clearly. This helps frame its responses effectively.
End of Protocol