---
name: plan
description: Make a lightweight implementation plan without wiki or documentation lookup, then wait for explicit user approval before making code changes.
argument-hint: "<small feature, bug, refactor, or fix>; optional: with <standard>[, <standard>]"
---

Handle small planning tasks with minimum ceremony.

Use this skill when the user wants a quick plan, a small fix, a narrow refactor, or an implementation approach that does not need durable repo memory or documentation lookup.

Do not perform agent-kit wiki lookup from this skill, even when `.agent-kit/config.yml` exists. Inspect code, tests, and config only as needed to make the immediate change safely.

Do not modify code while using this skill unless the user explicitly approves the implementation plan or explicitly asks to proceed with implementation.

## Optional standards

If the user names book standards (e.g. `with clean-code, refactoring`), apply the matching `llm-devkit-knowledge-<id>` skills as active guidance for this session only. In the source repo, valid ids are listed in `standards/catalog.md` and usage guidance is in `standards/USAGE.md`. Load at most three standards unless the user explicitly asks for more. If none are named, continue with no book bias.

## Operating mode

Default to planning first.

- Inspect the relevant files, then produce a concise implementation plan.
- If the task needs one important decision, ask exactly one concise question and recommend an answer.
- If the task is clearly implementable, still stop after the plan and ask for approval before editing.
- If the user approves, move into implementation, make the change, and validate it.
- If the task turns out larger or ambiguous, produce a brief plan and call out the uncertainty before asking for approval.
- If durable product or domain knowledge is required, recommend switching to `plan-with-docs` or `orient`.

## Quick plan shape

Keep plans small. Prefer 3-6 bullets covering:

- Target behavior
- Files or components likely touched
- Implementation steps
- Validation
- One risk or open question, only when meaningful

Avoid full specification documents, wiki updates, long alternatives, and speculative future work.

## Implementation approval gate

Before requesting approval:

- Read the smallest useful set of files.
- Follow nearby conventions and existing helpers.
- Prefer localized changes over new abstractions.
- Include focused tests in the plan when the change has behavior risk.

Ask for approval in plain language, such as:

> I can implement this plan now. Do you want me to proceed?

Do not treat silence, vague agreement, or continued discussion as approval to edit. Proceed only after an explicit confirmation such as "yes", "approved", "go ahead", "implement it", or equivalent.

After approval and editing:

- Run the narrowest relevant validation command available.
- If validation is not practical, explain what was checked and what remains unverified.

## Output

For planning work, provide:

- The brief implementation plan
- Files or areas likely touched
- Validation to run
- Any material risk or open question
- A request for approval before implementation

For completed fixes after approval, summarize:

- What changed
- Where it changed
- How it was validated
