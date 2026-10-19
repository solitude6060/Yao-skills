# History of evaluation practice

Read when positioning a protocol against prior work or answering "what do reviewers
expect". Rows cite only text read on 2026-10-08; anything else is marked
**unverified**.

## By era and paper type

| Era / paper type | Representative work | Split | Candidates | Metric | Source |
|---|---|---|---|---|---|
| Rating prediction (Netflix Prize era) | Matrix factorization on explicit ratings | Random or provided probe sets | Not a ranking task | RMSE | Era characterisation **unverified** here |
| Shift to top-N | Cremonesi, Koren & Turrin, RecSys 2010, "Performance of recommender algorithms on top-N recommendation tasks" | — | — | Top-N accuracy | Title, venue and year verified ([DOI](https://doi.org/10.1145/1864708.1864721)); content **unverified** (full text not opened) |
| Implicit top-N, neural CF | NCF, He et al., WWW 2017 | Per-user LOO (latest interaction) | 1+100 sampled | HR@10, NDCG@10 | [§4.1](https://arxiv.org/pdf/1708.05031) |
| Unseen-user evaluation | Mult-VAE, Liang et al., WWW 2018 | Held-out users ("strong generalization"), 80% fold-in | Full ranking | Recall@R, NDCG@R | [§4](https://arxiv.org/pdf/1802.05814) |
| Session-based | GRU4Rec, Hidasi et al., ICLR 2016 | Global temporal: RSC15 test = sessions of the day after the training period | Full item set (RSC15) | Recall@20, MRR@20 | [§4](https://arxiv.org/pdf/1511.06939) |
| Neural sequential | SASRec, ICDM 2018 | LOO, second-last validation | 1+100 uniform | HR@10, NDCG@10 | [§IV](https://arxiv.org/pdf/1808.09781) |
| Neural sequential | BERT4Rec, CIKM 2019 | LOO | 1+100 popularity-sampled | HR, NDCG, MRR | [§4.2](https://arxiv.org/pdf/1904.06690) |
| Neural sequential | S3-Rec, CIKM 2020 | LOO, second-last validation | 1+99 uniform | HR, NDCG, MRR | [§5.1.2](https://arxiv.org/pdf/2008.07873) |
| Sampled-metric critique | Krichene & Rendle, KDD 2020 | — | Full vs sampled | Sampled metrics inconsistent; avoid sampling | [IJCAI 2021 extended abstract §3](https://www.ijcai.org/proceedings/2021/0651.pdf) |
| Split critique | Meng et al., RecSys 2020 | LOO vs temporal user vs global temporal | **unverified** | Split changes model ranking | [abstract, §1](https://arxiv.org/pdf/2007.13237) |
| Reproducibility critique | Dacrema et al., RecSys 2019; Rendle et al. 2020 (venue RecSys 2020 **unverified**) | — | — | Simple tuned baselines often win | [Dacrema](https://arxiv.org/pdf/1907.06902), [Rendle](https://arxiv.org/pdf/2005.09683) |
| Benchmarking | DaisyRec 2.0, TPAMI 2023 | Survey of papers: split-by-ratio 69%, LOO 21%, split-by-time 6% | Compares settings | Split and sampling change scores | [§2.2.3](https://arxiv.org/pdf/2206.10848) |
| LLM as unified recommender | P5, RecSys 2022 | Sequential: LOO; rating etc.: random 80/10/10 | Direct rec.: 1+99 | HR, NDCG | [§5.1](https://arxiv.org/pdf/2203.13366) |
| LLM preference prediction | TALLRec, RecSys 2023 | 8:1:1 split | Binary like/dislike | AUC | [§3](https://arxiv.org/pdf/2305.00447) |
| LLM zero-shot ranking | LLMRank, ECIR 2024 | LOO; all ML-1M users, 6,000 sampled Games users | 20 candidates; also retrieved candidates | NDCG@K, ≥3 repeat runs | [§3](https://arxiv.org/pdf/2305.08845) |
| LLM + CF embeddings | A-LLMRec, KDD 2024 | LOO | 1+19 uniform | Hit@1 | [§5.1](https://arxiv.org/pdf/2404.11343) |
| LLM agents | AgentCF (venue WWW 2024 **unverified**) | Last event as test (sampled user subsets for API cost) | 1+9 | NDCG | [§3.1](https://arxiv.org/pdf/2310.09233) |
| LLM agents | InteRecAgent, Huang et al. (arXiv 2308.16505) | LOO | Retrieval from the full set and ranking of provided candidates; candidate count **unverified** | Recall@k, NDCG@k | [§4](https://arxiv.org/pdf/2308.16505) |
| LLM + sequential encoder | LLaRA, SIGIR 2024 | 8:1:1 | 20 candidates | HitRatio@1 | [§5.1](https://wujcan.github.io/papers/sigir24-llara.pdf) |
| LLM + sequential encoder | LLM-SRec, KDD 2025 | Leave-last-out | 1+99 | NDCG, HR | [§2.2](https://arxiv.org/pdf/2502.13909) |
| Methodology, 2023–2025 | Hidasi & Czapp RecSys 2023; Ji et al. TOIS 2023; Gusak et al. RecSys 2025 | Argue for global temporal evaluation | Full ranking | Leakage and sampling reverse or change rankings | [Hidasi](https://arxiv.org/pdf/2307.14951), [Ji](https://arxiv.org/pdf/2010.11060), [Gusak](https://arxiv.org/pdf/2507.16289) |

Venue notes: venues were checked in the paper text, arXiv metadata or Crossref; AgentCF and Rendle et al. venues could not be confirmed. InteRecAgent's journal venue (listed as TOIS 2025 in some surveys) was not
opened here: **unverified**. Section numbers refer to the arXiv versions linked.

## Prevalence data

- Gusak et al. §3.0.2: of 75 sequential-recommendation papers (RecSys, SIGIR, CIKM
  2022–2024) with offline evaluation, 77.3% used LOO-based splits, 16% GTS-based,
  6.7% GTS in the next-item setting.
- DaisyRec 2.0 §2.2.3: in their paper collection, split-by-ratio 69%, LOO 21%,
  split-by-time 6%, other 4%.
- Prevalence of full ranking versus sampled candidates after 2020: no survey count was
  opened here; **unverified**.

## What reviewers at RecSys / SIGIR / WWW / KDD typically expect today

This section is a synthesis from the methodology papers above, not a measured survey.

1. A split justified by the research question, with known leakage disclosed. LOO is
   accepted for sequential and LLM-ranking work because it is standard; reviewers
   aware of Ji et al., Meng et al. and Gusak et al. ask for a global temporal check
   or an explicit limitation.
2. Sampled-candidate results labelled as such, citing Krichene & Rendle, plus either
   full ranking or a two-stage end-to-end evaluation for the main claim.
3. Strong, tuned simple baselines (popularity, item-kNN, EASE, BPR-MF) and the
   standard sequential models (SASRec, BERT4Rec), run from official code.
4. Same candidates and inputs for every method; seeds/repeats; significance or
   intervals.
5. For LLM methods: cost and latency, position-bias handling, invalid-output counts,
   and a discussion of pretraining exposure.
6. Dataset versions and preprocessing stated precisely (release year, k-core, dedupe,
   split files), with code released.
