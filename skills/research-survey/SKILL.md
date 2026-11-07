---
name: research-survey
description: "Use when a research decision needs evidence from sources: a field survey, what official code and strong baselines actually do, whether a source supports a cited claim, model or dataset facts, or what a concurrent preprint changes."
argument-hint: "<landscape | practice | citation | concurrent | facts> <question or file | empty>"
---

# Research Survey: source evidence for a decision

A survey here serves one decision (a protocol choice, a novelty claim, a citation, a model fact) and leaves a
record that anyone can check against the source.

Chinese: [SKILL.zh.md](SKILL.zh.md). References: [practice-check.md](references/practice-check.md),
[citation-ladder.md](references/citation-ladder.md), [concurrent-work.md](references/concurrent-work.md).

## When to use

- A protocol or design choice needs precedent: what do official implementations and strong baselines do?
- A component is about to be called new, or a sentence cites a source.
- A model, dataset or provider fact (training data, size, version, licence) is about to be written down.
- A preprint appears that overlaps the study, or a milestone or submission is near.
- The next step is implementation and the code, checkpoints or data may not exist.

Not for: related-work prose (`paper-writing`); recommender protocol rules
(`recsys-evaluation`); a long narrative literature report (`deep-research` if installed; this skill frames
its questions and verifies its output).

## Modes

| Mode | Question form | Sources | Output row |
|---|---|---|---|
| Landscape | Which approaches address question Q, and what is missing? | Full papers, official code, surveys | Approach, setting, information used, protocol, gap |
| Practice check | What do official code and strong baselines do for choice X? | Code at a pinned revision, paper sections | Implementation, revision, file and line, behaviour |
| Citation check | Does source S support sentence C? | The source's full text | Ladder step reached, quote, location |
| Concurrent-work watch | Does a new preprint change our question, claims or comparisons? | Preprint servers, venue pages | Comparison row, reviewer questions |
| Facts | Training data, size, version, licence of a model or dataset | Model card, dataset card, official documentation | Fact, source, date read, limits |

## Evidence rules

- Read the paper body and the official code at a pinned revision. Abstracts, snippets and summaries are leads.
- Quote at most a short phrase, with file and line, or section and page.
- Cache each source (PDF, code revision, page snapshot) in persistent project storage and record where.
- Keep four absence labels apart: not found (searched, nothing), not disclosed (the source is silent),
  inferred absent (reasoned, unconfirmed), verified absent (full-text or code search confirms).
- Extract reported numbers with their units, denominators and protocol (percentage or fraction, sampled
  candidates or full catalogue, split).
- Describe a method at component level: what is trained, what runs at inference, what information each part
  reads, and under which protocol it was evaluated.
- A searcher's or agent's summary stays a lead until the quote has been checked in the source.
- Pretraining overlap of a model with the study's data is an empirical question: state what was checked and
  its limits.
- Check a provider's name for a model class against the literature's definition before the paper adopts it.

## Practice check

1. Name the decision and its options.
2. List the official implementations and strongest baselines that face the same choice.
3. Read the code path that implements it at a pinned revision; the README is a lead.
4. Record what each does, with file and line.
5. State the recommendation, its precedent, and any departure the project makes.

## Citation ladder and conceptual sources

A citation passes three steps: the source exists; its metadata is correct; the cited claim is present in the
source. Only step three enters the paper. Before a method component is called new, look for its conceptual
source (the same principle in earlier work) and cite it; without one, describe the component as a design
choice.

## Concurrent work

Check at each milestone and before submission. Compare each overlapping work in a table (setting,
information access, claims, overlap). Use it as contrast and as an evaluation caution; it never redefines
the research question, which changes only through the decision log. Record the reviewer questions it creates.

## Implementation feasibility

When the next step is implementation, record for each candidate: code (official or credible, revision,
licence), released checkpoints and their training data, data availability, the protocol it was evaluated
under, and whether its essential component can be reproduced.

## Search routes

- A landscape survey freezes its questions, runs read-only searchers in parallel (one question each), then
  synthesizes with verified citations.
- When a search tool's budget runs out, switch to another search tool or a read-only delegated searcher
  (`workflow-routing`); never report an unverified fact as checked.
- No personal data (email, names, tokens, account identifiers) in any query, header or parameter, whatever an
  API convention suggests.

## Output

One record per question in the project's survey folder: question, decision it serves, sources with revision
and cache location, finding, quote and location, absence label where relevant, confidence, decision impact.
Report to the owner in the project's chat language.
