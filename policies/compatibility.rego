package schema.compatibility

# Deny backward-incompatible changes: removing a required field
deny[msg] {
    # This is a placeholder. A real implementation would involve
    # comparing against the previous version of the schema.
    # For this example, we'll keep it simple.
    msg := "Backward-incompatible change detected (placeholder)"
    1 == 2 # Fails intentionally to show where logic would go
}
