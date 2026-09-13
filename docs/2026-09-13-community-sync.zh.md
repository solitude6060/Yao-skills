# 社群版 0.8.0 同步紀錄

日期：2026-09-13。[同步計畫](2026-09-13-community-sync-plan.zh.md)。

## 來源與範圍

社群版基準為 `ee0e5ae00e452a26d8b9972f3c4094094eff34f6`（0.3.0）。來源為
Yao-Garyu research-toolkit 0.8.0，合併提交
`38719bebcf2b5f67e7ce6dbdb14041a6b2495975`。wait-what 分支先前已推送，
本日透過來源 PR #1 完成 main 整合。本次讀取本機正典來源；社群版使用者無需
存取作者的私人來源 repository。

目前提供八個原創技能、karpathy-guidelines 與台灣版 wait-what。移除十四個
歷史 OMC 複本：`ralph`、`plan`、`deep-interview`、`deep-dive`、`learner`、
`skillify`、`sciomc`、`autoresearch`、`ralplan`、`ai-slop-cleaner`、`team`、
`release`、`autopilot`、`ultrawork`。NOTICE.md 保留其歷史授權，上游安裝及
既有未追蹤執行狀態未受修改。

## 社群版調整

| 範圍 | 調整 |
|---|---|
| 路由 | 讀專案指引指定的政策，預設位置範例為 docs/MODEL_ROUTING.md，不散布個人模型或帳號表 |
| 三個獨立審查 | 三個獨立對話、不同模型家族或明確允許的重疊、固定版本及對應已觀察失敗的備援 |
| 對話管理 | 成本改為明列計算假設的示意表，停止行程仍需授權 |
| 第一原理案例 | 不包含私人事件，依 SEC、NASA/JPL、OpenSSL 原始來源確認公開案例，修正沿用的部署描述 |
| 狀態報告 | 只列憑證名稱與設定狀態，移除個人政策參照 |
| Wait-what | 保留明確呼叫、Codex 設定、證據限制及完整上游 MIT 聲明 |
| 文件 | 補上實務流程及技能選擇，使用持久安裝路徑，更新行為範本及雙語對照 |
| Hook | 程式位元組不變，文件說明選用的雜湊自我檢查機制與限制 |

README 範例根據已讀取紀錄，整理測試設定隔離、依證據拒絕審查誤報，以及分別
追蹤實作與操作者驗收。研究指引依目前先取得證據的政策及各專案既有有效性
規則。範例只呈現工作方式，未包含私人專案身分、結果、策略、帳號設定或原始
紀錄，也未主張每個歷史案例都曾實際呼叫所列技能。

## 驗證

交付前在下方記錄驗證及獨立指引情境檢查。交付範圍固定為十個技能目錄、兩份
README、兩個套件設定、NOTICE.md、雙語範本及 hook 說明。沒有修改可執行
功能或實驗有效性定義。

skill-creator 內附驗證器的允許欄位比目標執行環境少，會拒絕既有 argument-hint
及 disable-model-invocation。保留受支援欄位，改用理解執行環境的設定檢查；
不修改驗證器或放寬 wait-what 的呼叫政策。

這些檢查確認套件及指引一致性，尚未量測理解成效、測試每個模型或證明每個
執行環境都已安裝。


### 完成的驗證

- `claude plugin validate .claude-plugin/plugin.json`：通過，沒有警告。
- `claude plugin validate .`：marketplace 通過，沒有警告。
- 來源與社群版的十個技能名稱一致，均有繁體中文對照檔。
- 執行環境設定檢查：名稱、說明、wait-what 明確呼叫及
  `allow_implicit_invocation: false` 通過；wait-what 授權與 Codex 設定位元組
  與來源相同。
- 本機 Markdown 連結、私人絕對路徑、README／範本／hook 章節結構、hook 程式
  未變及 `git diff --check` 均通過。
- 通用技能驗證器三個通過，七個僅因既有且受執行環境支援的設定欄位被拒絕。
  原始訊息及三十四個內容雜湊見[驗證收據](2026-09-13-community-validation.json)。

### 獨立指引情境檢查

另開原生 verifier（驗證代理），指定 Research Medium、GPT-5.6 Sol、high。
呼叫介面記錄此選擇，未提供另一份後端身分資訊。這是唯讀指引評估，未實際
啟動各代理執行環境測試。

| 情境 | 評估結果 |
|---|---|
| 沒有路由或任務指引檔的拼字修正 | 通過：可直接完成已授權工作 |
| wait-what 重講只有合成測試的結果 | 通過：保留證據界線及進行中工作，不增加執行授權 |
| 一個設定的審查者回傳空白，結束碼為零 | 通過：不能視為核准或任意改用備援，必要審查仍未完成 |
| 安裝文件提到 ralph 及 wait-what | 通過：只修改文件，不啟動流程 |
| 十八萬快取輸入的示意計算 | 通過：依所列假設為三萬四千單位，不授權停止無關行程 |

驗證代理提出一項中嚴重度紀錄缺漏：同步紀錄提到情境結果時，結果尚未附上。
本段及 JSON 收據已補齊，未提出技能行為問題。最後一致性檢查另將狀態技能
繁中檔殘留的個人政策標記改成「專案管理紀錄」，受審情境的輸入未變。
只補紀錄不需要再次進行指引審查。

## 面向初次閱讀者的 README 改寫

兩份 README 已說明作者何時使用 workflow-routing、first-principles 與 wait-what、
其他技能的情境選用，以及 ponytail／i-have-adhd 的搭配方式。入口頁移除內部設定
與交付稽核敘述，補上 Claude Code、Codex、Grok Build、Cursor、Pi Agent 本體及
技能的安裝方式；指令與技能載入／呼叫方式均連結官方文件。

2026-09-13 驗證：本機 Markdown 連結、十個技能與五種 agent 的涵蓋範圍、雙語
標題結構與程式區塊一致性，以及安裝指令呈現均通過。擷取的技能連結指令通過
Bash 與 zsh 語法檢查，並在各自的全新與既有安裝測試目錄執行兩次。既有資料夾、
檔案與失效連結均保留，新連結均指向預期技能目錄。未執行 agent 本體安裝或登入。
本次僅變更 Markdown，技能內容、執行環境設定與 0.8.0 版本未變更。本次 README
雜湊如下：

先前 community-validation.json 保留為 0.8.0 釋出快照；其中 README 雜湊
對應本次文字改寫之前的內容。

| File | SHA-256 |
|---|---|
| README.md | `a13676e3b008f19bb3af58c964052cb1f213627d623dc34064b3826e21e0614f` |
| README.zh.md | `333b3d8fb6f5f0223b67c1144dca7f4a4dfc7104d35b347f6af073207b742a96` |
