# Cache analysis

Identify cache provider, key construction, value ownership, read/write path, TTL, invalidation, serialization, and fallback behavior. Classify cache-aside or write-through only when the sequence proves it.

Look for explicit defenses against penetration, breakdown, avalanche, stale writes, and stampedes, plus local/distributed locking. Do not infer these defenses from Redis or a cache annotation alone. Explain consistency trade-offs and failure behavior from actual code.
