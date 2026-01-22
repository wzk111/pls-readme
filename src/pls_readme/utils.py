from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

DEFAULT_IGNORE_DIRS = {
    ".git", ".idea", ".vscode", "__pycache__", "node_modules", "dist", "build",
    ".pytest_cache", ".mypy_cache", ".venv", "venv", ".DS_Store",
}

DEFAULT_IGNORE_FILES = {
    ".DS_Store",
}

def is_hidden(path: Path) -> bool:
    return any(part.startswith(".") for part in path.parts)

def should_ignore(path: Path, include_hidden: bool) -> bool:
    name = path.name
    if not include_hidden and is_hidden(path):
        return True
    if path.is_dir() and name in DEFAULT_IGNORE_DIRS:
        return True
    if path.is_file() and name in DEFAULT_IGNORE_FILES:
        return True
    return False

def clamp(n: int, lo: int, hi: int) -> int:
    return max(lo, min(hi, n))

def human_int(n: int) -> str:
    return f"{n:,}"
