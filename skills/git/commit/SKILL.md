---
name: commit
description: Draft a conventional commit message from the staged changes.
---

Inspect the staged changes and draft a conventional commit message.

Use a short imperative subject with a conventional commit type and optional scope. Add a body only when it explains useful context that is not obvious from the subject.

Do not commit the changes unless the user explicitly asks you to commit them.

## Wiki memory (agent-coding-kit)

Commit drafting is usually mechanical - skip wiki lookup by default.

If the staged change clearly documents durable domain behavior and the repo has `.agent-kit/config.yml`, you may briefly check `{wiki.root}/index.md` for naming consistency. If durable knowledge should be recorded, recommend a follow-up `wiki-write` ingest rather than editing the wiki from this skill.
