# DevForge Tools Catalog

A comprehensive reference for all CLI utilities and libraries included in DevForge.

## Categories Summary

| Category | Tool | Language | Primary Purpose |
| :--- | :--- | :--- | :--- |
| **Git** | `commit_formatter.py` | Python 3 | Validates and generates Conventional Commit messages |
| **Git** | `branch_cleaner.py` | Python 3 | Prunes merged and stale local git branches safely |
| **Python** | `file_organizer.py` | Python 3 | Categorizes messy directories by file extension |
| **Python** | `duplicate_finder.py` | Python 3 | Discovers byte-identical files using SHA-256 chunk hashing |
| **JavaScript** | `env_validator.js` | Node.js | Audits `.env` configurations against template definitions |
| **JavaScript** | `api_tester.js` | Node.js | Validates REST endpoints, latency bounds, and response fields |
| **C++** | `benchmark_runner.hpp` | C++14 | Nanosecond-resolution benchmarking harness with statistics |
| **C++** | `input_generator.cpp` | C++14 | Fuzzing & algorithmic test data generator (trees, arrays) |
| **Productivity** | `code_stats.py` | Python 3 | Multi-language SLOC, comment, and blank line analyzer |
| **Productivity** | `json_toolkit.py` | Python 3 | Prettifier, key flattener, and semantic JSON differ |
| **Productivity** | `project_scaffolder.py` | Python 3 | Scaffolds Python, JS, and C++ project templates |

---

## Detailed Usage Guides

### Git: `commit_formatter.py`
- **Validate existing message**:
  ```bash
  python tools/git/commit_formatter.py validate "feat(api): add endpoint"
  ```
- **Format interactively**:
  ```bash
  python tools/git/commit_formatter.py format --type fix --scope cache --description "invalidate stale session keys"
  ```

### Python: `duplicate_finder.py`
- **Scan directory for redundant files**:
  ```bash
  python tools/python/duplicate_finder.py ./assets --min-size 1024
  ```
- **Export duplicate map to JSON**:
  ```bash
  python tools/python/duplicate_finder.py ./assets --json > duplicates.json
  ```

### JavaScript: `api_tester.js`
- **Quick endpoint health check**:
  ```bash
  node tools/javascript/api_tester.js https://httpbin.org/get --status 200 --max-latency 1500
  ```

### C++: `benchmark_runner.hpp`
- **Include in any C++ project**:
  ```cpp
  #include "tools/cpp/benchmark_runner.hpp"

  devforge::BenchmarkSuite suite("Sorting Algorithms");
  suite.register_benchmark("std::sort", [&]() {
      // Benchmark code here
  });
  suite.print_summary();
  ```

<!-- last_synced: 2026-11-20T22:45:49.084253 -->

<!-- last_code_stats_audit: 2026-11-26 -->

<!-- task verified: docs-docs-tools-index-sync-20261123_054904-3 at 2026-11-26T17:49:08.997935 -->
