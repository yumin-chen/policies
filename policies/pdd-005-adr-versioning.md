---
pdd_id: pdd-000-adr-versioning
title: ADR Storage & Versioning Policy
status: Proposed
date: 2025-11-27
authors:
  - System Architecture Council
scope: Organization-wide
---

# Purpose

Ensure all ADRs are stored in both **full** and **compact** Markdown versions to support:

- Compliance and auditability  
- Review and approval efficiency  
- Traceability and version control  
- Automation enforcement via OPA or equivalent policies

# Principles

## 1. Separation of Concerns

- **Full Markdown:** Intended for implementation, audit, and compliance.  
- **Compact Markdown:** Intended for reviews, approvals, and reference.  
- Files **must be stored separately** to prevent accidental edits in one affecting the other.

## 2. Version Control & Traceability

- Each version must have its **own commit, diff, and history**.  
- Stakeholders may reference the compact version without exposing detailed implementation notes.

## 3. Automation & Policy Enforcement

- OPA or equivalent policies **must validate the existence of both versions** before an ADR is considered committed.  
- PR, CI/CD, and workflow automation **must enforce this policy**.  

## 4. Storage Naming Convention

- **Full Markdown:** `adr-<id>-<title>-full.md`  
- **Compact Markdown:** `adr-<id>-<title>-comp.md`  
- Both files reside in the **same directory** (e.g., `architectural/design/`) but remain separate files.

# Enforcement Mechanism

### OPA Rego Example

```rego
package org.adr

default adr_storage_compliant = false

adr_storage_compliant {
    adr := input.adr
    adr.full_md_path != ""      # Full Markdown must exist
    adr.compact_md_path != ""   # Compact Markdown must exist
}
