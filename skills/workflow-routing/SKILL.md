---
name: workflow-routing
description: Pick the right plan / implement / review workflow for a coding task based on task type, difficulty, risk level, and current model quota. Use BEFORE non-trivial PR work, when deciding "which model plans and which implements".
---

# /workflow-routing — pick the plan / impl / review workflow

Before non-trivial implementation work, route the task through this matrix. The matrix is calibrated on real projects but is meant as a starting template — adjust workflow names, prices, and quotas for your own setup.

## When to use

- Before non-trivial impl work, run through this skill to pick a workflow
- When user asks "which workflow", "how do we tackle this", "plan/implement split"
- When opening a new feature/track plan-file
- **Not for**: typo fixes, single-line config tweaks, doc-only edits — skip routing, just do it

## The 5 workflow variants

### Workflow A — Opus plans / Codex implements / Opus verifies / triple-review
Best for: **SPEC / ADR-level decisions, algorithmic correctness, multi-file architectural changes, anything where planning precision > implementation speed.**

```
Opus → plan-file in repo (docs/<TRACK>_PLAN.md)
  ↓
Codex implementer (Agent tool, isolation:worktree) → implement
  ↓
Opus → verify (tests + type-check + lints + diff review)
  ↓
triple-review (Gemini + secondary Claude Code + Codex)
  ↓
fix round if findings, then auto-merge per project's merge gate
```

**Cost**: roughly $1-2 / PR — Opus is the expensive layer
**Wall time**: 30-60 min / PR

### Workflow B — Codex plans / Sonnet implements / Codex+Opus review
Best for: **mechanical / pattern-mirror implementations, well-spec'd small-to-medium features, anything where the plan is mostly transcription from existing patterns.**

```
Codex exec → plan-file in repo
  ↓
Claude Sonnet (Agent tool with model:"sonnet") → implement
  ↓
Codex review + Opus review (dual, parallel)
  ↓
fix round if findings
```

**Cost**: ~$0.3-0.8 / PR (Sonnet roughly 5× cheaper than Opus; Codex via OAuth = $0)
**Wall time**: ~25-50 min / PR

### Workflow C — Codex plans / Opus implements / triple-review / Opus final confirm
Best for: **highest-stakes work — risk validator / hard-limit / live-flag / phase transition / new SPEC invariant / algorithmic core.**

The maxim: **no single model owns the whole pipeline**. Codex plans (different brain than implementer), Opus implements (heavy reasoning + deeper context), three independent reviewers, then Opus re-confirms by reviewing the reviewers' verdicts — decision authority separated from implementation authority.

```
Codex exec → plan-file in repo
  ↓
Claude Opus (Agent tool with model:"opus") → implement
  ↓
triple-review (Gemini + secondary Claude Code + Codex) — no Opus in review pool
  ↓
Claude Opus → final confirm: read all 3 reviews, triage, decide merge / revise / block
  ↓
If revise → fix round (back to Opus implement); else merge
```

**Cost**: ~$3-5 / PR (highest — Opus implements + Opus final confirm)
**Wall time**: 45-90 min / PR

### Workflow D — Codex plans / Sonnet implements / triple-review / Opus triage (final integrator)
Best for: **most standard PRs when Opus quota is tight.** Opus appears only at the very end as the triage / decision integrator — NOT planner, implementer, or reviewer. Cheapest workflow that still keeps human-equivalent rigor via 3 independent reviewers.

```
Codex exec → plan-file in repo
  ↓
Claude Sonnet (Agent tool with model:"sonnet") → implement
  ↓
triple-review (Gemini + secondary Claude Code + Codex) — no Opus
  ↓
Claude Opus → triage: read 3 reviews, decide fix vs skip vs merge
  ↓
If fix needed → Sonnet applies; else direct merge
```

**Cost**: ~$0.5-1 / PR (Opus only at triage, roughly 10-20k tokens)
**Wall time**: 30-50 min / PR

