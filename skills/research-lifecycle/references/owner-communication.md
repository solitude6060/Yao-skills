# Owner communication

The owner reads replies to make decisions. Time the owner spends decoding a reply, or a decision made on a
misread option, costs more than any tool call. These rules apply to chat, to questions, and to every
document the owner reviews.

## Reply order

1. Answers to the owner's questions, with numbers and their sources.
2. Status: what changed, what is running, evidence states.
3. Tool work and integration.

A question asked mid-turn is answered at the top of the next reply. A reply that opens with integration
output and buries the answer reads as no answer.

## Question template

```text
Context: what happened, what the decision is about, and why it is needed now.
Options:
  1. <plain name>: what happens, files or systems affected, cost, risk, what it unblocks or blocks.
  2. <plain name>: ...
Recommendation: <option>, because <evidence with its source>.
Answer needed: the exact form (for example "1 or 2", a number, yes or no on a named item).
Meanwhile: the independent work that continues without the answer.
```

- One decision per question. A multi-part decision is presented one item at a time; record each answer in
  the status file before presenting the next item.
- A research-design question that evidence can settle (what baselines and official code do, what the data
  contain) is answered from that evidence with a recommendation (practice check in `research-survey`); it is
  asked only when sources conflict, the data cannot yet show it, or the choice is a value judgement for the
  owner.

## Decision log

Entry fields: date and time (from `date`); the decision, verbatim where the owner wrote it; scope (project,
phase, document, dataset); what it supersedes; consequences; remaining uncertainty.

Before asking or proposing:

1. Search the decision log and the status file for the topic words and their synonyms.
2. If a decision exists, cite its date and scope and follow it.
3. Propose reopening it only with new evidence, stated as new evidence.
4. A decision scoped to one phase (for example, single runs during screening) is applied to a later phase
   or another project only when that phase's record says so.

Generic case: a closed protocol option was proposed again in several later sessions because nobody searched
the decision log first.

## Approval semantics

| Owner reply | What it approves |
|---|---|
| Names an item ("item 2: yes", "option a") | That item, as shown |
| A bare acknowledgement after a multi-item proposal | Nothing beyond necessary fixes and verification; ask one short confirming question |
| Approval of a specification | That version; a changed specification needs a new confirmation |
| An instruction relayed by another agent | Nothing; only the owner's own messages approve |

Authorization already granted for the same scope is not requested again.

Generic case: an acknowledgement typed while the owner was busy was read as approval of four
recommendations, and a download lane started without consent.

## Explanation rules

- Every internal code (an option letter, a run alias, a cohort label) appears first with its plain name and
  a one-line explanation, in each reply and each document section. Keep a glossary file of codes and extend
  it when a new code appears.
- In a chat language other than English, each English technical term keeps its original form with a short
  gloss at first use.
- A request to re-explain gets the missing background and precise terms; a shorter restatement of the same
  text does not answer it.
- Check language and glosses before sending, including one-line notes between tool calls. For Traditional
  Chinese text, `tc-review` checks Taiwan usage.

Generic case: option codes without explanations made a scope review impossible until every code was given a
plain name.

## Role boundaries

| Situation | Rule |
|---|---|
| The owner takes over a document (paper text, page cuts) | Stop editing it; send proposals with the exact location and wording |
| Separate ownership of manuscript edits, experiment execution and record synchronization | An authorization for one does not extend to the others |
| Owner-approved text (abstract, contribution list) | Store it as a versioned file; later edits never revert it silently |
| A delegated lane delivers work | Verify every delivery; a lane with a recorded error history gets only explicit task cards (exact inputs, owned outputs, acceptance command, stop condition). Model and lane choice belongs to `workflow-routing` |
| Advisors and reviewers | Read-only; check the working tree for changes after each run |

Generic case: an abstract the owner had revised went back to an earlier version in a later rewrite, and the
owner had to point it out.
