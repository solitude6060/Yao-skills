---
name: workflow-routing
description: Pick the right plan / implement / review workflow (A / B / mini) for a coding task based on task type, difficulty, and risk level. Backed by ongoing narrative-trader A/B trials. Use BEFORE non-trivial PR work, when deciding "which model plans and which implements".
---

# /workflow-routing — pick the plan / impl / review workflow

Before non-trivial implementation work, route the task through this matrix. The
matrix is calibrated against narrative-trader A/B trial data (PR-B-6.5 in
Workflow A, ADR-022 A3 in Workflow B; updates land in `docs/MONEY_PATH_PLAN.md`
§10 as trials complete).

## When to use

- Before non-trivial impl work, run through this skill to pick A / B / mini
- When user asks "which workflow", "how do we tackle this", "plan/implement split"
- When opening a new feature/track plan-file (per CLAUDE.md §4)
- **Not for**: typo fixes, single-line config tweaks, doc-only edits — skip routing, just do it

## The 3 workflow variants

### Workflow A — Opus plans / codex implements / Opus verifies / triple-review
Best for: **SPEC / ADR-level decisions, algorithmic correctness, multi-file
architectural changes, anything where planning precision > implementation speed**.

```
Opus → plan-file in repo (docs/<TRACK>_PLAN.md)
  ↓
codex:codex-rescue (Agent tool, isolation:worktree) → implement
  ↓
Opus → verify (pytest + mypy + ruff + black + diff review)
  ↓
triple-review (gemini-cli + claude-mm/MiniMax + codex via codex-rescue)
  ↓
fix round if findings, then auto-merge per feedback_autonomous_merge.md
```

