# Policy-as-Code Prototype

This repository contains a prototype for a policy-as-code system using Open Policy Agent (OPA). It includes an Express.js API that enforces policies, a set of Rego policies, and a Docker Compose setup for local development and testing.

## Running the Prototype

To run the prototype locally, you need to have Docker and Docker Compose installed. Then, you can start the services using the following command:

```bash
docker-compose up
```

This will start the OPA server and the Express.js API. The API will be available at `http://localhost:3000`.
