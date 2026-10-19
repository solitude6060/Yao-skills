# Writing rules with examples

Rules collected from an author's corrections on full-paper drafts and from advisor feedback. Each rule
names the failure it prevents. Add a rule here in the same change whenever the author gives a new one.

## Structure

| Rule | Prevents |
|---|---|
| The introduction asks one main question and two or three sub-questions; the conclusion answers them in the same order and wording. | A paper that reports results but never says what they answer. |
| Every section opens with the question it serves and ends with its answer, a one-sentence take-away in bold or as the paragraph's last sentence. | Sections that read as lists of numbers. |
| Each point runs reason, description, analysis, conclusion. | Description without analysis ("only describes, never concludes"). |
| At most two or three highlights in the abstract and introduction; secondary findings become evidence under them. | Several claims of equal weight that dilute each other. |
| The abstract lists the contributions explicitly, each with one number. | An abstract that narrates the method and leaves the reader to guess the contribution. |
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
| Unknown causes are written as "the cause is not determined", and later text does not add a speculative cause. | — |
| Academic and professional register, not an engineering log; not stiff either. | Remove run identifiers, file names and dates from the body. |

## Numbers

| Rule | Prevents |
|---|---|
| One number format throughout: absolute difference, relative change in parentheses, e.g. +0.030 (+6.0%). The abstract may keep only relative changes. | Readers converting between formats. |
| The text cites the one or two numbers that carry the point; the rest stay in the table. | Mechanical recitation of every cell. |
| Fixed decimals per metric (three for NDCG and HR in most recommender papers); percentages from unrounded values. | Rounding disagreements between text and tables. |
| A claim with an interval that includes zero is written as "on par" or "within", with the interval. | "Outperforms" on a non-significant difference. |
| Every number in the text exists in a table, figure or the appendix, and in the result files. | Orphan numbers that cannot be traced. |

## Claims and evidence

| Rule | Prevents |
|---|---|
| Re-verify every quantified claim (at most, never, all, every, on both) whenever a dataset, model or cohort changes. | A bound that held on old data and fails on new data. |
| A load-bearing caveat appears in the body with its numbers; the full evidence goes to the appendix. | A caveat that only appendix readers see. |
| Disclose any selection among repeated runs; better, never choose among runs by test score. | Test-set selection presented as a result. |
| When a dataset is replaced after its results were seen, state the reason that holds independently of the results (for example, timestamps that record rating entry rather than consumption), or keep its results in the appendix. | An objection that datasets were chosen after the fact. |
| Hosted models without public weights are named as such; the main claims rest on reproducible models where possible. | Reproducibility objections against the headline result. |

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
