---
name: correct
description: Use when the user explicitly invokes correct, or keeps correcting agents for the same mistake in a repository — mine past corrections into mistake classes and make each one fail automatically, preferring architecture, types, lint and tests over prose rules.
disable-model-invocation: true
license: MIT
---

# Correct

Adapted from pstack `correct` by Lauren Tan (MIT, `cursor/plugins` at `1ba91fc`; see
`LICENSE`). The user keeps correcting agents in this repository for the same mistakes.
Change the repository so the next agent cannot make them.

Assume every contributor is an agent that sees only the files it opened, copies the nearest
example, and takes the shortest path that passes. Design the repository so a change that
looks right from one file is right for the whole repository.

## Find the mistake classes

Read, for this repository only:

- recent commits, reverts and fix commits;
- review documents, fix logs and triage tables;
- agent instruction files (`AGENTS.md`, `CLAUDE.md`) and project memory;
- agent transcripts for this workspace (for Claude Code,
  `~/.claude/projects/<workspace-slug>/*.jsonl`), searching for user corrections;
- comments that explain a workaround.

Group the mistakes into classes. A class counts once it has happened at least twice. Record
each occurrence with its commit, file or transcript line.

## Fix each class at the highest level that works

1. **Architecture.** Give each piece of state one owner and each task one supported way.
   Hide internals so the wrong import fails. Replace hand-synced lists with one source of
   truth. Delete old ways and dead code an agent would copy.
2. **Types and checks.** Make the bad state impossible to write. If bad code still runs, add
   a lint, validator or CI check whose error names the file, type or function to use
   instead. If the pattern is already common, fail only when a change adds more.
3. **Behavior tests.** Fix or delete any test that still passes when its behavior breaks, or
   fails when only internals change.
4. **Documentation or agent rules last**, only for judgment calls. Nothing fails when an
   agent skips them.

For a research repository, typical classes are leakage across splits, metric or candidate
definitions that drift between scripts, results written to temporary locations, and numbers
reported without provenance; prefer a validator or test that fails on the real past case.

## Fix and prove

- Work on a branch and follow the project's test-first and pull-request rules.
- Fix the most frequent classes first, one commit per class.
- Prove each new check fails on a real past mistake: check out or reconstruct the bad
  revision, run the check, and keep the failing output.
- Run the same command locally and in CI.
- Exceptions go on the offending line with a reason, an expiry date and the user's
  approval.

## Keep the rule table

Keep a table in the agent instruction file pairing each rule with what enforces it:

| Rule | Enforced by | Past mistake |
| --- | --- | --- |

When the user corrects an agent again, fix the mistake and add the rule. If the rule was
already there and nothing enforces it, treat it as a repeat and move it to a higher level in
the same change. Drop a rule once its mistake can no longer happen.

## Reply

Each class with its evidence, the level chosen and why a higher level did not work, the
failing-then-passing output, and any class left open for the user to decide.
