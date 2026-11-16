---
type: llm
focus: trace
weight: 1
---

charge() retries only transient failures (such as 5xx responses, connection errors or timeouts) and does not retry client errors such as 400, 401 or 402.
