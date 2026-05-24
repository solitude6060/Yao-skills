---
name: triple-review
description: Run an orchestrator-aware triple-reviewer code review. Claude Code orchestration uses codex/codex-family + agy/gemini + secondary endpoint; Codex orchestration uses claude + agy/gemini + secondary endpoint. Triage findings with severity calibration, apply TDD fixes, archive review artifacts, and auto-merge only if green.
argument-hint: "<PR# | branch name | (empty for current branch)>"
---

# /triple-review — three-reviewer PR review with TDD fix loop

Three independent reviewers beat two. Each model class catches a different bug class — a single missing reviewer means a whole bug class is invisible. This skill first identifies the current orchestrator, then selects three external reviewers so the orchestrator does not review its own work.

## When to use

- A code PR has been pushed and is ready for review
- Caller runs `/triple-review <PR#>` or just `/triple-review` (current branch)
- **Not for**: docs-only PRs, WIP / draft PRs, unpushed branches, config/lock-file-only diffs

## Reviewer selection

Pick reviewers from the current orchestrator:

| Orchestrator | Reviewer lanes |
|---|---|
| Claude Code | `codex` / `codex-family` + `agy` / `gemini` + secondary endpoint |
| Codex | `claude` + `agy` / `gemini` + secondary endpoint |

In both modes, `agy` is the preferred Gemini-class lane; `gemini` is the fallback. Do not include the current orchestrator as a reviewer unless the user explicitly asks for self-review.

## Prerequisites

- **Reviewer 1 (Gemini-class) — pick one of these two CLIs**:
  - **Primary (2026-05+): `agy` (antigravity-cli)** — install + Google OAuth. Model is fixed at the Gemini 3.x Pro class internally; no `-m` flag.
  - **Legacy: `gemini` CLI** — still works until Google retires it. `npm install -g @google/gemini-cli`. Keeps the explicit `-m <model>` flag (e.g. `-m gemini-3.1-pro-preview`) if you need to pin a specific Pro snapshot.
  - Only one is required. Both produce a Gemini-class review.
- A second Claude Code CLI on a different endpoint (e.g. a secondary provider configured via `CLAUDE_CONFIG_DIR`) — must run with `Read / Grep / Glob / Bash` available so it can verify findings against actual file contents
- If Claude Code is orchestrating: `codex` / `codex-family` CLI (ideally from a separate account to avoid burning the primary Codex quota)
- If Codex is orchestrating: `claude` CLI through the user's normal Claude Code account
- `gh` CLI authenticated
- The project has a `CLAUDE.md` / SPEC file that names invariants (without it the reviewers have no anchor and report quality collapses)
- PR base branch is typically `develop` or `main`

## Workflow

### Step 1 — Resolve the PR from `$ARGUMENTS`

- If numeric → PR number
- If branch name → `gh pr view --json number,headRefName,baseRefName --branch <name>`
- If empty → `gh pr view --json ...` for the current branch

Extract: `pr_number`, `head_branch`, `base_branch`, `head_sha`.

### Step 2 — Build the review prompt

Write to `/tmp/pr<n>_review_prompt.txt` with **four sections**:

**(0) Preamble — reviewer constraints (always include)**:

```
You are a code reviewer. Your only output is a markdown review of the PR diff below.

Do NOT spawn other reviewers (no nested agy / gemini / claude / codex calls).
Do NOT call gh CLI or run scripts.
Do NOT delegate to other skills or agents.
You MAY use Read / Grep / Glob to verify findings against actual file contents
(verify before flagging).

Format the review as:
1. Verdict: APPROVE / REQUEST CHANGES / BLOCK
2. Findings grouped by severity (CRITICAL / HIGH / MEDIUM / LOW), each with file:line + recommended fix
3. Specific risk callouts for the focus points listed below
```

Avoid trigger phrases that re-invoke the same skill: do not title the prompt "Triple PR Review"; use `## Context / ## Invariants / ## Focus / ## Diff` (not `(a)(b)(c)`).

**(a) Context**: what this PR does, what it builds on, which track / phase it belongs to.

