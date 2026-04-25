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
TEXT_EXTENSIONS = {".bib", ".json", ".md", ".qmd", ".tex", ".toml", ".txt", ".yml"}
EXECUTABLE_EXTENSIONS = {".py", ".sh"}


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


def should_skip_template_path(path: Path) -> bool:
    return path.name in {".DS_Store", "__pycache__"} or "__pycache__" in path.parts


def is_text_file(path: Path) -> bool:
    return path.suffix in TEXT_EXTENSIONS or path.name in {".gitignore", "latexmkrc"}


def write_template_file(source: Path, destination: Path, replacements: dict[str, str]) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if is_text_file(source):
        destination.write_text(apply_replacements(source.read_text(), replacements))
    else:
        shutil.copy2(source, destination)
    if source.suffix in EXECUTABLE_EXTENSIONS:
        destination.chmod(destination.stat().st_mode | 0o111)


def iter_template_files() -> list[Path]:
    source = template_root()
    return [
        path
        for path in source.rglob("*")
        if path.is_file() and not should_skip_template_path(path.relative_to(source))
    ]


def materialize_template(target_root: Path, replacements: dict[str, str]) -> None:
    source = template_root()
    shutil.copytree(source, target_root)
    for path in target_root.rglob("*"):
        if not path.is_file():
            continue
        if should_skip_template_path(path.relative_to(target_root)):
            path.unlink()
            continue
        if is_text_file(path):
            path.write_text(apply_replacements(path.read_text(), replacements))
        if path.suffix in EXECUTABLE_EXTENSIONS:
            path.chmod(path.stat().st_mode | 0o111)


def add_missing_template_files(target_root: Path, replacements: dict[str, str]) -> None:
    source = template_root()
    for source_path in iter_template_files():
        rel = source_path.relative_to(source)
        destination = target_root / rel
        if not destination.exists():
            write_template_file(source_path, destination, replacements)


def refresh_template_files(target_root: Path, archive_root: Path, replacements: dict[str, str]) -> None:
    source = template_root()
    for source_path in iter_template_files():
        rel = source_path.relative_to(source)
        destination = target_root / rel
        if destination.exists():
            archive_path = archive_root / rel
            archive_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(destination, archive_path)
        write_template_file(source_path, destination, replacements)


def build_replacements(project_name: str, field: str, institution: str) -> dict[str, str]:
    project_slug = slugify(project_name)
    return {
        "__PROJECT_NAME__": project_name,
        "__PROJECT_SLUG__": project_slug,
        "__FIELD__": field,
        "__INSTITUTION__": institution,
        "[YOUR PROJECT NAME]": project_name,
        "[YOUR INSTITUTION]": institution,
        "[YOUR FIELD — Economics by default. Can be adapted to Finance, Accounting, Marketing, etc.]": field,
        "[YOUR-PROJECT]": project_slug,
    }
