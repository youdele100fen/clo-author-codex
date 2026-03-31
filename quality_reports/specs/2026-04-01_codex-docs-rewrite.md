# Requirements Specification: Codex-First Documentation Rewrite

**Date:** 2026-04-01
**Status:** APPROVED

---

## Objective

Rewrite `README.md` and the guide site so the Clo-Author is documented as a Codex-first, plugin-driven workflow while preserving a dedicated migration appendix for users coming from the Claude-based version.

---

## Requirements

### MUST Have (Non-Negotiable)

- [x] Rewrite `README.md` to describe the Codex-first plugin architecture rather than the Claude workflow.
- [x] Rewrite the core guide pages: `index.qmd`, `user-guide.qmd`, `reference.qmd`, `customization.qmd`, `agents.qmd`, and `architecture.qmd`.
- [x] Explain the new project entry points: `AGENTS.md`, `clo-author.toml`, home-local plugin, skills, prompts, references, hooks, and scripts.
- [x] Replace slash-command framing with Codex skill framing while preserving the same 10 workflow families.
- [x] Preserve worker-critic, referee, and quality-gate concepts in the new documentation.
- [x] Add a migration appendix specifically for Claude-to-Codex users.

### SHOULD Have (Preferred)

- [x] Keep the new documentation shorter and cleaner than the original where possible.
- [x] Keep repository and guide terminology aligned.
- [x] Update the Quarto navbar so the migration appendix appears in the site navigation.

### MAY Have (Optional, If Time)

- [ ] Add screenshots or plugin-install visuals later.
- [ ] Add a more polished plugin packaging story once the plugin is distributed from versioned source.

---

## Clarity Status

| Aspect | Status | Notes |
|--------|--------|-------|
| Main documentation stance | CLEAR | User chose Codex-first. |
| Migration handling | CLEAR | User chose to retain a dedicated migration appendix for Claude users. |
| Scope of rewrite | CLEAR | `README.md` plus `guide/*.qmd` are in scope. |
| Runtime distribution story | ASSUMED | Document the current home-local plugin model directly, even though packaging may evolve later. |

---

## Success Criteria

- `README.md` reads as a Codex-first project overview.
- The guide pages consistently describe the Codex plugin, `AGENTS.md`, `clo-author.toml`, skills, prompts, references, hooks, and scripts.
- A dedicated migration appendix exists and is linked in the Quarto navbar.
- The main guide pages no longer depend on Claude-only concepts such as `CLAUDE.md`, slash commands, `.claude/settings.json`, or Claude panel instructions, except inside migration-specific sections.

---

## Approval

[x] User approved: 2026-04-01
