---
name: research-lifecycle
description: "Use when starting, resuming, handing over or closing a research project or milestone: research questions, verbatim instruction and decision logs, stage hand-offs, milestone gates, compute and budget, preservation, and new-topic start documents."
argument-hint: "<start | resume | milestone | status | handover | new-topic> <project path | empty>"
---

# Research Lifecycle: stages, records, hand-offs

Projects lose more time to drift than to single wrong numbers: an experiment that answers no question, an
instruction lost between sessions, a closed option proposed again. This skill keeps the project spine
(questions, records, decisions) and routes each stage to its skill.

Chinese: [SKILL.zh.md](SKILL.zh.md). References: [stage-map.md](references/stage-map.md), [owner-communication.md](references/owner-communication.md),
[compute-and-budget.md](references/compute-and-budget.md) (accelerators, paid APIs, storage, preservation),
[handover-template.md](references/handover-template.md) (session handover, new-topic start document).

## When to use

- Opening a project or follow-up topic; resuming after a break or context reset.
- A milestone: a decision made, a result admitted, a gate passed or failed, a review completed.
- Progress questions, blockers, hand-offs to another session, agent or person.

Not for: model choice (`workflow-routing`), merge review (`triple-review`), worktrees
(`worktree-hygiene`), session compaction (`context-hygiene`), experiment design (`experiment-planning`),
result admission (`experiment-contract`), writing (`paper-writing`).

## Stage map

| Stage | Skill | Entry artifact | Exit artifact |
|---|---|---|---|
| Lifecycle | this skill | owner request, north-star file | question file, records, next decision |
| Survey | [research-survey](../research-survey/SKILL.md) | a decision that needs sources | verified source records |
| Ideation | [research-ideation](../research-ideation/SKILL.md) | question file, source records | question chain, feasibility record, preliminary-study plan |
| Planning | [experiment-planning](../experiment-planning/SKILL.md) | approved direction | experiment cards, matrix, tracker, budget |
| Confirmation | [experiment-contract](../experiment-contract/SKILL.md) | approved card | preflight record; admitted or superseded rows |
| Verification | [research-verification](../research-verification/SKILL.md) | admitted rows, diffs, claims | verification record, triage table |
| Writing | [paper-argument](../paper-argument/SKILL.md), [paper-writing](../paper-writing/SKILL.md) | verified results | argument map, manuscript, submission package |

A failed check returns only the affected work to the earlier stage. Between planning and preflight,
implementation follows the project's test-first and source-fidelity rules; new analyses produced for the
argument pass `experiment-contract` admission before they enter the paper.

## Project spine

1. North-star file: the specification or goal statement. Read it before any plan or claim decision.
2. Research-question file: the current questions in one file, read at every milestone. Every plan item,
   experiment card and paper section names the question it serves.
3. Status, tracker and handover files: each owner instruction verbatim with its handling, written as it
   arrives, not only at milestones. Clock times come from `date`.
4. Decision log: each decision dated, with its scope (project, phase, document) and what it supersedes.
   Search it before asking or proposing; never reintroduce a closed option. A restriction stated for one
   phase keeps that scope and does not become a permanent rule.

## Owner communication

- Answer the owner's questions first, then the status, then tool work.
- Each question is self-contained: context, options with consequences, a recommendation, the exact answer needed.
- Present a multi-part decision one item at a time and record each answer before the next.
- A bare acknowledgement approves only the items the owner named, plus necessary fixes and verification.
- Never write an internal code without its plain name and a one-line explanation.
- Check the chat language and term glosses before sending, including short notes between tool calls.
- When the owner takes over a document, stop editing it and send proposals.

## Milestones

Close each milestone with the PR and review gate (`triple-review` where required) and a verifier run
(`research-verification`). Publish the result table, the paper and any project pages together from the
newest commit, naming it; deliver every build (each language edition, if the paper is bilingual) to one
fixed location.

## Progress and blockers

- Report progress from real output and process state (pid file, the log's last line, output counts, device
  use); a launch command shows intent only.
- Status view: each result carries one evidence state (planned, running, executed, verified, admitted,
  superseded); the report ends with the next decision and who makes it.
- Classify each blocker as authorization, technical prerequisite, resource, or optional preparation. Block
  only the work that depends on it; continue independent authorized work.
- Evidence before platform: the next milestone is the smallest result that can change a continue, adjust or
  stop decision. Defer infrastructure and breadth that cannot change it.
- Compute is scheduled and budgeted (compute reference): no idle accelerator; an estimate, a ledger and a
  pinned model version before paid calls.

## Red flags

| Observation | Action |
|---|---|
| A question the decision log already settled | Cite the entry; do not ask again |
| A published page or PDF older than changes the owner saw | Republish from the newest commit; name it |
| An accelerator idle overnight while work is queued | Find the stall cause and fix it |
| Owner-approved text changed back by a later edit | Restore it from the versioned copy |
| "Blocked by the owner" covering independent work | Reclassify the blocker; continue the rest |

## Output

Updated question file, decision log and status, tracker and handover files; a milestone record naming the
commit, review and verifier report; for a new topic, the start document. Report to the owner in the
project's chat language.
