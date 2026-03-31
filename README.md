# The Clo-Author: Codex Research Workflow for Empirical Social Science

[![Version](https://img.shields.io/github/v/release/hugosantanna/clo-author?style=flat-square&color=b44dff&label=version)](CHANGELOG.md)

> **Work in progress.** The workflow is evolving as the Codex migration matures. Expect a few rough edges while the plugin and docs settle.

The Clo-Author is a Codex-first research workflow for empirical social science: economics, finance, marketing, management, accounting, and public policy. It keeps the original clo-author ideas — plan-first execution, worker-critic review, journal-aware peer review, and quality gates — but now runs through a home-local Codex plugin plus lightweight project files such as `AGENTS.md` and `clo-author.toml`.

**Live guide:** [hugosantanna.github.io/clo-author](https://hugosantanna.github.io/clo-author/)
<br>**Historical origin:** [Pedro Sant'Anna's claude-code-my-workflow](https://github.com/pedrohcgs/claude-code-my-workflow)

---

## Quick Start

### 1. Prepare Codex and the plugin

The current recommended setup is:

- Codex with local plugin support
- A home-local plugin installed at `~/plugins/clo-author-codex`
- A marketplace entry at `~/.agents/plugins/marketplace.json`

If you are migrating an existing local clo-author installation, keep the legacy `.claude/` assets in place during the first pass and let the Codex workflow sit beside them.

### 2. Clone the repository

```bash
gh repo fork hugosantanna/clo-author --clone
cd clo-author
```

### 3. Open the repo in Codex

Once the plugin is installed, Codex should detect the project through:

- `AGENTS.md`
- `clo-author.toml`
- the research folder layout

### 4. Start with a skill or a plain-language request

You can work in either of these styles:

- Plain language: "Set up a literature review workflow for the effect of minimum wage on employment."
- Explicit skill naming: "Use `$discover` to build a literature map for minimum wage and employment."

For a fresh repository, start with `$new-project`. For an existing repository, the plugin should detect the project automatically and route you into the right workflow.

---

## What It Does

### Codex-First Workflow

The Codex version keeps the same research pipeline as the Claude version, but changes the runtime model:

- The home-local plugin carries skills, hooks, prompts, scripts, references, and template assets.
- The repository carries project-specific files like `AGENTS.md`, `clo-author.toml`, `MEMORY.md`, and `quality_reports/`.
- Codex defaults to plan-first execution for non-trivial work.
- Substantial work routes through a worker step and then a critic step by default.
- Verification evidence is expected before anything is treated as complete.

### Worker-Critic Roles

Every creator has a paired reviewer. Critics do not edit the artifact they inspect; workers do not self-approve. The role families remain:

| Phase | Worker | Critic / Reviewer |
|-------|--------|-------------------|
| Discovery | Librarian, Explorer | librarian-critic, explorer-critic |
| Strategy | Strategist | strategist-critic |
| Execution | Data-engineer, Coder, Writer | coder-critic, writer-critic |
| Peer Review | Editor-driven review flow | domain-referee, methods-referee |
| Presentation | Storyteller | storyteller-critic |
| Infrastructure | Orchestrator, Verifier | quality gates and verification |

### Journal-Aware Review

The `review` workflow still supports desk-style review, calibrated referee behavior, and staged revision logic. Journal profiles and domain profiles remain central. What changed is the invocation style: Codex uses skills and prompt-driven automation.

### 10 Workflow Families

The core workflows are unchanged in spirit:

| Category | Skills |
|----------|--------|
| Research | `new-project`, `discover`, `strategize`, `analyze`, `write` |
| Review | `review`, `revise` |
| Output | `talk`, `submit` |
| Utilities | `tools` |

### Quality Gates

Weighted quality gates remain the same:

| Score | Gate | Applies To |
|-------|------|------------|
| 80 | Commit | Weighted aggregate |
| 90 | PR | Weighted aggregate |
| 95 | Submission | Aggregate plus component minimums |
| -- | Advisory | Talks |

---

## Project Layout

The Codex version uses a split architecture: reusable plugin at home, project-specific files in the repo.

```text
your-project/
├── AGENTS.md                   # Codex-facing project constitution
├── clo-author.toml             # Project marker and workflow metadata
├── MEMORY.md                   # Durable project learnings
├── Bibliography_base.bib       # Centralized bibliography
├── paper/                      # Manuscript, tables, figures, talks, appendix
├── data/                       # Raw and cleaned datasets
├── scripts/                    # Analysis code
├── quality_reports/            # Specs, plans, logs, reviews, scores
├── explorations/               # Structured sandbox
└── master_supporting_docs/     # Reference papers and supporting materials
```

The plugin contributes:

- `skills/`
- `prompts/`
- `references/`
- `hooks.json` and hook scripts
- helper scripts for initialization, migration, logging, and review triggers
- project template assets

---

## Prerequisites

| Tool | Required For | Install |
|------|-------------|---------|
| Codex with local plugin support | Primary workflow runtime | your local Codex install |
| Python 3 | Plugin helper scripts | [python.org](https://www.python.org/) or system Python |
| XeLaTeX | Paper compilation | [TeX Live](https://tug.org/texlive/) or [MacTeX](https://tug.org/mactex/) |
| R | Analysis and figures | [r-project.org](https://www.r-project.org/) |
| `gh` CLI | GitHub integration | [cli.github.com](https://cli.github.com/) |

Optional: Stata, Python, Julia, Quarto.

---

## Adapting for Your Field

1. Fill in `AGENTS.md` and `clo-author.toml`.
2. Fill in the domain profile used by the plugin references.
3. Extend journal profiles for your field.
4. Set project conventions for language, output organization, and replication expectations.

The current repository includes both Codex-facing project files and the legacy `.claude/` assets for migration traceability.

---

## Migration from Claude

The Codex version is intentionally **Codex-first**, but it includes a migration path from the Claude-based workflow:

- `CLAUDE.md` becomes `AGENTS.md`
- `.claude/skills/` becomes plugin `skills/`
- `.claude/agents/` becomes plugin prompt roles
- `.claude/settings.json` hooks become plugin `hooks.json` plus helper scripts
- slash commands become skills or natural-language workflow requests

See the guide appendix for the full migration map.

---

## Origin

This project still traces back to [claude-code-my-workflow](https://github.com/pedrohcgs/claude-code-my-workflow), but the runtime story is now different. The current emphasis is a Codex-native plugin architecture that keeps the original research rigor while making the workflow portable across Codex-managed repositories.

Maintained by [Hugo Sant'Anna](https://hsantanna.org). MIT License.
