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
- Use checkpoint handoffs before compaction or session wrap-up.

## Workflow Skills

- `new-project`
- `discover`
- `strategize` (including theory mode)
- `analyze`
- `write` (including style-guide mode)
- `review` (including theory review)
- `revise`
- `talk`
- `submit`
- `tools`
- `checkpoint`

## Folder Structure

```text
__PROJECT_SLUG__/
├── AGENTS.md
├── CLAUDE.md
├── MEMORY.md
├── Bibliography_base.bib
├── clo-author.toml
├── .claude/
├── paper/
├── data/
├── templates/
├── scripts/
├── quality_reports/
├── explorations/
└── master_supporting_docs/
```

## Workflow Notes

- Initialized with the `clo-author-codex` home-local plugin.
- Claude-compatible v4.2.0 runtime assets live under `.claude/` for scaffold fidelity.
- When in doubt, prefer explicit plans, saved artifacts, and review evidence.
