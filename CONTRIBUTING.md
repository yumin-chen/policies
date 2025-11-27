# Contributing to this Repository

We welcome contributions from everyone. To ensure a smooth and consistent development process, we have established a set of guidelines for contributing to this repository.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Git Workflow](#git-workflow)
- [Branch Naming Conventions](#branch-naming-conventions)
- [Commit Message Format](#commit-message-format)
- [Submitting a Pull Request](#submitting-a-pull-request)

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## Getting Started

1.  **Create an issue:** Before you start working on a new feature or bug fix, please create an issue to discuss it with the maintainers.
2.  **Fork the repository:** Fork the repository to your own GitHub account.
3.  **Clone the repository:** Clone your forked repository to your local machine.

## Git Workflow

We use a Kanban-style workflow that is tightly integrated with GitHub. The following table maps our Kanban columns to GitHub entities:

| Kanban Column   | Git / GitHub Entity             | How to Use                                                                                                                                                 |
| --------------- | ------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **To Do**       | Issue / Backlog                 | Create an **issue** for every task. Leave it **open** and assign a label like `To Do`. This is your “task pool.”                                           |
| **In Progress** | Feature branch / assigned issue | Developer creates a **branch** off `main` (or `develop`) named after the issue, e.g. `feature/core-dag-scaffold`. Update the issue label to `In Progress`. |
| **Review**      | Pull Request                    | Once the branch is ready, open a **PR** targeting `main` (or `develop`). Label it `Review`. Assign reviewers. PR represents the “in review” state.         |
| **Done**        | Merged PR / Closed Issue        | After PR merge: close the issue automatically (or manually) and label it `Done`. Branch can be deleted.                                                    |

## Branch Naming Conventions

We use the following convention for branch names:

`<type>/<issue-id>-<short-description>`

-   **`<type>`:** `feature`, `fix`, `chore`, `docs`
-   **`<issue-id>`:** The ID of the issue you are working on (e.g., `CORE-1`)
-   **`<short-description>`:** A brief, kebab-case description of the changes.

**Examples:**

-   `feature/CORE-1-scaffold-dag`
-   `fix/MESH-2-api-bug`
-   `chore/DOC-1-readme-update`

## Commit Message Format

We use the following format for commit messages:

`<issue-id>: <short-description>`

**Example:**

`CORE-1: scaffold DAG module`

## Submitting a Pull Request

1.  Push your changes to your forked repository.
2.  Open a pull request to the `main` branch of the upstream repository.
3.  Fill out the pull request template, making sure to link to the issue you are addressing.
4.  Request a review from at least one maintainer.
