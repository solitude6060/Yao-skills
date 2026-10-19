# Tables and figures

Rules from an author's corrections and classic recommender-paper practice (SASRec, LightGCN, EASE
style tables). Change the generator, never the generated file.

## Tables

| Rule | Detail |
|---|---|
| One question per table | If a table answers two questions, split it or move one half to the appendix. |
| Comparison in adjacent cells | Put the proposed method next to the strongest baseline, or add a difference column. |
| A number in one place only | If two tables share rows (methods) or columns (datasets, metrics), merge them or drop the duplicate block. |
| Main metric first | Secondary metrics (MRR, HR at other cut-offs) go to the appendix when the body is full. |
| Short caption | First sentence: what the table shows. At most two more short sentences for marks and abbreviations. No paragraphs of notes. |
| Classic layout | booktabs rules (top, mid, bottom), no vertical lines, no shading, caption above the table. |
| Numbers | Fixed decimals per metric, aligned on the decimal point; best value in bold; second best underlined only when the comparison needs it. |
| Groups | Method families separated by a midrule with a short group label. |
| Consistent order | Same dataset order and method order in every table and figure. |
| Marks | Each symbol has a legend in the caption; use as few kinds of marks as possible. |
| Width | Prefer single-column tables; a full-width table must carry the main comparison. |

## Consolidation patterns

| Situation | Consolidation |
|---|---|
| A main results table and a separate table of paired differences with intervals | One table: add a difference column against the strongest baseline, or mark cells whose interval excludes zero; put the full interval table in the appendix. |
| Several robustness variants, each in its own table (different negatives, different time anchors) | One table with the variants as column groups and only the method rows that the claim needs; or one sentence per variant in the body and the table in the appendix. |
| An ablation table and a separate "single component alone" table | One table with two blocks, or keep only the removal block in the body. |
| A cost table and a cost figure that show the same numbers | Keep the figure in the body (quality against cost), the table in the appendix. |
| Settings, grids, prompts | Appendix only. |
| Per-cohort repeats of the same table (development and confirmation users) | Body shows the confirmation or full cohort; the other cohorts go to the appendix. |
| Small changes below a stated threshold | Collapse into one note line instead of separate rows. |

## Figures

| Rule | Detail |
|---|---|
| Vector format | PDF or PGF; fonts match the body text size after scaling. |
| Palette | One colour-blind-safe palette across the paper; a second encoding (marker shape or line style) for each series. |
| Clean axes | Light gridlines, no titles inside the plot (the caption carries the title), legend inside or shared. |
| Caption | Caption below the figure; first sentence states the finding. |
| Overview figure | Labels match the section and module names used in the text. |
| One figure, one message | A figure with several panels still answers one question; otherwise split or move panels to the appendix. |
