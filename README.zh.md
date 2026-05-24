# yao-skills

[English](./README.md) | 繁體中文

一組精簡、有觀點的 Claude Code skills，涵蓋 code review、incident triage、workflow routing、專案健康檢查；另外整併了 [oh-my-claudecode](https://github.com/Yeachan-Heo/oh-my-claudecode) 的部分編排類 skills，以及 [andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills) 的行為準則。

這是一份私人工具集的**公開、去識別化**版本。原本引用具體專案 / PR / 業務細節的範例，已替換為通用範例 — 方法論保留，但不外洩內部脈絡。

## Skills

### 自製

| Skill | 用途 |
|---|---|
| `triple-review` | 依 orchestrator 條件選 reviewer 的三審 PR review：Claude Code 用 `codex` + `agy`/`gemini` + `claude-mm`；Codex 用 `claude` + `agy`/`gemini` + `claude-mm`；含 severity triage、TDD 修復循環、自動 merge gate |
| `first-principles` | 假設稽核與 incident triage 紀律：5 題稽核、ground-truth 驗證、hotfix 強制雙 / 三審 |
| `workflow-routing` | 依 task 類型、風險等級、Opus / Codex 剩餘配額挑 A / B / C / D / Mini 工作流程 |
| `project-status-review` | 產生完整專案健康報告：code stats、branch 偏離度、blockers、依優先序排定的下一步建議 |
| `context-hygiene` | 管理 session context 成本：何時 `/compact`、何時改用 handover-doc + `/clear`；快取成本算式（cached input 是 0.1 倍而非零；output 不會被快取）；handover 範本；loop session checkpointing；以及 task → 工具的對應路由（Sonnet / Opus / codex / gemini-cli / claude-mm） |
| `distilled-caveman-lite-accuracy` | Lite 回答壓縮 — 移除客套與贅詞，保留 100% 技術準確度。保留限定詞、程式碼識別字、版本、步驟順序、安全脈絡。破壞性操作、驗證、加密、合規等高風險情境自動展開。觸發詞："caveman-lite"、"lite mode"、"brief but accurate"、"less tokens"、"回答短一點，但不要犧牲技術準確度" |

### 自 oh-my-claudecode 整併（MIT，詳見 `NOTICE.md`）

`ralph`、`plan`、`deep-interview`、`deep-dive`、`learner`、`skillify`、`sciomc`、`autoresearch`、`ralplan`、`ai-slop-cleaner`、`team`、`release`、`autopilot`、`ultrawork`。

### 自 andrej-karpathy-skills 整併（MIT，詳見 `NOTICE.md`）

| Skill | 用途 |
|---|---|
| `karpathy-guidelines` | 由 Andrej Karpathy 對 LLM coding 常見錯誤的觀察萃取出的行為準則：先想再寫、優先簡單、外科手術式修改、目標導向執行 |

#### 編排模式怎麼挑

OMC tier-0 編排類 skill，依任務形態挑選：

| 模式 | 運作方式 | 適用情境 |
|---|---|---|
| `autopilot` | 獨立自主的單一 lead agent | 從 2–3 行構想直接做出獨立功能 / 原型 |
| `team` | 5 階段管線（plan → prd → exec → verify → fix） | 跨多檔案、需要同儕架構審查的變更 |
| `ralph` | 持續性、自我參照、嚴格驗證的迴圈 | 必須徹底修好的關鍵 prod bug |
| `ultrawork` | 最大平行度、非 team 模式 | 跨多個無關 codebase 的大規模 refactor |
| `ralplan` | 執行前的共識規劃 gate | 模糊 / 不清楚的「ralph 一下」「autopilot 一下」請求 |

選擇順序：模糊請求 → 先 `ralplan`。獨立原型 → `autopilot`。多檔案、設計敏感變更 → `team`。必修 prod bug → `ralph`。可平行的批次 refactor → `ultrawork`。

## 安裝

### Claude Code（原生 — 建議用法）

兩條路：

**A. 一次性 marketplace 安裝（最簡）**

```
/plugin marketplace add solitude6060/Yao-skills
/plugin install yao-skills@yao-skills
```

開新 Claude Code session 後，全部 20 個 skill 都會透過 `Skill` tool 或 `/yao-skills:<skill-name>` 被叫起。

**B. 單一 skill 複製（只挑想要的）**

```bash
git clone https://github.com/solitude6060/Yao-skills /tmp/yao-skills
cp -r /tmp/yao-skills/skills/triple-review ~/.claude/skills/
cp -r /tmp/yao-skills/skills/first-principles ~/.claude/skills/
# ...其他依需求
```

Skill 透過 `Skill` tool 或 `/<skill-name>` 被叫起。

### `CLAUDE.md` 範本

```bash
cp templates/CLAUDE.md ~/.claude/CLAUDE.md   # 僅在你還沒有 CLAUDE.md 時執行
```

拷貝完依自己需求調整。

#### 範本的核心九條

`templates/CLAUDE.md` 是給 Claude Code 用的全域行為合約，偏好「嚴謹 + 稽核軌跡」勝於「速度」。九個段落：

1. **Spec Before Code** — 先讀 SPEC / README；偏離要先寫 ADR。code ≠ spec。
2. **Test Before Implementation** — Red → Green → Refactor。Bug fix = 重現測試 + 修正，不能只有修正。
3. **Surgical Changes + Audit Trail** — 只動任務需要的部分。Commit subject 寫「做了什麼」，body 寫「為什麼 + SPEC / ADR / issue 連結」。決策點放 observability event，不要塞 inline comment。
4. **Plan in Files, Not Chat** — 非瑣碎工作先把 plan 寫成檔案 commit（例如 `docs/<TRACK>_PLAN.md`）。Review 報告先以 `docs/<REVIEWER>_<DATE>_<SCOPE>.md` 落地，配套的 `_FIX_LOG.md` 隨修復 PR 一起 ship。
5. **Code-Review Handling** — 每條 finding 對著 code 驗證；依 severity triage；TDD 順序修；PR 一起帶 `_FIX_LOG.md`。
6. **Branch + PR Discipline** — Feature branch 從整合分支切出；經 PR 並用 `--no-ff` merge；部署鏈 `develop → main → production`；破壞性操作需要明確的人為簽核。
7. **First-Principles When Blocked** — 第一個冒出來的修法通常是 workaround；停下來重推。紅旗詞：「降低 threshold」「跳過檢查」「停用測試」「先 hardcode」。使用者反問「first principles?」→ 重推，不要辯護。
8. **When in Doubt** — 不確定就問，不要猜。可逆優先：先模擬再實單；先 staging 再 prod；先 dry-run 再 apply；先封存再刪除。
9. **Writing Style for Chat** — 自然語言、不在句中夾雜英文縮寫（當主要語言不是英文時）、不用比喻替代清晰描述、用具體數字 / 表格而非抽象論述。Repo 產物（程式碼、commit、PR description）保留英文。

**運作良好的訊號：** plan 檔案在 diff 之前先 land、review 都有對應的 fix-log、git history 看起來像 TDD 循環（`test:` → `feat:`）、釐清式的提問出現在錯誤之前而非之後。

### Codex CLI（OpenAI）

Codex 沒有 Claude Code 形式的 plugin marketplace。要把 Codex 視為獨立執行環境：相容的技能放在 `~/.codex/skills/<name>/SKILL.md`，全域行為規範放在 `~/.codex/AGENTS.md`。

```bash
mkdir -p ~/.codex
git clone https://github.com/solitude6060/Yao-skills ~/.codex/yao-skills

cat >> ~/.codex/AGENTS.md <<'EOF'

## Available skill references

When the user's request matches a skill below, read the corresponding SKILL.md and follow it:

- "triple review" / "PR review" → ~/.codex/yao-skills/skills/triple-review/SKILL.md
- "first principles" / "incident triage" → ~/.codex/yao-skills/skills/first-principles/SKILL.md
- "workflow routing" / "which workflow" → ~/.codex/yao-skills/skills/workflow-routing/SKILL.md
- "project status" / "health check" → ~/.codex/yao-skills/skills/project-status-review/SKILL.md
- "context hygiene" / "compact" / "clear" / "handover" → ~/.codex/yao-skills/skills/context-hygiene/SKILL.md
- "caveman-lite" / "lite mode" / "brief but accurate" / "less tokens" → ~/.codex/yao-skills/skills/distilled-caveman-lite-accuracy/SKILL.md
EOF
```

**注意事項：**

- 不要把整包 Claude Code plugin 直接覆蓋到 `~/.codex/skills`。部分技能假設 `/oh-my-claudecode`、Claude Code hooks 或 `.omc` 狀態，必須先改成 Codex 版。
- 如果本機已經有同名 Codex/OMX 技能，預設保留 Codex 版；只有明確移植完成時才用 Claude Code 版取代。
- 移除不相容技能時先移到 quarantine 目錄，不直接永久刪除；例如 `~/.codex/skills.quarantine.<date>/`，方便回復和比對。
- 重疊入口只保留一個主入口。例如新版 `first-principles` 已包含修復情境，可取代 `first-principles-fix`；單一 `ask` wrapper 可取代 `ask-claude` / `ask-gemini`。
- `triple-review` 依目前 orchestrator 選 reviewer。Codex orchestrating 時用 `claude` + `agy`/`gemini` + `claude-mm`；Claude Code orchestrating 時用 `codex`/`codex-family` + `agy`/`gemini` + `claude-mm`。除非使用者明確要求 self-review，否則不要把目前 orchestrator 放進 reviewer lanes。
- OMC 編排類 skills（`ralph`、`autopilot`、`ultrawork` 等）只有在執行階段依賴已移植到 OMX/Codex 時才值得放進 Codex。

### Gemini CLI（Google）

跟 Codex 同模式 — 從 `~/.gemini/GEMINI.md` 引用 skills。

```bash
mkdir -p ~/.gemini
git clone https://github.com/solitude6060/Yao-skills ~/.gemini/yao-skills

cat >> ~/.gemini/GEMINI.md <<'EOF'

## Skill references

If the user's request matches these keywords, read the SKILL.md before responding:

- "triple review" → ~/.gemini/yao-skills/skills/triple-review/SKILL.md
- "first principles" → ~/.gemini/yao-skills/skills/first-principles/SKILL.md
- "workflow routing" → ~/.gemini/yao-skills/skills/workflow-routing/SKILL.md
- "project status" → ~/.gemini/yao-skills/skills/project-status-review/SKILL.md
- "context hygiene" / "compact" / "handover" → ~/.gemini/yao-skills/skills/context-hygiene/SKILL.md
- "caveman-lite" / "lite mode" / "brief but accurate" → ~/.gemini/yao-skills/skills/distilled-caveman-lite-accuracy/SKILL.md
EOF
```

**注意事項：**

- `triple-review` 三個 reviewer 中其中一個就是 `gemini` CLI；在 Gemini CLI 內跑會 self-reference — 要嘛換掉那個 reviewer，要嘛在 Gemini 那邊跳過這個 skill。
- 沒有關鍵字 hook 自動觸發。

### opencode（sst/opencode）

opencode 會讀專案根目錄的 `AGENTS.md` 與 `~/.config/opencode/AGENTS.md` 兩處。

```bash
mkdir -p ~/.config/opencode
git clone https://github.com/solitude6060/Yao-skills ~/.config/opencode/yao-skills

cat >> ~/.config/opencode/AGENTS.md <<'EOF'

## Skill references

When the user's request matches a skill below, read the SKILL.md and follow it:

- "triple review" → ~/.config/opencode/yao-skills/skills/triple-review/SKILL.md
- "first principles" → ~/.config/opencode/yao-skills/skills/first-principles/SKILL.md
- "workflow routing" → ~/.config/opencode/yao-skills/skills/workflow-routing/SKILL.md
- "project status" → ~/.config/opencode/yao-skills/skills/project-status-review/SKILL.md
- "context hygiene" / "compact" / "handover" → ~/.config/opencode/yao-skills/skills/context-hygiene/SKILL.md
- "caveman-lite" / "lite mode" / "brief but accurate" → ~/.config/opencode/yao-skills/skills/distilled-caveman-lite-accuracy/SKILL.md
EOF
```

**注意事項：**

- opencode 支援多 provider；`triple-review` 的任一 reviewer 都可以換成指向其他 provider 的 opencode session，但 skill prompt 內提到的 provider 名稱要和實際指令一起改。
- opencode 自己的 command / agent 系統（`.opencode/command/*.md`）是更原生的 slash command 暴露方式；想要一級整合的話，參考 opencode 文件把 SKILL.md 的內容移植成 command 檔。

### Antigravity（Google IDE）

**不建議。** Antigravity 是 agent-first 的 IDE，採 workspace-scoped 的 YAML agent，沒有全域 plugin marketplace、沒有 CLI hook 層。

真的要用：

```bash
git clone https://github.com/solitude6060/Yao-skills /tmp/yao-skills
# 然後手動把相關 SKILL.md 的內容貼進 Antigravity 的 workspace prompt
# 或各 workspace 的 .agent.yaml
```

這套 skills 假設了 chat-driven 的 CLI agent + shell + git。Antigravity 的 IDE / browser-automation 模型大致正交 — 只有 `workflow-routing` 和 `project-status-review` 能完整轉譯，其餘多半失去價值。

## 更新（上游有新 commit 之後）

上游 repo 有新 commit 後，依各安裝路徑刷新：

| 安裝路徑 | 更新指令 |
|---|---|
| Claude Code（marketplace） | `/plugin marketplace update yao-skills` 然後 `/plugin update yao-skills@yao-skills` |
| Codex CLI | `git -C ~/.codex/yao-skills pull` |
| Gemini CLI | `git -C ~/.gemini/yao-skills pull` |
| opencode | `git -C ~/.config/opencode/yao-skills pull` |
| 單一 skill 複製（`~/.claude/skills/<name>`） | 重新 clone + `cp -r`，或當初是 git clone 過來就直接 `git -C` pull |
| 已部署的 CLAUDE.md 範本 | `cp templates/CLAUDE.md ~/.claude/CLAUDE.md`（會覆蓋；本地有改的話手動 merge） |

Claude Code 的 marketplace 更新完，重啟 CC session（或 `--resume`）讓新的 skill set 載入。`AGENTS.md` / `GEMINI.md` 的引用每個新 CLI session 都會重讀，不用額外動作。

## 對應你的環境

這套 skills 假設：

- 從 Claude Code 執行時：一個主要的 Claude Code（用 Anthropic OAuth）做編排
- 從 Codex 執行時：一個主要的 Codex CLI 做編排
- 一個次要的 Claude Code 端點（例如透過 `CLAUDE_CONFIG_DIR` 指向 MiniMax）提供 reviewer 多樣性
- 一個 `gemini` CLI 接 Google OAuth
- 一到兩個 `codex` CLI（不同帳號）做 reviewer 多樣性而不燒同一個額度

少其中任何一個的話，各個 skill 的 Troubleshooting 段落會說明降級版本（例如改成兩個 reviewer，並指出哪一類 bug 會因此看不到）。

## 授權

MIT（見 `LICENSE`）。第三方授權詳見 `NOTICE.md`。
