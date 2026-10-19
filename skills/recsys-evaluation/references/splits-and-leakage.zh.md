# 切分與洩漏

英文版 [splits-and-leakage.md](splits-and-leakage.md) 為執行規範。

選擇或稽核事件如何分成訓練、驗證與測試資料時閱讀。以下每項論文主張，除標示「未查證」者外，都已在 2026-10-08 對照連結的全文確認。

## 四種切分類型

| 切分 | 定義 | 回答的研究問題 | 允許的洩漏或扭曲 |
|---|---|---|---|
| 逐人 leave-one-out（LOO，留一法；亦稱 leave-last-out） | 每位使用者：最後一筆事件為測試，倒數第二筆為驗證，其餘為訓練 | 已知一位使用者較早的事件，方法能否預測該使用者的下一筆事件？ | 訓練資料包含其他使用者發生在測試使用者的目標之後的事件（跨使用者未來資料）。時間順序只在每位使用者內部成立，沒有全域順序。 |
| 全域時間切分（GTS，global temporal split） | 整個資料集使用一或兩個截止時間；訓練事件早於截止時間 | 在時間 t 訓練的模型，對 t 之後的事件表現如何？ | 訓練式模型沒有跨使用者未來資料。截止點之後的目標選擇會帶來自己的偏差（見下文）。測試使用者較少。 |
| 使用者隔離（user-disjoint；亦稱「強泛化」，strong generalization） | 使用者分成互不重疊的群組；測試使用者的事件不進訓練；每位測試使用者歷史的一部分（fold-in 比例）作為輸入 | 方法能否服務從未訓練過的使用者？ | 任務變成未見過使用者／冷啟動評估。ID embedding 模型需要 fold-in 程序，否則無法為這些使用者評分。 |
| 隨機或比例切分 | 隨機事件（全域或逐人）進入測試 | 不考慮時間順序的評分預測或矩陣補全 | 同時忽略局部與全域時間；同一位使用者的未來事件可能用來訓練模型。 |

定義的來源：以倒數第二筆作驗證的 LOO 見 [SASRec, §IV-A](https://arxiv.org/pdf/1808.09781) 與
[S3-Rec, §5.1.2](https://arxiv.org/pdf/2008.07873)；GTS 的分類與目標選項見
[Gusak et al., RecSys 2025, §3, Fig. 1](https://arxiv.org/pdf/2507.16289)；
保留使用者並以 80% 作 fold-in 集見
[Liang et al., Mult-VAE, WWW 2018, §4](https://arxiv.org/pdf/1802.05814)；
各切分類型的局部與全域時間軸見
[Ji et al., TOIS 2023, Table 2](https://arxiv.org/pdf/2010.11060)。

## LOO 下的跨使用者未來資料：影響方向不固定

[Ji et al., "A Critical Study on Data Leakage in Recommender System Offline Evaluation",
TOIS 2023](https://arxiv.org/pdf/2010.11060) 固定測試實例（使用者在某參考年份的最後一筆互動），並加入之後年份的訓練資料。

- §4.2 Finding 3："More future data can improve or deteriorate recommendation accuracy"。
  表 5 列出最低與最高的相對變化。NeuMF NDCG@20：Amazon-music 為 +40.2% 至 +89.5%；
  Amazon-electronic 為 −35.5% 至 +13.8%。論文指出這些變化 "in both signs and magnitudes"，且 "no particular pattern"。
- §4.2 Finding 4 與表 6：隨著加入更多未來資料，BPR、NeuMF、LightGCN 與 SASRec 的名次順序隨之改變。

規則：不要寫跨使用者未來資料「只會幫助」或「只會損害」某一方。揭露它；比較若承載主要主張，就用幾個關鍵方法做全域時間切分的敏感度執行來量測。

[Meng et al., "Exploring Data Splitting Strategies for the Evaluation of
Recommendation Models", RecSys 2020](https://arxiv.org/pdf/2007.13237) 比較 leave-one-last、
依使用者的時間切分與全域時間切分；摘要指出切分方式 "can markedly alter the ranking of state-of-the-art recommender systems"，
§1 指出 leave-one-last 與依使用者的時間切分會 "leak" 未來證據。確切的候選協議：**未查證**。

[Hidasi & Czapp, "Widespread Flaws in Offline Evaluation of Recommender Systems",
RecSys 2023](https://arxiv.org/pdf/2307.14951) 把 "information leaking through time" 列為四項缺陷之一（§2.3），並建議採用依時間的切分。

## 全域截止點何時重要

- 重要：任何在跨使用者共用的訓練集上擬合參數或統計量的方法（MF、SASRec、EASE、熱門度計數、協同記憶、由其他使用者建立的檢索索引）。它們的訓練資料可能含有測試目標之後的資訊。
- 對洩漏不重要：凍結、免訓練的方法，其輸入只有目標使用者自己嚴格較早的事件、商品文字與候選清單。不存在跨使用者的管道。凍結模型的預訓練曝露是另一個問題，必須揭露（見 `llm-recsys-evaluation.zh.md`）。
- 對這種凍結方法套用全域截止點，只會刪掉有效的個人歷史。這會改變問題，無法消除洩漏。

## 全域截止點之後的目標選擇

[Gusak et al., §4.2](https://arxiv.org/pdf/2507.16289)：全域時間點之後的 "First" 互動，與其前一筆事件的時間間隔，遠大於其他目標，"which makes this target biased. Thus, we do not recommend using the First item after the global timepoint as a target."；§5 結論是使用 Last、Random 或 Successive 目標的 GTS 是適當的。§3.0.2：在 RecSys、SIGIR 與 CIKM 2022–2024 的 75 篇做離線評估的序列推薦論文中，77.3% 使用以 LOO 為基礎的切分，16% 使用以 GTS 為基礎的切分，6.7% 使用下一個商品設定的 GTS。

## 使用者隔離的陷阱

使用者隔離切分看起來是較強的洩漏防護，實際上悄悄改變了任務：

- 訓練式基線從未看過測試使用者的歷史，因此被當成冷啟動／未見過使用者的模型來評估。在推論時讀取使用者歷史的凍結方法則不受影響。這時比較有利於凍結方法，原因與它本身的品質無關。
- ID embedding 模型（MF、BPR、NCF、含使用者 ID 的 SASRec）需要 fold-in 步驟（Mult-VAE 式），或只用序列的編碼器；否則無法為這些使用者評分。
- 只有研究問題是泛化到新使用者時才使用，並明說。

## 驗證與模型選擇

- 超參數在驗證目標上選擇，絕不在測試目標上選擇。
- 若有測試使用者分區（開發對鎖定的測試），用它限制哪些保留標籤可以影響調參；這不會使測試使用者變成未見過的使用者。
- Gusak et al. §4.6 報告：以訓練加驗證資料重新訓練，會改變測試指標；要說明最終模型是否重新訓練。
