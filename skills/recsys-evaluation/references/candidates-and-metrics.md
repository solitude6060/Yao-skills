# Candidates and metrics

Read when deciding which items a method must rank and how the result is scored.

## Candidate protocols

| Protocol | Definition | Typical use | What the score means |
|---|---|---|---|
| Full ranking | Target ranked against the whole catalogue (usually minus the user's training items) | Trained retrieval models; methodology papers after 2020 | Closest to the deployed retrieval task |
| Uniform sampled negatives, 1+n | Target plus n items drawn uniformly from items the user has not interacted with (n = 9, 19, 49, 99, 100 are common) | Neural sequential era; most LLM-ranking papers | Ranking quality on that candidate distribution only |
| Popularity-sampled negatives | Negatives drawn proportional to popularity | BERT4Rec | Harder for popularity-driven methods; a different distribution again |
| Retrieve-then-rerank (two-stage) | A first-stage retriever selects K items from the full catalogue; the method reranks them | LLM rerankers that cannot score the whole catalogue | End-to-end quality, bounded by retrieval recall |

Verified examples: SASRec 1+100 uniform ([§IV-D](https://arxiv.org/pdf/1808.09781));
BERT4Rec 1+100 popularity-sampled ([§4.2](https://arxiv.org/pdf/1904.06690));
S3-Rec 1+99 uniform ([§5.1.2](https://arxiv.org/pdf/2008.07873)); NCF LOO with
100 sampled items ([§4.1](https://arxiv.org/pdf/1708.05031)).

## Sampled metrics are not consistent with full-ranking metrics

- [Krichene & Rendle, "On Sampled Metrics for Item Recommendation", KDD 2020](https://dl.acm.org/doi/10.1145/3394486.3403226);
  authors' extended abstract [IJCAI 2021](https://www.ijcai.org/proceedings/2021/0651.pdf)
  §3.1: sampled metrics "are inconsistent with their exact counterpart"; "only AUC
  is consistent". KDD abstract: "sampling should be avoided for metric calculation,
  however if an experimental study needs to sample, the proposed corrections can
  improve the quality of the estimate." The KDD abstract adds that sampled metrics
  "do not persist relative statements, e.g., recommender A is better than B, not even
  in expectation". KDD full text not opened here; claims come from the extended
  abstract and the KDD abstract.
- [Hidasi & Czapp, RecSys 2023, §2.4, Fig. 4](https://arxiv.org/pdf/2307.14951):
  with 100 sampled negatives the true order A > C ≫ B on Rees46 (MRR) reads as
  B > A ≫ C; on Coveo, A beats B by 8.1% recall@20 under full ranking and loses by
  4.7% with 100 negatives. This is a candidate-set effect, separate from leakage.

Consequences:

1. Report sampled results as conditional on that candidate distribution ("NDCG@10
   with 1+49 uniform negatives"). Do not call them recommendation accuracy in general.
2. Do not compare numbers across papers that used different n or sampling schemes.
3. A load-bearing ranking claim needs either full ranking or a two-stage evaluation
   from the full catalogue.

## Two-stage (retrieve-then-rerank) rules

- Retriever must be fixed and identical for every reranker.
- Report end-to-end metrics over all test targets. A target missed by the retriever
  scores 0 for every reranker; count and report retrieval misses (retriever recall@K).
- Never inject the target into the retrieved list. Injection turns the task into a
  sampled-candidate evaluation with a retriever-chosen negative distribution.
- Say whether the reranker receives retriever scores or ranks. If the research question
  is about the reranker alone, it should not.
- Report the "no rerank" retriever order as a reference row.

## Metric definitions (one relevant item per query)

Let r be the 1-based rank of the target among n candidates.

- HR@K (hit ratio, = Recall@K with one target): 1 if r ≤ K, else 0.
- NDCG@K: 1 / log2(r + 1) if r ≤ K, else 0 (ideal DCG = 1).
- MRR (or MRR@K): 1 / r (0 if r > K for the @K form).
- A failed query (unparseable output, no ranking) contributes 0 to every metric and
  stays in the denominator.

## Random-ranking expectation

With the target uniformly placed among n candidates:

- E[HR@K] = K / n
- E[NDCG@K] = (1/n) · Σ_{r=1..K} 1 / log2(r+1)
- E[MRR] = (1/n) · Σ_{r=1..n} 1/r

| n candidates | E[HR@10] | E[NDCG@10] | E[MRR] |
|---|---|---|---|
| 20 | 0.500 | 0.227 | 0.180 |
| 50 | 0.200 | 0.091 | 0.090 |
| 100 | 0.100 | 0.045 | 0.052 |

(Computed from the formulas above.) Always print this row next to results on sampled
candidates; a method near it is not ranking.

## Scaling curves over candidate count

- Use nested candidate sets: the 20-candidate set is a subset of the 50-set, which is
  a subset of the 100-set, for the same user and target. Differences across n then
  reflect n, not a fresh random draw.
- Fix the candidate order seed or shuffle explicitly (position effects, see
  `llm-recsys-evaluation.md`).
- Record a hash of the candidate list per query so every method is proven to see identical sets.

## Popularity-weighted negatives as a stress test

Sampling negatives proportional to popularity makes popular non-targets frequent
in the candidate list. A pure popularity ranker then puts those negatives first and
can score below the random expectation. Treat this as a reverse stress test for
popularity reliance, not as a neutral main protocol. Direct evidence that a method
uses more than popularity comes from full ranking, history-swap controls and
stratification by target popularity.
