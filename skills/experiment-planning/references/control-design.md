# Control design

A control answers "what else could have produced this result?". Plan controls for the information each arm
reads as well as for its architecture, and decide them before the first result.

## Nearest simpler alternative

For every proposed mechanism, name the cheapest alternative that could produce the same result and run it
beside the method. Examples of the pattern: a learned combination against a fixed weighted sum; guidance
inside a model against late fusion of two scores; a new input against the same input with the field that
carries the claimed signal removed. A mechanism claim stands only where it beats its simpler alternative.

## Information controls

| Control | What it shows | When it is required |
|---|---|---|
| Model only | What the model contributes without the auxiliary signal | The method combines a model with another signal |
| Signal only | What the auxiliary signal achieves alone | Same |
| Matched information | Whether the gain survives when the comparison receives the same evidence | The method reads information the baseline does not (timestamps, cross-user statistics, item text) |
| Clean input | The increment from the user's own evidence, with every cross-user or future field removed | An input mixes information sources |

Write the access rule for every auxiliary signal in the protocol, in operational terms: which statistics may
be computed, from which events, up to which time, and which outputs of other fitted models are excluded.
The rule decides whether a variant is the same method or a cascade that needs its own decision record.

## System versus component attribution

| Claim | Evidence it needs |
|---|---|
| The method beats a baseline (system) | The main comparison on identical users, candidates and inputs |
| A component causes part of the gain (component) | A removal or replacement of that component with everything else fixed, plus the information controls above |
| A component carries a specific signal | An input intervention that removes, swaps or permutes that signal |

A result for the whole method is never attributed to one component without the second row.

## Fixed-parameter versus reselected ablations

| Ablation | Procedure | Question it answers |
|---|---|---|
| Fixed parameters | Remove the component; keep every other selected setting | What does the component add inside the selected method? |
| Reselected | Remove the component; select the remaining settings again on validation data | Can the rest of the method compensate for its absence? |

Report the type beside every ablation row. A variant selected under a different objective or on different
data is an analysis variant, not a replacement for the main configuration.

## Protocol findings are answered by experiments

When an internal audit rates a protocol asymmetry as high severity (for example, the method reads
request-time statistics that trained baselines never see), plan the experiment that answers it before the
claims freeze: a matched-information control, a sensitivity run that removes the asymmetry on both sides,
or a time-split selection check. Moving the finding to a limitation paragraph does not answer it.

Generic case: an audit flagged that the method's statistics used the request time while the trained
baselines did not. The finding was deprioritized; an external pre-submission review made it the central
objection, and the answering runs were done under deadline pressure.

## Competing explanations

For each planned claim, list the explanations a reviewer would offer and the control that rules out each:

| Claim | Competing explanation | Control |
|---|---|---|
| <claim> | More information, not a better model | Matched-information control |
| <claim> | The baseline is untuned or not the official configuration | Official configuration plus a labelled relaxed variant |
| <claim> | Selection on the reporting users | Fresh reporting cohort; exposure scan |
| <claim> | A shortcut through identifiers or the candidate sampler | Identifier-free inputs; sampler audit (`research-verification`) |
