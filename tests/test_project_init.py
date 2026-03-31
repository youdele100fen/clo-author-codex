import subprocess
import tempfile
import unittest
from pathlib import Path


INIT_SCRIPT = Path.home() / "plugins" / "clo-author-codex" / "scripts" / "init_project.py"


class ProjectInitTests(unittest.TestCase):
    def test_init_project_creates_codex_research_layout(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / "demo-project"
            subprocess.run(
                [
                    "python3",
                    str(INIT_SCRIPT),
                    "--target",
                    str(target),
                    "--project-name",
                    "Demo Project",
                ],
                check=True,
            )

            self.assertTrue(target.joinpath("AGENTS.md").exists())
            self.assertTrue(target.joinpath("clo-author.toml").exists())
            self.assertTrue(target.joinpath("quality_reports", "plans").exists())
            self.assertTrue(target.joinpath("quality_reports", "session_logs").exists())
            self.assertTrue(target.joinpath("paper", "sections").exists())

