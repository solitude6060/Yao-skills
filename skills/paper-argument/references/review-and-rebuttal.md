# Pre-submission review and rebuttal reserve

A reviewer-style review before submission finds the objections while there is still time to answer them with
analyses. A rebuttal reserve keeps those analyses ready. Third-party skills such as `pre-submission-reviewer`
and `rebuttal-guidance` can run the review and shape the replies if they are installed; this file covers
timing, triage and the reserve, and stays complete without them.

## Timing

- Run the first full review early enough that a missing experiment can still be run: before the abstract
  deadline when the venue has one, and again on the final build.
- The reviewer works in a fresh context, reads only the paper (and the call), and returns a verdict, the major
  concerns and the minor ones. A review that was interrupted or returned empty is not a result; run it again.
- Freeze the reviewed build by its commit, so every finding points to a page and line that still exists.

## Triage of each finding

Verify every finding against the source before acting; reviews can be wrong.

| Finding | Exists, partly or absent | Evidence (file, line, table cell) | Action | Author decision needed |
|---|---|---|---|---|
| <finding> | exists | <pointer> | experiment, text change, or scope narrowed | yes or no |

- A finding about the protocol (an information asymmetry, a selection on the reporting users) is answered by
  an experiment where one can be run; moving text is not an answer (`experiment-planning`).
- A finding of absence ("the paper lacks an AI-use statement") is confirmed by a full-text search first.
- A finding that a citation does not support its claim goes through the citation ladder of `research-survey`.
- Record each verdict and fix in the project's fix log; re-review the remediation, not the whole paper again.

## Rebuttal reserve

Prepare analyses that answer the likely questions before the reviews arrive, within a time budget fixed in
advance (for example, only analyses that finish within the time the rebuttal period leaves for computing).

| Likely question | Analysis that answers it | Cost | Status | Where the result is kept |
|---|---|---|---|---|
| <question> | <analysis> | <measured or estimated> | planned, done, admitted | <file> |

- Draw the likely questions from the pre-submission review, from the closest prior and concurrent work, and
  from the protocol choices a reviewer could contest.
- Results in the reserve pass the same admission checks as any other result before they appear in a reply.
- Draft replies only against the actual reviewer comments; the reserve supplies evidence, not text written
  for objections nobody raised.

## Concurrent preprints

When a concurrent preprint appears, compare it before submission and again before the rebuttal in the
comparison table of `research-survey`
([../../research-survey/references/concurrent-work.md](../../research-survey/references/concurrent-work.md)).
For the rebuttal, add two columns to its row: the reviewer questions the preprint creates ("how does this
differ from ...?") and the reserve analysis that answers each; add those analyses to the reserve. Cite the
preprint as related work or contrast; it does not redefine the paper's
question. The concurrent-work watch itself is part of `research-survey`
([../../research-survey/SKILL.md](../../research-survey/SKILL.md)).

## Generic cases

- A pre-submission review returned "reject in the form reviewed": the draft exceeded the page limit, an
  information asymmetry against the baselines was the central objection, an interval was overclaimed, a
  disclosure had been deleted in a rewrite, and some citations credited sources with content they lack.
  Each item was verified against the source before any fix.
- Two concurrent preprints appeared after submission; a comparison table and a short list of reserve
  analyses were prepared, and the analyses within the time budget were run before the reviews arrived.
