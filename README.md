# llm-devkit

Personal, tool-agnostic AI agent skills installed globally for Claude Code, Codex, and Cursor.

## Install

Clone this repo once per machine:

```bash
git clone <repo-url> ~/dev/llm-devkit
cd ~/dev/llm-devkit
./install.sh
```

The installer generates:

```text
~/.claude/skills/llm-devkit-<category>-<skill>/SKILL.md
~/.agents/skills/llm-devkit-<category>-<skill>/SKILL.md
dist/cursor-user-rules.md
```

Paste `dist/cursor-user-rules.md` into Cursor Settings -> Rules.

## Commands

```text
Claude: /llm-devkit-code-review
Codex:  $llm-devkit-code-review
Cursor: @llm-devkit-code-review
```

V1 skills:

- `llm-devkit-code-review`
- `llm-devkit-git-commit`
- `llm-devkit-git-pr`

## Maintenance

Preview changes:

```bash
./install.sh --dry-run
```

Remove generated global skills and local generated files:

```bash
./install.sh --clean
```

After updating this repo, rerun:

```bash
./install.sh
```

## Authoring Skills

Add skills at:

```text
skills/<category>/<skill>/SKILL.md
```

Example:

```markdown
---
name: review
description: Review code for correctness, bugs, security issues, and maintainability.
argument-hint: "<file, branch, diff, or PR number>"
---

Review the user-provided target.
```

Keep source skills tool-agnostic. Tool-specific output is handled by the installer.
