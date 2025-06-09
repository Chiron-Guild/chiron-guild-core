# Chiron Guild: LLM Interaction Protocols

**Version: 1.0**
**Date: June 9, 2025**
**Objective:** To define the strategic protocols for effective and token-efficient interaction with AI Co-pilots, ensuring optimal context management and maximizing the utility of AI augmentation across all Guild operations.

---

## 1. The Principle: Context Segmentation for Optimal Augmentation

AI Co-pilots, while powerful, operate within a "context window"—a limited memory of your conversation. Overloading this window with irrelevant information degrades performance, increases latency, and incurs unnecessary token costs.

The core principle of this protocol is **Context Segmentation**: Maintain distinct conversational contexts (separate chats) for different types of assistance. This allows the AI to stay focused and perform at its peak for specific tasks.

## 2. The Dual-Chat Strategy: Strategist & Engineer

Operatives will maintain at least two primary conversational contexts (separate LLM chat sessions) for distinct purposes:

### 2.1. The "Strategist" Co-pilot (Overall Advice & General Purpose)

*   **Primary Role:** This AI Co-pilot acts as your high-level strategic advisor, project manager, and philosophical guide. It is primed with the entire `Copilot_Context_Protocol.md` and maintains a long-term memory of your project's `meta_objectives`, `project_sectors`, and Guild ethos.
*   **Optimal Use Cases:**
    *   **Strategic Planning:** Decomposing new projects (Meta-Objectives, Project Sectors), high-level roadmap discussions.
    *   **Conceptual Guidance:** Brainstorming ideas, exploring ethical implications, aligning work with Guild values.
    *   **Problem-Solving (High-Level):** Diagnosing workflow bottlenecks, refining protocols, discussing operational efficiency.
    *   **Documentation Synthesis:** Summarizing `Context Compilations`, drafting overarching project documents (e.g., Project Requirements Documents).
    *   **Decision Support:** Exploring pros and cons of strategic choices.
    *   **General Troubleshooting:** High-level diagnosis of system issues, directing to relevant protocols.
*   **Context Management Strategy:**
    *   **Prioritize Long-Term Memory:** Avoid pasting large blocks of raw code, extensive debug logs, or excessively detailed technical specifications into this chat.
    *   **Summarize Inputs:** Condense lengthy external documents, logs, or code into concise summaries before providing them.
    *   **Focus on 'Why' and 'What':** Keep discussions at a strategic or conceptual level, rather than delving into the 'how' at a code level.
*   **Priming:** This Strategist Co-pilot should always be primed with the *full* `Copilot_Context_Protocol.md` at the beginning of a session or whenever its context window is reset.

### 2.2. The "Engineer" Co-pilot (Coding Focused & Technical Specifics)

*   **Primary Role:** This AI Co-pilot acts as your technical specialist, code generation engine, and debugging assistant. Its context is short-term and task-specific.
*   **Optimal Use Cases:**
    *   **Code Generation:** Writing specific functions, scripts, or code blocks (`DEV` Ops).
    *   **Debugging:** Analyzing error logs, stack traces, or specific code snippets to identify root causes.
    *   **Technical Architecture:** Discussing detailed implementation approaches, API choices, database schemas.
    *   **Regex & Pattern Matching:** Crafting complex regular expressions for data extraction or validation.
    *   **Prompt Engineering (Specific):** Refining prompts for specific, automated LLM calls (e.g., `review_generation_prompt_template.txt`).
    *   **File Parsing:** Assisting with the structure and logic of parsing specific file formats (e.g., JSON, YAML, Markdown).
*   **Context Management Strategy:**
    *   **Short-Term & Disposable:** These chats can be (and often should be) initiated for a specific technical problem and closed/reset once the problem is solved.
    *   **Raw Data Allowed:** It's acceptable to paste raw code, full error logs, or large JSON/YAML structures, as the focus is on a contained technical problem.
    *   **Focus on 'How':** Discussions here are granular and technical, directly addressing implementation details.
*   **Priming:** For new sessions, you might briefly prime with the specific project's name and relevant file paths, but avoid full Guild lore to preserve context.

## 3. Guidelines for Context Switching

Deciding which Co-pilot to engage is a critical skill for an Operative.

*   **When to start a new "Engineer" chat:**
    *   You need to write or debug a specific block of code.
    *   You are getting a technical error message that needs detailed analysis.
    *   You want to discuss a specific implementation detail that would clutter the "Strategist" chat.
    *   You are generating or refining a specific prompt template.
*   **When to return to the "Strategist" chat:**
    *   The technical problem is resolved, and you need to integrate the solution back into the broader project plan.
    *   You need to decide the *next* logical Guild Op.
    *   You require ethical or strategic guidance that transcends a specific technical challenge.
    *   You need to discuss the overall progress of a sector or project.

## 4. General Token Efficiency & Interaction Best Practices

Regardless of the Co-pilot, optimize your interactions:

*   **Be Explicit:** Clearly state your objective, desired output format, and any constraints upfront.
*   **Summarize Verbose Inputs:** Before pasting a large log or document, ask the AI to summarize it if you only need key takeaways.
*   **Prune History (If Supported):** If your LLM interface allows, periodically remove irrelevant past turns from a conversation to keep the context window focused.
*   **Iterate, Don't Dump:** Break down complex requests into smaller, sequential steps.
*   **Use Code Blocks:** Always format code, JSON, YAML, or logs using Markdown code blocks (```python, ```json, ```bash, etc.). This helps the AI parse it correctly and saves tokens.
*   **Be Clear about Output Length:** If you need a short summary, state "Provide a 3-sentence summary." If you need comprehensive details, state "Provide a detailed analysis."
*   **Review and Refine:** The AI is an assistant. Always review its output and guide it towards precision.

---
