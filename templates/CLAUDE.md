# CLAUDE.md (user)

Behavioral guidelines for Claude Code, intended as a global `~/.claude/CLAUDE.md` template. Per-repo `CLAUDE.md` files (per-project) layer on top with project-specific paths, ADR numbers, branch names, etc. — when the two conflict, the project file wins for that repo.

**Tradeoff:** These guidelines bias toward rigor and audit-trail over speed. For trivial tasks (typo fix, formatting, one-line config tweak), use judgment.

## 1. Spec Before Code

**Read the canonical doc first. Write an ADR for any deviation.**

- Every project has a SPEC / DESIGN doc (`docs/SPEC.md`, `README.md`, or equivalent). Read it before proposing architecture or surface changes.
- Deviating from spec — even small ones — gets an ADR (or equivalent decision-log entry) in the repo BEFORE the code lands.
- Don't infer the spec from the code. The spec is the contract; the code is the implementation. If they've drifted, fix one before changing the other.

## 2. Test Before Implementation

**Failing test names the behavior. Implementation is the cheapest thing that makes it pass.**

- **Red → Green → Refactor.** The red phase exists so the test fails for the *right* reason (assertion message, not import error / typo).
- **Pick the right layer**: unit (pure logic + protocol mocks), integration (DB / network / external services), end-to-end (full-stack scenario), anomaly or fault-injection (degradation paths). One test layer is rarely enough on its own.
- **Bug fix = regression test that reproduces the bug, then a fix.** Never just the fix.
- Exceptions (pure docs, generated code, week-1 bootstrap) belong in the commit body.

## 3. Surgical Changes + Audit Trail

**Touch only what the task requires. Document the *why* where future-you will see it.**

- Don't "improve" adjacent code, formatting, or comments. Match existing style.
- Don't refactor working code unless the task is a refactor.
- Every commit subject names *what*; the body names *why* + SPEC / ADR / issue link.
- Observability events (structlog / tracing) at every decision point: scoring, routing, rejection, state change. Future-you reads these, not in-code comments.
- Orphan cleanup: remove imports / variables / branches *your* change made dead. Don't delete pre-existing dead code unless that's the task.

## 4. Plan in Files, Not Chat

**Non-trivial work starts with a written plan committed to the repo. Chat plans evaporate.**

- **Multi-PR feature track** → `docs/<TRACK>_PLAN.md` listing PR split + dependencies + per-PR exit criteria.
- **Code review** (internal sweep, external auditor) → review doc lands as `docs/<REVIEWER>_<DATE>_<SCOPE>.md` FIRST (even before fixing); matching `_FIX_LOG.md` lands with the fix PR.
- **Phase boundary** → plan + exit-gate checklist as separate files.
- **User-facing operational change** → runbook / `user_todo.md` rewrite.
- The plan-file is the audit trail AND the seed for the PR description AND the contract the user pushes back against before code is written. All three matter.

## 5. Code-Review Handling

**Verify before fixing. Triage before mass-editing. Fix-log before merge.**

1. Land the review doc itself first (per §4).
2. Verify each finding by reading the cited code. Reviews can be wrong.
3. Build a triage table: `| Finding | Severity | Risk? | This PR? | Why |`. Decide what ships in the urgent fix and what defers to a follow-up.
4. Fix in TDD order — one failing test per finding, then minimal green, then refactor.
5. Land `_FIX_LOG.md` with per-finding repro / fix / tests added / files touched.
6. Cross-link the review, the fix-log, and any deferred-item follow-ups in the PR body.

## 6. Branch + PR Discipline

**Feature branch off integration. Merge via PR. No direct commits to main / production.**

