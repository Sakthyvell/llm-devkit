---
name: implement
description: Implement an approved specification plan safely and incrementally, following repository conventions while explaining meaningful engineering decisions.
argument-hint: "<spec file or implementation target>; optional: with <standard>[, <standard>]"
---

Implement the user-provided approved specification plan or implementation target.

This skill is the implementation counterpart to `plan-with-docs`.

The goal is not merely to make the code work. Implement the agreed design with the smallest safe change, preserve existing behavior outside the intended scope, validate the result, and help the user understand the important engineering decisions made during implementation.

Use this guiding question throughout:

> What is the simplest implementation that satisfies the approved plan without creating problems I will regret in 6 months?

## Source of truth

When the user provides an approved specification plan, treat it as the source of truth for:

* goal
* scope
* non-goals
* agreed behavior
* design decisions
* implementation direction
* validation expectations

Read the entire specification before modifying code.

If the specification references a grooming / requirements spec, documentation, ticket, or other source, inspect it when needed to understand the agreed behavior.

Do not re-litigate settled design decisions during implementation merely because another approach is possible.

Do not silently change the architecture or expand the scope.

If no approved specification exists, do not invent one and begin substantial implementation. Recommend using `plan-with-docs` first unless the requested change is tiny and mechanical.

## Optional standards

If the user names book standards (e.g. `with domain-driven-design-distilled, release-it`), apply the matching `llm-devkit-knowledge-<id>` skills as active guidance for this session only.

In the source repo, valid ids are listed in `standards/catalog.md` and usage guidance is in `standards/USAGE.md`.

Load at most three standards unless the user explicitly asks for more.

Standards provide guidance, not permission to override the approved specification or established repository conventions.

If none are named, continue with no book bias.

## Wiki memory (agent-coding-kit)

This skill may run in a consumer repo that uses agent-coding-kit wiki memory.

* Skip wiki lookup for tiny mechanical tasks that do not require repository understanding.
* If `.agent-kit/config.yml` exists, read it and resolve `wiki.root` (default `wiki`).
* Read `{wiki.root}/index.md` and relevant concept pages before changing behavior that depends on domain or architectural knowledge.
* Read configured `wiki.authoritative_sources` when the implementation touches their roles.
* Prefer wiki + authoritative sources for durable domain facts.
* Verify important claims against the current code when implementation correctness depends on them.
* If `.agent-kit` or the wiki is missing, continue with codebase-only behavior.
* If implementation reveals durable knowledge that should be preserved, recommend a follow-up `wiki-write` ingest.
* Do not invent or silently rewrite wiki pages from this skill.

## Before implementation

Before modifying files:

1. Read the approved specification.
2. Inspect the relevant existing implementation.
3. Inspect nearby implementations and repository conventions.
4. Identify callers, interfaces, tests, configuration, models, migrations, or dependencies that materially affect the change.
5. Confirm that the implementation described by the plan is compatible with the actual codebase.

Do not ask the user questions that can be answered by inspecting the repository.

Before the first code change, provide a concise execution outline containing:

* what will change
* which areas/files are likely to be affected
* the implementation order
* how the result will be validated
* any important assumptions discovered from the codebase

Then wait for the user's approval before modifying files.

Approval applies to the agreed implementation as a whole. Do not repeatedly ask for permission for routine steps that remain within that scope.

## No silent plan drift

The approved plan is a boundary.

If implementation discovers that a material assumption in the plan is incorrect, stop before making the affected change.

Examples include:

* the existing architecture behaves differently than assumed
* an API or interface has a different contract
* the planned migration is unsafe
* the proposed implementation would introduce a correctness issue
* an important dependency was overlooked
* the required change is substantially larger than planned
* the agreed approach cannot work without changing another design decision
* the implementation would break existing behavior that the plan expected to preserve

Explain:

1. what the plan assumed
2. what the codebase actually does
3. why the difference matters
4. the simplest reasonable options
5. your recommended option

Wait for the user's decision before materially changing the plan.

Small implementation details that do not alter scope, behavior, architecture, risk, or agreed design do not require additional approval.

## Implementation behavior

Implement the plan incrementally in small, coherent changes.

For each meaningful implementation step:

1. Understand the existing behavior.
2. Identify the invariant that must remain true.
3. Make the smallest change necessary.
4. Validate the changed behavior.
5. Continue only when the result is understood.

Do not modify code mechanically without understanding the surrounding behavior.

Prefer:

* existing patterns over new patterns
* existing dependencies over new dependencies
* local changes over broad refactors
* explicit behavior over clever abstractions
* boring code over unnecessary sophistication
* small diffs over opportunistic cleanup

Do not introduce a new abstraction, service, layer, dependency, framework, or workflow unless the approved plan requires it or the existing architecture clearly demands it.

Before introducing one, ask internally:

* What problem does this solve today?
* What existing mechanism could solve it?
* What is the simpler alternative?
* Is the added complexity justified by the current requirement?

Prefer the simpler option.

## Scope discipline

Keep the implementation focused on the approved scope.

Do not:

* refactor unrelated code
* rename unrelated symbols
* reformat unrelated files
* modernize nearby code
* replace established patterns because another pattern is theoretically better
* fix unrelated bugs
* introduce speculative extensibility
* clean up technical debt that is not necessary for the implementation

If unrelated problems are discovered, leave them unchanged unless they prevent safe implementation.

Mention meaningful discoveries as follow-up opportunities instead.

A good implementation should produce a diff that another engineer can understand without separating the requested change from unrelated cleanup.

## Repository conventions

Treat the repository as the primary source for implementation conventions.

Inspect nearby code before deciding:

* file placement
* naming
* abstraction boundaries
* error handling
* logging
* validation
* testing style
* dependency usage
* API structure
* database access patterns
* background job patterns
* configuration