**(b) Project invariants**: pull relevant rules from `CLAUDE.md` / SPEC — e.g. numeric precision discipline (Decimal vs float), type-check strictness, layer dependency rules, phase gates, anything project memory says is load-bearing.

**(c) Focus**: PR-specific concerns — algorithm correctness, edge cases at thresholds (`==` / `>` / `>=`), forward-compat with the next PR in series, coverage gaps, SPEC alignment on concrete values.

Append the diff:

```bash
git diff origin/<base_branch>...HEAD >> /tmp/pr<n>_review_prompt.txt
```

### Step 3 — Run three reviewers in parallel (single message, three tool calls)

All three use `run_in_background: true` so the assistant is not blocked.

**Reviewer 1 — Gemini-class** (pick one):

```bash
# Primary — agy (antigravity-cli)
agy --print-timeout 15m --dangerously-skip-permissions \
  -p "$(cat /tmp/pr<n>_review_prompt.txt)" \
  > /tmp/pr<n>_review_gemini.out 2>&1
```

⚠ **agy flag-order is load-bearing**: every flag (`--print-timeout`, `--dangerously-skip-permissions`, `--sandbox`, …) must come **before** `-p`. A flag placed after the prompt is absorbed into the prompt and the call hangs silently (observed: `agy -p "<prompt>" --print-timeout 10m` hung >14 min with no output). The default `--print-timeout` is 5 m; raise it for full-PR review prompts.

```bash
# Legacy — gemini-cli (still works until Google retires it)
gemini --skip-trust -p "$(cat /tmp/pr<n>_review_prompt.txt)" -m gemini-3.1-pro-preview \
  > /tmp/pr<n>_review_gemini.out 2>&1
```

Both CLIs share the output filename `_gemini.out` because Reviewer 1's **identity is the model class, not the CLI**. Record the actual CLI + version inside the archived review file body.

**Reviewer 2 — Claude Code via secondary endpoint**:
```bash
cd <repo-or-worktree-path>
# Point CLAUDE_CONFIG_DIR to a secondary config directory with different provider credentials.
# Unset any ANTHROPIC_* env vars that might override the secondary config.
cat /tmp/pr<n>_review_prompt.txt | env -u ANTHROPIC_BASE_URL -u ANTHROPIC_AUTH_TOKEN \
  -u ANTHROPIC_MODEL -u ANTHROPIC_DEFAULT_SONNET_MODEL \
  -u ANTHROPIC_DEFAULT_OPUS_MODEL -u ANTHROPIC_DEFAULT_HAIKU_MODEL \
  CLAUDE_CONFIG_DIR=$HOME/.claude-<your-secondary-endpoint> claude -p \
  > /tmp/pr<n>_review_secondary.out 2>&1
```

This reviewer runs full Claude Code tooling (Read / Grep / Glob / Bash) on the actual files, so it tends to catch the bugs that need file-context verification (collaborator function signatures, cross-file invariants).

**Reviewer 3 when Claude Code is orchestrating — Codex CLI from a secondary account**:
```bash
cd <repo-or-worktree-path>
# Use CODEX_HOME to point to a secondary Codex config if available.
# Adjust the codex path to match your installation (e.g. via nvm, npx, or global install).
cat /tmp/pr<n>_review_prompt.txt | CODEX_HOME=$HOME/.codex-secondary \
  codex exec \
  --sandbox read-only \
  --skip-git-repo-check \
  - > /tmp/pr<n>_review_codex.out 2>&1
```

The `read-only` sandbox lets Codex use `Read / Grep / Glob` to verify findings but blocks writes. `--skip-git-repo-check` lets it run inside worktrees.

**Reviewer 3 when Codex is orchestrating — Claude Code CLI**:
```bash
cd <repo-or-worktree-path>
cat /tmp/pr<n>_review_prompt.txt | claude -p \
  > /tmp/pr<n>_review_claude.out 2>&1
```

This lane is only for Codex-orchestrated runs. Do not add it to Claude Code-orchestrated runs unless the user explicitly asks for self-review.

All three run in background. Do not poll — wait for completion notifications.

### Step 4 — Triage (start only when all three reports are in)

For every finding, fill this table:

