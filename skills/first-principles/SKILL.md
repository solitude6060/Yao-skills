---
name: first-principles
description: Audit before acting on an inherited assumption — applies to build / plan / refactor AND fix. Distinguish workaround from root cause, verify ground truth per-item not via LLM-summarised bulk reads, never skip dual review on a hotfix. Three anonymised internal cases + three famous public cases (Knight Capital 2012, Mars Climate Orbiter 1999, Heartbleed 2014) anchor the discipline.
argument-hint: "<context — incident, feature request, refactor proposal, audit, or empty>"
---

# /first-principles — audit before acting on inherited assumption

Originally an incident-time discipline; the trigger is broader. Any moment a quick-reflex action would skip ground-truth verification — building, planning, refactoring, fixing — this skill is the gate.

Three failure modes that ship faster than a correct action can:

1. The action is a workaround that hides the real cause / underlying need
2. The "root cause" / "underlying need" was identified from an unreliable signal (LLM-summarised bulk API, hearsay, half-read log, sub-agent output)
3. The hotfix / decision skipped review because urgency or "obviousness" justified speed

## When to invoke

### Build / plan / refactor mode (proactive)

- Feature request where the user proposes a SOLUTION; you suspect the underlying NEED is different (dashboard vs single number; caching vs index; ML model vs baseline heuristic)
- Tool / library adoption — "everyone uses X" or "X is the modern way"
- Refactor proposal — "this module is too big" or "we need microservices"
- Naming / abstraction decision — "this should be a Manager / Service / Handler"
- **Evaluation result "too good to be true"** — outsized improvement, suspiciously uniform cross-method results, accuracy near ceiling. These have a high prior of being a data-leak / aggregation / filter bug, not a real win.

### Fix mode (the original trigger)

- A prod alarm fires (stale heartbeat, exception spam, recurring failures)
- A reviewer flags a CRITICAL/HIGH and you're about to write the "obvious" fix
- About to recommend any of: "drop the input", "lower the threshold", "skip the check", "disable the test", "hardcode this for now", "just retry"
- User pushback: "first principles?" / "is this a workaround?" / "did you verify?"

## Prerequisites

- The project's `CLAUDE.md` / SPEC is readable so invariants are explicit
- Project memory accessible (especially any `feedback_verify_*.md` or `feedback_aggregation_*.md` notes)
- Live API / data endpoints reachable for ground-truth checks
- A dual / triple review skill is available for hotfixes

## The 5-question audit — run literally, in the response

Type the questions and answers; the act of writing them is the discipline. Skipping it is how the wrong action ships.

### Build / plan / refactor variant

```
1. WHAT IS THE USER'S ACTUAL NEED?
   Not their proposed solution. A "dashboard" request often hides a single
   decision-relevant number. A "caching" request often hides "this query is too
   slow" with several different root causes (missing index? bad query plan?
   N+1?). An "ML model" request often loses to "median of last 30 days".

2. WHAT ASSUMPTION IS MAKING ME REACH FOR THIS APPROACH?
   Past similarity? Convention? Marketing? Authority? Name it explicitly in
   one sentence.

3. IS THE ASSUMPTION VERIFIED FOR THIS CASE, OR INHERITED?
   "Everyone uses X" is inherited. Verify YOUR constraints match the ones X
   solves. "It worked last time" is inherited; verify the THIS time looks
   like last time on the load-bearing axis.

4. IF THE ASSUMPTION WERE WRONG, WHAT WOULD I DO DIFFERENTLY?
   If the answer is "nothing", the assumption isn't load-bearing — proceed.
   If the answer is "build something else entirely", the assumption is
   load-bearing — verify before investing.

5. IS MY APPROACH ADDRESSING THE UNDERLYING NEED, OR A SYMPTOM OF IT?
   Adding a dashboard to surface a number is symptom-treatment if the user
   would have been happy with the number alone. Adding caching is symptom-
   treatment if the slow query was actually missing an index.
```

### Fix variant (original)

```
1. WHAT IS THIS CONSTRAINT ENFORCING?
   The thing about to be bypassed / dropped / loosened: what real property
   does it encode? A threshold, a test, a watchlist entry, a fail-loud raise
   — they all encode something.

2. WHAT IS THE USER ACTUALLY TRYING TO ACCOMPLISH?
   The literal blocker ("stop log spam") vs. the underlying goal ("valid
   coverage of the input set"). Relaxing the literal blocker often does NOT
   advance the goal.

3. IS THE CONSTRAINT SOUND, OR A STRUCTURAL MISMATCH WITH THE GOAL?
   If the constraint is wrong, the fix is changing the constraint via ADR —
   not bypassing it. If the goal is wrong, the fix is redefining the goal —
   not chasing it with workarounds.

4. DOES MY FIX PRESERVE THE PROPERTY UNDER TEST?
   If I'm dropping inputs to "stop log spam", do I still have their coverage?
   If I'm relaxing detector thresholds, does the hypothesis still hold?

5. IS THIS A WORKAROUND OR A ROOT-CAUSE FIX?
   Workaround tells: temporary, hides the real cause, ships a different system
   than the one tested.
   Root-cause tells: changes the constraint or the input space (not the
   boundary), preserves the original invariants, the next reader of the diff
   does not need the incident context.
```

