# Lessons learned

Generalized from one research project that compared frozen, training-free language-model
recommenders with trained recommenders and LLM rankers on public e-commerce, rating and
game-platform datasets. Each lesson names the inherited assumption, how it surfaced, and
the rule it produced. Lessons 18 to 29 come from the project's later audits, external
pre-submission review and follow-up topics.

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
  sensitivity in the body (one neutral body sentence that points to the appendix table;
  `paper-writing` principle 6), and measure the opposite exposure too (how much of the
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

### 18. The negative sampler identified the target

- Assumption: a deterministic, reproducible rule for drawing negatives is as good as a
  random draw.
- How it surfaced: an answer-path audit found that negatives were the catalogue items
  with the smallest salted hash, a rule applied to negatives but not to the target.
  Ranking candidates by the reversed rule put the target first for every audited user on
  one dataset. No method read the hash, but any future scorer that saw it could.
- Rule: draw negatives with a seeded uniform random generator (or a rule the target also
  satisfies), store the candidate file with its hash, and test whether any function of
  the sampling rule ranks the target above random.

### 19. Item identifiers in model requests carried an ordering signal

- Assumption: an item identifier in a request is a neutral label.
- How it surfaced: in a follow-up study a verifier ranked new-item candidate pools by
  identifier order alone and scored well above random, because identifiers were
  assigned in time order.
- Rule: never put item identifiers in model requests; use them only as keys and as the
  documented tie order. Run an identifier-only rule as a shortcut check when candidates
  differ in age.

### 20. A refit step that the sources do not use

- Assumption: after selecting hyperparameters on validation data, retraining on
  training plus validation events ("refit") is the standard protocol.
- How it surfaced: a collaborator asked which source used refit; refit was dropped and every
  refit row was superseded in an exceptions record. A later practice check of the official
  sequential-recommender code and a widely used library confirmed that they evaluate the
  best validation checkpoint without refit; some baseline-rigour studies refit and one
  official implementation merges the validation event into training.
- Rule: follow each baseline source's selection-versus-refit practice, name it in the
  protocol, and refit only where the source does.

### 21. A validation sample that excluded the evaluated users

- Assumption: a baseline's validation users can be any random sample.
- How it surfaced: on a large dataset the official baseline code selects on a sampled
  subset of users. The project drew that sample so that it contained the evaluated users,
  so baseline selection covered the users whose results are reported, and shared one
  sample file across baselines.
- Rule: when a validation sample is drawn, it contains the evaluated users; every
  baseline reads the same sample file, recorded with its hash and seed.

### 22. A high-severity protocol finding was deferred

- Assumption: a finding from an internal audit can wait until after the paper text is
  drafted.
- How it surfaced: an audit rated as high severity that the method's statistics used the
  request time while trained baselines did not. It was deprioritized; the external
  pre-submission review made it the central objection, and the answering experiments
  (lessons 23 and 24) were run late.
- Rule: answer a high-severity protocol finding with an experiment before the claims
  freeze; a limitation sentence alone does not answer it.

### 23. Fairness under a global cutoff has to remove events on both sides

- Assumption: the request-time advantage of the method is measured by changing only
  the method's inputs.
- How it surfaced: under leave-one-out, trained baselines learn from other users' events
  after a test user's request time, while the method's statistics see events up to that
  time. A run that applied one global time cutoff to both, removing later events from
  the method's statistics and from the baselines' training data, showed that every
  method dropped and that most of the drop came from targets that did not exist before
  the cutoff.
- Rule: when the method reads request-time cross-user information, run a global-cutoff
  sensitivity check that removes post-cutoff events from every method, and report which
  targets the cutoff makes unseen.

### 24. Time-aware baselines are needed when the method reads time

- Assumption: order-only sequential baselines are a fair comparison for a method whose
  inputs carry dates and time-decayed statistics.
- How it surfaced: the external review asked for an information-equal comparison;
  time-aware trained baselines (a temporal linear item-item model and a time-interval
  self-attention model) were added from their official code.
- Rule: when the method reads timestamps, include at least one time-aware trained
  baseline from its official source, and state the remaining asymmetries.

### 25. A sibling project reused exposed users

- Assumption: users that are fresh for one study are fresh for its follow-up.
- How it surfaced: a follow-up project's cohort overlapped the users that a sibling
  project had drawn for its own study; an exposure scan found the overlap before any
  result and the overlapping users were removed.
- Rule: before calling a cohort held out, scan every earlier run and every sibling
  project that used the same data for contact with its targets.

### 26. A cold-item premise failed its definitional count

- Assumption: targets that are new at the request time are cold items.
- How it surfaced: in a follow-up topic, counting showed that most targets labelled new
  at the request time already had interactions before the request, so the planned
  cold-start claim had few qualifying targets.
- Rule: before a cold-start or new-item claim, count the qualifying targets under the
  exact time and tie rule the protocol uses, and report the count with the claim.

### 27. Uniform negatives were easier for a time-aware method

- Assumption: uniform negatives are neutral across methods.
- How it surfaced: an internal audit noted that uniform negatives include items with no
  interaction before the request time, which request-time statistics reject easily but
  order-only baselines do not (lesson 14).
- Rule: when any method reads request-time activity, report a time-matched negative
  variant (negatives drawn from items active before the request) beside the uniform one.

### 28. One configuration of an LLM baseline was not enough

- Assumption: running an LLM-based baseline with its official settings settles the
  comparison.
- How it surfaced: the official input limit truncated part of the users' histories;
  the project ran the official configuration and a variant with a relaxed limit and
  reported them side by side.
- Rule: run the official configuration and, where its limits bind, a relaxed variant;
  label both, keep both in the tables, and say which one each claim uses.

### 29. Regeneration rounds were decided after seeing scores

- Assumption: retrying unparseable LLM outputs until they parse is harmless.
- How it surfaced: method failures of generative baselines were retried in several
  reruns; the protocol later fixed the number of regeneration rounds, kept the parser
  unchanged, and skipped an update after the declared rounds all failed.
- Rule: declare the regeneration rounds and the parser before the run, record the scores
  before and after retries, and count outputs that fail every round as method failures.
