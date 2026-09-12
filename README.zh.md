# yao-skills

[English](README.md) | 繁體中文

供開發、獨立審查、專案記憶及技術說明使用的可重用技能。**0.8.0** 分享目前
Yao-Garyu research-toolkit 的方法，包含台灣版 `wait-what`。

## 這個 repository 的存在意義

Yao-Garyu 維護我的個人工作流程。Yao-skills 是社群分享版，讓其他人使用自己的
專案、模型及工具，採用相同的決策方法：定義工作、驗證假設、測試修改、處理
審查意見，並保存足以接續工作的背景。

本 repository 提供技能指引、參考資料、行為範本及選用的 Claude Code hook
（工具呼叫前後執行的檢查）。執行工具、模型帳號與調度服務由採用者自行設定，
各專案的規格仍是工作依據。歡迎分支修改，並根據實際使用經驗提出改善。

[0.8.0 同步紀錄](docs/2026-09-13-community-sync.zh.md) 記錄來源版本及社群版調整。
英文檔案是技能的正典指引；繁體中文對照檔供閱讀與維護使用。

## 我的開發流程

以下整理我在軟體與研究專案使用的流程。範例來自已讀取的專案紀錄，經過匿名化，
不包含私人結果或帳號設定。依修改需要採用步驟；範圍小、規格明確的修改可以
直接完成並驗證。

```mermaid
flowchart LR
    A[讀規格與專案紀錄] --> B[記錄範圍與驗收方式]
    B --> C[失敗檢查與最小實作]
    C --> D[驗證結果與獨立審查]
    D --> E[授權範圍內建立與合併請求]
    E --> F[更新狀態、任務與交接]
```

1. **提方案前先讀。** 從規格或 README 開始，再讀 `status.md`、`tracker.md`、
   `handover.md`，核對真實輸入與現有實作。下一步依賴尚未確認的假設時，使用
   `first-principles`。只有紀錄無法解決的重要資訊才需要向使用者確認。
2. **先讓工作可以被檢查。** 非瑣碎工作從整合分支建立功能分支，先提交短計畫，
   寫明目標、範圍、檢查及停止條件。架構或契約變更先留下決策紀錄。
   規劃、實作或委派責任需要判斷時使用 `workflow-routing`；檔案多不直接代表需要團隊。
3. **做最小且可驗證的修改。** Bug 先用 regression test（回歸測試：重現問題，
   確認修正後不再發生）取得預期的失敗，再做最小修正、執行受影響的檢查。
   保留失敗與通過的提交歷史；純文件修改使用適合的驗證工具。
4. **委派有界線、可獨立完成的工作。** 由一個主代理負責整合。每個子代理都有
   輸入、可修改路徑、驗收方式與回報條件。執行環境支援時使用合適的原生子代理；
   外部工具保留自己的權限與帳號限制。模型、推理強度及備援集中在一份本機路由
   政策中，不能因可用額度而降低驗證標準。
5. **審查確切的修改版本。** 專案要求三個獨立審查時使用 `triple-review`。
   每個問題都對照來源與檢查結果，記錄有效問題及誤報，修正後重新審查受影響的
   差異。審查失敗或空白回覆不能算通過。一般文件採驗證工具；影響研究有效性的
   文件依專案審查要求。合併與部署遵守已取得的授權。
6. **留下能接續的紀錄。** 重要里程碑更新三個管理檔；操作方式變更則更新 runbook
   （操作手冊）。長對話交接前使用 `context-hygiene`，先保存下一個指令與尚未解除
   的條件，再清理對話背景。

| 專案檔案 | 我保留的內容 |
|---|---|
| `status.md` | 目前狀態、證據、決策與風險 |
| `tracker.md` | 進行中任務、相依關係、完成與停止條件 |
| `handover.md` | 本次修改、接續位置、指令及尚待回答的問題 |

### 實際工作中的使用方式

