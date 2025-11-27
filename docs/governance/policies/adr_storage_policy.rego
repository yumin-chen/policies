package sdlc.governance.adr_storage

import future.keywords.in

deny[msg] {
    some file in input.files
    not valid_suffix(file.path)
    msg := sprintf("Invalid file suffix for ADR: %s. Must be -full.md or -comp.md", [file.path])
}

valid_suffix(path) {
    endswith(path, "-full.md")
}
valid_suffix(path) {
    endswith(path, "-comp.md")
}
