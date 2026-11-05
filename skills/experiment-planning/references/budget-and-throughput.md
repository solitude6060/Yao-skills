# Budget and throughput

Plan cost from measurements, order work by what a result can change, and launch a costly batch once, after
its specification is confirmed. Execution integrity during the run (pid files, watchdogs, immutable inputs)
belongs to `experiment-contract`; paid-API ledgers and shared hardware belong to the compute reference of
`research-lifecycle` ([../../research-lifecycle/references/compute-and-budget.md](../../research-lifecycle/references/compute-and-budget.md)).

## Cost categories

Record each category separately; an efficiency claim names the categories it compares.

| Category | Content | Recurs |
|---|---|---|
| Preparation | Statistics, indexes, embeddings, caches built before serving | Once per data refresh |
| Selection | Search over coefficients, checkpoints or settings on validation data | Once per selection |
| Inference | Per-request computation: calls, tokens, latency, device memory | Every request |
| Retries | Repeated calls after method failures under the declared policy | Per failure |
| Refresh | Rebuilding preparation or selection when the data changes | Per refresh interval |

A latency-only comparison does not support a claim about total cost; state which categories were measured
and on which hardware.

## Runtime from measured throughput

1. Run the real configuration on a small slice of real inputs (the largest candidate set, the longest input).
2. Measure units per hour and peak memory.
3. Divide the planned units by the measured units per hour, then add model loading and final ranking; label
   the result as an estimate until the batch confirms it.
4. Run independent jobs in parallel when the measured memory allows it; declare each job's memory need.

An estimate that comes from scaling a different dataset or input length is marked as such, with the reason
it may be off.

## Minimal real-input capability check

Before the batch, confirm on real inputs that the interface can do what the plan assumes: input length
limits, memory at the largest candidate count, the readout or probability operation the method needs,
parsing of the output, and any per-request limits of the interface (for example images per request as well
as tokens). A generic case: a set-wise readout ran out of memory at the largest candidate count, and every
user in the batch failed after the queue had started.

## Low-cost trial tier and promotion

- Keep a low-cost, wide trial tier (small hardware, few users) for variants that are possible but untested.
- Write the promotion rule before the trials: which observation promotes a variant to the expensive tier,
  and who decides (for example, two independent reviewers agree).
- Trial-tier results choose what to run next; they never enter the result table.
- The tier is distinct from the screening evidence stage (`experiment-planning`, section 4). A one-run result
  on the reporting setup is a screening-stage row: it may be admitted with the label "screening" and
  supports no robustness or superiority claim.

## Decision value

Rank pending runs by what their outcome changes. A run whose success would replace a whole matrix (for
example a larger model that, if better, makes the smaller model's matrix obsolete) goes first. Minor
variants wait while the important ones are untested.

## Launching a costly rerun

1. Write the full specification: cards, matrix cells, inputs, versions, failure policy, cost estimate.
2. The owner confirms it; record the confirmation verbatim with its scope.
3. Launch once. Meanwhile run parts that do not depend on the pending decision.
4. A partial rerun followed by another partial rerun is the failure this procedure prevents.

## Generic cases

- Several partial reruns after a protocol change cost more than one confirmed full rerun would have.
- A long run on minor variants delayed the run whose result would have replaced the whole comparison.
- A runtime estimate scaled linearly from another dataset, with no measured slice of the new inputs, was
  the only basis for reserving a shared accelerator.
