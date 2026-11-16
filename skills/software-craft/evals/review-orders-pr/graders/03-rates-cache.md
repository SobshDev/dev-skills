---
type: llm
focus: trace
weight: 1
---

The review flags the module-level _rates_cache as a problem, because it never expires or is unbounded or caches a rate forever.
