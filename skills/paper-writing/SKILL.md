---
name: paper-writing
description: Use when drafting, cutting or restructuring a research paper's prose, tables and figures, or when deciding what stays in the body and what moves to the appendix under a page limit.
argument-hint: "<paper path | section | table list | empty>"
---

# Paper Writing: body, tables, appendix

Reviewers decide from the body; many venues tell them they need not read past the page limit. Each body
sentence asks a question, says how it is tested, reports what was observed, or says what it means.
Anything else is cut or moved to the appendix.

Chinese explanation: [SKILL.zh.md](SKILL.zh.md). Rules with examples: [references/writing-rules.md](references/writing-rules.md).
Tables and figures: [references/tables-and-figures.md](references/tables-and-figures.md). Body versus appendix:
[references/body-appendix.md](references/body-appendix.md). Section budgets and patterns from twelve exemplar papers:
[references/section-patterns.md](references/section-patterns.md).

## When to use

- A draft is over the page limit, wordy, or reads like an experiment log.
- Tables repeat numbers, carry long notes, or answer several questions at once.
- A dataset, model or result changed and the text has to follow.
- Before a draft goes to an advisor, co-author or submission system.

Not for: building the argument itself (use `paper-argument`), protocol validity (use `recsys-evaluation`), or
checking an inherited assumption (use `first-principles`).

## Principles

1. **One argument.** The introduction asks one main question and its sub-questions. Each section serves one of
   them and ends with its answer. The conclusion answers them in the same order and words.
2. **Point order: reason, description, analysis, conclusion.** A paragraph that only describes is unfinished;
   end each experiment paragraph with what the result means.
3. **Numbers live in tables and figures.** The text cites the one or two numbers that carry the point, in one
   format throughout (absolute difference with the relative change in parentheses, e.g. +0.030 (+6.0%)).
   No recitation of ranges and cell lists.
4. **Plain register.** Short sentences, few parentheses, no dashes as sentence connectors, standard terms, no
   metaphors or self-praise adjectives. Confident and factual; a human tone.
5. **Claims hold where they are stated.** Quantified claims ("at most", "never", "on all datasets") are
   rechecked against the result files whenever data, models or cohorts change. Prefer a range with the
   datasets named over a universal bound.
6. **Load-bearing caveats stay in the body.** If a result depends on the protocol, the body says so in one
   sentence with the key numbers; the appendix holds the full table.

## Body versus appendix

Body: the problem and question, the method at the level needed to reproduce the idea, the main comparison,
the analysis that answers each core question (one table or figure each), one sentence per robustness check
with its key number, limitations of named claims, the conclusion.

Appendix: settings, grids and prompts, hardware and versions, per-dataset details, full robustness tables,
extra baselines, derivations, further cases.

Test for each paragraph or float: if removing it leaves every body claim supported, move it.
Details and a decision table: [references/body-appendix.md](references/body-appendix.md).

## Tables

- One question per table. The comparison the reader must make sits in adjacent columns or in a difference column.
- A number appears in one table only. Merge tables that share rows or columns; replace a separate interval
  table with a difference column or significance marks in the main table.
- Main metric first; secondary metrics go to the appendix when space is short.
- The caption's first sentence states what the table shows; at most two short sentences of legend.
- Classic style: booktabs rules, no vertical lines, fixed decimals aligned on the point, best value in bold,
  the same dataset and method order in every table.
- Change the generator, never the generated file.

## Procedure

1. **Inventory.** Words per section, floats per section, caption and note lengths, numbers repeated across
   tables, compiled page count.
2. **Map.** Tag each paragraph and float with the question it serves, then mark keep, cut, move or merge.
3. **Budget.** Set words per section from the page limit. A two-column eight-page paper typically fits
   about 5,000 to 5,500 words with six to eight floats; treat this as a starting estimate and compile to check.
4. **Rewrite** section by section in the closed-loop order; regenerate tables from their generators;
   recompile and check page breaks and float placement on every page.
5. **Re-verify** every number and quantified claim against the result files.
6. **Language pass** by two independent readers from different model families or people, then the author.
7. **Record** each change with the rule it follows. When the author gives a new writing rule, add it to
   [references/writing-rules.md](references/writing-rules.md) in the same change.

## Output

A plan (inventory, map, budget), the revised source on a branch, a change log that maps each edit to a rule,
and the compiled PDF. Report to the author in the language of the conversation.
