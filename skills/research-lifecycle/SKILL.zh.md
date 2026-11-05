# 研究生命週期：階段、紀錄、交接

英文 [SKILL.md](SKILL.md) 是執行規範。參考檔：[stage-map.zh.md](references/stage-map.zh.md)（交接順序與可選的第三方 skill）、[owner-communication.zh.md](references/owner-communication.zh.md)（提問、核准與角色分工）、[compute-and-budget.zh.md](references/compute-and-budget.zh.md)（加速器、付費 API、儲存空間與備份保存）、[handover-template.zh.md](references/handover-template.zh.md)（session 交接與新題目的起始文件）。

研究專案浪費的時間，多半來自方向漂移，少數才來自單一錯誤數字：實驗沒有對應任何研究問題、指令在 session（工作階段）之間遺失、已關閉的選項又被提出來。這個 skill 維護專案主軸（研究問題、紀錄、決定），並把每個階段交給負責的 skill。

## 何時使用

- 開始一個專案或後續題目；中斷或 context 重置（對話上下文清空）後接續工作。
- 里程碑（milestone）：做出決定、結果收錄、關卡通過或未通過、審查完成。
- 擁有者問進度、有人回報阻礙（blocker），或要把工作交接（hand-off）給另一個 session、agent（代理程式）或人。

不適用：選模型（`workflow-routing`）、合併前審查（`triple-review`）、worktree（同一 repository 的額外工作目錄）管理（`worktree-hygiene`）、壓縮 session（`context-hygiene`）、實驗設計（`experiment-planning`）、結果收錄（`experiment-contract`）、論文撰寫（`paper-writing`）。

## 階段對照

| 階段 | Skill | 進入時的產出物 | 離開時的產出物 |
|---|---|---|---|
| 生命週期 | 本 skill | 擁有者的要求、north-star file（北極星文件：專案規格或目標說明） | 研究問題檔、紀錄、下一個決定 |
| 文獻調查 | [research-survey](../research-survey/SKILL.zh.md) | 一個需要來源佐證的決定 | 已查證的來源紀錄 |
| 發想 | [research-ideation](../research-ideation/SKILL.zh.md) | 研究問題檔、來源紀錄 | 問題鏈、可行性紀錄、preliminary study（初步研究）計畫 |
| 實驗規劃 | [experiment-planning](../experiment-planning/SKILL.zh.md) | 已核准的方向 | 實驗卡、完整矩陣、追蹤表、預算 |
| 確認實驗內容 | [experiment-contract](../experiment-contract/SKILL.zh.md) | 已核准的實驗卡 | 啟動前檢查紀錄；收錄或被取代的結果列 |
| 驗證 | [research-verification](../research-verification/SKILL.zh.md) | 已收錄的結果列、diff（程式差異）、主張 | 驗證紀錄、處置表 |
| 論文撰寫 | [paper-argument](../paper-argument/SKILL.zh.md)、[paper-writing](../paper-writing/SKILL.zh.md) | 已驗證的結果 | 論證對照表、稿件、投稿檔案包 |

檢查未通過時，只把受影響的工作退回前一個階段。實驗規劃與啟動前檢查之間的實作，遵守專案的測試先行（test-first）與忠於原始碼（source fidelity）規則；為論證新做的分析，先通過 `experiment-contract` 的收錄檢查，才能進入論文。

## 專案主軸

1. North-star file：專案規格或目標說明。任何計畫或主張的決定之前先讀。
2. 研究問題檔：目前的研究問題集中在一個檔案，每個里程碑都重讀。每個計畫項目、實驗卡與論文章節都寫明它回答哪個問題。
3. status、tracker、handover 三個管理檔：擁有者的每個指令照原文記錄並寫明處理方式，指令一到就寫，不等到里程碑。時間一律取自 `date`。
4. 決策紀錄（decision log）：每個決定寫日期、適用範圍（專案、階段、文件）與它取代了什麼。提問或提案前先搜尋；已關閉的選項不再提出。只針對某一階段的限制保留原本的範圍，不會變成永久規則。

## 與擁有者溝通

- 先回答擁有者的問題，再報告狀態，最後才是工具操作。
- 每個問題自成一體：背景、各選項與後果、建議，以及需要擁有者給的確切答案。
- 多項決定一次討論一項，記下答案後再提下一項。
- 只回一句確認（例如「ok」）時，只核准擁有者點名的項目，加上必要的修正與驗證。
- 內部代號一律附白話名稱與一句說明。
- 送出前檢查回覆語言與術語說明，工具呼叫之間的簡短說明也一樣。
- 擁有者接手某份文件後，停止編輯該文件，改送修改建議。

## 里程碑

每個里程碑以 PR（pull request：合併請求）與專案的審查關卡（需要時用 `triple-review`）結束，並跑一次驗證者檢查（`research-verification`）。結果表、論文與專案的網頁（若有發布）一起從最新的 commit（版本提交）發布，並寫明 commit；每次建置的檔案（論文為雙語時含每個語言版本）放到同一個固定位置。

## 進度與阻礙

- 進度依實際輸出與程序狀態回報（pid file：記錄程序編號的檔案、紀錄檔最後一行、輸出數量、裝置使用量）；啟動指令只代表意圖。
- 狀態檢視：每個結果標一個證據狀態（planned 已規劃、running 執行中、executed 已執行、verified 已驗證、admitted 已收錄、superseded 已被取代）；報告最後寫下一個決定與由誰決定。
- 每個阻礙分類為授權、技術前置條件、資源，或非必要的準備工作。只擋住依賴它的工作；其他已授權的獨立工作繼續。
- 先有證據，再建平台：下一個里程碑是能改變「繼續、調整、停止」決定的最小結果。不能改變這個決定的基礎建設與擴充範圍延後。
- 運算資源要排程並編列預算（見 compute 參考檔）：加速器不閒置；付費呼叫前先估算費用、寫帳本、固定模型版本。

## 警訊

| 觀察 | 處理 |
|---|---|
| 提出的問題在決策紀錄中已有決定 | 引用該紀錄，不再詢問 |
| 發布的網頁或 PDF 比擁有者已看過的修改還舊 | 從最新的 commit 重新發布並寫明 commit |
| 有排隊的工作，加速器卻整夜閒置 | 找出卡住的原因並修復 |
| 擁有者核准過的文字被後來的修改改回去 | 從版本化的副本還原 |
| 用「等擁有者」擋住了不相依的工作 | 重新分類阻礙，其餘工作繼續 |

## 輸出

更新專案中的研究問題檔、決策紀錄與 status、tracker、handover；里程碑紀錄寫明 commit、審查與驗證報告；新題目另附起始文件。以專案的對話語言向擁有者報告。