| 情況 | 已讀取紀錄呈現的做法 | 對應技能 |
|---|---|---|
| 測試依賴開發者家目錄的設定 | 記錄隔離計畫、重現外部設定造成的失敗、補回歸測試並驗證修正 | `first-principles`、`workflow-routing` |
| Reviewer（審查者）認為匯入問題阻擋交付 | 核對實際使用位置與編譯結果，記錄拒絕誤報的依據 | `triple-review` |
| 功能實作完成，驗收仍需操作者決定 | 在三個管理檔分別記錄實作狀態及未完成的驗收條件 | `project-status-review` |
| 研究專案可能擴大成完整實驗平台 | 先執行能決定繼續、調整或停止的最小有效真實資料實驗，讀完結果再擴大 | `first-principles`、`workflow-routing` |
| 研究或工程說明缺少決策前提 | 明確呼叫 `wait-what`，補回背景、機制、證據及實際影響 | `wait-what` |

前三列整理已記錄的開發案例。研究列也反映目前「先取得證據」的政策；實際能執行
哪些工作，仍由各專案的資料、指標及授權規定決定。說明列呈現新技能的預期用途，
尚未量測理解成效是否改善。

研究工作的第一個里程碑，是取得能改變下一步決策的最早可信證據。保留專案要求
的來源、資料識別、防止資料洩漏的邊界、指標定義與持久產物，無效或結論待定的
執行也要保留。合成資料測試通過，尚不足以建立真實資料上的結果。

Worktree（同一 repository 的獨立工作目錄）及完整複本放在持久的同層目錄，
例如 `../project-wt-fix`。本套件的 `worktree-hygiene` 將實驗產物放在另一個持久
同層目錄，例如 `../project-runs`，並要求移除工作目錄前先盤點。工作及證據的
唯一副本不得放在暫存空間。

## 我在什麼情況使用哪個 skill

| 技能 | 使用時機 | 預期產物 |
|---|---|---|
| [first-principles](skills/first-principles/SKILL.zh.md) | 提議修正、既有慣例或異常結果需要確認 | 對照可觀察證據的假設檢查 |
| [workflow-routing](skills/workflow-routing/SKILL.zh.md) | 規劃、實作或審查責任不明 | 依本機路由政策選出的工作方式 |
| [triple-review](skills/triple-review/SKILL.zh.md) | 合併前需要多模型獨立審查 | 綁定版本的審查、核實後的分類與修正紀錄 |
| [worktree-hygiene](skills/worktree-hygiene/SKILL.zh.md) | 建立、盤點或移除工作目錄 | 移除前的責任歸屬與產物檢查 |
| [project-status-review](skills/project-status-review/SKILL.zh.md) | 需要核對完成項目、阻塞及下一個決策 | 依 repository 證據整理的狀態報告 |
| [context-hygiene](skills/context-hygiene/SKILL.zh.md) | 對話背景過長，或要換 session（工作階段） | 聚焦的壓縮內容或持久交接檔 |
| [wait-what](skills/wait-what/SKILL.zh.md) | 明確要求重新講清楚 | 補背景、精確術語的台灣繁體中文說明 |
| [distilled-caveman-lite-accuracy](skills/distilled-caveman-lite-accuracy/SKILL.zh.md) | 希望回答短一點 | 保留條件、識別碼與不確定性，刪除贅語 |
| [tc-review](skills/tc-review/SKILL.zh.md) | 準備繁體中文內容 | 依上下文檢查台灣用語及術語 |
| [karpathy-guidelines](skills/karpathy-guidelines/SKILL.zh.md) | 寫程式時需要提醒假設與範圍 | 簡單、精準且有明確完成條件的修改 |

安裝對應技能後，可以這樣提出要求：

```text
使用 workflow-routing，決定如何實作這份已接受的計畫。
使用 first-principles，驗證這個修正方案依賴的假設。
使用 triple-review，以專案設定的審查者檢查這個合併請求。
使用 project-status-review，核對現況與未完成的工作。
使用 wait-what，從問題、缺少的前提、機制與證據重新說明。
使用 distilled-caveman-lite-accuracy，縮短回答但保留成立條件。
```

`wait-what` 只在明確呼叫時啟用，提到、安裝或討論名稱都不會自動啟動。
Codex 使用 `$wait-what`；Claude Code 套件安裝後使用 `/yao-skills:wait-what`。
它調整目前的說明，保留進行中的任務；不授權修改檔案或啟動實驗。

