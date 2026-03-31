# Codex Plugin Migration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a home-local Codex plugin that ports the clo-author workflow into Codex-native skills, hooks, prompts, scripts, and project templates.

**Architecture:** The implementation is split between a reusable home-local plugin in `~/plugins/clo-author-codex` and the current `clo-author` repository as the migration source. The plugin owns runtime behavior, project initialization, prompt assets, and hooks. The repository contributes template content, migration notes, and verification fixtures.

**Tech Stack:** Codex plugin manifest JSON, Markdown skills/prompts/references, Python helper scripts, shell verification commands, existing clo-author repo assets

---

### Task 1: Scaffold the home-local plugin shell

**Files:**
- Create: `~/plugins/clo-author-codex/.codex-plugin/plugin.json`
- Create: `~/plugins/clo-author-codex/skills/`
- Create: `~/plugins/clo-author-codex/hooks/`
- Create: `~/plugins/clo-author-codex/scripts/`
- Create: `~/plugins/clo-author-codex/references/`
- Create: `~/plugins/clo-author-codex/prompts/`
- Create: `~/plugins/clo-author-codex/assets/`
- Modify: `~/.agents/plugins/marketplace.json`

- [ ] **Step 1: Generate the failing bootstrap expectation**

Create a verification command expectation that should fail before the plugin exists:

```bash
test -f ~/plugins/clo-author-codex/.codex-plugin/plugin.json
```

Expected: exit status `1`

- [ ] **Step 2: Run the bootstrap expectation and verify it fails**

Run:

```bash
test -f ~/plugins/clo-author-codex/.codex-plugin/plugin.json
```

Expected: non-zero exit because the plugin has not been scaffolded yet

- [ ] **Step 3: Scaffold the plugin with the Codex plugin creator**

Run:

```bash
python3 /Users/youdele100fen/.codex/skills/.system/plugin-creator/scripts/create_basic_plugin.py clo-author-codex \
  --path ~/plugins \
  --marketplace-path ~/.agents/plugins/marketplace.json \
  --with-marketplace \
  --with-skills \
  --with-hooks \
  --with-scripts \
  --with-assets
```

- [ ] **Step 4: Verify the scaffold now exists**

Run:

```bash
test -f ~/plugins/clo-author-codex/.codex-plugin/plugin.json
```

Expected: exit status `0`

### Task 2: Define the plugin manifest and Codex-facing layout

**Files:**
- Modify: `~/plugins/clo-author-codex/.codex-plugin/plugin.json`
- Create: `~/plugins/clo-author-codex/README_INTERNAL.md` (temporary notes are not needed; skip this)
- Create: `~/plugins/clo-author-codex/prompts/orchestrator.md`
- Create: `~/plugins/clo-author-codex/prompts/worker-critic-contract.md`
- Create: `~/plugins/clo-author-codex/references/workflow-map.md`

- [ ] **Step 1: Write the failing manifest validation test**

Create a Python test file that asserts the manifest includes the intended plugin name and interface metadata:

```python
import json
from pathlib import Path


def test_plugin_manifest_has_expected_name():
    manifest = json.loads(Path.home().joinpath("plugins/clo-author-codex/.codex-plugin/plugin.json").read_text())
    assert manifest["name"] == "clo-author-codex"
```

- [ ] **Step 2: Run the test and verify it fails for the uncustomized scaffold**

Run:

```bash
python3 -m unittest discover -s clo-author/tests
```

Expected: failure until the test file and manifest customization land

- [ ] **Step 3: Customize the manifest and add the shared prompt/reference skeleton**

Edit the manifest so it has a concrete description, interface metadata, and a stable local plugin identity. Create prompt and reference files that define:

```md
# Orchestrator

Coordinate the clo-author workflow in Codex.
- Detect project state
- Default to plan-first for non-trivial work
- Trigger worker-critic review for substantial artifacts
- Route to review, submit, or revision flows when quality gates require it
```

- [ ] **Step 4: Re-run the manifest validation**

Run:

```bash
python3 -m unittest discover -s clo-author/tests
```

Expected: manifest test passes

### Task 3: Build the project template and initializer

**Files:**
- Create: `~/plugins/clo-author-codex/assets/project-template/AGENTS.md`
- Create: `~/plugins/clo-author-codex/assets/project-template/MEMORY.md`
- Create: `~/plugins/clo-author-codex/assets/project-template/clo-author.toml`
- Create: `~/plugins/clo-author-codex/assets/project-template/paper/.gitkeep`
- Create: `~/plugins/clo-author-codex/assets/project-template/quality_reports/plans/.gitkeep`
- Create: `~/plugins/clo-author-codex/assets/project-template/quality_reports/session_logs/.gitkeep`
- Create: `~/plugins/clo-author-codex/scripts/init_project.py`

