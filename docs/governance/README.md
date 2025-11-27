# Governance Policies

This directory contains Open Policy Agent (OPA) policies used to enforce governance rules across the SDLC_IDE ecosystem.

## Policies

| Policy File | Description | Namespace |
|---|---|---|
| `adr_policy.rego` | Enforces ADR naming conventions and sequential numbering. | `sdlc.governance` |
| `mesh_policy.rego` | Validates Mesh extension schemas and allowed edges. | `sdlc.governance.mesh` |
| `vendor_lock_policy.rego` | Prevents the use of vendor-locked or proprietary technologies. | `sdlc.governance.vendor` |
| `adr_template_policy.rego` | Validates ADRs against the mandatory template structure. | `sdlc.governance.adr_template` |
| `adr_storage_policy.rego` | Enforces dual-file storage (full & compact) for ADRs. | `sdlc.governance.adr_storage` |

## Running Policy Checks

You can use `conftest` to verify compliance locally.

### Prerequisites
- [Conftest](https://www.conftest.dev/) installed.

### Commands

**Validate ADRs:**
```bash
conftest test docs/architecture/design/ \
  --policy docs/governance/policies/adr_policy.rego \
  --namespace sdlc.governance
```

**Validate Mesh Extensions:**
```bash
conftest test docs/mesh/extensions/ \
  --policy docs/governance/policies/mesh_policy.rego \
  --namespace sdlc.governance.mesh
```

**Check for Vendor Lock-in:**
```bash
conftest test . \
  --policy docs/governance/policies/vendor_lock_policy.rego \
  --namespace sdlc.governance.vendor
```

**Validate ADR Template Compliance:**
```bash
conftest test docs/architecture/design/ \
  --policy docs/governance/policies/adr_template_policy.rego \
  --namespace sdlc.governance.adr_template
```

**Validate ADR Storage Compliance:**
```bash
conftest test docs/architecture/design/ \
  --policy docs/governance/policies/adr_storage_policy.rego \
  --namespace sdlc.governance.adr_storage
```
