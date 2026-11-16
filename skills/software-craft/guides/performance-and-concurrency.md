# Performance and concurrency

This guide covers two jobs: making code faster without guessing, and making code that runs on several threads correct. The most important idea is the same for both. Let evidence decide: measure before and after every speed change, and keep shared mutable state small, private and guarded by well-known library primitives instead of trusting that a race will not happen.

**Read this when:** a change aims to make code faster, someone reports that code is slow, a loop calls a database, service or disk once per item, a reviewer asks for proof of a speed gain, code adds a thread, pool, queue or lock, several threads read or write the same field or collection, a background worker must shut down cleanly, or a threaded test fails only now and then.

**Entry IDs** such as `WELC-T12` point to `../books/<book>/techniques.md` (T) or `principles.md` (P);
the prefix table is in [SKILL.md](../SKILL.md).

## Contents

- [Rules: speed](#rules-speed)
- [Rules: shared state and locks](#rules-shared-state-and-locks)
- [Rules: threads, pools and queues](#rules-threads-pools-and-queues)
- [Rules: testing concurrent code](#rules-testing-concurrent-code)
- [Playbooks](#playbooks)
- [Where the books disagree](#where-the-books-disagree)
- [Review checklist](#review-checklist)
- [More entries in this area](#more-entries-in-this-area)

Timeouts, circuit breakers, load shedding and bulkheads are covered in [production reliability](production-reliability.md). Transactions, isolation levels and races inside a database are covered in [data systems](data-systems.md). Immutable values and parallel combinators are covered in [functional style](functional-style.md).

## Rules: speed

### 1. Measure before changing code for speed

Programmers guess badly about where time goes, so a profiler or benchmark, not intuition, decides whether and where to tune. Editing code that is not the hot spot makes it harder to read and buys nothing. Profile at several input sizes before you invest in tuning. [POSD-T48, PP-T46, REF-T87]

- **Do:** Before any edit for speed, record a baseline from a profiler or benchmark that names the hot spot. When a design choice depends on what an operation costs, benchmark that operation first. For capacity and scaling decisions, record real throughput, peaks and percentile latency, and benchmark on your own workload at larger data volumes before adding machines. [POSD-T48, PP-T46, DDIA-P7]
- **Not when:** A change that also makes the system simpler needs no measured speed gain to stay. A significant measured slowdown can justify undoing an earlier refactoring. Averages are still the right figure when you estimate throughput limits. [POSD-T48, REF-T87, DDIA-P7]
- **Check:** The PR names the profiler or benchmark output that identified the hot spot and gives its baseline numbers.

### 2. Ship the measurement with every optimization

Reviewers have to judge whether an optimization is worth its cost, and a measurement is the evidence they can check. A change that shows no measured gain should be backed out. [SWE-T64, POSD-T48, REF-T87]

- **Do:** Include before and after results, or a benchmark test, in the change. Put the speed change in its own commit, apart from restructuring and behavior changes. Remember that a pure restructuring can change performance too, so a restructuring gets its own performance check. Back out a speed change that measures no better than the baseline. [SWE-T64, REF-T87, WELC-P3, POSD-T48]
- **Not when:** A change that also simplifies the system can stay without a measured gain. [POSD-T48]
- **Check:** The optimization commit holds benchmark results or benchmark tests with baseline and post-change numbers, and no unrelated restructuring.

### 3. Estimate how cost grows with the input

A rough growth estimate flags a risk early, and measurement then confirms or dismisses it. Multiply the bounds of nested loops over the input to see quadratic cost, and make the same estimate for recursion over input of variable size. [PP-T45, PP-T46]

- **Do:** For each loop inside another loop over input, and for each recursion over a collection, write down how the work grows with input size. Treat a quadratic or worse estimate on input that can grow as a risk to measure under rule 1.
- **Check:** Nested loops and recursion over collections in the diff have been reviewed for quadratic growth, and the risky ones have a measurement.

### 4. Keep per-item remote calls, disk access and allocations off frequent paths

Network round trips, disk access and memory allocation cost far more than ordinary computation, so on a path that runs once per item or once per request they dominate the total time. [POSD-T49]

- **Do:** Restructure a frequent path so that it does not make a network call or disk access for each item. Avoid allocating per item there, and store array elements inline rather than as pointers to separate objects. If you replace many small queries with one larger one that can return rows without limit, add a row limit or paging to it (RI-T68) and see [data systems](data-systems.md). Any remote call that remains needs a timeout. [POSD-T49, RI-T68, RI-T22]
- **Not when:** A path that runs rarely and does no I/O keeps the simpler code. When you cannot tell whether a path runs often enough to matter, measure it first. [POSD-T49]
- **Check:** Loops and per-request handlers in the diff make no per-item remote call, disk access or allocation, unless the path runs rarely and does no I/O.

### 5. Fix the algorithm or data structure before tuning details

Once measurement has found the slow component, change its data structure or algorithm before you tune constants. A fundamental fix removes the work, while tuning only makes the same work slightly cheaper. [POSD-T50]

- **Do:** Look first for a different data structure or algorithm for the slow component. Tune constants or micro-details only when no such change exists, and redesign around the common case only as a last step.
- **Not when:** No fundamental fix exists. Then a redesign around the common case is the remaining option, and POSD expects that to be needed rarely. [POSD-T50]
- **Check:** The speed fix changes a data structure or algorithm, or the PR explains why no such change exists.

### 6. Test rare special cases once at the start of a hot path

Each check for a rare condition inside the common path adds work to every call. On a hot path with several rare conditions that the normal path cannot handle safely, fold them into one value, test it once at the top, and send the rare cases to separate code. [POSD-T51]

- **Do:** Start the hot function with a single guard over the combined special-case value. Keep the common path after it free of further special-case checks.
- **Not when:** Where special cases matter little for speed, structure them for simplicity instead, and let the normal path absorb empty or absent states without extra checks. [POSD-T51, POSD-T30]
- **Check:** The hot function begins with one guard, and the rare cases branch to separate code.

### 7. Use the library's sort and search routines

Library sort and search routines are tested and tuned, so a custom version rarely beats them. Hand-written code that does what a library call already does should become that call. [PP-T47, REF-T56]

- **Do:** Call the standard library to sort or search. Write a custom routine only when a benchmark shows that the library call is the bottleneck and that your version is faster.
- **Not when:** Beating a library routine usually takes substantial effort, so benchmark before you invest in a custom one. Keep the hand-written code when the library call reads poorly at the call site or the resemblance is only coincidental. [PP-T47, REF-T56]
- **Check:** Every custom sort or search routine in the diff is justified by a cited benchmark.

### 8. Add a cache or snapshot only for a measured cost

Computing a value from its sources keeps it from going stale, so derive by default. Cache a derived value only when it is expensive and read often, keep the cache private, and give every cache an explicit size bound so it cannot grow until memory runs out. A query that caches its result still counts as free of side effects. [PP-T09, REF-T28, RI-P4, DDD-T30]

- **Do:** Show the cost first, for example with a benchmark at realistic data volumes, as Learning DDD asks before adding aggregate snapshots. Then add a private cache with a configured bound. [POSD-T48, DDD-T30, RI-P4, PP-T09]
- **Not when:** Aggregates that stay far below the event counts where replay gets slow need no snapshots. [DDD-T30]
- **Check:** Each new cache in the diff cites a measured cost, is private to its owner, and sets a size bound in its constructor.

### 9. Measure the latency that users actually see

A median can look fine while the slowest requests stay bad, and measuring only your own processing time leaves out the time a request waits in a queue. Track high percentiles, measure residence time from the moment a request reaches the server, and compute durations from a monotonic clock, because wall clocks can jump. [DDIA-T09, RI-T75, DDIA-T41, DDIA-P7]

- **Do:** Report p95, p99 and p999 beside the median. Start latency timers when the request arrives at the server socket. Read elapsed time from a monotonic clock API. More on service-level monitoring is in [production reliability](production-reliability.md).
- **Not when:** Stop at the 99.9th percentile unless a 99.99th percentile goal clearly pays for itself. Use the wall clock when users need a date or time of day. Averages still suit throughput estimates. [DDIA-T09, DDIA-T41, DDIA-P7]
- **Check:** Latency metrics in the diff include percentile series above the median, start at socket arrival, and never subtract wall-clock readings.

## Rules: shared state and locks

### 10. Keep thread, queue and lock calls out of business logic

Business rules that contain no thread, queue or lock calls can run and be tested without starting a thread or a process. Put that machinery in small boundary functions, and pass threaded collaborators in as parameters so tests can swap them. [CC-T55, CC-T12]

- **Do:** Keep queue, thread, process and lock calls in small boundary functions or classes, away from policy classes. Keep executor and thread types out of public signatures. Where application code needs operating-system threads and timers, as in embedded code, reach them through an abstraction layer. [CC-T55, FPS-P4, CA-T73]
- **Check:** Policy modules in the diff contain no queue, thread, process, executor or lock calls, and public signatures name no executor or thread types.

### 11. Confine shared mutable state to a few guarded writers

Limiting which code writes shared data limits where races can happen. Keep every field or collection that more than one thread can reach private, and let only a few guarded methods write it. [CC-T57, CA-T09, REF-P5]

- **Do:** Make shared fields private, route every write to them through one update function or a few guarded methods, and keep the number of shared mutable variables small and confined to named components. Keep the variables of a context object that many components share immutable. [CC-T57, CA-T09, REF-P5, POSD-T44]
- **Not when:** Some shared resources, such as database connections, often cannot be removed, so guard them rather than trying to eliminate the sharing. Immutable data needs no guard, and data that only one small function uses may stay local. [CC-T57, REF-P5]
- **Check:** Every field reachable from more than one thread is private and written only from a few guarded methods.

### 12. Use thread-safe library types for shared data

Plain collections and counters can lose updates or corrupt their contents when threads use them at once. A small set of well-known primitives used in known ways is safer than concurrency code you build yourself. [CC-T58, RI-T19]

- **Do:** Use concurrent collections and atomic counters for data that several threads read or write. Build pools, queues and other shared concurrency code from library classes, not home-made ones. [CC-T58, RI-T19]
- **Check:** Shared collections and counters use concurrent or atomic types, and the diff adds no home-built pool or queue.

### 13. Hold one lock across a multi-step sequence

Each method on a shared object can be thread safe while a sequence of them is not, because another thread can run between two separately locked calls and break the sequence. [CC-T56]

- **Do:** When a client must call several methods on one shared object in order, run the whole sequence under one lock. If you can change the shared object, give it one method that performs the sequence under its own lock, so clients cannot get the order wrong. For a read-modify-write cycle against a data store, the guard is an atomic operation, a lock, a conditional write or lost-update detection, as described in [data systems](data-systems.md). [CC-T56, DDIA-T36]
- **Check:** Each multi-step operation on a shared object runs inside one lock scope or one locking method.

```java
// Broken: each call is synchronized, but another thread can run between them.
if (!registry.containsKey(id)) registry.put(id, build(id));

// One lock across the whole check-then-act sequence.
synchronized (registry) {
    if (!registry.containsKey(id)) {
        registry.put(id, build(id));   // build() is local work, no remote call
    }
}
```

### 14. Keep remote calls out of locked sections

A thread that holds a lock while it waits on a remote system keeps every other thread that wants the lock blocked for the whole call. This matters most in caches, registries and circuit breakers that call out. [RI-T20, RI-P2]

- **Do:** Make the remote call with no lock held, and lock only around the in-memory reads and writes. Do not let one lock serialize every call that passes through a circuit breaker. Give each lock wait an explicit time limit. [RI-T20, RI-P2]
- **Check:** No synchronized method or lock scope in the diff wraps a remote call, breaker state does not serialize calls, and lock waits pass a timeout.

```java
Value lookup(Key k) {
    synchronized (this) {                       // in-memory only
        Value cached = entries.get(k);
        if (cached != null) return cached;
    }
    Value fresh = remote.fetch(k, FETCH_TIMEOUT); // no lock held here
    synchronized (this) {
        entries.putIfAbsent(k, fresh);
        return entries.get(k);
    }
}
```

### 15. Put a bounded queue in front of an unavoidable shared resource

When callers must share a resource that cannot be avoided, a queue or buffer between them and the resource absorbs bursts, so the resource sees steadier demand. The queue itself needs a finite bound, because unbounded growth eventually exhausts memory or pushes response times past target. [RI-T21, RI-P4]

- **Do:** Route calls to the shared resource through a queue or buffering component, and give that queue an explicit size limit. What to do when the queue is full is covered in [production reliability](production-reliability.md). [RI-T21, RI-P4, RI-T37]
- **Check:** Calls to the shared resource pass through a queue or buffer whose constructor sets a bound.

### 16. Document which thread calls each handler

A reader cannot tell from an event handler's code when it fires or which thread runs it unless its interface comment says so. [POSD-T56]

- **Do:** In each event handler's interface comment, name the trigger and the thread that invokes it.
- **Check:** Handler interface comments in the diff name the trigger and the calling thread.

## Rules: threads, pools and queues

### 17. Give every blocked thread a way to stop

A thread that cannot stop hangs the process at exit and loses the work it held. Every thread that can block, such as a parent waiting on its children or a consumer waiting on a producer, needs a path to receive a stop signal and finish. [CC-T59, RI-T33]

- **Do:** Give each waiting thread a stop signal it can see while blocked, and make producers and consumers stop together. Handle termination signals so the process finishes in-flight work before it exits. [CC-T59, RI-T33]
- **Check:** A test stops all threads and confirms that shutdown completes, and shutdown code handles termination signals.

### 18. Keep pool tasks from waiting on their own pool

On a bounded pool, a task that submits another task to the same pool and then blocks on its result can leave every thread waiting on the others, which is a deadlock. Run blocking outbound calls on an executor separate from the request threads, with a caller-side timeout, so the request thread can time out and reply while the outbound call is still blocked. [FPS-T40, RI-T29, RI-T13]

- **Do:** Do not block inside a pool task on a future submitted to the same executor. Run blocking outbound or library calls on an executor separate from the request-handling threads, with a caller-side timeout. Give every checkout from a pool a maximum wait and handle the timeout path. [FPS-T40, RI-T29, RI-T13]
- **Not when:** A pool that grows without bound cannot deadlock this way. Be aware that wrapping outbound calls this way can grow into a reactive wrapper around a whole client library. [FPS-T40, RI-T29]
- **Check:** No task body calls a blocking get on a future from its own executor, blocking outbound calls run on a separate executor with a timeout, and pool checkouts pass a maximum wait.

## Rules: testing concurrent code

### 19. Treat every intermittent failure as a probable threading defect

A failure that happens once in many runs, or passes on a rerun, is most likely a race, and calling it a one-off lets it come back under load. Passing unit tests alone do not show that concurrent code is correct. [CC-T60, TDD-P8]

- **Do:** Investigate the failure as a threading defect. Do not mark the test as skipped, retried or one-off. [CC-T60]
- **Not when:** Clean Code lets a slow or broken test be disabled with a stated reason, but that exception does not cover an intermittent threaded test. Any test that is skipped needs an open ticket explaining why. [CC-T69, PP-T73]
- **Check:** The diff adds no skip, retry or flaky marker to a threaded test.

### 20. Vary thread timing in tests through one jiggle hook

Rare thread orderings seldom appear in normal test runs, and random delays at the points where threads interleave can expose them. Calls to sleep or yield left in production code slow it down, so route them through one swappable hook. [CC-T61, SWE-T09]

- **Do:** Define one hook and call it at each interleaving point. Bind it to a no-op in production and to a random sleep or yield in tests, and run those tests many times. Control thread scheduling and the clock in tests rather than leaving them to chance. Where code checks a lease before acting, have tests inject a pause between the check and the action. [CC-T61, SWE-T09, DDIA-T42]
- **Not when:** Manual yield or sleep calls must not stay in production code, because they slow it down. [CC-T61]
- **Check:** Production binds the hook to a no-op, and the threaded tests repeat with random timing.

```java
interface Jiggle { void point(); }

Jiggle production = () -> {};                // no cost outside tests
Jiggle randomized = () -> {                  // test binding
    if (rnd.nextBoolean()) Thread.yield();
    else sleepQuietly(rnd.nextInt(3));
};

// In the threaded code, at each place where threads interleave:
jiggle.point();
```

### 21. Wait for asynchronous work with bounded polls, not sleeps

A fixed sleep in a test is either too long, which slows the suite, or too short, which makes it flaky. Poll for the expected state with a timeout, or subscribe to an event that signals completion. [SWE-T55, SWE-T06]

- **Do:** Replace each fixed sleep in a test with a bounded poll or an event wait. In production code, remove sleeps and retries that trial and error added, unless a comment or a test justifies each one. [SWE-T55, PP-T66]
- **Check:** Test code contains no fixed sleep calls, and every remaining sleep or retry in production code has a documented reason or a test that needs it.

### 22. Trace timing bugs in one parseable format

Timing and concurrency bugs require following state over time, and one uniform format lets a script do that. Give every trace message the same fixed prefix and labeled fields. More on investigating defects is in [debugging](debugging.md). [PP-T60]

- **Do:** Use one trace format with a fixed prefix and labeled fields for any bug that depends on timing, concurrency or event order.
- **Check:** Trace calls added for the investigation share one format.

## Playbooks

### When someone says the code is slow

1. Reproduce the slowness with a profiler or benchmark at several input sizes, and record the baseline. [PP-T46, POSD-T48, REF-T87]
2. If the complaint comes from users, look at percentile latency and residence time, not means or processing time alone. [DDIA-T09, RI-T75]
3. At the hot spot, estimate growth by multiplying nested loop bounds and checking recursion over the input. [PP-T45]
4. Look for per-item network calls, disk access and allocations on the hot path. [POSD-T49]
5. Prefer a different data structure or algorithm, use library sort and search routines, and tune constants only if no fundamental fix exists. [POSD-T50, PP-T47]
6. If the code is messy, restructure it first in separate behavior-preserving commits, as the [refactoring](refactoring.md) guide describes, and only then tune. [REF-T87]
7. Measure again. Back out the change if it shows no gain, unless it also made the system simpler. [POSD-T48]
8. Commit the speed change on its own, with benchmark results or a benchmark test. [SWE-T64, REF-T87]

### When a loop calls a database, service or disk for each item

1. Decide whether the path runs per item or per request, or performs I/O. If so, the rule against per-item calls applies. If it runs rarely and does no I/O, keep the simpler code. [POSD-T49]
2. Estimate how the number of calls grows with the input. [PP-T45]
3. Restructure the path so that it makes no remote call or disk access per item, and add a row limit or paging to any combined query that can return rows without limit. [POSD-T49, RI-T68]
4. Give any remaining remote call an explicit timeout, and keep it outside every lock. [RI-T22, RI-T20]
5. Measure before and after, and put the numbers in the change. [POSD-T48, SWE-T64]

### When you add state that several threads share

1. Keep the business logic free of thread, queue and lock calls, and put the threading in a boundary layer. [CC-T55]
2. Make the shared fields private and limit writes to a few guarded methods. [CC-T57, CA-T09]
3. Use concurrent collections and atomic counters from the library. [CC-T58, RI-T19]
4. List every multi-step sequence on the shared object, and put each under one lock or one locking method. [CC-T56]
5. Confirm that no lock is held during a remote call, and that every lock wait has a time limit. [RI-T20, RI-P2]
6. If extraction promoted locals to fields, check that those fields are not static and shared by threads, and use per-caller instances or locks if they are. [CC-T35, CC-T40]
7. Document which thread calls each event handler that touches the state. [POSD-T56]
8. Add tests that run repeatedly with the jiggle hook bound to random timing. [CC-T61]

### When you add a background thread, worker or consumer

1. Build it from a library pool or queue, not a home-made one. [RI-T19]
2. Put a bounded queue in front of any shared resource it feeds. [RI-T21, RI-P4]
3. Run blocking outbound calls on their own executor with a timeout, and give pool checkouts a maximum wait. [RI-T29, RI-T13]
4. Make sure no task blocks on a future it submitted to its own pool. [FPS-T40]
5. Give every blocking wait a stop path, and handle termination signals so in-flight work finishes. [CC-T59, RI-T33]
6. Write a test that stops all threads and confirms shutdown completes, waiting with bounded polls rather than sleeps. [CC-T59, SWE-T55]

### When a threaded test fails now and then

1. Treat it as a threading defect. Do not skip it, retry it or mark it as a one-off. [CC-T60, CC-T69]
2. Make the failure more frequent by running the test many times with the jiggle hook bound to random timing, and control scheduling and the clock. [CC-T61, SWE-T09]
3. Replace fixed sleeps in the test with bounded polls or event waits. [SWE-T55]
4. Add trace statements in one parseable format to follow the order of events. [PP-T60]
5. Look for shared fields written from many places, plain collections or counters used across threads, and multi-step sequences without one lock. [CC-T57, CC-T58, CC-T56]
6. Remove production sleeps or retries that nobody can justify, since they may be hiding the race. [PP-T66]
7. Keep the check that exposed the race as an automated test. [PP-T62]

## Where the books disagree

### Should a hot path give up clean structure for speed?

- **Refactoring:** Tune only after the structure is clean. Split a loop that builds two results for clarity, keeping the combined loop only when profiling shows a real bottleneck. [REF-T87, REF-T32]
- **POSD:** Back out a speed change that shows no measured gain unless it also simplifies the system. Structure special cases for simplicity except on hot paths, where one early guard is better. [POSD-T48, POSD-T51, POSD-T30]
- **Clean Code:** Replace magic numbers with named constants and helpers, except where those calls would cost unacceptable time on a critical path. [CC-T24]
- **Pragmatic Programmer:** Leave assertions enabled in release builds unless they are measured as too costly, and an extra full pass on a hot path may be. [PP-T15]
- **Decide:** Keep the clean form by default. Give it up only on a path that measurement shows to be hot, only for a change with a measured gain, and record that measurement in the commit. [REF-T87, REF-T32, POSD-T48, PP-T15, CC-T24]

### Design for speed up front, or only after measuring?

- **POSD:** Keep frequently executed code free of per-item remote calls, disk access and allocations from the start, because those costs dominate, and benchmark the operations a design depends on before building around them. [POSD-T49, POSD-T48]
- **Pragmatic Programmer:** Estimate growth while you write the code, then profile before you invest in tuning. [PP-T45, PP-T46]
- **Refactoring:** Profile before changing any code for speed. [REF-T87]
- **Decide:** While you write a path that clearly runs per item or per request, or performs I/O, keep per-item remote calls, disk access and allocations out of it without waiting for a measurement, and estimate growth as you go. Measure the doubtful cases first. [POSD-T49, PP-T45] When someone suspects existing code is slow, or you consider tuning it, profile first and keep the baseline, which satisfies all three books. [REF-T87, PP-T46, POSD-T48]

### One lock over the whole sequence, or no lock during remote calls?

- **Clean Code:** Run a multi-step sequence on one shared object under one lock, so other threads cannot interleave. [CC-T56]
- **Release It!:** Keep remote calls out of locked sections, because the lock blocks every waiting thread for the length of the call. [RI-T20]
- **Decide:** The two rules collide only when the sequence includes a remote call. Keep the lock over the in-memory steps on the shared object, and make the remote call outside it. [CC-T56, RI-T20] If the sequence is only correct when the remote result and the in-memory steps happen as one atomic unit, the entries give no deciding rule. Follow the codebase's existing convention and state the trade-off in the PR.

### Share working state through fields, or keep it per thread?

- **Clean Code and Refactoring:** Promote locals that several extracted helpers need into fields of one object, or move a tangled function into a command object that stores its arguments and locals as fields. Hide mutable state behind one public method. Refactoring adds that plain functions usually suffice, and changing locals should be split first. [CC-T35, REF-T81, CC-T40]
- **Clean Code's own caveats:** Static fields shared by several threads can break such helpers, and multithreaded use needs locks or per-caller instances. [CC-T35, CC-T40]
- **Clean Architecture and FP in Scala:** Confine mutable state to a few named components, and prefer immutable values with state passed explicitly. FP in Scala notes that copying a large state on every call is costly, and efficient persistent structures help. [CA-T09, FPS-P2]
- **Decide:** Promote locals to fields only on an instance that one caller owns, such as a new command object per call. When the object is reachable from several threads, give each caller its own instance or guard the fields with a lock, and avoid static fields for this working state. [CC-T35, CC-T40, REF-T81, CA-T09]

## Review checklist

- [ ] Every change made for speed cites a profiler or benchmark baseline that names the hot spot. [PP-T46, POSD-T48, REF-T87]
- [ ] Optimization commits include before and after numbers or a benchmark test, and contain no unrelated restructuring. [SWE-T64, REF-T87]
- [ ] A speed change with no measured gain is backed out, unless it also simplifies the code. [POSD-T48]
- [ ] Nested loops and recursion over input have been checked for quadratic growth. [PP-T45]
- [ ] Loops and per-request handlers make no per-item network call, disk access or allocation, unless the path runs rarely and does no I/O. [POSD-T49]
- [ ] The speed fix changes an algorithm or data structure, or the PR says why none exists. [POSD-T50]
- [ ] Custom sort or search code has a benchmark that justifies it. [PP-T47]
- [ ] Each new cache or queue sets a size bound, and each cache cites a measured cost. [RI-P4, PP-T09, POSD-T48]
- [ ] Latency metrics use percentiles, start at request arrival, and read a monotonic clock. [DDIA-T09, RI-T75, DDIA-T41]
- [ ] Policy modules contain no thread, queue, process, executor or lock calls. [CC-T55, FPS-P4]
- [ ] Fields reachable from several threads are private and written only by a few guarded methods. [CC-T57, CA-T09]
- [ ] Shared collections and counters use concurrent or atomic library types, and no home-built pool or queue appears. [CC-T58, RI-T19]
- [ ] Each multi-step sequence on a shared object runs under one lock or one locking method. [CC-T56]
- [ ] No lock scope wraps a remote call, and lock waits and pool checkouts pass a time limit. [RI-T20, RI-P2, RI-T13]
- [ ] No pool task blocks on a future it submitted to its own executor, and blocking outbound calls use a separate executor. [FPS-T40, RI-T29]
- [ ] Event handler comments name their trigger and calling thread. [POSD-T56]
- [ ] A test stops every thread and confirms that shutdown completes. [CC-T59]
- [ ] No intermittent threaded test is skipped, retried or labeled a one-off. [CC-T60]
- [ ] Any jiggle hook is a no-op in production and randomized in tests. [CC-T61]
- [ ] Tests wait with bounded polls or event waits, never fixed sleeps, and production sleeps or retries have a stated reason. [SWE-T55, PP-T66]

## More entries in this area

- `CC-T62` — Render async views only after loading finishes: when a view depends on data that loads asynchronously, check a loaded flag before creating it.
- `RI-T59` — Call independent providers in parallel with timeouts: when a feature depends on several external vendors, call each in parallel with its own timeout.
- `FPS-T39` — Combine parallel results with map2: merge two independent parallel results through the library's combinator instead of a hand-written join.
- `FPS-T49` — Balance folds for parallel combining: reduce a large sequence by halves when the halves can be combined in parallel.
- `FPS-P6` — Describe lazily and evaluate only what is needed: build lazy descriptions so work nobody reads is never done.
- `DDIA-T42` — Recheck a lease at the point of action: a thread can pause between checking a lease and acting on it.
- `DDIA-T43` — Fence writes with increasing tokens: when a former leaseholder may still write, let storage reject stale tokens.
- `DDIA-T37` — Check decisions over several rows for write skew: when a transaction's check reads several rows before writing others.
- `DDD-T72` — Lock before processing a single-consumer notification: when several consumers receive a message that only one should handle.
- `RI-T09` — Run steady longevity load on a spare machine: when leaks and slow growth must be found before release and a spare machine is available.
- `RI-T18` — Keep in-memory session contents small: when server memory per session limits capacity.
- `PP-T03` — Prototype risky parts in disposable code: when an unproven performance concern affects the design.
