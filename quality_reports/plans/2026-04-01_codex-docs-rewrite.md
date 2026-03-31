# Codex-First Documentation Rewrite Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rewrite the public-facing repository and guide documentation so the Clo-Author is presented as a Codex-first plugin workflow with a dedicated Claude migration appendix.

**Architecture:** The docs rewrite is split into three parts: repository overview (`README.md`), guide core pages (quick start, user guide, reference, customization, agents, architecture), and a new migration appendix. Shared language centers on the home-local plugin, project markers, skills, hooks, and worker-critic automation.

**Tech Stack:** Markdown, Quarto `.qmd`, Quarto navbar config, repository docs, Codex plugin terminology

---

### Task 1: Rewrite repository overview and guide landing pages

**Files:**
- Modify: `README.md`
- Modify: `guide/index.qmd`

- [ ] **Step 1: Replace Claude-first quick start with Codex-first setup**
- [ ] **Step 2: Explain the plugin + project split (`~/plugins/clo-author-codex` + repo files)**
- [ ] **Step 3: Keep the 10 workflow families, but describe them as skills and automatic flows**
- [ ] **Step 4: Link readers to the guide and migration appendix**

### Task 2: Rewrite core workflow and reference pages

**Files:**
- Modify: `guide/user-guide.qmd`
- Modify: `guide/reference.qmd`

- [ ] **Step 1: Replace slash-command language with skill-intent language**
- [ ] **Step 2: Describe automatic worker-critic and referee behavior in Codex terms**
- [ ] **Step 3: Update examples to use `AGENTS.md`, `clo-author.toml`, and plugin-aware workflows**
- [ ] **Step 4: Preserve concrete guidance for discovery, strategy, analysis, writing, review, revision, talks, and submission**

### Task 3: Rewrite architecture and customization pages

**Files:**
- Modify: `guide/customization.qmd`
- Modify: `guide/agents.qmd`
- Modify: `guide/architecture.qmd`

- [ ] **Step 1: Replace the old six-layer Claude architecture with the Codex plugin architecture**
- [ ] **Step 2: Reframe agents as prompt roles and workflow roles rather than Claude-only runtime entities**
- [ ] **Step 3: Document hooks, scripts, references, prompts, and template assets**
- [ ] **Step 4: Keep quality gates and worker-critic loop diagrams aligned with the new runtime model**

### Task 4: Add migration appendix and navigation updates

**Files:**
- Create: `guide/migration-from-claude.qmd`
- Modify: `guide/_quarto.yml`

- [ ] **Step 1: Add a migration appendix with old-to-new mapping**
- [ ] **Step 2: Update the Quarto navbar to include the migration appendix**
- [ ] **Step 3: Ensure main docs mention migration only briefly and point to the appendix**

### Task 5: Verify the rewrite

**Files:**
- Verify: `README.md`
- Verify: `guide/*.qmd`

- [ ] **Step 1: Search for stale Claude-first references in the rewritten core docs**
- [ ] **Step 2: Render the Quarto guide if available**
- [ ] **Step 3: Record the verification and remaining follow-ups in a session log**
