---
name: pr
description: Draft a pull request title and body from the current branch changes.
argument-hint: "<base branch, default: main>"
---

Inspect the commits and diffs on the current branch since it diverged from the user-provided base branch.

If no base branch is provided, use `main`.

Draft a pull request title of 70 characters or fewer. Then draft a body with Summary bullets and a Test plan checklist. Mention notable risks, migrations, or follow-up work when relevant.
