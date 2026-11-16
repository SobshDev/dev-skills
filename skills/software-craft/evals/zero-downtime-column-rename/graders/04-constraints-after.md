---
type: llm
focus: trace
weight: 1
---

NOT NULL and UNIQUE constraints on email_address are added only after the backfill, not in the first additive migration.
