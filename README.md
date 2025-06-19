# The Chiron Guild Framework

A system for organizing, executing, and tracking AI-augmented knowledge work.

[![Project Status: Phase 0 - Foundation](https://img.shields.io/badge/status-Phase%200%3A%20Foundation-blueviolet)](docs/strategic_phases.md)

This repository contains the core infrastructure for the Chiron Guild, a community building a new, more equitable model for digital work. To understand the philosophy behind our work, please read our **[Community Manifesto](docs/Guild_Manifesto.md)**.

---

## What is This, Really?

At its heart, this is a sophisticated framework built on top of familiar tools like GitHub. It's designed to create a transparent, verifiable, and highly organized system for managing projects and tracking contributions.

In its current **Phase 0**, it functions as a powerful **"Personal Operating System"** for a solo knowledge worker or a small team. You can use it to:
*   Define your work with incredible clarity.
*   Use AI assistants in a structured, repeatable way.
*   Automatically build a permanent, auditable record of everything you accomplish.

Our long-term vision is to scale this framework into a full, worker-owned digital cooperative. But we start here: by building a tool that is immensely valuable for the individual.

## Core Features (Current - Phase 0)

*   **Automated Contribution Tracking:** When you close an `issue` (a task), a GitHub Action automatically logs it to a permanent `registry.md` file, creating a verifiable record of your work.
*   **Structured Task Management:** Use our issue templates to define tasks with precision, including categories, types, dependencies, and clear acceptance criteria.
*   **AI-Powered Assistance:** We provide standardized protocols and prompts to help you use Large Language Models (LLMs) for research, planning, and content generation, ensuring your AI use is efficient and well-documented.
*   **Built on Proven Tools:** The entire system runs on the GitHub ecosystem (Issues, Actions, Pull Requests), making it robust and easy to adopt for anyone familiar with modern development workflows.

## Getting Started

You can use this framework for your own projects right now.

1.  **Fork the Repository:** Create your own copy of this repository to use as a template for your work.
2.  **Configure Secrets:** Set the necessary GitHub Secrets (like `GH_TOKEN`) to allow the GitHub Actions workflows to run correctly.
3.  **Customize Your Registry:** Edit the `data/registry.md` file to list yourself as the initial member.
4.  **Create Your First Task:** Go to the "Issues" tab and open a new issue using one of the provided templates (e.g., `[TASK]`). Fill out the details.
5.  **Do the Work:** Complete the task as described.
6.  **Log Your Accomplishment:** Close the issue. The `log-work-to-registry` action will automatically run and append your accomplishment to your personal registry.

## How to Contribute

We are actively building this framework and welcome all contributors. The best way to start is by helping us build the system itself.

1.  **See Our Project Board:** Check the **[Issues Tab](https-placeholder-for-issues-link)** to see what tasks we're currently working on.
2.  **Pick a Task:** Find an open issue that interests you, especially those labeled `good first issue`.
3.  **Follow the Process:** Follow the instructions in our **[`CONTRIBUTING.md`](CONTRIBUTING.md)** guide to get set up, do the work, and submit it for review.

Every contribution you make is a **Verified Accomplishment** that builds your reputation within our community.

## Our Vision

We are building the foundation for a new economic infrastructure—one that is owned and controlled by the people who create the value. By starting with a system that empowers the individual, we are laying the groundwork for a network of collaborators who can tackle ambitious projects, share in their success, and define a better future of work.

---

**Ready to get started? Fork this repository or check out our [contribution guide](CONTRIBUTING.md).**