來源在 0.7.0 移除了 OMC 調度技能，本社群版在 0.8.0 跟進。`plan`、`team`、
`ralph`、`autopilot`、`ultrawork` 等工作流程請從
[oh-my-claudecode](https://github.com/Yeachan-Heo/oh-my-claudecode)
或對應執行環境的套件取得。持續執行的流程需要操作者明確提出範圍與停止條件；
讀到文件裡的流程名稱不會啟動它。

## 安裝

### Claude Code

```text
/plugin marketplace add solitude6060/Yao-skills
/plugin install yao-skills@yao-skills
```

套件提供十個技能，呼叫格式為 `/yao-skills:<skill-name>`。安裝後重新載入套件
或開啟新對話。參考官方[套件安裝說明](https://code.claude.com/docs/en/discover-plugins)。

### Codex 與個別技能安裝

將 repository 放在持久位置。下列範例只為 Codex 安裝 `wait-what`，不取代
既有的同名目錄：

```bash
mkdir -p "$HOME/Research" "$HOME/.agents/skills"
git clone https://github.com/solitude6060/Yao-skills.git "$HOME/Research/Yao-skills"
ln -s "$HOME/Research/Yao-skills/skills/wait-what" "$HOME/.agents/skills/wait-what"
```

若來源或目標已存在，先確認其內容，再更新既有安裝。Codex 從 `~/.agents/skills`
尋找使用者技能，支援符號連結；若尚未出現，重新啟動。`agents/openai.yaml`
保留 `wait-what` 的明確呼叫設定。也可以請內建 `$skill-installer` 從本 repository
安裝指定資料夾。參考 [OpenAI 官方技能文件](https://learn.chatgpt.com/docs/build-skills)。

其他代理請使用官方說明的技能目錄，或在指引檔明確列出要讀取的 `SKILL.md`。
確認該執行環境實際提供的工具及呼叫方式。Claude marketplace 設定與選用的 hook
適用於 Claude Code。

### 本機政策與行為範本

將 [templates/CLAUDE.md](templates/CLAUDE.zh.md) 的適用部分合併至既有的
`CLAUDE.md` 或 `AGENTS.md`。範本供採用者編輯，沒有安裝或覆寫功能；需設定
專案規格、整合分支、驗證命令與部署界線。

需要委派或獨立審查時，在指引檔指定路由政策位置，例如 `docs/MODEL_ROUTING.md`。
集中記錄允許的工具、實際模型名稱、支援的推理強度、任務資格、審查者、帳號與
資料界線及可使用的備援；若有任務說明規範，也一併連結。這些是各專案設定，
套件不內附固定模型表。沒有路由表時仍可直接完成授權範圍內的工作；需要但尚未
設定的審查者，只阻擋該項審查。

### 選用 hook

[tc-quality-hook](hooks/tc-quality-hook/README.zh.md) 是需另外設定的 Claude Code
`PreToolUse` 檢查，對象為 `AskUserQuestion`。依該目錄說明安裝；安裝技能本身
不會啟用 hook。提示模型自我檢查的機制，尚不足以證明文字品質。

## 更新與驗證

Claude marketplace 安裝者先更新 marketplace，再使用套件管理介面的更新動作。
本機複本可執行：

```bash
git -C "$HOME/Research/Yao-skills" pull --ff-only
```

符號連結會使用更新後的來源。複製安裝則需要另行同步，先保留本機修改並檢查
0.8.0 的移除清單；OMC 上游安裝保持獨立。

維護者可在 repository 根目錄檢查套件：

```bash
claude plugin validate .
git diff --check
```

[同步紀錄](docs/2026-09-13-community-sync.zh.md) 列出本次使用的清單、可移植性
與雙語檢查。它們驗證套件一致性，尚未量測技能成效或驗證每個執行環境。

## 授權

MIT。原創技能、karpathy-guidelines、wait-what 改寫及歷史 OMC 授權見
[LICENSE](LICENSE) 與 [NOTICE.md](NOTICE.md)。
