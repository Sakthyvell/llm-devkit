---
name: plan-with-docs
description: Collaboratively draft a practical specification plan using codebase documentation and agent-kit wiki memory when relevant.
argument-hint: "<feature, problem, idea, or target file>; optional: with <standard>[, <standard>]"
---

Help the user create or refine a Markdown specification plan in the root directory for the user-provided feature, problem, idea, or target file.

If the user provides a grooming / requirements spec (e.g. from `scrum-groom`, `<ISSUE-KEY>-grooming-spec.md`), treat it as the agreed intent and scope input. Do not re-litigate settled grooming decisions unless the user asks; focus this skill on implementation design.

If a question can be answered by exploring the codebase, inspect the relevant files instead of asking the user. Prefer existing project conventions, nearby implementations, tests, configuration, and documentation over assumptions.

The goal is not to design the perfect solution. The goal is to create the simplest plan that solves the problem clearly and safely.

Use this guiding question throughout:

> What is the cheapest implementation that I won't be embarrassed by in 6 months?

## Optional standards

If the user names book standards (e.g. `with domain-driven-design-distilled, release-it`), apply the matching `llm-devkit-knowledge-<id>` skills as active guidance for this session only. In the source repo, valid ids are listed in `standards/catalog.md` and usage guidance is in `standards/USAGE.md`. Load at most three standards unless the user explicitly asks for more. If none are named, continue with no book bias.

## Wiki memory (agent-coding-kit)

This skill may run in a consumer repo that uses agent-coding-kit wiki memory.

- Skip wiki lookup for tiny mechanical tasks that do not require repo understanding.
- For planning and feature design: if `.agent-kit/config.yml` exists, read it, resolve `wiki.root` (default `wiki`), read `{wiki.root}/index.md`, and open relevant concept pages. Also read configured `wiki.authoritative_sources` when the topic touches their roles.
- Prefer wiki + authoritative sources for durable domain facts; verify against code when claims matter.
- If `.agent-kit` / wiki is missing, continue with codebase-only behavior and mention that the kit wiki is not attached.
- If planning surfaces durable knowledge worth keeping, recommend a follow-up `wiki-write` ingest. Do not invent or silently rewrite wiki pages from this skill.

## Planning behavior

Resolve only the decisions that materially affect the implementation.

Do not explore hypothetical future requirements, speculative edge cases, or unnecessary abstractions unless there is evidence they are needed.

Ask exactly one question at a time.

For each question:

* Explain why the decision matters when useful.
* Provide your recommended answer.
* Wait for the user's answer before moving to the next question.
* If the answer changes an earlier assumption, update the plan.
* Skip questions that can be answered from the codebase or existing conventions.

## Simplicity bias

Prefer:

* Existing patterns over new patterns
* Clear code over clever abstractions
* Fewer moving parts over architectural elegance
* Shipping a working version over designing an extensible version
* Capturing future ideas as future improvements instead of implementing them now

Before introducing a new abstraction, service, dependency, layer, or workflow, ask:

* What problem does this solve today?
* What is the simpler alternative?
* Is the added complexity justified?

Prefer the simpler option unless there is a clear reason not to.

## Specification output

Maintain a Markdown specification plan with only the sections that are relevant.

Common sections include:

* Goal
* Non-goals
* User-facing behavior
* Constraints and assumptions
* Design decisions
* Data model or interfaces, when relevant
* Implementation steps
* Validation and test plan
* Open questions
* Future improvements

Keep the plan actionable but not overly detailed.

The planning process is complete when the goal, scope, major decisions, implementation approach, and validation plan are clear enough to begin work.

Do not continue asking questions once the plan is actionable.

Do not implement code while using this skill unless the user explicitly asks to move from planning into implementation.
