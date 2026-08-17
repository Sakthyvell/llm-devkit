---
name: review
description: Engineering-focused code review that explains the change, evaluates the design, identifies merge risks, and helps the reviewer improve their engineering judgment.
argument-hint: "<file, branch, diff, or PR number>"
---

Review the user-provided target. The target may be a file path, branch name, diff, or PR number.

If no target is provided, inspect the current working tree diff.

The goal is not only to find problems. Help the reviewer understand the change, evaluate the engineering decisions behind it, determine whether it is safe to merge, and learn something useful from the review.

Do not begin by hunting for isolated issues. First understand what the change is trying to accomplish and how it fits into the existing system.

## 1. Understand and teach the change

Before reviewing individual lines, build a mental model of the change.

Assume the reviewer is an experienced software engineer who may be unfamiliar with this subsystem and may have gaps in some underlying concepts. Do not dumb down the engineering. Dumb down the entry point. Start concrete, then introduce the proper engineering terminology.

Explain the change in layers. The reviewer should not need to understand repository-specific jargon, serializer names, framework internals, or architecture terminology before they can understand the bug or feature.

### Layer 1: The story

Start with the simplest concrete explanation of what happened from the user/system point of view.

For a bug, explain:

* What was the user or system trying to do?
* What did they expect to happen?
* What actually happened?
* What simple mismatch or mistake caused that behavior?

Use a small concrete example when it makes the behavior easier to visualize. Prefer a mental movie over an abstract summary.

Do not begin with class names, method names, framework terminology, or implementation details unless they are necessary to understand the story.

### Layer 2: Connect the story to the code

After the story is clear, map it onto the implementation. Show the important flow as a short sequence, for example:

`request -> serializer -> validation -> database write`

Use the actual functions, classes, fields, or components from the change, but explain what each one is doing in ordinary language.

### Layer 3: Root cause

State the root cause explicitly. Do not make the reviewer infer it from the before/after behavior.

Answer:

* What assumption in the old implementation was wrong or incomplete?
* Where was that assumption encoded in the code?
* Why did that produce the observed failure?
* Why had the existing behavior/tests not prevented it, when this can be determined?

Distinguish the root cause from the symptom. For example, a broken UI error may be a symptom while an incorrect backend validation assumption is the root cause.

### Layer 4: What the fix changes

Explain the implementation as a few simple behavioral rules before discussing design quality.

Then introduce the proper technical terminology and connect it back to the simple explanation. For example: “This is a compatibility fallback: old stored drafts may still have the missing field, so submit also repairs the value.”

Inspect surrounding code, tests, callers, models, configuration, migrations, interfaces, and nearby implementations when needed.

If something can be determined from the codebase, investigate it rather than asking the user.

If the intent cannot be confidently determined, clearly state what is uncertain.

Avoid unexplained jargon. When introducing an important technical term, briefly define it through this PR: what it means here and why it matters. The goal is for the reviewer to learn the terminology after understanding the concrete behavior, not to require the terminology in order to understand the review.

## 2. Evaluate the approach

Do not assume the implementation is the best approach simply because it already exists.

For meaningful design decisions:

1. Identify the realistic implementation approaches that could have been used.
2. Briefly explain the important tradeoffs of each.
3. Identify which approach this implementation uses.
4. Judge whether that approach is appropriate for this codebase and problem.

Prefer practical alternatives over theoretical possibilities.

Evaluate solutions using:

* correctness
* simplicity
* maintainability
* performance
* reliability
* security
* consistency with the existing architecture
* operational complexity
* expected future requirements

"Optimal" does not mean the most sophisticated design.

Prefer the simplest implementation that solves the problem safely and fits the system.

Call out unnecessary abstractions, premature generalization, cleverness, duplicated mechanisms, or complexity that does not provide meaningful value.

Also avoid recommending abstractions merely because they are considered good practice elsewhere.

Repository conventions and existing architecture matter.

## 3. Review behavior and correctness

Determine the behavioral contract of the changed code.

Consider:

* expected inputs
* outputs
* side effects
* state transitions
* invariants that must remain true
* existing behavior that must remain compatible
* assumptions the implementation depends on

Look beyond the happy path.

When relevant, reason through:

