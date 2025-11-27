package template.authz

default allow = false

# By default, deny and provide a reason
reasons[reason] {
    not allow
    reason := "default deny"
}

allow {
    actor_has_required_role
    not template_contains_forbidden_fields
    not llm_authored_forbidden_definitions
    lifecycle_transitions_are_valid
}

# 1) Actor must be bound to a role allowed to perform action.
actor_has_required_role {
  required := required_role_for_action[input.action]
  required != ""
  # Check 1: Role directly assigned to the actor
  required_in_actor_roles(required)
} else {
  required := required_role_for_action[input.action]
  required != ""
  # Check 2: Principal is bound to the role in the template, either directly or via group membership
  required_in_template_bindings(required)
}

# Check if the actor's principal ID is a member of the required group/principal
principal_is_member_of(principal_id, required_principal) {
    principal_id == required_principal
}
principal_is_member_of(principal_id, required_principal) {
    # Check if required_principal is a group (e.g., 'team:...') and the actor is a member
    data.identity.groups[required_principal][_] == principal_id
}

# The actor must have the required role directly in their claims
required_in_actor_roles(required) {
  some i
  input.actor.roles[i] == required
}

# The required role must be assigned to the actor (or their team) in the template's bindings
required_in_template_bindings(required) {
  some j
  binding := input.template.bindings[j]
  binding.role == required
  principal_is_member_of(input.actor.principal_id, binding.principal)
}

# Define the roles required for actions
required_role_for_action := {
    "register_template": "template_author"
}

# 2) Template must not contain forbidden fields
template_contains_forbidden_fields {
    input.template.spec.exec
}

reasons[reason] {
    template_contains_forbidden_fields
    reason := "template contains forbidden executable fields"
}

# 3) LLM-authored templates cannot define bindings or lifecycle
llm_authored_forbidden_definitions {
    input.template.provenance.created_by == "llm"
    count(input.template.bindings) > 0
}

llm_authored_forbidden_definitions {
    input.template.provenance.created_by == "llm"
    count(input.template.lifecycle.transitions) > 0
}

reasons[reason] {
    llm_authored_forbidden_definitions
    reason := "LLM authored permission/lifecycle definitions are forbidden"
}

# 4) Lifecycle transitions must be permitted by the Core DAG
lifecycle_transitions_are_valid {
    every transition in input.template.lifecycle.transitions {
        some i
        data.core_dag.transitions[i] == transition
    }
}

reasons[reason] {
    not lifecycle_transitions_are_valid
    reason := "lifecycle transitions not permitted by Core DAG"
}

reasons[reason] {
    not actor_has_required_role
    reason := "actor not bound to required role"
}
