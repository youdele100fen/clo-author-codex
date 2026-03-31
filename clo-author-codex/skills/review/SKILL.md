---
name: review
description: Run the clo-author Codex review workflow, including default worker-critic review, referee-style review, and quality-gate reporting.
---

# Review

Use this skill when the user wants code review, manuscript review, peer-style review, or a quality-gate decision.

For detailed migration-source behavior, read `../../references/legacy-skills/review.md`.

## Workflow

1. Identify the artifact type and relevant critic or referee prompt.
2. Load `references/quality.md` and any applicable domain or journal references.
3. Produce a scored report under `quality_reports/`.
4. Treat review evidence as the gate for completion claims.
