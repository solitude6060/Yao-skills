---
name: formal-verification
description: Use when concurrency, retries, state machines, parsers or unsafe code need more than tests ("model-check this race", "prove this invariant"), or when code covered by an existing formal check has changed since it was last confirmed.
license: MIT
---

# Formal Verification

Adapted from pstack `create-formal-verification-skill` and
`maintain-formal-verification-skill` by Lauren Tan (MIT, `cursor/plugins` at `1ba91fc`; see
`LICENSE`). A test checks the cases someone thought to write. Formal verification checks
every case in a stated scope: every interleaving in a model, every input up to a bound, or
every input. This skill verifies one property where that matters most and leaves a
project-local skill so the next agent can recheck it.

Two modes: **create** (below) and **maintain** (`references/maintain.md`, for a check whose
covered code changed without a recheck).

## Choose the target from the code

Answer from the codebase; ask the user only what cannot be observed. If the user named an
area or a bug, start there. A good target is a promise the code makes, where a break harms
users or results and tests rarely reach the breaking case: a lock protocol, a work queue, a
retry loop, a state machine, a parser, a reduction across threads or ranks. Choose the
strongest such target, not the easiest one.

## Let the question choose the tool

- Whether events can happen in a bad order: a model checker over a small model of the
  design. TLA+ with TLC is the default in any language.
- Whether the code itself behaves for every input (memory safety, overflow, a data-structure
  invariant): a verifier that runs on the code, such as CBMC or ESBMC for C and C++, Kani for
  Rust, or an SMT-backed verifier.
- No verifier for the language: say so, and test the real code with generated inputs
  (property-based testing), not a hand model of the function.
- A property that must hold at every size: a proof assistant may be needed.

Prefer a tool the repository's developers can install and run, pin its version, and state
why you chose it.

## What makes it good

- **True to the code.** Every part of the model points to code a reviewer can open. What the
  model treats as one atomic step is one atomic step in the code. Names come from the
  repository.
- **Able to fail.** Show each property failing on a broken variant of the code it guards,
  such as a removed lock or a reordered step. A check never seen failing proves nothing.
- **Findings stay findings.** When the current code breaks the property, report the
  counterexample in the code's terms. Do not weaken the property or the model until it
  passes, and do not change product code unless the user asks.
- **Honest about scope.** State what is verified, under which bounds and assumptions, and
  what is left out. A pass covers the model or the bound, not the whole system.
- **Readable without the tool.** State the property and the harm in one plain sentence each.
  Retell a counterexample as a short numbered sequence of steps in the code's words.
- **Cheap to rerun.** One command, a pinned tool version, and a run short enough to use on
  every relevant change. Keep outputs in a persistent project location, not `/tmp`.
- **Kept in step with the code.** Record which files and functions each check covers and
  the commit at which the verification was last confirmed to describe them.

## Generate the project-local skill

Write a skill in the project's skill directory (for Claude Code, `.claude/skills/<area>/`;
mirror or link it where the project's other agents read skills) with frontmatter naming the
area and when to use it. From that skill alone, the next agent must be able to tell whether a
change touches the verified code, run the check, tell a real bug from a modeling error, and
update the verification when a change is intended. Include the coverage record and the sync
commit, and tell the next agent to move the sync commit only after confirming the
verification describes the code at the new commit. Use real commands, paths and names; leave
no placeholders.

For a TLA+ model, a state chart of the reachable behavior helps a reader judge it. pstack's
`statechart` skill renders one from TLC output (upstream, optional; it installs Java and TLC
through mise). Do not copy its commands into the generated skill.

## Prove it before handing off

Follow the generated skill once, as the next agent would, on a scratch change that breaks
the property in the real code. It must catch the break. Then drop the scratch change and
confirm the check is back where it started: passing, or failing only on the findings you
will report. If the skill misses the break or a step does not run, fix the skill or the
verification, not the scratch change.

## Hand off

Report what was verified, the tool and why, the bounds, what the check found in plain words,
how to run it, and what it does not cover. Commit the verification and the generated skill
in a change separate from any product fix.
