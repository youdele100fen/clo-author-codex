#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import sys


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from clo_author_common import detect_project


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Detect whether a directory is a clo-author project.")
    parser.add_argument("project_root", help="Project root to inspect")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    project_root = Path(args.project_root)
    matched, details = detect_project(project_root)
    if matched:
        print(f"MATCH: clo-author project detected via {', '.join(details)}")
        raise SystemExit(0)

    print(f"NO MATCH: {', '.join(details)}")
    raise SystemExit(1)


if __name__ == "__main__":
    main()
