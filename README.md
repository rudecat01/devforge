# DevForge

> Practical developer utilities engineered for cleaner workflows, automated maintenance, and reproducible testing.

[![CI](https://github.com/rudecat01/devforge/actions/workflows/ci.yml/badge.svg)](https://github.com/rudecat01/devforge/actions/workflows/ci.yml)
[![Daily Maintenance](https://github.com/rudecat01/devforge/actions/workflows/daily-maintenance.yml/badge.svg)](https://github.com/rudecat01/devforge/actions/workflows/daily-maintenance.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.12%20%7C%203.13-blue.svg)](https://python.org)
[![Node](https://img.shields.io/badge/Node.js-18%20%7C%2020%20%7C%2022-green.svg)](https://nodejs.org)
[![C++](https://img.shields.io/badge/C%2B%2B-14%20%7C%2017-orange.svg)](https://isocpp.org)

DevForge is an open-source toolkit organized into modular, language-independent utilities designed to grow systematically. Each tool is built with standalone CLI support, isolated unit tests, and minimal external dependencies.

---

## 🛠️ Tool Catalog

| Category | Tool | Language | Summary |
| :--- | :--- | :--- | :--- |
| **Git** | `commit_formatter.py` | Python 3 | Validates and formats Conventional Commit messages |
| **Git** | `branch_cleaner.py` | Python 3 | Detects and cleans stale/merged local git branches |
| **Python** | `file_organizer.py` | Python 3 | Organizes files into categorized folders with dry-run mode |
| **Python** | `duplicate_finder.py` | Python 3 | High-speed duplicate file detector using chunked SHA-256 |
| **JavaScript** | `env_validator.js` | Node.js | Validates `.env` files against schemas and templates |
| **JavaScript** | `api_tester.js` | Node.js | Micro-benchmarking HTTP endpoint tester with assertions |
| **C++** | `benchmark_runner.hpp` | C++14 | Nanosecond-resolution benchmarking harness |
| **C++** | `input_generator.cpp` | C++14 | Test case and input data generator for algorithms & fuzzing |
| **Productivity** | `code_stats.py` | Python 3 | Multi-language SLOC, comment, and blank line analyzer |
| **Productivity** | `json_toolkit.py` | Python 3 | Formats, flattens, unflattens, and diffs JSON data |
| **Productivity** | `project_scaffolder.py` | Python 3 | Scaffolds Python, Node, and C++ starter boilerplates |

---

## 🚀 Quick Start

### 1. Requirements
- Python 3.10+
- Node.js 18+
- GCC / G++ 7+ (or Clang)

### 2. Installation
```bash
git clone https://github.com/rudecat01/devforge.git
cd devforge
pip install -r requirements.txt
```

### 3. Run Repository Verification
Run the comprehensive test suite across all languages with a single command:
```bash
python scripts/validate.py
```

---

## 📖 Usage Examples

### Validate a Conventional Commit
```bash
python tools/git/commit_formatter.py validate "feat(auth): support token refresh"
```

### Organize a Directory
```bash
python tools/python/file_organizer.py ~/Downloads --dry-run
```

### Audit Environment Variables
```bash
node tools/javascript/env_validator.js --env .env --example .env.example
```

### Run Code Statistics
```bash
python tools/productivity/code_stats.py .
```

---

## 🤖 Daily Automated Maintenance

DevForge includes an automated background maintenance engine configured via GitHub Actions (`.github/workflows/daily-maintenance.yml`).

- **Schedule**: Every day at **10:00 PM IST (16:30 UTC)**.
- **Workflow**: Pulls verified maintenance tasks from `scripts/backlog.json`, executes code and documentation improvements, runs `scripts/validate.py`, and commits changes with author attribution.
- **Continuous Backlog**: Tasks auto-replenish to maintain regular, credible engineering contributions.

See [docs/automation-guide.md](docs/automation-guide.md) for full architecture details.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
