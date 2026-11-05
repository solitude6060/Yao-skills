# Baselines and fairness

Read when choosing comparison methods, running them, or writing the comparison claim.

## Layer baselines by information access

A comparison is interpretable only when each method's information access is stated.
Group methods by what they may read:

| Layer | Information the method may use | Examples |
|---|---|---|
| A. Own history + item text | Target user's strictly earlier events, item titles/descriptions, the candidate list | Frozen LLM ranking, lexical matching (BM25), category match, recency rules |
| B. + cross-user statistics | Counts or co-occurrence over other users' training events, no learned parameters | Popularity, item-kNN, co-occurrence rules, EASE (closed form) |
| C. + target-domain training | Parameters fit on the target domain's training data | BPR-MF, NCF, SASRec, BERT4Rec, LightGCN, UniSRec fine-tuned, fine-tuned LLM recommenders |
| D. Zero-shot transfer | Parameters fit on other domains only, applied without target-domain updates | Pretrained text-based sequential models without fine-tuning |

Write claims per layer ("among methods that use only the user's own history and item
text ..."), and state which layers a method beats or approaches. Mixing layers in one
ranking without labels hides why a method wins.

## Same inputs for every method

For each query, every method must use the same: user set, target event, candidate set
(a hash of the candidate list), visible history cut (strictly before the target), catalogue, and
item text fields (or state the difference). Record the per-query hashes and check them
before computing metrics.

## Source fidelity

- Priority: official author code > credible public implementation with traceable
  authorship, revision and license > custom implementation, with the reason recorded
  for each step down.
- Pin the repository URL, commit and imported files. Keep model graph, loss, sampling,
  initialization and optimizer as the source defines them; adapt only data ingestion
  and evaluation.
- Tune trained baselines with the same budget and on validation targets.
- Context: [Dacrema et al., RecSys 2019](https://arxiv.org/pdf/1907.06902) considered
  18 top-n algorithms from top venues; only 7 could be reproduced with reasonable effort,
  and 6 of those were often outperformed by simple heuristics (abstract).
  [Rendle et al., 2020](https://arxiv.org/pdf/2005.09683) report that a
  properly tuned dot product substantially outperforms the MLP-learned similarity
  proposed in NCF (abstract). Include well-tuned simple baselines (popularity, item-kNN,
  EASE, BPR-MF) before claiming progress.

## Selection checkpoint versus refit

- Two practices exist. Selection: train on training events, keep the checkpoint or
  setting that scores best on validation targets, and evaluate it. Refit: after
  selection, retrain on training plus validation events with the selected setting.
- Official sequential-recommender code and widely used libraries mostly evaluate the
  selected checkpoint; several baseline-rigour studies refit; some official code merges
  the validation event into training by design. Run a practice check of each source.
- Follow each baseline's source, name the practice per baseline in the protocol, and
  refit only where the source does. A protocol change between the two supersedes the
  affected rows explicitly (`lessons-learned.md`, lesson 20).
- When the official code selects on a sample of validation users, every baseline reads
  the same sample file; under per-user leave-one-out the sample contains the evaluated
  users, under a user-disjoint protocol it excludes them (lesson 21).

## Official and relaxed configurations

- Run every baseline first with its official configuration. When an official limit
  binds on this data (input length, history window, step budget), add a relaxed
  variant and label it beside the official row, for example "official" and "relaxed
  limit".
- Both rows stay in the tables; each claim says which one it uses. A relaxed variant
  never replaces the official row silently.
- For generative LLM baselines, the regeneration rounds after unparseable output and the
  parser are declared before the run; scores before and after retries are kept
  (lessons 28, 29).

## Seeds and repeats

Screening runs during iteration may use one run per cell with point estimates or paired
differences to choose the next experiment; the run counts below apply to confirmatory
claims (`experiment-planning`, evidence stages).

| Method type | Randomness | Runs |
|---|---|---|
| Frozen local model, deterministic logit/likelihood readout, fixed candidates and order | None | 1 run; a second run is a determinism check |
| Closed-form models (EASE, popularity) | None | 1 run |
| Trained models (MF, SASRec, ...) | Initialization, sampling, data order | Several seeds; report mean and spread |
| LLM ranking with sampled decoding | Decoding | Several seeds or repeats |
| Hosted API models | Server-side nondeterminism even at temperature 0 | Repeat a subset and report the spread |
| Candidate-order permutation | Order | Fix order seed, or average over permutations |

Fix the test set (users, targets, candidates) across seeds; vary only the method seed.
A per-user bootstrap of the paired difference covers user sampling only; a confirmatory claim
against a method with training or decoding randomness adds these seeds or repeats, or states
that it holds for one training run.
LLMRank averaged at least three repeat runs ([Hou et al., §3](https://arxiv.org/pdf/2305.08845)).

## Execution failures versus method failures

- Execution failure: out-of-memory, HTTP 5xx, crash, timeout, missing file, port
  conflict. It is not a result. Rerun the affected queries until they succeed; a run
  with unresolved execution failures is not reported. Record attempts and cause.
- Method failure: the method returns unparseable or invalid output, or by design cannot
  rank this input (e.g. a trained model with no in-catalogue history for this user). It
  stays in the denominator with utility 0 and is reported as a separate count.
- Every results table shows the failure count next to the score.

## Selection bias from tuning on reporting users

Trying many prompt, readout or method variants and reporting the best one on the same
users inflates the reported score (winner's curse). Rules:

1. Tune on a development user set; freeze the configuration; report on fresh users.
2. When the user sample grows for the final run, the added users are fresh; report on
   them, or on the full set with the development subset reported separately.
3. Report how many variants were tried.

## Comparison claims

- Prefer paired comparisons on the same queries (paired bootstrap intervals over users)
  to separate per-method scores.
- Relative claims ("within X of", "beats") should name the layer, dataset, split,
  candidate protocol and failure counts.
- Valid negative and ablation results stay in the tables.
