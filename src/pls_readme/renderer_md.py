from __future__ import annotations
from pathlib import Path
from typing import List

from .scanner import RepoScan
from .heuristics import Suggestions
from .utils import human_int

def render_tree(repo_path: Path, depth: int = 3, include_hidden: bool = False, max_entries: int = 200) -> str:
    """
    Lightweight tree rendering.
    """
    lines: List[str] = []
    repo_path = repo_path.resolve()

    def walk(dir_path: Path, prefix: str, level: int, entries_left: List[int]):
        if level > depth or entries_left[0] <= 0:
            return
        items = sorted(dir_path.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))
        if not include_hidden:
            items = [p for p in items if not any(part.startswith(".") for part in p.relative_to(repo_path).parts)]
        
        items = [p for p in items if p.name not in {".git", "node_modules", "build", "dist", ".venv", "venv"}]

        for i, p in enumerate(items):
            if entries_left[0] <= 0:
                return
            connector = "└── " if i == len(items) - 1 else "├── "
            lines.append(prefix + connector + p.name + ("/" if p.is_dir() else ""))
            entries_left[0] -= 1
            if p.is_dir():
                extension = "    " if i == len(items) - 1 else "│   "
                walk(p, prefix + extension, level + 1, entries_left)

    lines.append(f"{repo_path.name}/")
    walk(repo_path, "", 1, [max_entries])
    return "\n".join(lines)

def _render_badges(github_repo: str | None) -> str:
    """
    Generate GitHub badges.
    - If github_repo is provided (OWNER/REPO), use it.
    - Otherwise, fall back to placeholder 'username/repo'.
    """
    repo = github_repo if github_repo else "username/repo"

    return (
        f"![Repo Size](https://img.shields.io/github/repo-size/{repo}"
        f"?style=for-the-badge&color=blue)\n"
        f"![Languages](https://img.shields.io/github/languages/count/{repo}"
        f"?style=for-the-badge&color=orange)\n"
        f"![Forks](https://img.shields.io/github/forks/{repo}"
        f"?style=for-the-badge&color=brightgreen)\n"
        f"![Issues](https://img.shields.io/github/issues/{repo}"
        f"?style=for-the-badge&color=red)\n"
    )

def render_markdown(scan: RepoScan, sug: Suggestions, depth: int, include_hidden: bool, show_tree: bool = True, github_repo: str | None = None) -> str:
    name = scan.repo_path.name

    # Formatting Language list
    langs = "\n".join([f"- {k}: {v} file(s)" for k, v in scan.languages.items()]) or "- (No recognized source files found)"
    key_folders = ", ".join(scan.key_folders) if scan.key_folders else "(none detected)"

    # Tree Block
    tree_block = ""
    if show_tree:
        tree = render_tree(scan.repo_path, depth=min(3, depth), include_hidden=include_hidden)
        tree_block = f"\n## 📂 Project Structure\n\n```text\n{tree}\n```\n"

    tech_stack = "\n".join([f"- {t}" for t in sug.tech_stack]) or "- (unknown)"
    how_to_run = "\n".join(sug.how_to_run) if isinstance(sug.how_to_run, list) else str(sug.how_to_run)
    notes = "\n".join([f"- {n}" for n in sug.notes]) if sug.notes else "- (none)"

    badges = _render_badges(github_repo)

    # Construction of the new visual format
    return f"""# {name}

{badges}

---

![Project Screenshot](https://via.placeholder.com/800x400.png?text=Exemplo+imagem)

> This project is currently in development. Replace this block with a 2-3 line introduction about what the project does. Keep it concise; people appreciate brevity.

---

## 📊 Repo Stats
- **Files scanned:** {human_int(scan.file_count)}
- **Directories scanned:** {human_int(scan.dir_count)}
- **Key folders:** {key_folders}

## 🛠 Tech Stack
{tech_stack}

## 📜 Language Breakdown
{langs}
{tree_block}
## 🚀 How to Run
{how_to_run}

## 📝 Notes
{notes}

## ✅ Ajustes e melhorias (Roadmap)
The project is under active development. The following tasks are planned:

- [x] Initial repository scan logic
- [x] Tech stack inference
- [ ] Smarter entrypoint detection
- [ ] Support for `.gitignore`
- [ ] Automatic badge URL generation
"""