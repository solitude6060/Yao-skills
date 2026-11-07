# Run identity

The minimum provenance a run needs so that another person can say which program, model and data produced
each number, and rerun it. Keep small records (this list, configuration snapshots, hashes, aggregates) in
version control; keep large or private material (raw responses, checkpoints, caches, logs) in persistent
storage linked from the result table.

## Fields

| Group | Fields |
|---|---|
| Run | Run id, contract or card version, research question, evidence stage, launch and end time from `date` |
| Source | Upstream URL and revision for each reused method; files actually imported and their hashes, including adapters, parsers and scoring scripts; local differences from the source and their authorization |
| Configuration | Full configuration snapshot; which values are source defaults, published settings or project additions |
| Data | Dataset release, preprocessing steps, split rule, event and item mapping, dataset hash |
| Units | Cohort ids, target rule, candidate rule; candidate hash |
| Inputs | Evidence hash, rendered-request hash and candidate hash, kept as three separate values |
| Model | Requested model id; returned model id per response for hosted models; provider version string; weight revision and hash for local models; checkpoint id, selection stage and refit stage for trained models |
| Randomness | Seeds; whether determinism was observed, and under which runtime (same session, same device) |
| Environment | Interpreter, framework and dependency versions, device, driver |
| Execution | Exact commands, attempts per unit with causes, retry rounds used |
| Outputs | Raw request and response paths (stored before any metric is computed), per-unit result file, aggregate |
| Cost | Calls, tokens, wall time, latency median and p95, peak memory, API cost |

## Exclusions

Never store credentials: no API keys, tokens, passwords or session cookies in configuration snapshots,
logs, receipts or published records. Record which credential role was used, not its value. Strip personal
data from requests and logs that leave the machine.

## Determinism

Determinism is observed, not assumed. A method with no random component can still return different
outputs across server sessions or devices. Record what was observed ("identical across two sends in one
session"), not the expectation. Generic case: answers that repeated exactly within one server session did
not repeat exactly across sessions; the cause was not determined, and the identity record now states the
session.
