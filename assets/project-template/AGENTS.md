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
- Use the plugin adapter notes (`references/codex-adapter.md` in the installed plugin) to translate Claude Code agent dispatch and hook semantics into Codex.
- On first Clo-Author Codex use in this project, ask the user once whether to default allow Codex subagents: "本项目中使用 Clo-Author Codex 时，默认允许使用 Codex subagents；当插件说明要 dispatch agent/critic/referee 时，尽量用 subagent 模拟 Claude Code 的行为。"

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
- `dashboard`
- `freeze`
- `careful`

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
- Claude-compatible current-main runtime assets live under `.claude/` for scaffold fidelity.
- Codex-facing workflow entrypoints are plugin skills; Claude-compatible examples in `CLAUDE.md` remain available for round-trip use in Claude Code.
- Subagent preference starts as ask-on-first-use. Once the user answers, follow that project preference for later Clo-Author Codex workflows unless they change it.
- In Codex, `freeze` and `careful` are soft session guard instructions unless the active plugin runtime confirms `PreToolUse` hook enforcement; in Claude Code they are hard guards via `.claude/hooks/session-guard.py`.
- When in doubt, prefer explicit plans, saved artifacts, and review evidence.
