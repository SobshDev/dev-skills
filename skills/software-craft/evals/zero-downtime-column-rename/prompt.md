---
tags: [skill-creator]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

we need to rename users.email to users.email_address (postgres). we deploy with rolling updates across 3 app instances and can't have downtime. write the migration(s) and update app/users.py

Input files: migrations/0001_create_users.sql, app/users.py, app/__init__.py, README.md
