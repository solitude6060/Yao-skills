---
name: research-verification
description: Use when one or two major work items are done, before a milestone or submission, when a result looks too good, or when a reviewer or agent reports a finding, to verify numbers, claims, code paths and reviews in a fresh context and record what was checked.
argument-hint: "<task card, result table, paper path or finding list | empty>"
---

# Research Verification

Whoever produced a result is the weakest check on it: they read their own code as they meant it and
expect the number they got. Run the checks in a fresh read-only context, keep numerical agreement apart
from contract compliance and claim support, and record what was not checked.

Chinese: [SKILL.zh.md](SKILL.zh.md). Templates: [verifier brief](references/verifier-brief.md),
[answer-path audit](references/answer-path-audit.md), [finding triage](references/finding-triage.md).

## When to run

| Trigger | Scope |
|---|---|
| After every one or two major work items (result table, integration, paper revision, published page) | Items since the last verification |
| Before a milestone merge | Everything the milestone admits |
| Before submission | Every number, consistency between sentences, tables and sections, every reference |
| A gain looks large or too clean | Answer-path audit |
| A reviewer, review or agent reports a finding or a fact about a source | Finding triage |

Not for: the bound and noise of one measurement ([explain-the-number](../explain-the-number/SKILL.md));
an inherited assumption ([first-principles](../first-principles/SKILL.md)); merge gates
([triple-review](../triple-review/SKILL.md)); breakage beyond a diff ([blast-radius](../blast-radius/SKILL.md));
the producer's own planned-versus-actual check before admission
([experiment-contract](../experiment-contract/SKILL.md)); this skill re-checks it independently.

## 1. Verifier brief

Start a fresh read-only context. For a load-bearing claim, use a model from a family other than the one
that produced the work. The brief gives the task card, the owner's requests quoted, raw file paths, the
exact claims, and three questions:

1. Completeness: is everything on the task card and in the owner's requests done?
2. Correctness: recompute a sample of numbers from raw files with the exact row filters, and read the
   cited code or diff.
3. Direction: does the work serve the research questions and the current priorities?

The verifier records what it could not access or execute (a device, a service, a file outside its
sandbox); observations it did not make itself stay labelled with their source. Check afterwards that it
changed no file.

## 2. Verdict fields

Report three fields; one never implies another.

| Field | Question | Values |
|---|---|---|
| Numerical agreement | Do recomputed numbers match the reported ones? | agrees; differs (cells); not checked |
| Contract compliance | Did the run follow the agreed objective, cohorts, inputs and identities? | complies; differs (item); not checked |
| Claim support | Does the evidence support the sentence as worded? | supported; supported if narrowed; unsupported |

Generic case: a reselection analysis recomputed exactly, but used a different selection objective from the
main study, and its "equivalent" wording was unsupported.

## 3. Answer-path audit

When a gain looks large, audit before writing about it:

- Data-path proof per component: which fields reach the score, under which time boundary.
- Set intersections between evaluated targets and everything a component reads (training data, memory,
  selection targets, caches).
- Independent recomputation of the headline number from raw outputs.
- At least one reviewer from another model family.
- Sampled negatives: a selection rule applied to negatives but not to the target can identify the target.
  Rank candidates by that rule alone, without history; a hit rate far above random is a leak.
- Identifiers in model inputs: an identifier-only rule on the same candidates must score near random.

## 4. Findings, sources and paper numbers

- Verify each review or agent finding against the source before acting: exists, partly, absent, with
  `file:line`.
- A claim of absence needs a full-text search of the whole document or repository.
- Recheck an agent-reported fact about a source (a setting the original authors used) at that source.
- Text and table tests must fail on a mutated copy; an assertion that compares a value with itself
  certifies nothing.
- Regenerate paper numbers from the table generator, reading the admitted row; never copy numbers from a
  rewrite suggestion.
- An interval that includes zero is no significant difference at this sample size; it shows equivalence
  only when the whole interval lies inside a margin declared before the run
  ([explain-the-number](../explain-the-number/SKILL.md)).
- Compare latencies only on the same device; otherwise measure a small sample of both sides on one device.
- An interrupted, empty or exit-code-only review is not an approval.

## Output

Write next to the task card: the verification record (brief, verifier identity, access limits, the three
verdict fields), the triage table (finding, source, evidence, exists, partly or absent, disposition,
rationale) and the fix log. Tell the owner the verdict in one or two lines in the project's chat language.
A failed check returns only the affected work to the earlier stage.
