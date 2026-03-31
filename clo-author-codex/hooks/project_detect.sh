#!/bin/sh
SCRIPT_DIR="$(CDPATH= cd -- "$(dirname "$0")" && pwd)"
python3 "$SCRIPT_DIR/../scripts/detect_project.py" "${1:-$PWD}" || true