| Finding | Source | Severity | Action |
|---|---|---|---|
| ... | Gemini / Secondary / Claude-or-Codex / multi | CRITICAL/HIGH/MEDIUM/LOW | Fix / Fold / Skip + reason |

**Severity-calibration heuristics** when the three reviewers disagree on the same finding:

- **Gemini** tends toward **invariant-first** (cites project rules)
- **Secondary Claude Code** tends toward **operational-first** (does this work at realistic scale)
- **Claude-or-Codex lane** tends toward **diff-correctness + cross-reference** (ADR vs implementation, untested call sites)
- **Three agree** → use the consensus
- **Two vs one** → majority wins; **but if the dissenter is Gemini citing a specific invariant, invariant-first wins**
- **Three-way split** → invariant-first wins; document in the fix-log: "Secondary LOW + Codex MEDIUM reclassified HIGH per Gemini — violates invariant X"

Common patterns observed across many reviews:

- Secondary Claude Code (or any operational-first reviewer) labels real bugs as LOW because they "work at realistic scale"
- Gemini reclassifies the same finding HIGH/CRITICAL because it violates `CLAUDE.md` / SPEC
- The third lane adds a layer the other two miss — coverage gaps, ADR-vs-impl drift, untested call sites

**⚠ Reviewer hallucination — verify factual claims**:

"Invariant-first wins" does **not** mean "reviewer-always-right". Any reviewer can hallucinate facts about external APIs, stdlib behavior, or what the SPEC actually says. Before accepting a finding whose premise is a factual claim:

1. Grep / Read the cited file:line yourself
2. Confirm collaborator function signatures with `grep -n`
3. Read stdlib docs for the exact return type / behavior
4. Find the SPEC value, do not accept the reviewer's quote of it

If the reviewer's premise was wrong but the fix direction is still correct, take the fix and note in the fix-log: "reviewer's premise was wrong; fix direction still correct".

**Severity patterns worth knowing**:

