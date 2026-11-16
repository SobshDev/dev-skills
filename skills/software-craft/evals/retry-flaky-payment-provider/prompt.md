---
tags: [skill-creator]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

our payment provider has been flaky this week (random 502s and some requests that just hang forever). can you add retries to PaymentClient.charge in payments/client.py? keep it simple pls, checkout is waiting on this

Input files: payments/client.py, payments/__init__.py, tests/test_client.py, README.md
