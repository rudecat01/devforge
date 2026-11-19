#!/usr/bin/env python3
"""
DevForge Repository Validation Script
Runs sanity checks, directory structure validation, and automated test suites for all languages.
"""

import sys
import os
import subprocess
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

def log_section(title: str):
    print(f"\n{'=' * 60}\n  {title}\n{'=' * 60}")

def check_directory_structure() -> bool:
    log_section("1. Verifying Repository Directory Structure")
    required_paths = [
        ROOT_DIR / "README.md",
        ROOT_DIR / "CONTRIBUTING.md",
        ROOT_DIR / "LICENSE",
        ROOT_DIR / "CHANGELOG.md",
        ROOT_DIR / "tools",
        ROOT_DIR / "tests",
        ROOT_DIR / "docs",
        ROOT_DIR / "scripts",
        ROOT_DIR / ".github" / "workflows" / "ci.yml",
        ROOT_DIR / ".github" / "workflows" / "daily-maintenance.yml"
    ]

    all_exist = True
    for p in required_paths:
        if p.exists():
            print(f"  [OK] Found: {p.relative_to(ROOT_DIR)}")
        else:
            print(f"  [FAIL] Missing required file or directory: {p.relative_to(ROOT_DIR)}")
            all_exist = False

    return all_exist

def run_python_tests() -> bool:
    log_section("2. Running Python Test Suite (pytest)")
    test_dir = ROOT_DIR / "tests" / "python"
    if not test_dir.exists():
        print("  [SKIP] No python tests directory found.")
        return True

    cmd = [sys.executable, "-m", "pytest", str(test_dir), "-v"]
    res = subprocess.run(cmd, cwd=str(ROOT_DIR))
    return res.returncode == 0

def run_javascript_tests() -> bool:
    log_section("3. Running JavaScript Test Suite (node:test)")
    test_file = ROOT_DIR / "tests" / "javascript" / "test_javascript_tools.test.js"
    if not test_file.exists():
        print("  [SKIP] No JavaScript test file found.")
        return True

    cmd = ["node", "--test", str(test_file)]
    res = subprocess.run(cmd, cwd=str(ROOT_DIR), shell=(os.name == "nt"))
    return res.returncode == 0

def run_cpp_tests() -> bool:
    log_section("4. Compiling & Running C++ Test Suite")
    test_file = ROOT_DIR / "tests" / "cpp" / "test_cpp_tools.cpp"
    out_exe = ROOT_DIR / "tests" / "cpp" / ("test_cpp_runner.exe" if os.name == "nt" else "test_cpp_runner")

    if not test_file.exists():
        print("  [SKIP] No C++ test file found.")
        return True

    compile_cmd = ["g++", "-std=c++14", "-O2", str(test_file), "-o", str(out_exe)]
    comp_res = subprocess.run(compile_cmd, cwd=str(ROOT_DIR), shell=(os.name == "nt"))
    if comp_res.returncode != 0:
        print("  [FAIL] C++ compilation failed.")
        return False

    run_res = subprocess.run([str(out_exe)], cwd=str(ROOT_DIR))
    # Cleanup compiled binary
    if out_exe.exists():
        try:
            out_exe.unlink()
        except OSError:
            pass

    return run_res.returncode == 0

def main():
    print("DevForge CI / Local Repository Validator Starting...")
    results = [
        ("Directory Structure", check_directory_structure()),
        ("Python Tests", run_python_tests()),
        ("JavaScript Tests", run_javascript_tests()),
        ("C++ Tests", run_cpp_tests())
    ]

    log_section("Validation Summary")
    all_passed = True
    for name, passed in results:
        status = "PASSED" if passed else "FAILED"
        print(f"  - {name:<25}: {status}")
        if not passed:
            all_passed = False

    if all_passed:
        print("\n✅ All validation suites passed successfully!\n")
        sys.exit(0)
    else:
        print("\n❌ Validation checks failed. Please inspect errors above.\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
