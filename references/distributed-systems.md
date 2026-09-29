# Distributed-system reasoning

Apply only to flows that cross process or persistence boundaries. Locate the consistency invariant first, then evaluate transaction boundaries, eventual consistency, outbox/saga/compensation, idempotency key and storage, retry/backoff, concurrency control, leader/lock lease, deduplication, and partial failures.

Separate implementation from intention. Comments and configuration indicate intent; executable paths and tests strengthen evidence. Never claim high availability, exactly-once processing, or distributed transactions merely because middleware is present.
