package template.authz

import data.core_dag

# Mock data for testing
mock_template_valid := {
    "id": "test/valid:v1",
    "provenance": {"created_by": "github:alice"},
    "bindings": [{"role": "template_author", "principal": "github:alice"}],
    "lifecycle": {
        "transitions": [["draft", "review"]]
    },
    "spec": {"kind": "K8sDeployment"}
}

mock_template_exec := mock_template_valid with spec.exec = "rm -rf /"

mock_template_llm_violation := mock_template_valid with provenance.created_by = "llm"

mock_core_dag_data := {
  "core_dag": {
    "transitions": [
      ["draft","review"],
      ["review","approved"],
      ["approved","active"],
      ["active","decommissioned"]
    ]
  }
}

test_allow_valid_registration {
    # Alice registers her template
    input := {
        "action": "register_template",
        "actor": {"principal_id": "github:alice", "roles": ["template_author"]},
        "template": mock_template_valid
    }
    # Load the necessary core_dag data for the lifecycle check
    result := decision with input as input with data as mock_core_dag_data

    assert result.allow == true
    assert count(result.reasons) == 0
}

test_deny_unbound_actor {
    # Bob tries to register, but isn't bound as template_author
    input := {
        "action": "register_template",
        "actor": {"principal_id": "github:bob", "roles": ["runtime_operator"]},
        "template": mock_template_valid
    }
    result := decision with input as input with data as mock_core_dag_data

    assert result.allow == false
    assert result.reasons[_] == "actor not bound to required role"
}

test_deny_exec_code {
    # Template has a forbidden 'exec' key
    input := {
        "action": "register_template",
        "actor": {"principal_id": "github:alice", "roles": ["template_author"]},
        "template": mock_template_exec
    }
    result := decision with input as input with data as mock_core_dag_data

    assert result.allow == false
    assert result.reasons[_] == "template contains forbidden executable fields"
}

test_deny_llm_violates_policy {
    # LLM-created template tries to define bindings
    input := {
        "action": "register_template",
        "actor": {"principal_id": "github:alice", "roles": ["template_author"]},
        "template": mock_template_llm_violation
    }
    result := decision with input as input with data as mock_core_dag_data

    assert result.allow == false
    assert result.reasons[_] == "LLM authored permission/lifecycle definitions are forbidden"
}

test_deny_invalid_lifecycle {
    # Template defines an invalid transition: approved -> draft
    invalid_lifecycle_template := mock_template_valid with lifecycle.transitions = [["approved", "draft"]]
    input := {
        "action": "register_template",
        "actor": {"principal_id": "github:alice", "roles": ["template_author"]},
        "template": invalid_lifecycle_template
    }
    result := decision with input as input with data as mock_core_dag_data

    assert result.allow == false
    assert result.reasons[_] == "lifecycle transitions not permitted by Core DAG"
}
