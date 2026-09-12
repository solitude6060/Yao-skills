---
name: workflow-routing
description: Use before non-trivial coding or research work when deciding who plans, who implements, whether to delegate, and whether triple-review applies — or when an older lettered-workflow or quota-downgrade recipe would otherwise pick the models.
---

# Workflow Routing

Read the model-routing policy configured by the project in `AGENTS.md` or
`CLAUDE.md` before classifying, selecting, or delegating. When no project
location is configured, use `docs/MODEL_ROUTING.md` when it exists. That policy
is the only source for table, tier, client, model, effort, fallback, and
approval gates. This skill chooses workflow shape. It does not copy or replace
those tables.

When planning or delegating, read task guidance at the location named in the
project instructions, or `docs/TASK_GUIDANCE.md` when it exists. If no guidance
file is configured or present, use the project instructions and this skill without
treating the missing file as a blocker. Lettered workflows, vendor-specific
recipes, and quota-driven model downgrades are superseded.

## When to use

- Before non-trivial implementation or research work, or when opening a track plan file
- When the user asks which workflow, who plans versus implements, or whether to review
- Skip for a typo, single-line config, or ordinary document edit the current root can finish in session

## Classify first

1. Pick the table: Coding for software artifacts; Research for knowledge artifacts. Mixed work uses the table of the deliverable that carries the risk.
2. Classify Low / Medium / High / Very High / Extreme from uncertainty, blast radius, reversibility, security, architecture, and validation cost. File count and model availability do not set the tier.
3. State table, tier, client, model, effort, and write permissions before any delegation.
4. Keep the user's selected root. The root may finish a small in-scope action directly when coordination would cost more. Do not pick a frontier child for Low work or relabel a hard task as Low.

Use only the configured policy for provider availability, client exceptions, and
confirmation gates. If no routing policy is available, the current root may
finish direct in-scope work; delegation or review that requires undefined lanes
stops only that action and reports the missing setup.

## Workflow shapes

Pick a shape. Then select the client, model, and effort from the configured policy.

### Direct

The current root plans, implements, and verifies in one pass. Use for Coding Low or Research extraction when the specification is local and the blast radius is small. Use project validators. Do not invent a cheaper child to save quota.

### Planned implementation

Write a durable plan file first. Implement from that plan with a policy-qualified model. The implementer does not add architecture, fields, or invariants the plan did not authorize.

Use for ordinary Coding Medium features, refactors, and well-specified multi-file work.

### Split authority

A model other than the implementer owns the plan. Implementation uses a qualified model from the same classified tier. Verification of a load-bearing result never returns to the producer and never uses a lower tier than the work.

Use when the change creates a SPEC or ADR invariant, an algorithmic core, a risk or safety control, a live or production gate, or otherwise matches Coding High or above, or Research Medium and above analysis or planning.

### Research decision

Substantive analysis, method choice, experimental design, and claims use the Research policy. Follow its analysis floor and decision-owner requirements; supporting models do not become the decision owner.

## Review

- Invoke `triple-review` for code changes and for documents that define experiment validity, data boundaries, held-out procedure, metrics, result admission, or formal results.
- Lanes come from the independent review configuration in the project's policy. Cross-verification requirements per tier come from that policy.
- Ordinary documents use validators. Configuration and lock-file changes are reviewed when behavior, supply chain, deployment, or reproducibility is at stake.
- The root triages. Reviewers do not merge, comment, or write.

## Delegation

- The root is the sole orchestrator. Children do not spawn workers.
- Client order, model allowlists, provider preferences, confirmation gates, and fallback behavior come from the configured policy; apply them as written, do not infer or restate them here.
- Fallbacks stay in the same table and tier. Record the first choice, why it failed, and the substitute. If no same-tier fallback exists, stop and ask.

## Parallelism

Independent writers own disjoint paths. Use `worktree-hygiene` when creating, auditing, or retiring worktrees. Persistent artifacts never go to `/tmp`. One writer per checkout.

## Anti-patterns

| Excuse | Reality |
|---|---|
| Follow an old lettered workflow as written | It may pin retired models. Classify against the configured policy. |
| Downgrade the model because quota is yellow | Quality first. Same-tier recorded fallback only. |
| Copy the Coding or Research tables into this skill | The project policy is the live table. |
| Implementer adds an unplanned field while here | Escalate to a plan or ADR. |
| Child dispatches another model | Root only. |
| Skip triple-review because the implementation model is strong | Review is a tier and process gate. |

## Stop condition

Announce table, tier, shape, selected model and effort, and whether triple-review applies. Then start the first authorized step. Do not post, approve, or merge unless the current task authorizes it.
