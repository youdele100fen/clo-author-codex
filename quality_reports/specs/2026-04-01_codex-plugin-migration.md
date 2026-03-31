# Requirements Specification: Codex Plugin Migration for Clo-Author

**Date:** 2026-04-01
**Status:** APPROVED

---

## Objective

Replace the Claude-specific workflow infrastructure with a home-local Codex plugin that can both initialize new clo-author-style research projects and automatically support existing research repositories with Codex-native skills, hooks, scripts, prompts, and review loops.

---

## Requirements

### MUST Have (Non-Negotiable)

- [x] Create a home-local plugin at `~/plugins/clo-author-codex` with a valid `.codex-plugin/plugin.json`.
- [x] Register the plugin in `~/.agents/plugins/marketplace.json`.
- [x] Support initialization of brand-new research projects using a clo-author-style project template.
- [x] Support existing repositories by detecting a clo-author-compatible project layout and activating the workflow automatically.
- [x] Expose Codex-native skill entry points that map to the 10 existing workflow families: new project, discover, strategize, analyze, write, review, revise, talk, submit, and tools.
- [x] Preserve the worker-critic operating model as a default behavior for substantial artifact creation and review.
- [x] Preserve plan logging, session logging, quality thresholds, and verification expectations.
- [x] Migrate Claude-only prompt assets into Codex-usable prompts, references, and scripts without requiring `.claude/settings.json`.
- [x] Provide a project-level `AGENTS.md` template so initialized repositories load the Codex workflow consistently.

### SHOULD Have (Preferred)

- [x] Archive or retain the original `.claude/` material in a non-default reference location for migration traceability.
- [x] Provide migration helpers for converting an existing clo-author repository into the Codex-driven structure.
- [x] Provide reusable prompt templates for orchestrator, workers, critics, and referees.
- [x] Include script-level tests for plugin bootstrap, project detection, and project initialization behavior.
- [x] Keep the initialized project structure compatible with the current clo-author research folders and quality report conventions.

### MAY Have (Optional, If Time)

- [ ] Provide plugin branding assets and polished marketplace metadata.
- [ ] Add optional documentation-site regeneration support for the Codex version.
- [ ] Add optional MCP or richer desktop integrations in a follow-up phase.

---

## Clarity Status

| Aspect | Status | Notes |
|--------|--------|-------|
| Plugin install scope | CLEAR | User chose `home-local plugin`. |
| Project creation support | CLEAR | User wants the plugin to initialize new clo-author-style projects. |
| Workflow entry style | CLEAR | User chose Codex-native skill entry points rather than slash-command emulation. |
| Review model | CLEAR | User wants worker-critic review to trigger by default. |
| Automation posture | CLEAR | User wants the plugin to take over as much of the workflow as practical. |
| Source of truth for template content | ASSUMED | The current `clo-author` repository becomes the migration source for prompts, references, folder layout, and quality conventions. |
| Existing repository migration behavior | ASSUMED | Existing repos will be adapted by adding Codex-facing files and helpers without deleting legacy `.claude/` assets during the first implementation pass. |
| Hook scope | ASSUMED | Hooks will focus on detection, planning nudges, protection, session-state capture, and post-action review triggers rather than trying to reproduce every Claude event exactly. |

**Status Definitions:**
- **CLEAR:** Fully specified, no ambiguity
- **ASSUMED:** Reasonable assumption made in absence of clarity; user can override
- **BLOCKED:** Cannot proceed until this is answered

---

## Success Criteria

- A valid plugin exists at `~/plugins/clo-author-codex` and is registered in the local Codex marketplace.
- The plugin contains Codex skills, hooks, scripts, prompt templates, references, and template assets for clo-author workflows.
- Running the project initializer creates a new repository skeleton with `AGENTS.md`, research folders, quality report directories, and workflow support files.
- Existing clo-author repositories can be recognized and given Codex-facing workflow support without depending on Claude-only settings.
- The plugin includes tests or verification scripts for the bootstrap and initialization flows.

---

## Approval

[x] User approved: 2026-04-01
