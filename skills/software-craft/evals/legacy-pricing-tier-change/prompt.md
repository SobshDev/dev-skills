---
tags: [skill-creator]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

in shop/pricing.py gold customers should now get 15% off orders over 100 (it's 10% today), and we're adding a platinum tier with 20% off over 100. there are no tests for this file at all. calc() is used by checkout and invoices so please don't break anything else

Input files: shop/pricing.py, shop/checkout.py, shop/invoices.py, shop/__init__.py
