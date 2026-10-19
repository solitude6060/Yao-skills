# Lessons learned

Generalized from one research project that compared frozen, training-free language-model
recommenders with trained recommenders and LLM rankers on public e-commerce and rating
datasets. Each lesson names the inherited assumption, how it surfaced, and the
rule it produced.

### 1. An inherited split was not checked against the research question

- Assumption: the project specification prescribed a user-disjoint split plus a
  global time cutoff "to prevent leakage"; it was implemented as written.
- How it surfaced: a collaborator asked why trained baselines scored low. Trained
  baselines had never seen the evaluation users' histories, so the comparison measured
  unseen-user performance, while the frozen method read each user's history at
  inference time.
- Impact: every trained-baseline result from that protocol was evaluated under a
  condition unfavourable to the baselines and could not support a "frozen method
  matches trained baselines" claim. All results had to be rerun under a new protocol.
- Rule: before implementing a split, write the research question in one sentence and
  check that each method's training and inference inputs match it.

### 2. A protocol rule stronger than the leak it targets changes the question

- The global cutoff targets cross-user future data in training sets. For the frozen
  method, which reads only the user's own earlier events, there is no such channel.
  Applying the cutoff to it only removed valid history.
- Restricting baselines' training data to events before the cutoff left a large share
  of evaluation users with no training events at all, which again turned the task
  into cold-start evaluation.
- Rule: for each protection, name the leak channel, the methods that have it, and
  whether the rule removes more than that channel. Disclose the leak instead of
  over-correcting when the correction changes the task.

### 3. "First eligible event after the cutoff" as the target

- The specification chose each user's first eligible event inside a time window as the
  target. Gusak et al. (RecSys 2025, §4.2) show this target has longer gaps to the
  previous event and recommend against it.
- Rule: use the last event (LOO) or GTS with Last/Random/Successive targets.

### 4. A catalogue frozen at the cutoff hid history items from baselines

- The item catalogue was built from items seen before the cutoff. Items that first
  appeared later were dropped from the catalogue, and so from ID-based baselines'
  view of the user's history, while the text-reading method still saw their titles.
- Rule: count visible history items per method per query; the counts must match, or
  the difference is a labelled condition.

### 5. A leakage direction was asserted without measurement

- A project status note stated that cross-user future data under LOO "can only raise"
  trained-baseline scores. Ji et al. (TOIS 2023, Table 5) report changes in both
  directions (e.g. NeuMF NDCG@20 −35.5% to +13.8% on Amazon-electronic) and changed
  model rankings. The note was corrected.
- Rule: write the direction of a leak's effect only from a measurement on the data at
  hand; otherwise write "direction not determined" and plan a sensitivity check.

### 6. A self-made 5-core split differed from the official split

- A locally built 5-core LOO split differed from the official benchmark split of a
  public review dataset; the official files dedupe (user, item) pairs keeping the
  earliest review before splitting. On one product category, a 5-core built without
  deduplication kept a few percent more users and items than the official 5-core
  split, which has no repeated item within a user sequence and no test target in its
  history.
- Rule: download the official split when it exists, record hashes, and verify user,
  item and event counts, that each user sequence has no repeated items, and that no
  test target appears in its own history.

### 7. Popularity-weighted negatives inverted the popularity baseline

- With 50 candidates, uniform-random ranking has expected NDCG@10 0.091. Under
  popularity-weighted negatives the popularity ranker scored below that, because the
  most popular candidates were usually negatives.
- Rule: treat popularity-weighted negatives as a reverse stress test; answer "does the
  method rely on popularity" with full ranking, history-swap controls and
  stratification by target popularity.

### 8. Many method variants were compared on the reporting users

- Prompt, readout and history-length variants were all scored on the same users. The
  per-user oracle over variants (choosing the best variant per user using the target)
  produced large gains that a deployable selector did not reproduce.
- Rule: tune on development users, freeze, report on fresh users; report the number
  of variants tried; never report per-user oracle selection as a method result.

