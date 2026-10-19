# Analysis catalog: how papers explain why a simple method works

Compiled on 2026-10-17 from three independent readings of the literature; "verified" means a reader read the paper
text, not that the result was reproduced. Items that two readers described differently are marked; check the paper
before citing a figure number.

| Paper | Analysis | Form | Claim it supports | Status |
|---|---|---|---|---|
| kNN-LM, Khandelwal et al., ICLR 2020, arXiv 1911.00172 | Perplexity against the interpolation weight lambda (tuned on validation; optimum differs in-domain and under domain adaptation); datastore size against perplexity and tuned lambda; examples where the memory raises the target probability; control with an interpolated n-gram model | Fig. 5 lambda curve; Fig. 2 datastore; examples table; Fig. 7 n-gram control | The memory helps where the parametric model is weak (rare patterns); the weight is data dependent; a cheaper memory does not substitute | Verified by two readers |
| Xu, Alon, Neubig, ICML 2023, arXiv 2301.02828 | Replace each kNN component by a parametric alternative and measure the recovered gain (ensembling two representations, approximate search, softmax temperature); datastore subsampling | Tables 1-2, Fig. 2 | The gain decomposes into named factors | Verified by two readers |
| Drozdov et al., Findings of EMNLP 2022, arXiv 2210.15859 | Queries in 20 bins by similarity of the top retrieved context; relative gain per bin; TF-IDF variant; removal of overlapping n-grams; adaptive lambda per bin | Fig. 2, Table 1, Fig. 4 | Retrieval helps where retrieval quality is high; the weight can depend on the query | Verified by two readers |
| He, Neubig, Berg-Kirkpatrick, EMNLP 2021, arXiv 2109.04212 | Share of tokens where the memory beats the model; adaptor predicting lambda from cheap features; quality against the fraction of retrievals removed, against random removal | Fig. 3 | The memory is needed for a minority of predictions, predictable from cheap features | Verified by two readers |
| Spalm, Yogatama et al., TACL 2021, arXiv 2102.02557 | Histograms of the gate between local context and long-term memory per dataset; gate traces; examples | Figs. 4-6 | Which source is used depends on the data and is visible in the gate distribution | Verified by two readers |
| Lee, SIGIR 1997, doi 10.1145/258525.258587 | Relevant overlap against non-relevant overlap between retrieval runs (unequal overlap property); CombMNZ | Overlap table | Fusion works when runs agree on relevant items and differ on non-relevant ones | Verified by one reader; a second could not obtain the full text; a third gave another DOI |
| Vogt and Cottrell, Information Retrieval 1999, doi 10.1023/A:1009980820262 | Linear combination; separation d (mean score on relevant minus non-relevant); regression of fused performance on component performance and overlap; skimming, chorus and dark-horse effects | Regression table | A linear combination helps when components are strong, share relevant items and differ on non-relevant ones | Verified from text by two readers |
| FPMC, Rendle et al., WWW 2010, doi 10.1145/1772690.1772773 | Factorization, Markov chain and their combination on dense and sparse subsets; transition-matrix fill | Fig. 6, Table 2 | Which signal dominates depends on density; the combination covers both | Verified by two readers |
| Fossil, He and McAuley, ICDM 2016, arXiv 1609.09152 | Learned per-user short-term weight against the user's number of actions; examples | Fig. 7 scatter | Short-term dynamics matter most for sparse users | Verified by two readers; a third described a different figure |
| SASRec, Kang and McAuley, ICDM 2018, arXiv 1808.09781 | Average attention by position on sparse versus dense datasets, with and without positional embedding, by layer | Fig. 4 heatmaps | Attention goes to recent items on sparse data and older items on dense data; attention is not causal importance | Verified by two readers |
| CLSR, Zheng et al., WWW 2022, arXiv 2202.13090 | Fusion weight by behaviour type; shuffle (removes short-term order) and truncate (weakens long-term) protocols; fixed fusion weight sweep against adaptive fusion | Tables 3-4, Figs. 5, 7 | Long- and short-term interests are separated; adaptive fusion beats any fixed weight | Verified by two readers; a third described a different analysis |
| SLi-Rec, Yu et al., IJCAI 2019 | Long-only, short-only, fixed and adaptive fusion; long-term weight by time gap | Table 5, Fig. 1 | Longer gaps go with more long-term weight | One reader verified; a second verified only the equation |
| Hou et al., ECIR 2024, arXiv 2305.08845 | Original, shuffled and fake (replaced) histories; history length 5 to 50; target position; popularity of the top item | Figs. 2-3 | LLM rankers use history content but little of its order, and carry position and popularity bias | Verified by two readers |

Analysis types and their precedents:

| Type | Precedents |
|---|---|
| Interpolation-weight curve | kNN-LM; CLSR (fixed weight sweep) |
| Grouping by frequency or retrieval quality | kNN-LM; Drozdov et al.; He et al. |
| Memory or datastore size | kNN-LM; Xu et al. |
| Factor isolation by substitution | Xu et al.; kNN-LM n-gram control |
| Gate or weight distributions | Spalm; Fossil; SLi-Rec; CLSR |
| Input interventions (shuffle, truncate, replace) | CLSR; Hou et al. |
| Fusion overlap and separation | Lee; Vogt and Cottrell |
| Dense versus sparse data | FPMC; SASRec; Fossil |

Full-text check on 2026-10-17 by a separate reader (text only, figures not viewed): all arXiv ids and venues above confirmed; the chorus
and dark-horse effects are credited to Diamond 1998 inside Vogt and Cottrell, not to Lee. Additional precedents read in full: He et al.
CIKM 2023 (LLM recommender input perturbation), Ji et al. SIGIR 2020 (time-aware popularity), STAR arXiv 2410.16458 (venue unverified),
CoRRe CIKM 2026 (stepwise rank progression), PRINCE WSDM 2020 (minimal counterfactual removal).
