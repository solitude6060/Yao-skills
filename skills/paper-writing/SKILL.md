---
name: paper-writing
description: Use when drafting, cutting or restructuring a research paper's prose, tables and figures, deciding what stays in the body and what moves to the appendix under a page limit, or preparing the submission package.
argument-hint: "<paper path | section | table list | empty>"
---

# Paper Writing: body, tables, appendix

Reviewers decide from the body; many venues tell them they need not read past the page limit. Each body
sentence asks a question, says how it is tested, reports what was observed, or says what it means.
Anything else is cut or moved to the appendix.

Chinese explanation: [SKILL.zh.md](SKILL.zh.md). Rules with examples: [references/writing-rules.md](references/writing-rules.md).
Tables and figures: [references/tables-and-figures.md](references/tables-and-figures.md). Body versus appendix:
[references/body-appendix.md](references/body-appendix.md). Submission package:
[references/submission-and-release.md](references/submission-and-release.md). Section budgets and patterns
from twelve exemplar papers: [references/section-patterns.md](references/section-patterns.md).

## When to use

- A draft is over the page limit or reads like an experiment log; tables repeat numbers or answer several
  questions at once.
- A dataset, model or result changed and the text has to follow.
- Before a draft goes to an advisor, co-author or submission system; preparing the submission package.

Not for: building the argument (`paper-argument`), protocol validity (`recsys-evaluation`), independent
checks of numbers and claims (`research-verification`), or checking an inherited assumption
(`first-principles`).

## Principles

1. **One argument.** The introduction asks one main question and its sub-questions. Each section serves one of
   them and ends with its answer. The conclusion answers them in the same order and words.
2. **Point order: reason, description, analysis, conclusion.** A paragraph that only describes is unfinished;
   end each experiment paragraph with what the result means.
3. **Numbers live in tables and figures.** The text cites the one or two numbers that carry the point, in one
   format throughout (absolute difference with the relative change in parentheses, e.g. +0.030 (+6.0%)).
   A quoted difference equals the difference of the printed cells, or one stated rounding rule covers every
   quoted difference. An interval that includes zero is reported as no significant difference, never as
   "on par". No recitation of ranges and cell lists.
4. **Plain register.** Short sentences, few parentheses, no dashes as sentence connectors, standard terms, no
   metaphors or self-praise adjectives, no self-posed questions, no bold take-aways. Confident and factual; a
   human tone.
5. **Claims hold where they are stated.** Quantified claims ("at most", "never", "on all datasets") are
   rechecked against the result files whenever data, models or cohorts change. Prefer a range with the
   datasets named over a universal bound. Process claims are literally true. The paper never prints
   "cause not determined": resolve the cause, or omit the statement and keep the observation in the appendix.
6. **Protocol-dependent results get one neutral body sentence** that names the condition and points to the
   appendix table holding the numbers, intervals and full comparison. No bold, no negative conclusion
   sentence; deployment limits are written as conditions ("requires faster hardware for sub-second
   serving"). Procedure disclosures (development users, selection rules, exposure) are never removed; check a
   must-keep list after each rewrite.
7. **Text sources.** Author-approved text is versioned and never reverted silently. Another model's rewrite
   is an idea source; check its facts against the result files before adopting any of it. Key terms
   follow the field's definition; no untested aside against the method's own components, while measured adverse effects are reported; bilingual
   editions change together.

## Body versus appendix

Body: the problem and question, the method at the level needed to reproduce the idea, the main comparison,
the analysis that answers each core question (one table or figure each), one neutral sentence per
robustness or protocol check (principle 6), limitations of named claims, the conclusion.

Appendix: settings, grids and prompts, hardware and versions, per-dataset details, full robustness tables,
extra baselines, derivations, further cases.

Test for each paragraph or float: if removing it leaves every body claim supported, move it.

## Tables

One question per table, with the comparison in adjacent columns or a difference column; each number in one
table only; main metric first; a caption whose first sentence states what the table shows. Layout and
merging patterns: [references/tables-and-figures.md](references/tables-and-figures.md). Change the generator,
never the generated file.

## Procedure

1. **Inventory.** Words per section, floats per section, caption and note lengths, numbers repeated across
   tables, compiled page count.
2. **Map.** Tag each paragraph and float with its question; mark keep, cut, move or merge.
3. **Budget.** Set words per section from the page limit (two columns, eight pages: start from about
   5,000 to 5,500 words and six to eight floats); compile to check.
4. **Rewrite** section by section in the closed-loop order; regenerate tables from their generators;
   recompile and check page breaks and float placement on every page.
5. **Re-verify** every number and quantified claim against the result files, the must-keep list, and every
   reference (the citation ladder of `research-survey`).
6. **Language pass** by two independent readers from different model families or people, then the author.
7. **Package.** Before submission, run the page gate and the venue, release and edition checks in
   [references/submission-and-release.md](references/submission-and-release.md).
8. **Record** each change with the rule it follows. When the author gives a new writing rule, add it to
   [references/writing-rules.md](references/writing-rules.md) in the same change.

## Output

A plan (inventory, map, budget), the revised source on a branch, a change log that maps each edit to a rule,
and each edition's compiled PDF with its commit. Report to the author in the language of the conversation.
