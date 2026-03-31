import subprocess
import tempfile
import unittest
from pathlib import Path


DETECT_SCRIPT = Path.home() / "plugins" / "clo-author-codex" / "scripts" / "detect_project.py"


class ProjectDetectTests(unittest.TestCase):
    def test_detect_project_identifies_clo_author_layout(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            for rel in ["paper", "quality_reports/plans", "quality_reports/session_logs"]:
                root.joinpath(rel).mkdir(parents=True, exist_ok=True)
            root.joinpath("AGENTS.md").write_text("# Demo Project\n")
            root.joinpath("clo-author.toml").write_text("[project]\nname = 'Demo'\n")

            result = subprocess.run(
                ["python3", str(DETECT_SCRIPT), str(root)],
                capture_output=True,
                text=True,
                check=True,
            )

            self.assertIn("MATCH", result.stdout)

