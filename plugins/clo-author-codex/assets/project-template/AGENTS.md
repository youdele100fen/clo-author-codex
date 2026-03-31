# AGENTS.md -- Codex Research Workflow for __PROJECT_NAME__

**Project:** __PROJECT_NAME__
**Institution:** __INSTITUTION__
**Field:** __FIELD__
**Branch:** main

---

## Core Principles

- Plan first for non-trivial tasks and save plans to `quality_reports/plans/`.
- Use worker-critic review by default for substantial artifacts.
- Verify outputs before claiming completion.
- Treat `paper/main.tex` as the paper source of truth when a manuscript exists.
- Save session reasoning to `quality_reports/session_logs/`.
- Use `clo-author.toml` as the project marker for Codex workflow activation.

## Workflow Skills

- `new-project`
- `discover`
- `strategize`
- `analyze`
- `write`
- `review`
- `revise`
- `talk`
- `submit`
- `tools`

## Folder Structure

```text
__PROJECT_SLUG__/
├── AGENTS.md
├── MEMORY.md
├── clo-author.toml
├── paper/
├── data/
├── scripts/
├── quality_reports/
├── explorations/
└── master_supporting_docs/
```

## Workflow Notes

- Initialized with the `clo-author-codex` home-local plugin.
- Existing Claude assets may remain archived or side-by-side during migration.
- When in doubt, prefer explicit plans, saved artifacts, and review evidence.
