# Preliminary-study plan template

A preliminary study produces the smallest result that can decide continue, adjust or stop for a direction.
It is not the full experiment matrix; that is built in `experiment-planning` after the gate passes.

## Sections

| Section | Content |
|---|---|
| 0. Relation to earlier documents | Table: document, topic, relation (inherited, superseded, background only) |
| 1. Questions | Table: identifier with a plain name, question, research question it serves, what it decides |
| 2. Shared rules | Information boundary; selection on validation data only; execution versus method failures; per-request hashes; evidence stage and seeds; official sources for baselines; output location |
| 3. Data and cohorts | Datasets, cohorts and their exposure history, candidate construction, what is reused without new model calls |
| 4. Stages | Table: stage, content, completion condition, device or service |
| 5. Continue or stop conditions | Table: point, condition, what happens if it is not met |
| 6. Schedule | Real dates, known conflicts (other deadlines, rebuttal windows, resource availability) |
| 7. Tests written first | Boundary, candidate, request and identity tests that must pass before stage 1 |
| 8. Outputs and records | One folder per stage with a README, code, metrics file and raw responses; records in status, tracker and handover |
| 9. Decided and pending | Owner decisions verbatim and dated; open decisions as self-contained questions |
| 10. References | Grouped by role: closest work, concurrent work, methods used, protocol sources |

## Writing the continue or stop conditions

- Each condition is a comparison against a named baseline or control, read on validation data, stated in
  plain words: "the guided model ranks the validation targets higher than late fusion of the same signals on
  both datasets".
- No arbitrary numeric bar. A margin appears only when the claim is equivalence, and it is declared before
  the run.
- Test targets are reported once, after the settings are frozen; they never decide a gate.
- A pre-declared adjustment, if any, is written with the condition ("one change of the loss or step count,
  then stop if it still fails"). Nothing else changes after the result is seen.
- A stage that is screening (one run, point estimates or paired differences) can choose the next step; it
  cannot support a robustness or superiority claim.

## Example rows

| Point | Condition | If not met |
|---|---|---|
| After stage A | The adjusted output beats the unadjusted output of the same model on validation targets, on both datasets | Keep stage A as an analysis only |
| After stage B1 | The new model class reaches the accuracy of the strong baseline it starts from, on validation targets | One pre-declared adjustment, then stop direction B |
| After stage B2 | Guidance beats late fusion and feature injection of the same signals on validation targets | Record "guidance did not beat late fusion on validation targets at this stage"; stop direction B |
| Decision date | The owner chooses a direction and a venue from the results above | Next venue in the fallback list, or stop |

Generic case: a preliminary gate passed on one dataset and failed on the other; by the pre-declared rule the
component stayed as an analysis, and the plan moved on without rewording the gate.
