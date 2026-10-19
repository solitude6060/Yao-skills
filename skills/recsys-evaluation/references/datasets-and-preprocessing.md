# Datasets and preprocessing

Read before building or reusing a processed dataset. Preprocessing decisions change
user counts, targets and scores, and they are often invisible in the paper text.

## Use the official benchmark files when they exist

If a dataset publisher ships a split, use it and record the file hashes. A self-made
split that "follows the same rule" usually differs in user and item counts because of
filter order (dedupe before or after k-core, k-core iterated to a fixed point or once,
tie handling).

Amazon Reviews 2023 ([McAuley Lab dataset page](https://amazon-reviews-2023.github.io/);
paper [Hou et al., arXiv 2403.03952](https://arxiv.org/abs/2403.03952), which introduces
the dataset with over 570 million reviews and 48 million items). The
[benchmark scripts README](https://github.com/hyp1231/AmazonReviews2023/tree/main/benchmark_scripts)
states:

- Duplicates: "We remove repeated reviews (those from the same pair of user & item,
  but may with different review text and ratings) and only keep the earliest ones."
- k-core: "k = 0 or 5".
- Last-out split: "For each user, the latest review will be used for testing, the
  second latest review will be used for validation, and all the remaining reviews are
  used for training."
- Timestamp split: training (−∞, t1), validation [t1, t2), test [t2, +∞) with fixed
  millisecond cutoffs t1 = 1628643414042, t2 = 1658002729837.

## k-core filtering

- k-core keeps users and items with at least k interactions, usually iterated until
  stable. State k, whether it was iterated, and whether it ran before or after dedupe.
- [Hidasi & Czapp, §2.2 "Overzealous preprocessing"](https://arxiv.org/pdf/2307.14951)
  warn against general claims drawn from heavily preprocessed data.
- Report the final user, item and event counts and compare with the official or
  previously published counts. A mismatch is a finding to explain, not to ignore.

## Duplicate (user, item) interactions and repeat consumption

- Options: keep earliest, keep latest, keep all. Amazon Reviews 2023 benchmark keeps
  the earliest (above).
- RecBole `rm_dup_inter`: "if `rm_dup_inter=first`, we will keep the first user-item
  interaction in duplicates; if `rm_dup_inter=last`, ... the last ... Defaults to
  `None`" (no removal) —
  [RecBole data settings](https://recbole.io/docs/user_guide/config/data_settings.html).
- [Li et al., "Repetition and Exploration in Sequential Recommendation", SIGIR 2023](https://dl.acm.org/doi/10.1145/3539618.3591914)
  ([PDF](https://staff.fnwi.uva.nl/m.derijke/wp-content/papercite-data/pdf/li-2023-repetition.pdf)):
  repeat items in a dataset "often act as easy shortcuts"; models show repetitive
  bias. If repeats are kept, report repeat-target and new-target results separately.
- Whatever the choice, the target must not appear in the user's visible history
  unless repeat recommendation is the research question.

## Timestamp ties

- Many datasets have coarse timestamps. Hidasi & Czapp §2.1 report day-level
  resolution in Amazon and Steam and many collisions in MovieLens-10M; MovieLens-10M
  ships sorted by user and item ID, so ties sorted by item ID create the same false
  sequence for different users ([§2.1](https://arxiv.org/pdf/2307.14951)).
- Break ties by the dataset's original row order (or an explicit secondary timestamp).
  Never break ties by item ID.
- Visible history must strictly precede the target in (timestamp, row order).

## Common datasets and why the version matters

| Dataset | Notes | Source examples |
|---|---|---|
| MovieLens-1M | 6,040 users, 3,416 items after SASRec preprocessing; long histories (avg 163.5 actions per user) | [SASRec Table II](https://arxiv.org/pdf/1808.09781) |
| Amazon 2014 (Beauty, Sports, Toys, Games, ...) | 2014 crawl; per-category 5-core files widely reused; Beauty 52,024 users / 57,289 items in SASRec, 40,226 / 54,542 in BERT4Rec (different preprocessing) | [SASRec Table II](https://arxiv.org/pdf/1808.09781), [BERT4Rec Table 1](https://arxiv.org/pdf/1904.06690) |
| Amazon Reviews 2023 | New crawl, official dedupe rule and official splits; not comparable to 2014 numbers | links above |
| Steam | 334,730 users / 13,047 items in SASRec; 281,428 / 13,044 in BERT4Rec | same tables |
| Yelp | Several releases; used in DaisyRec, Ji et al. | [DaisyRec 2.0](https://arxiv.org/pdf/2206.10848), [Ji et al.](https://arxiv.org/pdf/2010.11060) |

The same dataset name in two papers does not imply the same data: the Beauty counts
above differ between SASRec and BERT4Rec. Name the release year, the filter and the
split file.

## Item catalogue and history visibility

- Define the catalogue once (all items that appear in training, or all items in the
  split) and apply it to every method.
- A catalogue frozen at a cutoff can drop items that appear in a user's visible
  history. If one method still reads those items as text while another cannot index
  them, the methods no longer see the same evidence. Check the number of history
  items per method, not only the number of users.
- Items in validation/test that never appear in training cannot be recommended by
  ID-based models. Count such targets and report them.

## Minimum preprocessing record

Source file and hash; dedupe rule; k and filter order; tie rule; split rule or official
split file; final user/item/event counts; number of targets with history length 0 or
below a threshold; catalogue definition; evidence hash and candidate hash per query.
