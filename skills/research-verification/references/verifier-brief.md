# Verifier brief

A verifier knows only what the brief gives it. Give it the evidence and the claims, not the conclusion
you hope it reaches.

## Template

```markdown
# Verification brief: <work item>

Mode: read-only. Do not edit, create or delete files; do not launch runs; do not delegate.

## Work under check
- Task card: <path>
- Owner's requests, quoted: "<request>" (<where recorded>)
- Deliverables: <paths: result rows, report sections, diff range, page build>
- Claims to check, verbatim: <sentence or table cell>, ...

## Evidence
- Raw files: <per-unit outputs, raw responses, logs>
- Generators: <table builder, page builder, paper number generator>
- Contract: <experiment card, admission record>
- Research questions and current priorities: <paths>

## Questions
1. Completeness: list each item of the task card and each quoted request; mark done, partly, not done,
   with the evidence path.
2. Correctness: recompute these numbers from raw files with the stated row filters: <cells>; plus at
   least one cell of your own choice. Read <code paths or diff range> and say whether they compute what
   the record says.
3. Direction: does the work answer the research question it names? Does it follow the current priorities?
   Name any work that answers no question.

## Report format
- Verdict fields: numerical agreement, contract compliance, claim support (values as in the skill).
- Findings table: id, severity, evidence (`file:line` or command and output), impact, proposed repair.
- Access limits: what you could not read or run, and which statements therefore rest on others' records.
```

## Sampling numbers to recompute

- Always the headline number and every number the paper's abstract or conclusion uses.
- One cell chosen at random from each table touched by the work.
- Any cell that changed since the last verification, and any extreme cell (largest gain, lowest
  failure count).
- Recompute with the exact filters (method, configuration, cohort, candidate count, stage) and from the
  per-unit files, not from an aggregate another script wrote. Record the command.

## Paper checks

For a manuscript revision, add:

- every number in the text matches the generator output for the admitted row;
- a difference quoted in the text equals the difference of the printed cells, or one stated rounding rule
  covers all quoted differences;
- sentences, tables, captions and appendix agree with each other (counts, cohort sizes, condition names);
- every reference passes the citation ladder of [research-survey](../../research-survey/SKILL.md): it
  exists, its metadata are correct, and the source contains the cited claim;
- each process statement is literally true for the procedure that was run.

## Sizing

Size the check to the claim: a supporting analysis gets a sampled recomputation; a headline result gets
the answer-path audit as well. A verifier pass is a check of the work, not a new review round for a
document whose review budget is already set by the project's review gate (`triple-review`).

## Independence

- Fresh context: the verifier did not take part in producing the work.
- Another model family for load-bearing claims; record the actual model and session.
- After the verifier finishes, check the working tree for file changes; a plan or read-only mode states
  intent and does not by itself prevent writes.
