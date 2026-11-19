#!/usr/bin/env python3
"""
File Organizer Utility
Sorts files in a directory into categorized subdirectories based on their file extensions.
"""

import os
import shutil
import argparse
from pathlib import Path

CATEGORY_MAPPINGS = {
    "images": {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".svg", ".webp", ".ico"},
    "documents": {".pdf", ".docx", ".doc", ".txt", ".rtf", ".odt", ".pptx", ".xlsx", ".csv", ".md"},
    "audio": {".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a"},
    "video": {".mp4", ".mkv", ".avi", ".mov", ".wmv", ".webm"},
    "archives": {".zip", ".tar", ".gz", ".7z", ".rar", ".bz2", ".xz"},
    "code": {".py", ".js", ".ts", ".jsx", ".tsx", ".cpp", ".c", ".h", ".hpp", ".java", ".go", ".rs", ".html", ".css"},
    "data": {".json", ".yaml", ".yml", ".xml", ".sql", ".sqlite", ".db"}
}

def determine_category(extension: str) -> str:
    ext = extension.lower()
    for cat, extensions in CATEGORY_MAPPINGS.items():
        if ext in extensions:
            return cat
    return "other"

def organize_directory(
    target_dir: str,
    dry_run: bool = True,
    recursive: bool = False
) -> list[dict]:
    """Scan and organize directory items into category folders."""
    path = Path(target_dir).resolve()
    if not path.is_dir():
        raise ValueError(f"Target path does not exist or is not a directory: {target_dir}")

    actions = []
    
    # We ignore our target category subdirectories to prevent nested moving
    category_dirs = set(CATEGORY_MAPPINGS.keys()) | {"other"}

    items = path.rglob("*") if recursive else path.iterdir()
    for item in items:
        if not item.is_file():
            continue

        # If it's already inside a category directory directly under target_dir, skip
        try:
            rel = item.relative_to(path)
            if len(rel.parts) > 1 and rel.parts[0] in category_dirs:
                continue
        except ValueError:
            pass

        cat = determine_category(item.suffix)
        dest_dir = path / cat
        dest_file = dest_dir / item.name

        actions.append({
            "source": str(item),
            "destination": str(dest_file),
            "category": cat,
            "filename": item.name
        })

        if not dry_run:
            dest_dir.mkdir(parents=True, exist_ok=True)
            # Avoid overwriting existing files
            target_dest = dest_file
            counter = 1
            while target_dest.exists() and target_dest != item:
                target_dest = dest_dir / f"{item.stem}_{counter}{item.suffix}"
                counter += 1
            shutil.move(str(item), str(target_dest))

    return actions

def main():
    parser = argparse.ArgumentParser(description="DevForge File Organizer")
    parser.add_argument("path", nargs="?", default=".", help="Directory to organize (default: current directory)")
    parser.add_argument("--dry-run", action="store_true", default=True, help="Preview file moves without applying (default: True)")
    parser.add_argument("--execute", dest="dry_run", action="store_false", help="Apply file movements")
    parser.add_argument("-r", "--recursive", action="store_true", help="Organize subdirectories recursively")

    args = parser.parse_args()

    try:
        moves = organize_directory(args.path, dry_run=args.dry_run, recursive=args.recursive)
        mode_label = "[DRY-RUN] " if args.dry_run else ""
        print(f"{mode_label}Identified {len(moves)} file(s) to organize:")
        for m in moves:
            print(f"  {m['filename']} -> {m['category']}/")
        if args.dry_run and moves:
            print("\nRun with --execute to commit the file moves.")
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

if __name__ == "__main__":
    main()
