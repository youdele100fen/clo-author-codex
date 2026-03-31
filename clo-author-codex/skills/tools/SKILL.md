---
name: tools
description: Run clo-author Codex utility workflows for compilation, validation, context inspection, and housekeeping.
---

# Tools

Use this skill for compile, validate, workflow-state inspection, and related utility tasks.

For detailed migration-source behavior, read `../../references/legacy-skills/tools.md`.

## Workflow

1. Detect the project and relevant file targets.
2. Run the smallest correct verification or utility command.
3. Save outputs or reports when the command affects workflow state.
4. Prefer evidence-producing commands over verbal assurances.
