```md
# pls-readme

Generate a clean, structured README.md draft for any local repository — in seconds.

pls-readme scans your project structure, infers the tech stack, and produces a well-organized README draft so you can focus on building, not documenting.

--------------------------------------------------

FEATURES

- Scans repository structure (src/, include/, tests/, etc.)
- Infers tech stack from file types and build configs
- Generates a readable, standard README draft
- Optional directory tree rendering
- Safe by default (preview first, overwrite only with confirmation)
- Fast, local, no external dependencies

--------------------------------------------------

QUICK START

INSTALLATION

git clone https://github.com/your-username/pls-readme.git
cd pls-readme
pip install -e .

GENERATE A README DRAFT

pls-readme /path/to/your/project

This will generate:

README.generated.md

OVERWRITE EXISTING README.md (WITH CONFIRMATION)

pls-readme /path/to/your/project --write

--------------------------------------------------

USAGE

pls-readme [REPO_PATH] [OPTIONS]

OPTIONS

-o, --output PATH
    Output file path (default: README.generated.md)

--write
    Overwrite README.md in target repo

--include-hidden
    Include hidden files and folders

--max-files N
    Max number of files to scan (default: 5000)

--depth N
    Max folder depth to scan (default: 6)

--no-tree
    Disable directory tree rendering

--------------------------------------------------

GENERATED README STRUCTURE

The generated README follows this structure:

# Project Name
## Overview
## Repo Stats
## Tech Stack
## Language Breakdown
## Project Structure
## How to Run
## Notes
## Future Improvements

--------------------------------------------------

EXAMPLE OUTPUT

Repo Stats
- Files scanned: 1,248
- Directories scanned: 96
- Key folders: src, tests, docs

Tech Stack
- Python (214 files)
- JavaScript (98 files)
- CMake

--------------------------------------------------

HOW IT WORKS

1. Recursively scans the repository (respecting depth & file limits)
2. Detects programming languages via file extensions
3. Identifies common build systems (CMake, npm, pip)
4. Applies heuristics to suggest "How to Run"
5. Renders everything into a Markdown README draft

--------------------------------------------------

ROADMAP

- Support .gitignore rules
- Smarter entrypoint detection (main.py, app.js, CMake targets)
- GitHub URL scanning (remote repos)
- README badges (CI, coverage, license)
- Optional AI-assisted project summary

--------------------------------------------------

CONTRIBUTING

1. Fork the repository
2. Create a feature branch
3. Add tests if applicable
4. Submit a pull request with a clear description

--------------------------------------------------

LICENSE

MIT License

--------------------------------------------------

ACKNOWLEDGEMENTS

Built with love to make documentation less painful for developers.
```
