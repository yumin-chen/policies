---
pdd_id: "PDD-20231027-006"
title: "Git Workflow and Contribution Policy"
status: "Active"
authors:
  - "Jules <jules@example.com>"
date: "2023-10-27"
scope: "Org-wide"
---

# Git Workflow and Contribution Policy

## Purpose

This document establishes a standardized Git workflow to ensure traceability, consistency, and a clear mapping between our project management tools (Kanban) and our codebase.

## Principles

- **Traceability:** Every change in the codebase should be traceable to a specific task or issue.
- **Consistency:** All contributors should follow the same process for branching, committing, and submitting changes.
- **Clarity:** The status of any given task should be easily discernible from its corresponding GitHub entity (issue, branch, or pull request).

## Enforcement Mechanisms

- **Issue and Pull Request Templates:** Standardized templates will be used to guide contributors and ensure that all necessary information is provided.
- **`CONTRIBUTING.md`:** A detailed `CONTRIBUTING.md` file in the root of the repository will serve as the primary source of documentation for this workflow.
- **Automated Checks:** GitHub Actions can be used to enforce certain aspects of this workflow, such as requiring that all pull requests are linked to an issue.

## Governance

The Engineering Leadership Team is the decision-making authority for this PDD. Any exceptions or changes to this workflow must be approved by the team.

## Rationale

This workflow provides a clear and efficient process for managing contributions to our codebase. By tightly integrating our project management tools with GitHub, we can improve visibility into the development process and make it easier for everyone to stay on the same page.
