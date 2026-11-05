# Admission and supersession

A number is admitted only after these checks. Until then it is pending, and pending numbers never appear
in a published page or the paper.

## Admission checklist

1. Completeness. Every planned unit has an output. Units with execution failures are rerun until they
   succeed; a run with unresolved execution failures is not admitted.
2. Failure classes. Count each class separately:

   | Class | Examples | Treatment |
   |---|---|---|
   | Execution failure | Out of memory, server error, crash, timeout, missing file, port conflict | Rerun; record attempts and cause; never a result |
   | Over-limit input | An input longer than the model's or interface's limit | Apply the declared truncation rule first (oldest history first; record the kept events and tokens). An input still over the limit is labelled over-limit, counted and reported beside the score, and stays in that method's denominator with utility zero, or all methods are reported on the common units; never drop it for one method only |
   | Method failure | Output that cannot be parsed or is invalid; no ranking possible by design | Keep in the denominator with utility zero; report the count beside the score |

3. Cost fields. Every run: wall time, per-unit latency (median and p95), peak accelerator memory, device.
   Model-calling runs (language-model or agent calls) add calls per unit, mean input and output tokens,
   and API cost for hosted models; trained models record inference time per unit on the same candidates.
   Fill missing fields from raw records where possible and state the method; a row without them waits.
4. Recomputation. Recompute the aggregate from per-unit files with the exact row filters (method,
   configuration, cohort, candidate count, stage). The reported value and the recomputed value match.
5. Identity. The returned model id, the imported source hashes and the data, candidate and evidence hashes
   match the contract ([run-identity.md](run-identity.md)). Every derived table checks the checkpoint
   identity of each of its rows against the main table.
6. Semantics. The selection objective is the contract's objective, and the request does what the label
   says. A run with another objective is a labelled variant.
7. Run choice. The first pre-registered run is admitted. Choosing the best of several repeated test runs
   is test-set selection; repeats are reported as repeats.
8. Ledgers. Budget notes, receipts and caps were written before spending and count every attempt,
   including aborted ones.

## Cache reuse

Reuse cached scores or ranks only when every scientific dependency is unchanged:

| Dependency | Examples |
|---|---|
| Data | Release, preprocessing, split, event mapping |
| Units | Cohort, targets, candidate lists |
| Inputs | Evidence, rendering, prompt, time boundary |
| Model | Weights or returned model id |
| Code | Scoring and parsing code hashes |
| Selection | Selected settings, selection objective, refit stage |

A change to any of them reruns the affected part. Evaluating more units or a larger candidate set with an
unchanged model does not require retraining, but it does require new inference for the new inputs.

## Difference classes

| Class | Meaning | Consequence |
|---|---|---|
| Authorized adaptation | A data, evaluation or runtime adapter the owner approved | Admit; cite the authorization |
| Analysis variant | A valid run that answers a different or narrower question | Label analysis-only; never replaces the main row |
| Execution defect | The run did not do what the contract says | Rerun the affected units |
| Method failure | The method produced no valid answer by design | Count in the denominator |
| Unresolved discrepancy | Cause not determined | Keep pending; raise with the owner |

## Status labels

| Label | Where it may appear |
|---|---|
| Pending | Internal records only |
| Admitted for a named claim | Result table, pages, paper, for that claim |
| Analysis-only | Analysis documents and the appendix, labelled |
| Superseded | Exceptions archive only |

## Supersession

When a protocol or boundary change, or a documented defect, replaces rows:

1. Run and admit the replacement first; excluded rows stay excluded while the replacement is pending.
2. Move the old rows out of active tables into the exceptions archive. Never delete them, and never
   archive a row because its score is poor.
3. Record per row set: old run, replacement run, reason, original values, configuration and artifact
   paths. Keep working references when raw artifacts move.
4. Valid ablations and valid negative results stay in their comparison.

## Synchronization

One change updates together: the main result table, every derived projection, the report or analysis,
the plan, every published page (rebuilt from the newest committed copy), and the project's status,
tracker and handover records. Check the row projections against the main table before publishing.

## Generic cases

- Rows from an earlier time boundary stayed in a comparison next to rows under the corrected boundary
  until they were moved to the exceptions archive with their original values.
- The best of three test runs was admitted and later reverted to the first pre-registered run.
- A page showed numbers that had not passed admission; the owner asked for them to be removed.
