---
name: first-principles-fix
description: When a prod incident or bug needs a fix, slow down and audit your proposed fix BEFORE writing code — distinguish workaround from root cause, verify ground truth per-item not via LLM-summarised bulk reads, and never skip dual review on a hotfix.
argument-hint: "<incident description | PR# under work | empty for current context>"
---

# /first-principles-fix — incident triage with three loaded checkpoints

When a prod incident demands a fix, the temptation is to write code immediately because the bleeding has to stop. **Don't.** Three failure modes ship faster than a hotfix can:

1. The fix is a workaround that hides the real cause
2. The "root cause" was identified from an unreliable signal (LLM-summarised bulk API, hearsay, half-read log)
3. The hotfix skipped review because urgency justified speed

This skill is the discipline that should fire the moment the incident alarm does.

## When to use

- A prod alarm fires (stale heartbeat, exception spam, recurring tick failures)
- A reviewer flags a CRITICAL/HIGH and you're about to write the "obvious" fix
- You're about to recommend any of: "drop the symbol", "lower the threshold", "skip the check", "disable the test", "hardcode this for now"
- A user pushes back with "first principles?" / "is this a workaround?" / "did you verify?"

## Prerequisites

- The project's `CLAUDE.md` / SPEC is readable so invariants are explicit
- Project memory is accessible (especially any `feedback_verify_*.md` notes)
- Live API endpoints are reachable for ground-truth checks
- A dual / triple review skill is available

## Workflow — three checkpoints, in order

### Checkpoint 1 — Audit the proposed fix BEFORE writing code

Answer these five questions out loud in the response (not as internal monologue). The act of writing them is the discipline; skipping it is how workarounds ship:

```
1. WHAT IS THIS CONSTRAINT ENFORCING?
   The thing I'm about to bypass / drop / loosen — what real
   property does it encode? A threshold, a test, a watchlist
   entry, a fail-loud raise — they all encode something.

2. WHAT IS THE USER ACTUALLY TRYING TO ACCOMPLISH?
   The literal blocker ("stop log spam") versus the underlying
   goal ("valid coverage of mid-cap symbols on both exchanges").
   Relaxing the literal blocker often does NOT advance the goal.

3. IS THE CONSTRAINT SOUND, OR A STRUCTURAL MISMATCH WITH THE GOAL?
   If the constraint is wrong, the fix is changing the constraint
   via ADR — not bypassing it. If the goal is wrong, the fix is
   redefining the goal — not chasing it with workarounds.

4. DOES MY FIX PRESERVE THE PROPERTY UNDER TEST?
   If I'm dropping inputs to "stop log spam", do I still have
   their coverage? If I'm relaxing detector thresholds, does
   the hypothesis still hold?

5. IS THIS A WORKAROUND OR A ROOT-CAUSE FIX?
   Workaround tells: temporary, hides the real cause, ships a
   different system than the one tested.
   Root-cause tells: changes the constraint or the input space
   (not the boundary), preserves the original invariants, the
   next reader of the diff does not need the incident context.
```

If (5) is "workaround", the next move is one of:

- **Accept honestly** — write an ADR redefining the goal/criterion
- **Reframe the test** — the gate criterion was wrong about what it measured
- **Change the upstream input** — wider data / more cases — not the threshold
- **Wait** — the system may be correctly reporting "nothing to do"

### Checkpoint 2 — Verify ground truth, never trust LLM summarisation

When the alleged root cause is "X exists / X doesn't exist / field V is N", verify with the smallest possible direct query:

| Class of claim | Reliable verification | Unreliable verification |
|---|---|---|
| "Symbol X exists on exchange Y" | per-item GET on `<api>/<endpoint>?id=X` | bulk-list endpoint summarised by an LLM ("which of these N exist") |
| "Field V of record X is N" | direct fetch of one record | bulk list parsed by LLM (LLM hallucinates specific values) |
| "Reviewer claims line 209 has bug Y" | `Read file:line` and check the assertion against current code | accept because severity is high |
| "Threshold T should be N per spec" | grep the SPEC for the value | accept the reviewer's quote of what the spec says |

**Worked example** (anonymised real incident): a futures exchange's `/exchangeInfo` returns 800+ symbols. Asking an LLM to "summarise which of [A, B, C, ...] exist" produced 11 false negatives — symbols that *did* trade. Asking the per-symbol kline endpoint with `?symbol=A&interval=1m&limit=1` returned a small array per symbol — unmistakably "valid". Same exchange, same data, completely different reliability.

**Rule**: for every factual claim in your fix's reasoning, you must be able to cite a verification artefact (a URL, a `file:line`, a probe output). Never "I remember" or "the bulk summary said".

### Checkpoint 3 — Hotfixes still go through review

Speed pressure does not waive review. The most dangerous category of hotfix is "we skipped review to ship faster" — the same urgency that justified the shortcut also makes the fix statistically more likely to be wrong than the average PR.

**Cost of running dual / triple review**:
- ~10 minutes for reviewers to return
- 0 lines of code

**Cost of skipping it on a wrong fix**:
- Ship the wrong PR through the release chain
- Realise it's wrong post-deploy
- Roll out a second hotfix with another full chain
- 4× the latency of the original review

Always run review on a hotfix PR before merging.

## Output — what this skill leaves behind

After running the checkpoints, write a brief audit (PR body or comment) naming each checkpoint's outcome:

```markdown
## First-principles audit

### Checkpoint 1: workaround vs root cause
- Constraint enforced: <X>
- Underlying goal: <Y>
- Constraint sound? <yes/no with reason>
- Property preserved? <yes/no>
- Verdict: <root cause / workaround>
- If workaround: <why this PR is still the right call now, and which ADR carries the root-cause fix>

### Checkpoint 2: ground-truth verification
- Claim: <"X exists on exchange Y" / "value V is N">
- Verification: <URL, file:line, command output>
- Result: <true/false>

### Checkpoint 3: review
- Review run: <link to artefacts>
- CRITICAL/HIGH findings: <count + summary>
- All addressed: <yes/no>
```

If any checkpoint produces "no" / "workaround" / "unverified" / "skipped", the PR is not ready to merge.

## Anti-patterns (red flags worth pausing on)

| You're saying / doing | Reality check |
|---|---|
| "It's just a hotfix, no time for review" | The fix you're rushing is statistically more likely to be wrong than the average PR. Review matters more here, not less. |
| "I checked the bulk endpoint, all good" | Did you check via per-item GET, or did you ask an LLM to summarise the bulk response? |
| "Let me drop / lower / disable X to make this go away" | Workaround tell. Run Checkpoint 1. |
| "The reviewer is wrong" | Maybe. Verify the factual claim against ground truth before deciding the reviewer is wrong. |
| "I'll fix it properly after we ship" | "After we ship" rarely happens. Ship the proper fix or commit to a follow-up ADR + ticket today. |

## Related artefacts to read before fixing

- The project's `CLAUDE.md` — SPEC pointers + invariants
- Project memory `feedback_verify_*.md` — ground-truth verification protocols
- Past incident `_FIX_LOG.md` files — failure patterns from prior bugs

$ARGUMENTS
