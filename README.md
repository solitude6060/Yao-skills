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

`ralph`, `plan`, `deep-interview`, `deep-dive`, `learner`, `skillify`, `sciomc`, `autoresearch`, `ralplan`, `ai-slop-cleaner`, `team`, `release`.

## Install

### Per-skill (user-level)

Copy the directory of any skill into `~/.claude/skills/`:

```bash
git clone https://github.com/solitude6060/Yao-skills /tmp/yao-skills
cp -r /tmp/yao-skills/skills/triple-review ~/.claude/skills/
cp -r /tmp/yao-skills/skills/first-principles-fix ~/.claude/skills/
# ...etc
```

Open a new Claude Code session — the skill becomes invocable via `Skill` tool / `/<skill-name>`.

### `CLAUDE.md` template

```bash
cp templates/CLAUDE.md ~/.claude/CLAUDE.md   # only if you don't already have one
```

Then edit to your needs.

## Adapting to your setup

The skills assume:

- A primary Claude Code (Anthropic OAuth) for orchestration
- A secondary Claude Code endpoint (e.g. MiniMax via `CLAUDE_CONFIG_DIR`) for reviewer diversity
- A `gemini` CLI authenticated to Google OAuth
- One or two `codex` CLIs (different accounts) for reviewer diversity without quota burn

If you do not have all of these, the skills' Troubleshooting sections describe graceful subsets (e.g. running with two reviewers and noting which bug class becomes invisible).

## License

MIT (see `LICENSE`). Third-party attribution in `NOTICE.md`.