* invalid or missing input
* empty values
* partial failures
* database failures
* external service failures
* retries
* duplicate requests
* concurrent execution
* race conditions
* timeouts
* stale state
* unexpected ordering
* large inputs or datasets
* boundary conditions
* backward compatibility

Do not merely name a possible problem.

Explain the concrete scenario that triggers it and what observable failure could result.

## 4. Determine blast radius

For important changes, determine what else can be affected.

Inspect callers, consumers, shared models, APIs, tasks, events, configuration, and other dependencies where practical.

Explain:

* what paths use the changed code
* whether the change is isolated or shared
* which existing flows could regress
* whether old data or existing clients are affected
* whether deployment order matters
* how difficult the change would be to roll back

Pay extra attention to small changes made in central or widely reused code.

## 5. Review data and persistence

When the change interacts with persistent data, consider:

* transaction boundaries
* partial writes
* constraints
* uniqueness
* nullability
* defaults
* migrations
* migration safety
* existing/historical data
* indexes
* query behavior
* query count
* locking
* concurrency
* rollback behavior
* deployment compatibility

Do not flag theoretical database concerns without connecting them to realistic behavior or scale in this system.

## 6. Review boundaries and contracts

When the change crosses a system boundary, inspect the contract.

This includes:

* APIs
* frontend/backend interfaces
* external services
* queues
* background jobs
* events
* shared libraries
* public functions
* serialized data
* configuration

Consider whether producers and consumers remain compatible and whether components can be deployed independently.

Look for implicit assumptions that are not enforced by the contract.

## 7. Review security

Consider security where relevant, including:

* authentication
* authorization
* trust boundaries
* user-controlled input
* injection
* sensitive information
* secrets
* unsafe deserialization
* permission changes
* information exposure

Prioritize realistic attack paths over speculative security warnings.

Explain who or what can trigger the issue and what the consequence would be.

## 8. Review tests as evidence

Do not simply report that tests exist or are missing.

Determine:

* what behavior the tests actually prove
* which important behavior is not covered
* whether assertions test outcomes rather than implementation details
* whether failure paths are exercised
* whether regression scenarios are represented
* whether the tests could pass while the implementation remains broken

Recommend additional tests only when they meaningfully increase confidence.

For each important missing test, explain the scenario it should prove.

## 9. Review operability

When relevant, consider what happens after this code reaches production.

Ask:

* If this fails, will we know?
* Can the failure be diagnosed from existing logs or telemetry?
* Is enough context available to identify the affected request, user, job, or entity?
* Could retries or failures create noisy logs or alerts?
* Is there a safe recovery path?
* Would support or engineering be able to understand what happened?

Do not demand observability infrastructure for trivial code.

Apply this proportionally to the operational importance of the change.

## 10. Consider future change pressure

Do not design for hypothetical futures.

However, consider the most obvious next requirement when it exposes an important weakness in the current design.

Ask:

> If the next realistic variation of this requirement arrives, does this implementation remain straightforward to change?

Call out genuine design traps, but do not recommend premature abstraction merely to make future extension theoretically easier.

## 11. Distinguish severity from preference

Do not treat every observation as equally important.

Classify findings as:

### Blocker

Do not merge until resolved.

Examples include realistic risks of:

* incorrect behavior
* data corruption or loss
* security vulnerabilities
* broken contracts
* serious regressions
* unsafe migrations
* major production incidents

### Should Fix

A meaningful issue that should normally be addressed before merging, but is not an immediate correctness or safety failure.

Examples include significant maintainability problems, realistic performance problems, weak failure handling, or missing tests for important behavior.

### Non-blocking

Useful improvements that do not justify preventing the merge.

Examples include small simplifications, clearer naming, minor duplication, or localized maintainability improvements.

### Question

Something that may be intentional but cannot be determined confidently from the code.

Phrase these as questions for the author rather than assuming the implementation is wrong.

Style preferences should rarely affect the merge decision unless they materially hurt readability or violate established repository conventions.

## 12. Teach through the review

Use the change as an opportunity to improve the reviewer's engineering judgment.

When a finding involves an important engineering concept:

1. Name the concept.
2. Explain it using the actual code.
3. Explain why it matters here.
4. Keep the explanation proportional to its importance.

Examples include:

