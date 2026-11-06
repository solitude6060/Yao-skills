---
name: experiment-planning
description: "Use before implementing, launching or expanding an experiment batch: question per experiment, controls, full matrix and tracker, evidence stage, cohorts and exposure, information parity, official baselines, budget and the decision each result can change."
argument-hint: "<plan file | research question | batch to expand | empty>"
---

# Experiment Planning: cards, controls, matrix, cohorts, budget

Most reruns come from batches that answered no stated question, compared methods that saw different
information, or reported on users who had already shaped the method. Plan cards and one tracked matrix
before code or launch.

Chinese: [SKILL.zh.md](SKILL.zh.md). References: [experiment-card.md](references/experiment-card.md),
[control-design.md](references/control-design.md), [cohorts-and-exposure.md](references/cohorts-and-exposure.md),
[budget-and-throughput.md](references/budget-and-throughput.md).

## When to use

- Before implementing a variant, baseline or analysis, or launching a batch that costs hours or money.
- Before expanding users, candidate sets, datasets or models; after a protocol change, review finding or
  failed gate.

Not for: recommender split, candidate and metric rules (`recsys-evaluation`); checking a run against its
contract and admitting results ([../experiment-contract/SKILL.md](../experiment-contract/SKILL.md)); choosing
the research direction ([../research-ideation/SKILL.md](../research-ideation/SKILL.md)).

## 1. One card per experiment

Write for a reader outside the project; explain every label.

| Field | Content |
|---|---|
| Question | The research question it serves, by name |
| Purpose | What is unknown now and why it matters |
| Intervention | The one thing that changes |
| Nearest simpler control | The cheapest alternative that could produce the same result |
| Inputs, outputs | Data, cohort, candidates, model, readout; per-unit files and metrics |
| Expected reading | A direction against a named comparison, and the result that would contradict the claim |
| Cost | Time, memory, money; measured or marked as an estimate |
| Decision it changes | The next action for each outcome |

A card with no question or decision is dropped.

## 2. Controls for information as well as architecture

- A gain that comes with extra information does not show a better model. Plan model-only,
  auxiliary-signal-only and matched-information controls (both sides get the same evidence) now.
- System attribution (the method beats a baseline) differs from component attribution (this part causes the
  gain), which needs removing or replacing that part.
- A fixed-parameter ablation (remove a part, keep the other settings) and a reselected ablation (remove it,
  select again) answer different questions; plan the one the claim needs and label it.
- Write the boundary of auxiliary signals as an access rule (for example, counting statistics allowed,
  another fitted model's scores not).

## 3. One matrix with a tracker

List every cell once: method × dataset × condition × cohort. The tracker marks each cell done, running or
pending, with per-method coverage, so a skipped condition is visible. Grow in a ladder: few users before
more, small candidate sets before larger, a complete prototype with few models before more models.

## 4. Evidence stage and readings

| Stage | Runs and statistics | It can support |
|---|---|---|
| Screening (iteration) | One run; point estimates or paired differences; no intervals | Choosing the next experiment; a labelled screening row; no robustness or superiority claim |
| Confirmatory (final claims) | Paired-difference uncertainty over the shared test units (for example a per-user bootstrap), plus several seeds or repeats for methods with training or decoding randomness, or a claim scoped to one training run | Claims in the paper |

A per-unit bootstrap covers unit sampling only, not seed variance. Determinism is observed under a stated
runtime, never assumed. Set no arbitrary numeric success bar: a gate is a comparison against a named
baseline on validation data, in plain words. Declare a margin, before the run, only for an equivalence claim.

## 5. Cohorts, exposure, information parity

- Reserve development, reporting and, when needed, selection cohorts before the first result. Choose
  variants on development users; select settings on validation targets (the reporting users' only
  under leave-one-out); score reporting users' test targets once. An expanded sample contains the users
  already evaluated; report the added users separately.
- Before calling a cohort held out, scan its exposure: every earlier run, analysis and sibling project that
  read these users' targets.
- Decide in the protocol what each method may read at training and at inference. A high-severity
  protocol finding is answered by an experiment before claims freeze, not by moving text.

## 6. Baselines

Choose baselines per family. Run each from its official source and configuration, label any relaxed variant
beside it, and refit only if the source does. Define the method class operationally: what is never updated,
what is selected on validation data, how long selection takes.

## 7. Budget and launch

- Estimate runtime from measured throughput on the real configuration; run jobs in parallel when memory allows.
- Record cost per category: preparation, selection, inference, retries, refresh.
- Keep a low-cost trial tier with a written promotion rule; its results never enter the
  result table. Rank work by decision value: a run whose success would replace a whole matrix goes first.
- Before the batch, check on real inputs: input length, memory at the largest size, readout, parsing.
- For a costly rerun the owner confirms the full specification, then it launches once; safe independent
  parts run meanwhile.

## Output

Cards, matrix and tracker go in the project's plan file; the confirmed specification goes to
`experiment-contract` for preflight. Report to the owner in the project's chat language.
