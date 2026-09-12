---
name: worktree-hygiene
description: Use when creating, auditing, retiring or sweeping git worktrees, whenever `git worktree remove` is being considered, or when a repository has accumulated worktrees holding gitignored experiment artifacts.
argument-hint: "<create | audit | retire | sweep>"
---

# Worktree Hygiene

Worktrees hold tracked code only. Deleting one must never destroy experiment
data, and no removal happens without the four gates below.

## Rules

- **R1 — artifacts live outside worktrees.** Runs, checkpoints, scores,
  datasets and receipts go to a persistent sibling such as `<project>-runs/`.
  Validate the output root with `realpath`; reject anything that resolves
  inside a registered worktree.
- **R2 — register on create, retire through four gates.** Registry line:
  `| <name> | <purpose> | <owner-session> | <created> | <expires> |` in
  `docs/worktree-registry.md` or the project equivalent.
- **R3 — one writer per checkout.** Mark ownership with a session lease file.
  All worktrees share one `.git`; concurrent ref updates, fetch/prune and GC
  collide. External agents that need write access get a full clone.
- **R4 — non-cache scan, read-only.** On create and before retire:

  ```bash
  git ls-files --others --ignored --exclude-standard | \
    grep -v -E '^(\.(venv|venv-oc|uv-cache|pytest_cache|ruff_cache|mypy_cache|omc)|__pycache__|node_modules)/'
  ```

  Cross-check with `find -print0`. Anything outside the committed whitelist
  (`docs/archive-manifests/<date>-cache-whitelist.txt`) is an artifact in the
  wrong place: move it to the archive. Never `git add` it or edit `.gitignore`.
- **Cap:** at most 5 live worktrees including the main checkout. Retire the
  oldest before creating a new one.

## Retire gates — all green before `git worktree remove`

1. **Quiescence** — no open handles or cwd inside the tree
   (`lsof -nP | grep -F '<name>'`, `/proc/*/cwd` scan). Check immediately
   before each removal, not once for a batch.
2. **Reproducibility inventory** — every non-cache ignored file is in the
   archive with a matching SHA-256 or moved there with a manifest entry.
   Covers run data, checkpoints, dataset material, configs / seeds / locks /
   commit hashes, and review artifacts. Test: reproducible from archive plus
   git history without this tree.
3. **Backup** — git bundle regenerated after the manifest commit, with an
   off-device copy.
4. **Refs on origin** — the tree's HEAD is reachable from an origin ref.

## Actions

| Action | Steps |
|---|---|
| `create` | Check cap → `git worktree add ../<project>-wt-<purpose> <branch>` → register → R4 scan (expect zero) |
| `audit` | `git worktree list` → per tree: registry entry, quiescence, ignored count, merged / ahead / behind, expiry → table with recommendation |
| `retire` | Gate 1 → enumerate ignored files → SHA-256 manifest + lstat TSV → same-filesystem `mv` (chmod u+w both ends if needed; append-only move log) → `sha256sum -c`; source remainder zero → commit manifest → bundle + off-device → gate 4 → `git worktree remove` (`--force` only after gates 1–4) → mark retired |
| `sweep` | Freeze the tree list first → `audit` → `retire` each flagged tree → per-tree removal, never batch `rm -rf`; new trees created mid-sweep wait for the next sweep |

Manifest formats: SHA-256 lines `<hash>  <worktree>/<relpath>` (symlinks as
`SYMLINK:<target>  <worktree>/<relpath>`); lstat TSV columns
`worktree relpath type mode size nlink inode device symlink_target symlink_target_exists`,
one real tab-separated column per `stat -c` field.

## Out of scope

Deleting without explicit user authorization; editing `.gitignore`; touching
the main checkout's large ignored trees; replacing project-level R1–R4 rules.

## Report

Worktree count before → after, registry state, trees flagged, archive
verification result, remaining user decisions (backup destination, per-tree
approvals).
