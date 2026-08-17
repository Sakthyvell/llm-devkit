# Knowledge Standards Usage

Use these standards as optional, task-scoped engineering guidance.

- Prefer `mini.md` for normal planning, implementation, refactoring, and review.
- Load at most three standards for one task unless the user explicitly asks for more.
- If standards overlap, choose the one most specific to the work instead of loading both.
- Treat the standards as decision pressure, not as a replacement for local code conventions.
- Do not apply a standard globally just because it exists in this repository.

Invocation examples:

- `plan with clean-code`
- `plan with refactoring, working-effectively-with-legacy-code`
- `review with release-it`
- `orient with domain-driven-design-distilled`

When a user names a standard, load `standards/<id>/mini.md` or invoke the matching installed skill `llm-devkit-knowledge-<id>`.
See `standards/catalog.md` for valid ids.
