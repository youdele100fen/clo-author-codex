from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
INIT_SCRIPT = PLUGIN_ROOT / "scripts" / "init_project.py"
MIGRATE_SCRIPT = PLUGIN_ROOT / "scripts" / "migrate_existing_project.py"
DETECT_SCRIPT = PLUGIN_ROOT / "scripts" / "detect_project.py"
EXPECTED_CURRENT_SKILLS = {
    "analyze",
    "careful",
    "checkpoint",
    "dashboard",
    "discover",
    "freeze",
    "new-project",
    "review",
    "revise",
    "strategize",
    "submit",
    "talk",
    "tools",
    "write",
}


def run_script(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *args],
        cwd=PLUGIN_ROOT,
        text=True,
        capture_output=True,
        check=True,
    )


def run_script_unchecked(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *args],
        cwd=PLUGIN_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


class CloAuthorScriptTests(unittest.TestCase):
    def test_plugin_documents_codex_adapter_semantics(self) -> None:
        adapter = PLUGIN_ROOT / "references" / "codex-adapter.md"
        workflow_map = PLUGIN_ROOT / "references" / "workflow-map.md"

        self.assertTrue(adapter.exists())
        adapter_text = adapter.read_text()
        self.assertIn("Claude Code surface", adapter_text)
        self.assertIn("Codex surface", adapter_text)
        self.assertIn("worker-critic separation", adapter_text)
        self.assertIn("references/codex-adapter.md", workflow_map.read_text())

    def test_detect_project_help_uses_standard_cli_help(self) -> None:
        result = run_script_unchecked(str(DETECT_SCRIPT), "--help")

        self.assertEqual(0, result.returncode)
        self.assertIn("usage:", result.stdout)
        self.assertIn("project_root", result.stdout)
        self.assertEqual("", result.stderr)

    def test_detect_project_recognizes_upstream_claude_scaffold(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "upstream-project"
            project.joinpath(".claude").mkdir(parents=True)
            project.joinpath("paper").mkdir()
            project.joinpath("quality_reports/plans").mkdir(parents=True)
            project.joinpath("quality_reports/session_logs").mkdir(parents=True)
            project.joinpath("CLAUDE.md").write_text("# CLAUDE\n")

            result = run_script_unchecked(str(DETECT_SCRIPT), str(project))

            self.assertEqual(0, result.returncode)
            self.assertIn("MATCH: clo-author project detected", result.stdout)

    def test_init_project_creates_current_runtime_scaffold(self) -> None:
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
            self.assertIn("Claude-compatible current-main runtime assets", target.joinpath("AGENTS.md").read_text())
            self.assertIn("Codex-facing workflow entrypoints", target.joinpath("AGENTS.md").read_text())
            self.assertIn("default allow Codex subagents", target.joinpath("AGENTS.md").read_text())
            self.assertIn("ask the user once", target.joinpath("AGENTS.md").read_text())
            self.assertIn("subagents_default = \"ask-on-first-use\"", target.joinpath("clo-author.toml").read_text())
            self.assertIn("Demo Project", target.joinpath("CLAUDE.md").read_text())
            self.assertTrue(target.joinpath(".claude/hooks/pre-compact.py").stat().st_mode & 0o111)
            self.assertTrue(target.joinpath(".claude/hooks/protect-files.sh").stat().st_mode & 0o111)

    def test_adapter_documents_subagent_first_use_prompt(self) -> None:
        adapter_text = PLUGIN_ROOT.joinpath("references/codex-adapter.md").read_text()

        self.assertIn("ask the user once", adapter_text)
        self.assertIn("default allow Codex subagents", adapter_text)
        self.assertIn("legacy agents", adapter_text)

    def test_codex_skill_surface_tracks_current_upstream_main(self) -> None:
        skill_names = {
            path.parent.name
            for path in PLUGIN_ROOT.joinpath("skills").glob("*/SKILL.md")
        }

        self.assertEqual(EXPECTED_CURRENT_SKILLS, skill_names)

    def test_template_includes_current_guard_dashboard_and_html_assets(self) -> None:
        required_paths = [
            "assets/project-template/.claude/hooks/session-guard.py",
            "assets/project-template/.claude/skills/freeze/SKILL.md",
            "assets/project-template/.claude/skills/careful/SKILL.md",
            "assets/project-template/.claude/skills/dashboard/SKILL.md",
            "assets/project-template/.claude/rules/html-dashboard.md",
            "assets/project-template/scripts/generate_dashboard.py",
            "assets/project-template/scripts/generate_html_report.py",
            "assets/project-template/templates/html/base/styles.css",
            "assets/project-template/templates/html/base/components.js",
            "assets/project-template/templates/pipeline-state.json",
        ]

        for rel in required_paths:
            self.assertTrue(PLUGIN_ROOT.joinpath(rel).exists(), rel)

    def test_talk_skill_is_quarto_first_with_beamer_opt_in(self) -> None:
        skill_text = PLUGIN_ROOT.joinpath("skills/talk/SKILL.md").read_text()
        scaffold_text = PLUGIN_ROOT.joinpath(
            "assets/project-template/.claude/skills/talk/SKILL.md"
        ).read_text()

        for text in (skill_text, scaffold_text):
            self.assertIn("Quarto RevealJS is the default", text)
            self.assertIn("--beamer", text)
            self.assertNotIn("Beamer (default)", text)

    def test_init_project_creates_current_main_runtime_scaffold(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "current-main-project"

            run_script(
                str(INIT_SCRIPT),
                "--target",
                str(target),
                "--project-name",
                "Current Main Project",
                "--field",
                "Economics",
                "--institution",
                "Codex Lab",
            )

            expected_paths = [
                ".claude/hooks/session-guard.py",
                ".claude/skills/freeze/SKILL.md",
                ".claude/skills/careful/SKILL.md",
                ".claude/skills/dashboard/SKILL.md",
                ".claude/skills/analyze/templates/pre-code-report.md",
                "scripts/generate_dashboard.py",
                "scripts/generate_html_report.py",
                "templates/html/base/styles.css",
                "templates/html/base/components.js",
                "templates/pipeline-state.json",
            ]
            for rel in expected_paths:
                self.assertTrue(target.joinpath(rel).exists(), rel)

            self.assertTrue(target.joinpath(".claude/hooks/session-guard.py").stat().st_mode & 0o111)
            self.assertTrue(target.joinpath("scripts/generate_dashboard.py").stat().st_mode & 0o111)
            self.assertTrue(target.joinpath("scripts/generate_html_report.py").stat().st_mode & 0o111)

    def test_dashboard_script_smoke_test(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "dashboard-project"
            run_script(
                str(INIT_SCRIPT),
                "--target",
                str(target),
                "--project-name",
                "Dashboard Project",
                "--field",
                "Economics",
                "--institution",
                "Codex Lab",
            )

            result = subprocess.run(
                [sys.executable, "scripts/generate_dashboard.py"],
                cwd=target,
                text=True,
                capture_output=True,
                check=True,
            )

            dashboard = target / "project_dashboard.html"
            self.assertTrue(dashboard.exists(), result.stdout + result.stderr)
            self.assertIn("Dashboard Project", dashboard.read_text())

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
            self.assertEqual('{"custom": true}\n', project.joinpath(".claude/settings.json").read_text())
            self.assertTrue(project.joinpath(".claude/skills/checkpoint/SKILL.md").exists())

    def test_migrate_refresh_adds_template_settings_when_no_settings_exist(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "fresh-settings-project"
            project.mkdir()

            run_script(
                str(MIGRATE_SCRIPT),
                str(project),
                "--project-name",
                "Fresh Settings Project",
                "--field",
                "Economics",
                "--institution",
                "Codex Lab",
                "--refresh-scaffold",
            )

            self.assertIn("PreCompact", project.joinpath(".claude/settings.json").read_text())

    def test_migrate_refresh_preserves_custom_domain_profile_and_settings(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "customized-project"
            project.mkdir()
            profile = project / ".claude" / "references" / "domain-profile.md"
            settings = project / ".claude" / "settings.json"
            local_settings = project / ".claude" / "settings.local.json"
            profile.parent.mkdir(parents=True)
            profile.write_text("# Domain Profile\n\nCustom field evidence.\n")
            settings.write_text('{"custom": true}\n')
            local_settings.write_text('{"local": true}\n')

            run_script(
                str(MIGRATE_SCRIPT),
                str(project),
                "--project-name",
                "Customized Project",
                "--field",
                "Economics",
                "--institution",
                "Codex Lab",
                "--refresh-scaffold",
            )

            self.assertEqual("# Domain Profile\n\nCustom field evidence.\n", profile.read_text())
            self.assertEqual('{"custom": true}\n', settings.read_text())
            self.assertEqual('{"local": true}\n', local_settings.read_text())


if __name__ == "__main__":
    unittest.main()
