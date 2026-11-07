# Stage map and hand-offs

The order below runs once per study and again, in part, at each milestone. A stage starts from its entry
artifact and ends when its exit artifact exists in the project's files. Chat is not an artifact: a result,
decision or plan that exists only in a conversation has not been handed off.

## Hand-off order

| Step | Stage | Skill | Entry artifact | Exit artifact |
|---|---|---|---|---|
| 1 | Open or resume | `research-lifecycle` | owner request; north-star file | research-question file; status, tracker, handover; decision log |
| 2 | Survey | `research-survey` | a decision that needs sources | verified source records; practice checks; concurrent-work table |
| 3 | Ideation | `research-ideation` | question file; source records | question chain; feasibility record on the real data; scope; preliminary-study plan with continue or stop conditions |
| 4 | Planning | `experiment-planning` | approved direction or preliminary-study plan | experiment cards; full matrix and tracker; cohorts; information-parity decisions; budget |
| 5 | Contract preflight | `experiment-contract` | approved card and specification | preflight record: pinned identities, smoke run on real data, rerun map |
| 6 | Execution | `experiment-contract` (execution mode) | preflight record | raw outputs, logs, cost fields, failure records |
| 7 | Contract admission | `experiment-contract` | raw outputs | rows admitted, labelled or superseded; result table and records synchronized |
| 8 | Verification | `research-verification` | admitted rows; diffs; claims | verification record; triage table; fix log |
| 9 | Argument | `paper-argument` | verified results | argument map; mechanism analyses with pre-declared readings |
| 10 | Writing | `paper-writing`; compare each section with strong papers at the target venue | argument map; admitted tables | manuscript, tables, figures |
| 11 | Paper checks | `research-survey` (citation check); `research-verification` (on the paper) | manuscript | citation records; number and claim verification |
| 12 | Review and rebuttal | `paper-argument` (review and rebuttal); `paper-writing` (submission package) | manuscript; reviews | triaged findings; rebuttal reserve; submission package |
| 13 | Decide | `research-lifecycle` | outputs of steps 1 to 12 | continue, adjust, stop or hand off; handover or new-topic start document |

Implementation sits between steps 4 and 5. It follows the project's test-first and source-fidelity rules
(official source first, pinned revision, recorded differences); its exit artifact is tested code and the
source record that preflight pins. New analyses produced at step 9 for the argument are results: they pass
contract admission (step 7) before they enter the paper.

Supporting skills at every step: `explain-the-number` before a number is reported or acted on;
`first-principles` when an inherited assumption is load-bearing; `recsys-evaluation` at steps 4, 5, 7 and 8
when the study evaluates recommenders; `triple-review` to close a milestone where the project requires it;
`workflow-routing` when work is delegated.

## Return paths

A failed check sends only the affected work back. The rest of the study continues.

| Failure found at | Returns to | Generic case |
|---|---|---|
| Preflight: identity mismatch or failed smoke run | Implementation of that card | A set-wise request ran out of memory at the largest candidate count; only that configuration was rebuilt |
| Admission: unresolved execution failures, missing cost fields | Execution of the affected units | A batch with server errors on some users was rerun for those users only |
| Verification: a number disagrees with the raw files | Admission of the affected rows | A paper table cited the best of several rows; the admitted row replaced it |
| Verification: a protocol finding of high severity | Planning: a control experiment answers it | An information asymmetry between the method and the baselines was answered by a run that removed it on both sides |
| Paper checks: a cited claim is absent from its source | Survey citation check for that sentence | A reference credited a source with content it does not contain |
| A preliminary gate fails | Ideation: adjust or stop | The premise of a topic failed on the real data; the topic was stopped |

## Optional third-party companions

Use these when they are installed. Each skill in this cluster stays complete without them; their text is
not copied here.

| Companion (if installed) | Stage | Use it for | This cluster still owns |
|---|---|---|---|
| `deep-research` | Survey | a long narrative literature report | framing its questions and verifying its citations (`research-survey`) |
| `idea-evaluator` | Ideation | scoring an idea that already exists | feasibility on the real data, scope, inherit-and-diff (`research-ideation`) |
| `tech-paper-template`, `benchmark-paper-template` | Ideation, argument | a paper skeleton | the question chain and the mechanism evidence (`paper-argument`) |
| `paper-writer`, `intro-drafter` | Writing | drafting prose from verified material | the owner's writing rules and claim checks (`paper-writing`) |
| `paper-polish` | Writing | meaning-preserving language passes | re-verifying numbers and claims after each pass |
| `figure-designer` | Writing | figure layout | figure and text agreement in each language edition |
| `pre-submission-reviewer`, `academic-paper-review` | Review | reviewer-style audits | verifying each finding against the source (`research-verification`) |
| `rebuttal-guidance` | Rebuttal | responses to actual reviewer comments | the rebuttal reserve prepared before reviews arrive |
