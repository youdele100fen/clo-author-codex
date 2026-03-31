#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from clo_author_common import build_replacements, template_root


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Migrate an existing clo-author project to Codex.")
    parser.add_argument("project_root", help="Existing project root")
    parser.add_argument("--project-name", default=None)
    parser.add_argument("--field", default="Empirical Social Science")
    parser.add_argument("--institution", default="TBD")
    return parser.parse_args()


def ensure_text_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(content)


def main() -> None:
    args = parse_args()
    project_root = Path(args.project_root).expanduser().resolve()
    if not project_root.exists():
        raise SystemExit(f"Project root does not exist: {project_root}")

    project_name = args.project_name or project_root.name.replace("-", " ").title()
    replacements = build_replacements(project_name, args.field, args.institution)
    source = template_root()

    agents_template = source.joinpath("AGENTS.md").read_text()
    memory_template = source.joinpath("MEMORY.md").read_text()
    toml_template = source.joinpath("clo-author.toml").read_text()

    for rel in [
        "quality_reports/specs",
        "quality_reports/plans",
        "quality_reports/session_logs",
        "archive/claude",
    ]:
        project_root.joinpath(rel).mkdir(parents=True, exist_ok=True)

    ensure_text_file(
        project_root / "AGENTS.md",
        agents_template.replace("__PROJECT_NAME__", replacements["__PROJECT_NAME__"])
        .replace("__PROJECT_SLUG__", replacements["__PROJECT_SLUG__"])
        .replace("__FIELD__", replacements["__FIELD__"])
        .replace("__INSTITUTION__", replacements["__INSTITUTION__"]),
    )
    ensure_text_file(project_root / "MEMORY.md", memory_template.replace("__PROJECT_NAME__", project_name))
    ensure_text_file(
        project_root / "clo-author.toml",
        toml_template.replace("__PROJECT_NAME__", replacements["__PROJECT_NAME__"])
        .replace("__PROJECT_SLUG__", replacements["__PROJECT_SLUG__"])
        .replace("__FIELD__", replacements["__FIELD__"])
        .replace("__INSTITUTION__", replacements["__INSTITUTION__"]),
    )
    ensure_text_file(
        project_root / "archive/claude/README.md",
        "# Legacy Claude Assets\n\nThe original `.claude/` workflow remains in place for reference during Codex migration.\n",
    )
    print(f"Migrated clo-author project at {project_root}")


if __name__ == "__main__":
    main()
