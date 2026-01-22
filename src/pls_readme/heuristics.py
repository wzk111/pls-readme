from __future__ import annotations
from dataclasses import dataclass
from typing import List
from pathlib import Path

from .scanner import RepoScan

@dataclass
class Suggestions:
    tech_stack: List[str]
    how_to_run: List[str]
    notes: List[str]

def infer_suggestions(scan: RepoScan) -> Suggestions:
    tech: List[str] = []
    run: List[str] = []
    notes: List[str] = []

    # Tech stack hints
    for lang, cnt in scan.languages.items():
        tech.append(f"{lang} ({cnt} files)")

    if scan.has_cmake:
        tech.append("CMake")
        run += [
            "```bash",
            "cmake -S . -B build",
            "cmake --build build -j",
            "./build/<your_binary>",
            "```",
        ]
    if scan.has_makefile:
        tech.append("Make")
        run += [
            "```bash",
            "make",
            "```",
        ]
    if scan.has_package_json:
        tech.append("Node.js / npm")
        run += [
            "```bash",
            "npm install",
            "npm run dev  # or npm start / npm test",
            "```",
        ]
    if scan.has_pyproject or scan.has_requirements:
        tech.append("Python")
        if scan.has_pyproject:
            run += [
                "```bash",
                "python -m venv .venv",
                "source .venv/bin/activate  # Windows: .venv\\Scripts\\activate",
                "pip install -e .",
                "```",
            ]
        else:
            run += [
                "```bash",
                "python -m venv .venv",
                "source .venv/bin/activate  # Windows: .venv\\Scripts\\activate",
                "pip install -r requirements.txt",
                "```",
            ]

    if not run:
        run = [
            "- Add a `How to Run` section describing build/install commands.",
            "- If this is a library, include a minimal usage example.",
        ]

    if scan.file_count >= 5000:
        notes.append("Large repo detected: consider raising `--max-files` or `--depth` for deeper scanning.")

    return Suggestions(tech_stack=tech, how_to_run=run, notes=notes)
