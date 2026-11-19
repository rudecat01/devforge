#!/usr/bin/env python3
"""
Changelog Generator Script
Parses git commit logs using Conventional Commits and updates CHANGELOG.md.
"""

import sys
import re
import subprocess
from datetime import datetime
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

TYPE_MAPPING = {
    "feat": "Features",
    "fix": "Bug Fixes",
    "perf": "Performance Improvements",
    "docs": "Documentation",
    "refactor": "Refactoring",
    "test": "Tests",
    "ci": "CI / CD",
    "chore": "Maintenance & Chores"
}

def get_git_commits(since_tag: str = "") -> list[str]:
    range_arg = f"{since_tag}..HEAD" if since_tag else "HEAD"
    cmd = ["git", "log", range_arg, "--pretty=format:%H|||%s|||%an|||%ad", "--date=short"]
    try:
        res = subprocess.run(cmd, cwd=str(ROOT_DIR), capture_output=True, text=True, check=False)
        if res.returncode == 0 and res.stdout.strip():
            return res.stdout.strip().splitlines()
    except FileNotFoundError:
        pass
    return []

def parse_commit_line(line: str) -> dict | None:
    parts = line.split("|||")
    if len(parts) < 4:
        return None

    commit_hash, subject, author, date = parts
    match = re.match(r"^(?P<type>[a-z]+)(\((?P<scope>[a-zA-Z0-9_\-\./]+)\))?(?P<breaking>!)?:\s+(?P<desc>.+)$", subject)
    if not match:
        return {
            "hash": commit_hash[:7],
            "type": "chore",
            "scope": "",
            "breaking": False,
            "description": subject,
            "author": author,
            "date": date
        }

    return {
        "hash": commit_hash[:7],
        "type": match.group("type"),
        "scope": match.group("scope") or "",
        "breaking": bool(match.group("breaking")),
        "description": match.group("desc"),
        "author": author,
        "date": date
    }

def format_changelog_section(version: str, commits: list[dict]) -> str:
    today = datetime.now().strftime("%Y-%m-%d")
    grouped = {cat: [] for cat in TYPE_MAPPING.values()}
    grouped["Breaking Changes"] = []

    for c in commits:
        if c["breaking"]:
            scope_prefix = f"**{c['scope']}**: " if c["scope"] else ""
            grouped["Breaking Changes"].append(f"- {scope_prefix}{c['description']} ({c['hash']})")

        cat_name = TYPE_MAPPING.get(c["type"], "Maintenance & Chores")
        scope_prefix = f"**{c['scope']}**: " if c["scope"] else ""
        grouped[cat_name].append(f"- {scope_prefix}{c['description']} ({c['hash']})")

    lines = [f"## [{version}] - {today}\n"]

    if grouped["Breaking Changes"]:
        lines.append("### ⚠️ Breaking Changes")
        lines.extend(grouped["Breaking Changes"])
        lines.append("")

    for cat_name, items in grouped.items():
        if cat_name != "Breaking Changes" and items:
            lines.append(f"### {cat_name}")
            lines.extend(items)
            lines.append("")

    return "\n".join(lines)

def main():
    version = sys.argv[1] if len(sys.argv) > 1 else "v0.1.0"
    raw_commits = get_git_commits()

    parsed = []
    for r in raw_commits:
        p = parse_commit_line(r)
        if p:
            parsed.append(p)

    if not parsed:
        print("No new commits found.")
        return

    section = format_changelog_section(version, parsed)
    print(section)

if __name__ == "__main__":
    main()