### 9. Execution failures mixed with method failures

- Out-of-memory crashes and server errors appeared as zero-utility queries in early
  tables.
- Rule: rerun execution failures until they succeed; only method failures (invalid or
  unparseable output, or no ranking by design) stay in the denominator with utility 0;
  show the failure count beside each score.

### 10. Repeated runs of a "deterministic" method differed

- A local frozen model produced small score differences across runs on identical
  inputs (cause not determined at the time); a hosted API re-query changed rankings for
  a sizeable share of users.
- Rule: run a determinism check (two identical runs) before declaring a method needs
  one run; repeat hosted-API queries on a subset.

### 11. The best of several test runs was admitted

- Assumption: a hosted model's run-to-run variation is noise, so keeping the highest
  of three repeated runs is harmless.
- How it surfaced: a pre-submission review found that the main table read the highest
  of three repeats on the development users, while the repeat record said the admitted
  row stayed the original run.
- Impact: a small difference in the metric, but it is test-set selection and
  contradicts "test scored once".
- Rule: admit the first pre-registered run; report repeat variability as a
  reproducibility measurement; never choose among runs by a test score.

### 12. Derived tables read an older checkpoint than the main table

- Assumption: once baselines are re-selected, every analysis picks up the new runs.
- How it surfaced: baselines were re-selected with a larger validation sample; the main
  table used the new checkpoints, but a fusion control and a time-anchor comparison still
  read result files written before the re-selection (one baseline scored visibly
  differently on the same users).
- Rule: every table builder asserts the checkpoint identity (hash or run id) of each
  baseline row against the main table's; a re-selection triggers a rerun of every
  derived analysis.

### 13. Quantified claims did not transfer to a replacement dataset

- Assumption: replacing one dataset only changes the numbers in the tables.
- How it surfaced: after the swap, three universal bounds in the text (phrases such as
  "at most" and "never above" with a fixed number) failed on the new or added data.
- Rule: list every quantified claim before a dataset change and re-verify each per
  dataset; prefer ranges with the datasets named.

### 14. A request-time protocol drove most of the gain on one dataset

- Assumption: cross-user statistics computed up to the request time are a fair input
  because a serving system observes those events.
- How it surfaced: with the statistics anchored at the user's last visible event, the
  method's NDCG@10 dropped by a large amount on one dataset; with time-matched
  negatives it fell below two sequential baselines. A sizeable share of the uniform
  negatives had no interaction before the request day, which request-time counts
  reject easily.
- Rule: report the default protocol with its reason, the anchor and matched-negative
  sensitivity in the body, and measure the opposite exposure too (how much of the
  trained baselines' training data lies after the request time under leave-one-out).

### 15. A model input carried cross-user information

- Assumption: the frozen model's increment over the statistics measures what the model
  reads from the user's own history and item text.
- How it surfaced: on two datasets the selected input added a sentence about whether
  other users had chosen the candidate next, and that sentence counted same-day events
  of other users with an earlier row, a looser time boundary than the statistics used.
- Rule: report the increment with an input free of cross-user information beside the
  selected one; use one time boundary for every component, or disclose each.

### 16. A dataset was dropped after its results were seen

- Assumption: the paper may keep the datasets that best illustrate the method.
- How it surfaced: two datasets added under a written pre-commitment ("every result
  enters the comparison") were nearly left out of the plan, while an older dataset with
  unfavourable results was removed.
- Rule: write a pre-commitment before downloading new datasets and follow it; when an
  existing dataset is removed, record a reason that holds independently of its results.

### 17. A hosted model changed behind its name

- Assumption: a hosted endpoint's model name identifies a fixed model.
- How it surfaced: the provider re-pointed the endpoint to a new model mid-study; a
  reproduction check against a repeat-noise floor showed a different model.
- Rule: store the returned model identifier with every response, check identity before
  each new batch, rerun all cells under the new model and disclose the change.
