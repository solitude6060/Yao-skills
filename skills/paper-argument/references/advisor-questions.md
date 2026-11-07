# Advisor questions and author adjustments

Collected from advisor and colleague feedback on a full-paper draft, from the author's later corrections and
from a pre-submission review. They refine the four parts of SKILL.md.

## The three questions per component (advisor)

For every component of a simple method (for example: interaction statistics, a frozen model's score, a weighted
sum that combines them), answer three questions:

1. **What does it represent?** Its physical meaning: what quantity it estimates and under which assumption
   (for example, a log count of transitions estimates how often an item follows another).
2. **Why was it chosen?** The alternatives and the property that made this one preferable (one request instead of
   many, no parsing, no fine-tuning, a closed form).
3. **Why does it work?** The mechanism, supported in this order of preference: a derivation or established
   principle, an intervention (remove, replace, permute, swap), a measured correlation, and only then case studies.

Each answer has three layers: the principle, the literature that uses the same principle, and the paper's own
evidence. A literature citation enters the paper only after its quoted claim was checked in the source.

## Closed loop (advisor and author)

- The introduction states the main question and the sub-questions; each analysis subsection answers one
  sub-question; the conclusion answers them in the same order and words.
- Each results or analysis paragraph runs purpose or evidence pointer, design, table or figure, observation, mechanism,
  and a plain closing sentence that answers the sub-question; it never opens with a self-posed question.
- Limitations scope named claims; they do not introduce new results.

## Highlights and presentation (colleague and author)

- At most two selling points. Secondary findings (long-tail behaviour, popularity sensitivity) become evidence
  under one of them, not separate claims.
- The abstract lists the contributions explicitly ("Our contributions are twofold/threefold: (1) ...");
  match its shape, contribution list and number count to how strong papers at the target venue write their
  abstracts.
- One number format in the whole paper: absolute difference with the relative change in parentheses.
- At least one case study, drawn by a rule fixed before looking at the cases; state that the cases do not
  represent their strata.
- Tables that are hard to read are redesigned (relative changes, fewer rows, small changes collapsed into a
  note), not explained in longer captions.

## Evidence discipline (author)

- A dataset swap is a rewrite: every quantified claim is re-verified on the new data, and conclusions that came
  from the removed dataset are deleted rather than relabelled.
- An increment attributed to "the model's own evidence" must come from an input that carries no cross-user
  statistics; if the selected input mixes sources, report a clean variant beside it.
- Robustness results that depend on the protocol (a different negative-sampling rule, a different time anchor)
  get one neutral body sentence that names the condition, gives the reason the default protocol is the
  realistic one with references to the practice it follows, may state the information the baselines see
  that the method does not, and points to the appendix table. The numbers, intervals and full comparison go
  to the appendix. No bold and no negative conclusion sentence (`paper-writing`, principle 6).
- When results are pre-committed (datasets added after a written commitment), every pre-committed result enters
  the comparison, favourable or not.

## Definitions, model class and nearest method (author and reviewers)

- **Definition check for headline terms.** For each term in the title, abstract and research questions
  (for example "personalized", "training-free", "generalization"), check the term against the definition
  the venue's literature uses, and against the advisor's definition when the advisor will judge the paper;
  if they differ, define the term in the paper (for example, a method that gives the same output for the
  same history may be called per-user or history-conditioned rather than personalized when the readers
  expect user-level parameters). Use the chosen term and definition in every section and in each language
  edition.
- **"Why this model class" table.** When the method depends on a model class (for example a frozen model
  that scores declared options without generating text), answer why this class with one row per claimed
  benefit:

  | Claimed benefit | Principle | Control that isolates it | Analysis | Status |
  |---|---|---|---|---|
  | <benefit> | <why it should hold> | <same pipeline with another model class> | <measurement> | exists, planned, missing |

  A benefit without a control is written as a design property, not as a finding. A reviewer objection that
  the class adds little over its base model is answered by the control column.
- **Nearest-method difference paragraph.** Name the closest prior method and state in one paragraph what
  differs: the information used, what is trained or fitted, how the parts are combined, and what the method
  can do that the prior one cannot. Place it in related work or at the method's first description.
- **Sources for weighting and combination choices.** Every weighting, normalization or combination rule cites
  a conceptual source that uses the same principle before it is written as new; a known method is preferred
  over an invented one. The cited claim is checked in the source.