* transaction boundaries
* idempotency
* race conditions
* isolation
* indexing
* N+1 queries
* caching
* retry semantics
* API compatibility
* state ownership
* coupling
* cohesion
* dependency direction

Do not turn ordinary observations into lectures.

At the end, identify at most 1–3 engineering concepts genuinely worth learning from this change.

## 13. Questions for the author

When useful, identify questions an experienced engineer should ask before approving the change.

Prefer questions that uncover assumptions, such as:

* Can this operation execute more than once?
* Is partial success intentional?
* What happens when this dependency is unavailable?
* What is the expected maximum dataset size?
* Does anything depend on the previous behavior?
* Why was this approach chosen over the existing pattern?

Do not manufacture questions when the answer is already clear from the code.

## 14. Merge assessment

Finish with a clear recommendation:

* **Safe to merge**
* **Merge after fixes**
* **Needs discussion**
* **Do not merge**

Explain the decision briefly.

State the concrete things the reviewer should verify or resolve before merging.

## Output format

Structure the review in this order:

### The story

Explain the change as a concrete mental movie in plain English.

For bugs, cover what the user/system tried to do, what should have happened, what actually happened, and the simple reason it went wrong. Use a small example when useful.

This section should be understandable before the reviewer knows the relevant framework or subsystem. Avoid leading with code names or jargon.

### Code flow

Map the story to the actual codebase.

Show the important path through functions, classes, fields, storage, queues, APIs, or other components as a short sequence. Explain the role of each important step in ordinary language.

Keep this focused on the path needed to understand the change.

### Root cause

State the RCA explicitly and simply.

Separate:

* the visible symptom
* the underlying incorrect assumption or missing behavior
* the location where that assumption exists in the code
* why it produces the failure

If there are multiple contributing causes, distinguish the primary root cause from secondary issues.

### What the fix does

Explain the new behavior as simple rules first.

Then explain how the changed code implements those rules and why each changed location is needed. Make clear when part of the fix exists for old/stored data, backward compatibility, failure recovery, or another non-obvious reason.

### Engineering approach

Only after the behavior, code flow, RCA, and fix are understandable, evaluate the design.

Explain the approach used, realistic alternatives, important tradeoffs, and whether the chosen approach is appropriate.

Introduce technical terms here when they help the reviewer build engineering vocabulary. Define them using this PR rather than assuming the reviewer already knows them.

Keep this section proportional to the complexity of the change.

### Findings

Report findings grouped by:

1. Blocker
2. Should Fix
3. Non-blocking
4. Questions

For every meaningful finding include:

* file and line reference when possible
* what is happening
* why it matters
* a realistic failure or maintenance scenario
* what should change or be verified

Do not include empty severity sections.

For findings involving unfamiliar concepts, explain the concrete problem first and name the engineering concept second.

### Merge risk

Explain the blast radius and the main ways this change could cause a regression.

Explicitly state what existing behavior is most important to verify before merging.

### Tests and confidence

Explain what the existing tests prove in behavioral terms, what remains uncertain, and any important missing scenarios.

Do not merely list test names. Translate each important test into “this proves that ...”.

### What to learn from this PR

Choose at most 1–3 worthwhile engineering concepts demonstrated by the change.

For each concept, teach in this order:

1. The concrete situation in this PR.
2. The engineering term for it.
3. What that term means.
4. Why recognizing it will help in future reviews or implementations.

Do not give generic textbook definitions disconnected from the change.

### Verdict

Give one merge recommendation and a short justification.

State the concrete things the reviewer should verify or resolve before merging.

## Review principles

Throughout the review:

* Make the change understandable before evaluating it.
* Understand before criticizing.
* Explain concrete behavior before introducing jargon.
* Explain before labeling.
* Prefer concrete failure scenarios over vague warnings.
* Separate correctness from preference.
* Prefer repository conventions over generic architecture advice.
* Investigate the codebase instead of guessing.
* Do not invent requirements.
* Do not manufacture findings to make the review look thorough.
* Say when something is genuinely good engineering and explain why.
* A simple correct implementation is often better than a sophisticated one.
* Be concise when the change is simple and go deeper when the risk or engineering decision warrants it.
* The reviewer should finish understanding both **whether this should be merged** and **why the engineering decisions are good or bad**.

