---
type: llm
focus: trace
weight: 1
---

During the rollout, the updated app/users.py writes both columns (or a trigger keeps them in sync), so instances running old and new code both see correct data.
