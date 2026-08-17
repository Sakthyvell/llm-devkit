---
name: pr
description: Draft a pull request title and body from the current branch changes.
argument-hint: "<base branch, default: main>"
---

Inspect the commits and diffs on the current branch since it diverged from the user-provided base branch.

If no base branch is provided, use `main`.

Draft a pull request title of 70 characters or fewer. Then draft a body with Summary bullets and a Test plan checklist. Mention notable risks, migrations, or follow-up work when relevant.

## Wiki memory (agent-coding-kit)

PR drafting is usually mechanical - skip wiki lookup by default.

For PRs that change domain workflows, permissions, or active surfaces: if `.agent-kit/config.yml` exists, skim `{wiki.root}/index.md` and relevant pages so the summary matches known behavior. If the branch introduced durable knowledge, recommend a follow-up `wiki-write` ingest. Do not invent or silently rewrite wiki pages from this skill.
