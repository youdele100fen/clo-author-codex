import subprocess
import tempfile
import unittest
from pathlib import Path


MIGRATE_SCRIPT = Path.home() / "plugins" / "clo-author-codex" / "scripts" / "migrate_existing_project.py"


class ProjectMigrateTests(unittest.TestCase):
    def test_migration_adds_codex_files_without_removing_claude_assets(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir) / "legacy-project"
            root.mkdir()
            for rel in [".claude/skills", "paper", "quality_reports/plans", "quality_reports/session_logs"]:
                root.joinpath(rel).mkdir(parents=True, exist_ok=True)
            root.joinpath("CLAUDE.md").write_text("# Legacy\n")

            subprocess.run(["python3", str(MIGRATE_SCRIPT), str(root)], check=True)

            self.assertTrue(root.joinpath("AGENTS.md").exists())
            self.assertTrue(root.joinpath("clo-author.toml").exists())
            self.assertTrue(root.joinpath(".claude").exists())
