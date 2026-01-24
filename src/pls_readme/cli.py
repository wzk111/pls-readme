from __future__ import annotations
import argparse
from pathlib import Path
import sys

from .scanner import scan_repo
from .heuristics import infer_suggestions
from .renderer_md import render_markdown

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="pls-readme",
        description="Generate a clean README.md draft for a local repository.",
    )
    p.add_argument("repo", nargs="?", default=".", help="Path to the repository (default: .)")
    p.add_argument("-o", "--output", default="README.generated.md", help="Output file path (default: README.generated.md)")
    p.add_argument("--write", action="store_true", help="Write to REPO/README.md (overwrite with confirmation).")
    p.add_argument("--include-hidden", action="store_true", help="Include hidden files/folders.")
    p.add_argument("--max-files", type=int, default=5000, help="Max files to scan (default: 5000).")
    p.add_argument("--depth", type=int, default=6, help="Max folder depth to scan (default: 6).")
    p.add_argument("--no-tree", action="store_true", help="Disable directory tree rendering.")
    p.add_argument("--no-gitignore", action="store_true", help="Do not respect .gitignore rules (scan everything except built-in ignores).")
    p.add_argument("--github", metavar="OWNER/REPO", help="GitHub repository in the form OWNER/REPO (used to generate badges).")
    return p

def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    repo_path = Path(args.repo).resolve()
    scan = scan_repo(repo_path, include_hidden=args.include_hidden, max_files=args.max_files, depth=args.depth, respect_gitignore=(not args.no_gitignore))
    sug = infer_suggestions(scan)
    md = render_markdown(scan, sug, depth=args.depth, include_hidden=args.include_hidden, show_tree=(not args.no_tree), github_repo=args.github)


    if args.write:
        out_path = repo_path / "README.md"
        if out_path.exists():
            resp = input(f"[pls-readme] Overwrite {out_path}? (y/N): ").strip().lower()
            if resp != "y":
                print("[pls-readme] Cancelled.")
                return 1
        out_path.write_text(md, encoding="utf-8")
        print(f"[pls-readme] Wrote: {out_path}")
        return 0

    out_path = Path(args.output).resolve()
    out_path.write_text(md, encoding="utf-8")
    print(f"[pls-readme] Wrote: {out_path}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
