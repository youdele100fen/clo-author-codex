#!/bin/sh
SCRIPT_DIR="$(CDPATH= cd -- "$(dirname "$0")" && pwd)"
python3 "$SCRIPT_DIR/../scripts/queue_review.py" "${1:-$PWD}" || true
