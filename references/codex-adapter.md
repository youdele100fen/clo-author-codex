# Codex Adapter Notes

This plugin keeps the current upstream clo-author main skills, agents, rules, references, and scaffold assets intact, then adds a thin Codex adapter around them. Treat the upstream `.claude/` runtime as the source of workflow truth and this file as the execution map for Codex.

## Surface Mapping

| Claude Code surface | Codex surface | Adapter behavior |
| --- | --- | --- |
| `.claude/skills/*/SKILL.md` | `skills/*/SKILL.md` | Preserved verbatim so slash-command behavior and quality gates match upstream. |
| `.claude/agents/*.md` | `prompts/legacy-agents/*.md` and scaffold `.claude/agents/*.md` | Preserved verbatim for worker, critic, referee, verifier, and orchestrator roles. |
| `.claude/rules/*.md` | `references/legacy-rules/*.md` and scaffold `.claude/rules/*.md` | Preserved verbatim for content invariants, quality gates, revision protocol, and logging. |
| `.claude/references/*.md` | `references/*.md` and scaffold `.claude/references/*.md` | Preserved verbatim for domain profile, journal profiles, style guide, and coding standards. |
| Claude `Task` agent dispatch | Codex subagent-style dispatch | Use Codex delegation when available; otherwise run the named legacy-agent prompt in-process and record the role in the output. Preserve worker-critic separation. |
| Claude `WebSearch` / `WebFetch` | Codex web browsing | Use web search/fetch only for tasks that need current literature, data, journal, or novelty checks. Cite sources in the final artifact. |
| Claude `EnterPlanMode` | Codex planning discipline | In Codex, produce an explicit plan artifact under `quality_reports/plans/` and wait for user approval when the upstream skill requires plan mode. |
| Claude hooks in scaffold `.claude/settings.json` | Codex plugin `hooks.json` plus scaffold hooks | Plugin hooks perform lightweight detection/review hints; scaffold hooks preserve upstream Claude Code behavior for projects also opened in Claude Code. |
| Claude `/freeze` and `/careful` hard guards | Codex `freeze` and `careful` skills | Write the same `.claude/state/session-guards.json` state and honor it as a session instruction. Hard blocking depends on whether the active Codex plugin runtime exposes a compatible `PreToolUse` hook. |
| Claude dashboard/report scripts | Codex project scripts | Generated projects include `scripts/generate_dashboard.py`, `scripts/generate_html_report.py`, and the shared HTML templates; run them from the project root. |

## Execution Rules

- Keep upstream text stable unless upstream changes; put Codex-specific clarifications in adapter files, helper scripts, or project `AGENTS.md`.
- On first Clo-Author Codex use in a generated project, ask the user once whether to default allow Codex subagents: "本项目中使用 Clo-Author Codex 时，默认允许使用 Codex subagents；当插件说明要 dispatch agent/critic/referee 时，尽量用 subagent 模拟 Claude Code 的行为。" Record and follow the answer as the project preference.
- This preference applies to clo-author legacy agents such as Coder, Writer, Strategist, critics, referees, and Verifier when the skill requests agent dispatch.
- When a skill says to dispatch an agent, load the corresponding prompt from `prompts/legacy-agents/<agent>.md` or the scaffold `.claude/agents/<agent>.md`.
- When a skill pairs a creator with a critic, run the creator first, then the critic, and save both artifacts or summaries under `quality_reports/`.
- When multiple upstream agents are independent, parallelize only when Codex has an explicit delegation mechanism available. If not, run them sequentially and state that the role separation is preserved.
- Critics must not edit source artifacts. If fixes are needed, route back to the paired creator or ask the user for approval when the upstream protocol requires it.
- Preserve the original `.claude/` scaffold in generated projects for round-trip compatibility with Claude Code.

## Known Non-Identical Semantics

- Codex plugin hooks do not expose every Claude Code hook event. The generated project still includes upstream `.claude/settings.json` and hook scripts for Claude Code parity.
- In this Codex runtime, `/freeze` and `/careful` should be treated as soft session guard instructions unless `PreToolUse` hooks are confirmed active. They preserve upstream state files for round-trip use in Claude Code, but they must not be described as guaranteed hard blockers in Codex.
- Codex does not use Claude Code auto-memory paths. The checkpoint workflow should always write `SESSION_REPORT.md` and `quality_reports/research_journal.md`; Codex-specific durable memory can be captured in `MEMORY.md`.
- The upstream skills use slash-command examples such as `/review --peer`. In Codex, invoke the matching skill name, for example `$review`, or ask the plugin by its display name.
