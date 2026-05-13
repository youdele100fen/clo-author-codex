#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from clo_author_common import build_replacements, materialize_template


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Initialize a clo-author Codex project.")
    parser.add_argument("--target", required=True, help="Target directory for the project")
    parser.add_argument("--project-name", required=True, help="Human-readable project name")
    parser.add_argument("--field", default="Empirical Social Science")
    parser.add_argument("--institution", default="TBD")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    target = Path(args.target).expanduser().resolve()
    if target.exists():
        raise SystemExit(f"Target already exists: {target}")

    replacements = build_replacements(args.project_name, args.field, args.institution)
    materialize_template(target, replacements)
    print(f"Created clo-author Codex project at {target}")


if __name__ == "__main__":
    main()
