# Body versus appendix

Many venues limit the content pages and allow references and an appendix after them (for example, the ACM Web
Conference 2027 call: eight content pages, at most twelve pages in total in a single PDF, and reviewers are not
required to read past the eighth page). Check the current call for the target venue: page counts, whether a
separate supplementary file is accepted, and whether the appendix counts toward a total.

## Decision table

| Content | Body | Appendix |
|---|---|---|
| Problem, question, contributions | yes | no |
| Method: equations and the design reason of each component | yes | derivations, implementation details |
| Datasets: names, sizes, protocol in one paragraph or one small table | yes | preprocessing, filters, statistics beyond the table |
| Baselines: list with one-line descriptions and sources | yes | settings, search spaces, versions, hardware |
| Main comparison table | yes | per-cohort or secondary-metric versions |
| Significance or intervals for the main claim | marks or a difference column | full interval tables |
| Analysis answering each core question | one table or figure each | further variants, sensitivity sweeps |
| Robustness and protocol sensitivity | one sentence per check with its key number | full tables |
| Cost and latency | one figure or one compact table | full cost table with all fields |
| Case study | one compact example if it supports a core claim | further cases |
| Limitations | named claims and their scope | — |
| Prompts, templates, grids, model versions, ethics details | no | yes |

## Tests

1. **Removal test.** If removing a paragraph or float leaves every body claim supported, move it.
2. **Self-contained test.** Read only the body: every claim has its evidence, every symbol is defined, every
   load-bearing caveat is visible.
3. **Pointer test.** Each appendix section is cited once from the body at the point where a reader would ask for it.
4. **Single-PDF test.** If the venue accepts one PDF only, a separate supplementary file has no place; merge it
   into the appendix within the page total or drop it.
