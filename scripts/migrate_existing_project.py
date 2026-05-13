#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from clo_author_common import add_missing_template_files, build_replacements, refresh_template_files


PRESERVED_REFRESH_FILES = (
    ".claude/references/domain-profile.md",
    ".claude/settings.json",
    ".claude/settings.local.json",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Migrate an existing clo-author project to Codex.")
    parser.add_argument("project_root", help="Existing project root")
    parser.add_argument("--project-name", default=None)
    parser.add_argument("--field", default="Empirical Social Science")
    parser.add_argument("--institution", default="TBD")
    parser.add_argument(
        "--refresh-scaffold",
        action="store_true",
        help="Archive and refresh plugin-managed scaffold files instead of only filling gaps",
    )
    return parser.parse_args()


def snapshot_existing_files(project_root: Path, relative_paths: tuple[str, ...]) -> dict[str, str]:
    snapshots: dict[str, str] = {}
    for rel in relative_paths:
        path = project_root / rel
        if path.exists() and path.is_file():
            snapshots[rel] = path.read_text()
    return snapshots


def restore_snapshots(project_root: Path, snapshots: dict[str, str]) -> None:
    for rel, contents in snapshots.items():
        path = project_root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(contents)


def main() -> None:
    args = parse_args()
    project_root = Path(args.project_root).expanduser().resolve()
    if not project_root.exists():
        raise SystemExit(f"Project root does not exist: {project_root}")

    project_name = args.project_name or project_root.name.replace("-", " ").title()
    replacements = build_replacements(project_name, args.field, args.institution)

    if args.refresh_scaffold:
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        archive_root = project_root / "archive" / "codex-plugin-refresh" / timestamp
        preserved = snapshot_existing_files(project_root, PRESERVED_REFRESH_FILES)
        refresh_template_files(project_root, archive_root, replacements)
        restore_snapshots(project_root, preserved)
        print(f"Refreshed clo-author scaffold at {project_root}")
        print(f"Archived replaced files under {archive_root}")
        if preserved:
            print(f"Preserved custom files: {', '.join(sorted(preserved))}")
    else:
        add_missing_template_files(project_root, replacements)
        print(f"Migrated clo-author project at {project_root}")


if __name__ == "__main__":
    main()
