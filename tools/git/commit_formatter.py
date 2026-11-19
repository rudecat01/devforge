#!/usr/bin/env python3
"""
Commit Formatter Utility
Validates and formats git commit messages according to Conventional Commits specification.
"""

import sys
import re
import argparse

CONVENTIONAL_TYPES = [
    "feat", "fix", "docs", "style", "refactor",
    "perf", "test", "build", "ci", "chore", "revert"
]

COMMIT_PATTERN = re.compile(
    r"^(?P<type>[a-z]+)(\((?P<scope>[a-zA-Z0-9_\-\./]+)\))?(?P<breaking>!)?:\s+(?P<description>.+)$"
)

def validate_commit_message(message: str) -> tuple[bool, str]:
    """Validates if a commit message complies with Conventional Commits standard."""
    lines = message.strip().splitlines()
    if not lines or not lines[0].strip():
        return False, "Commit message cannot be empty."

    header = lines[0].strip()
    if len(header) > 72:
        return False, f"Header line is too long ({len(header)} chars, max recommended is 72)."

    match = COMMIT_PATTERN.match(header)
    if not match:
        return False, (
            "Header does not match format: <type>(<scope>): <description>\n"
            f"Allowed types: {', '.join(CONVENTIONAL_TYPES)}"
        )

    commit_type = match.group("type")
    if commit_type not in CONVENTIONAL_TYPES:
        return False, f"Unknown commit type '{commit_type}'. Allowed types: {', '.join(CONVENTIONAL_TYPES)}"

    desc = match.group("description")
    if desc.endswith("."):
        return False, "Description should not end with a period."

    if desc[0].isupper():
        return False, "Description should start with a lowercase letter."

    return True, "Valid conventional commit message."

def format_commit_message(
    commit_type: str,
    description: str,
    scope: str = "",
    breaking: bool = False,
    body: str = "",
    footer: str = ""
) -> str:
    """Constructs a standardized commit message from components."""
    type_clean = commit_type.strip().lower()
    desc_clean = description.strip()
    if desc_clean and desc_clean[0].isupper():
        desc_clean = desc_clean[0].lower() + desc_clean[1:]
    if desc_clean.endswith("."):
        desc_clean = desc_clean[:-1]

    header_parts = [type_clean]
    if scope.strip():
        header_parts.append(f"({scope.strip().lower()})")
    if breaking:
        header_parts.append("!")
    header_parts.append(f": {desc_clean}")

    header = "".join(header_parts)
    parts = [header]

    if body.strip():
        parts.append("")
        parts.append(body.strip())

    if breaking and "BREAKING CHANGE:" not in (body or "") and "BREAKING CHANGE:" not in (footer or ""):
        parts.append("")
        parts.append("BREAKING CHANGE: " + (footer.strip() if footer.strip() else desc_clean))
    elif footer.strip():
        parts.append("")
        parts.append(footer.strip())

    return "\n".join(parts)

def main():
    parser = argparse.ArgumentParser(description="DevForge Commit Formatter & Validator")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Validate subcommand
    val_parser = subparsers.add_parser("validate", help="Validate a commit message")
    val_parser.add_argument("message", nargs="?", help="Commit message string or read from stdin")

    # Format subcommand
    fmt_parser = subparsers.add_parser("format", help="Format a commit message")
    fmt_parser.add_argument("-t", "--type", required=True, choices=CONVENTIONAL_TYPES, help="Commit type")
    fmt_parser.add_argument("-d", "--description", required=True, help="Short imperative description")
    fmt_parser.add_argument("-s", "--scope", default="", help="Optional scope component")
    fmt_parser.add_argument("-b", "--body", default="", help="Optional detailed commit body")
    fmt_parser.add_argument("-f", "--footer", default="", help="Optional footer (e.g. Closes #123)")
    fmt_parser.add_argument("--breaking", action="store_true", help="Flag breaking change")

    args = parser.parse_args()

    if args.command == "validate":
        msg = args.message
        if not msg:
            if not sys.stdin.isatty():
                msg = sys.stdin.read()
            else:
                parser.error("Please provide a message or pipe input via stdin.")
        is_valid, reason = validate_commit_message(msg)
        print(reason)
        sys.exit(0 if is_valid else 1)

    elif args.command == "format":
        res = format_commit_message(
            commit_type=args.type,
            description=args.description,
            scope=args.scope,
            breaking=args.breaking,
            body=args.body,
            footer=args.footer
        )
        print(res)

    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
