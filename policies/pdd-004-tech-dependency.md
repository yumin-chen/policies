---
pdd_id: PDD-TECH-RECOMMENDATION-POLICY
title: Technology Recommendation Policy
status: Proposed
authors: ["Jules"]
date: 2025-11-27
scope: Org-wide
---

# Human Manifesto
<<<HUMAN:TECH_RECOMMENDATION_POLICY>>>
Purpose:
Prevent the adoption of vendor-locked frameworks, proprietary protocols, or components that could create a technology monopoly, while ensuring the SDLC-IDE codebase remains interoperable, maintainable, and auditable.

Scope:
Applies to all libraries, services, platforms, and protocols introduced into the SDLC-IDE codebase or infrastructure.

Policy Requirements:
1. Prefer open-source, OSI-approved solutions wherever possible.
2. Select technologies with at least two independent implementations (community + commercial, or equivalent).
3. Favor open standards that are interoperable across vendors.
4. Document any remaining vendor-specific dependencies and provide a clear migration path.

Exceptions:
Temporary use of vendor-specific technologies is allowed only under:
- Regulatory mandates
- Critical time-to-market constraints
All exceptions must be documented with a mitigation plan and reviewed by the architecture team.

Enforcement:
- CI/CD pipelines will automatically flag disallowed dependencies.
- All flagged violations must be resolved before code merge.
- Architecture and SDLC governance teams are responsible for auditing compliance and approving exceptions.
<<<END_HUMAN>>>

# Machine Guardrail
<<<FORMAL:JSON TECH_RECOMMENDATION_POLICY>>>
{
  "policy_id": "TECH_RECOMMENDATION_POLICY",
  "scope": ["libraries", "services", "platforms", "protocols"],
  "requirements": [
    {
      "id": "R1",
      "description": "Only use open-source, OSI-approved solutions",
      "check": "dependency_license in OSI_APPROVED"
    },
    {
      "id": "R2",
      "description": "Technologies must have at least two independent implementations",
      "check": "dependency_implementations_count >= 2"
    },
    {
      "id": "R3",
      "description": "Use open standards interoperable across vendors",
      "check": "protocol_standard in OPEN_STANDARD_LIST"
    },
    {
      "id": "R4",
      "description": "Document vendor-specific dependencies with migration path",
      "check": "if dependency_vendor_specific then documentation_exists == true and migration_path_defined == true"
    }
  ],
  "exceptions": {
    "allowed_for": ["regulatory_mandates", "critical_time_to_market"],
    "require_documentation": true,
    "require_approval": true
  },
  "enforcement": {
    "ci_pipeline": "fail_on_flagged_dependencies",
    "audit_team": "verify_exceptions_and_compliance"
  }
}
<<<END_FORMAL>>>
