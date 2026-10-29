# Maintain a formal check

Adapted from pstack `maintain-formal-verification-skill` by Lauren Tan (MIT, `cursor/plugins`
at `1ba91fc`).

When the code changes and the verification does not, the check can keep passing while it
describes code that no longer exists. That pass is the dangerous case, because it looks like
a proof. Use this pass for changes that skipped the project-local verify skill: merges, edits
made without it, and drift across many commits.

## Outcomes

Give each check one outcome, and say which:

- **in sync**: nothing since the last sync alters what the check describes, and it passes.
- **updated**: the verification now describes the new code, and the check passes.
- **bug**: the verification describes the current code, and the code breaks the property.
- **blocked**: the check could not be brought back in line or could not run; say why.

A check can be both updated and bug.

## Edit scope

Edit only the verification: models, harnesses, property files and the verify skill. Never
edit product code unless the user asks. Never weaken a property or model to make it pass.

## Pass

1. **Find the checks.** Find project skills that run a model checker, prover or verifier
   against named code. For each, collect the property, covered code, bounds and assumptions,
   command, and sync commit. Without a recorded sync commit, use the last commit that changed
   the verification files and say so. With no verify skill, stop and use the create mode.
2. **Run it as it is** before changing anything, and record the result. A pass says the old
   description still holds, not that the code is correct.
3. **Read every change to covered code** from the sync commit to now, including renamed,
   split or moved functions and new code that writes the guarded state. Classify each:
   no effect (checked against the model, not the commit message); the verification no longer
   describes the code; the promise changed on purpose (cite the doc comment, test, changelog
   or commit message); or the promise may be broken.
4. **Update from the code, not from the result.** Write the update from the code before
   rerunning. Keep one atomic step in the code as one step in the model. Change a property
   only for an intended promise change, recording old wording, new wording and evidence.
   Keep bounds unless the change makes them wrong; report any reduction.
5. **Rerun and judge.** On a pass, break the new code the way the property guards against
   and confirm the check catches it, then drop the break. On a failure, replay the
   counterexample against the real code step by step: a step that cannot happen means the
   verification is wrong; fix the verification and say what was wrong. If every step can
   happen, it is a bug. Name the introducing commit, retell the counterexample in the code's
   words, and state the harm in one sentence. If a cheap test or reproduction against the
   real code shows the bug, add it to the report as evidence; do not commit it to the
   product code.
6. **Update the verify skill**: covered code, commands, bounds, assumptions and sync commit.
   Set the sync commit to the commit you checked. For a blocked check, do not move it, and
   say so in the report. Follow
   the skill once to confirm its steps still run.

## Report

Per check: outcome and commits read; what changed in the verification and why; rerun result
and the break used to show it can still fail; each bug in plain words; and what remains
uncovered. Say which failures were drift and which were bugs. For a check that passed before
the update and fails after, say the old pass was on a stale description. Put verification
updates in a change of their own, separate from any product fix.
