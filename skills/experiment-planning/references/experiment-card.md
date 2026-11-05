# Experiment card, matrix and tracker

An experiment card is the unit of planning: one question, one intervention, one decision. The matrix lists
every cell the study needs; the tracker shows which cells exist. Keep all three in the project's existing
plan file or result registry; do not create a parallel document system.

## Card template

Write the card so that a reader outside the project understands it on first reading. Every internal label
(a cohort name, a variant code) gets a short explanation where it first appears.

```text
Card:                 <short descriptive name, not a code>
Question:             <the research question it serves, named as in the project's question file>
Purpose:              <what is unknown now, and why the answer matters>
Intervention:         <the one thing that changes between the compared arms>
Nearest simpler control: <the cheapest alternative that could produce the same result; run beside it>
Held constant:        <data version, cohort file, candidate file, model revision, readout, seeds>
Population and target: <derived from the question; domain rules come from the protocol skill>
Inputs:               <data, cohort file with hash, candidate file with hash, model and revision, input format>
Outputs:              <per-unit result files, metrics, cost fields, location>
Evidence stage:       screening | confirmatory
Expected reading:     <direction against a named comparison>; contradicting result: <what would refute the claim>
Failure policy:       <execution failures rerun until they succeed; method failures counted; retry rounds declared>
Cost:                 <measured throughput x units, money, device; "estimate" until measured>
Decision it changes:  <outcome -> next action, for each outcome>
Status:               planned | running | executed | verified | admitted | superseded
```

Generic example of an expected reading: "the combined method ranks above the frozen model alone on the
validation users; if it does not, the auxiliary signal is dropped from the method". It names a direction
and a comparison, not a numeric bar such as "at least 0.02 better".

## Rules and the failures they prevent

| Rule | Failure it prevents |
|---|---|
| Every card names the question it serves; a card with no question or no decision is dropped or merged. | Experiments that answer nothing, collected before a claim exists. |
| Inputs and outputs are explicit, including the method's readout and the files written. | Results nobody can interpret or reproduce later. |
| The expected reading is a direction against a named comparison, written before the run. | Gates argued after the result is known. |
| The retry policy for method failures (rounds, unchanged parser) is part of the card, and the pre-retry scores are kept. | Retries chosen after seeing scores. |
| Status uses one fixed vocabulary across cards, tracker and status reports. | A "done" cell that was never verified or admitted. |

## Matrix and tracker

The matrix is written once, when the protocol is settled, as the product method × dataset × condition ×
cohort (add candidate-set size or another axis when the study varies it). Columns of the tracker:

| Column | Content |
|---|---|
| Method | Name and variant, with the variant explained once |
| Dataset, condition, cohort | The cell's coordinates |
| Evidence stage | Screening or confirmatory |
| Status | planned, running, executed, verified, admitted, superseded |
| Run identity | Run identifier or result-file path |
| Cost | Measured time, memory, money |
| Card | The card the cell belongs to |
| Note | Why a cell is skipped, with who decided |

Add a coverage view: methods as rows, conditions as columns, each cell done, pending or skipped with a
reason. It shows at a glance which method ran a larger condition without the smaller one, or which model
size is missing from a comparison. Check the coverage view before any comparison is written.

## Ladder

Expand only after the previous rung produced a usable signal:

| Axis | Ladder |
|---|---|
| Users | A small development cohort, then the reporting cohort, then larger samples that contain the earlier ones |
| Candidates | Small candidate sets, then larger ones, then the full catalogue where the protocol needs it |
| Models | A complete prototype with one or two models, then size or training variants, then closed models |
| Datasets | The development dataset, then pre-committed additional datasets |

Keep the breadth of the comparison and the depth of mechanism analysis on separate budgets: compare broadly,
analyse deeply only the models whose results are informative.

## Generic cases

- A batch reported results at the larger candidate size for some methods only; the comparison could not be
  read until the tracker listed which method skipped which size.
- A larger model's runs were found missing late because no coverage view existed.
- Experiment pages listed results without purpose, inputs or outputs; a reader outside the project could
  not tell what each result answered.
