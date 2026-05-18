---
name: project-status-review
description: |
  Comprehensive project health check and status analysis. Use when user asks to "check project status",
  "review progress", "analyze development state", "assess project health", "review milestones",
  "check blockers", "what's the current state of", or any request about understanding where a project
  stands in its development lifecycle. Triggers especially when user mentions "進度" (progress),
  "狀態" (status), "開發" (development), or asks about "已完成" vs "待完成" items.
  This skill is NOT for implementation - it produces a comprehensive written status report with
  visual diagrams, tables, blockers, and prioritized next steps.
disable-model-invocation: true
allowed-tools: Bash(git log:*), Bash(git branch:*), Bash(git diff:*), Bash(find:*), Bash(wc:*), Bash(ls:*), Bash(npm test:*), Bash(npm run build:*), Bash(npm run smoke:*), Bash(npm audit:*), Read, Glob, Grep, LSP_diagnostics
argument-hint: "[project-path]"
---

# Project Status Review

Perform a comprehensive project health check. Generate a detailed status report with visual diagrams, statistics tables, blocker analysis, and prioritized action items.

## Workflow

### Step 1: Gather Basic Context

Run these commands in parallel to get a quick overview:

```bash
# 1. Recent commits (last 20)
git log --oneline -20

# 2. All branches
git branch -a

# 3. Commit difference between develop and main (or current branch vs main)
git log --oneline main..develop 2>/dev/null || echo "No main branch or same"
```

Read these files if they exist in the project:
- `README.md`
- `docs/STATUS_UPDATE.md`
- `docs/ROADMAP_zh.md` (or `ROADMAP.md`)
- `docs/DEPLOYMENT.md`
- `package.json` (or `app/package.json`)

### Step 2: Code Statistics

Collect quantitative data in parallel:

```bash
# Source file count (ts/tsx/js/jsx)
find . -type f \( -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.jsx" \) ! -path "./node_modules/*" ! -path "./.next/*" | wc -l

# Test files
find . -type f -name "*.test.ts" -o -name "*.test.tsx" ! -path "./node_modules/*" 2>/dev/null | wc -l

# Total lines of source code (excluding node_modules and generated)
find . -type f \( -name "*.ts" -o -name "*.tsx" \) ! -path "./node_modules/*" ! -path "./.next/*" -exec cat {} + 2>/dev/null | wc -l

# List documentation files
find . -name "*.md" -path "*/docs/*" -o -name "*.md" -maxdepth 2 2>/dev/null | head -20
```

### Step 3: Build and Test Verification

```bash
# Check if package.json has test/build/smoke scripts
# Run available verification commands if in appropriate directory
# (Skip if node_modules not installed - just note "need npm install first")
```

### Step 4: Dependency Audit

```bash
# Check for package-lock.json age and security issues
# Note if audit was run or if deps are stale
```

### Step 5: Synthesize into Report

Organize findings into the standard report format:

## Report Structure

```markdown
# [Project Name] 專案狀態全面檢視

**檢視日期**: [YYYY-MM-DD]
**專案描述**: [One-line description]
**目前分支**: `[branch]` (HEAD: `[commit]`)
**最後活動**: [YYYY-MM-DD]（距今約 **X 個月** / **X 週** / **X 天** 未有新 commit）

---

## 1) 整體開發進度

Use a markdown diagram or ASCII table showing completed milestones vs current blocker:

```
✅ M1 基礎平台 → ✅ M2 認證隔離 → ✅ M3 AI 核心 → ✅ M4 健身模組 → ✅ M5 進階功能 → ✅ M6 CI/CD+監控 → 🚧 Production Deploy
```

---

## 2) 程式碼統計

| 指標 | 數值 |
|------|------|
| 原始碼檔案數（`.ts` / `.tsx`） | X 個 |
| 原始碼總行數 | ~X 行 |
| 測試檔案 | X 個 |
| 測試案例結果 | **X passed** |
| CI/CD Workflows | X 個 |
| 文件 | X 份 |

---

## 3) 已完成功能清單

### 核心模組
- ✅ [feature 1]
- ✅ [feature 2]

### 進階功能
- ✅ [feature]
```

