---
name: review
description: Review code for correctness, bugs, security issues, and maintainability.
argument-hint: "<file, branch, diff, or PR number>"
---

Review the user-provided target. The target may be a file path, branch name, diff, or PR number.

If no target is provided, inspect the current working tree diff.

Prioritize correctness, bugs, regressions, security issues, missing tests, maintainability, and style. Report findings first, grouped by severity. Include file and line references when possible. Keep summaries brief and place them after the findings.
