# 評估做法的演變

英文版 [history-of-practice.md](history-of-practice.md) 為執行規範。

把協議放進前人研究中定位，或回答「審稿人通常期待什麼」時閱讀。各列只引用在 2026-10-08 讀過的文字；其餘一律標為**未查證**。

## 依時期與論文類型

| 時期／論文類型 | 代表作品 | 切分 | 候選 | 指標 | 來源 |
|---|---|---|---|---|---|
| 評分預測（Netflix Prize 時期） | 以顯式評分做矩陣分解 | 隨機，或提供的 probe 集合 | 不是排序任務 | RMSE | 時期的描述在此**未查證** |
| 轉向 top-N | Cremonesi, Koren & Turrin, RecSys 2010, "Performance of recommender algorithms on top-N recommendation tasks" | — | — | Top-N 準確度 | 標題、場所與年份已查證（[DOI](https://doi.org/10.1145/1864708.1864721)）；內容**未查證**（未開啟全文） |
| 隱式 top-N，神經協同過濾 | NCF, He et al., WWW 2017 | 逐人 LOO（最近一筆互動） | 1+100 抽樣 | HR@10, NDCG@10 | [§4.1](https://arxiv.org/pdf/1708.05031) |
| 未見過使用者的評估 | Mult-VAE, Liang et al., WWW 2018 | 保留使用者（"strong generalization"），80% fold-in | 全排序 | Recall@R, NDCG@R | [§4](https://arxiv.org/pdf/1802.05814) |
| 以 session 為基礎 | GRU4Rec, Hidasi et al., ICLR 2016 | 全域時間：RSC15 測試 = 訓練期間之後一天的 session | 完整商品集合（RSC15） | Recall@20, MRR@20 | [§4](https://arxiv.org/pdf/1511.06939) |
| 神經網路序列模型 | SASRec, ICDM 2018 | LOO，倒數第二筆驗證 | 1+100 均勻 | HR@10, NDCG@10 | [§IV](https://arxiv.org/pdf/1808.09781) |
| 神經網路序列模型 | BERT4Rec, CIKM 2019 | LOO | 1+100 依熱門度抽樣 | HR, NDCG, MRR | [§4.2](https://arxiv.org/pdf/1904.06690) |
| 神經網路序列模型 | S3-Rec, CIKM 2020 | LOO，倒數第二筆驗證 | 1+99 均勻 | HR, NDCG, MRR | [§5.1.2](https://arxiv.org/pdf/2008.07873) |
| 對抽樣指標的批評 | Krichene & Rendle, KDD 2020 | — | 全排序對抽樣 | 抽樣指標不一致；避免抽樣 | [IJCAI 2021 延伸摘要 §3](https://www.ijcai.org/proceedings/2021/0651.pdf) |
| 對切分的批評 | Meng et al., RecSys 2020 | LOO 對依使用者的時間切分對全域時間切分 | **未查證** | 切分會改變模型名次 | [摘要、§1](https://arxiv.org/pdf/2007.13237) |
| 對可重現性的批評 | Dacrema et al., RecSys 2019；Rendle et al. 2020（場所 RecSys 2020 **未查證**） | — | — | 調得好的簡單基線常常勝出 | [Dacrema](https://arxiv.org/pdf/1907.06902)、[Rendle](https://arxiv.org/pdf/2005.09683) |
| Benchmark | DaisyRec 2.0, TPAMI 2023 | 論文調查：依比例切分 69%、LOO 21%、依時間切分 6% | 比較各種設定 | 切分與抽樣會改變分數 | [§2.2.3](https://arxiv.org/pdf/2206.10848) |
| LLM 作為統一的推薦器 | P5, RecSys 2022 | 序列：LOO；評分等任務：隨機 80/10/10 | 直接推薦：1+99 | HR, NDCG | [§5.1](https://arxiv.org/pdf/2203.13366) |
| LLM 偏好預測 | TALLRec, RecSys 2023 | 8:1:1 切分 | 二元喜歡／不喜歡 | AUC | [§3](https://arxiv.org/pdf/2305.00447) |
| LLM 零樣本排序 | LLMRank, ECIR 2024 | LOO；ML-1M 全部使用者，Games 抽樣 6,000 位使用者 | 20 個候選；也使用檢索得到的候選 | NDCG@K，至少 3 次重複執行 | [§3](https://arxiv.org/pdf/2305.08845) |
| LLM 加協同過濾 embedding | A-LLMRec, KDD 2024 | LOO | 1+19 均勻 | Hit@1 | [§5.1](https://arxiv.org/pdf/2404.11343) |
| LLM agent | AgentCF（場所 WWW 2024 **未查證**） | 以最後一筆事件為測試（為節省 API 成本而抽樣使用者子集） | 1+9 | NDCG | [§3.1](https://arxiv.org/pdf/2310.09233) |
| LLM agent | InteRecAgent, Huang et al. (arXiv 2308.16505) | LOO | 從完整集合檢索，並對提供的候選排序；候選數量**未查證** | Recall@k, NDCG@k | [§4](https://arxiv.org/pdf/2308.16505) |
| LLM 加序列編碼器 | LLaRA, SIGIR 2024 | 8:1:1 | 20 個候選 | HitRatio@1 | [§5.1](https://wujcan.github.io/papers/sigir24-llara.pdf) |
| LLM 加序列編碼器 | LLM-SRec, KDD 2025 | Leave-last-out | 1+99 | NDCG, HR | [§2.2](https://arxiv.org/pdf/2502.13909) |
| 方法論，2023–2025 | Hidasi & Czapp RecSys 2023；Ji et al. TOIS 2023；Gusak et al. RecSys 2025 | 主張採用全域時間評估 | 全排序 | 洩漏與抽樣會使名次反轉或改變 | [Hidasi](https://arxiv.org/pdf/2307.14951)、[Ji](https://arxiv.org/pdf/2010.11060)、[Gusak](https://arxiv.org/pdf/2507.16289) |

場所備註：場所已在論文本文、arXiv 中繼資料或 Crossref 核對；AgentCF 與 Rendle et al. 的場所無法確認。InteRecAgent 的期刊場所（部分調查列為 TOIS 2025）在此未開啟：**未查證**。章節編號對應所連結的 arXiv 版本。

## 普及程度的資料

- Gusak et al. §3.0.2：在 RecSys、SIGIR、CIKM 2022–2024 中，75 篇做離線評估的序列推薦論文裡，77.3% 使用以 LOO 為基礎的切分，16% 使用以 GTS 為基礎的切分，6.7% 使用下一個商品設定的 GTS。
- DaisyRec 2.0 §2.2.3：在他們蒐集的論文中，依比例切分 69%，LOO 21%，依時間切分 6%，其他 4%。
- 2020 年之後，全排序與抽樣候選的普及比例：在此未開啟任何調查統計；**未查證**。

## RecSys／SIGIR／WWW／KDD 的審稿人現在通常期待什麼

這一節綜合上述方法論論文的內容，並未做調查統計。

1. 切分要有研究問題支持的理由，並揭露已知的洩漏。序列推薦與 LLM 排序的工作，因為 LOO 是標準做法而被接受；知道 Ji et al.、Meng et al. 與 Gusak et al. 的審稿人，會要求全域時間檢查或明確的限制說明。
2. 抽樣候選的結果要如實標示並引用 Krichene & Rendle，主要主張另外附上全排序，或兩階段的端到端評估。
3. 調得好的強簡單基線（popularity、item-kNN、EASE、BPR-MF），以及標準的序列模型（SASRec、BERT4Rec），以官方程式碼執行。
4. 每個方法使用相同的候選與輸入；seed／重複次數；顯著性或區間。
5. 對 LLM 方法：成本與延遲、位置偏差的處理、無效輸出的筆數，以及對預訓練曝露的討論。
6. 資料集版本與前處理要精確陳述（發布年份、k-core、去重、切分檔），並公開程式碼。
