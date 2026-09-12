---
name: triple-review
description: Use before merging a code change, or a document that defines experiment validity, data boundaries, metrics or result admission, when the project gate requires independent multi-model review of an exact revision.
argument-hint: "<PR number | branch | current branch>"
---

# Triple Review

Use this workflow for an exact PR revision or an explicitly requested local review target. The root agent remains the sole
orchestrator, triager, and decision owner; reviewer lanes do not delegate,
write, run scripts, call GitHub, post comments, or merge.

## Scope and target identity

1. Resolve the base, head branch, and exact `head_sha`; capture the target
   content hash when the review target is not a Git commit. Review only that
   immutable content.
2. Read the relevant specification, ADRs, invariants, and changed interfaces.
   Include the base-to-exact-head diff, context, and explicit review focus in
   the prompt. Require verdict, severity, `file:line`, evidence, impact, and
   a proposed repair for every finding.
3. Store the prompt, raw lane outputs, commands, target identity, and triage
   in a persistent project path or persistent sibling artifact directory.
   Resolve every destination with `realpath`; never use `/tmp` for review
   state or the sole copy of an artifact.

An approval binds only to the recorded commit/content hash. Any changed
reviewed content requires a review of the affected diff. Records-only changes retain
existing document approval when the reviewed document hashes are unchanged.

## Lane selection

Read the independent review-lane configuration in the project's `AGENTS.md` or
`CLAUDE.md`; when no location is configured, use `docs/MODEL_ROUTING.md` when it
exists. Use only lanes explicitly configured for the project and task. Never
hardcode provider, model, account, or absolute-path assumptions in this skill.
If a required independent lane is not configured, stop only that review action
and report the missing setup; an undefined lane is not an approval.

Use three reviewer sessions independent of the implementation context. Use
distinct underlying model families unless the project policy explicitly permits
a specific overlap. Accounts and client names do not establish family diversity.
Record the
actual reviewer identities, model families, and any policy-authorized overlap
with the root. Do not self-approve. Review validity and permission gates remain
mandatory. Fallbacks are allowed only when the project policy explicitly
authorizes that fallback for the observed failure; never silently substitute or
count a failed, empty, stale, or unverified replacement as approval.

Reviewers are instructed to remain read-only. Plan modes express intent and do not by
themselves prove OS-level isolation. Retain available sandbox enforcement.

## Execution and liveness

Run independent lanes in parallel where practical. Archive the actual command
and raw output for each attempt. An output is a verdict only when it contains a
substantive completed review of the exact target. Exit success, an empty file,
or source-catalog availability is never approval.

Use observed stream events, output growth, and process state to assess
liveness. Zero output alone does not prove a hang. If no new event arrives for
15 minutes, record the condition, make at most one bounded retry when the
failure appears transient, then use only the explicitly authorized fallback for that failure or
report the lane as unavailable. Never count a failed, empty, stale, or
unverified replacement as approval.

## Evidence triage and repair

Review evidence is not majority voting. Verify each factual claim against the
exact checkout, tests, specification, ADR, or authoritative documentation
before accepting or rejecting it. Record a triage table with finding, source,
severity, verified evidence, disposition, and rationale. Include a separate
integration-wiring check whenever changed components exchange data or control.

For accepted code findings at CRITICAL, HIGH, or MEDIUM severity:

1. add a regression test that fails for the intended behavior;
2. make the smallest repair and run the focused test green;
3. run proportionate repository checks; and
4. re-review the affected diff with the three configured independent review lanes until
   the code gate passes. The document round limit below does not waive a code gate.

Triage may defer a finding only with direct evidence that it is invalid,
out-of-scope, or safely owned by a recorded follow-up. Preserve TDD and exact
revision checks throughout.

## Document and configuration review

Documents defining experiment validity, data boundaries, held-out procedure,
metric definitions, result admission, or formal results require model review.
They pass with zero unresolved CRITICAL/HIGH findings; record MEDIUM/LOW
findings and resolve them after merge unless the project rule requires earlier
action. Allow one review round and at most one remediation re-review of the
affected diff, then stop for a user decision.

Ordinary documents use applicable validators and do not need this workflow.
Configuration and lock-file changes are risk-based: review them when their
behavior, supply-chain, deployment, or reproducibility impact warrants it;
they are not blanket-exempt.

## Records and stop condition

Archive review records and a fix log in the repository convention. Each record
names base and exact head/content hash, reviewer identity and model, command,
raw-output path, verdict, findings, verification evidence, triage, repairs,
and checks. Update project tracking records when the review changes their
truth.

Stop when required findings are repaired or evidence-triaged, required
re-review and validation pass, and all artifacts bind the final reviewed
revision. Do not post a PR comment, approve, merge, or otherwise mutate an
external service unless the current task explicitly authorizes that action.
