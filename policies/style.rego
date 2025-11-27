package schema.style

# Deny field names in snake_case
deny[msg] {
    some field in object.keys(input.properties)
    contains(field, "_")
    msg := sprintf("Field '%s' is in snake_case. Use camelCase.", [field])
}
