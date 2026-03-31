---
name: discover
description: Run the clo-author Codex discovery workflow for interviews, literature review, data discovery, and idea generation while saving outputs to quality_reports.
---

# Discover

Use this skill for research interviews, literature mapping, data discovery, and early-stage ideation.

For detailed migration-source behavior, read `../../references/legacy-skills/discover.md`.

## Workflow

1. Detect the project with `scripts/detect_project.py`.
2. Read `references/domain-profile.md` before field-specific discovery work.
3. Produce a worker artifact in `quality_reports/`.
4. Run a critic pass by default before treating the artifact as approved.
