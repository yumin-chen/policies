package sdlc.governance.vendor

# Disallow usage of proprietary or vendor‑locked technologies
disallowed_technologies {
    input.tech in {"aws-sdk-go", "azure-sdk-go", "gcp-sdk-go", "proprietary-db-client"}
}

allow {
    not disallowed_technologies
}
