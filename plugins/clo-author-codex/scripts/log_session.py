#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Write a clo-author session log stub.")
    parser.add_argument("project_root")
    parser.add_argument("--title", default="codex-session")
    parser.add_argument("--status", default="IN PROGRESS")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    project_root = Path(args.project_root).expanduser().resolve()
    slug = args.title.strip().lower().replace(" ", "-")
    log_path = project_root / "quality_reports" / "session_logs" / f"{date.today().isoformat()}_{slug}.md"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    if not log_path.exists():
        log_path.write_text(
            f"# Session Log: {date.today().isoformat()} -- {args.title}\n\n"
            f"**Status:** {args.status}\n\n"
            "## Objective\n\n"
            "- Capture the current Codex workflow state.\n"
        )
    print(log_path)


if __name__ == "__main__":
    main()
