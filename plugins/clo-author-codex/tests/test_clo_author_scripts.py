from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
INIT_SCRIPT = PLUGIN_ROOT / "scripts" / "init_project.py"
MIGRATE_SCRIPT = PLUGIN_ROOT / "scripts" / "migrate_existing_project.py"


def run_script(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *args],
        cwd=PLUGIN_ROOT,
        text=True,
        capture_output=True,
        check=True,
    )


class CloAuthorScriptTests(unittest.TestCase):
    def test_init_project_creates_v42_runtime_scaffold(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "demo-project"

            run_script(
                str(INIT_SCRIPT),
                "--target",
                str(target),
                "--project-name",
                "Demo Project",
                "--field",
                "Economics",
                "--institution",
                "Codex Lab",
            )

            expected_paths = [
                "AGENTS.md",
                "CLAUDE.md",
                "MEMORY.md",
                "Bibliography_base.bib",
                "clo-author.toml",
                ".gitignore",
                ".claude/settings.json",
                ".claude/hooks/pre-compact.py",
                ".claude/hooks/post-compact-restore.py",
                ".claude/rules/content-invariants.md",
                ".claude/references/personal-style-guide.md",
                ".claude/skills/checkpoint/SKILL.md",
                ".claude/agents/theorist.md",
                ".claude/agents/theorist-critic.md",
                ".claude/state/obsidian-config.md.example",
                "templates/decision-record.md",
                "paper/latexmkrc",
                "quality_reports/plans",
                "quality_reports/session_logs",
            ]
            for rel in expected_paths:
                self.assertTrue(target.joinpath(rel).exists(), rel)

            self.assertIn("Demo Project", target.joinpath("AGENTS.md").read_text())
            self.assertIn("Demo Project", target.joinpath("CLAUDE.md").read_text())
            self.assertTrue(target.joinpath(".claude/hooks/pre-compact.py").stat().st_mode & 0o111)
            self.assertTrue(target.joinpath(".claude/hooks/protect-files.sh").stat().st_mode & 0o111)

    def test_migrate_default_preserves_existing_files_and_adds_missing_scaffold(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "existing-project"
            project.mkdir()
            project.joinpath("AGENTS.md").write_text("CUSTOM AGENTS\n")
            project.joinpath(".claude").mkdir()
            project.joinpath(".claude/settings.json").write_text('{"custom": true}\n')

            run_script(
                str(MIGRATE_SCRIPT),
                str(project),
                "--project-name",
                "Existing Project",
                "--field",
                "Economics",
                "--institution",
                "Codex Lab",
            )

            self.assertEqual("CUSTOM AGENTS\n", project.joinpath("AGENTS.md").read_text())
            self.assertEqual('{"custom": true}\n', project.joinpath(".claude/settings.json").read_text())
            self.assertTrue(project.joinpath(".claude/skills/checkpoint/SKILL.md").exists())
            self.assertTrue(project.joinpath(".claude/agents/theorist.md").exists())
            self.assertTrue(project.joinpath("clo-author.toml").exists())

    def test_migrate_refresh_scaffold_archives_then_replaces_managed_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "refresh-project"
            project.mkdir()
            project.joinpath("AGENTS.md").write_text("CUSTOM AGENTS\n")
            project.joinpath(".claude/hooks").mkdir(parents=True)
            project.joinpath(".claude/settings.json").write_text('{"custom": true}\n')

            run_script(
                str(MIGRATE_SCRIPT),
                str(project),
                "--project-name",
                "Refresh Project",
                "--field",
                "Economics",
                "--institution",
                "Codex Lab",
                "--refresh-scaffold",
            )

            archives = sorted(project.glob("archive/codex-plugin-refresh/*"))
            self.assertEqual(1, len(archives))
            self.assertEqual("CUSTOM AGENTS\n", archives[0].joinpath("AGENTS.md").read_text())
            self.assertEqual('{"custom": true}\n', archives[0].joinpath(".claude/settings.json").read_text())
            self.assertIn("Refresh Project", project.joinpath("AGENTS.md").read_text())
            self.assertIn("PreCompact", project.joinpath(".claude/settings.json").read_text())
            self.assertTrue(project.joinpath(".claude/skills/checkpoint/SKILL.md").exists())


if __name__ == "__main__":
    unittest.main()