- [ ] **Step 1: Write the failing initializer test**

Create a test that initializes a project into a temporary directory and checks for the required files:

```python
import subprocess
import tempfile
from pathlib import Path


def test_init_project_creates_codex_research_layout():
    with tempfile.TemporaryDirectory() as tmpdir:
        target = Path(tmpdir) / "demo-project"
        subprocess.run(
            [
                "python3",
                str(Path.home() / "plugins/clo-author-codex/scripts/init_project.py"),
                "--target",
                str(target),
                "--project-name",
                "Demo Project",
            ],
            check=True,
        )
        assert target.joinpath("AGENTS.md").exists()
        assert target.joinpath("clo-author.toml").exists()
        assert target.joinpath("quality_reports/plans").exists()
```

- [ ] **Step 2: Run the test and verify it fails before the initializer exists**

Run:

```bash
python3 -m unittest discover -s clo-author/tests
```

Expected: failure because `init_project.py` and the template files do not exist yet

- [ ] **Step 3: Implement the template and initializer minimally**

Create an initializer that:

```python
from pathlib import Path
import argparse
import shutil


def copy_template(template_root: Path, target_root: Path) -> None:
    shutil.copytree(template_root, target_root)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", required=True)
    parser.add_argument("--project-name", required=True)
    args = parser.parse_args()
```

and then copies the template, writes project metadata into `AGENTS.md` and `clo-author.toml`, and creates the research directory skeleton.

- [ ] **Step 4: Re-run the initializer test**

Run:

```bash
python3 -m unittest discover -s clo-author/tests
```

Expected: initializer test passes

### Task 4: Port workflow assets into Codex skills, prompts, and references

**Files:**
- Create: `~/plugins/clo-author-codex/skills/new-project/SKILL.md`
- Create: `~/plugins/clo-author-codex/skills/discover/SKILL.md`
- Create: `~/plugins/clo-author-codex/skills/strategize/SKILL.md`
- Create: `~/plugins/clo-author-codex/skills/analyze/SKILL.md`
- Create: `~/plugins/clo-author-codex/skills/write/SKILL.md`
- Create: `~/plugins/clo-author-codex/skills/review/SKILL.md`
- Create: `~/plugins/clo-author-codex/skills/revise/SKILL.md`
- Create: `~/plugins/clo-author-codex/skills/talk/SKILL.md`
- Create: `~/plugins/clo-author-codex/skills/submit/SKILL.md`
- Create: `~/plugins/clo-author-codex/skills/tools/SKILL.md`
- Create: `~/plugins/clo-author-codex/references/domain-profile.md`
- Create: `~/plugins/clo-author-codex/references/journal-profiles.md`
- Create: `~/plugins/clo-author-codex/references/quality.md`

- [ ] **Step 1: Write the failing skill inventory test**

Create a test that asserts all 10 workflow skills exist:

```python
from pathlib import Path


def test_all_workflow_skills_exist():
    skill_root = Path.home() / "plugins/clo-author-codex/skills"
    expected = {
        "new-project",
        "discover",
        "strategize",
        "analyze",
        "write",
        "review",
        "revise",
        "talk",
        "submit",
        "tools",
    }
    assert expected.issubset({path.name for path in skill_root.iterdir() if path.is_dir()})
```

- [ ] **Step 2: Run the test and verify it fails**

Run:

```bash
python3 -m unittest discover -s clo-author/tests
```

Expected: failure until the skill directories and files are created

- [ ] **Step 3: Port the minimal viable skill set**

Each `SKILL.md` should define:

```md
---
name: discover
description: Run the clo-author discovery workflow in Codex for interviews, literature review, data discovery, and ideation.
---

# Discover

- Detect project metadata from `clo-author.toml` and `AGENTS.md`
- Read the relevant prompt and reference files
- Default to worker output followed by critic review
- Save artifacts under `quality_reports/`
```

- [ ] **Step 4: Re-run the skill inventory test**

Run:

```bash
python3 -m unittest discover -s clo-author/tests
```

Expected: the skill inventory test passes

### Task 5: Implement auto-detection and automatic workflow hooks

