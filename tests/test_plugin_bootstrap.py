import json
import unittest
from pathlib import Path


PLUGIN_ROOT = Path.home() / "plugins" / "clo-author-codex"


class PluginBootstrapTests(unittest.TestCase):
    def test_plugin_manifest_exists_and_is_customized(self) -> None:
        manifest_path = PLUGIN_ROOT / ".codex-plugin" / "plugin.json"
        self.assertTrue(manifest_path.exists(), "plugin manifest should exist")

        manifest = json.loads(manifest_path.read_text())
        self.assertEqual(manifest["name"], "clo-author-codex")
        self.assertEqual(manifest["skills"], "./skills/")
        self.assertEqual(manifest["hooks"], "./hooks.json")

        interface = manifest["interface"]
        self.assertEqual(interface["displayName"], "Clo-Author Codex")
        self.assertIn("research", interface["shortDescription"].lower())

    def test_all_workflow_skills_exist(self) -> None:
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
        skill_root = PLUGIN_ROOT / "skills"
        self.assertTrue(skill_root.exists(), "skills directory should exist")
        found = {path.name for path in skill_root.iterdir() if path.is_dir()}
        self.assertTrue(expected.issubset(found), f"missing workflow skills: {expected - found}")

