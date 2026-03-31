#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from clo_author_common import detect_project


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: detect_project.py <project-root>")

    project_root = Path(sys.argv[1])
    matched, details = detect_project(project_root)
    if matched:
        print(f"MATCH: clo-author project detected via {', '.join(details)}")
        raise SystemExit(0)

    print(f"NO MATCH: {', '.join(details)}")
    raise SystemExit(1)


if __name__ == "__main__":
    main()
