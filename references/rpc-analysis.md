# RPC and downstream calls

Detect REST/HTTP clients, gRPC, Dubbo, Feign, Thrift, GraphQL, and other generated or hand-written clients. Map caller → client method → contract → downstream boundary → response/error handling.

Inspect timeout, retry eligibility and budget, circuit breaker, load balancing/discovery, authentication, fallback, and failure propagation. Beware multiplicative retries and non-idempotent operations. A normal HTTP call is a service dependency, not proof of a complex distributed architecture.
