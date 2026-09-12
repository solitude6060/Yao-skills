---
name: first-principles
description: Use before acting on an assumption not verified this session — a proposed fix, an inherited convention, a reviewer claim, a sub-agent's number, a too-good result — or when about to lower a threshold, skip a check, disable a test or hardcode a value.
argument-hint: "<incident | feature request | refactor proposal | result | empty>"
---

# First Principles

Re-derive from what you can observe before acting on what you inherited.
Three failure modes ship faster than a correct action: the action is a
workaround that hides the real need; the "root cause" came from an unreliable
signal (LLM-summarised bulk read, hearsay, sub-agent output); or urgency
skipped review.

## When to run

- User proposes a solution and the underlying need may differ
- "Everyone uses X", "it worked last time", "this module is too big"
- A result is outsized (+200%, NDCG 0.99, suspiciously uniform)
- A reviewer flags CRITICAL/HIGH and the "obvious" fix is ready
- About to say: drop it, lower the threshold, skip the check, disable the test, hardcode for now, just retry
- User asks "first principles?" or "is this a workaround?" — re-derive, do not defend

## The five questions — type them in the response

Build / plan / refactor:

1. What is the user's actual need, as distinct from the proposed solution?
2. What assumption makes me reach for this approach?
3. Is that assumption verified for this case, or inherited?
4. If it were wrong, what would I do differently? If nothing, proceed.
5. Does the approach address the need, or a symptom of it?

Fix:

1. What real property does the constraint I am about to bypass encode?
2. What is the user trying to accomplish beyond the literal blocker?
3. Is the constraint sound, or a structural mismatch with the goal?
4. Does my fix preserve the property under test?
5. Workaround or root cause? Root cause changes the constraint or the input
   space, preserves invariants, and needs no incident knowledge to read.

Verdict "workaround" means one of: write an ADR redefining the criterion;
reframe the test; widen the upstream input; or wait because the system is
correctly reporting nothing to do.

## Verify ground truth

| Claim | Reliable check | Unreliable check |
|---|---|---|
| "Item X exists / has value V" | per-item direct query | LLM summary of a bulk list |
| "Reviewer says line N has bug Y" | read file:line in the exact checkout | accept because severity is high |
| "Sub-agent's aggregate is M" | re-run aggregation locally with the canonical filter | accept the table |
| "Result improved +480%" | trace metric to raw path; spot-check 2–3 records for leakage | accept the headline |

Every factual claim points at an artefact: URL, `file:line`, probe output,
row count. Never "I remember" or "the summary said".

## Review is not waived by urgency

A hotfix skips review because it feels obvious; the same pressure makes it
more likely wrong. Run the project's review gate (`triple-review` where
required) before merging a hotfix. Cost of review: minutes. Cost of a wrong
hotfix: a second hotfix chain plus trust.

## Output

Leave a short audit in the PR body, plan file, or comment:

```markdown
## First-principles audit
- Need / constraint: <stated> vs <actual>
- Assumption relied on: <Z> — verified? <artefact | inherited>
- Ground truth: <claim> → <check> → <result>
- Verdict: root-cause | workaround (ADR #, deadline) | valid build decision
- Review: <artefacts>; CRITICAL/HIGH open: <n>
```

Any "inherited", "unverified", or "workaround without ADR" means not ready.

## Rationalizations

| Excuse | Reality |
|---|---|
| "Just a hotfix, no time for review" | Rushed fixes are more likely wrong; review matters more. |
| "I checked the bulk endpoint" | Per-item probe or it is unverified. |
| "The sub-agent already aggregated it" | Re-aggregate locally with the canonical filter. |
| "+480% is the new SOTA" | Audit the data pipeline before writing prose. |
| "Everyone uses X" | Verify your constraints match the ones X solves. |
| "Lower / disable X to make it go away" | Run the five questions. |
| "The reviewer is wrong" | Verify against the code before deciding. |
| "I'll fix it properly after we ship" | ADR plus ticket today, or ship the proper fix. |

## Read before acting

- The project's `CLAUDE.md` / `AGENTS.md` — SPEC pointers and invariants
- Project memory files covering ground-truth verification protocols
- Past `_FIX_LOG.md` files — failure patterns from prior bugs
- Research projects: relevant documents under `docs/audits/`
- `references/cases.md` — three near-misses and three public incidents; read
  when the result is load-bearing or the incident is in production
