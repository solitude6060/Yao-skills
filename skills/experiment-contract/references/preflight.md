# Preflight

Run before a batch, a costly rerun, or the first run of a new model, dataset or condition. The goal is
that the run which starts is the run the plan describes, and that it will not fail after hours for a
reason a few units would have shown.

## Contract fields

Write these in the experiment card or plan before launch; the card fields come from
[experiment-planning](../../experiment-planning/references/experiment-card.md) (held constants, failure policy,
evidence stage). A run with a missing field is not ready.

| Field | Content | Failure it prevents |
|---|---|---|
| Question | The research question the run answers, by identifier and in words | A run that answers no question |
| Cohorts | Development, reporting and calibration units; which earlier runs saw each | Selection on the reporting cohort |
| Candidates | Candidate rule, size and hash | Comparisons on different candidate sets |
| Inputs | Fields each method reads, history length, time boundary | One method reading more than its competitor |
| Readouts | Output format, parser, how a score or rank is read | Two models compared through different readouts |
| Evidence stage | Screening (one run, point estimates) or confirmatory (paired-difference uncertainty over the test units, plus several seeds or repeats for methods with training or decoding randomness, or a claim scoped to one training run); seeds per method | A screening run used for a robustness claim; a per-unit bootstrap taken as covering seed variance |
| Selection objective | What is selected on validation data, by which objective | A variant with another objective taken as the main row |
| Retries | Declared retry rounds; parser unchanged between rounds | Retries chosen after seeing scores |
| Cost fields | Wall time, latency, peak memory, device; for model-calling runs also calls, tokens and API cost; for trained models inference time per unit | Cost tables that cannot be compared |
| Expected reading | A direction against a named comparison | A result argued after the fact |

## Identity pinning

Field list: [run-identity.md](run-identity.md). Before each new batch:

- Hosted model: send one probe request and compare the returned model id with the requested one; record
  the provider's version string. Generic case: a hosted endpoint answered one model name with another
  model, and results mixed two models.
- Local model: record the weight revision and file hash, not only the model name.
- Code: hash every file the run imports, including adapters, parsers and scoring scripts. Generic case: a
  seal hashed the main script but not a scoring script edited after the seal, so the program that produced
  the result had to be reconstructed.
- Compare the identities with the previous batch. A change is an unresolved discrepancy until explained.

## Smoke run

Run the exact configuration on real data, at full size, for a few units:

- the largest candidate set and the longest input, where memory peaks (generic case: a readout that fit at
  small candidate counts ran out of memory at the largest one and every unit of the batch failed);
- ports free, servers start and stop, model servers released when the runner ends;
- outputs parse, every output path is written, cost fields are present;
- the request does what its label says (an intervention named "order only" changes only the order, and
  does not, for example, average two orders).

A smoke run on synthetic data or at a smaller size does not count.

## Parity

For models that are compared with each other:

- per-unit hashes of the evidence, the rendered request and the candidate list match where the protocol
  says they match; keep these three hashes separate so a mismatch points to its cause;
- token counts per unit are a quick check: a large gap means one side received more or different text;
- visible-history counts per unit match, or the difference is a labelled condition.

## Rerun map

For each change to inputs, prompts, boundaries, parsers or code:

| Changed | Runs that read it | Rerun? | Reason when no rerun |
|---|---|---|---|
| | | yes / no | |

A change that touches a shared input reruns every run that reads it. A change that touches no input of a
run still gets a written reason.

## Approval

For a costly rerun, give the owner the complete specification (the fields above, the rerun map, cost and
runtime estimated from measured throughput) and launch once after confirmation. Partial reruns started
before the specification is complete are often rerun again. Run the parts the pending decision cannot
affect in the meantime.
