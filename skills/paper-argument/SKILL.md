---
name: paper-argument
description: Use when a paper has results but a thin argument (before an advisor meeting or submission, or when a reviewer asks why it works). Organizes motivation, highlights, method and proof, and plans the mechanism evidence for the proof.
argument-hint: "<paper path | claim to defend | advisor notes | empty>"
---

# Paper Argument: motivation, highlights, method, proof

A result says that a method works. A paper must also say why it works, what each part contributes, and why
the design is reasonable. This skill organizes that argument in the four parts an advisor uses to take a
paper apart, and plans the evidence for the fourth part, which is usually missing.

Chinese explanation: [SKILL.zh.md](SKILL.zh.md). Analysis precedents with sources: [references/analysis-catalog.md](references/analysis-catalog.md). Evidence ladder, reviewer objections and pitfalls: [references/evidence-ladder.md](references/evidence-ladder.md). Advisor questions and author adjustments: [references/advisor-questions.md](references/advisor-questions.md).

## When to use

- Results exist, the method is simple (a weighted sum, a frozen model plus statistics, a retrieval mixture), and
  the text explains what was done but not why it works.
- Before an advisor meeting or a submission; after an advisor or reviewer asks "is this reasonable?",
  "where is the personalization?", "what does this component add?".
- When planning analyses: to decide which analyses support which claim, and what goes into the body.

Not for: protocol validity of the experiments themselves (use `recsys-evaluation`), or checking an inherited
assumption (use `first-principles`). Use them first if the numbers themselves are in doubt.

## The four parts

Write one short paragraph per part, then the argument map (below). Each part names the evidence that supports it.

1. **Motivation.** Cost and deployment setting lead to a pain point; the pain point leads to the question.
   Define the key terms precisely (for a "training-free" method: what is never updated, what is still selected on
   validation data, how long selection takes). A generalization claim needs a frozen-transfer test; separately
   selected settings per domain show adaptability, not generalization.
2. **Highlights.** At most two or three things a reader should remember; the abstract lists them as
   contributions with one number each. Each highlight points to one result or one analysis. A highlight with no evidence is removed or turned into future work.
3. **Method.** For each component: the information it carries, its data source and time scale, and what it
   adds that the others lack ("what I add"). Classify components on two axes, global (population) versus local
   (anchored on the user or query), and static versus dynamic (time-decayed, order-dependent). State which
   quantities are per user (contributions, gates) and which are global (weights).
4. **Proof.** Why it works and the mechanism, beyond the metric. Plan it with the evidence ladder,
   then check it from the reviewer's side. Ladder: utility, necessity, information, decomposition, balance,
   complementarity, conditions, stability, cases ([references/evidence-ladder.md](references/evidence-ladder.md)).
   Climb only as far as the claims need; label each analysis as an intervention or a correlation. For each
   component answer what it represents, why it was chosen and why it works, each with the principle, the
   literature and the paper's own evidence ([references/advisor-questions.md](references/advisor-questions.md)).

## Procedure

1. Read the paper and the advisor's notes. Transcribe handwritten notes with an explicit reading per line and mark
   uncertain words; ask only where two readings lead to different work.
2. Write the four parts (one paragraph each) and the **argument map**: claim → evidence → type (intervention,
   correlation, descriptive) → status (exists, planned, missing) → location (body, appendix).
3. Write a shared brief (method formula, component table with source and time scale, current results, data and
   compute available, project rules). Ask two or three independent advisors, from different model families or
   different people, for an analysis program and the five strongest reviewer objections. Advisors stay read-only;
   check afterwards that no files changed. Treat their expected numbers as guesses, never as pre-declared readings.
4. Build the data slice every analysis needs first (for additive scores: one row per query and candidate with each
   raw term, gate, weight, contribution, score and rank), with an exact-reproduction check against the already
   reported results as a stop condition.
5. Pre-declare the reading of each analysis (expected outcome and the outcome that would contradict the claim)
   before computing; run the cheap CPU analyses first and the small GPU interventions in parallel.
6. Report every reading as held, partly held or not held, with numbers and sources. A reading that failed is not
   promoted into a claim.
7. Allocate the paper: the body gets at most one figure (usually the interpolation curve plus one intervention
   panel) and one small table (decomposition shares, rescues and losses); everything else goes to the appendix.
   Write the text with `paper-writing` (closed loop, body versus appendix, tables).

Before submission, answer each objection in the reviewer table of [references/evidence-ladder.md](references/evidence-ladder.md)
with an analysis, or narrow the claim; check its pitfalls list.

## Output

Write to the project's planning folder: the four-part summary, the argument map, the analysis cards with
pre-declared readings, and after the runs a results note with each reading's outcome. Report to the author in the
language of the conversation.