If the verdict is "workaround", the next move is one of these — not the workaround:

- **Accept honestly** — write an ADR redefining the goal / criterion
- **Reframe the test** — the gate criterion was wrong about what it measured
- **Change the upstream input** — wider data / more cases — not the threshold
- **Wait** — the system may be correctly reporting "nothing to do"

## Verify ground truth (any mode)

When the alleged cause / claim is "X exists / X has value V / endpoint E returns R / sub-agent reports M", verify with the smallest possible direct query:

| Class of claim | Reliable verification | Unreliable verification |
|---|---|---|
| "Symbol X exists on exchange Y" | per-item GET on per-symbol endpoint | bulk list endpoint summarised by an LLM |
| "Field V of record X is N" | direct fetch of one record | LLM-summarised bulk parse |
| "Reviewer claims line 209 has bug Y" | `Read file:line` against current code | accept because severity is high |
| "Sub-agent's aggregated metric is M" | re-run aggregation locally on raw inputs with the canonical filter applied | accept the sub-agent's table as-is |
| "Result improved +400%" | trace each metric back to raw data path; spot-check 2-3 cases by hand for leakage / wrong filter | accept the headline number |

For every factual claim in the reasoning, point at a verification artefact (URL, `file:line`, probe output, raw row count). Never "I remember" or "the bulk summary said".

## Hotfix → dual review (any mode)

Speed pressure does not waive dual / triple review. The most dangerous category of hotfix is "we skipped review to ship faster" — the same urgency that justified the shortcut also makes the fix statistically more likely to be wrong than the average PR.

- Cost of running review: ~10 minutes for reviewers to return, 0 lines of code
- Cost of skipping review on a wrong fix: ship the wrong PR → realise post-deploy → second hotfix with another chain → 4× the original latency + trust damage

Always run review on a hotfix PR before merging.

## Real cases — when the audit caught the error (or didn't)

### Internal — LLM-summarised exchange listing (anonymised, trading project)

- **Inherited assumption**: an LLM summarisation of a futures exchange's bulk `/exchangeInfo` endpoint claimed 11 of 17 candidate symbols were "not listed" → drop them from the watchlist.
- **First-principles trigger**: a per-symbol probe to the kline endpoint contradicted the bulk summary; all 11 returned valid OHLCV data.
- **What audit found**: the bulk endpoint returned 800+ symbols; the LLM hallucinated 11 valid PERPETUAL contracts as missing. The actual bug was upstream — symbol-translation logic mishandled 4 memecoin tickers.
- **What workaround would have shipped**: a PR that dropped 17 valid symbols — losing real mid-cap coverage.
- **What root-cause fix shipped**: PR dropped only the 4 genuinely problematic symbols; the symbol-translation logic was fixed in a follow-up ADR.
- **Lesson encoded**: per-item probe beats bulk-summary every time the question is "which of these N items exists / has value V".

### Internal — Sequential training pipeline leakage (anonymised, research project)

- **Inherited assumption**: a preliminary experiment showed an outsized improvement (+143-488%) of one training variant over the baseline on sequential-input backbones → "we have a paper".
- **First-principles trigger**: numbers too dramatic; the researcher demanded a self-audit + dual review + Codex triple review before writing up.
- **What audit found**: a backfill step in the data preprocessing added the test target as the last element of each user's training session; the sequential dataset class used that last element as the *training target* → the model literally trained on the answer. 100% of sequential users affected. Sparse datasets amplified the visible effect.
- **What workaround would have shipped**: a paper claiming a major mining-method win — invalid; would have been retracted publicly after peer review.
- **What root-cause fix shipped**: the work was HALTED before the planned 72-cell rerun; the backfill step was removed; a regression test was added; the experimental narrative was retracted in the report.
- **Lesson encoded**: "too good to be true" findings are first-principles triggers, not paper triggers. Audit the data pipeline before writing prose.

### Internal — Sub-agent aggregated metrics (anonymised, research project)

- **Inherited assumption**: a sub-agent (smaller model) had aggregated results for a comparison table; "integrate it as-is".
- **First-principles trigger**: numbers didn't match the canonical results table on a spot-check.
- **What audit found**: the sub-agent had averaged ALL runs — including smoke / debugging variants and unrelated hyperparameter sweeps — without applying the project's canonical filter (which restricts to the agreed-upon seed count, hyperparameter family, etc.). The wrong conclusion reversed the ranking of two methods.
- **What workaround would have shipped**: a paper section with the methods ranked in the wrong order.
- **What root-cause fix shipped**: re-aggregated locally with the canonical filter; added a top-of-doc warning banner explaining the original error; updated the comparison narrative.
- **Lesson encoded**: sub-agent output is a hypothesis, not ground truth. Re-aggregate locally with the canonical filter before integrating sub-agent metrics.

