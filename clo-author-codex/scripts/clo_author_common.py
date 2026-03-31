from __future__ import annotations

import re
import shutil
from pathlib import Path


PROJECT_MARKERS = ("clo-author.toml", "AGENTS.md", "CLAUDE.md")
REQUIRED_LAYOUT = (
    "paper",
    "quality_reports/plans",
    "quality_reports/session_logs",
)
TEXT_EXTENSIONS = {".md", ".toml", ".txt"}


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.strip().lower())
    slug = re.sub(r"-{2,}", "-", slug)
    return slug.strip("-") or "research-project"


def detect_project(root: Path) -> tuple[bool, list[str]]:
    root = root.expanduser().resolve()
    reasons: list[str] = []
    for marker in PROJECT_MARKERS:
        if root.joinpath(marker).exists():
            reasons.append(marker)
    if root.joinpath(".claude").exists():
        reasons.append(".claude")
    missing_layout = [rel for rel in REQUIRED_LAYOUT if not root.joinpath(rel).exists()]
    if reasons and not missing_layout:
        return True, reasons
    return False, missing_layout if missing_layout else ["missing clo-author markers"]


def template_root() -> Path:
    return Path(__file__).resolve().parents[1] / "assets" / "project-template"


def apply_replacements(text: str, replacements: dict[str, str]) -> str:
    for key, value in replacements.items():
        text = text.replace(key, value)
    return text


def materialize_template(target_root: Path, replacements: dict[str, str]) -> None:
    source = template_root()
    shutil.copytree(source, target_root)
    for path in target_root.rglob("*"):
        if path.is_file() and path.suffix in TEXT_EXTENSIONS:
            path.write_text(apply_replacements(path.read_text(), replacements))


def build_replacements(project_name: str, field: str, institution: str) -> dict[str, str]:
    return {
        "__PROJECT_NAME__": project_name,
        "__PROJECT_SLUG__": slugify(project_name),
        "__FIELD__": field,
        "__INSTITUTION__": institution,
    }