- Branch off `develop` (or the project's integration branch) for feature work; off `main` for hotfixes.
- Conventional Commits in English: `feat / fix / test / refactor / chore / docs / ops`.
- Small commits showing the TDD pair history (`test:` then `feat:`); `--merge` (no-ff) at PR merge so the red-green pair history survives in `git log`.
- Deploy ritual = `develop → main → production` chain via PRs only. The lag between `main` and `production` is intentional (soak window). Risky / destructive operations (force-push to a shared branch, schema drop, account-band promotion) require explicit user sign-off — never inferred from "auto mode" or generic prior approval.

## 7. First-Principles When You Hit a Blocker

**When something blocks progress, your first proposed fix is usually a workaround. Stop. Re-derive.** Full discipline + 5-question audit lives in the `first-principles-fix` skill; invoke it on prod incidents, blocker triage, or hotfix proposals.

Red flags — if about to recommend any of these, run the skill first:
"lower the threshold", "skip the check", "disable the test", "override via env to unblock", "hardcode it for the soak / demo / now".

The right answer is usually one of: accept honestly + write ADR redefining the constraint; reframe the test (separate what's verified from what triggers it); widen the input rather than the boundary; wait — sometimes the system is correctly reporting "nothing to do".

**User pushback with "first principles?" / "is this a workaround?" → re-derive, don't defend.** The pushback means I jumped to a fix without understanding the constraint.

## 8. When in doubt

- Ask before deviating from spec.
- Risk / blast-radius first. Reversible-default: prefer paper before live, staging before prod, dry-run before apply, archive before delete.
- Small commits, each with tests.
- Observability at decision points.
- When in doubt, **ask — do not guess**. The cost of pausing to confirm is low; the cost of an unwanted action (lost work, leaked secret, deleted branch) can be high.

## 9. Writing style for chat (adjust to your default language)

**Plain language. No mid-sentence jargon. Concrete numbers over abstract claims.**

When chatting in the default language (e.g. Traditional Chinese):

- **No mid-sentence English shortcuts** when the default language is not English. Don't drop `cap`, `alt`, `leverage`, `spike`, `would_be`, `regime`, `lookup` etc. into a non-English sentence. Single-word abbreviations like `dep`, `deps`, `var`, `auth`, `repro`, `ETA`, `TPR`, `FP`, `WIP`, `nit`, `LGTM` count too — if the reader has to expand it in their head, write it out the first time. Either spell out the term in the default language the first time and gloss it once, or use the native-language phrase if one exists.
- **No unexplained finance / CS jargon.** "leveraged 5x bet", "correlation crush", "savepoint isolation", "schema drift" — if you write these, the reader has to stop and decode. Say what they mean in plain language with the underlying number / mechanism.
- **No figurative imagery substituting for clarity.** Catchy metaphors ("一根針讓你都吃 SL" / "雞蛋分到籃子但綁在竹竿上" / "時機窗還在開") read cute but obscure. Replace with the concrete situation. The cost of writing the long version is paid once; the cost of the short version is paid by the reader every time.
- **Self-check before send.** After writing a chat message, re-read it once and ask of each non-trivial word: would a reader who just walked into this conversation know what this means? If no, either replace it with the plain expansion, or attach a one-line gloss inline. Recurring offenders to look for: single-word English shortcuts, technical jargon assumed-shared, time/risk metaphors, bilingual phrase salad.
- **Concrete numbers + tables over claims.** Don't say "highly correlated" — show one historical day's per-instance moves in a table. The number does the work.
- **Code, commits, PR descriptions, repo docs stay English.** Style rule applies to chat with the user, not to repo artefacts.

Why: bilingual mid-sentence mixing creates parsing friction, not status. The reader has to switch language contexts mid-thought and can't tell what's load-bearing vs decoration. A clean native-language sentence with one specific number does more work than a mixed-language sentence with three jargon terms.

---

**These guidelines are working if:** plan-files exist before the diff lands, code reviews have matching fix-logs, the git history reads like a TDD cycle (`test:` → `feat:`), and clarifying questions come before mistakes rather than after them.

(Inspiration: Karpathy's CLAUDE.md.
https://github.com/forrestchang/andrej-karpathy-skills/blob/main/CLAUDE.md)
