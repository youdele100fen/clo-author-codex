---
name: analyze
description: Run the clo-author Codex analysis workflow for data cleaning, estimation, robustness checks, and production of publication-ready outputs.
---

# Analyze

Use this skill when implementing or reviewing analysis scripts, figures, tables, or cleaned data outputs.

For detailed migration-source behavior, read `../../references/legacy-skills/analyze.md`.

## Workflow

1. Default to plan-first for non-trivial analysis changes.
2. Produce scripts and outputs in `scripts/`, `paper/tables/`, and `paper/figures/`.
3. Trigger worker-critic review by default for substantial code or output changes.
4. Save verification evidence before completion.
