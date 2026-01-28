# pls-readme

**pls-readme** is a lightweight CLI tool that scans a repository and generates a clean,  
structured `README.md` draft — so developers can focus on code, not boilerplate documentation.


---

## ✨ Features

* **📂 Structure Scanning** – Automatically parses folders like `src/`, `include/`, and `tests/`.
* **🧠 Tech Stack Inference** – Detects languages and tools from file extensions and build configs.
* **🧾 Standardized Output** – Generates a readable, industry-standard README template.
* **🌳 Tree Rendering** – Optional visual directory tree for better project visualization.
* **🔒 Safe by Default** – Previews changes first; overwrites only with explicit confirmation.
* **⚡ Zero Dependencies** – Fast, local execution with no external API calls required.

---

## 🚀 Quick Start

### Installation

```bash
git clone https://github.com/wzk111/pls-readme.git
cd pls-readme
pip install -e .
```

### Generate a Draft

To scan a project and generate `README.generated.md`:

```bash
pls-readme /path/to/your/project
```

### Generate With Real GitHub Badges

To generate `README.generated.md` with your real github badges (requires manual confirmation):

```bash
pls-readme /path/to/your/project --github username/repo

```

### Overwrite Existing README

To update your existing `README.md` (requires manual confirmation):

```bash
pls-readme /path/to/your/project --write

```

---

## 🛠 Usage

```bash
pls-readme [REPO_PATH] [OPTIONS]

```

### Options

| Option | Description | Default |
| --- | --- | --- |
| `--github OWNER/REPO` | Generate GitHub badges using the given repository | `Disabled` |
| `-o, --output PATH` | Set a custom output file path | `README.generated.md` |
| `--write` | Overwrite the existing `README.md` in target repo | `False` |
| `--include-hidden` | Include hidden files and folders in the scan | `False` |
| `--max-files N` | Max number of files to scan | `5000` |
| `--depth N` | Max folder depth to scan | `6` |
| `--no-tree` | Disable directory tree rendering | `Enabled` |
| `--no-gitignore` | Do not respect `.gitignore` rules during scanning | `False` |

---

## 🏗 Generated Structure

The tool produces a structured document containing:

1. **Project Name** & **Overview**
2. **Repo Stats** (Scan metrics)
3. **Tech Stack** (Inferred tools)
4. **Language Breakdown** (%)
5. **Project Structure** (Visual tree)
6. **How to Run** (Inferred from build files)
7. **Notes** & **Future Improvements**

---

## ⚙️ How It Works

1. **Recursive Scan:** Navigates the repository while respecting your `depth` and `file limit` settings.
2. **Language Detection:** Maps file extensions to their respective programming languages.
3. **Build System ID:** Identifies markers like `CMakeLists.txt`, `package.json`, or `requirements.txt`.
4. **Heuristic Analysis:** Suggests "How to Run" instructions based on detected entry points.
5. **Markdown Rendering:** Compiles all data into a clean, formatted `.md` file.

---

## 🗺 Roadmap

* [ ] **.gitignore Support:** Automatically skip files ignored by git.
* [ ] **Smart Entrypoints:** Better detection for `main.py`, `app.js`, and CMake targets.
* [ ] **Remote Scanning:** Support for scanning GitHub URLs directly.
* [ ] **Dynamic Badges:** Add CI status, coverage, and license badges automatically.
* [ ] **AI Summary:** Optional integration for LLM-generated project descriptions.

---

## 🤝 Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create.

1. **Fork** the Project
2. Create your **Feature Branch** (`git checkout -b feature/AmazingFeature`)
3. **Commit** your Changes (`git commit -m 'Add some AmazingFeature'`)
4. **Push** to the Branch (`git push origin feature/AmazingFeature`)
5. Open a **Pull Request**

---

## 📄 License

Distributed under the **MIT License**. See `LICENSE` for more information.

---

## ❤️ Acknowledgements

Built with love to make documentation less painful for developers.

---
