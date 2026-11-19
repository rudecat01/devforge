#!/usr/bin/env python3
"""
Project Scaffolder Utility
Generates boilerplate structures and starter files for Python, Node.js, and C++ utilities.
"""

import sys
import argparse
from pathlib import Path

TEMPLATES = {
    "python": {
        "files": {
            "main.py": (
                '#!/usr/bin/env python3\n'
                '"""\nEntrypoint for {name}\n"""\n\n'
                'def run():\n'
                '    print("Running {name}...")\n\n'
                'if __name__ == "__main__":\n'
                '    run()\n'
            ),
            "test_main.py": (
                'import pytest\n'
                'from main import run\n\n'
                'def test_smoke():\n'
                '    assert True\n'
            ),
            "README.md": (
                '# {name}\n\n'
                'A lightweight Python utility.\n\n'
                '## Usage\n```bash\npython main.py\n```\n'
            )
        }
    },
    "javascript": {
        "files": {
            "index.js": (
                '#!/usr/bin/env node\n'
                '// Entrypoint for {name}\n\n'
                'function main() {\n'
                '  console.log("Running {name}...");\n'
                '}\n\n'
                'if (require.main === module) {\n'
                '  main();\n'
                '}\n\n'
                'module.exports = { main };\n'
            ),
            "index.test.js": (
                'const test = require("node:test");\n'
                'const assert = require("node:assert");\n'
                'const { main } = require("./index.js");\n\n'
                'test("smoke test", () => {\n'
                '  assert.strictEqual(typeof main, "function");\n'
                '});\n'
            ),
            "package.json": (
                '{\n'
                '  "name": "{name}",\n'
                '  "version": "0.1.0",\n'
                '  "scripts": {\n'
                '    "test": "node --test"\n'
                '  }\n'
                '}\n'
            )
        }
    },
    "cpp": {
        "files": {
            "main.cpp": (
                '#include <iostream>\n\n'
                'int main() {\n'
                '    std::cout << "Running {name}..." << std::endl;\n'
                '    return 0;\n'
                '}\n'
            ),
            "CMakeLists.txt": (
                'cmake_minimum_required(VERSION 3.10)\n'
                'project({name})\n\n'
                'set(CMAKE_CXX_STANDARD 17)\n'
                'add_executable({name} main.cpp)\n'
            )
        }
    }
}

def scaffold_project(name: str, language: str, output_dir: str) -> Path:
    lang = language.lower()
    if lang not in TEMPLATES:
        raise ValueError(f"Unsupported language '{language}'. Options: {', '.join(TEMPLATES.keys())}")

    target = Path(output_dir) / name
    target.mkdir(parents=True, exist_ok=True)

    template = TEMPLATES[lang]
    for rel_path, content in template["files"].items():
        dest = target / rel_path
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(content.replace("{name}", name), encoding="utf-8")

    return target

def main():
    parser = argparse.ArgumentParser(description="DevForge Project Scaffolder")
    parser.add_argument("name", help="Name of the new tool/project")
    parser.add_argument("-l", "--lang", choices=["python", "javascript", "cpp"], default="python", help="Target language")
    parser.add_argument("-o", "--out", default=".", help="Target parent directory (default: .)")

    args = parser.parse_args()

    try:
        dest = scaffold_project(args.name, args.lang, args.out)
        print(f"✅ Successfully scaffolded {args.lang} project at: {dest}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
