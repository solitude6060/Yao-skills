# yao-skills

English | [繁體中文](./README.zh.md)

A small, opinionated set of Claude Code skills for code review, incident triage, workflow routing, and project health checks — plus a curated subset of [oh-my-claudecode](https://github.com/Yeachan-Heo/oh-my-claudecode) skills for planning and orchestration, and behavioral guidelines from [andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills).

**This is a community-shared version.** The methodology and decision frameworks are the core value — they transfer across projects and tech stacks. Specific tool names (Codex, Gemini CLI, etc.) are examples; adapt them to your own multi-model setup. Fork it, modify it, make it yours. If you build something useful on top of it, PRs and issues are welcome.

## Skills

### Author-original

| Skill | What it does |
|---|---|
| `triple-review` | Orchestrator-aware three-reviewer PR review: Claude Code uses `codex` + `agy`/`gemini` + secondary endpoint; Codex uses `claude` + `agy`/`gemini` + secondary endpoint; includes severity triage, TDD fix cycle, auto-merge gate |
| `first-principles` | Assumption-audit and incident triage discipline: 5-question audit, ground-truth verification, mandatory dual/triple review on hotfixes |
| `workflow-routing` | Pick A/B/C/D/E/Mini workflow per task type, risk level, and current Opus / Codex quota |
| `project-status-review` | Generate a comprehensive project status report — code stats, branch divergence, blockers, prioritized next steps |
| `context-hygiene` | Manage session context cost: when to `/compact` vs handover-doc + `/clear`, the cache cost math (cached input is 0.1x not zero; output never cached), handover template, loop session checkpointing, and task-to-tool routing (Sonnet/Opus/Codex/Gemini CLI/secondary endpoint) |
| `distilled-caveman-lite-accuracy` | Lite response compression — removes filler and pleasantries while preserving 100% technical accuracy. Keeps qualifiers, code identifiers, versions, step order, safety context. Safety fallback auto-expands for destructive ops, auth, crypto, compliance. Trigger: "caveman-lite", "lite mode", "brief but accurate", "less tokens" |

### Curated from oh-my-claudecode (MIT, see `NOTICE.md`)

`ralph`, `plan`, `deep-interview`, `deep-dive`, `learner`, `skillify`, `sciomc`, `autoresearch`, `ralplan`, `ai-slop-cleaner`, `team`, `release`, `autopilot`, `ultrawork`.

### Curated from andrej-karpathy-skills (MIT, see `NOTICE.md`)

| Skill | What it does |
|---|---|
| `karpathy-guidelines` | Behavioral guidelines distilled from Andrej Karpathy's observations on LLM coding pitfalls: think before coding, simplicity first, surgical changes, goal-driven execution |

#### When to use which orchestration mode

| Mode | Operating style | Best for |
|---|---|---|
| `autopilot` | Independent autonomous single-lead agent | Fast independent feature dev / prototyping from a 2–3 line idea |
| `team` | 5-stage pipeline (plan → prd → exec → verify → fix) | Multi-file changes needing peer architecture review |
| `ralph` | Persistent self-referential strict-verification loop | Critical prod bug fixes that must be fully resolved |
| `ultrawork` | Max-parallel non-team agent operation | Large-scale refactor across unrelated codebases |
| `ralplan` | Consensus planning gate before execution | Vague / ambiguous "ralph this" / "autopilot this" requests |

Picker order: vague request → `ralplan` first. Independent prototype → `autopilot`. Multi-file design-sensitive change → `team`. Must-fix prod bug → `ralph`. Parallel-friendly bulk refactor → `ultrawork`.

## Install

### Claude Code (native — recommended)

Two paths:

**A. One-shot marketplace install (easiest)**

```
/plugin marketplace add solitude6060/Yao-skills
/plugin install yao-skills@yao-skills
```

Open a new Claude Code session and all 21 skills become invocable via the `Skill` tool / `/yao-skills:<skill-name>`.

**B. Per-skill copy (if you only want some)**

```bash
git clone https://github.com/solitude6060/Yao-skills /tmp/yao-skills
cp -r /tmp/yao-skills/skills/triple-review ~/.claude/skills/
cp -r /tmp/yao-skills/skills/first-principles ~/.claude/skills/
# ...etc
```

Skill becomes invocable via the `Skill` tool / `/<skill-name>`.

### `CLAUDE.md` template

```bash
cp templates/CLAUDE.md ~/.claude/CLAUDE.md   # only if you don't already have one
```

Then edit to your needs.

#### Core concepts in the template

`templates/CLAUDE.md` is a global behavioral contract for Claude Code, biased toward rigor + audit-trail over speed. Nine sections:

1. **Spec Before Code** — read SPEC/README first; ADR before deviating. Code ≠ spec.
2. **Test Before Implementation** — Red → Green → Refactor. Bug fix = regression test + fix, never just the fix.
3. **Surgical Changes + Audit Trail** — touch only what the task requires. `what` in commit subject; `why + SPEC/ADR/issue link` in body. Observability events over inline comments.
4. **Plan in Files, Not Chat** — non-trivial work starts with a plan file committed to the repo (`docs/<TRACK>_PLAN.md`). Reviews land as `docs/<REVIEWER>_<DATE>_<SCOPE>.md` _before_ fixes; matching `_FIX_LOG.md` ships with the fix PR.
5. **Code-Review Handling** — verify each finding against code; triage by severity; TDD-order fixes; ship `_FIX_LOG.md` with the PR.
6. **Branch + PR Discipline** — feature branch off integration; merge via PR with `--no-ff`; deploy chain `develop → main → production`; destructive ops require explicit sign-off.
7. **First-Principles When Blocked** — first proposed fix is usually a workaround; stop and re-derive. Red flags: "lower threshold", "skip check", "disable test", "hardcode for now". User pushback "first principles?" → re-derive, don't defend.
8. **When in Doubt** — ask, don't guess. Reversible-default: paper before live, staging before prod, dry-run before apply, archive before delete.
9. **Writing Style for Chat** — plain language, no mid-sentence English jargon (when the default language is non-English), no figurative imagery substituting for clarity, concrete numbers + tables over claims. Repo artefacts (code, commits, PR descriptions) stay English.

**Working signal:** plan-files exist before the diff lands, reviews have matching fix-logs, git history reads like a TDD cycle (`test:` → `feat:`), and clarifying questions come before mistakes rather than after them.

### Codex CLI (OpenAI)

Codex has no Claude Code-style plugin marketplace. Treat Codex as its own
runtime: install compatible skills under `~/.codex/skills/<name>/SKILL.md` and
put global behavioral guidance in `~/.codex/AGENTS.md`.

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

**Caveats:**

- Do not bulk-copy the whole Claude Code plugin into `~/.codex/skills`. Some
  skills assume `/oh-my-claudecode`, Claude Code hooks, or `.omc` state and need
  a Codex-specific rewrite.
- If a same-name Codex/OMX skill already exists locally, keep the Codex version
  unless you intentionally port the Claude Code version.
- Quarantine removed or incompatible skills instead of deleting them outright;
  a directory such as `~/.codex/skills.quarantine.<date>/` keeps rollback cheap.
- Prefer one canonical entrypoint for overlapping skills. For example, the
  broad `first-principles` skill supersedes `first-principles-fix`, and a single
  `ask` wrapper should supersede separate `ask-claude` / `ask-gemini` entries.
- `triple-review` is orchestrator-aware. If Codex is orchestrating, use
  `claude` + `agy`/`gemini` + secondary endpoint. If Claude Code is orchestrating,
  use `codex`/`codex-family` + `agy`/`gemini` + secondary endpoint. Do not include the
  current orchestrator as a reviewer unless the user explicitly asks for
  self-review.
- OMC orchestration skills (`ralph`, `autopilot`, `ultrawork`, etc.) only make
  sense on Codex if their runtime dependencies have been ported to OMX/Codex.

### Gemini CLI (Google)

Same pattern as Codex — reference skills from `~/.gemini/GEMINI.md`.

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

**Caveats:**

- `triple-review` calls `gemini` CLI as one of its three reviewers. Running it _inside_ Gemini CLI is self-referential; either swap that reviewer for another secondary endpoint, or skip the skill on Gemini.
- No auto-trigger via keyword hook.

### opencode (sst/opencode)

opencode reads `AGENTS.md` from project root and `~/.config/opencode/AGENTS.md` for global rules.

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

**Caveats:**

- opencode supports multiple providers. You can swap any `triple-review` reviewer for an opencode session pointed at a different provider, but keep the provider names in the skill prompt aligned with the actual commands.
- opencode's own command/agent system (`.opencode/command/*.md`) is a more native way to expose these as slash commands — see the opencode docs to port the SKILL.md content to a command file if you want first-class integration.

### Antigravity (Google IDE)

**Not recommended.** Antigravity is an agent-first IDE with workspace-scoped agents (YAML), no global plugin marketplace, no CLI hook layer.

If you really want to:

```bash
git clone https://github.com/solitude6060/Yao-skills /tmp/yao-skills
# Then manually paste relevant SKILL.md content into Antigravity workspace prompts
# or .agent.yaml files per workspace.
```

The skills assume a chat-driven CLI agent with shell + git access. Antigravity's IDE/browser-automation paradigm is largely orthogonal — `workflow-routing` and `project-status-review` are the only ones that translate cleanly; the others lose most of their value.

## Update (after upstream changes)

After the upstream repo gets new commits, refresh on each install path:

| Install path | Update command |
|---|---|
| Claude Code (marketplace) | `/plugin marketplace update yao-skills` then `/plugin update yao-skills@yao-skills` |
| Codex CLI | `git -C ~/.codex/yao-skills pull` |
| Gemini CLI | `git -C ~/.gemini/yao-skills pull` |
| opencode | `git -C ~/.config/opencode/yao-skills pull` |
| Per-skill copy (`~/.claude/skills/<name>`) | re-clone + `cp -r` again, or `git -C` if you originally clone'd |
| CLAUDE.md template (already deployed) | `cp templates/CLAUDE.md ~/.claude/CLAUDE.md` (overwrites — merge by hand if you edited locally) |

After a Claude Code marketplace update, restart your CC session (or `--resume`) for the new skill set to load. `AGENTS.md` / `GEMINI.md` references re-read on each new CLI session — no extra step.

## Adapting to your setup

The skills assume:

- A primary Claude Code (Anthropic OAuth) for orchestration when running from Claude Code
- A primary Codex CLI for orchestration when running from Codex
- A secondary Claude Code endpoint (via `CLAUDE_CONFIG_DIR` pointing to a different provider) for reviewer diversity
- A `gemini` CLI authenticated to Google OAuth
- One or two `codex` CLIs (different accounts) for reviewer diversity without quota burn

If you do not have all of these, the skills' Troubleshooting sections describe graceful subsets (e.g. running with two reviewers and noting which bug class becomes invisible).

## License

MIT (see `LICENSE`). Third-party attribution in `NOTICE.md`.