### Public — Knight Capital, August 2012 ($440M loss in 45 minutes)

- **Inherited assumption**: dead code path from 8-year-old retail-routing logic was harmless because its flag was disabled; "we'll clean it later".
- **What went wrong**: a deploy reactivated the flag accidentally on 7 of 8 servers; the dead code ran live against production order flow, executing ~4 million unintended orders in 45 minutes.
- **Lesson**: workarounds that "stay around because they're harmless" are not harmless. Workaround → root-cause cleanup needs a deadline, not "later".
- Reference: SEC Release 34-70694 (2013).

### Public — Mars Climate Orbiter, September 1999 ($327M spacecraft lost)

- **Inherited assumption**: Lockheed Martin's ground software output pound-force seconds for thruster impulse; NASA's navigation team assumed Newton-seconds. Each side trusted "the interface is consistent because it always has been".
- **What went wrong**: orbiter entered Mars atmosphere ~57 km below target altitude, destroyed by atmospheric stress.
- **Lesson**: cross-team interfaces need explicit per-side unit verification at integration time, not "everyone knows the units".
- Reference: NASA Mars Climate Orbiter Mishap Investigation Board (1999).

### Public — Heartbleed (CVE-2014-0160), April 2014

- **Inherited assumption**: OpenSSL's heartbeat extension had a length-bounds check on the response payload — assumed because "this is battle-tested, reviewed code".
- **What went wrong**: missing length validation let a malformed request leak up to 64KB of process memory per call — including private keys, session cookies, passwords.
- **Lesson**: "battle-tested" is a comfort assumption. Coverage of THIS code path must be proven, not inherited from the package's general reputation.
- Reference: RFC 6520 heartbeat extension; OpenSSL CVE-2014-0160.

## Output — what this skill leaves behind

After running the audit, write a brief note (PR body, plan-file, or comment) naming each checkpoint's outcome:

```markdown
## First-principles audit

### 1. Need / constraint
- Stated need / constraint: <X>
- Actual underlying need: <Y>
- Same? <yes/no with reason>

### 2. Inherited assumption check
- Assumption I'm relying on: <Z>
- Verified for this case? <yes/no — verification artefact>

### 3. Ground-truth verification
- Claim: <"X exists" / "value V is N" / "metric M is +400%">
- Verification: <URL, file:line, command output, raw row count>
- Result: <true/false>

### 4. Verdict
- This is: <root-cause / workaround / valid build decision>
- If workaround / deferred-cleanup: <ADR # carrying the proper fix, deadline>

### 5. Review (for hotfixes / risky decisions)
- Review run: <link to artefacts>
- CRITICAL/HIGH findings: <count + summary>
- All addressed: <yes/no>
```

If any section produces "no" / "workaround without ADR" / "unverified" / "skipped", the PR / plan is not ready to merge / commit.

## Anti-patterns

| You're saying / doing | Reality check |
|---|---|
| "It's just a hotfix, no time for review" | The fix you're rushing is statistically more likely to be wrong than the average PR. Review matters more here, not less. |
| "I checked the bulk endpoint, all good" | Did you per-item GET, or did you ask an LLM to summarise? Bulk-summary is the classic LLM-hallucination failure mode. |
| "The sub-agent already aggregated it" | Re-aggregate locally with the canonical filter. Sub-agent output is a hypothesis, not ground truth. |
| "+400% improvement is the new SOTA" | Audit the data pipeline first. Outsized improvement with no ablation is the classic data-leak signature. |
| "Everyone uses X, we should too" | Verify YOUR constraints match the ones X solves. Convention is not evidence. |
| "Let me drop / lower / disable X to make this go away" | Workaround tell. Run the 5-question audit. |
| "The reviewer is wrong" | Maybe. Verify the factual claim against ground truth before deciding the reviewer is wrong. |
| "I'll fix it properly after we ship" | "After we ship" rarely happens. Either ship the proper fix or commit to a follow-up ADR + ticket today. |
| "Defending the workaround when challenged ('but it works')" | "Works" ≠ "is correct" — muting the symptom can mask a worse bug downstream. |

## Related artefacts to read before acting

- The project's `CLAUDE.md` — SPEC pointers + invariants
- Project memory: `feedback_verify_*.md`, `feedback_aggregation_*.md` — ground-truth verification protocols
- Past incident `_FIX_LOG.md` files — failure patterns from prior bugs
- For research projects: any `docs/audits/` directory tends to capture past first-principles incidents

$ARGUMENTS
