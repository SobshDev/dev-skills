---
type: llm
focus: trace
weight: 1
---

The change prevents retries from charging the customer twice, by sending the same idempotency key or request id on every attempt of one charge, or by explicitly not retrying when the outcome is unknown and explaining why.
