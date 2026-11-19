#!/usr/bin/env python3
"""
Branch Cleaner Utility
Identifies merged, stale, or deleted remote tracking git branches and prunes them safely.
"""

import sys
import subprocess
import argparse

def run_git_command(args: list[str]) -> tuple[int, str]:
    """Execute a git command and return returncode and output."""
    try:
        proc = subprocess.run(
            ["git"] + args,
            capture_output=True,
            text=True,
            check=False
        )
        return proc.returncode, proc.stdout.strip()
    except FileNotFoundError:
        return 1, "Git executable not found in PATH."

def get_current_branch() -> str:
    code, out = run_git_command(["rev-parse", "--abbrev-ref", "HEAD"])
    return out if code == 0 else ""

def get_merged_branches(base_branch: str = "main") -> list[str]:
    """Return local branches merged into the target base branch."""
    code, out = run_git_command(["branch", "--merged", base_branch])
    if code != 0:
        # Try master fallback
        if base_branch == "main":
            return get_merged_branches("master")
        return []

    branches = []
    for line in out.splitlines():
        b = line.strip().lstrip("* ").strip()
        if b and b not in [base_branch, "main", "master", "develop"]:
            branches.append(b)
    return branches

def clean_branches(branches: list[str], dry_run: bool = True, force: bool = False) -> list[str]:
    """Prune specified local branches."""
    deleted = []
    flag = "-D" if force else "-d"
    for b in branches:
        if dry_run:
            deleted.append(f"[DRY-RUN] Would delete branch: {b}")
        else:
            code, msg = run_git_command(["branch", flag, b])
            if code == 0:
                deleted.append(f"Deleted branch: {b}")
            else:
                deleted.append(f"Failed to delete {b}: {msg}")
    return deleted

def main():
    parser = argparse.ArgumentParser(description="DevForge Branch Cleaner")
    parser.add_argument("-b", "--base", default="main", help="Base branch to check merges against (default: main)")
    parser.add_argument("--dry-run", action="store_true", default=True, help="Preview without deleting (default: True)")
    parser.add_argument("--execute", dest="dry_run", action="store_false", help="Perform actual branch deletion")
    parser.add_argument("-f", "--force", action="store_true", help="Force deletion even if not fully merged")

    args = parser.parse_args()

    curr = get_current_branch()
    if not curr:
        print("Error: Not inside a valid git repository or git command failed.")
        sys.exit(1)

    print(f"Current branch: {curr}")
    print(f"Checking branches merged into: {args.base}")

    merged = get_merged_branches(args.base)
    # Don't delete current branch
    merged = [b for b in merged if b != curr]

    if not merged:
        print("No merged branches found to clean.")
        sys.exit(0)

    print(f"Found {len(merged)} candidate branch(es): {', '.join(merged)}")
    results = clean_branches(merged, dry_run=args.dry_run, force=args.force)
    for res in results:
        print(res)

if __name__ == "__main__":
    main()
