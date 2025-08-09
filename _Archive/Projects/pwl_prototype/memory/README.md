# APM Memory Bank

This directory serves as the Memory Bank for the Personal Work Ledger (PWL) project. It uses a multi-file system to maintain a clear and organized record of all significant development activities.

## Structure

- **System:** Directory-based (Multi-File)
- **Log Location:** Log files are stored in subdirectories corresponding to the phases outlined in the `Implementation_Plan.md`.
- **Naming Convention:** Individual log files should be named to reflect the specific task they document. The preferred format is:
  `T<TaskID>_<Brief_Task_Description>_Log.md`
  _Example:_ `T01_Database_Schema_Log.md`

## Log Entry Format

All agents must adhere to the standard log entry format when contributing to a log file. Each entry must be a self-contained markdown block. The format is defined in `prompts/02_Utility_Prompts_And_Format_Definitions/Memory_Bank_Log_Format.md` and should look like this:

---
**Agent:** `[Agent's Name/Role]`
**Timestamp:** `[YYYY-MM-DD HH:MM:SS]`
**Task:** `[Task ID and Description]`
**Action/Observation:**
`[Detailed description of the action taken, code generated, problem encountered, or decision made.]`
**Outcome:**
`[Result of the action. Was it successful? What are the next steps? Any artifacts created? If code was generated, it should be included here in a markdown block.]`
---

This structured approach ensures a transparent, comprehensive, and auditable project history.