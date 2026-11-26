#!/usr/bin/env python3
"""
Duplicate Finder Utility
Finds duplicate files efficiently across directories using file size grouping and SHA-256 chunk hashing.
"""

import os
import sys
import hashlib
import json
import argparse
from pathlib import Path
from collections import defaultdict

CHUNK_SIZE = 64 * 1024  # 64 KB
BUFFER_SIZE_OPTIONS = {'small': 16*1024, 'default': 64*1024, 'large': 256*1024}

def compute_file_hash(filepath: Path) -> str:
    """Compute SHA-256 hash of a file reading in chunks."""
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(CHUNK_SIZE):
            hasher.update(chunk)
    return hasher.hexdigest()

def find_duplicates(target_dir: str, min_size: int = 1) -> dict[str, list[str]]:
    """Scan directory and return a mapping of file_hash -> list of duplicate paths."""
    root = Path(target_dir).resolve()
    if not root.is_dir():
        raise ValueError(f"Path is not a valid directory: {target_dir}")

    # Pass 1: Group by file size to quickly eliminate unique files
    size_groups = defaultdict(list)
    for p in root.rglob("*"):
        if p.is_file():
            try:
                sz = p.stat().st_size
                if sz >= min_size:
                    size_groups[sz].append(p)
            except (OSError, PermissionError):
                continue

    # Pass 2: Hash files that share the same size
    duplicates = defaultdict(list)
    for sz, file_list in size_groups.items():
        if len(file_list) < 2:
            continue

        hash_groups = defaultdict(list)
        for filepath in file_list:
            try:
                file_hash = compute_file_hash(filepath)
                hash_groups[file_hash].append(str(filepath))
            except (OSError, PermissionError):
                continue

        for f_hash, paths in hash_groups.items():
            if len(paths) > 1:
                duplicates[f_hash].extend(paths)

    return dict(duplicates)

def main():
    parser = argparse.ArgumentParser(description="DevForge Duplicate File Finder")
    parser.add_argument("path", nargs="?", default=".", help="Directory to scan (default: current dir)")
    parser.add_argument("--min-size", type=int, default=1, help="Minimum file size in bytes to check (default: 1)")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")

    args = parser.parse_args()

    try:
        results = find_duplicates(args.path, min_size=args.min_size)
        if args.json:
            print(json.dumps(results, indent=2))
            return

        total_dups = sum(len(paths) - 1 for paths in results.values())
        print(f"Scanned: {args.path}")
        print(f"Found {len(results)} duplicate group(s) with {total_dups} redundant file(s).\n")

        for idx, (f_hash, paths) in enumerate(results.items(), start=1):
            print(f"Group #{idx} [Hash: {f_hash[:12]}...]:")
            for p in paths:
                print(f"  - {p}")
            print()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
