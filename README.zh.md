# Yao-skills

[English](README.md) | 繁體中文

與 coding agent 協作的可重用 skills。這是我的 Yao-Garyu 工具集的社群版，
讓你可以挑選適合的工作流程，帶進自己的專案。

Skill（技能）是一組讓 agent（代理）在特定任務中載入的指引。這些 skills 來自我的
軟體開發與研究工作，涵蓋工作安排、假設查驗、變更審查、技術解釋，以及推薦系統研究的評估與論文寫作。
可以先從下面的使用情境挑選，再依照[安裝方式](#安裝方式)加入你使用的 agent。

## 我什麼時候用哪個 skill

### workflow-routing：決定工作如何安排

開始較大的實作或研究工作前，我會用
[workflow-routing](skills/workflow-routing/SKILL.zh.md)，決定要直接處理、
先寫計畫、把獨立部分交給其他 agent，或安排獨立審查。
它會依照專案的模型與工具政策分配責任。修正錯字或範圍明確的小修改，通常直接完成並檢查即可。

例如，一個功能同時影響介面、實作與幾組獨立測試。Routing（工作分配）會先釐清
哪些事情有先後依賴、哪些可以平行進行、誰負責整合，以及如何確認完成。

> 用 workflow-routing 安排這個功能：先確認依賴關係、實作責任與必要檢查，再開始處理。

### first-principles：查驗下一步依賴的假設

當修正方法或重要結論依賴尚未驗證的前提，我會用
[first-principles](skills/first-principles/SKILL.zh.md)（第一性原理）。
常見時機包括反覆失敗、結果好得出乎預期、收到審查意見，或有人提議降低門檻、跳過檢查。

例如，同一個測試在兩台機器上的結果不同，我會先檢查它實際讀取的輸入、環境與設定，
再依據證據決定修正位置。研究中遇到異常分數時，也會先核對資料識別與指標計算方式，
再解讀結果。

> 用 first-principles 查這個測試為什麼失敗：指出目前的假設，以及能確認或推翻它的最小觀察。

### recsys-evaluation：確認推薦系統的分數代表什麼

設計、檢查或撰寫離線推薦系統評估之前，或換了協議後結果的方向相反時，我會用
[recsys-evaluation](skills/recsys-evaluation/SKILL.zh.md)。它依研究問題推導切分、候選集合、
前處理與比較對象，不沿用現成設定，並寫明每個方法可以讀到什麼資訊。
只是在 notebook 上做快速檢查時，不需要用它。

例如，凍結的 LLM 排序器在抽樣候選清單上的分數，接近訓練式序列模型。寫下這個結論之前，
我會檢查切分方式與各方法看得到的資訊、負例數量對應的隨機排序期望值、每個方法是否拿到
相同的候選與歷史，以及失敗的查詢如何計入。

> 用 recsys-evaluation 檢查這份評估計畫：對照研究問題核對切分、候選協議與比較對象，並列出每個方法可以讀到什麼。

### paper-argument：把結果整理成論證

已經有結果、但論文還沒說明方法為什麼有效時，我會用
[paper-argument](skills/paper-argument/SKILL.zh.md)：和指導教授開會前、投稿前，
或審稿人問某個元件補了什麼之後。它把動機、亮點、方法與證明整理成四個部分，
並規劃證明所需的機制證據。

例如，一個方法把幾個簡單的分數項加權相加，結果勝過基線。我會替每一項寫出它代表什麼、
為什麼選它、為什麼有效，再規劃檢驗每項主張的分析，例如移除某一項、把使用者的歷史換成
另一位使用者的歷史，或拆解分數差距，並在計算之前先寫下哪種結果會推翻主張。

> 用 paper-argument 整理這份草稿：寫出四個部分、從主張到證據的對照表，以及解釋方法為什麼有效的分析計畫。

### paper-writing：讓正文只談一個論證

撰寫、刪減或重組論文的內文、表格與圖時，我會用
[paper-writing](skills/paper-writing/SKILL.zh.md)：草稿超過頁數上限、讀起來像實驗紀錄，
或資料集與結果有變動、文字必須跟著更新。它讓同一個問題從引言貫穿到結論，把數字放進表格，
並決定哪些內容留在正文、哪些移到附錄。

例如，草稿超出頁數上限兩頁，三張表重複同一組數字。我會標出每個段落與表格服務的問題，
合併表格，把設定與次要結果移到附錄，最後把每個量化主張對照結果檔重新驗證。

> 用 paper-writing 處理這份草稿：標出每個段落與表格服務的問題，建議哪些要刪除、合併或移到附錄，並列出需要重新驗證的量化主張。

### wait-what：補足我沒跟上的解釋

當我無法跟上說明，例如術語沒有定義、結論省略了前提，或回答太短而缺少必要推理，
我會主動呼叫 [wait-what](skills/wait-what/SKILL.zh.md)。

這個台灣改寫版會用繁體中文重新建立說明，保留技術術語原文並附上簡短解釋，
先給具體例子，再補需要的形式化細節。證據與不確定性都要保留，說明完再接續原本的工作。
它只處理當次解釋。

> wait-what：再解釋一次為什麼這兩個結果不能直接比較。先說各自量測什麼，
> 以及什麼前提成立時才可以比較。

實際呼叫指令見下方各 agent 的安裝表。
`workflow-routing`、`first-principles`、`recsys-evaluation`、`paper-argument` 與 `paper-writing`
也可以由 agent 依任務選用；`wait-what` 需要我主動要求。

## 哪些交給 agent 依情境選用

安裝後，以下 skills 由 agent 在工作符合說明時選用。實際選用仍取決於 agent 與可用工具。

| Skill | 在我的流程中何時使用 |
|---|---|
| [karpathy-guidelines](skills/karpathy-guidelines/SKILL.zh.md) | 寫程式與審查時，明確交代假設、保持修改範圍集中，並定義完成檢查。 |
| [triple-review](skills/triple-review/SKILL.zh.md) | 專案要求合併前經過多模型獨立審查時，逐項核對意見，再修正確認成立的問題。一般文件使用驗證工具檢查。 |
| [worktree-hygiene](skills/worktree-hygiene/SKILL.zh.md) | 建立、檢查或移除 Git worktree（同一 repository 的獨立工作目錄）時，確認責任歸屬並保留未完成工作與結果。 |
| [context-hygiene](skills/context-hygiene/SKILL.zh.md) | 對話變長或需要換 session（工作階段）時，保存決策、未解問題與下一步。 |
| [tc-review](skills/tc-review/SKILL.zh.md) | 送出或發布繁體中文前，檢查台灣用語與技術術語。 |

另外兩個則依我的要求使用：

| Skill | 我何時要求使用 |
|---|---|
| [project-status-review](skills/project-status-review/SKILL.zh.md) | 我明確要求狀態檢視時，依 repository 證據核對已完成工作、阻塞與下一個決策。 |
| [distilled-caveman-lite-accuracy](skills/distilled-caveman-lite-accuracy/SKILL.zh.md) | 我希望回答更短，同時保留必要條件、識別資訊與不確定性時。 |

## 如何放進我的開發流程

我會先讀專案規格與現況。工作較大時，先記錄範圍與驗收方式；需要協調分工時再用 routing。
修正錯誤先建立會失敗的 regression test（迴歸測試：重現錯誤並避免再次發生），
再完成足以通過驗證的最小實作。變更通過專案要求的檢查與審查後，才合併 pull request（合併請求）。

研究工作則先找出能影響「繼續、調整或停止」決策的最小有效真實資料實驗。
看過結果後，再擴充實作或實驗組合。當某個假設開始決定要做什麼、能主張什麼時，
就適合用 first-principles 查驗。做推薦系統評估時，先用 recsys-evaluation 核對協議；
結果出來後，用 paper-argument 整理方法為什麼有效，再用 paper-writing 把論證放進頁數限制。

每個里程碑會更新 `status.md` 的現況與證據、`tracker.md` 的剩餘工作，
以及 `handover.md` 的下次接續位置。任何階段只要需要重新理解推理，我都可以用 `wait-what`。

## 我還會搭配的 skills

| 搭配的 skill | 我的使用方式 |
|---|---|
| [ponytail](https://github.com/DietrichGebert/ponytail) | 實作與審查時，優先使用既有程式碼、標準函式庫與平台原生功能，檢查是否需要新增抽象設計，讓解法維持精簡。 |
| [i-have-adhd](https://github.com/ayghri/i-have-adhd) | 先呈現下一個動作，把工作拆成容易執行的步驟，讓目前進度容易掌握。 |

這兩個是獨立專案，安裝方式見各自的說明。精簡回答如果省略了我需要的背景，
我就用 `wait-what` 展開當次解釋。

## 安裝方式

### 安裝 coding agent

選擇你使用的 agent 即可。以下終端機指令適用於 macOS 或 Linux；前置需求、登入與其他
支援平台見各自的官方文件。Pi 的 npm 指令需要 Node.js 與 npm；Cursor 指令安裝的是終端機 agent。

| Agent 與官方文件 | 安裝指令 | 啟動 |
|---|---|---|
| [Claude Code](https://code.claude.com/docs/en/setup) | `curl -fsSL https://claude.ai/install.sh \| bash` | `claude` |
| [Codex](https://learn.chatgpt.com/docs/codex/cli) | `curl -fsSL https://chatgpt.com/codex/install.sh \| sh` | `codex` |
| [Grok Build](https://docs.x.ai/build/overview) | `curl -fsSL https://x.ai/cli/install.sh \| bash` | `grok` |
| [Cursor](https://prod.cursor.com/docs/cli/installation) | `curl https://cursor.com/install -fsS \| bash` | `agent` |
| [Pi Agent](https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/docs/quickstart.md) | `npm install -g --ignore-scripts @earendil-works/pi-coding-agent` | `pi` |

### 把 skills 加入 Claude Code

在 Claude Code 內執行：

```text
/plugin marketplace add solitude6060/Yao-skills
/plugin install yao-skills@yao-skills
```

執行 `/reload-plugins` 或開啟新 session，再用
`/yao-skills:wait-what`、`/yao-skills:workflow-routing` 或
`/yao-skills:first-principles` 呼叫技能。詳見[套件安裝文件](https://code.claude.com/docs/en/discover-plugins)。

### 把 skills 加入 Codex、Grok Build、Cursor 或 Pi Agent

這四種 agent 都會讀取 `~/.agents/skills` 的本機使用者 skills。
安裝 Git 後，執行一次即可讓這台機器上的上述 agent 使用整套 skills：

```bash
mkdir -p "$HOME/Research" "$HOME/.agents/skills"
git clone https://github.com/solitude6060/Yao-skills.git "$HOME/Research/Yao-skills"

for skill in "$HOME/Research/Yao-skills/skills"/*; do
  destination="$HOME/.agents/skills/${skill##*/}"
  if [ ! -e "$destination" ] && [ ! -L "$destination" ]; then
    ln -s "$skill" "$destination"
  fi
done
```

已有 repository 時跳過 clone 指令；既有的同名 skill 會保留。
只想安裝部分 skills，可以個別連結需要的資料夾，省略迴圈。
開啟新的 agent session 後選取 skill：

| Agent 與技能文件 | 明確呼叫範例 |
|---|---|
| [Codex](https://learn.chatgpt.com/docs/build-skills) | `$wait-what`；用 `/skills` 瀏覽。 |
| [Grok Build](https://docs.x.ai/build/features/skills-plugins-marketplaces) | `/wait-what`；用 `/skills` 瀏覽。 |
| [Cursor](https://prod.cursor.com/docs/skills) | 在 Agent 對話輸入 `/`，選取 `wait-what`。 |
| [Pi Agent](https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/docs/skills.md) | `/skill:wait-what`。 |

其他 skill（例如 `workflow-routing`、`first-principles`、`recsys-evaluation`）也使用相同格式。
Cursor 的共用使用者目錄適用於本機 session；遠端 agent 需要在其執行環境安裝 skills。

### 更新

Claude Code 套件透過 `/plugin` 更新 marketplace 與已安裝套件。
使用上述連結安裝時，更新 repository：

```bash
git -C "$HOME/Research/Yao-skills" pull --ff-only
```

連結會讀到更新後的檔案；若尚未出現變更，開啟新 session。

## 延伸閱讀

- [全部 skills](skills)：各工作流程的指引與參考資料。
- [專案指引範本](templates/CLAUDE.zh.md)：依專案需求調整的起點。
- [選用繁體中文品質 hook](hooks/tc-quality-hook/README.zh.md)：Claude Code 的整合方式。

## 授權

MIT。作者與上游來源見 [LICENSE](LICENSE) 及 [NOTICE.md](NOTICE.md)。