**Workflow D vs B**: B has Opus AS a reviewer (dual review codex+Opus); D has Opus AFTER reviewers as final integrator + adds 3rd reviewer (Gemini). Trade some cost for diversity.

**Workflow D vs A**: A has Opus AS planner + verifier (heavy); D moves planning to Codex + drops Opus verify (Sonnet's clean impl + triple-review compensates). Big Opus saving.

### Workflow Mini — solo, no triple-review
Best for: **hotfixes, single-file deploys, config tweaks, doc-only changes, anything where speed-to-merge > review depth.**

```
Whoever is in context → plan + implement in single pass
  ↓
Self-verify (run tests if applicable)
  ↓
Single reviewer (or skip if obvious + low-risk)
  ↓
Direct merge
```

**Cost**: ~$0.1 / PR
**Wall time**: 5-15 min / PR

## Decision matrix

| Task pattern | Difficulty | Workflow | Why |
|---|---|---|---|
| Hotfix (deploy blocker, single-file) | Small | **Mini** | Speed-to-merge wins |
| Typo / doc fix | Trivial | **Mini via secondary CLI** | secondary endpoint = $0 marginal; save Opus budget for triage |
| Config / Docker / docker-compose | Small-Med | **Mini or D** | Mechanical; multi-file env wiring → D for triple-review safety |
| Pattern-mirror impl (clone existing pattern) | Small-Med | **B or D** | Plan = transcription; Sonnet fast at this; D when Opus quota tight |
| Pattern-mirror impl with risk concern | Med | **D** | Triple-review catches subtleties; Opus triages |
| SPEC / ADR-level new invariant | Med-Large | **A** (Opus available) or **D** (Opus tight) | Plan must own the decision |
| Algorithmic correctness (math / EMA / window logic) | Med-Large | **C** | High-stakes correctness deserves the 4-layer review chain |
| Risk validator / hard-limit change | Any | **C** | NEVER substitute D here — max model diversity protects against single-model blind spots |
| New SPEC invariant / phase-transition gate | Large | **C** | If this lands wrong, an ADR has to undo it. Pay for diversity. |
| Live-flag flip / capital scaling | Large | **C** | Highest blast radius |
| New infra / data ingestion | Med | **D** | Structural; data correctness caught by triple-review |
| Plan-file / track plan / phase exit doc | Small-Med | **A** (Opus available) or **D** (Opus tight) | Planning IS the work |
| Refactor with no behavior change | Small-Med | **D** | Pattern-mirror at scale; tests pin behavior; Opus only at triage |
| Hotfix touching prod hot-path | Small | **Mini + paired dual review** | Speed but extra eyes |
| Multi-track parallel work | Any | **D per sub-track** | Don't bundle workflows in one PR |
| Doc PR (ADR / plan revision / handover) | Small-Med | **D or Mini-via-secondary-CLI** | Trivial → secondary CLI; ADR → D with full review |

**Default when row unclear**: **D** (covers most cases with rigor and minimal Opus burn). Fall back to A only when Opus is freshly recharged AND the plan's decision authority needs to be Opus.

### Workflow cost / wall-time / safety summary

| | Cost / PR | Wall time | Opus burn | Bug-catch depth | Use when |
|---|---|---|---|---|---|
| **Mini** | ~$0.1 | 5-15 min | minimal (or $0 via secondary CLI) | minimal | hotfix / typo / config tweak |
| **D** | ~$0.5-1 | 30-50 min | low (~10-20k for triage) | high (triple-review + Opus triage) | **default** when Opus is yellow/red |
| **B** | ~$0.3-0.8 | 25-50 min | mid (Opus as reviewer) | mid | mechanical pattern-mirror impls when Opus has budget |
| **A** | ~$1-2 | 30-60 min | high (Opus plan + verify) | high | SPEC-level / multi-file when Opus available |
| **C** | ~$3-5 | 45-90 min | maximum (Opus impl + Opus final) | maximum | risk / live / algorithmic-core / capital |

## Anti-patterns

- ❌ Switching workflows mid-PR (plan in A then dispatch B mid-flight) — sample pollution + spec drift
- ❌ Skipping plan-file for "obvious" tasks that turn out to have edge cases — upgrade to A on discovery
- ❌ Picking B for risk-validator-touching code — invariant #1 wins regardless of speed
- ❌ Picking Mini for anything touching the project's risk / execution / safety layers
- ❌ Letting an implementer (Codex or Sonnet) make planning decisions ("I'll just add field X" without ADR) — escalate to planner

## How to apply (decision algorithm)

1. Read the task description
2. Match against matrix row patterns
3. If matched → tentative pick
4. If no match → default D (or A if Opus is fresh)
5. If risk-touching → C (max diversity wins)
6. **Apply elasticity gate** — if the tentative pick's primary model is rate-limited / near burn, fall back
7. **Apply parallelism gate** — if 2+ independent tracks → all must run in `isolation: "worktree"` agents. Sequential shared-tree edits cause race conditions.
8. Announce: "Routing this as Workflow [X] because [matrix row reason] + usage gate [OK / fell back from Y to X]"
9. Invoke the workflow's first step

## Elastic routing per usage budget

Before committing to a workflow, check model availability. A pre-flight check beats hitting a wall mid-task.

### Codex quota (used by B planner + A implementer + reviewers)
- Quota: ChatGPT Plus 5-hour rolling window
- Burn-rate heuristic: each Codex review ~ 20-40k tokens; each Codex impl task ~ 25-45k tokens. ~5 medium tasks per 5h window is the practical ceiling.
- **Yellow** (~70% burn): downgrade — pick Mini or A-with-fewer-codex-roles
- **Red**: skip Codex entirely this window; A becomes "Opus plans + Sonnet implements + Gemini-only review" or defer

### Claude (Opus / Sonnet) quota
- Opus quota tighter than Sonnet (Anthropic plan tier-dependent)
- Burn-rate heuristic: each Opus plan-file ~ 30-80k tokens; verify pass ~ 15-30k; review ~ 20-40k. Heavy A can burn 150k+/PR.
- **Yellow** (~60% burn): drop Opus from verify role, use Sonnet (~5× cheaper); keep Opus only at planner role
- **Red**: A falls back to "Sonnet plans with extra plan-review" or full B; or defer
- **Sonnet is the elastic buffer** — almost always available, ~5× cheaper than Opus, fast. When in doubt, prefer Sonnet over Opus.

### Routing under stress

| Yellow / Red condition | Substitution |
|---|---|
| Codex yellow | Use Codex for impl only (skip Codex review role) |
| Codex red | A: Opus plans → Sonnet impl → Gemini+secondary review (no Codex). B: defer |
| Opus yellow | A: keep Opus plan, drop Opus verify → Sonnet verify |
| Opus red | Drop A entirely; use B if Codex green, else Mini-with-Sonnet |
| Both yellow | Mini-only; defer non-urgent A/B work to next window |
| Both red + urgent | Pause; explain to user; recommend waiting for window reset |

## Parallel work hygiene

When 2+ independent tasks dispatch in parallel:

- **Every parallel agent MUST use `isolation: "worktree"`** on the Agent tool. No shared main-repo working-tree edits — multiple Codex agents on the shared main repo race over HEAD + clobber untracked files.
- **Codex agent prompts MUST NOT contain `cd /home/.../<main-repo>`.** That leaves the worktree sandbox and pulls the agent into the shared main repo, defeating isolation.
- **`git add -A` is dangerous in parallel-work zones.** Use specific paths. Add `.gitignore` rules for harness state (`.omc/`, `.claude/worktrees/`, etc.).
- **Branch creation is in-prompt only.** Brief the agent to rename its branch AFTER work completes; never `git checkout -b feature/X origin/develop` mid-agent (race).
- **After parallel agents complete**, collect work via `git worktree list` — cherry-pick or merge from each worktree's branch.

## Cross-references

- `skills/triple-review/SKILL.md` — invoked at end of A; conditionally at end of B
- Project's `docs/<plan-file>` — live A/B trial metrics (if any)
