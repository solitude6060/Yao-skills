# Evidence ladder, reviewer view and pitfalls

Reference for [../SKILL.md](../SKILL.md).

## Evidence ladder for the proof

Climb only as far as the claims need. Interventions outrank correlations; label every analysis as one or the other.

| Step | Question | Standard analysis |
|---|---|---|
| 1 Utility | Does it work? | Main table, paired differences, bootstrap intervals over users |
| 2 Necessity | Is each component needed? | Fixed-weight removal of each term (weights unchanged), next to removal with reselection; per-user better/worse/same |
| 3 Information | What information does a component use? | Input interventions: no input, another matched user's input, truncation (latest k vs earliest k), order reversal; replace a component by a simpler one that carries only one factor (Xu et al. 2023) |
| 4 Decomposition | How much of each decision comes from each part? | For additive scores, the margin of the target over a negative is exactly the sum of per-term differences; report scale-free shares (pairwise contrast primary, standard-deviation share as robustness) and group them by information source |
| 5 Balance | Why this weighting? | Interpolation curve between two parts with the deployed point marked, on validation and test (kNN-LM Fig. 5); per-weight multipliers; width of the plateau |
| 6 Complementarity | Why a sum and not one part? | Hit contingency (both, only A, only B, neither), rescues and losses, oracle rate; relevant versus non-relevant overlap (Lee 1997); separation d per term (Vogt and Cottrell 1999) |
| 7 Conditions | Where does it help? | Stratify by a pre-declared property (item frequency, history length, evidence support); keep post-hoc groups descriptive (kNN-LM rare patterns, Drozdov et al. 2022 similarity bins) |
| 8 Stability | Are the selected settings meaningful? | Selection folds, users never used for selection, alternative candidate samplers; claim stability of effects, not of raw weights |
| 9 Cases | Can a reader follow one decision? | Cases chosen by a rule fixed in advance (for example nearest the median of the positive, zero and negative change strata), failures included, every term's contribution shown |

## Reviewer view (check before submission)

For each objection, name the analysis that answers it, or narrow the claim.

| Objection | Answer |
|---|---|
| "A large grid on few users overfits." | Selection folds, users never used for selection, plateau width; claim the effect is stable, not the weights |
| "The weights are arbitrary scale compensation." | Scale-free contributions and exact margins; never compare raw weights across terms |
| "There is no personalization; it is popularity." | Swap the user's history in the user-anchored terms and in the model input; group shares by source |
| "The model adds an item prior or supplied evidence, not user information." | No-history and matched-other-user interventions; remove injected evidence from the input as a separate condition |
| "The gain is an artifact of the candidate sampler or position." | Repeat the decomposition under another sampler; position or order checks, or state the limit |

## Pitfalls

- Raw weights are not importance: terms have different scales and per-query standardization.
- Weights selected on the same users as the test are optimistic; cite held-out users and folds.
- Tie-breaking can carry a removed component (for example a model's confidence); remove it with the component.
- Visible dates reveal chronology, so reversing the list tests list position only.
- An input that already contains collaborative evidence mixes sources; isolate it before attributing the effect.
- Post-hoc groups (by the held-out answer) are descriptive; no method may see them.
- A component that adds nothing on one dataset is reported as such, with the dataset property that explains the
  difference only if measured.
- Do not write causal language for correlational analyses, and do not coin new terms where a standard one exists.
