#!/usr/bin/env python3
"""
JSON Toolkit Utility
Validates, formats, sorts, flattens, and diffs JSON data structures.
"""

import sys
import json
import argparse
from pathlib import Path

def flatten_json(data: dict, prefix: str = "", separator: str = ".") -> dict:
    """Flatten nested dictionary into dot-separated keys."""
    items = {}
    for k, v in data.items():
        key = f"{prefix}{separator}{k}" if prefix else str(k)
        if isinstance(v, dict):
            items.update(flatten_json(v, prefix=key, separator=separator))
        elif isinstance(v, list):
            for i, elem in enumerate(v):
                list_key = f"{key}[{i}]"
                if isinstance(elem, dict):
                    items.update(flatten_json(elem, prefix=list_key, separator=separator))
                else:
                    items[list_key] = elem
        else:
            items[key] = v
    return items

def unflatten_json(data: dict, separator: str = ".") -> dict:
    """Reconstruct nested dictionary from flattened dot-separated keys."""
    result = {}
    for key, value in data.items():
        parts = key.split(separator)
        current = result
        for part in parts[:-1]:
            if part not in current or not isinstance(current[part], dict):
                current[part] = {}
            current = current[part]
        current[parts[-1]] = value
    return result

def diff_json(obj1: dict, obj2: dict) -> dict:
    """Compare two JSON objects and list added, removed, and modified keys."""
    flat1 = flatten_json(obj1)
    flat2 = flatten_json(obj2)

    keys1 = set(flat1.keys())
    keys2 = set(flat2.keys())

    added = {k: flat2[k] for k in keys2 - keys1}
    removed = {k: flat1[k] for k in keys1 - keys2}
    changed = {
        k: {"from": flat1[k], "to": flat2[k]}
        for k in keys1 & keys2
        if flat1[k] != flat2[k]
    }

    return {
        "identical": not (added or removed or changed),
        "added": added,
        "removed": removed,
        "changed": changed
    }

def main():
    parser = argparse.ArgumentParser(description="DevForge JSON Toolkit")
    subparsers = parser.add_subparsers(dest="command", help="Command")

    # Format
    fmt_p = subparsers.add_parser("format", help="Format and prettify JSON")
    fmt_p.add_argument("file", help="Path to JSON file")
    fmt_p.add_argument("--sort-keys", action="store_true", help="Sort keys alphabetically")
    fmt_p.add_argument("--indent", type=int, default=2, help="Indentation spaces (default: 2)")

    # Flatten
    flat_p = subparsers.add_parser("flatten", help="Flatten nested JSON to key.subkey paths")
    flat_p.add_argument("file", help="Path to JSON file")

    # Diff
    diff_p = subparsers.add_parser("diff", help="Diff two JSON files")
    diff_p.add_argument("file1", help="First JSON file")
    diff_p.add_argument("file2", help="Second JSON file")

    args = parser.parse_args()

    if args.command == "format":
        with open(args.file, "r", encoding="utf-8") as f:
            data = json.load(f)
        print(json.dumps(data, indent=args.indent, sort_keys=args.sort_keys))

    elif args.command == "flatten":
        with open(args.file, "r", encoding="utf-8") as f:
            data = json.load(f)
        flat = flatten_json(data)
        print(json.dumps(flat, indent=2))

    elif args.command == "diff":
        with open(args.file1, "r", encoding="utf-8") as f1, open(args.file2, "r", encoding="utf-8") as f2:
            d1 = json.load(f1)
            d2 = json.load(f2)
        diff = diff_json(d1, d2)
        print(json.dumps(diff, indent=2))

    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
