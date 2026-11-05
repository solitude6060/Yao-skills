# Finding triage

A finding from a reviewer, an external review, a verifier or an agent is a claim about the source. Its
severity label is not evidence. Verify it against the exact checkout, data or document before acting.

## Triage table

| Id | Finding (short) | Reported by | Claimed location | Verified evidence (`file:line`, command and output) | Status | Disposition | Rationale |
|---|---|---|---|---|---|---|---|

Status values:

| Status | Meaning |
|---|---|
| Exists | The defect is present as described |
| Partly | Present, but narrower, different in cause, or with a different impact |
| Absent | Not present; the evidence shows why |

Disposition values: fix now, fix with a narrower claim, deferred with an owner and a recorded follow-up,
rejected with evidence. A HIGH protocol finding is not deferred by moving text; it is answered by an
experiment (a matched-information control). Narrowing the claim is allowed only in addition to that
experiment, with the owner's approval.

## Verification rules

- Read the cited `file:line` in the exact revision under review, not a later checkout.
- A claim that something is missing ("no statement on X", "no test for Y") needs a full-text search of the
  whole document or repository. Generic case: a compliance check searched only the appendix and reported a
  missing statement that was in the main text.
- A finding that rests on a source's default setting needs the actual setting of the run. Generic case: a
  review inferred a training length from a source default; the checkpoint record showed a different
  value and the finding was withdrawn.
- A comparison that changes the whole system does not isolate one component; a finding that attributes an
  effect to one component needs a control that changes only that component.
- Agent-reported facts about sources (what the original authors used, what another paper reports) are
  rechecked at the source before they enter a plan or a paper.
- Text and table tests: introduce a deliberate error into a copy of the document (change a number, delete
  a sentence) and confirm that the tests fail. Generic case: three assertions compared values with
  themselves and passed on any input; a mutation run exposed them.

## Interrupted and empty reviews

An interrupted review (quota, timeout, crash), an empty output, or an exit code without a substantive
review is not an approval, even when it produced some useful findings. Record it, triage the partial
findings, and complete the review on the exact revision. An approval binds to the content it reviewed.

## Fix log

```markdown
# Fix log: <work item or review>

| Finding id | Status | Reproduction | Fix | Test or check added | Files touched | Re-verified by |
|---|---|---|---|---|---|---|
```

Cross-link the triage table, the fix log and any follow-up items from the project's status
records.
