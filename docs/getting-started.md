# Getting Started with DevForge

Welcome to **DevForge** — an open-source collection of developer utilities engineered to streamline everyday coding workflows.

## Prerequisites

- **Python**: 3.10 or higher
- **Node.js**: 18.0 or higher
- **C++ Compiler**: GCC 7+, Clang 10+, or MSVC 2019+

## Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/rudecat01/devforge.git
   cd devforge
   ```

2. **Install Python test dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify the entire environment**:
   Run the repository validation suite to confirm all tools, compilers, and test suites are functioning:
   ```bash
   python scripts/validate.py
   ```

## Directory Overview

```text
devforge/
├── tools/             # Production utility code
│   ├── git/           # Git automation helpers
│   ├── python/        # File & system tools
│   ├── javascript/    # Web & runtime validators
│   ├── cpp/           # Performance & algorithmic utilities
│   └── productivity/  # Scaffolding & metrics
├── tests/             # Multi-language test suites
├── docs/              # Comprehensive guides
├── scripts/           # Validation & maintenance automation
└── .github/           # Actions CI and issue templates
```

## Quick Tool Usage Examples

### 1. Conventional Commit Formatter
```bash
python tools/git/commit_formatter.py format -t feat -s auth -d "integrate oauth2 provider"
```

### 2. File Organizer
```bash
python tools/python/file_organizer.py ~/Downloads --dry-run
```

### 3. Environment Validator
```bash
node tools/javascript/env_validator.js --env .env --example .env.example
```

### 4. Code Statistics Analyzer
```bash
python tools/productivity/code_stats.py .
```
