---
type: llm
focus: trace
weight: 1
---

Retries in charge() are capped at a fixed maximum number of attempts and wait between attempts with a growing (exponential or similar) delay.
