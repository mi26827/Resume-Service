# Messaging analysis

Trace producer → topic/queue/stream → consumer/group → business logic and state changes across Kafka, RabbitMQ, RocketMQ, Pulsar, NATS, SQS/SNS, Redis Streams, or other brokers.

Record destination, payload contract, partition/shard key, ordering scope, ACK/offset semantics, retry, dead-letter handling, duplicate-delivery protection, idempotency, transaction/outbox relationship, back pressure, and accumulation controls when evidenced.

Determine the actual purpose: async processing, decoupling, traffic shaping, events, notifications, synchronization, or eventual consistency. Apply broker-specific terminology only after detecting that broker.
