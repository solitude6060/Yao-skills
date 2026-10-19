# 資料集與前處理

英文版 [datasets-and-preprocessing.md](datasets-and-preprocessing.md) 為執行規範。

建立或重用處理過的資料集之前閱讀。前處理的決定會改變使用者人數、目標與分數，而且常常不在論文正文中顯示。

## 有官方 benchmark 檔案時就使用

資料集發布者提供切分時，使用它並記錄檔案雜湊值。自行建立、「遵循相同規則」的切分，常因篩選順序不同而使使用者與商品數量不同（去重在 k-core 之前或之後、k-core 迭代到穩定或只做一次、同時間事件的處理）。

Amazon Reviews 2023（[McAuley Lab 資料集頁面](https://amazon-reviews-2023.github.io/)；
論文 [Hou et al., arXiv 2403.03952](https://arxiv.org/abs/2403.03952)，該論文介紹的資料集含超過 5.7 億則評論與 4,800 萬個商品）。
[benchmark scripts README](https://github.com/hyp1231/AmazonReviews2023/tree/main/benchmark_scripts)
說明：

- 重複："We remove repeated reviews (those from the same pair of user & item,
  but may with different review text and ratings) and only keep the earliest ones."
- k-core："k = 0 or 5"。
- 最後一筆留出切分："For each user, the latest review will be used for testing, the
  second latest review will be used for validation, and all the remaining reviews are
  used for training."
- 時間戳記切分：訓練 (−∞, t1)，驗證 [t1, t2)，測試 [t2, +∞)，固定的
  毫秒截止時間 t1 = 1628643414042、t2 = 1658002729837。

## k-core 篩選

- k-core 保留至少有 k 筆互動的使用者與商品，通常迭代到穩定。寫明 k、是否迭代，以及在去重之前或之後執行。
- [Hidasi & Czapp, §2.2 "Overzealous preprocessing"](https://arxiv.org/pdf/2307.14951)
  提醒不要從經過大量前處理的資料得出一般性的主張。
- 報告最終的使用者、商品與事件筆數，並與官方或先前發表的筆數比較。筆數不符是需要解釋的發現，不能忽略。

## 重複的（使用者，商品）互動與重複消費

- 選項：保留最早、保留最晚、全部保留。Amazon Reviews 2023 benchmark 保留最早（見上）。
- RecBole 的 `rm_dup_inter`："if `rm_dup_inter=first`, we will keep the first user-item
  interaction in duplicates; if `rm_dup_inter=last`, ... the last ... Defaults to
  `None`"（不移除）——
  [RecBole data settings](https://recbole.io/docs/user_guide/config/data_settings.html)。
- [Li et al., "Repetition and Exploration in Sequential Recommendation", SIGIR 2023](https://dl.acm.org/doi/10.1145/3539618.3591914)
  （[PDF](https://staff.fnwi.uva.nl/m.derijke/wp-content/papercite-data/pdf/li-2023-repetition.pdf)）：
  資料集中的重複商品 "often act as easy shortcuts"；模型呈現重複偏差。保留重複時，分開報告目標為重複商品與目標為新商品的結果。
- 無論如何選擇，除非研究問題是重複推薦，目標不得出現在使用者可見的歷史中。

## 時間戳記相同的事件

- 許多資料集的時間戳記解析度很粗。Hidasi & Czapp §2.1 指出 Amazon 與 Steam 為日等級解析度，MovieLens-10M 有大量時間戳記重複；MovieLens-10M 的檔案依使用者與商品 ID 排序，因此以商品 ID 排序同時間事件，會對不同使用者產生相同的假序列（[§2.1](https://arxiv.org/pdf/2307.14951)）。
- 依資料集原始的列順序（或明確的次要時間戳記）決定同時間事件的先後。絕不以商品 ID 決定。
- 可見歷史必須在（時間戳記，列順序）上嚴格早於目標。

## 常見資料集與版本為何重要

| 資料集 | 備註 | 來源範例 |
|---|---|---|
| MovieLens-1M | 經 SASRec 前處理後為 6,040 位使用者、3,416 個商品；歷史很長（平均每位使用者 163.5 個行為） | [SASRec Table II](https://arxiv.org/pdf/1808.09781) |
| Amazon 2014（Beauty、Sports、Toys、Games 等） | 2014 年爬取；各類別的 5-core 檔案被廣泛重用；Beauty 在 SASRec 為 52,024 位使用者／57,289 個商品，在 BERT4Rec 為 40,226／54,542（前處理不同） | [SASRec Table II](https://arxiv.org/pdf/1808.09781)、[BERT4Rec Table 1](https://arxiv.org/pdf/1904.06690) |
| Amazon Reviews 2023 | 新的爬取，有官方去重規則與官方切分；數字無法與 2014 年版本比較 | 見上方連結 |
| Steam | SASRec 為 334,730 位使用者／13,047 個商品；BERT4Rec 為 281,428／13,044 | 同上兩張表 |
| Yelp | 有多個版本；DaisyRec、Ji et al. 使用 | [DaisyRec 2.0](https://arxiv.org/pdf/2206.10848)、[Ji et al.](https://arxiv.org/pdf/2010.11060) |

兩篇論文使用相同的資料集名稱，不代表資料相同：上表 Beauty 的筆數在 SASRec 與 BERT4Rec 之間就不同。要寫明發布年份、篩選條件與切分檔。

## 商品目錄與歷史可見性

- 商品目錄只定義一次（訓練中出現的所有商品，或切分中的所有商品），並套用到每個方法。
- 在截止點凍結的商品目錄，可能漏掉出現在使用者可見歷史中的商品。若某個方法仍把這些商品當文字讀取，另一個方法卻無法為它們建立索引，兩個方法看到的證據就不再相同。要檢查每個方法的歷史商品數量，不只檢查使用者人數。
- 驗證／測試中從未出現在訓練的商品，ID 式模型無法推薦。計算並報告這類目標的數量。

## 最低限度的前處理紀錄

來源檔案與雜湊值；去重規則；k 與篩選順序；同時間事件規則；切分規則或官方切分檔；最終的使用者／商品／事件筆數；歷史長度為 0 或低於門檻的目標數量；商品目錄的定義；每個查詢的證據雜湊值與候選雜湊值。
