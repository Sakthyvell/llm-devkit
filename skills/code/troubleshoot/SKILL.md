---
name: troubleshoot
description: Investigate and resolve production issues, broken pipelines, failing tests, regressions, deployments, outages, and other urgent software failures.
argument-hint: "<symptom, failing command, log excerpt, incident, pipeline, service, or target file>"
---

Troubleshoot urgent or unclear failures by moving from evidence to containment, root cause, fix, and verification.

Use this skill for production issues, broken CI/CD pipelines, failed deploys, failing test suites, regressions, data or integration incidents, flaky behavior, and "something is broken" debugging.

## First response

Start by identifying:

- The reported symptom
- The affected surface, command, job, service, or user path
- What changed recently, if discoverable
- The fastest way to reproduce or observe the failure
- Whether immediate containment is needed before a code fix

If the issue may be user-impacting or production-facing, prioritize containment and verification over broad refactoring.

## Investigation workflow

Gather evidence before changing code.

- Read the failure output, logs, stack traces, CI job details, deployment messages, or monitoring clues the user provided.
- Reproduce locally when feasible with the narrowest command.
- Inspect relevant code, tests, config, environment references, migrations, lockfiles, build scripts, and recent diffs.
- Compare expected behavior to observed behavior.
- Form a short hypothesis, then test it.

Prefer concrete signals over guesses. If evidence contradicts the hypothesis, revise it instead of forcing the theory.

## Fix behavior

When the cause is clear:

- Make the smallest targeted fix that addresses the failure.
- Preserve existing behavior outside the failing path.
- Add or update a regression test when practical.
- Avoid broad cleanups during incident work unless they are required for the fix.

When the cause is not clear:

- Add temporary local diagnostics only when they materially improve understanding.
- Remove temporary diagnostics before finishing unless the user explicitly wants them kept.
- Escalate the key unknowns clearly instead of burying uncertainty.

## Pipeline and deployment issues

For broken pipelines, inspect:

- The exact failing step and command
- Dependency install behavior and lockfile changes
- Environment variables, secrets references, paths, versions, and caches
- Test ordering, timeouts, flaky tests, and generated artifacts
- Differences between local and CI environments

Do not assume the pipeline is wrong until the failing command and surrounding configuration have been checked.

## Production issue posture

For live incidents:

- Separate mitigation from permanent fix.
- Prefer reversible, low-blast-radius changes.
- Watch for data integrity, retries, idempotency, rate limits, permissions, and backward compatibility.
- Clearly state what is confirmed, what is suspected, and what is still unknown.

## Wiki memory (agent-coding-kit)

For substantive debugging in a consumer repo with `.agent-kit/config.yml`, read the wiki index and relevant pages when durable domain or architecture context could change the diagnosis. Skip wiki lookup for purely mechanical failures, small syntax issues, obvious test failures, or tasks where the failing output and nearby code are enough.

If the investigation uncovers durable operational knowledge worth keeping, recommend a follow-up `wiki-write` ingest. Do not invent or silently rewrite wiki pages from this skill.

## Output

For completed troubleshooting, report:

- Root cause or strongest confirmed cause
- Fix made
- Validation run and result
- Residual risk or follow-up, only when meaningful

For unresolved troubleshooting, report:

- Evidence gathered
- Hypotheses tested
- Most likely remaining cause
- The next command, log, or access needed
