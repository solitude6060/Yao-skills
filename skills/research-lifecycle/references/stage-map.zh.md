# 階段對照與交接

英文版 [stage-map.md](stage-map.md) 為執行規範。

下面的順序在每個研究中完整跑一次，之後每個里程碑再跑其中一部分。一個階段從它的進入產出物開始，在離開產出物存在於專案檔案中時結束。對話不是產出物：只存在於對話中的結果、決定或計畫，都還沒有交接。

## 交接順序

| 步驟 | 階段 | Skill | 進入產出物 | 離開產出物 |
|---|---|---|---|---|
| 1 | 開始或接續 | `research-lifecycle` | 擁有者的要求；north-star file（北極星文件：專案規格或目標說明） | 研究問題檔；status、tracker、handover 三個管理檔；決策紀錄 |
| 2 | 文獻調查 | `research-survey` | 一個需要來源佐證的決定 | 已查證的來源紀錄；實務對照；同期作品比較表 |
| 3 | 發想 | `research-ideation` | 研究問題檔；來源紀錄 | 問題鏈；用真實資料做的可行性紀錄；範圍；附「繼續或停止」條件的 preliminary study（初步研究）計畫 |
| 4 | 實驗規劃 | `experiment-planning` | 已核准的方向或初步研究計畫 | 實驗卡；完整矩陣與追蹤表；使用者群（cohort）；資訊對等的決定；預算 |
| 5 | 契約的啟動前檢查 | `experiment-contract` | 已核准的實驗卡與規格 | preflight（啟動前檢查）紀錄：固定的身分、在真實資料上的 smoke run（小規模試跑）、重跑清單 |
| 6 | 執行 | `experiment-contract`（執行模式） | preflight 紀錄 | 原始輸出、紀錄檔、成本欄位、失敗紀錄 |
| 7 | 契約的收錄 | `experiment-contract` | 原始輸出 | 收錄、加標籤或被取代的結果列；結果表與各項紀錄同步 |
| 8 | 驗證 | `research-verification` | 已收錄的結果列；diff（程式差異）；主張 | 驗證紀錄；分流表；修正紀錄（fix log） |
| 9 | 論證 | `paper-argument` | 已驗證的結果 | 論證對照表；附事先宣告判讀的機制分析 |
| 10 | 撰寫 | `paper-writing`；每一節都和目標會議的優秀論文對照寫法 | 論證對照表；已收錄的表格 | 稿件、表格、圖 |
| 11 | 論文檢查 | `research-survey`（引用檢查）；`research-verification`（針對論文） | 稿件 | 引用紀錄；數字與主張的驗證 |
| 12 | 審查與 rebuttal（作者回覆） | `paper-argument`（審查與回覆）；`paper-writing`（投稿檔案包） | 稿件；審查意見 | 分流後的意見；rebuttal 備用分析；投稿檔案包 |
| 13 | 決定 | `research-lifecycle` | 步驟 1 到 12 的產出 | 繼續、調整、停止或交接；交接文件或新題目的起始文件 |

實作位於步驟 4 與 5 之間。它遵守專案的測試先行（test-first）與忠於原始碼（source fidelity）規則（官方原始碼優先、固定版本、記錄差異）；它的離開產出物是通過測試的程式，以及 preflight 會固定下來的來源紀錄。步驟 9 為論證新做的分析也是結果：先通過契約收錄（步驟 7），才能進入論文。

每個步驟都可搭配的 skill：數字回報或據以行動之前，用 `explain-the-number`；沿用的假設會決定結論時，用 `first-principles`；研究評估推薦系統時，在步驟 4、5、7、8 用 `recsys-evaluation`；專案要求時，用 `triple-review` 結束里程碑；委派工作時，用 `workflow-routing`。

## 退回路徑

檢查未通過時，只把受影響的工作退回。研究的其他部分繼續。

| 在哪裡發現未通過 | 退回到 | 通用案例 |
|---|---|---|
| Preflight：身分不符或 smoke run 失敗 | 該實驗卡的實作 | 一個 set-wise（一次讀入整組候選）請求在最大候選數時記憶體不足；只重建那個設定 |
| 收錄：仍有未解決的執行失敗、缺成本欄位 | 受影響單位的執行 | 一批實驗中部分使用者遇到伺服器錯誤，只重跑這些使用者 |
| 驗證：數字與原始檔不符 | 受影響結果列的收錄 | 論文表格引用了多列中最好的一列；改用已收錄的那一列 |
| 驗證：高嚴重度的協定問題 | 實驗規劃：用對照實驗回答 | 方法與基線之間的資訊不對等，以一次在雙方都拿掉該資訊的執行回答 |
| 論文檢查：被引用的主張不在來源中 | 該句的文獻調查引用檢查 | 一筆參考文獻被寫成包含它沒有的內容 |
| 初步研究的關卡未通過 | 發想：調整或停止 | 某題目的前提在真實資料上不成立；該題目停止 |

## 可選的第三方 skill

已安裝時使用。本系列的每個 skill 沒有它們也完整；它們的內容不複製到這裡。

| 搭配的 skill（已安裝時） | 階段 | 用途 | 本系列仍負責 |
|---|---|---|---|
| `deep-research` | 文獻調查 | 長篇敘述式文獻報告 | 替它定問題並查證它的引用（`research-survey`） |
| `idea-evaluator` | 發想 | 替已存在的想法評分 | 在真實資料上的可行性、範圍、沿用前作並記錄差異（`research-ideation`） |
| `tech-paper-template`、`benchmark-paper-template` | 發想、論證 | 論文骨架 | 問題鏈與機制證據（`paper-argument`） |
| `paper-writer`、`intro-drafter` | 撰寫 | 由已驗證的材料起草文字 | 擁有者的寫作規則與主張檢查（`paper-writing`） |
| `paper-polish` | 撰寫 | 不改變意思的語言潤飾 | 每次潤飾後重新驗證數字與主張 |
| `figure-designer` | 撰寫 | 圖的版面 | 每個語言版本中圖與文字一致 |
| `pre-submission-reviewer`、`academic-paper-review` | 審查 | 審稿人角度的稽核 | 每一則意見都對照來源查證（`research-verification`） |
| `rebuttal-guidance` | 作者回覆 | 回應實際的審稿意見 | 審查意見到達之前就準備好的 rebuttal 備用分析 |
