# Daily Automation & Maintenance Guide

DevForge features a scheduled maintenance engine powered by GitHub Actions and a task backlog runner.

## Scheduling

- **Schedule**: Every day at 10:00 PM IST (16:30 UTC).
- **Trigger**: `schedule` cron in `.github/workflows/daily-maintenance.yml` + manual `workflow_dispatch`.

## How the Pipeline Operates

```text
Scheduled Trigger (10 PM IST)
            │
            ▼
Inspect Repository & Backlog
   (scripts/backlog.json)
            │
            ▼
Select Daily Tasks
   (Targets 1-5 tasks; if 0 tasks available -> 0 commits)
            │
            ▼
Execute & Test Changes
   (Runs python scripts/validate.py)
            │
            ▼
Personal Attribution Commit & Push
   (Author: rudecat01 <dhruvchaudhary13978@gmail.com>)
```

## Credible Activity Principles

The random target represents a threshold of work, not an excuse to create empty commits:

| Target Count | Available Valuable Work | Resulting Commits |
| :---: | :---: | :---: |
| 4 | 4 tasks available | 4 commits |
| 5 | 2 tasks available | 2 commits |
| 3 | 0 tasks available | 0 commits |

If no useful task is pending or if changes fail validation, the pipeline exits cleanly without creating unneeded commits.

## GitHub Contribution Attribution

To ensure automated runs count towards the user's GitHub contribution graph:
1. Commits are explicitly authored with the account's registered email (`dhruvchaudhary13978@gmail.com`).
2. Commits land directly on the default branch (`main`) after passing automated validation checks.

<!-- task verified: ci-matrix-validation-refinement at 2026-11-23T05:49:07.709462 -->

<!-- task verified: docs-security-and-attribution-guide at 2026-11-23T05:49:09.080113 -->
