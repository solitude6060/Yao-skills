# Handover and new-topic start documents

Two documents carry a project across a boundary: the session handover (same project, next session) and the
new-topic start document (a follow-up study in a new repository or session). Both live in persistent project
files; a conversation summary is not a handover.

## Session handover

Use the generic template in `context-hygiene` and add these research fields:

| Field | Content |
|---|---|
| Running jobs | Command, pid file, log path, the end line that marks completion, expected finish from measured throughput |
| Evidence states | Each open result: planned, running, executed, verified, admitted or superseded |
| Pending owner decisions | Plain name, options, recommendation, what waits on it |
| Last admitted state | Result-table commit, report commit, published page commit |
| Resume steps | The first command, then the next concrete action |
| Known traps | Running scripts that must not be edited, live inputs, shell quirks, resource restrictions in force |

## New-topic start document

A follow-up topic starts from one document. A new session reads it first and should be able to start work
without re-deriving any decision.

| Section | Content |
|---|---|
| 0. Relation to earlier documents | Table: document, topic, relation (inherited, superseded, background only) |
| 1. Read order | Table: order, document and sections, purpose |
| 2. Location | Repository and experiment-output locations, resolved with `realpath` and outside temporary storage |
| 3. First commands | `date`; reproduce the inherited numbers the topic builds on and diff against the saved output; resource status queries only; credential presence tests that never print a value |
| 4. Inherited rules and differences | What is kept from the previous protocol, what changes and why. Re-examine each inherited restriction: it binds the new topic only if the new question needs it |
| 5. Inherited assets | Data, cohorts with their exposure history, checkpoints with identities, code at a pinned commit |
| 6. Decided items | Owner decisions, verbatim and dated: venue order, resource limits, locations, evidence stage, data allowed in external requests |
| 7. Questions to ask first | Self-contained questions with a recommendation (see owner-communication.md) |
| 8. First work items | Records to create, tests written first, stage 0 reproduction, the first preliminary stage |
| 9. Opening prompt | Paste-ready text for the new session (template below) |

### Opening prompt template

```text
This is the first session of <project>. Topic: <one sentence that names the method by what it does>.

1. Read first, in order: <start document, sections 0 to 8>; <inherited rules file>; <feasibility record>.
2. Already decided by the owner (dated): <venue order>; <resource limits>; <locations>; <seeds and evidence
   stage>; <data allowed in external requests>.
3. Ask the owner first (self-contained, with a recommendation): <open decisions>.
4. First work: <create the records>; <tests written first>; <stage 0 reproduction>; <first preliminary stage>.
5. Rules: <continue or stop conditions read validation data only>; <information boundary>; <execution versus
   method failures>; <cost fields>; <verifier cadence>; <owner instructions recorded verbatim, times from
   date>; <artifacts of the previous project stay frozen>; <no personal data in external requests>; <chat
   language and writing rules>.
```

Generic cases: a draft protocol for a follow-up treated model training as an exception because the earlier
study was training-free, although the new question required training; the owner asked why another draft
protocol differed from the earlier study, and it was rewritten as the earlier protocol plus a list of
differences.

## Archive completeness when the paper scope narrows

Removing a dataset, baseline or analysis from the paper keeps its rows in the result table, its records,
its pages and its raw artifacts. Move the paper-only files to the project's archive folder and record why;
the experiment archive stays complete and reproducible.

Generic case: an incomplete baseline was removed from the manuscript while its rows and artifacts stayed in
the result table and the experiment log.
