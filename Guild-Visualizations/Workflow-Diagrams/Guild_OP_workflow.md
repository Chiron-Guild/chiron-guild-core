```mermaid
graph TD
    %% -- Theme Definition --
    classDef operative fill:#e0f7fa,stroke:#0097a7,stroke-width:2px,color:#263238;
    classDef ai fill:#e8f5e9,stroke:#388e3c,stroke-width:2px,color:#263238;
    classDef github fill:#f0f4c3,stroke:#afb42b,stroke-width:2px,color:#263238;
    classDef automated fill:#fff3e0,stroke:#ff8f00,stroke-width:2px,color:#263238;
    classDef future fill:#fce4ec,stroke:#d81b60,stroke-width:2px,color:#263238;
    classDef document fill:#eceff1,stroke:#607d8b,stroke-width:2px,color:#263238;
    classDef start_end fill:#cfd8dc,stroke:#455a64,stroke-width:2px,color:#263238;


    %% -- Lanes (Subgraphs) --
    subgraph "I. Project Inception & High-Level Briefing"
        direction LR
        start1(Start: New Project Idea) --> K_Idea
        K_Idea[Operative: Idea Generation & Initial Brainstorming]:::operative
        K_Idea -- "Requests Guidance" --> AI_Soundboard
        AI_Soundboard{AI Copilot: Strategic Sounding Board & Scope Refinement}:::ai
        AI_Soundboard -- "Refined Brief" --> K_Brief_Output
        K_Brief_Output[Operative: Refined Project Brief]:::operative
    end

    subgraph "II. Project Decomposition & Guild Op Brief Generation"
        K_Brief_Output --> K_Parent_Issue[Operative: Create Parent GitHub Issue]:::operative
        K_Parent_Issue -- "Requires Brief Gen" --> AI_Brief_Gen
        AI_Brief_Gen{AI Copilot: Guide Parent & Guild Op Brief Generation}:::ai
        AI_Brief_Gen -- "Suggests Decomposition" --> K_Decompose[Operative: Decompose into N Guild Ops]:::operative
        K_Decompose -- "Posts to GitHub" --> GH_Parent_Post(GitHub: Parent Issue Posted)
        K_Decompose -- "Posts to GitHub" --> GH_Guild_Op_Post(GitHub: N Guild Op Briefs Posted)
        GH_Parent_Post --> GH_Parent_Issue("GitHub: Parent Issue <br> (Master Brief, Tracking)"):::github
        GH_Guild_Op_Post --> GH_Guild_Op_Issues("GitHub: N Guild Op Issues <br> (status:todo)"):::github
        GH_Guild_Op_Post --> Auto_Initial_Label[Automated GitHub Action: Initial Labeling]:::automated
        Auto_Initial_Label --> GH_Guild_Op_Issues
    end

    subgraph "III. Guild Op Execution & Context Compilation"
        GH_Guild_Op_Issues -- "Selects one" --> K_Select_Op[Operative: Select Guild Op for Execution]:::operative
        K_Select_Op --> K_Work_Exec[Operative: Work Execution]:::operative
        K_Work_Exec -- "Periodically" --> AI_Context_Guide{AI Copilot: Context Compilation Guidance}:::ai
        AI_Context_Guide -- "Suggestions, Prompts" --> K_Work_Exec
        K_Work_Exec -- "Commits Changes" --> K_Git_Workflow["Operative: Git Workflow (Local Commits)"]:::operative
        K_Git_Workflow -- "Pushes to Remote" --> GH_Push_Branch["Automated GitHub Action: Branching (Feature Branch)"]:::automated
        GH_Push_Branch --> GH_Feature_Branch("GitHub: Feature Branch <br> with Context Compilations"):::github
    end

    subgraph "IV. Review, Verification & Guild Seal Awarding"
        GH_Feature_Branch --> K_Create_PR[Operative: Create Pull Request]:::operative
        K_Create_PR -- "Requests Review" --> AI_PR_Review{AI Copilot: PR Review & Scrutiny}:::ai
        AI_PR_Review -- "Feedback" --> K_Self_Review[Operative: Self-Review & Testing]:::operative
        K_Self_Review --> GH_PR_Registered(GitHub: PR Registered):::github
        GH_PR_Registered -- "Ready to Merge?" --> K_Merge_PR_Decision{Operative: Merge PR?}:::operative
        K_Merge_PR_Decision -- "Yes" --> Auto_PR_Merge["Automated GitHub Action: PR Merged (or manual)"]:::automated
        K_Merge_PR_Decision -- "No (Revisions)" --> K_Work_Exec
        Auto_PR_Merge --> K_Update_Issue[Operative: Update Guild Op Issue Status]:::operative
        K_Update_Issue --> Auto_Close_Issue["Automated GitHub Action: Guild Op Issue Closed (status:done)"]:::automated
        Auto_Close_Issue --> GH_Guild_Op_Done(GitHub: Guild Op Completed):::github

        %% Future Automation Steps
        GH_Guild_Op_Done -- "Triggers (Phase 1+)" --> Auto_Mint_Op_Sigil[Automated GitHub Action: Mint Op Sigil]:::future
        Auto_Close_Issue -- "Triggers (Phase 1+)" --> Auto_Update_Rep_Matrix[Automated GitHub Action: Update Reputation Matrix]:::future
        Auto_Update_Rep_Matrix --> Auto_Assess_Laurel[Automated GitHub Action: Assess & Issue Chironic Laurel]:::future

        Auto_Mint_Op_Sigil & Auto_Update_Rep_Matrix & Auto_Assess_Laurel --> end1(End: Chironic Laurel Awarded)
    end

    %% -- Class Assignments --
    class K_Idea,K_Brief_Output,K_Parent_Issue,K_Decompose,K_Select_Op,K_Work_Exec,K_Git_Workflow,K_Create_PR,K_Self_Review,K_Merge_PR_Decision,K_Update_Issue operative
    class AI_Soundboard,AI_Brief_Gen,AI_Context_Guide,AI_PR_Review ai
    class GH_Parent_Post,GH_Guild_Op_Post github
    class GH_Parent_Issue,GH_Guild_Op_Issues,GH_Feature_Branch,GH_PR_Registered,GH_Guild_Op_Done github
    class Auto_Initial_Label,Auto_PR_Merge,Auto_Close_Issue automated
    class Auto_Mint_Op_Sigil,Auto_Update_Rep_Matrix,Auto_Assess_Laurel future
    class start1,end1 start_end
    ```
