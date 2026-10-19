# Full checklist and red flags

Long form of the checklist and red-flag table in `SKILL.md`, with the failure each
question prevents and the check for each red flag.

## Decision checklist

| # | Question | Failure it prevents |
|---|---|---|
| 1 | What is the research question, in one sentence, including whether users are known (have history) or unseen? | A split that silently answers a different question |
| 2 | For each method, what may it read at inference (own history, item text, cross-user statistics) and what was it trained on (nothing, other domains, target-domain training data)? | Comparing methods across information-access layers without saying so |
| 3 | Which split answers question 1: per-user LOO, global temporal, user-disjoint, random? Which leak does it allow, and for which methods? | Undisclosed leakage, or a guard that removes valid evidence |
| 4 | Does any method fit parameters or statistics across users? If none, a global cutoff protects nothing; if some do, plan a global-temporal sensitivity check or disclose cross-user future data | Over-correcting a frozen method; claiming a fixed leak direction |
| 5 | If a user-disjoint split is used: is unseen-user generalization the question, and how do ID-embedding models fold in new users? | Accidental cold-start evaluation |
| 6 | How is the target chosen? (last event; not "first event after a cutoff") | Target bias toward long inter-event gaps (Gusak et al. 2025, §4.2) |
| 7 | Does an official split file exist for this dataset and version? If yes, use it and record hashes | Self-made 5-core data that differ from published splits |
| 8 | Duplicate (user, item) rule, timestamp tie rule (row order, never item ID), k-core order — written down? | Repeat-item shortcuts; false sequences from ID-sorted ties |
| 9 | Candidates: full ranking, sampled 1+n (uniform or popularity), or retrieve-then-rerank? Is the claim conditional on that distribution? | Sampled metrics that reverse model order (Krichene & Rendle 2020; Hidasi & Czapp 2023 §2.4) |
| 10 | For two-stage evaluation: fixed retriever, end-to-end metrics, retrieval misses counted, target never injected? | Inflated rerank scores |
| 11 | Do all methods receive identical users, targets, candidate sets, visible history and item text, verified by per-query hashes? | Unequal evidence hidden by aggregate tables |
| 12 | Is the visible-history count per query equal across methods (catalogue filters can drop history items for ID models only)? | One method seeing history another cannot |
| 13 | Seeds and repeats per method type; determinism check for "deterministic" methods? | Single-run noise reported as differences |
| 14 | Where are prompt or method variants tuned, and are the reporting users fresh? | Selection bias (winner's curse) |
| 15 | Failure policy: execution failures rerun; method failures kept as utility 0 and counted? | Crashes reported as results, or dropped failures inflating scores |
| 16 | For LLM methods: candidate order, parse failures, text fields, lexical and category controls, history-swap control, cost with equal caching, pretraining exposure? | Gains explained by position, word overlap or memorization |
| 17 | Is the random-ranking expectation printed next to sampled results? | Mistaking near-random scores for ranking ability |

## Red flags

| Observation | Likely cause | Check |
|---|---|---|
| Trained baselines far below simple rules | Test users unseen in training (user-disjoint or cutoff), or untuned baselines | Count training events per evaluation user; compare with official code defaults |
| "Leakage only helps the baselines" in a draft | Direction asserted without measurement | Ji et al. Table 5; run a GTS sensitivity check |
| Popularity below random | Popularity-weighted negatives | Compare uniform and popularity sampling; use full ranking |
| Method order flips between 1+99 and full ranking | Sampled-metric inconsistency | Report full ranking or two-stage end-to-end |
| User/item counts differ from the official benchmark | Dedupe/k-core order, different release | Use official split files; record hashes |
| Target appears in visible history | Repeats kept or wrong tie handling | Repeat rule; strict (timestamp, row order) cut |
| Same history for different users | Ties sorted by item ID | Sort ties by original row order |
| Rerank metric higher than retriever recall allows | Target injected into retrieved list | Recompute end-to-end with misses as 0 |
| Score correlates with description length or list position | Text-length or position bias | Text-field control; order permutation |
| Large gain from per-user best variant | Oracle selection using the target | Report only deployable selectors |
| Zero-utility queries with OOM or HTTP 500 in logs | Execution failures counted as method failures | Rerun until success; separate counts |
| Frozen model scores differ across identical runs | Nondeterministic kernels or serving | Determinism check before claiming one run suffices |
