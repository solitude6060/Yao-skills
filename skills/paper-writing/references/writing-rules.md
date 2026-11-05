# Writing rules with examples

Rules collected from an author's corrections on full-paper drafts, from advisor feedback and from a
pre-submission review. Each rule names the failure it prevents. Add a rule here in the same change whenever the
author gives a new one.

## Structure

| Rule | Prevents |
|---|---|
| The introduction asks one main question and two or three sub-questions; the conclusion answers them in the same order and wording. | A paper that reports results but never says what they answer. |
| Every section opens with the purpose or the evidence it serves, never a self-posed question, and ends with its answer as the plain last sentence, not in bold (check how strong papers at the target venue write results paragraphs: few open with a question or set the finding in bold). | Sections that read as lists of numbers, or as a dialogue with the author. |
| Each point runs reason, description, analysis, conclusion. | Description without analysis ("only describes, never concludes"). |
| At most two or three highlights in the abstract and introduction; secondary findings become evidence under them. | Several claims of equal weight that dilute each other. |
| The abstract lists the contributions explicitly and states the main result in words; at most one or two numbers, each naming the comparison or dataset it applies to (check the abstracts of strong papers at the target venue). | An abstract that narrates the method and leaves the reader to guess the contribution, or one that reads as a result table. |
| Contributions map one-to-one to sections, and the mapping is stated. | Contributions that no section supports. |

## Sentences

| Rule | Example of the fix |
|---|---|
| Short sentences; one claim per sentence. | Split a sentence that carries a result, its condition and its caveat into two or three. |
| Few parentheses. Move parenthetical details to a table, a footnote or the appendix. | "(first 1,000 users, 99 sampled negatives, seed 0)" belongs in the table caption once, not in every sentence. |
| No dashes as sentence connectors. Number-range dashes are fine. | Replace "X — which Y — Z" with two sentences. |
| Standard terms; no coined phrases for concepts that have a name. | "truncation", not "over-length". |
| No metaphors and no personification in technical statements. | "The interval overlaps the baseline", not "the error bar still covers the baseline". |
| No "it is X, not Y" contrasts; state the observation. | "All three checks fall within the noise range." |
| No self-praise adjectives (remarkable, superior, novel paradigm). Confident claims are fine when the number supports them. | "exceeds every trained baseline by at least 5%", not "remarkably outperforms". |
| A cause that is not determined never appears in the paper: resolve the cause, or omit the statement and keep the observation in the appendix. Internal records (logs, reports) write "cause not determined", and their later text adds no speculative cause. | Delete "the cause is not determined" from a results paragraph; the observation moves to an appendix table without a cause sentence. |
| Academic and professional register, not an engineering log; not stiff either. | Remove run identifiers, file names and dates from the body. |

## Numbers

| Rule | Prevents |
|---|---|
| One number format throughout: absolute difference, relative change in parentheses, e.g. +0.030 (+6.0%). The abstract may keep only relative changes. | Readers converting between formats. |
| The text cites the one or two numbers that carry the point; the rest stay in the table. | Mechanical recitation of every cell. |
| Fixed decimals per metric (three for NDCG and HR in most recommender papers). A difference quoted in the text equals the difference of the printed cells, or one stated rounding rule covers every quoted difference. | A quoted difference one unit away from the difference of the two printed cells. |
| A difference whose interval includes zero is reported as no significant difference at this sample size, never as "on par" or "outperforms". Equivalence is claimed only when the whole interval lies inside a margin declared before the run (see `explain-the-number`). The interval itself stays in the table or the appendix, not in running text. | "Outperforms" or "on par" on a non-significant difference; an absence of evidence presented as equivalence; prose cluttered with bounds. |
| Every number in the text exists in a table, figure or the appendix, and in the result files. | Orphan numbers that cannot be traced. |

## Claims and evidence

| Rule | Prevents |
|---|---|
| Re-verify every quantified claim (at most, never, all, every, on both) whenever a dataset, model or cohort changes. | A bound that held on old data and fails on new data. |
| A result that depends on the protocol gets one neutral body sentence that names the condition and points to the appendix table; the numbers, intervals and full comparison go to the appendix. The sentence may give the reason for the default protocol, with references to the practice it follows. No bold and no negative conclusion sentence. Deployment limits are written as conditions: "requires faster hardware for sub-second serving", not "exceeds the serving budget and is far slower than trained models". | A caveat that body readers never see, or a body that argues against its own claim. |
| Keep a must-keep list of procedure disclosures: development users and what they were used for, selection rules and the data they read, and the exposure of the evaluated users. Check the list after every rewrite; these sentences may be shortened or moved to the appendix, never removed. | A disclosure deleted in a rewrite and then reported by a reviewer as a concealed procedure. |
| Process claims are literally true. Write what the procedure did ("test targets were never used for selection"), not a broader assurance that a record contradicts ("the test set was never seen", when development users' test targets were inspected). | A false statement about the procedure. |
| Check each headline term against the definition the venue's literature uses, and against the advisor's definition when the advisor will judge the paper; if they differ, define the term in the paper (for example, a method that gives the same output for the same history may be called per-user or history-conditioned rather than personalized when the readers expect user-level parameters). | A definitional objection to the main claim. |
| No untested aside against the method's own components: no comparison phrased against a part the method adds, no aside suggesting that one of its signals has a bias the paper does not test. A measured adverse effect of a component (an ablation in which adding it lowers a metric) is still reported, with its condition and evidence stage. | Self-inflicted objections, or negative evidence left out of the paper. |
| Disclose any selection among repeated runs; better, never choose among runs by test score. | Test-set selection presented as a result. |
| When a dataset is replaced after its results were seen, state the reason that holds independently of the results (for example, timestamps that record rating entry rather than consumption), or keep its results in the appendix. | An objection that datasets were chosen after the fact. |
| Hosted models without public weights are named as such; the main claims rest on reproducible models where possible. | Reproducibility objections against the headline result. |

## Sources of text

| Rule | Prevents |
|---|---|
| Author-approved text (a submitted abstract, a contribution list the author rewrote) is stored as a versioned file. Later edits start from it and never revert it silently. | Approved wording that returns to an older form. |
| Rewrites and reviews by other models are idea sources. Adopt their phrasing only after checking every factual statement against the result files; regenerate every number from the table generator. A reason for an empty cell or a row choice that the result files do not support is never adopted. | Fabricated reasons and wrongly selected rows entering the paper. |
| In a bilingual paper every edit lands in both editions in one change; figure text and captions are in each edition's language; terms match the main table. | Editions that disagree. |

## Figures and tables in the text

| Rule | Prevents |
|---|---|
| Prefer a small table or figure over a paragraph that lists settings or numbers. | Dense enumerative prose. |
| Refer to every float in the text before it appears, and say what to look at. | Floats the reader must interpret alone. |
| Running cells or pending results stay blank without explanation in drafts; never invent a reason for an empty cell. | Unverified statements in captions. |

## Final checks

1. Search the source for every quantified word and every dataset name; re-verify each against the result files.
2. Search for dashes, banned adjectives, metaphors and "not X but Y" constructions.
3. Compile and look at every page: overfull lines, float placement, table widths, figure fonts.
4. Two independent language passes (different model families or people), then the author.
5. Verify every reference: it exists, its metadata are correct, and the cited claim is in the source. A
   reference stays only after the third step (the citation ladder of `research-survey`).
6. Check the must-keep disclosure list against the current text, and every quoted difference against the
   printed cells.
7. In a bilingual paper, compare both editions for the same edits, numbers and terms.
