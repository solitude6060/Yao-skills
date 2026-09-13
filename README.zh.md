# Yao-skills

[English](README.md) | 繁體中文

與 coding agent 協作的可重用 skills。這是我的 Yao-Garyu 工具集的社群版，
讓你可以挑選適合的工作流程，帶進自己的專案。

Skill（技能）是一組讓 agent（代理）在特定任務中載入的指引。這些 skills 來自我的
軟體開發與研究工作，涵蓋工作安排、假設查驗、變更審查與技術解釋。
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

### wait-what：補足我沒跟上的解釋

當我無法跟上說明，例如術語沒有定義、結論省略了前提，或回答太短而缺少必要推理，
我會主動呼叫 [wait-what](skills/wait-what/SKILL.zh.md)。

這個台灣改寫版會用繁體中文重新建立說明，保留技術術語原文並附上簡短解釋，
先給具體例子，再補需要的形式化細節。證據與不確定性都要保留，說明完再接續原本的工作。
它只處理當次解釋。

> wait-what：再解釋一次為什麼這兩個結果不能直接比較。先說各自量測什麼，
> 以及什麼前提成立時才可以比較。

實際呼叫指令見下方各 agent 的安裝表。
`workflow-routing` 與 `first-principles` 也可以由 agent 依任務選用；`wait-what` 需要我主動要求。

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
就適合用 first-principles 查驗。

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

`workflow-routing` 與 `first-principles` 也使用相同格式。
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
