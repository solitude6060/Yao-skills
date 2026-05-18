# yao-skills

A small, opinionated set of Claude Code skills for code review, incident triage, workflow routing, and project health checks — plus a curated subset of [oh-my-claudecode](https://github.com/Yeachan-Heo/oh-my-claudecode) skills for planning and orchestration.

This is the **public, sanitized** version of a private personal toolkit. Examples that referenced specific projects / PRs / business details have been replaced with generic placeholders so the methodology is preserved without leaking internal context.

## Skills

### Author-original

| Skill | What it does |
|---|---|
| `triple-review` | Three-reviewer PR review (Gemini + Claude Code on a secondary endpoint + Codex CLI), severity triage, TDD fix cycle, auto-merge gate |
| `first-principles-fix` | Incident triage discipline: 5-question audit, ground-truth verification, mandatory dual/triple review on hotfixes |
| `workflow-routing` | Pick A/B/C/D/Mini workflow per task type, risk level, and current Opus / Codex quota |
| `project-status-review` | Generate a comprehensive project status report — code stats, branch divergence, blockers, prioritized next steps |

### Curated from oh-my-claudecode (MIT, see `NOTICE.md`)

`ralph`, `plan`, `deep-interview`, `deep-dive`, `learner`, `skillify`, `sciomc`, `autoresearch`, `ralplan`, `ai-slop-cleaner`, `team`, `release`, `autopilot`, `ultrawork`.

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

Open a new Claude Code session and all 18 skills become invocable via the `Skill` tool / `/yao-skills:<skill-name>`.

**B. Per-skill copy (if you only want some)**

```bash
git clone https://github.com/solitude6060/Yao-skills /tmp/yao-skills
cp -r /tmp/yao-skills/skills/triple-review ~/.claude/skills/
cp -r /tmp/yao-skills/skills/first-principles-fix ~/.claude/skills/
# ...etc
```

Skill becomes invocable via the `Skill` tool / `/<skill-name>`.

### `CLAUDE.md` template

```bash
cp templates/CLAUDE.md ~/.claude/CLAUDE.md   # only if you don't already have one
```

Then edit to your needs.

### Codex CLI (OpenAI)

Codex has no plugin marketplace; the equivalent is referencing skills from `~/.codex/AGENTS.md`.

```bash
mkdir -p ~/.codex
git clone https://github.com/solitude6060/Yao-skills ~/.codex/yao-skills

cat >> ~/.codex/AGENTS.md <<'EOF'

## Available skill references

When the user's request matches a skill below, read the corresponding SKILL.md and follow it:

- "triple review" / "PR review" → ~/.codex/yao-skills/skills/triple-review/SKILL.md
- "first principles" / "incident triage" → ~/.codex/yao-skills/skills/first-principles-fix/SKILL.md
- "workflow routing" / "which workflow" → ~/.codex/yao-skills/skills/workflow-routing/SKILL.md
- "project status" / "health check" → ~/.codex/yao-skills/skills/project-status-review/SKILL.md
EOF
```

**Caveats:**

- No auto-trigger via keyword hook (Claude Code feature). User must mention the skill name or matching phrase.
- The `triple-review` skill itself calls Codex CLI as one of its reviewers. Running it _inside_ Codex creates self-reference; usable but unusual.
- OMC orchestration skills (`ralph`, `autopilot`, `ultrawork`, etc.) rely on Claude Code hooks and background tasks; porting to Codex has limited value.

### Gemini CLI (Google)

Same pattern as Codex — reference skills from `~/.gemini/GEMINI.md`.

```bash
mkdir -p ~/.gemini
git clone https://github.com/solitude6060/Yao-skills ~/.gemini/yao-skills

cat >> ~/.gemini/GEMINI.md <<'EOF'

## Skill references

If the user's request matches these keywords, read the SKILL.md before responding:

- "triple review" → ~/.gemini/yao-skills/skills/triple-review/SKILL.md
- "first principles" → ~/.gemini/yao-skills/skills/first-principles-fix/SKILL.md
- "workflow routing" → ~/.gemini/yao-skills/skills/workflow-routing/SKILL.md
- "project status" → ~/.gemini/yao-skills/skills/project-status-review/SKILL.md
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
- "first principles" → ~/.config/opencode/yao-skills/skills/first-principles-fix/SKILL.md
- "workflow routing" → ~/.config/opencode/yao-skills/skills/workflow-routing/SKILL.md
- "project status" → ~/.config/opencode/yao-skills/skills/project-status-review/SKILL.md
EOF
```

**Caveats:**

- opencode supports multiple providers; the `triple-review` reviewer set assumes specific CLIs (`gemini`, secondary CC, `codex`). You can swap any reviewer for an opencode session pointed at a different provider, but the skill prompt mentions provider names you'll want to edit.
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

## Adapting to your setup

The skills assume:

- A primary Claude Code (Anthropic OAuth) for orchestration
- A secondary Claude Code endpoint (e.g. MiniMax via `CLAUDE_CONFIG_DIR`) for reviewer diversity
- A `gemini` CLI authenticated to Google OAuth
- One or two `codex` CLIs (different accounts) for reviewer diversity without quota burn

If you do not have all of these, the skills' Troubleshooting sections describe graceful subsets (e.g. running with two reviewers and noting which bug class becomes invisible).

## License

MIT (see `LICENSE`). Third-party attribution in `NOTICE.md`.
