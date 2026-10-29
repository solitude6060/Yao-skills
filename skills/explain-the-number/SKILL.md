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
  and the result that would change a decision. Name the noise floor you expect. Stop when the
  run-to-run spread is larger than the effect.
- **Read the measurement code.** Note what it times, counts, averages and ignores.
- **Check the machine.** `uptime`, `nproc`, `nvidia-smi` when a GPU is involved. If something
  else is running and cannot be stopped, interleave the sides and say so.

## The four obligations

1. **Ask "why not double?"** Name the resource or code path that bounds the result: a core,
   a lock, memory bandwidth, the disk, the network, the GPU, the data loader, or the load
   generator. Get it from a profile or system counters taken during a run, then map it to
   source. A guess from reading the code is not a limiter. If you cannot say why the number
   is not twice as good, you do not know what you measured.
2. **List what else the number could measure, and rule out each with evidence.** Usual
   suspects: errors or skipped work, cached results, code that never ran, an untuned side,
   noise, a component too small to matter end to end. For evaluation metrics add: leakage
   across the split, a different candidate set or metric definition between sides, a
   baseline run on defaults, and a single seed.
3. **Show it reproduces.** Performance: at least five alternating runs per side
   (A, B, A, B), median and range. Evaluation: several seeds, mean with spread or an
   interval, and a paired comparison when the sides share test users. A gap smaller than
   the run-to-run spread is no measurable difference.
4. **Keep the evidence with the number.** Record run count, spread, limiter, command,
   commit and data version in the notes, result table or a linked artifact.

For a performance number, answer the seven questions in
`references/benchmark-checklist.md`. For a recommender metric, apply `recsys-evaluation`
for split, candidates and baselines. For any number that will support a claim, the
project's own result-admission rules still apply.

## Report

- Lead with the verdict: faster, slower, better, worse, no measurable difference, or
  inconclusive.
- Give the number with unit, run or seed count, range, and limiter, for example
  "p50 41 ms → 33 ms, median of 7 runs per side, range 32–35 ms, bound by JSON parsing on
  one core".
- Call it inconclusive when the limiter is unnamed, a side ran untuned, errors were not
  counted, or you could not confirm the work happened. Name the gap.

For a quick ballpark the user asked for, one run is enough; still confirm it did not error
and the work happened, and say it is one run. A choice between options is never a ballpark.

## Signs you skipped this

- A run started without the result that would change a decision.
- A reported number has no run count, no spread, or no named limiter.
- The time saved exceeds the time the changed piece took, or a metric gain exceeds what the
  changed component can affect.

Distinct from `first-principles`, which re-derives an assumption before acting; this skill
vets a measurement before trusting it.
