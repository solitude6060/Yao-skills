# Splits and leakage

Read when choosing or auditing how events are divided into training, validation and
test data. Every paper claim below was checked against the linked full text on
2026-10-08 unless marked **unverified**.

## The four split families

| Split | Definition | Research question it answers | Leakage or distortion it allows |
|---|---|---|---|
| Per-user leave-one-out (LOO, "leave-last-out") | For each user: last event = test, second-last = validation, rest = training | Given a known user's earlier events, can the method predict that user's next event? | Training contains other users' events that happen after a test user's target (cross-user future data). Ordering is local to each user, not global. |
| Global temporal split (GTS) | One or two cutoff times for the whole dataset; training events precede the cutoff | How would a model trained at time t perform on events after t? | No cross-user future data for trained models. Target choice after the cutoff introduces its own bias (see below). Fewer test users. |
| User-disjoint ("strong generalization") | Users are partitioned; test users contribute no events to training; a fold-in share of each test user's history is given as input | Can the method serve users it has never been trained on? | Converts the task into unseen-user / cold-start evaluation. ID-embedding models need a fold-in procedure or cannot score these users. |
| Random or ratio split | Random events (globally or per user) go to test | Rating prediction or matrix completion without time order | Ignores both local and global time; future events of the same user can train the model. |

Sources for definitions: LOO with second-last validation in
[SASRec, §IV-A](https://arxiv.org/pdf/1808.09781) and
[S3-Rec, §5.1.2](https://arxiv.org/pdf/2008.07873); GTS taxonomy and target options
in [Gusak et al., RecSys 2025, §3, Fig. 1](https://arxiv.org/pdf/2507.16289);
held-out users with an 80% fold-in set in
[Liang et al., Mult-VAE, WWW 2018, §4](https://arxiv.org/pdf/1802.05814); local vs
global timeline per split type in
[Ji et al., TOIS 2023, Table 2](https://arxiv.org/pdf/2010.11060).

## Cross-user future data under LOO: direction is not fixed

[Ji et al., "A Critical Study on Data Leakage in Recommender System Offline Evaluation",
TOIS 2023](https://arxiv.org/pdf/2010.11060) fix the test instances (users' last
interactions in a reference year) and add training data from later years.

- §4.2 Finding 3: "More future data can improve or deteriorate recommendation accuracy".
  Table 5 reports the lowest and highest relative change. NeuMF NDCG@20:
  Amazon-music +40.2% to +89.5%; Amazon-electronic −35.5% to +13.8%. The paper states
  the changes occur "in both signs and magnitudes" with "no particular pattern".
- §4.2 Finding 4 and Table 6: the ranking order of BPR, NeuMF, LightGCN and SASRec
  changes as more future data is added.

Rule: never write that cross-user future data "only helps" or "only hurts" one side.
Disclose it, and if the comparison is load-bearing, measure it with a GTS sensitivity
run on a few key methods.

[Meng et al., "Exploring Data Splitting Strategies for the Evaluation of
Recommendation Models", RecSys 2020](https://arxiv.org/pdf/2007.13237) compare
leave-one-last, temporal user split and global temporal split; the abstract states
the split "can markedly alter the ranking of state-of-the-art recommender systems",
and §1 notes that leave-one-last and temporal user split "leak" future evidence.
Exact candidate protocol: **unverified**.

[Hidasi & Czapp, "Widespread Flaws in Offline Evaluation of Recommender Systems",
RecSys 2023](https://arxiv.org/pdf/2307.14951) list "information leaking through time"
as one of four flaws (§2.3) and recommend time-based splits.

## When a global cutoff matters

- Matters: any method that fits parameters or statistics on a training set shared
  across users (MF, SASRec, EASE, popularity counts, collaborative memories, retrieval
  indices built from other users). Their training data can contain information from
  after the test target.
- Does not matter for leakage: a frozen, training-free method whose only input is the
  target user's own strictly earlier events, item text and the candidate list. No
  cross-user channel exists. Pretraining exposure of the frozen model is a separate
  issue and must be disclosed (see `llm-recsys-evaluation.md`).
- A global cutoff applied to such a frozen method only removes valid personal
  history. That changes the question, it does not remove a leak.

## Target selection after a global cutoff

[Gusak et al., §4.2](https://arxiv.org/pdf/2507.16289): the "First" interaction after
the global timepoint has a much larger time gap to its previous event than other
targets, "which makes this target biased. Thus, we do not recommend using the First
item after the global timepoint as a target." §5 concludes that GTS with Last, Random
or Successive targets is appropriate. §3.0.2: of 75 sequential-recommendation papers
at RecSys, SIGIR and CIKM 2022–2024, 77.3% used LOO-based splits, 16% GTS-based, and
6.7% GTS in the next-item setting.

## The user-disjoint trap

A user-disjoint split looks like a stronger leakage guard, but it silently changes
the task:

- Trained baselines never see the test users' histories, so they are evaluated as
  cold-start / unseen-user models. A frozen method that reads the user's history at
  inference time is unaffected. The comparison then favours the frozen method for a
  reason unrelated to its quality.
- ID-embedding models (MF, BPR, NCF, SASRec with user IDs) need a fold-in step
  (Mult-VAE-style) or a sequence-only encoder; otherwise they cannot score these users.
- Use it only when the research question is generalization to new users, and say so.

## Validation and model selection

- Select hyperparameters on validation targets, never on test targets.
- If test-user partitions exist (development vs locked test), use them to restrict
  which held-out labels may influence tuning; this does not make test users unseen.
- Gusak et al. §4.6 report that retraining on training+validation data changes test
  metrics; state whether the final model was retrained.
