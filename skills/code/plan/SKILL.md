---
name: plan
description: Collaboratively draft a specification plan by interviewing the user one decision at a time.
argument-hint: "<feature, problem, idea, or target file>"
---

Help the user create or refine a Markdown specification plan for the user-provided feature, problem, idea, or target file.

If a question can be answered by exploring the codebase, inspect the relevant files instead of asking the user. Prefer existing project conventions, nearby implementations, tests, configuration, and documentation over assumptions.

Interview the user relentlessly about every aspect of the plan until you reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one by one. Ask exactly one question at a time.

For each question:

- Explain why this decision matters when useful.
- Provide your recommended answer.
- Wait for the user's answer before moving to the next question.
- If the user's answer changes an earlier assumption, update the plan and revisit dependent decisions.

As decisions settle, maintain a Markdown spec document. The spec should capture:

- Goal and non-goals
- User-facing behavior
- Constraints and assumptions
- Design decisions
- Data model or interfaces, when relevant
- Implementation phases
- Validation and test plan
- Open questions

Do not implement code while using this skill unless the user explicitly asks to move from planning into implementation. The output of this skill is a shared plan that both the user and agent can keep editing through the conversation.
