#!/usr/bin/env python3
"""
Code Statistics Utility
Analyzes directories to report lines of code (SLOC), comments, blank lines, and file counts by language.
"""

import sys
import json
import argparse
from pathlib import Path
from collections import defaultdict

LANGUAGE_EXTENSIONS = {
    "Python": {".py"},
    "JavaScript": {".js", ".mjs", ".cjs", ".jsx"},
    "TypeScript": {".ts", ".tsx"},
    "C++": {".cpp", ".cxx", ".cc", ".hpp", ".h"},
    "C": {".c"},
    "HTML": {".html", ".htm"},
    "CSS": {".css", ".scss", ".less"},
    "Markdown": {".md"},
    "JSON/YAML": {".json", ".yaml", ".yml"},
    "Shell": {".sh", ".bash", ".zsh"}
}

COMMENT_PREFIXES = {
    "Python": ("#",),
    "JavaScript": ("//", "/*", "*"),
    "TypeScript": ("//", "/*", "*"),
    "C++": ("//", "/*", "*"),
    "C": ("//", "/*", "*"),
    "HTML": ("<!--",),
    "CSS": ("/*", "*"),
    "Markdown": tuple(),
    "JSON/YAML": ("#",),
    "Shell": ("#",)
}

def detect_language(ext: str) -> str:
    ext = ext.lower()
    for lang, exts in LANGUAGE_EXTENSIONS.items():
        if ext in exts:
            return lang
    return "Other"

def analyze_file(filepath: Path, lang: str) -> dict:
    total = 0
    blank = 0
    comment = 0
    code = 0

    prefixes = COMMENT_PREFIXES.get(lang, ())

    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                total += 1
                stripped = line.strip()
                if not stripped:
                    blank += 1
                elif any(stripped.startswith(p) for p in prefixes):
                    comment += 1
                else:
                    code += 1
    except (OSError, PermissionError):
        pass

    return {
        "total": total,
        "blank": blank,
        "comment": comment,
        "code": code,
        "bytes": filepath.stat().st_size if filepath.exists() else 0
    }

def analyze_directory(target_dir: str, exclude_dirs: set[str] = None) -> dict:
    root = Path(target_dir).resolve()
    if not root.is_dir():
        raise ValueError(f"Path is not a valid directory: {target_dir}")

    if exclude_dirs is None:
        exclude_dirs = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build", ".pytest_cache"}

    stats = defaultdict(lambda: {"files": 0, "total": 0, "code": 0, "comment": 0, "blank": 0, "bytes": 0})

    for item in root.rglob("*"):
        if not item.is_file():
            continue
        if any(part in exclude_dirs for part in item.parts):
            continue

        lang = detect_language(item.suffix)
        file_metrics = analyze_file(item, lang)

        s = stats[lang]
        s["files"] += 1
        s["total"] += file_metrics["total"]
        s["code"] += file_metrics["code"]
        s["comment"] += file_metrics["comment"]
        s["blank"] += file_metrics["blank"]
        s["bytes"] += file_metrics["bytes"]

    return dict(stats)

def main():
    parser = argparse.ArgumentParser(description="DevForge Code Statistics Analyzer")
    parser.add_argument("path", nargs="?", default=".", help="Directory to analyze (default: current directory)")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")

    args = parser.parse_args()

    try:
        metrics = analyze_directory(args.path)

        if args.json:
            print(json.dumps(metrics, indent=2))
            return

        print(f"\nDevForge Code Metrics: {args.path}")
        print("=" * 76)
        print(f"{'Language':<16} {'Files':>8} {'Total':>10} {'Code':>10} {'Comment':>10} {'Blank':>10} {'Bytes':>8}")
        print("-" * 76)

        total_files = total_lines = total_code = total_comment = total_blank = total_bytes = 0

        for lang, data in sorted(metrics.items(), key=lambda x: x[1]["code"], reverse=True):
            print(f"{lang:<16} {data['files']:>8} {data['total']:>10} {data['code']:>10} {data['comment']:>10} {data['blank']:>10} {data['bytes']:>8}")
            total_files += data["files"]
            total_lines += data["total"]
            total_code += data["code"]
            total_comment += data["comment"]
            total_blank += data["blank"]
            total_bytes += data["bytes"]

        print("=" * 76)
        print(f"{'TOTAL':<16} {total_files:>8} {total_lines:>10} {total_code:>10} {total_comment:>10} {total_blank:>10} {total_bytes:>8}\n")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
