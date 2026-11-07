# Concurrent work

A preprint that overlaps the study can sharpen the contribution or redirect it by accident. The rule is to
compare it, cite it as contrast and an evaluation caution, and keep the research question under the
project's own decision log.

## When to check

- At each milestone, and again before the abstract and full-paper deadlines.
- When the owner, an advisor or a reviewer names a new paper.
- When a follow-up topic is chosen (closest and concurrent work are a feasibility check in
  `research-ideation`).

Search the preprint servers and venue pages with the study's core terms and every name under which the
method's model class is published; record the queries and the date.

## Comparison table

| Column | Content |
|---|---|
| Work | Citation at step 2 or 3 of the citation ladder |
| Task and setting | What is predicted, from which inputs, under which split |
| Information access | What the method reads at inference and what it was trained on; whether the target is placed in the candidate set |
| Candidate construction and protocol | Full ranking, sampled candidates (how), retrieve-then-rerank |
| Claims | Their headline claims, quoted with location |
| Overlap with this study | Same question, same signals, same model class, same data |
| Difference | What this study does that the work does not, and the reverse |
| Effect on this study | None; a new baseline; a new control; a disclosure; a scope change proposed through the decision log |

## Rules

- A concurrent work never redefines the research question. A proposed change goes to the decision log with
  its evidence and the owner decides.
- Use its protocol as an evaluation caution when it differs in a way that changes scores (for example, a
  target injected into the candidate set), and measure the effect when a claim depends on it.
- Where it overlaps, state the difference in one paragraph of the related-work section.
- Results from its paper are quoted with their protocol; numbers from different protocols are not placed in
  one comparison column.

Generic cases: an early concurrent preprint nearly redirected the study's questions toward its own
reranking setting before the owner asked to keep it as contrast only; two preprints that appeared after
submission were compared in a table, and the comparison produced the likely reviewer questions.

## Reviewer questions and rebuttal link

For each overlapping work, write the questions a reviewer is likely to ask ("how does this differ from X?",
"why not compare with X?") and, for each, the evidence that answers it: an existing table, a sentence, or a
reserve analysis. Reserve analyses that fit within the rebuttal time budget are planned in the review and
rebuttal reference of `paper-argument` ([review-and-rebuttal.md](../../paper-argument/references/review-and-rebuttal.md)).
