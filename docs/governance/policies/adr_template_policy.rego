package sdlc.governance.adr_template

import future.keywords.in

deny[msg] {
    some file in input.files
    not valid_frontmatter(file)
    msg := sprintf("Missing required frontmatter fields in %s", [file.path])
}

deny[msg] {
    some file in input.files
    not valid_status(file)
    msg := sprintf("Invalid status in %s", [file.path])
}

deny[msg] {
    some file in input.files
    not valid_body(file)
    msg := sprintf("Missing mandatory sections in body of %s", [file.path])
}

deny[msg] {
    some file in input.files
    not pdd_001_reference(file)
    msg := sprintf("Missing PDD-001 reference in %s (required for Core DAG mutations)", [file.path])
}

valid_frontmatter(file) {
    file.frontmatter.adr_id
    file.frontmatter.title
    file.frontmatter.status
    file.frontmatter.date
    file.frontmatter.authors
    file.frontmatter.scope
    file.frontmatter.repository
    # references is optional in schema but required for logic? User template shows it.
}

valid_status(file) {
    file.frontmatter.status in {"Proposed", "Accepted", "Superseded"}
}

valid_body(file) {
    body := file.body
    contains(body, "## 1. Context")
    contains(body, "## 2. Decision")
    contains(body, "## 3. Compliance")
}

pdd_001_reference(file) {
    contains(file.body, "Core DAG")
    contains(file.frontmatter.references[_], "PDD-001")
} else {
    not contains(file.body, "Core DAG")
}
