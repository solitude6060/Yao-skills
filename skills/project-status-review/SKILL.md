---
name: project-status-review
description: Use when the user asks where a project stands — "check project status", "review progress", "what's the current state", "check blockers", "進度", "狀態", or completed-versus-remaining items. Produces a written report, not implementation.
disable-model-invocation: true
allowed-tools: Bash(git log:*), Bash(git branch:*), Bash(git diff:*), Bash(find:*), Bash(wc:*), Bash(ls:*), Bash(npm test:*), Bash(npm run build:*), Bash(npm run smoke:*), Bash(npm audit:*), Read, Glob, Grep, LSP_diagnostics
argument-hint: "[project-path]"
---

# Project Status Review

Read-only health check. Output is a report in the project's document language
(Traditional Chinese by default), cross-checked against the project's own
status files.

## Gather (run in parallel)

1. `git log --oneline -20`, `git branch -a`, `git log --oneline main..develop`
   (or the integration branch the project uses).
2. Read `status.md`, `tracker.md`, `handover.md` (project memory) and `README.md`;
   fall back to `docs/STATUS*`, `docs/ROADMAP*`, `docs/DEPLOYMENT*`.
3. Counts: source files, test files, source lines, docs. Exclude
   `node_modules`, build output and virtual environments.
4. If a test / build / smoke script exists and dependencies are installed, run
   it once; otherwise record "not run" with the reason.
5. Lock-file age and audit status.

## Report template

Fill every section; replace the example rows with the project's own stack and
secret names/status only. Never print secret values. Flag last activity > 60
days, integration branch > 20 commits ahead
of `main` or > 2 months unmerged, and pre-release majors.

````markdown
# [Project] 專案狀態全面檢視

**檢視日期**: YYYY-MM-DD ・ **專案描述**: <one line>
**目前分支**: `<branch>` (HEAD `<sha>`) ・ **最後活動**: YYYY-MM-DD（距今 X 天）

## 1) 整體開發進度
✅ M1 <name> → ✅ M2 <name> → 🚧 <current blocker>

## 2) 程式碼統計
| 指標 | 數值 |
|---|---|
| 原始碼檔案數 | X |
| 原始碼總行數 | ~X |
| 測試檔案 / 測試結果 | X / **X passed** |
| CI/CD workflows / 文件 | X / X |

## 3) 已完成功能清單
### 核心模組
- ✅ <feature>

## 4) Git 分支狀態
| 分支 | 最後活動 | 說明 |
|---|---|---|
| `main` | YYYY-MM-DD | <desc> |
| `develop` | YYYY-MM-DD | 領先 main **X commits**，未合併 |

> [!WARNING] develop 累積 X commits（Y 檔、+Z/−W 行）未合併回 main，部署前先 merge。

## 5) 技術堆疊
| 層級 | 技術 | 版本 |
|---|---|---|
| 前端 | Next.js / React / TypeScript | X.X |
| 資料層 | Prisma + PostgreSQL | X.X |
| 認證 | NextAuth | beta.X |
| AI | Google Gemini `@google/genai` | X.X |
| 測試 / CI | Vitest / GitHub Actions | X.X |

## 6) 🚧 Blockers — 上線前必須完成
### P0: Secrets & 環境變數
| Secret | 設定位置 | 狀態 |
|---|---|---|
| `VERCEL_TOKEN` | GitHub Secrets | ❌ / ✅ |
| `SENTRY_AUTH_TOKEN` | GitHub Secrets | ❌ / ✅ |
### P0: 部署決策（需你決定）
- [ ] 部署策略：develop → main 再部署，或直接從 develop 部署
- [ ] 網域策略：`*.vercel.app` 先上，或一開始綁自訂網域
- [ ] 告警策略：GitHub 通知，或接 Slack / Discord webhook

## 7) 後續版本規劃
| 版本 | 目標 | 主要項目 |
|---|---|---|
| v1.0.1 | 穩定上線與可觀測性 | … |
| v1.1 | 帳號與安全 | … |

## 8) 風險與建議
| 風險 | 等級 | 建議 |
|---|---|---|
| <risk> | 🟡 中 / 🟢 低 | <advice> |

## 9) 建議立即行動
1. **P1**: <action> — <reason>
2. **P2**: <action> — <reason>
3. **P3**: <action> — <reason>

## 10) 文件與實況落差
- <status doc says X; observed Y>

## 相關文件
- Related documents: `status.md` ・ `ROADMAP` ・ `DEPLOYMENT`
````

Blocker priority: P0 blocks deployment, P1 before next minor, P2 later.
Every number names the command or file it came from; do not carry a figure
forward from an older status file without re-measuring.

End with one question: which recommended action, if any, to start.
