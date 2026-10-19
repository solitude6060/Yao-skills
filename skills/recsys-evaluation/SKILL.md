---
name: recsys-evaluation
description: Use before designing, auditing or writing up an offline recommender evaluation — split, candidates, metrics, datasets, baselines — or when comparing LLM or frozen-model recommenders with trained ones.
argument-hint: "<design | audit | write-up> <protocol, plan file or result table | empty>"
---

# Recommender-System Evaluation

The split, the candidate set and the preprocessing decide what a score means. Most
invalid comparisons come from a protocol that was inherited rather than derived from
the research question. Run the checklist before building an experiment and again
before a result enters a report.

## When to run

- Designing or changing an offline evaluation protocol
- Inheriting a split, cutoff, candidate rule or dataset from a spec, paper or repo
- Comparing methods with different information access (frozen LLM vs trained model)
- A result is surprising, or changes sign between protocols
- Writing a protocol section, limitation or reviewer response

## Decision checklist — answer in order, in the plan file

1. **Research question in one sentence**, including whether users are known (have
   history) or unseen. Prevents a split that answers a different question.
2. **Information access per method**: what it reads at inference (own history, item
   text, cross-user statistics) and what it was trained on. Prevents unlabelled
   cross-layer comparisons.
3. **Split**: per-user leave-one-out (LOO), global temporal (GTS), user-disjoint or
   random — and which leak it allows for which methods.
4. **Does any method fit across users?** If none, a global cutoff protects nothing and
   only removes valid history. If some do, disclose cross-user future data and plan a
   GTS sensitivity check. Never assert the leak's direction without measuring it.
5. **User-disjoint only if unseen users are the question**; state how ID-embedding
   models fold in new users. Prevents accidental cold-start evaluation.
6. **Target = last event.** Not "first event after a cutoff" (biased toward long gaps).
7. **Official split files** for this dataset version? Use them; record hashes.
8. **Preprocessing written down**: duplicate (user, item) rule, tie order (row order,
   never item ID), k-core order. Prevents repeat shortcuts and false sequences.
9. **Candidates**: full ranking, sampled 1+n (uniform or popularity), or
   retrieve-then-rerank. Sampled claims are conditional on that distribution.
10. **Two-stage**: fixed retriever, end-to-end metrics, misses counted, target never
    injected.
11. **Identical inputs**: same users, targets, candidates, visible history and item
    text for every method, proven by per-query hashes; equal visible-history counts.
12. **Runs**: seeds for trained or sampled methods, repeats for hosted APIs, a
    determinism check before declaring one run enough; never choose among runs by test score.
13. **Tuning users vs reporting users** are different. Prevents selection bias.
14. **Failures**: execution failures (OOM, HTTP 5xx, crash) are rerun, never reported;
    method failures (invalid output, no ranking by design) stay in the denominator
    with utility 0 and are counted.
15. **LLM methods**: candidate order, parse failures, text fields, lexical and category
    controls, history-swap control, cost under equal caching, pretraining exposure.
16. **Random expectation** printed next to sampled results.

"Inherited from the spec" as an answer to 1–6 means the protocol is not ready:
derive it or record an ADR.

## Core facts

- LOO allows cross-user future data in training; its effect runs in both directions
  and reorders models (Ji et al., TOIS 2023, Tables 5–6).
- GTS targets: Last, Random or Successive; not First (Gusak et al., RecSys 2025, §4.2, §5).
- Sampled metrics do not preserve model order even in expectation (Krichene & Rendle,
  KDD 2020).
- One target at rank r of n: HR@K = 1[r ≤ K]; NDCG@K = 1/log2(r+1) for r ≤ K;
  MRR = 1/r. Random: E[HR@K] = K/n; E[NDCG@K] = (1/n)·Σ_{r=1..K} 1/log2(r+1);
  NDCG@10 = 0.227 / 0.091 / 0.045 for n = 20 / 50 / 100.

## Red flags

| Observation | Likely cause |
|---|---|
| Trained baselines far below simple rules | Test users unseen in training, or untuned baselines |
| "Leakage only helps the baselines" | Direction asserted without measurement |
| Popularity below random | Popularity-weighted negatives |
| Order flips between 1+99 and full ranking | Sampled-metric inconsistency |
| Counts differ from the official benchmark | Dedupe/k-core order or release version |
| Target inside visible history; identical histories | Repeat rule; ties sorted by item ID |
| Rerank score above retriever recall | Target injected into retrieved list |
| Large gain from per-user best variant | Oracle selection using the target |
| Zero-utility queries with OOM or HTTP 500 | Execution failures counted as method failures |

## Reporting

Each results table states dataset and release, split and target rule, candidate
protocol, user count, random expectation, failure counts, seeds or repeats, and each
method's information-access layer. LLM rows add tokens, latency and cost. Disclose
cross-user future data under LOO and pretraining exposure of frozen models.

## Read before acting

- `references/checklist-and-red-flags.md` — full checklist with failures prevented; red flags with checks
- `references/splits-and-leakage.md` — split families, evidence, cutoff, user-disjoint trap
- `references/candidates-and-metrics.md` — sampling, two-stage rules, formulas, nested sets
- `references/datasets-and-preprocessing.md` — official splits, dedupe, ties, versions
- `references/baselines-and-fairness.md` — access layers, source fidelity, seeds, failures
- `references/llm-recsys-evaluation.md` — position bias, parsing, controls, cost, exposure
- `references/history-of-practice.md` — protocols by era with sources; reviewer expectations
- `references/lessons-learned.md` — failures from a recommender-evaluation study and the rule each produced
- Pair with `first-principles` when a protocol rule is inherited or a result is load-bearing.
