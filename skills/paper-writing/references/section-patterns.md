# Section patterns from exemplar papers

A writing study read twelve recommender and AI papers in full and measured each section. The patterns below
are paraphrased; section numbers point to the arXiv versions read. Use them to set budgets and to decide what a section
contains; they describe these papers, not a law.

Exemplars: SASRec (Kang and McAuley, ICDM 2018, arXiv 1808.09781), LightGCN (He et al., SIGIR 2020, 2002.02126), EASE
(Steck, WWW 2019, 1905.03375), kNN-LM (Khandelwal et al., ICLR 2020, 1911.00172), LLMRank (Hou et al., ECIR 2024,
2305.08845), TALLRec (Bao et al., RecSys 2023, 2305.00447), gSASRec (Petrov and Macdonald, RecSys 2023, 2308.07192), HSTU
(Zhai et al., ICML 2024, 2402.17152), NCF versus MF revisited (Rendle et al., RecSys 2020, 2005.09683), "Are we really making
much progress?" (Ferrari Dacrema et al., RecSys 2019, 1907.06902), sampled metrics (Krichene and Rendle, KDD 2020), RLMRec
(Ren et al., WWW 2024, 2310.15950).

## Proportions measured

| Part | Range in the exemplars | Note |
|---|---|---|
| Abstract | about 170 to 240 words (EASE 70) | at most one headline number; the classic ones give none |
| Introduction | 6% to 11% of body prose in the classic four; up to 15% to 17% in two empirical papers | five to eight short paragraphs |
| Method | 16% to 38% | the model is analysed inside the method (reductions to known models, readings of the solution) |
| Setup | 11% to 20% | the protocol fits in one paragraph when it is borrowed |
| Results plus analysis | 15% to 40% | analysis alone 7% to 22% in the classic four |
| Conclusion | about 100 to 380 words | usually no result numbers |
| Captions | median 15 to 35 words | long captions only for overview figures or when they state a finding |
| Numbers in results prose | 2.1 to 6.3 per 100 words (all numbers) in recent papers; 0.3 to 0.9 decimals or percentages per 100 words in the classic four | prose interprets; tables carry the values |
| Body floats | 4 to 11 | one master table plus one float per question |

## Section by section

**Abstract.** Problem, idea, one result in words or one number, one implication. Contribution lists are rare in abstracts
(none of the classic four); when a venue or co-author wants them, keep one number per item.

**Introduction.** Problem, limits of the existing paradigms, the key idea, the result in words, what the analyses show.
Contribution bullets, when present, are short and carry no numbers (LightGCN §1, three bullets) or are numbered implications
with section pointers (EASE §1). A strong closed loop can rest on one hypothesis sentence stated early and answered in the
analysis and the conclusion (kNN-LM §1, §6, §8). Questions are stated once: as a list in the introduction (LLMRank,
Ferrari Dacrema) or at the head of the experiments (SASRec §IV, TALLRec, gSASRec, Krichene and Rendle §6, RLMRec §4).

**Related work.** Grouped by viewpoint, each group ending with one contrast sentence (EASE §4). Several papers place it after
the results so the technical content starts early (LightGCN §5, kNN-LM §7, Rendle et al.).

**Method.** Each component with its design reason. Analysis of the model belongs here: relations to known models (SASRec
§III-G, LightGCN §3.2) or a reading of the solution (EASE §3.2). Options tried and dropped get one or two sentences.

**Setup.** Borrow a known protocol and say so in one sentence; grids, final hyperparameters and dataset statistics go to the
appendix (Rendle et al. §3.1 and Appendix A; RLMRec §4.1). Baselines in named groups, one line each, plus a short note on
omitted baselines (SASRec §IV-B).

**Results.** Questions named at the start of each subsection; subsection titles can carry the question (LLMRank, gSASRec) or
the finding (Rendle et al. §4). Order of a results paragraph: the pattern across baselines, the margin, one likely reason,
a pointer to the analysis that tests it (SASRec §IV-E). One master table holds all methods and the main metrics; secondary
analyses use one metric or one dataset (SASRec Table IV, gSASRec §6.2.3). Significance is a mark inside the main table
(TALLRec, gSASRec) or one stated threshold (HSTU); no exemplar adds a second body table that restates the main comparison as
paired differences.

**Analysis.** Each probe opens with its question or purpose, runs one test and ends with one implication; the section closes
with a short numbered answer to the hypothesis (kNN-LM §6). An explanatory quantity gets one small table or figure (LightGCN
§4.4.3, EASE §5.2).

**Robustness and secondary checks.** One sentence with the exception named (Rendle et al. §3.3; Ferrari Dacrema §3.3 and §3.4),
or one small figure plus two bullets (RLMRec §4.4). The full numbers go to the appendix.

**Limitations and conclusion.** The conclusion restates the answer in words, without result numbers, in about 100 to 150
words; future work in one or two sentences. Limits take one or two sentences or one discussion paragraph inside the results.

**Appendix.** Holds reproduction and audit material: optimizer equations, grids, final values, prompts with examples, dataset
statistics, further instances of a body point. Three of the four classic papers have no appendix at all and omit repeated
results with a one-clause note.

## Captions

Two styles work: a label plus definitions of the marks (SASRec, LightGCN, LLMRank, RLMRec; up to about 35 words), or a title
followed by the finding (kNN-LM, nine of thirteen body captions). Define each mark once in the paper.

## Repetition

Each number is printed once. Anchor rows (the best baseline repeated as the reference of a second table) are the only
accepted repetition in the body (LightGCN Tables 4 and 5, LLMRank Table 3). One quantity has one name and one value; when the
same quantity appears for several cohorts, report the confirmation or full cohort in the body and the others in the appendix.