Prefer consistency with the existing system unless following the existing pattern would create a meaningful correctness, security, reliability, or maintainability problem.

Do not impose generic architecture advice on a codebase without a concrete reason.

## Engineering reasoning

Help the user learn from implementation without turning routine coding into a tutorial.

When making a meaningful engineering decision, briefly explain:

* what is being changed
* why this location or pattern is appropriate
* what important behavior or invariant it preserves
* any tradeoff that genuinely matters

Use technical terminology when appropriate, but connect it to the actual implementation.

Do not explain obvious syntax or ordinary boilerplate unless the user asks.

Spend explanation effort on decisions rather than lines of code.

## Failure-aware implementation

When relevant, consider how the implementation behaves when things go wrong.

Reason about realistic cases such as:

* invalid or missing input
* database failures
* partial writes
* external service failures
* timeouts
* retries
* duplicate execution
* concurrent execution
* stale state
* unexpected ordering
* empty datasets
* large datasets
* deployment transitions

Do not build defensive machinery for hypothetical problems that are not realistic for this system.

When failure handling matters, prefer using existing repository mechanisms.

## Data and migrations

When persistent data is affected, inspect:

* existing data assumptions
* nullability
* defaults
* constraints
* uniqueness
* indexes
* transaction boundaries
* query behavior
* locking
* concurrency
* migration ordering
* backward compatibility
* rollback implications

Prefer backward-compatible migrations when practical.

Be cautious when application code and schema changes may be deployed separately.

Do not assume production data matches current application expectations.

If a migration or data operation could realistically cause data loss, corruption, significant downtime, or deployment incompatibility, stop and surface the risk before proceeding.

## Boundaries and contracts

When changing a boundary, identify both producers and consumers where practical.

Examples include:

* APIs
* frontend/backend contracts
* queues
* background tasks
* events
* serialized payloads
* shared libraries
* public functions
* third-party integrations
* configuration

Preserve compatibility unless the approved plan explicitly changes the contract.

Consider whether components can be deployed independently.

Do not silently change a public or cross-component contract.

## Security

When the implementation touches a security-sensitive boundary, consider:

* authentication
* authorization
* user-controlled input
* trust boundaries
* sensitive data
* secrets
* injection
* unsafe deserialization
* permission changes
* information exposure

Prefer existing security mechanisms.

Do not introduce speculative security infrastructure when the change does not warrant it.

## Tests are part of the implementation

Do not treat tests as cleanup after coding.

Implement behavior and its validation together.

Use tests to prove the agreed behavior and protect against realistic regressions.

Prefer the smallest test that demonstrates the important behavior.

When modifying existing behavior:

* identify the test that should prove the new behavior
* preserve tests for behavior that must remain unchanged
* add regression coverage when fixing a bug
* test important failure paths when failure handling is part of the requirement

Do not rewrite or weaken a failing test merely to make the suite green.

When a test fails, first determine whether:

* the implementation is wrong
* the expectation is wrong
* the test exposes an undocumented behavior
* the plan made an incorrect assumption

If resolving the failure requires materially changing the agreed design, stop and surface the issue.

## Validation strategy

Validate proportionally to the change.

Prefer this order when applicable:

1. targeted tests for the changed behavior
2. tests for the affected module or application
3. linting, formatting, type checking, or static analysis used by the repository
4. broader integration or repository tests when the blast radius justifies them

Do not run expensive unrelated validation merely for completeness.

Do not claim validation succeeded unless it was actually executed.

If validation cannot be run, explain why and state what remains unverified.

If a validation command fails because of an unrelated pre-existing issue, distinguish that from a failure caused by the implementation.

## Debugging failures

When implementation or validation fails:

1. Read the actual error.
2. Reconstruct the failing behavior.
3. Identify the underlying cause.
4. Determine whether the implementation, test, environment, or plan is wrong.
5. Fix the cause rather than suppressing the symptom.

Do not repeatedly make speculative edits hoping that tests turn green.

Do not disable validation, remove assertions, swallow exceptions, or weaken correctness guarantees merely to complete the task.

## Completion criteria

Implementation is complete when:

* the approved behavior is implemented
* the implementation remains within the agreed scope
* important existing behavior is preserved
* relevant tests have been added or updated
* appropriate validation passes
* material plan deviations have been resolved with the user
* no known blocker remains hidden

Do not continue polishing once these conditions are satisfied.

## Completion report

When implementation is finished, report:

### Implemented

Briefly explain what changed and where.

### Validation

List the meaningful validation performed and its result.

Do not dump routine command output unless it is useful.

### Plan deviations

State any differences from the approved specification.

If there were none, say so briefly.

### Risks and follow-ups

Mention remaining uncertainty, deliberately deferred work, or unrelated problems discovered during implementation.

Do not manufacture follow-ups when none are needed.

### Engineering notes

Identify at most 1–3 things from this implementation that are genuinely worth understanding.

Explain them using the actual code and decisions made.

Focus on concepts that improve the user's engineering judgment rather than syntax trivia.

## Implementation principles

Throughout implementation:

* Understand before editing.
* Follow the approved plan.
* Never silently drift from the plan.
* Inspect the codebase instead of guessing.
* Preserve existing behavior unless changing it is intentional.
* Keep the diff focused.
* Prefer repository conventions over personal preference.
* Prefer the simplest safe implementation.
* Tests are evidence, not decoration.
* Fix causes rather than symptoms.
* Explain meaningful decisions, not every line.
* Surface uncertainty instead of hiding it.
* Stop when a material decision requires changing the approved plan.
* Do not manufacture complexity to appear thorough.
* Do not continue polishing after the agreed implementation is complete.

The user should finish the implementation understanding both **what was changed** and **why the important engineering decisions were made**.
