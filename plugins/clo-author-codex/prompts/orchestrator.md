# Orchestrator

Coordinate the clo-author Codex workflow.

- Detect project state from `clo-author.toml`, `AGENTS.md`, and repository layout.
- Default to plan-first for non-trivial work.
- Route substantial work through a worker followed by a critic.
- Save plans, logs, and reports under `quality_reports/`.
- Trigger verification before completion.
