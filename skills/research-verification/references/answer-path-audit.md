# Answer-path audit

Run when a gain looks large, uniform or cheaper than expected, before any prose is written about it. The
question is whether any path from the held-out answer to the score exists. Finding none is a result only
when each path below was checked.

## 1. Data path per component

For each component of the method, write one row:

| Component | Fields it reads | Source of each field | Time boundary | Can it see the target, its rating, its timestamp or later events? | Evidence |
|---|---|---|---|---|---|

- One time boundary for every component. Events with equal timestamps are ordered by original row order,
  never by item identifier; check that every component uses the same rule.
- Request-time information: if a component reads the time of the held-out event, the comparison methods
  must receive it too, or the paper must state the asymmetry and a control must remove it. An internal
  audit that rates this HIGH is answered by an experiment (a matched-information control), not by moving
  text.

## 2. Set intersections

Compute and record the size of each intersection; the expected value is stated before computing.

- Evaluated targets ∩ training events of any fitted component.
- Evaluated targets ∩ memory, index or statistics the method reads at inference.
- Reporting users' test targets ∩ targets used for development or selection (the same users may supply
  validation targets; their test targets must not), in this project and in sibling projects that share
  data.
- Cached outputs reused ∩ runs with a changed dependency.

## 3. Independent recomputation

Recompute the headline number from raw outputs with a script that does not import the project's scoring
code. Agreement with the reported number to the printed precision is required.

## 4. Sampled-negative audit

When candidates are sampled:

1. Write down the rule that selects negatives (hash order, popularity, time window).
2. Check whether the target passed through the same rule. If not, the rule can identify the target.
3. Score every candidate list by the selection rule alone, with no history and no model, and report the
   hit rate against the random expectation.
4. A hit rate far above random is a leak, even if the current method does not use it; a later method or
   model might. Fix the sampler (draw uniformly, or apply the same rule to the target), and record the
   audit.

Generic case: negatives were the items with the smallest salted hash while the target was not; ranking by
the reversed hash put the target first for nearly every user.

## 5. Identifier audit

If item or user identifiers appear in model inputs:

- score the same candidates by an identifier-only rule (largest id, smallest id, id order in the list);
- the rule must score near random. If it does not, remove identifiers from the inputs and rerun.

Generic case: on new-item candidate pools, a largest-id rule that read no history scored well above
random.

## 6. Cross-family review

Give the audit table, the intersection counts and the code paths to at least one reviewer from another
model family in a fresh context. Ask it to find a path the table missed. Verify each reported path
against the code before accepting or rejecting it ([finding-triage.md](finding-triage.md)).

## Record

The audit record lists each section above with its result, the commands, and what was not checked. A
section that was skipped is written as not checked; it is never summarized as "no leakage".
