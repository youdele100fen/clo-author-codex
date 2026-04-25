#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from clo_author_common import detect_project


REVIEW_PREFIXES = ("paper", "scripts", "AGENTS.md", "clo-author.toml")


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit("Usage: queue_review.py <project-root> [changed-paths...]")

    project_root = Path(sys.argv[1]).expanduser().resolve()
    matched, _ = detect_project(project_root)
    if not matched:
        print("SKIP: not a clo-author project")
        raise SystemExit(0)

    changed = sys.argv[2:]
    if not changed:
        print("REVIEW_REQUIRED: substantial edit review should be considered")
        raise SystemExit(0)

    if any(path.startswith(REVIEW_PREFIXES) for path in changed):
        print("REVIEW_REQUIRED: worker-critic review recommended")
    else:
        print("REVIEW_OPTIONAL: no high-signal paths detected")


if __name__ == "__main__":
    main()
