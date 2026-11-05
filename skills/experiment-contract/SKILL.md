---
name: experiment-contract
description: Use before launching an experiment, while it runs, and before its result enters a table, page or paper, to check code, data, configuration, model identity and execution against the agreed contract, classify failures, and admit, label or supersede the result.
argument-hint: "<preflight | execution | admission> <plan, run directory or result rows | empty>"
---

# Experiment Contract

The contract is the agreed specification of a run: the question, data, code, model, readout, and what
counts as its result. Invalid results often come from runs that differed from it unnoticed: another model
behind the same name, a changed scoring script, a best-of-several run admitted. Compare the contract with
what actually ran before launch, during the run and before admission.

Chinese: [SKILL.zh.md](SKILL.zh.md). Procedures: [preflight](references/preflight.md),
[execution](references/execution-integrity.md), [admission](references/admission-and-supersession.md),
[run identity](references/run-identity.md).

## When to use

- Before a batch, a costly rerun, or the first run of a new model, dataset or condition.
- While queues run unattended, and after any change to inputs, prompts, boundaries, code or a hosted model.
- Before a number enters the result table, a published page or the paper.

Not for: experiment design ([experiment-planning](../experiment-planning/SKILL.md)); independent re-checks
after major work ([research-verification](../research-verification/SKILL.md)); recommender split, candidate
and baseline rules ([recsys-evaluation](../recsys-evaluation/SKILL.md)).

## 1. Preflight: before launch

1. Contract fields. Per run: research question, cohorts (development, reporting, calibration), candidates,
   inputs, readouts, seeds, evidence stage (screening or confirmatory), selection objective, retry rounds,
   cost fields. A missing field means the run is not ready.
2. Identity pinning. Model revision, or for a hosted model the requested and the returned model id;
   dataset, candidate and code hashes; hashes of every source file the run imports, including adapters and
   scoring scripts. An endpoint alias is not a model identity.
3. Smoke run. The real configuration at full size (largest candidate set, longest input) on real data for
   a few units: memory, ports, parsing, output paths, cost fields written.
4. Parity. Compared models receive identical inputs and readouts: per-unit input hashes, and token counts
   as a quick check.
5. Rerun map. For any change to inputs, prompts or boundaries, list the runs to rerun, or write why none is
   needed.
6. Approved specification. For a costly rerun the owner confirms the full specification, then it launches
   once. Parts the decision cannot affect may run meanwhile.

## 2. Execution: while it runs

- A running script and its live inputs are immutable. Never edit a running shell script (the shell has
  read ahead) or extract files over inputs a job reads. Stage changes, stop the queue, relaunch the rest.
- Write a pid file at launch and wait on it (`kill -0` plus process state), never on a pattern match such
  as `pgrep -f`, which can match the waiting command itself. A zombie process has finished.
- Before leaving a queue unattended, arm a watchdog that fires on an idle accelerator with no queue
  process, a step much shorter than expected, a non-zero exit, or a repeating failure. Fix each cause.
- Retries are declared and bounded; then stop and diagnose. Never skip a mismatch to keep a queue moving.
- Report progress from real output and process state, never from a launch command's exit status.

## 3. Admission: before a result enters a table

| Check | Rule |
|---|---|
| Failures | Execution failures (out of memory, server error, crash, timeout, missing file, port conflict) rerun until they succeed, attempts and cause recorded, never reported. Method failures (invalid output, no ranking by design) stay in the denominator with utility zero and are counted. Over-limit inputs: apply the declared truncation rule; a unit still over the limit is counted and kept in the denominator with utility zero, or all methods report the common units; never dropped for one method only. |
| Cost | Wall time, latency median and p95, peak memory, device; model-calling runs add calls, tokens, API cost; trained models record inference time per unit. |
| Recomputation | Aggregates recomputed from per-unit files with the exact row filters. |
| Identity | Returned model id, source hashes and each derived row's checkpoint match the main table. |
| Semantics | Selection objective and request semantics match the contract and the label. |
| Run choice | The first pre-registered run is admitted; choosing among test runs is test-set selection. |
| Cache reuse | Only when every scientific dependency (data, split, candidates, inputs, model, code, selection settings) is unchanged. |
| Records | Ledgers written before spending; every attempt counted. |

Classify each difference between contract and run: authorized adaptation (admit, record the
authorization), analysis variant (label analysis-only, never the main row), execution defect (rerun the
affected units), method failure (keep in the denominator, report the count), unresolved discrepancy (keep
pending, raise it with the owner).

Status labels: pending, admitted for a named claim, analysis-only, superseded. Pending numbers never appear
in pages or the paper. A protocol or boundary change supersedes rows explicitly: move them to an exceptions
archive with reason, replacement and original values; never delete. One change synchronizes the result
table, its projections, reports, plan, published pages and project records.

## Output

Write the preflight and admission records next to the run directory, and an exceptions entry per
superseded row. Report to the owner in the project's chat language, one line per run: status and open
discrepancies. Admitted rows go on to [research-verification](../research-verification/SKILL.md).
