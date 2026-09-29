# Backend architecture mapping

Start from executable entrypoints and deployment units, then map module imports and runtime edges. Distinguish source folders from independently deployable services.

For each representative business flow capture: trigger, route/event/job, handler, application/domain service, repository/client, state read/write, response/event, error path, and evidence. Note sync versus async edges and transaction boundaries.

Architecture labels require evidence:

- **Monolith:** one deployment/runtime boundary; folders alone do not imply services.
- **Modular monolith:** one deployment with intentional internal module boundaries.
- **Microservices:** multiple independently deployable services with network contracts.
- **Event-driven:** events materially drive state or processing, not merely incidental notifications.
- **Serverless:** functions/jobs form deployed execution units.

Describe uncertainty and avoid diagram edges not found in code/configuration.
