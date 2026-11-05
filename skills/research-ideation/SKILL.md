---
name: research-ideation
description: "Use when choosing, reshaping or naming a research direction, or starting a follow-up topic: question chain, closest simpler alternative, feasibility on the real data, scope, utility bar, venue fit and a preliminary-study plan with stop conditions."
argument-hint: "<new direction | reframe | follow-up topic | name> <notes or plan path | empty>"
---

# Research Ideation: from a direction to a preliminary study

An idea is ready for experiments when it answers a stated question, names the simpler explanation it must
beat, and has survived cheap checks on the real data. Collecting experiments before that point produces
results without a claim.

Chinese: [SKILL.zh.md](SKILL.zh.md). References: [feasibility-checks.md](references/feasibility-checks.md),
[preliminary-study-template.md](references/preliminary-study-template.md),
[venue-and-schedule.md](references/venue-and-schedule.md).

## When to use

- Choosing or reshaping a direction, or reframing one that has stalled.
- Naming a method or a topic.
- Starting a follow-up topic from a finished study.
- Before committing weeks of work or a paid budget to a topic.

Not for: generic idea scoring (`idea-evaluator` if installed); a paper skeleton (`tech-paper-template` if
installed; `paper-argument`); experiment batches ([experiment-planning](../experiment-planning/SKILL.md)).

## Order of work

1. Direction: where the work goes.
2. The question it answers, in one sentence.
3. The contribution and its novelty against the closest work ([research-survey](../research-survey/SKILL.md)).
4. Only then, the experiments it needs.

Question the inherited task framing before adopting it: why this pipeline stage (for example, reranking a
retriever's list), and could the method do the task directly?

## The idea as a mechanism

- State the mechanism and a discriminating prediction: an observation that holds if the mechanism is right
  and fails if a simpler explanation is.
- Name the closest simpler alternative and plan to beat it (for example, late fusion of the same signals
  versus guidance inside the model).
- Keep system-level gain and component attribution apart; a whole-method score does not show what one part
  contributed.
- Name the idea by what it does. A narrow label (calling a family of memory signals "calibration") narrows
  the plan by accident.

## Utility bar and method shape

- The headline needs competitive accuracy against named strong baselines before secondary advantages (cost,
  latency, analysis) can carry the paper.
- When the method runs on pretrained models, state it as a procedure over a model class, with a model
  portfolio: one or two main models, a few size or training variants, one or two closed models.
- Prefer explainable structure (hierarchy, evidence, memory) over unexplained ensembles. Fold every component
  that helped on development or validation data into one method; confirm the folded method once on a
  reporting cohort it did not shape.

## Feasibility on the real data

Before commitment, check on the data the method will use: the needed modality or field exists; the defining
counts hold (how many targets are new or cold under the actual time rule); the obvious variant is not
already saturated; closest and concurrent work are known; code, checkpoints and budget exist. Procedure and
cases: [references/feasibility-checks.md](references/feasibility-checks.md).

## Scope

- One scope per paper: what this paper can claim, and what moves to a second paper or future work.
- Check each proposed addition (dataset, model, condition) against the scope before planning it.
- Budget comparison breadth and mechanism-analysis depth separately.

## Follow-up topics

- Inherit the previous protocol and record only the differences.
- Re-examine each inherited constraint: a predecessor's restriction (for example, no training) belongs to its
  question and binds the new topic only if the new question needs it.
- Build the start document with the handover template of
  [research-lifecycle](../research-lifecycle/references/handover-template.md).

## Venue

Choose from the current call: topic fit, contribution type, evidence maturity, dates, and
concurrent-submission rules. A paper under review cannot be submitted elsewhere until its notification; a
venue whose deadline falls before that notification is not a fallback for it. List fallbacks with dates
checked on the official pages ([references/venue-and-schedule.md](references/venue-and-schedule.md)).

## Preliminary-study plan

Write questions, shared rules, stages, and outputs
([references/preliminary-study-template.md](references/preliminary-study-template.md)). Each stage has a
continue or stop condition read on validation data: a comparison against a named baseline, stated in plain
words, never an arbitrary numeric bar. A failed gate is evidence to adjust or stop; never rewrite the gate
after seeing the result.

## Red flags

| Observation | Action |
|---|---|
| Experiments listed before the question is written | Write the question chain first |
| No simpler alternative named | Name it and add it as a control |
| The premise is untested on the real data | Run the feasibility checks first |
| A new dataset or model enters without a scope check | Check it against the paper's scope |
| A gate is reworded after a failed result | Restore the gate; record the failure as evidence |
| A follow-up copies every predecessor restriction | Re-examine each against the new question |

## Output

In the project's plan folder: the question chain, the feasibility record with its script and saved output,
the scope statement, and the preliminary-study plan; the decisions go to the decision log. Report to the owner
in the project's chat language.
