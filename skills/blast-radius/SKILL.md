---
name: blast-radius
description: Use before shipping or approving a change that looks small but is not trusted yet, or when asked "what could this break" — find breakage beyond the diff and prove the one fact the change is safe because of by running real code.
license: MIT
---

# Blast Radius

Adapted from pstack `blast-radius` by Lauren Tan (MIT, `cursor/plugins` at `1ba91fc`; see
`LICENSE`). Find what a change breaks somewhere else before it ships.

Listing callers is not the job; grep does that in a second. The job is the breakage grep
does not show.

## Do not trust your own writeup

A blast-radius writeup that sounds right reads as convincing whether or not it is true. Find
the one or two facts the change's safety depends on and prove them by running code.

### Evidence levels

For each fact the change's safety depends on, push it as far down this list as is cheap, and
say where it stopped:

1. Asserted. Worthless on its own.
2. Cited. A real `file:line`, or the dependency's own source at the pinned version.
3. Reasoned. The failure case walked step by step and shown not to occur.
4. Executed. A script or test that calls the real code and fails loudly if the fact is wrong.
5. Reproduced in the running system: the app, the pipeline, or the experiment.

Level 4 is usually one small script that imports the same library version the project ships
and calls the exact function in question.

## Steps

1. **Read the change.** The diff, the symbols it adds, changes and deletes, and what it now
   does differently, including what the diff does not spell out. Read the commit messages
   and the linked plan or issue.
2. **Find the one fact it is safe because of.** Most risky-looking changes are safe because
   of a single fact, such as "this call only drops cache entries that are already invalid".
   If that fact holds, most risky cases clear at once. Spend the time here, not on a long
   list of possibilities.
3. **Look where grep stops.** Read the source of the library you call, at its pinned version
   and with any local patch. Work out when things run: import time, asynchronous callbacks,
   teardown, worker processes, GPU streams. Follow what a symbol search misses: serialized
   formats, file and column names, a checkpoint or cache another script reads, configuration
   keys, environment variables, feature flags, another language reading the same bytes, code
   several hops downstream. In research code also check seeds, data splits, metric code and
   saved results that downstream tables read.
4. **Be honest about each risk.** Give each a realistic likelihood and cost. Keep confirmed
   risks; list checked-and-cleared ones separately. Cite a real `file:line`; a search that
   finds nothing is still an answer. Never invent a caller or an API.
5. **Prove the one fact.** Write a script or test that runs the real code, run it, and paste
   the output.
6. **For a wide or high-risk change**, ask an independent model from a different family the
   same question, selected through the project's routing policy, and merge only findings you
   can verify. Different models catch different real bugs.

## Hand back

- **What it does**, including the part that is not obvious.
- **The one fact it is safe because of**, the evidence level reached, and the proof. If it
  could not be proven, write "unproven".
- **Risks**: how each breaks, `file:line`, likelihood and cost, and how to check. Paste
  proof for the ones that matter.
- **Cleared**: what was checked and why it is fine.
- **Before merge**: the cheapest test or reproduction that catches the real bug, including
  the script written. Commit it as a regression test when the project's test rules call for
  one.

Strip private paths, credentials and unpublished data before anything goes public.
