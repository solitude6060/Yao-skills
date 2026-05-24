---
name: workflow-routing
description: Pick the right plan / implement / review workflow (A / B / C / D / E / Mini) for a coding task based on task type, difficulty, and risk level. Backed by real-world A/B trial data. Use BEFORE non-trivial PR work, when deciding "which model plans and which implements".
---

# /workflow-routing — pick the plan / impl / review workflow

Before non-trivial implementation work, route the task through this matrix. The
matrix is calibrated against real-world A/B trial data across multiple projects;
update the calibration rows as you accumulate your own observations.

## When to use

- Before non-trivial impl work, run through this skill to pick A / B / C / D / E / Mini
- When user asks "which workflow", "how do we tackle this", "plan/implement split"
- When opening a new feature/track plan-file (per CLAUDE.md §4)
- **Not for**: typo fixes, single-line config tweaks, doc-only edits — skip routing, just do it

## The workflows

### Workflow A — Opus plans / Codex implements / Opus verifies / triple-review
Best for: **SPEC / ADR-level decisions, algorithmic correctness, multi-file
architectural changes, anything where planning precision > implementation speed**.

```
Opus → plan-file in repo (docs/<TRACK>_PLAN.md)
  ↓
Codex (Agent tool, isolation:worktree) → implement
  ↓
Opus → verify (tests + type-check + lint + diff review)
  ↓
triple-review (3 independent reviewers from different model families)
  ↓
fix round if findings, then merge
```

**Cost**: ~$1-2 / PR (Opus is the expensive layer)
**Wall time**: 30-60 min / PR

### Workflow B — Codex plans / Sonnet implements / Codex+Opus review
Best for: **mechanical / pattern-mirror implementations, well-spec'd small-to-medium
features, anything where the plan is mostly transcription from existing patterns**.

```
Codex (high effort) → plan-file in repo
  ↓
Claude Sonnet (Agent tool with model:"sonnet") → implement
  ↓
Codex review + Opus review (dual, parallel)
  ↓
fix round if findings
```

**Cost**: ~$0.3-0.8 / PR (Sonnet ~5x cheaper than Opus; Codex via OAuth = $0)
**Wall time**: ~25-50 min / PR

### Workflow C — Codex plans / Opus implements / triple-review / Opus final confirm
Best for: **highest-stakes work — risk validators, hard limits, live flags,
phase transitions, new SPEC invariants, algorithmic core (e.g., precision math,
numerical correctness, walk-forward integrity)**.

The maxim of this workflow: **no single model owns the whole pipeline**.
Codex plans (different brain than implementer), Opus implements (heavy
reasoning + deeper context), three independent reviewers, then Opus
re-confirms by reviewing the reviewers' verdicts — final decision authority
separated from implementation authority.

```
Codex (high effort) → plan-file in repo
  ↓
Claude Opus (Agent tool with model:"opus") → implement
  ↓
triple-review (3 independent reviewers — no Opus in review pool)
  ↓
Claude Opus → final confirm: read all 3 reviews, triage, decide merge / revise / block
  ↓
If revise → fix round (back to Opus implement); else merge
```

**Cost**: ~$3-5 / PR (highest — Opus implements + Opus final confirm)
**Wall time**: 45-90 min / PR (longest due to 4-layer review chain)

### Workflow D — Codex plans / Sonnet implements / triple-review / Opus triage
Best for: **most standard PRs when Opus quota is tight**. Opus only appears at the
very end as the triage/decision integrator — NOT planner, implementer, or reviewer.
Cheapest workflow that still keeps human-equivalent rigor via 3 independent reviewers.

```
Codex (high effort) → plan-file in repo
  ↓
Claude Sonnet (Agent tool with model:"sonnet") → implement
  ↓
triple-review (3 independent reviewers — no Opus)
  ↓
Claude Opus → triage: read 3 reviews, decide fix vs skip vs merge
  ↓
If fix needed → Sonnet applies; else direct merge
```

