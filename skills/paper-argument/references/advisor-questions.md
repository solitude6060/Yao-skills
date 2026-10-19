# Advisor questions and author adjustments

Collected from advisor and colleague feedback on a full-paper draft and from the author's later corrections.
They refine the four parts of SKILL.md.

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
- Each results or analysis paragraph runs question, design, table or figure, observation, mechanism, take-away.
- Limitations scope named claims; they do not introduce new results.

## Highlights and presentation (colleague and author)

- At most two selling points. Secondary findings (long-tail behaviour, popularity sensitivity) become evidence
  under one of them, not separate claims.
- The abstract lists the contributions explicitly ("Our contributions are twofold/threefold: (1) ..."), each
  with one number.
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
- Robustness results that change the headline (a different negative-sampling rule, a different time anchor)
  are summarized in the body in one sentence with numbers, together with the reason the default protocol is the
  realistic one and with the information the baselines see that the method does not.
- When results are pre-committed (datasets added after a written commitment), every pre-committed result enters
  the comparison, favourable or not.
