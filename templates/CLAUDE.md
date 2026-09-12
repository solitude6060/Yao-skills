# Project agent instructions — adaptable template

Merge the relevant sections into your project's CLAUDE.md or AGENTS.md. Preserve
existing rules and fill in project-specific references; do not overwrite a global
configuration with this file. This template follows the community workflow in
[README.md](../README.md).

## Project contract

- Specification: `<canonical specification or README>`.
- Project memory: `status.md`, `tracker.md`, `handover.md` at the repository root.
- Integration branch: `<develop or the project's actual branch>`.
- Verification commands: `<focused tests, build and relevant validators>`.
- Deployment and external-action boundary: `<staging/production and approvals>`.
- Routing policy, if delegation/review is needed: `<path, e.g. docs/MODEL_ROUTING.md>`.
- Task-packet guidance, if maintained: `<path, e.g. docs/TASK_GUIDANCE.md>`.

Read the contract and real inputs before proposing changes. For narrow status or
settings work, read status.md if present; for development or research, read all
three management files and the specification. Existing task authorization persists.
Ask only when material scope, a missing requirement or an unapproved irreversible
action prevents a correct next step. Continue independent authorized work.

## Plan and implementation

For non-trivial work, commit a short plan on the authorized feature branch before
implementation. Include the outcome, scope, checks and stopping condition. Record
material architecture or contract decisions before changing the implementation.

For a bug, first add a regression test that fails for the intended behavior, then
make the smallest correction and run the affected checks. Preserve the failing-test
and passing-implementation history. Pure documentation and generated changes use
proportionate validators; state the exception in the commit body.

Reuse working patterns and standard-library or native features before adding code.
Do not introduce speculative abstractions or change adjacent code. Remove only the
imports and paths made unused by this change. Keep unrelated work intact.

## Delegation and model routing

The root owns integration and final verification. Delegate only independent work
that benefits from a separate agent. State the task, inputs, owned paths, acceptance
checks and escalation condition. Children do not delegate further.

Use the single routing policy named above for task qualification, model, client,
effort, account/data boundaries and fallbacks. Verify the actual runtime identity
when available. Do not downgrade a decision owner because of quota or silently
substitute a failed review lane. Missing routing setup blocks the affected
assignment; it does not block direct work within existing authorization.

Skill instructions apply only when the runtime exposes the skill and it fits the
request. Discussing a workflow does not invoke it. Persistent or repeated execution
requires an explicit operator request with scope and a stopping condition.

## Review and delivery

Follow the project's review gate. Use triple-review when three independent reviews
are required. Bind each review to the exact revision, retain raw outputs and verify
each finding against code or authoritative evidence. Record triage, accepted repairs,
false positives and deferred work in a fix log. An empty or failed review is not
approval. The implementer does not approve their work in the same context.

For accepted code findings, reproduce the problem, repair it, verify the correction
and re-review the affected diff. Ordinary documents use validators. Documents that
define experiment validity or formal results follow the project's scientific review
gate. Review records alone do not invalidate an unchanged document approval.

Use feature branches and pull requests; preserve commit history with a merge commit
where project policy requires it. Commit subjects state intent in Conventional
Commit form; bodies record the reason and useful constraints, checks and limitations.
Do not add AI co-author trailers. Merge, publishing and deployment require the task's
authorization. Identify exact targets before destructive actions, preserve unknown
artifacts, and never infer permission to force-push, drop data or stop another service.

## Evidence and research

Every factual claim needs a traceable file, command result or source. Verify numbers
at their producing artifact; an agent summary is a lead to check. Keep observation,
inference and unknowns separate. Report an unknown cause as unknown.

Before a consequential decision, check the need, the assumption, whether it was
verified, what changes if it is wrong, and whether current work produces evidence
or only preparation. Use first-principles when the audit adds value.

Research work starts with the smallest credible experiment that can decide continue,
adjust or stop. Use the project's existing data, leakage, metric and result-admission
rules. Preserve provenance and persistent outputs; inspect the first result before
expanding the platform. Do not invent a new evaluation protocol from this template.

## Persistent work and project memory

Keep worktrees and full clones in persistent sibling directories. Check destinations
with realpath before launch. Under the shipped worktree-hygiene policy, keep runs and
checkpoints in a separate persistent sibling and verify the inventory before retiring
a worktree. Temporary storage must never hold the only copy of work or evidence.

Update status.md, tracker.md and handover.md at relevant milestones. Record actual
results, unresolved conditions and the exact continuation command. Update the runbook
when operator behavior changes. Before clearing context, save the handover; do not
interrupt a process merely because a time or context threshold was reached.

## Communication and optional skills

Use the user's requested language. For Traditional Chinese, use Taiwan vocabulary,
retain standard technical terms and explain them briefly on first use. Keep exact
identifiers, commands, numbers and units; avoid unexplained shorthand and invented
terminology. Repository documents and commits use the project's declared language.

Use tc-review for Traditional Chinese text. Use distilled-caveman-lite-accuracy when
shorter answers are requested. An explicit wait-what request restores missing
background and explains the mechanism without losing evidence or conditions. It
changes the current explanation only; it authorizes no new edits or execution.
