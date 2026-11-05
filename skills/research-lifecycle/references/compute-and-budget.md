# Compute, paid APIs, storage and preservation

Compute, money and disk are scheduled resources of the study. The per-batch budget (throughput, cost
categories, low-cost trial tier) is planned in `experiment-planning`; launch, waiting and watchdog mechanics are
in `experiment-contract` ([execution-integrity.md](../../experiment-contract/references/execution-integrity.md)).
This file holds the project-level rules.

## Accelerators

- An accelerator does not idle while authorized work is queued. Before an unattended period (overnight, a
  long meeting), queue the next authorized jobs and arm a watchdog. On every watchdog exit, find the root
  cause and fix it; skipping the job leaves the cause in place.
- Run jobs in parallel when device memory allows. Each job declares its memory. If the host has a shared
  device lock, hold it in shared mode (a model server that needs the whole device holds it exclusively);
  otherwise check free memory on the whole device before each launch.
- Estimate runtime from measured throughput (a short run of the real configuration) before promising a date.
- Order the queue by decision value: a run whose result would make other runs unnecessary goes first.

Generic cases: two queues sat idle for hours overnight because a relaunch failed on a file permission and the
launch check matched its own command line; a waiter on a finished but unreaped process lost most of a night.

## Shared or borrowed hardware

| Rule | Failure it prevents |
|---|---|
| Agree with the lender where weights, environments, caches and outputs live; write nothing large elsewhere | Filling the lender's system disk |
| Cap memory on whole-device use minus the pre-start baseline, and cap the server itself (allocator or utilization limit) | A per-process guard that never fires because the container does not report per-process memory |
| Announce sustained full load to the owner before starting | Power or memory trouble for the lender's own work on the same device |
| Check free memory and other users' processes before each run; never touch another project's processes | Crashing someone else's job |
| A deletion script first proves which host it runs on | Deleting originals on a host that uses the same paths as the borrowed copy |

Generic case: a model server briefly exceeded the agreed memory cap on a borrowed device because the guard
read per-process memory, which the container reported as unavailable.

## Paid APIs

1. Before each run, estimate tokens and cost from a measured rate on the same request form, and compare the
   estimate with the remaining balance.
2. Keep a ledger: run, date, requests, input and output tokens, estimated cost, actual charge, balance, with
   a per-run cap and a cumulative cap. Write the entry before the spending, and reconcile it with the
   provider's record afterwards.
3. Run whole cells only. A cell whose estimate exceeds the remaining balance does not start; ask the owner
   before exceeding the balance.
4. Pin the model version and record the version or model identifier the service returns with every
   response. Switching to a newer version is an owner decision, supported by a small paired check.
5. Record cost by category: preparation, selection, inference, retries, refresh. A per-request cost claim
   excludes one-off preparation and states how often refresh recurs.

Generic cases: runs were planned against a balance only slightly above their estimate; when the provider
released a newer version, the owner kept the earlier one so that results stayed comparable.

## Storage hygiene

- Keep the selected checkpoint of each configuration and the raw per-unit scores of admitted runs.
- Grid checkpoints for every setting and raw scores saved at every epoch are moved to persistent archive
  storage (preservation rules below) once selection is recorded and nothing reads them; check readers first.
- Check free space before a batch; a full disk stops every queue on the host.

Generic case: per-setting checkpoints of a closed-form model and per-epoch raw scores in a text format filled
the disk and stopped the queues.

## Preservation

1. Back up before cleanup, checkout replacement or retirement: tracked, untracked and ignored material,
   environments, and the targets of symlinks (copying a link does not preserve its target).
2. Write one archive per unit with a per-file checksum manifest; verify each archive by reading it back from
   the destination.
3. After any network or storage fault during a backup, re-verify every archive written around the fault.
4. Delete locally only after every unit verifies and the owner confirms the list. Retire working copies
   through the recorded gates of `worktree-hygiene`.
5. Keep private backups private and persistent; record restore instructions next to the manifest.

Generic cases: a backup to a network share stalled for a long period after a connection fault and had to be
resumed; one archive was found corrupted only at read-back verification.
