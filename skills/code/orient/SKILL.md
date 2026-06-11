---
name: orient
description: Explain how the relevant code currently works before planning or implementation.
argument-hint: "<feature, problem, idea, file, branch, diff, or PR number>"
---

Help the user understand the current implementation before planning or changing anything.

The goal of this skill is to build a clear mental model of the existing codebase area related to the user-provided feature, problem, idea, file, branch, diff, or PR number.

Do not propose a full implementation plan yet unless the user explicitly asks for one.

Do not modify code while using this skill.

## Investigation behavior

Inspect the relevant codebase files, tests, configuration, documentation, and nearby implementations.

Prefer evidence from the codebase over assumptions.

Trace the current behavior through the system, including:

* Entry points
* Request or event flow
* Main functions, classes, services, jobs, or handlers
* Data models and database interactions
* External dependencies or integrations
* Validation, permissions, and error handling
* Existing tests
* Existing conventions and patterns

If the user provides a target file, branch, diff, or PR number, start there, then inspect related code as needed.

If the target is unclear, make a reasonable best-effort search before asking questions.

Ask questions only when the answer cannot be reasonably inferred from the codebase.

## Output

Produce a Markdown orientation note that explains the current state of the system.

Use only the sections that are relevant.

Common sections include:

### Summary

Briefly explain what this area of the code currently does.

### Current flow

Explain the current behavior step by step.

Include important files, functions, classes, endpoints, jobs, or modules.

### Working parts

List the key pieces that already exist and what each one is responsible for.

### Data and interfaces

When relevant, explain:

* Database models or tables
* API contracts
* Events or messages
* Request and response shapes
* External service calls
* Configuration values

### Existing conventions

Identify nearby patterns the implementation should probably follow.

Mention whether the current code favors services, repositories, serializers, factories, direct model usage, async jobs, events, or other conventions.

### Where the proposed change may touch

Explain which parts of the codebase are likely to be affected.

Separate likely touchpoints from uncertain touchpoints.

### Risks and dangers

Identify things that could break or require care, such as:

* Backward compatibility
* Data integrity
* Permissions
* Validation gaps
* Race conditions
* Retry or idempotency concerns
* Performance issues
* Migration risks
* Hidden coupling
* Missing tests
* External integration behavior
* Error handling edge cases

### Unknowns

List anything that is still unclear after inspecting the code.

Do not guess silently.

### Suggested next step

Recommend whether the user should:

* Proceed to planning
* Inspect another area first
* Write characterization tests first
* Clarify requirements
* Avoid the change
* Use a simpler approach

Keep the recommendation practical and grounded in the code.

## Style

Be clear, concrete, and codebase-specific.

Prefer explaining actual behavior over giving generic advice.

When mentioning files, functions, classes, endpoints, or tests, include their names.

Avoid overexplaining obvious code.

Focus on helping the user understand enough to make a safe implementation decision.

The output of this skill is a shared understanding of the existing system, not an implementation plan.