**Cost**: ~$0.5-1 / PR (Opus only at triage step, ~10-20k tokens)
**Wall time**: 30-50 min / PR

Workflow D vs B: B has Opus AS a reviewer (dual review Codex+Opus); D has Opus AFTER reviewers as final integrator + adds 3rd reviewer. Slight cost tradeoff for diversity gain.

Workflow D vs A: A has Opus AS planner + verifier (heavy); D moves planning to Codex + drops Opus verify (Sonnet's clean impl + triple-review compensates). Big Opus saving.

### Workflow E — Sonnet plans / Codex implements / triple-review / Opus triage
Best for: **mechanical refactor at scale (module extraction, library swap, multi-PR pattern-mirror track), data-flow rewiring where Sonnet's Read/Grep visibility into cross-section dependencies pays off, and tasks where the plan is mostly "find all callsites and move literally"**.

The maxim of this workflow: **Sonnet sees the codebase, Codex follows the plan literally**. Sonnet's Read/Grep tooling catches cross-section dependencies that Codex CLI (in sandboxed plan-mode) misses. Codex implementer is the most disciplined "literal mover" — it won't add defensive guards (a recurring Opus failure mode in mechanical PRs) and won't drift from plan placement.

```
Claude Sonnet (Agent tool with model:"sonnet") → plan-file in repo
  ↓
Codex (Agent tool, isolation:"worktree") → implement
  ↓
triple-review (3 independent reviewers)
  ↓
Claude Opus → triage: read 3 reviews, decide fix vs skip vs merge
  ↓
If fix needed → Opus applies in-PR fix-round; else direct merge
```

**Cost**: ~$0.3-0.5 / PR (Sonnet plan ~5-15k tokens; Codex impl via OAuth; Opus only at triage ~10-20k)
**Wall time**: 25-40 min / PR

Workflow E vs D: D uses Codex planner + Sonnet impl; E swaps both — Sonnet's Read/Grep makes plans grep-accurate, and Codex's literal-execution discipline avoids the "implementer adds something the plan didn't call for" failure mode.

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
Direct merge (hotfix branch off main if applicable)
```

**Cost**: ~$0.1 / PR
**Wall time**: 5-15 min / PR

## Decision matrix

| Task pattern | Difficulty | Workflow | Why |
|---|---|---|---|
| Hotfix (deploy blocker, single-file) | Small | **Mini** | Speed-to-merge wins |
| Typo / doc fix | Trivial | **Mini** | No review surface to speak of |
| Config / Docker / docker-compose | Small-Med | **Mini or D** | Mechanical; if multi-file env wiring → D for triple-review safety |
| Pattern-mirror impl (cloning existing pattern) | Small-Med | **B or D** | Plan = transcription; Sonnet fast at this. D when Opus quota tight. |
| Pattern-mirror impl with risk concern | Med | **D** | Triple-review catches subtle bugs; Opus triage makes the merge call |
| SPEC / ADR-level new invariant | Med-Large | **A** (if Opus available) or **D** (Opus tight) | Plan must own the decision; D's Codex-planner suffices if Opus is scarce |
| Algorithmic correctness (math / precision logic) | Med-Large | **C** | High-stakes correctness deserves the 4-layer review chain |
| Risk validator / hard-limit change | Any | **C** | Maximum model diversity protects against single-model blind spots. NEVER substitute D here. |
| New SPEC invariant / phase-transition gate | Large | **C** | If this lands wrong, an ADR has to undo it. Pay for the diversity. |
| New infrastructure / data ingestion | Med | **D** | Structural + medium decision; data correctness caught by triple review |
| Plan-file / track plan / phase exit doc | Small-Med | **A** (if Opus available) or **D** (Opus tight) | Planning IS the work; D delegates plan to Codex with rigor recovery via triple-review |
| Refactor with no behavior change | Small-Med | **D** | Pattern-mirror at scale; tests pin behavior; Opus only at triage |
| Mechanical module-extract / multi-PR refactor track | Small-Med per PR | **E** | Sonnet plan catches cross-section dependencies; Codex impl never drifts from plan or adds defensive code |
| Library swap / version upgrade with no API change | Small-Med | **E** | Same literal-move profile as module extract |
| Multi-PR track where each PR is small + mechanical | Per-PR Small | **E** (per PR) | Cheap per PR; Opus triage compounds across PRs without burning Opus per impl |
| Hotfix touching prod hot-path | Small | **Mini + paired dual review** | Speed but extra eyes |
| Multi-track parallel work | Any | **D per sub-track** (coordinator dispatches) | Don't bundle workflows in one PR |
| Doc PR (ADR / plan revision / handover) | Small-Med | **D or Mini** | Trivial → Mini; ADR → D with full review |

**Default when row unclear**: **D** (the broad default when Opus quota is tight). Use **E** specifically for mechanical refactor / literal-move tasks where "the plan is mostly grep + transcription" — E saves Opus completely (only at triage) and avoids the Opus-implementer failure modes (defensive coercion, "happens to satisfy" placement). Fall back to A only when Opus is freshly recharged AND the decision authority on the plan needs to be Opus.

### Workflow cost / wall-time / safety summary

| | Cost / PR | Wall time | Opus burn | Bug-catch depth | Use when |
|---|---|---|---|---|---|
| **Mini** | ~$0.1 | 5-15 min | minimal | minimal | hotfix / typo / config tweak |
| **D** | ~$0.5-1 | 30-50 min | low (~10-20k for triage) | high (triple-review + Opus triage) | **default** for most PRs when Opus is scarce |
| **B** | ~$0.3-0.8 | 25-50 min | mid (Opus as reviewer) | mid | mechanical pattern-mirror impls when Opus has budget |
| **A** | ~$1-2 | 30-60 min | high (Opus plan + verify) | high | SPEC-level / multi-file / paper-mode work when Opus available |
| **E** | ~$0.3-0.5 | 25-40 min | minimum (~10-20k for triage only) | high (triple-review + Opus triage) | **mechanical refactor / multi-PR module-extract track** |
| **C** | ~$3-5 | 45-90 min | maximum (Opus impl + Opus final) | maximum | risk / live / algorithmic-core / capital |

## Observed patterns — model-as-implementer failure modes

Sampled across multiple mechanical refactor PRs where the task was
"extract N functions from module A into module B":

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
this) and the plan can stay Codex-light.

## Anti-patterns

- ❌ Switching workflows mid-PR (plan in A then dispatch B mid-flight) — sample
  pollution + spec drift
- ❌ Skipping plan-file for "obvious" tasks that turn out to have edge cases —
  upgrade to A if discovery shows hidden complexity
- ❌ Picking B for risk-critical code — safety invariants win regardless of speed
- ❌ Picking Mini for anything that touches risk or execution paths
- ❌ Letting an implementer (Codex or Sonnet) make planning decisions ("I'll just
  add field X" without ADR) — escalate to planner

## How to apply (decision algorithm)

1. Read task description
2. Match against matrix row patterns (§Decision matrix)
3. If match found → tentative pick
4. If no match → default D
5. If risk-touching → C regardless (safety invariants win)
6. **Apply elasticity gate** (§Elastic routing per usage budget) — if the
   tentative pick's primary model is rate-limited / near burn, fall back
7. **Apply parallelism gate** — if 2+ independent tracks → all must run in
   `isolation: "worktree"` agents (§Parallel work hygiene). Sequential
   shared-tree edits cause race conditions.
8. Announce: "Routing this as Workflow [A|B|C|D|E|Mini] because [matrix row reason] +
   usage gate [OK / fell back from X to Y]"
9. Invoke the workflow's first step

## Elastic routing per usage budget

Before committing to a workflow, check the model availability that workflow
depends on. **A pre-flight check beats hitting a wall mid-task.**

### Codex — used by planner + implementer + reviewer roles

- Quota: typically a rolling-window rate limit; check your plan's quota dashboard
- Burn-rate heuristic: each Codex review ~ 20-40k tokens; each Codex impl
  task ~ 25-45k tokens. ~5 medium tasks per window is the practical ceiling.
- **Yellow light** (~70% burn): downgrade — pick Mini or A-with-fewer-Codex-roles
- **Red light** (rate-limited): skip Codex entirely this window; defer to next window

### Claude Code (Opus / Sonnet) — used by planner / verifier / reviewer roles

- Opus quota tighter than Sonnet (plan-tier-dependent)
- Burn-rate heuristic: each Opus plan-file ~ 30-80k tokens; verify pass ~
  15-30k; review ~ 20-40k. Heavy A workflow can burn 150k+/PR.
- **Yellow light** (~60% burn): drop Opus from verify role, use Sonnet (cheaper
  ~5x); keep Opus only at planner role
- **Red light** (rate-limited Opus): A workflow falls back to "Sonnet plans
  with extra plan-review" or full B; or defer
- **Sonnet is the elastic buffer** — almost always available, ~5x cheaper than
  Opus, fast. When in doubt, pick Sonnet over Opus.

### Routing under stress

| Yellow / Red conditions | Substitution |
|---|---|
| Codex yellow | Use Codex for impl only (skip Codex review role) |
| Codex red | Opus plans → Sonnet impl → remaining reviewers (no Codex). Or defer |
| Opus yellow | Keep Opus plan, drop Opus verify → Sonnet verify |
| Opus red | Drop A entirely; use B if Codex green, else Mini-with-Sonnet |
| Both yellow | Mini-only; defer non-urgent A/B work to next window |
| Both red + task urgent | Pause; explain to user; recommend wait for window reset |

## Parallel work hygiene

When 2+ independent tasks dispatch in parallel:

- **Every parallel agent MUST use `isolation: "worktree"`** on the Agent tool.
  No shared main-repo working-tree edits. Agents that share main-repo cwd
  race over HEAD + clobber untracked files.
- **Agent prompts MUST NOT contain `cd /<absolute-path-to-repo>`.** That
  command leaves the worktree sandbox and pulls the agent into the shared
  main repo, defeating worktree isolation.
- **`git add -A` is dangerous in parallel-work zones.** Use specific paths.
  Add `.gitignore` rules for harness state directories.
- **Branch creation is in-prompt only.** The Agent harness places agents in
  worktree-`<id>` branch by default. Brief tells the agent what to rename it to
  after work is done; never `git checkout -b feature/X origin/develop` mid-
  agent (race).
- **After parallel agents complete**, collect work via `git worktree list` —
  cherry-pick or merge from each worktree's branch.

## Adapting to your setup

This skill assumes a multi-model CLI toolkit. Adapt the specific tool names to
your environment:

| Role in workflow | Example tools | What matters |
|---|---|---|
| Planner | Codex CLI, Claude Opus, Claude Sonnet | Can read codebase + produce structured plan |
| Implementer | Codex CLI, Claude Sonnet, Claude Opus | Can edit files in isolation (worktree) |
| Reviewer (lane 1) | Gemini CLI (`agy` or `gemini`), any non-Claude LLM | Model-family diversity from implementer |
| Reviewer (lane 2) | Secondary Claude Code endpoint | Operational / file-context verification |
| Reviewer (lane 3) | Codex CLI (secondary account) | Cross-reference / ADR-vs-impl drift |
| Triage / final call | Claude Opus | Integrates 3 reviews, makes merge decision |

The methodology (planner/implementer separation, 3-reviewer diversity, elastic
fallback) transfers regardless of which specific CLIs you have. If you only have
two reviewer endpoints, run with two and note which bug class becomes invisible
(see `triple-review` skill's Troubleshooting section).
