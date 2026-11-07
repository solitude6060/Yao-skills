# Execution integrity

A run is valid only if the code and inputs it read are the ones recorded, and only useful if someone
notices when it stops. These rules cover both.

## Immutable snapshots

- A shell reads a script ahead of execution. An edit to a running script, even a same-length
  replacement, may not take effect, so a removed condition can still run. To change a running queue: stop
  the queue script so it launches nothing new, stop the runner, stop any model server by its pid (a
  terminated runner may leave its server holding the accelerator), note the stop in the queue log, then
  launch a new script that lists only the remaining commands.
- Never extract an archive or copy files over inputs a running job reads. Extraction rewrites files in
  place even when the bytes are identical, and a reader can hit a half-written file. Skip files already
  present with an equal checksum, or extract into a staging directory and move into place when no job
  reads those inputs.
- Freeze the prepared inputs of a run (data, candidate lists, configuration) before launch and point the
  run at the frozen copy.

## Launch and wait

```bash
bash run_queue.sh > queue.log 2>&1 &
echo $! > queue.pid
ps -p "$(cat queue.pid)" && head -n 1 queue.log    # confirm the launch
```

Launch with `bash script.sh`, so a missing execute bit cannot fail the launch. Wait on the pid file and
the process state; a zombie (state `Z`) has finished, but `kill -0` still succeeds on it:

```bash
pid=$(cat queue.pid)
while kill -0 "$pid" 2>/dev/null && ! ps -o stat= -p "$pid" | grep -q '^ *Z'; do
  sleep 30
done
```

Waiting for the job's own end line in its log is better still. Never confirm or wait with
`pgrep -f '<command>'`: the pattern also matches the command line of the shell that runs the check, so a
failed launch looks confirmed and a wait never ends.

## Watchdog

Before leaving queues unattended, arm a watchdog that exits, and so notifies, when:

| Condition | Usual cause |
|---|---|
| Accelerator idle and no queue process | Launch failed, queue ended early, waiter missed the end |
| A step ends much sooner than expected | Missing input, permission error, immediate crash |
| Non-zero exit | Any failure |
| The same failure repeats | A daemon retrying one failing job without limit |
| No log progress for a set time | A hang, a stalled transfer, a waiter on a zombie |

On each exit find the root cause, fix it and re-arm. Skipping the failing job is not a fix.

## Retries

Declare the retry count per unit before the run. When it is used up, stop that unit and diagnose; never
loop without limit, and never skip a manifest or identity mismatch to keep the queue moving. Record each
attempt with its cause; the attempt count goes into the run's receipt.

## Progress reports

Report from what the run produced: completed units over total, the last log line and its time, the process
state. An exit status of the launch command, a pid that exists, or a log file that exists is not progress.
Take clock times in records from `date`; never estimate them.

## Generic cases

- A same-length edit to a running queue script did not take effect, and a condition the owner had
  cancelled used accelerator hours.
- An archive extracted over a live input file made a reader fail on a half-written file and stopped a
  queue.
- A waiter on a process that had become a zombie never fired, and an overnight window was lost.
- A launch check matched its own command line, so a failed launch was reported as running.
- A daemon retried one failing job without limit while the rest of the queue waited.
