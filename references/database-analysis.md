# Database analysis

Support relational databases, document/key-value/wide-column stores, and search engines. Locate schemas/migrations/models, repositories/queries, transaction APIs, and call sites.

Analyze only evidenced properties: schema relationships; indexes and their target query; query shapes; read/write pattern; transaction scope and isolation; pagination strategy; batching; optimistic/pessimistic locks; N+1 risk; partition/shard key; hotspots; and search mappings.

Connect an index to query predicates/order before discussing intent. Never claim improvement without before/after plans, benchmarks, monitoring, or user evidence. Distinguish a plausible risk from a demonstrated defect.