- **Hardcoded literal in production code** → usually calibrates to CRITICAL (most projects' CLAUDE.md says "no hardcoded thresholds")
- **Wiring gap** (component A and B each unit-tested, but the hand-off untested) → unit tests green + dual review green but prod behavior broken; **the most dangerous class**, only e2e / integration coverage catches it
- **Soft-degrade on missing config that gates a downstream invariant** → use `log.error` + invariant-blocking message (not `raise`, so other ticks of the same daemon survive)
- **List operations on prod data without LIMIT / ORDER BY** → always HIGH (scaling cliff is certain)
- **Tier mapping / config dict without test for every member** → Codex usually catches; MEDIUM but cheap to test

**Skip judgment**:

- Pure cosmetic / style choices that match the codebase pattern
- Defensive coding for impossible scenarios (CLAUDE.md "trust internal guarantees")
- Forward-compat speculation with no concrete consumer
- `is` vs `==` and similar pattern-conformance choices the codebase already made
- Findings whose factual premise turned out to be wrong (after verification)

### Step 5 — TDD fix cycle (per `Fix` row)

**Test commit**:
- Write the failing test pinning the contract
- Run the single file: red for the **right reason** (assertion failure, not import error)
- Commit: `test: failing tests for PR #<n> triple review fixes` — include the triage table in the body

**Fix commit**:
- Smallest change that turns the test green
- Run the project's full check suite — tests, type-checker, lints, formatters
- Commit: `fix: address PR #<n> triple review (...)` — body references the three review artefacts by filename

### Step 6 — Archive the reviews

Write all three to `docs/PR_REVIEW_<YYYY-MM-DD>_PR<n>_{GEMINI,SECONDARY,CODEX}.md`, each with:

- Title, PR URL, base/head, head SHA, review date, reviewer identifier (model + invocation command)
- Findings grouped by severity
- Each finding: `file:line`, description, recommended fix, actual disposition (Fixed / Skipped + reason)
- Verdict (APPROVE / REQUEST CHANGES / BLOCK) and whether resolved this round

Optionally collapse into one file with three sections.

### Step 7 — PR comment

```bash
gh pr comment <n> --body "$(cat <<'EOF'
## Triple code review — fix round

Three reviews ran; artefacts archived in this branch:
- docs/PR_REVIEW_<date>_PR<n>_GEMINI.md — <verdict + counts>
- docs/PR_REVIEW_<date>_PR<n>_SECONDARY.md — <verdict + counts>
- docs/PR_REVIEW_<date>_PR<n>_CODEX.md — <verdict + counts>

### Triage
<table>

### Notable
<severity disagreements, complementary catches, three-way ship-blockers>

### Commits
- <test commit SHA>
- <fix commit SHA>

### Verification
- tests → N passed
- type-check → clean
- lints + formatters clean
EOF
)"
```

### Step 8 — Auto-merge if green

Five-item gate:

1. All three reviews archived
2. Triage table posted to PR comment
3. Every HIGH and MEDIUM is either fixed or explicitly skipped with reason
4. Full check suite green (tests, type-check, lints, formatters)
5. `gh pr view <n> --json mergeable -q '.mergeable'` → `MERGEABLE`

All green → merge:

```bash
gh pr merge <n> --merge --delete-branch
git checkout <base_branch>
git pull --ff-only
```

If the project has a "human merges only" rule (e.g. for production-branch promotion), stop at step 7 and let the user decide.

## End-of-cycle summary

Five-to-ten lines back to the user:

- PR # merged (commit SHA)
- Real bugs caught — especially the ones a single or dual reviewer would have missed
- Net diff: lines / tests added
- What's next

## Troubleshooting

- **Reviewer 1 (Gemini-class) 429 / quota / model unavailable**:
  - **agy path**: retry once with ≥30 s gap; agy has no `-m` flag to swap models, so if the quota is gone, fall back to `gemini` CLI (if installed) or drop the Reviewer 1 slice.
  - **gemini-cli path**: retry once; fall back to `agy` (if installed) or drop the slice. If both fail, run Reviewer 2 (secondary Claude Code) + Codex only and tell the user that the invariant-first calibration heuristic does not fully apply this round.
- **`agy` hangs with no output for >10 min**: 99% likely the flag-order rule was broken. Inspect the running command — every CLI flag must come before `-p`. `agy -p "<prompt>" --print-timeout 10m` parses `--print-timeout 10m` as prompt content and waits forever for the continuation. Fix: re-order to `agy --print-timeout 10m -p "<prompt>"`.
- **Secondary Claude Code hangs**: full-tool runs of 10+ min are normal for complex reviews. Check `ps aux | grep CLAUDE_CONFIG_DIR=<endpoint-dir>` for an active process and watch output file size for growth. Only kill after 15 min of no output.
- **Recursion (reviewer output starts with the secondary's identity banner + "Skill ...")**: the prompt is missing the Step 2 §0 preamble, or the title is too close to "Triple PR Review". Rebuild the prompt with the literal preamble.
- **Codex auth missing in Claude Code orchestration**: verify `CODEX_HOME=<secondary> codex login status` shows logged-in; if not, the user must run the login interactively. If the secondary Codex is unavailable, fall back to the primary Codex (note the cost), and only as a last resort run with two reviewers and tell the user a whole reviewer slice is missing.
- **Claude auth missing in Codex orchestration**: verify `claude -p "ping"` or the local equivalent works. If not, do not substitute Codex for itself; run two reviewers and tell the user the Claude slice is missing.
- **Reviewer hallucinates a factual claim** (collaborator API, stdlib return type, SPEC value): always verify with `grep` / `Read` / official docs before accepting. Take fixes whose direction is right even if the premise was wrong; note both in the fix-log.
- **Reviewers strongly disagree**: invariant-first wins, **but verify the invariant is real** — reviewers sometimes invent invariants.
- **Diff > ~1000 lines**: split the prompt into focused slices, or ask the user to split the PR.
- **All three approve but a real wiring-gap bug ships**: add a focus item to future prompts: "verify there is a test that calls A then asserts on what B returns".

## What NOT to use this for

- Docs-only PRs (plan files, runbooks, ADRs) — these are taste calls; show them to the user
- Risky operations (force-push, prod-chain promotion, prod schema migrations) — should not bypass a human gate
- Config-only / lock-file PRs — no review surface to speak of

$ARGUMENTS