## Report Structure (continued)

```
---

## 4) Git 分支狀態

Use a table:

| 分支 | 最後活動 | 說明 |
|------|---------|------|
| `main` | YYYY-MM-DD | [description] |
| `develop` | YYYY-MM-DD | 領先 main **X 個 commit**，未合併 |
| `feature/*` | — | [status] |

> [!WARNING]
> If develop is significantly ahead of main (>20 commits) or very stale (>2 months):
> "⚠️ `develop` 累積了 X 個 commit（Y 檔變更、+Z/-W 行），長期未合併回 `main`。建議在部署前執行 merge。"

---

## 5) 技術堆疊

| 層級 | 技術 | 版本 |
|------|------|------|
| 前端 | Next.js / React / TypeScript | X.X.X |
| UI | TailwindCSS + Radix UI | v4 |
| 資料層 | Prisma ORM + PostgreSQL | vX.X.X |
| 認證 | NextAuth v5 | beta.X |
| AI | Google Gemini | @google/genai vX.X.X |
| 測試 | Vitest + Testing Library | vX.X.X |
| CI/CD | GitHub Actions | — |

---

## 6) 🚧 目前 Blockers — 上線前必須完成

### P0: Secrets & 環境變數

| Secret | 設定位置 | 狀態 |
|--------|---------|------|
| `VERCEL_TOKEN` | GitHub Secrets | ❌ / ✅ |
| `SENTRY_AUTH_TOKEN` | GitHub Secrets | ❌ / ✅ |

### P0: 部署決策（需你決定）

- [ ] **部署策略**：先將 `develop` merge 到 `main` 再部署？還是直接從 `develop` 部署？
- [ ] **網域策略**：先用 `*.vercel.app`？或一開始就綁自訂網域？
- [ ] **告警策略**：GitHub 通知就好？還是要接 Slack/Discord Webhook？

---

## 7) 後續版本規劃

| 版本 | 目標 | 主要項目 |
|------|------|----------|
| **v1.0.1** | 穩定上線與可觀測性 | [items] |
| **v1.1** | 帳號與安全 | [items] |
| **v2.0** | 平台化 | [items] |

---

## 8) 風險與建議

| 風險 | 等級 | 建議 |
|------|------|------|
| [risk] | 🟡 中 / 🟢 低 | [advice] |

---

## 9) 建議立即行動

1. **[Priority 1]**: [action] — [reason]
2. **[Priority 2]**: [action] — [reason]
3. **[Priority 3]**: [action] — [reason]

---

## 相關文件

- [STATUS_UPDATE.md](file://[path])
- [ROADMAP.md](file://[path])
- [DEPLOYMENT.md](file://[path])
```

## Key Analysis Points

### Staleness Check
- Calculate months/weeks since last commit
- Flag if >2 months without activity

### Commit Divergence
- Count commits between branches
- Note file change count and line diff (+/-)
- Flag if >20 commits divergence as risk

### Blocker Triage
- P0 = blocks production deployment
- P1 = should fix before v1.1
- P2 = nice to have for v1.2

### Technical Debt Flags
- Beta versions of major libraries
- Missing secrets for production
- Long-running unmerged branches
- Stale dependencies

### Risk Severity
- 🟡 中 = moderate risk, should address soon
- 🟢 低 = low risk, can defer

## Output Format

Always produce a comprehensive report in Traditional Chinese (or Simplified Chinese if that's the project language) with:
1. Visual progress diagram
2. Code statistics table
3. Completed features by category
4. Git branch analysis with divergence count
5. Technology stack table
6. Blocker list with P0 priorities
7. Future roadmap version table
8. Risk assessment with severity
9. Prioritized action items with clear reasoning

If project documentation exists, cross-reference it and note any discrepancies between docs and reality.

End with a question asking if the user wants to proceed with any of the recommended actions.