**Cost**: ~$1-2 / PR (Opus is the expensive layer)
**Wall time**: 30-60 min / PR (measured on PR #187/#188/#189 in narrative-trader 2026-05-12)

### Workflow B — codex plans / Sonnet implements / codex+Opus review
Best for: **mechanical / pattern-mirror implementations, well-spec'd small-to-medium
features, anything where the plan is mostly transcription from existing patterns**.

```
codex exec --model gpt-5.5 (effort: high) → plan-file in repo
  ↓
Claude Sonnet (Agent tool with model:"sonnet") → implement
  ↓
codex review + Opus review (dual, parallel)
  ↓
fix round if findings
```

**Cost**: ~$0.3-0.8 / PR (Sonnet ~5x cheaper than Opus; codex via OAuth = $0)
**Wall time**: ~25-50 min / PR (pending trial validation)

### Workflow C — codex plans / Opus implements / triple-review / Opus final confirm
Best for: **highest-stakes work — risk validator / hard-limit / live-flag /
phase transition / new SPEC invariant / algorithmic core (e.g., EMA math,
Decimal precision, walk-forward correctness)**.

The maxim of this workflow: **no single model owns the whole pipeline**.
Codex plans (different brain than implementer), Opus implements (heavy
reasoning + deeper context), three independent reviewers, then Opus
re-confirms by reviewing the reviewers' verdicts — final decision authority
separated from implementation authority.

```
codex exec --model gpt-5.5 (effort: high) → plan-file in repo
  ↓
Claude Opus (Agent tool with model:"opus") → implement
  ↓
triple-review (gemini-cli + claude-mm/MiniMax + codex via codex-rescue) — no Opus in review pool
  ↓
Claude Opus → final confirm: read all 3 reviews, triage, decide merge / revise / block
  ↓
If revise → fix round (back to Opus implement); else merge
```

**Cost**: ~$3-5 / PR (highest — Opus implements + Opus final confirm)
**Wall time**: 45-90 min / PR (longest due to 4-layer review chain)

### Workflow D — codex plans / Sonnet implements / triple-review / Opus 統籌 (final triage)
Best for: **most standard PRs when Opus is in yellow/red quota**. Opus only appears at the very end as the triage/decision integrator — NOT planner, implementer, or reviewer. Cheapest workflow that still keeps human-equivalent rigor via 3 independent reviewers.

```
codex exec --model gpt-5.5 (effort: high) → plan-file in repo
  ↓
Claude Sonnet (Agent tool with model:"sonnet") → implement
  ↓
triple-review (gemini-cli + claude-mm/MiniMax + codex via codex-rescue) — no Opus
  ↓
Claude Opus → 統籌: read 3 reviews, triage findings, decide fix vs skip vs merge
  ↓
If fix needed → Sonnet applies; else direct merge
```

**Cost**: ~$0.5-1 / PR (Opus only at triage step, ~10-20k tokens; codex + gemini + claude-mm all OAuth-free)
**Wall time**: 30-50 min / PR (planning + impl + parallel review + triage)

Workflow D vs B: B has Opus AS a reviewer (dual review codex+Opus); D has Opus AFTER reviewers as final integrator + adds 3rd reviewer (gemini). Slight cost tradeoff for diversity gain.

Workflow D vs A: A has Opus AS planner + verifier (heavy); D moves planning to codex + drops Opus verify (Sonnet's clean impl + triple-review compensates). Big Opus saving.

### Workflow E — Sonnet plans / Codex implements / triple-review / Opus 統籌
Best for: **mechanical refactor at scale (module extraction, library swap, multi-PR pattern-mirror track), data-flow rewiring where Sonnet's Read/Grep visibility into cross-section dependencies pays off, and tasks where the plan is mostly "find all callsites and move literally"**.

The maxim of this workflow: **Sonnet sees the codebase, Codex follows the plan literally**. Sonnet's Read/Grep tooling catches cross-section dependencies that codex CLI (in sandboxed plan-mode) misses. Codex implementer is the most disciplined "literal mover" — it won't add defensive guards (a recurring Opus failure mode in mechanical PRs) and won't drift from plan placement (the F9b lesson where Opus picked "happens to satisfy" position instead of "earliest safe").

```
Claude Sonnet (Agent tool with model:"sonnet", no isolation needed) → plan-file in repo
  ↓
Codex (Agent tool with subagent_type:"codex:codex-rescue", isolation:"worktree") → implement
  ↓
triple-review (agy/gemini-cli + claude-mm/MiniMax + codex via codex-family CLI)
  ↓
Claude Opus → 統籌: read 3 reviews, triage, decide fix vs skip vs merge
  ↓
If fix needed → Opus applies in-PR fix-round; else direct merge
```

**Cost**: ~$0.3-0.5 / PR (sonnet plan ~5-15k tokens; codex impl + reviewers all OAuth-free; Opus only at triage ~10-20k)
**Wall time**: 25-40 min / PR (validated on scheduler F9a-F9c trials 2026-05-25)

Workflow E vs D: D uses codex planner + Sonnet impl; E swaps both — Sonnet's Read/Grep makes plans grep-accurate, and Codex's literal-execution discipline avoids the "implementer adds something the plan didn't call for" failure mode that bit Opus in F9a (defensive coercion) and F9b (late setter placement).

Workflow E vs A: A is heavy-Opus (plan + verify). E is light-Opus (triage only). E pays for the saving with a slightly weaker planner (Sonnet < Opus on architecture trade-offs) — only use E when the task is mechanical/transcriptional, not SPEC-level.

### Workflow Mini — solo, no triple-review
Best for: **hotfixes, single-file deploys, config tweaks, doc-only changes, anything
where speed-to-merge > review depth**.

```
Whoever is in context → plan + implement in single pass
  ↓
Self-verify (run tests if applicable)
  ↓
Single reviewer (or skip if obvious + low-risk)
  ↓
Direct merge (per ADR-015 if applicable, hotfix branch off main)
```

**Cost**: ~$0.1 / PR
**Wall time**: 5-15 min / PR

## Decision matrix

| Task pattern | Difficulty | Workflow | Why |
|---|---|---|---|
| Hotfix (deploy blocker, single-file) | Small | **Mini** | Speed-to-merge wins; e.g. PR #193 (apps/web/public/.gitkeep) |
| Typo / doc fix | Trivial | **Mini via claude-mm** | claude-mm = $0 marginal; saves any Opus budget for triage roles |
| Config / Docker / docker-compose | Small-Med | **Mini or D** | mechanical; if multi-file env wiring → D for triple-review safety |
| Pattern-mirror impl (new detector cloning existing pattern) | Small-Med | **B or D** | Plan = transcription; Sonnet fast at this. D when Opus quota tight (which is the default lately). |
| Pattern-mirror impl with risk concern | Med | **D** | Triple-review catches alpha-affecting subtleties; Opus 統籌 makes the merge call |
| SPEC / ADR-level new invariant | Med-Large | **A** (if Opus available) or **D** (Opus tight) | Plan must own the decision; D's codex-planner suffices if Opus is yellow |
| Algorithmic correctness (math / EMA / window logic) | Med-Large | **C** | PR #188 EMA bug suite — Opus plan + codex reviewer caught 4 HIGH; high-stakes correctness deserves the 4-layer review chain |
| Risk validator / hard-limit change | Any | **C — codex plans + Opus implements + 3 reviewers + Opus final** | CLAUDE.md invariant #1 — "risk controls outrank alpha"; maximum model diversity protects against single-model blind spots. NEVER substitute D here. |
| New SPEC invariant / phase-transition gate | Large | **C** | If this lands wrong, an ADR has to undo it. Pay for the diversity. |
| Live-flag flip / capital scaling | Large | **C** | Highest blast radius decision in the project |
| New backtest infra / data ingestion | Med | **D** (Workflow A's planner role is overkill — Workflow B/D's codex planner + Sonnet impl + triple review = sufficient) | Structural + medium decision; data correctness caught by triple review |
| Plan-file / track plan / phase exit doc | Small-Med | **A** (if Opus available) or **D** (Opus tight) | Planning IS the work; D delegates plan to codex w/ rigor recovery via triple-review |
| Refactor with no behavior change | Small-Med | **D** | Pattern-mirror at scale; tests pin behavior; Opus only at triage |
| Mechanical module-extract / multi-PR refactor track (e.g. split a big file into sections) | Small-Med per PR | **E** | scheduler F9a-F9c validated: Sonnet plan catches cross-section dependencies (e.g. F9c's `escapeHtml` shared by health section), Codex impl never drifts from plan or adds defensive coercion. F9a (codex plan + Opus impl) and F9b (same) each had 1 Opus-induced fix-round; F9c (E) shipped clean. |
| Library swap / version upgrade with no API change | Small-Med | **E** | Same literal-move profile as module extract |
| Multi-PR track where each PR is small + mechanical | Per-PR Small | **E** (per PR) | Cheap per PR; Opus triage compounds across PRs without burning Opus per impl |
| Hotfix touching prod hot-path | Small | **Mini + paired dual review** | Speed but extra eyes; e.g. ADR-022 deferred urgent fix |
| Multi-track parallel work | Any | **D per sub-track** (coordinator dispatches); 統籌 is Opus's role per track | Don't bundle workflows in one PR |
| Doc PR (ADR / plan revision / handover) | Small-Med | **D or Mini-via-claude-mm** | Trivial → claude-mm; ADR → D with codex+gemini+claude-mm review |

**Default when row unclear**: **D** (the broad default when Opus is in yellow/red). Use **E** specifically for mechanical refactor / literal-move tasks where "the plan is mostly grep + transcription" — E saves Opus completely (only at triage) and avoids the Opus-implementer failure modes (defensive coercion, "happens to satisfy" placement). Fall back to A only when Opus is freshly recharged AND the decision authority on the plan needs to be Opus.

### Workflow cost / wall-time / safety summary

| | Cost / PR | Wall time | Opus burn | Bug-catch depth | Use when |
|---|---|---|---|---|---|
| **Mini** | ~$0.1 | 5-15 min | minimal (or $0 via claude-mm) | minimal | hotfix / typo / config tweak |
| **D** | ~$0.5-1 | 30-50 min | low (~10-20k for triage) | high (triple-review + Opus 統籌) | **default** for most PRs when Opus is yellow/red |
| **B** | ~$0.3-0.8 | 25-50 min | mid (Opus as reviewer) | mid | mechanical pattern-mirror impls when Opus has budget |
| **A** | ~$1-2 | 30-60 min | high (Opus plan + verify) | high | SPEC-level / multi-file / paper-mode work when Opus available |
| **E** | ~$0.3-0.5 | 25-40 min | minimum (~10-20k for triage only) | high (triple-review + Opus 統籌) | **mechanical refactor / multi-PR module-extract track** — Sonnet plan + Codex impl combo is the cleanest "literal mover" available |
| **C** | ~$3-5 | 45-90 min | maximum (Opus impl + Opus final) | maximum | risk / live / algorithmic-core / capital |

## Calibration notes (from narrative-trader 2026-05-12 trials)

- **Workflow A trial (PR-B-6.5)**: Opus plan got 3 HIGH + 5 MEDIUM + 3 LOW in
  codex plan-review round 1. After revision, awaiting round 2. Sample of 1 — too
  early to conclude plan-quality.
- **Workflow A side-effect data (PR #187 / #188 / #189)**: codex implementer
  produced mypy/black/ruff/pytest-green first commit 3/3 times. Triple-review
  caught 4 HIGH on #188 + 1 HIGH on #189 + 1 MEDIUM on #187 — all real bugs.
- **Multi-codex race condition (lesson)**: codex agents must NOT `cd` into the
  main repo from their worktree (per `feedback_multi_codex_parallel.md`).
  Applies to both A and B.

## Calibration notes (from scheduler F9 module-split track, 2026-05-25)

Sampled across 3 mechanical refactor PRs (F9a/F9b/F9c) where the task was
"extract N functions from src/app.js into a new src/sections/X.js module":

- **F9a (Workflow inverse: codex plan + Opus impl)**: PR #45 triple-review
  found 1 MEDIUM — Opus added `Array.isArray ? x : []` defensive coercion to
  setters that codex plan never called for. Fix-round required. Plan was
  correct; implementer overstepped.
- **F9b (same: codex plan + Opus impl)**: PR #46 triple-review found 1 HIGH —
  Opus wired a callback setter at "happens to satisfy" position (right before
  fetch, but AFTER a top-level synchronous boot path the plan didn't enumerate
  in detail). Fix-round required. Plan said "wire before Y"; implementer chose
  late position instead of earliest safe.
- **F9c (NEW: Sonnet plan + Codex impl = Workflow E)**: PR #47 triple-review
  ... (running at time of writing; pending result will update this note).
  Sonnet plan caught the `escapeHtml` cross-section dependency that codex
  CLI plan would have missed (sandbox can't easily grep across whole repo).
  Codex impl shipped 461/461 tests green, picked plan's Option A (single-
  source escapeHtml) without drift.

**Recurring Opus-implementer failure modes** (record for future routing):
1. Adds defensive guards (try/catch, Array.isArray, null-check) not in the plan
2. Picks "happens to satisfy" position instead of "earliest safe" position
3. Edits adjacent code "while I'm here" — violates "surgical changes"

Codex-implementer empirically avoids all three. Sonnet-implementer (Workflow D)
sits in the middle — better than Opus on (1) and (3), comparable to Codex on (2).

**Recurring Sonnet-planner advantage**:
- Read/Grep tooling enumerates cross-section dependencies. Codex CLI runs in
  sandbox-read-only and can grep but its scratch context is smaller. Sonnet's
  Agent runtime has the same full Read/Grep available without sandbox limits.

**Workflow E adoption recommendation**: for any task in the matrix marked
"refactor with no behavior change" OR "pattern-mirror at scale" OR "multi-PR
track of small mechanical PRs", route to E instead of D. Reserve D for cases
where the implementer needs to make small judgment calls (Sonnet > Codex at
this) and the plan can stay codex-light.

## Anti-patterns

- ❌ Switching workflows mid-PR (plan in A then dispatch B mid-flight) — sample
  pollution + spec drift
- ❌ Skipping plan-file for "obvious" tasks that turn out to have edge cases —
  upgrade to A if discovery shows hidden complexity
- ❌ Picking B for risk-validator-touching code — invariant #1 wins regardless of
  speed
- ❌ Picking Mini for anything that touches `packages/risk` or `packages/execution`
- ❌ Letting an implementer (codex or Sonnet) make planning decisions ("I'll just
  add field X" without ADR) — escalate to planner

## How to apply (decision algorithm)

1. Read task description
2. Match against matrix row patterns (§Decision matrix)
3. If match found → tentative pick
4. If no match → default A
5. If risk-touching → A regardless (CLAUDE.md invariant #1 wins)
6. **Apply elasticity gate** (§Elastic routing per usage budget) — if the
   tentative pick's primary model is rate-limited / near burn, fall back
7. **Apply parallelism gate** — if 2+ independent tracks → all must run in
   `isolation: "worktree"` agents (§Parallel work hygiene). Sequential
   shared-tree edits cause race conditions.
8. Announce: "Routing this as Workflow [A|B|Mini] because [matrix row reason] +
   usage gate [OK / fell back from X to Y]"
9. Invoke the workflow's first step

## Elastic routing per usage budget

Before committing to a workflow, check the model availability that workflow
depends on. **A pre-flight check beats hitting a wall mid-task.**

### Codex (gpt-5.5 / gpt-5.4 / spark) — used by B planner + A implementer + reviewers

- Quota: ChatGPT Plus 5-hour rolling window; rate limit visible via
  `codex companion status --json` (or watching for `429` in recent runs)
- Burn-rate heuristic: each codex review ~ 20-40k tokens; each codex impl
  task ~ 25-45k tokens. ~5 medium tasks per 5h window is the practical ceiling.
- **Yellow light** (~70% burn): downgrade — pick Mini or A-with-fewer-codex-roles
- **Red light** (rate-limited): skip codex entirely this window; A becomes
  "Opus plans + Sonnet implements + gemini-only review" or defer to next window

### Claude Code (Opus / Sonnet) — used by A planner / A verifier / B reviewer

- Opus quota tighter than Sonnet (Anthropic plan tier-dependent)
- Burn-rate heuristic: each Opus plan-file ~ 30-80k tokens; verify pass ~
  15-30k; review ~ 20-40k. Heavy A workflow can burn 150k+/PR.
- **Yellow light** (~60% burn): drop Opus from verify role, use Sonnet (cheaper
  ~5x); keep Opus only at planner role
- **Red light** (rate-limited Opus): A workflow falls back to "Sonnet plans
  with extra plan-review" or full B; or defer
- **Sonnet is the elastic buffer** — almost always available, ~5x cheaper than
  Opus, fast. When in doubt, pick Sonnet over Opus.

### Pre-flight quick checks (run before dispatching)

```bash
# Codex
node ~/.claude/plugins/cache/openai-codex/codex/*/scripts/codex-companion.mjs setup --json | jq '.usage'

# Claude (proxy: count recent agent calls + estimate)
# No direct API; estimate from session history. If last 3 agents have been Opus
# heavy → switch next dispatch to Sonnet
```

### Routing under stress

| Yellow / Red conditions | Substitution |
|---|---|
| Codex yellow | Use codex for impl only (skip codex review role) |
| Codex red | A: Opus plans → Sonnet impl → gemini+claude-mm review (no codex). B: defer |
| Opus yellow | A: keep Opus plan, drop Opus verify → Sonnet verify |
| Opus red | Drop A entirely; use B if codex green, else Mini-with-Sonnet |
| Both yellow | Mini-only; defer non-urgent A/B work to next window |
| Both red + task urgent | Pause; explain to user; recommend wait for window reset |

## Parallel work hygiene

When 2+ independent tasks dispatch in parallel:

- **Every parallel agent MUST use `isolation: "worktree"`** on the Agent tool.
  No shared main-repo working-tree edits. Per
  `feedback_multi_codex_parallel.md`: codex agents that share main-repo cwd
  race over HEAD + clobber untracked files (observed 2026-05-12, recovery cost
  ~20 min).
- **Codex agent prompts MUST NOT contain `cd /home/.../<repo>`.** That
  command leaves the worktree sandbox and pulls the agent into the shared
  main repo, defeating worktree isolation.
- **`git add -A` is dangerous in parallel-work zones.** Use specific paths.
  Add `.gitignore` rules for harness state (`.omc/`, `.claude/worktrees/`,
  worktree-tag files like `.omx-*`).
- **Branch creation is in-prompt only.** The Agent harness places codex in
  worktree-`<id>` branch by default. Brief tells codex what to RENAME it to
  AFTER work is done; never `git checkout -b feature/X origin/develop` mid-
  agent (race).
- **After parallel agents complete**, collect work via `git worktree list` —
  cherry-pick or merge from each worktree's branch. Don't expect them to
  push individually; harness does.

## Cross-references

- `~/.claude/skills/triple-review/SKILL.md` — invoked at end of A; conditionally at end of B
- `docs/MONEY_PATH_PLAN.md §10` (project-specific) — live A/B trial metrics
- `feedback_multi_codex_parallel.md` — codex parallelism pitfall
- `feedback_autonomous_merge.md` — merge gate criteria

## Pending updates

- When PR-B-6.5 (Workflow A trial) completes, fill MONEY_PATH_PLAN.md §10 column A
- When ADR-022 A3 (Workflow B trial) completes, fill column B
- After both, revise matrix rows with TBD → concrete recommendation
