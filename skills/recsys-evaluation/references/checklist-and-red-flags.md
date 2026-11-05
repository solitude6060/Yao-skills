# Full checklist and red flags

Long form of the checklist and red-flag table in `SKILL.md`, with the failure each
question prevents and the check for each red flag. Questions 18 onward extend the
`SKILL.md` checklist with the later lessons in `lessons-learned.md`.

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
| 13 | Seeds and repeats per method type for confirmatory claims (screening may use one run to choose the next experiment); determinism check for "deterministic" methods? | Single-run noise reported as differences |
| 14 | Where are prompt or method variants tuned, and are the reporting users fresh? | Selection bias (winner's curse) |
| 15 | Failure policy: execution failures rerun; method failures kept as utility 0 and counted? | Crashes reported as results, or dropped failures inflating scores |
| 16 | For LLM methods: candidate order, parse failures, text fields, lexical and category controls, history-swap control, cost with equal caching, pretraining exposure? | Gains explained by position, word overlap or memorization |
| 17 | Is the random-ranking expectation printed next to sampled results? | Mistaking near-random scores for ranking ability |
| 18 | Are negatives drawn by a seeded uniform generator (or a rule the target also satisfies), and does no function of the sampling rule rank the target above random? | A sampler that identifies the target (lesson 18) |
| 19 | Are item identifiers kept out of every model request, and does an identifier-only rule score near random? | Shortcuts through identifier order (lesson 19) |
| 20 | Does each trained baseline follow its source's selection-versus-refit practice, named in the protocol? | Refit rows that the sources never produce (lesson 20) |
| 21 | When validation users are sampled, does the sample contain the evaluated users, with one shared sample file? | Baselines selected on a different population (lesson 21) |
| 22 | Is every high-severity protocol finding from an audit answered by an experiment before claims freeze? | A late central objection from reviewers (lesson 22) |
| 23 | If a method reads request-time cross-user information: is there a global-cutoff check that removes post-cutoff events from every method, and at least one time-aware trained baseline? | Information asymmetry credited to the method (lessons 23, 24) |
| 24 | Has the exposure of the reporting cohort been scanned across earlier runs and sibling projects? | A "held-out" cohort that shaped earlier choices (lesson 25) |
| 25 | For a cold-start or new-item claim, how many targets qualify under the protocol's exact time and tie rule? | A claim with few or no qualifying targets (lesson 26) |
| 26 | If a method reads request-time activity, is a time-matched negative variant reported beside uniform negatives? | Gains from negatives that had no activity at the request time (lesson 27) |
| 27 | For LLM baselines: official configuration plus a labelled relaxed variant where limits bind; regeneration rounds and parser declared before the run? | An unfaithful or post-hoc tuned LLM baseline (lessons 28, 29) |

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
| Target ranks first under a rule over candidate hashes or ids | Negatives chosen by a rule the target does not pass | Redraw negatives uniformly; test the rule as a ranker |
| An identifier-order rule beats random on candidate pools | Identifiers assigned in time order | Remove identifiers from requests; report the rule as a shortcut check |
| Method gain shrinks under time-matched negatives | Uniform negatives with no activity at the request time | Report both negative variants |
| Baseline rows read a refit model the source does not train | Refit step outside the source's practice | Practice check of the official code; supersede refit rows |
| Most "new" targets already have interactions | Definitional count not checked | Count qualifying targets under the protocol's time and tie rule |
