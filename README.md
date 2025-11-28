# Policy-as-Code Prototype

This repository contains a prototype for a policy-as-code system using Open Policy Agent (OPA). It includes an Express.js API that enforces policies, a set of Rego policies, and a Docker Compose setup for local development and testing.

## Architecture

The system is composed of two main services that run in Docker containers:

1.  **OPA Server (`opa`):** This is the policy engine. It loads all the Rego policies and data from the `/opa/policies` directory. It exposes an HTTP API to evaluate policies.
2.  **Registry API (`registry-api`):** This is an Express.js application that serves as the policy enforcement point. When it receives a request to register a template, it queries the OPA server to determine if the request is allowed.

### Request Flow

1.  A client sends a `POST` request to the `/templates` endpoint of the **Registry API** with a template payload.
2.  The `enforcePolicyMiddleware` in the Express app intercepts the request.
3.  The middleware constructs an `input` object containing the request details (action, actor, template) and sends it to the **OPA Server's** `/v1/data/template/authz/allow` endpoint.
4.  The **OPA Server** evaluates the `allow` rule in the `allow_template_rego.rego` policy against the provided input.
5.  OPA returns a decision (`true` or `false`).
6.  If the decision is `true`, the middleware passes the request to the next handler. If `false`, it returns a `403 Forbidden` error.

## Running the Prototype

To run the prototype locally, you need to have Docker and Docker Compose installed. Then, from the root of the repository, you can start the services using the following command:

```bash
docker-compose -f infrastructure/docker-compose.yml up
```

This will start the OPA server and the Express.js API. The API will be available at `http://localhost:3000`.
