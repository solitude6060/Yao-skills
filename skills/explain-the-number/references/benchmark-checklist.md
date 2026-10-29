# Benchmark checklist

Adapted from pstack `benchmark-checklist` by Lauren Tan (MIT, `cursor/plugins` at `1ba91fc`).
Answer each question with evidence from a run, not a guess about the code.

1. **Why not double?** Name the limiter. Profile in a run you do not report, because
   profilers and tracers slow the work. Use CPU per process (`top`, `pidstat`), a runtime
   profiler (`py-spy`, `perf`, `nsys`, `node --cpu-prof`), I/O wait, and syscall counts
   (`strace -c`), then map the hot spot to source. Watch the load generator: if it
   saturates first, you measured the load generator. If a change did not move the number,
   the limiter explains why; find it before calling the change useless.
2. **Was it tuned?** Run every side the way it runs for real: release or optimized builds,
   production flags and environment, batching and transaction settings, thread and pool
   sizes, caches as warm or cold as real use sees them, same versions and data. If one side
   runs on defaults, you compared configurations, not implementations. A limiter that is a
   setting (a commit per row, a debug build, a missing index, `OMP_NUM_THREADS` unset)
   means that side is untuned; tune it and measure again before picking a winner.
3. **Did it break limits?** Do the arithmetic: bytes per second against disk, memory and
   network bandwidth; operations per second times cost per operation against cores; the
   time saved against the time the changed piece took. Removing a piece that takes 10% of
   the run makes the run at most about 11% faster (Amdahl's law). A parallel speedup above
   the core count, or a result past a limit, measured something other than the work: a
   cache, a no-op, or a bug.
4. **Did it error?** Count failures and non-success responses, and check outputs are
   correct, not just present. Rejections are often fast; timeouts and retries are slow. If
   the script does not count errors, add the count.
5. **Does it reproduce?** Run each side at least five times, alternating, so warmup, lazy
   initialization, caches and thermal drift favor neither. Report median and range. When
   the call is close, use a rank-sum test or the harness's own statistics.
6. **Does it matter?** Next to any micro result, measure the end-to-end path a user or
   experiment waits on, with realistic sizes and concurrency, and report the micro result
   as a share of the whole.
7. **Did it even happen?** Confirm the work ran inside the timed region: the kernel
   launched and synchronized, the rows were written, the bytes were read, the result was
   used. Lazy code (unconsumed generators, unawaited promises, results the compiler can
   discard, asynchronous GPU calls without a synchronize) produces numbers for work that
   never happened.
