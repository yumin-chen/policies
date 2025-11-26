# Principal Decision Documents (PDDs)

This repository contains **Principal Decision Documents (PDDs)** for organization-wide governance, policies, and rules.  
It serves as the **single source of truth** for all cross-project decisions and is designed for discoverability, compliance, and automation.

---

## Table of Contents

- [Purpose](#purpose)  
- [Repository Structure](#repository-structure)  
- [Adding or Updating PDDs](#adding-or-updating-pdds)  
- [Policy Enforcement](#policy-enforcement)  
- [Governance and Approval](#governance-and-approval)  
- [Reference & Links](#reference--links)

---

## Purpose

- Centralize all **org-wide policies** and **principal decisions**.  
- Ensure **consistency**, **traceability**, and **compliance** across all projects.  
- Serve as the **source of truth** for automated policy enforcement, including OPA and CI/CD checks.

---

## Repository Structure

```

policies/
├── PDD-ADR-VERSIONING.md           # ADR storage & versioning policy
├── PDD-SECURITY-GUIDELINES.md      # Security standards and protocols
├── PDD-CODE-OWNERSHIP.md           # Code ownership and review rules
└── README.md                       # This documentation

```

- Each PDD is a separate Markdown file.  
- Metadata headers should include:
  - `pdd_id`  
  - `title`  
  - `status` (Proposed / Active / Approved)  
  - `authors`  
  - `date`  
  - `scope` (Org-wide or specific projects)

---

## Adding or Updating PDDs

1. Create a new Markdown file following the naming convention:  
   `PDD-<TITLE>.md`  

2. Include **metadata headers** at the top of the file.  

3. Follow the **PDD template**:
   - Purpose  
   - Principles  
   - Enforcement Mechanisms  
   - Governance  
   - Rationale  

4. Submit a **pull request** for review and approval.  

5. Upon approval, the PDD is merged and becomes **effective immediately**, unless otherwise stated.

---

## Policy Enforcement

- Automated checks can reference this repository for **OPA policy evaluation**, CI/CD validations, and audit reporting.  
- Example enforcement includes:  
  - Validating ADR storage (full + compact Markdown versions)  
  - Ensuring project compliance with org-wide standards  
  - Automatic rejection of non-compliant pull requests  

---

## Governance and Approval

- **Decision Authority:** System Architecture Council or equivalent org-wide governance body  
- **Review Process:** All proposed PDDs must go through formal review and approval via pull request  
- **Exceptions:** Only allowed via council resolution  

---

## Reference & Links

- [PDD Template](./TEMPLATE-PDD.md) — For creating new Principal Decision Documents  
- [OPA Policies](../opa-policies/) — Example Rego policies enforcing PDD rules  
- [SDLC_IDE ADRs](../adrs/) — Related project-level ADR repository
```

