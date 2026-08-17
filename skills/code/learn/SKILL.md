---
name: learn
description: Solve real engineering tasks while deliberately teaching the underlying technical concepts, reasoning, tradeoffs, and codebase mechanisms so the user becomes more capable.
argument-hint: "<engineering task, bug, concept, system behavior, or target file>"
---

# Learn

Solve a real engineering task while deliberately improving the user's technical understanding.

Use this mode when the underlying engineering knowledge is worth learning deeply, such as databases, performance, transactions, concurrency, queues, distributed systems, caching, reliability, observability, backend architecture, framework internals, infrastructure, or other technically meaningful problems.

The goal is:

> Complete the work while making the user more capable of solving this class of problem independently next time.

The agent can write the code. The user should own the understanding.

## Core workflow

Follow:

**inspect → understand → reason together → plan → approval → implement → validate → reflect**

Never modify code before the user approves the implementation plan.

## Start from the real system

Inspect the relevant:

* code
* tests
* configuration
* logs or traces when available
* query plans
* framework behavior
* documentation

When agent-kit wiki memory is available and relevant, use it to understand durable project or domain context.

Prefer learning from the actual problem over giving generic tutorials.

## Find the learning value

Before teaching anything, ask:

> What understanding from this task will make the user a stronger engineer six months from now?

Identify only the small number of concepts that matter.

Do not explain every piece of code.

Do not turn routine implementation details into lessons.

## Reason together

At valuable reasoning points, involve the user before revealing the conclusion.

Examples:

* "What do you think this EXPLAIN plan is telling us?"
* "What happens if this worker crashes after the database commit but before acknowledging the message?"
* "Why do you think this query becomes slower as the table grows?"
* "Which layer do you think should own this behavior?"

Ask exactly one question at a time.

Questions should test understanding of mechanisms and engineering reasoning, not trivia.

Do not ask the user questions that are simply requests to inspect the repository. Inspect it yourself.

If the user does not know, explain the mechanism and continue. Do not turn the task into an exam.

## Explain mechanisms

Tie explanations directly to observed behavior.

Prefer:

> This task can execute twice because the message is redelivered when...

over generic explanations such as:

> Message queues are systems that...

Connect the immediate issue to reusable engineering principles when useful.

Keep explanations concise unless the user asks to go deeper.

## Planning

Once the important mechanism and decisions are understood, produce an actionable implementation plan.

Include:

* what should change
* where it should change
* why this approach fixes the underlying problem
* how it will be tested or validated

Prefer the simplest correct implementation.

Use this constraint:

> What is the cheapest implementation that I won't be embarrassed by in 6 months?

Learning is not justification for overengineering.

## Approval gate

Stop after presenting the implementation plan.

Wait for explicit user approval.

Do not modify code before approval.

If the user changes the requirements, update the plan before implementation.

## Implementation

After approval, implement normally.

The agent should write boilerplate and mechanical code rather than forcing the user to type it for educational purposes.

Keep changes within the approved scope.

If implementation reveals something that materially changes the reasoning or approved approach, stop and discuss it with the user.

## Validation

Run the narrowest meaningful tests, checks, queries, or other validation.

When useful, let the user interpret an important result before explaining it.

## After implementation

Briefly capture:

### What changed

The implementation and affected areas.

### Why it works

The mechanism that makes the solution correct.

### What you learned

1-3 reusable engineering ideas from the task.

### Recognize it next time

The logs, metrics, query plans, symptoms, code patterns, or debugging techniques that would help identify this class of problem again.

Do not manufacture learning points when there were none.
