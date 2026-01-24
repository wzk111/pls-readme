from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional

import pathspec


@dataclass
class IgnoreMatcher:
    """
    Matches paths relative to repo root using .gitignore rules.
    """
    repo_root: Path
    spec: pathspec.PathSpec

    def match_rel(self, rel_posix: str) -> bool:
        # pathspec expects posix-style paths
        return self.spec.match_file(rel_posix)


def load_gitignore_spec(repo_root: Path) -> IgnoreMatcher:
    """
    Load ignore rules from:
      - <repo>/.gitignore
      - <repo>/.git/info/exclude (optional)
    Note: This is a pragmatic subset, not a full 'git check-ignore' clone.
    """
    repo_root = repo_root.resolve()
    patterns: List[str] = []

    gitignore = repo_root / ".gitignore"
    if gitignore.exists() and gitignore.is_file():
        patterns += _read_patterns(gitignore)

    exclude = repo_root / ".git" / "info" / "exclude"
    if exclude.exists() and exclude.is_file():
        patterns += _read_patterns(exclude)

    # Always ignore .git itself (even if not present in gitignore)
    patterns.append(".git/")

    spec = pathspec.PathSpec.from_lines("gitwildmatch", patterns)
    return IgnoreMatcher(repo_root=repo_root, spec=spec)


def _read_patterns(path: Path) -> List[str]:
    lines: List[str] = []
    for raw in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        s = raw.strip()
        if not s or s.startswith("#"):
            continue
        lines.append(s)
    return lines