**Files:**
- Create: `~/plugins/clo-author-codex/hooks/project-detect.sh`
- Create: `~/plugins/clo-author-codex/hooks/post-action-review.sh`
- Create: `~/plugins/clo-author-codex/scripts/detect_project.py`
- Create: `~/plugins/clo-author-codex/scripts/log_session.py`
- Create: `~/plugins/clo-author-codex/scripts/queue_review.py`

- [ ] **Step 1: Write the failing detection test**

Create a test that feeds a clo-author-style temp directory to the detector and expects a positive match:

```python
import subprocess
import tempfile
from pathlib import Path


def test_detect_project_identifies_clo_author_layout():
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        for rel in ["paper", "quality_reports/plans", "quality_reports/session_logs"]:
            root.joinpath(rel).mkdir(parents=True, exist_ok=True)
        root.joinpath("clo-author.toml").write_text("[project]\nname='Demo'\n")
        result = subprocess.run(
            [
                "python3",
                str(Path.home() / "plugins/clo-author-codex/scripts/detect_project.py"),
                str(root),
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        assert "MATCH" in result.stdout
```

- [ ] **Step 2: Run the test and verify it fails**

Run:

```bash
python3 -m unittest discover -s clo-author/tests
```

Expected: failure because the detection script does not exist yet

- [ ] **Step 3: Implement the detector and hook shims**

Create a detector that checks for `clo-author.toml`, `AGENTS.md`, and the research directory layout, then emits a simple structured result. Create hook shims that call the detector, initialize plan/log behavior, and enqueue review prompts for substantial edits.

- [ ] **Step 4: Re-run the detection test**

Run:

```bash
python3 -m unittest discover -s clo-author/tests
```

Expected: detection test passes

### Task 6: Add migration utilities for existing repositories

**Files:**
- Create: `~/plugins/clo-author-codex/scripts/migrate_existing_project.py`
- Create: `~/plugins/clo-author-codex/assets/project-template/archive/README.md`
- Modify: `~/plugins/clo-author-codex/assets/project-template/AGENTS.md`

- [ ] **Step 1: Write the failing migration test**

Create a test that points the migration script at a copy of the current repo and expects Codex-facing files to be created without deleting `.claude/`:

```python
def test_migration_adds_codex_files_without_removing_claude_assets():
    ...
```

- [ ] **Step 2: Run the test and verify it fails**

Run:

```bash
python3 -m unittest discover -s clo-author/tests
```

Expected: failure because the migration utility does not exist yet

- [ ] **Step 3: Implement the migration utility minimally**

The migration utility should:

```python
def migrate_existing_project(project_root: Path) -> None:
    # add AGENTS.md if missing
    # add clo-author.toml if missing
    # ensure quality_reports/specs exists
    # leave .claude untouched on first pass
```

- [ ] **Step 4: Re-run the migration test**

Run:

```bash
python3 -m unittest discover -s clo-author/tests
```

Expected: migration test passes

### Task 7: Verify the end-to-end plugin flow

**Files:**
- Test: `clo-author/tests/test_plugin_bootstrap.py`
- Test: `clo-author/tests/test_project_init.py`
- Test: `clo-author/tests/test_project_detect.py`
- Test: `clo-author/tests/test_project_migrate.py`

- [ ] **Step 1: Run the focused test suite**

Run:

```bash
python3 -m unittest discover -s clo-author/tests -v
```

Expected: all plugin bootstrap, init, detection, and migration tests pass

- [ ] **Step 2: Run an end-to-end initializer smoke test**

Run:

```bash
TMPDIR="$(mktemp -d)" && python3 ~/plugins/clo-author-codex/scripts/init_project.py --target "$TMPDIR/demo" --project-name "Demo Project"
```

Expected: exit `0` and generated project files under `$TMPDIR/demo`

- [ ] **Step 3: Run an end-to-end migration smoke test**

Run:

```bash
TMPDIR="$(mktemp -d)" && cp -R /Users/youdele100fen/Documents/Codex/Project\ 0401/clo-author "$TMPDIR/clo-author-copy" && python3 ~/plugins/clo-author-codex/scripts/migrate_existing_project.py "$TMPDIR/clo-author-copy"
```

Expected: exit `0`, `AGENTS.md` present, `.claude/` still present

- [ ] **Step 4: Record verification evidence**

Save verification details to:

```text
/Users/youdele100fen/Documents/Codex/Project 0401/clo-author/quality_reports/session_logs/2026-04-01_codex-plugin-migration.md
```
