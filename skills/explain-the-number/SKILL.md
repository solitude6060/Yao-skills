---
name: explain-the-number
description: Use before measuring, reporting or acting on a measured number — a speedup, regression, throughput, latency, benchmark or evaluation metric — to name what limits it and rule out that it measured something other than the intended work.
license: MIT
---

# Explain the Number

Adapted from pstack `principle-explain-the-number` and `benchmark-checklist` by Lauren Tan
(MIT, `cursor/plugins` at `1ba91fc`; see `LICENSE`). A number is not a result until you can
say what bounds it and why it is not measuring something else.

## Before the run

- **Write the decision first.** State the sentence you expect to ship ("training step is
  1.8x faster with 8 threads on the 1M-row set"; "Recall@20 improves by 0.012 over SASRec")
  and the result that would change a decision, as a direction against a named comparison.
  Declare a margin (the smallest effect that would matter) only for a claim of no
  difference. Name the noise floor, the comparison design (independent runs or paired by
  seed, user or input) and the evidence stage. Stop when the uncertainty of the difference
  under that design exceeds the expected effect.
- **Read the measurement code.** Note what it times, counts, averages and ignores.
- **Check the machine.** `uptime`, `nproc`, `nvidia-smi` when a GPU is involved. If something
  else is running and cannot be stopped, interleave the sides and say so. Compare latencies
  only on one device; otherwise remeasure both sides there.

## The four obligations

1. **Ask "why not double?"** For a performance number, name the resource or code path that
   bounds the result: a core, a lock, memory bandwidth, the disk, the network, the GPU, the
   data loader, or the load generator. Get it from a profile or system counters taken during
   a run, then map it to source. A guess from reading the code is not a limiter. If you
   cannot say why the number is not twice as good, you do not know what you measured. For an
   evaluation metric, name what bounds the score instead: data coverage (for example items
   absent from training), the metric's ceiling under the protocol, candidate-set size, label
   noise, or the protocol itself. Profilers do not answer this. If the mechanism is not
   established, report the measured result and the unexplained bound separately.
2. **List what else the number could measure, and rule out each with evidence.** Usual
   suspects: errors or skipped work, cached results, code that never ran, an untuned side,
   noise, a component too small to matter end to end. For evaluation metrics add: leakage
   across the split, a different candidate set or metric definition between sides, a
   baseline run on defaults, a single seed, runs that did not complete the task, and a gap
   seen on only one model or dataset (say so if it is), and ask whether the scenario
   matters.
3. **Show it reproduces.** Performance: at least five alternating runs per side
   (A, B, A, B), median and range. Evaluation has two stages.
   Screening: one run, point estimates or paired differences, no intervals; it may choose
   the next experiment but cannot support a robustness or superiority claim. Confirmatory,
   for final claims: the uncertainty of the paired difference over the shared test units
   (for example a per-user bootstrap), plus several seeds or repeats for a method with
   training or decoding randomness, or a claim scoped to one training run. Judge the
   difference by its own uncertainty, not by each side's spread. Report no measurable
   difference only when the whole interval lies inside the margin declared before the run; an interval that includes zero otherwise means inconclusive: no
   significant difference at this sample size. Determinism is observed under a stated
   runtime, never assumed.
4. **Keep the evidence with the number.** Record the exact result row (method,
   configuration, cohort, filters; the admitted row, never the best of several), run count,
   spread, limiter, command, commit and data version.

Performance numbers: answer the seven questions in `references/benchmark-checklist.md`.
Recommender metrics: apply `recsys-evaluation`. A number that supports a claim also passes
the project's result admission (`experiment-contract`).

## Report

- Lead with the verdict: faster, slower, better, worse, no measurable difference, or
  inconclusive; label a screening result as one run.
- Give the number with unit, run or seed count, range, and limiter, for example
  "p50 41 ms → 33 ms, median of 7 runs per side, range 32–35 ms, bound by JSON parsing on
  one core".
- Call a verdict inconclusive when a side ran untuned or errors were not counted; for
  performance, also when the limiter is unnamed or the work was not confirmed; for evaluation,
  when the protocol differs between sides, runs did not complete, or a confirmatory claim
  lacks the difference's uncertainty. Name the gap.

A ballpark or screening run still needs proof that it did not error and the work happened;
if it looks wrong, do the full check.

## Signs you skipped this

- A run started without the result that would change a decision.
- A reported number has no run count, or a claim lacks the uncertainty its stage requires;
  a performance number has no named limiter; an evaluation number has neither a named score
  bound nor a statement that the bound is unexplained.
- The time saved exceeds the time the changed piece took, or a metric gain exceeds what the
  changed component can affect.

Distinct from `first-principles`, which re-derives an assumption before acting; this skill
vets a measurement before trusting it.
