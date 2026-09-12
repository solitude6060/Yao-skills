---
name: context-hygiene
description: Use when session context exceeds about 100k tokens, before switching to an unrelated task, before starting a long-running loop, when usage cost spikes, or when the user says "compact", "clear", "handover", "session太長" or "usage太貴".
---

# Context Hygiene

Context grows every turn. The cost model below is illustrative: replace its
weights with the provider's current pricing and cache behavior before using it
for a budget or routing decision. It is not a universal price sheet or a
measurement of any provider. Assume cached input costs 0.1 units per token,
new input costs 1 unit per token, output costs 5 units per token, and each turn
adds 1k new input plus 3k output. Total = cached tokens × 0.1 + 1k + 3k × 5.

| Context | Illustrative cached-input units | Illustrative output units (3k) | Illustrative per-turn units |
|---|---|---|---|
| 30k | 3k | 15k | ~19k |
| 90k | 9k | 15k | ~25k |
| 180k | 18k | 15k | ~34k |

Cache lifetime and re-caching behavior are provider-specific; verify them
before relying on a pause or cache hit.

## Decide

| Situation | Action |
|---|---|
| < 80k | Continue |
| 80–150k, same task, mid-flow | `/compact` with a focus prompt |
| Task boundary or > 150k | Handover file, then `/clear` |
| Starting a loop (ralph, autopilot, `/loop`) | Fresh session; never inherit |
| Loop needs a checkpoint or reaches its explicit stop condition | Checkpoint to disk; stop or restart only when authorized |
| Inside a red → green pair | Wait; do not split the failing test from its fix |

## /compact

Always give a focus prompt; without one the model drops the wrong things.

```
/compact focus on the current plan, files touched, code paths under change, and open TODOs. drop full file contents, exploratory tool outputs, and resolved sub-questions.
```

Compaction size is provider- and model-specific. Inspect the resulting context;
do not assume a fixed reduction ratio.

## Handover, then /clear

Write the handover to disk before clearing; the conversation is what you are
about to lose. Locations, in order of preference: the project's `handover.md`
(project memory); `docs/HANDOVER_<branch>.md` for branch-specific work;
`.omc/notepad.md` when the OMC runtime manages scratch state. The new session
reads that file first.

```markdown
# HANDOVER — <date> — <branch / topic>
## Goal
<one sentence>
## Status
- [x] Done: ...
- [~] In progress: <what> — <file:line>
- [ ] Next: ...
## Key files / functions
- `path:line` — why it matters
## Open questions / decisions pending
- <question> — <current leaning>
## Watch out for
- <gotcha / prior failure / spec constraint>
## Last commit
<sha subject>
## How to resume
1. Read this doc
2. <next concrete action>
```

## Loops and subagents

- Checkpoint every N iterations to a persistent path; resume from disk, not memory.
- Route inner work using the model-routing policy configured by the project in
  `AGENTS.md` or `CLAUDE.md`; use `docs/MODEL_ROUTING.md` by default when it
  exists. `workflow-routing` picks the shape. No second model table lives here.
- A subagent summary consumes output units under the active provider's pricing;
  its own run is billed separately. Do not spawn one for what fits in two or
  three inline calls; batch related questions.

## Mistakes

| Mistake | Effect |
|---|---|
| Compacting below 80k | Wastes the compact, loses nuance |
| Compacting without focus | Important context dropped |
| Clearing without a handover on disk | In-progress state lost |
| Loop inherits a 100k conversation | Pays for irrelevant context every turn |
| "The cache will save me" | Re-read the table above |
