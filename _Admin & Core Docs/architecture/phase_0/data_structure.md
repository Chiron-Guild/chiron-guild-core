# Conceptual Data Structure (for Phase 0)

This is a logical model. For Phase 0, the "database" is simply the GitHub repository and its text files.

### **Key Entities**

1.  **`Member`**
    *   **Description:** The individual user/owner of the repository. In Phase 0, this is a single, implicit entity.
    *   **Attributes:**
        *   `github_username` (string): The user's unique GitHub handle.
    *   **Storage:** Implicitly the repository owner; explicitly listed in `registry.md`.

2.  **`Task`**
    *   **Description:** A discrete unit of work, perfectly represented by a GitHub Issue.
    *   **Attributes:**
        *   `task_id` (integer): The GitHub Issue number.
        *   `title` (string): The clear, descriptive title of the task.
        *   `description` (text): The body of the issue, following a template.
        *   `status` (enum): Open, Closed.
        *   `assignee` (string): The `github_username` of the member responsible.
        *   `labels` (array of strings): Categories for the task (e.g., `Type:Bug`, `Project:Chiron`, `Category:Docs`).
        *   `created_at` (datetime): Timestamp of creation.
        *   `closed_at` (datetime): Timestamp of completion.
    *   **Storage:** GitHub Issues.

3.  **`Contribution`**
    *   **Description:** A permanent record of a completed task. It is the manifestation of "Verifiable Provenance."
    *   **Attributes:**
        *   `contribution_id` (string): A unique identifier (e.g., a hash or timestamp).
        *   `task_id` (integer): Foreign key linking to the `Task`.
        *   `member_username` (string): Foreign key linking to the `Member`.
        *   `completion_date` (date): The date the task was closed.
        *   `summary` (string): The title of the completed task.
    *   **Storage:** A formatted line item within the `data/registry.md` file.

### **Relationships**

*   A `Member` can be assigned many `Tasks`.
*   A `Task`, when its `status` becomes "Closed," generates exactly one `Contribution`.
*   A `Contribution` belongs to exactly one `Member` and is derived from exactly one `Task`.
