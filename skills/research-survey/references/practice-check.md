# Practice check

A practice check answers one question: for a protocol or design choice, what do the official
implementations and the strongest baselines actually do? It replaces an invented setting with a precedent,
or makes a departure from precedent explicit before reviewers find it.

## When it is required

- A setting is about to be chosen without a cited precedent (split, target rule, tie order, validation
  sampling, selection and refit, retries, filters).
- A setting inherited from a specification, an earlier project or another paper is load-bearing.
- A reviewer or advisor asks "is this how others do it?".
- The owner asks a design question that evidence can settle; answer it from the check, with a recommendation.

## Template

```markdown
## Practice check: <decision in one line>

Decision and options: <the choice and the alternatives>
Question it serves: <research question id with its plain name>

| Source | Kind | Revision | Location | What it does |
|---|---|---|---|---|
| <official implementation> | official code | <commit or tag> | <file:line> | <behaviour> |
| <strong baseline or library> | library code | <version> | <file:line> | <behaviour> |
| <paper> | paper text | <version> | <section, page> | <stated setting> |

Agreement: <all agree | split, with the reason>
Recommendation: <setting>, precedent <sources>
Departure from precedent: <none | what differs, why, where it is disclosed>
Absence labels: <not found / not disclosed / inferred absent / verified absent, per source where relevant>
Cache: <where the code revision and PDFs are stored>
```

Read the code path that runs the setting (the training or evaluation entry point and the functions it
calls), not only the README or the configuration defaults. A default in a configuration file can differ
from what a released checkpoint used; record which one the claim rests on.

## Generic examples

| Decision | Where to look | What to record |
|---|---|---|
| Split and target rule (which event is the test target; which one validates) | The evaluation data loader of each official implementation; the paper's protocol section | The target index per user, how validation is formed, whether the split is per user or global |
| Tie order for events with equal timestamps | Preprocessing code; dataset documentation on timestamp resolution | Sort keys in order (timestamp, then original row order, or item identifier); the timestamp resolution |
| Validation sampling on large datasets | The validation loop of the official code | Whether all users or a sample is validated, the sample size rule, the seed, whether the evaluated users are inside the sample |
| Selection checkpoint versus refit | The training loop and the reporting script | Whether the reported model is the best validation checkpoint or a model refit on training plus validation data |
| Retry rounds for generative baselines | The baseline's inference script and paper | Whether failed outputs are regenerated, how many rounds, whether the parser changes between rounds |
| Dataset filters (minimum interactions, items without text) | Official preprocessing scripts | Filter order, thresholds, the resulting counts against the published statistics |

Generic cases: in one recorded check, the official code of a sequential recommender and a widely used
library both reported the best validation checkpoint without refitting, which settled a refit question that
had already produced many superseded rows; a validation sample drawn without the evaluated users had to be
redrawn so that the larger sample contained them.

## Rules

- A practice check cites code at a pinned revision; a blog post, a summary or an agent's description is a
  lead to that code.
- When precedents disagree, record each and the reason; pick the one that fits the research question and
  disclose the choice.
- A departure from precedent is decided in the protocol before the run and recorded in the decision log.
- A practice check that changes a running protocol triggers the rerun map in `experiment-contract`.
