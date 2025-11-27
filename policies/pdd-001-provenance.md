### **PDD-001: Provenance Rule for Core DAG Mutations**

**Strengths:**

* Clear scope and purpose: emphasizes traceability and human governance.
* Explicit principles: separates authority between Core DAG and Mesh.
* Enforcement mechanisms are actionable and mappable to ADRs + automation.
* References relevant ADRs for cross-linking.

**Suggestions for improvement:**

1. **Metadata consistency:** Use consistent casing and naming for `authors` and `scope`. For example:

```yaml
authors: [Yumin Chen, System Architecture Council]
scope: Org-wide
```

2. **Explicit “Who/What” mapping:** In Enforcement Mechanisms, note **which agent(s)** or **component(s)** enforce each rule:

```markdown
- Orchestrator (ADR-005) rejects mutations
- Governor (OPA/Rego) enforces policy
```

3. **Add “Verification” section:** Optional but helps automate compliance audits. Example:

```markdown
## Verification

- Automated audit logs confirm that each Core DAG mutation references a human-approved ADR.
- Periodic CI/CD compliance checks validate that no direct DAG edits bypass ADR approval.
```

4. **Minor Wording Refinement:** In Principles, “Mesh layer extensions may suggest semantic or structural links” → “Mesh extensions may propose semantic or lateral links but cannot mutate the Core DAG.”

---

### **PDD-000: ADR Storage & Versioning Policy**

**Strengths:**

* Clearly separates **full vs compact** Markdown usage.
* Covers automation enforcement and storage naming.
* OPA example is practical for CI/CD integration.

**Suggestions for improvement:**

1. **Metadata consistency:** Add `title` casing consistent with PDD-001:

```yaml
title: ADR Storage and Versioning Policy
```

2. **Clarify enforcement scope:** Define exactly **who or what checks for compliance**:

```markdown
- OPA policies enforce before PR merge
- CI/CD pipelines block merges if both files do not exist
- Local pre-commit hooks may optionally validate structure
```

3. **Add rationale section:** Explains *why full + compact are necessary*:

```markdown
# Rationale

- Full Markdown: Complete reference for auditors, legal, and technical stakeholders.
- Compact Markdown: Facilitates quick review, approvals, and stakeholder access.
- Dual storage prevents accidental overwrites and ensures traceability.
```

4. **Optional:** Include **example directory layout** to illustrate naming convention.
