---
name: new-project
description: Initialize a new clo-author Codex project with AGENTS.md, clo-author.toml, research folders, quality report directories, and automatic worker-critic defaults.
---

# New Project

Use this skill when the user wants to start a fresh empirical research repository in the clo-author Codex format.

For detailed migration-source behavior, read `../../references/legacy-skills/new-project.md`.

## Workflow

1. Collect the target path, project name, field, and institution if they are missing.
2. Run `scripts/init_project.py`.
3. Confirm that `AGENTS.md`, `clo-author.toml`, and `quality_reports/` were created.
4. Suggest the next workflow stage: `discover` or `strategize`.
