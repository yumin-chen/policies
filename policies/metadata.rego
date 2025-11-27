package schema.metadata

# Enforce the presence of a 'metadata' field
deny[msg] {
    not input.properties.metadata
    msg := "Schema is missing required 'metadata' field"
}

# Enforce 'metadata' has 'version' and 'owner'
deny[msg] {
    not input.properties.metadata.properties.version
    msg := "Schema metadata is missing 'version'"
}
deny[msg] {
    not input.properties.metadata.properties.owner
    msg := "Schema metadata is missing 'owner'"
}
