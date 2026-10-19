# Evaluating LLM-based and frozen-model recommenders

Read when any compared method is a language model, an LLM agent, or a frozen
model that scores candidates from text.

## Candidate list size

- LLM-ranking papers mostly use small sampled candidate lists: LLMRank 20 candidates
  ([Hou et al., ECIR 2024, §3](https://arxiv.org/pdf/2305.08845)), A-LLMRec 1+19
  ([§5.1](https://arxiv.org/pdf/2404.11343)), AgentCF 1+9
  ([§3.1](https://arxiv.org/pdf/2310.09233)), LLM-SRec 1+99
  ([§2.2](https://arxiv.org/pdf/2502.13909)), LLaRA 20 candidates with HitRatio@1
  ([§5.1](https://wujcan.github.io/papers/sigir24-llara.pdf)).
- Prompt length, latency and position effects grow with n. Report a candidate-count
  curve on nested sets (20 ⊂ 50 ⊂ 100) rather than a single n.
- For a full-catalogue claim, use two-stage evaluation (see `candidates-and-metrics.md`).

## Position bias and order permutation

- [LLMRank §3.2](https://arxiv.org/pdf/2305.08845): LLMs "suffer from position bias
  and popularity bias while ranking"; ranking each candidate set 3 times with shuffled
  order (bootstrapping) reduces position bias.
- Fix and record the candidate order seed. Check that the target position is uniform
  over queries. For a load-bearing claim, run a permutation check (same queries,
  shuffled order) and report the change.

## Parse and invalid-output failures

- Generative rankers can return items outside the candidate list, duplicates, truncated
  lists or free text. Define the parser once, apply it to every generative method, and
  count failures by type.
- Unparseable output is a method failure: utility 0, kept in the denominator, count
  reported. A token-limit truncation caused by the method's own verbosity is a method
  failure; a server error is an execution failure and is rerun.
- Readout methods that score each candidate by likelihood or logits have no parse
  failures; say so rather than reporting 0 as an achievement.

## Item text

- State the text fields used: title only, title + category, title + description,
  reviews. Results change with text richness and text length.
- Check whether a score correlates with description length or prompt position; if the
  target's text is systematically shorter or longer than the negatives' in the sampled
  set, a length heuristic can score above random.
- Every method in the comparison gets the same text fields, or the difference is a
  labelled condition.

## Controls that show the method uses personal evidence

| Control | What it rules out |
|---|---|
| Lexical overlap baseline (BM25 between history text and candidate text) | Gains explained by word overlap |
| Category match rule | Gains explained by category continuity |
| Popularity and recency rules | Gains explained by item popularity or recent items |
| History swap / mismatch (give user A's history to user B's query) | The method ignores the history; a large drop from correct to swapped history shows personal evidence use |
| Empty or truncated history | Dependence on history length |
| Stratification by target popularity | Reliance on popular targets |

Report correct-minus-swapped differences with paired intervals.

## Latency, tokens and cost

- Report per-query latency (median and tail), input and output tokens, and cost per
  1,000 queries with the price date.
- Use equal caching for every method: either all methods reuse prompt prefix caches or
  none do. State the hardware, batch size and serving stack.
- Separate one-time costs (training, index building) from per-query costs.

## Pretraining exposure

- A frozen model may have seen the dataset's reviews or item pages during pretraining.
  This is not the same channel as cross-user future data in the training split, and it
  is not removed by any split.
- Disclose the model's training data cutoff and known sources relative to the
  dataset period. Where possible, add a domain or period the model is unlikely to have
  seen, or a dataset released after the model's cutoff.

## Other LLM-specific reporting

- Model identity as returned by the API, request hashes, decoding parameters, and the
  full prompt template.
- For agents (multi-step tool use, memory): the number of LLM calls per query, and
  whether memory was built from training users only.
- Distinguish target-domain training (fine-tuned LLM recommenders such as TALLRec,
  LLaRA, A-LLMRec, LLM-SRec) from training-free use; they belong in different
  information-access layers (`baselines-and-fairness.md`).
