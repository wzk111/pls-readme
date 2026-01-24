from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List
from collections import Counter

from .utils import should_ignore
from .gitignore import load_gitignore_spec

EXT_TO_LANG = {
    ".py": "Python",
    ".js": "JavaScript",
    ".ts": "TypeScript",
    ".java": "Java",
    ".cpp": "C++",
    ".cc": "C++",
    ".c": "C",
    ".hpp": "C++",
    ".h": "C/C++ Header",
    ".cs": "C#",
    ".go": "Go",
    ".rs": "Rust",
    ".kt": "Kotlin",
    ".swift": "Swift",
    ".rb": "Ruby",
    ".php": "PHP",
    ".html": "HTML",
    ".css": "CSS",
    ".sql": "SQL",
    ".yml": "YAML",
    ".yaml": "YAML",
    ".json": "JSON",
    ".md": "Markdown",
    ".sh": "Shell",
    ".bat": "Batch",
    ".ps1": "PowerShell",
}

KEY_FOLDERS = ["src", "include", "tests", "test", "docs", "examples", "scripts"]

@dataclass
class RepoScan:
    repo_path: Path
    file_count: int
    dir_count: int
    languages: Dict[str, int]
    key_folders: List[str]
    has_cmake: bool
    has_package_json: bool
    has_pyproject: bool
    has_requirements: bool
    has_makefile: bool
    top_files: List[str] = field(default_factory=list)

def scan_repo(
    repo_path: Path,
    include_hidden: bool = False,
    max_files: int = 5000,
    depth: int = 6,
    respect_gitignore: bool = True,
) -> RepoScan:
    repo_path = repo_path.resolve()
    if not repo_path.exists() or not repo_path.is_dir():
        raise FileNotFoundError(f"Repo path not found or not a directory: {repo_path}")

    max_files = max(1, max_files)
    depth = max(1, depth)

    # NEW: load .gitignore matcher once
    ignore = load_gitignore_spec(repo_path) if respect_gitignore else None

    lang_counter: Counter[str] = Counter()
    file_count = 0
    dir_count = 0

    found_key_folders = set()
    top_files: List[str] = []

    def within_depth(p: Path) -> bool:
        rel_parts = p.relative_to(repo_path).parts
        return len(rel_parts) <= depth

    def is_gitignored(p: Path) -> bool:
        if ignore is None:
            return False
        rel = p.relative_to(repo_path).as_posix()
        if p.is_dir() and not rel.endswith("/"):
            rel_dir = rel + "/"
            return ignore.match_rel(rel_dir) or ignore.match_rel(rel)
        return ignore.match_rel(rel)

    for p in repo_path.rglob("*"):
        if not within_depth(p):
            continue

        # your existing "hidden + common folders" ignore
        if should_ignore(p, include_hidden=include_hidden):
            continue

        # NEW: skip gitignored paths
        if is_gitignored(p):
            continue

        if p.is_dir():
            dir_count += 1
            if p.name in KEY_FOLDERS and p.parent == repo_path:
                found_key_folders.add(p.name)
            continue

        if p.is_file():
            file_count += 1
            if file_count <= 30:
                top_files.append(str(p.relative_to(repo_path)))

            if file_count >= max_files:
                break

            ext = p.suffix.lower()
            lang = EXT_TO_LANG.get(ext)
            if lang:
                lang_counter[lang] += 1

    has_cmake = (repo_path / "CMakeLists.txt").exists()
    has_package_json = (repo_path / "package.json").exists()
    has_pyproject = (repo_path / "pyproject.toml").exists()
    has_requirements = (repo_path / "requirements.txt").exists()
    has_makefile = (repo_path / "Makefile").exists()

    return RepoScan(
        repo_path=repo_path,
        file_count=file_count,
        dir_count=dir_count,
        languages=dict(lang_counter.most_common()),
        key_folders=sorted(found_key_folders),
        has_cmake=has_cmake,
        has_package_json=has_package_json,
        has_pyproject=has_pyproject,
        has_requirements=has_requirements,
        has_makefile=has_makefile,
        top_files=top_files,
    )
