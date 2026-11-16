# Production reliability: stability, operations, deployment

This guide covers code and configuration for software that serves real traffic: calls to other systems, timeouts and circuit breakers, bulkheads, bounded resources, overload handling, health checks and metrics, rollouts, schema migrations, versioning and chaos experiments. The single most important idea is that every dependency will fail, so each call needs a time limit and a handled failure path, and each change needs a small, staged, reversible way into production.

**Read this when:** adding or changing a call to a remote service, database, queue or API, configuring a connection or thread pool, adding a cache, queue or session field, handling overload or rate limits, adding retries, writing health checks, metrics or SLOs, writing a deployment script or pipeline, planning a canary or percentage rollout, changing a database schema or message format that running code reads, adding a feature flag or kill switch, preparing a service for its first production release, planning a fault-injection experiment.

**Entry IDs** such as `WELC-T12` point to `../books/<book>/techniques.md` (T) or `principles.md` (P);
the prefix table is in [SKILL.md](../SKILL.md).

## Contents

- [Core rules: integration points](#core-rules-integration-points)
- [Core rules: circuit breakers and bulkheads](#core-rules-circuit-breakers-and-bulkheads)
- [Core rules: bounded resources and overload](#core-rules-bounded-resources-and-overload)
- [Core rules: observability](#core-rules-observability)
- [Core rules: deployment and runtime operations](#core-rules-deployment-and-runtime-operations)
- [Core rules: versioning and migrations](#core-rules-versioning-and-migrations)
- [Core rules: readiness and chaos experiments](#core-rules-readiness-and-chaos-experiments)
- [Playbooks](#playbooks)
- [Where the books disagree](#where-the-books-disagree)
- [Review checklist](#review-checklist)
- [More entries in this area](#more-entries-in-this-area)

## Core rules: integration points

### 1. Give every dependency a handled failure path

Treat every integration point and component as something that will fail, often in a way nobody predicted, and design so the failure stays contained and the system recovers. Release It! asks for an explicit failure path per dependency, and adds that when two designs both meet the functional requirements, the one that behaves better under failure usually costs about the same to build. [RI-P1, RI-T08]

- **Do:** For each external call or I/O the change adds, list how it can fail: refused connection, timeout, no response, slow response, missing or malformed reply, reset, and an oversized reply. Write a handled path for each one. When choosing between designs that both meet the functional requirements, record in the design note how each design behaves under failure, and pick the one that behaves better. [RI-T12, RI-T08]
- **Not when:** Listing every failure mode exhaustively is often impractical, except in life-critical systems, where it is expected. Prevention still matters: stop foreseeable failures where that is practical, rather than only containing them. [RI-T12, RI-P1]
- **Check:** Each dependency call in the diff has an error, timeout or fallback path, and a test drives at least one failure through it. [RI-P1, SWE-T53]

Writing those failure tests is covered in [testing](testing.md).

### 2. Put an explicit time limit on every wait

A wait with no limit can hold its caller forever, and one stalled dependency can tie up every thread, because many client and pool defaults never time out. Release It! asks for an explicit limit on each remote call, socket read and write, lock wait and pool checkout that the change adds or touches. [RI-P2, RI-T22]

- **Do:** Pass a timeout to every outbound client call. Set read timeouts and request-write timeouts on sockets and HTTP clients instead of the infinite default. Give every pool checkout a maximum wait and handle the timeout branch. Give request-reply exchanges over message queues an expiry path, so a reply that never arrives does not leave the requester waiting. [RI-T22, RI-T14, RI-T13, RI-T11]
- **Check:** No remote call, socket, lock acquire or pool checkout in the diff can wait indefinitely, and each timeout branch is handled. [RI-P2, RI-T13]

Measure those durations with a monotonic clock, as described in [data systems](data-systems.md). [DDIA-T41]

### 3. Fit sequential calls into one time budget

Individually safe timeouts do not add up to a safe caller: safety does not compose, so a chain of calls can exceed the caller's own limit even when each call respects its own. When a feature needs several independent providers, calling them in parallel with separate timeouts keeps one failing provider from taking the others down with it. [RI-T69, RI-T59]

- **Do:** Add up the worst-case waits of calls made in sequence and check that the sum fits the caller's overall timeout. Call independent carriers or vendors in parallel, each with its own timeout. [RI-T69, RI-T59]
- **Not when:** Calling the providers one after another, or without timeouts, defeats the split, so the parallel form only helps when both conditions hold. [RI-T59]
- **Check:** A timeout test or budget check covers the summed latency of sequential calls, and parallel provider calls each carry their own timeout. [RI-T69, RI-T59]

### 4. Validate the reply and the connection before trusting them

A reply in an unexpected shape breaks code that assumes the success format, and a pooled connection that reports itself open may still be unable to run statements after a network event or failover. Database drivers do not repeat failed inserts, updates or stored procedure calls on their own after a failover. [RI-T15, RI-T06, RI-T38]

- **Do:** Branch on status code and content type before deserializing a remote response. Wrap statement calls on pooled connections in error handling, whatever the connection's open flag says. Catch and handle the database error on writes that fail during a failover. Acquire connections before a try block and release them in a finally clause or scope-based cleanup. In JDBC cleanup code, guard each close so that a failing statement close cannot skip the connection close, since the JDBC specification allows statement close to throw. [RI-T15, RI-T06, RI-T38, RI-T72, PP-T38]
- **Check:** Response handling inspects status and content type before parsing, write paths handle failover errors, and no single exception in cleanup can leak a connection. [RI-T15, RI-T38, RI-T72]

### 5. Treat a timed-out call as possibly completed

A timeout tells the caller nothing about whether the remote side applied the request, so a write reported as failed may in fact have happened. DDIA asks designs to keep that unknown state distinct from a confirmed failure, and to make repeatable operations idempotent so a retry cannot apply the effect twice. [DDIA-P2, DDIA-P3]

- **Do:** Separate confirmed failures from timeouts in error handling, and never report a timed-out write as failed. Give each mutating request a client-generated ID that travels through every layer, and skip repeats of it. [DDIA-P2, DDIA-T55, DDIA-P3]
- **Not when:** Idempotence by ID only holds when replays arrive in their original order, the handler is deterministic and one writer owns each key. Operations that are not naturally idempotent need extra metadata, and fencing during failover. [DDIA-P3]
- **Check:** Error handling has a distinct timeout branch, and mutating endpoints store operation IDs and ignore repeats. [DDIA-P2, DDIA-P3]

The storage side of idempotence (offsets, unique constraints, fencing) is in [data systems](data-systems.md).

### 6. Wait, back off and cap before retrying

Inside a data center a remote problem tends to last, so an immediate retry usually fails again, and repeated immediate retries multiply the very load that caused the failure. Both Release It! and DDIA ask for a delay before each retry. DDIA specifies exponentially growing, randomized delays with a cap on attempts, and for aborted transactions it retries only errors that are transient. Release It! also retries only documented transient errors, with a bounded count. [RI-T23, DDIA-T11, DDIA-T35]

- **Do:** Wait before every retry, grow the delay exponentially with jitter, cap the number of attempts in configuration, and retry only errors documented as transient, such as deadlock or failover. Make the retried operation idempotent first (rule 5). [DDIA-T11, RI-T23, DDIA-T35, DDIA-P3]
- **Not when:** Transient problems such as dropped packets over a WAN may clear with a prompt retry. Permanent errors, such as constraint violations, never succeed on retry, so they are not retried. [RI-T23, DDIA-T35]
- **Check:** Retry loops sleep with growing, jittered delays, stop at a configured maximum, and filter on a list of transient errors. [DDIA-T11, RI-T23, DDIA-T35]

```python
def call_with_retry(op, request_id, max_attempts, base_delay):
    for attempt in range(max_attempts):              # capped attempts
        try:
            return op(request_id, timeout=CALL_TIMEOUT)  # explicit timeout
        except TransientError:                       # only documented transient errors
            if attempt == max_attempts - 1:
                raise
            delay = base_delay * (2 ** attempt)
            sleep(random.uniform(0, delay))          # growing, randomized wait
    # PermanentError is never caught here, so it is not retried
```

## Core rules: circuit breakers and bulkheads

### 7. Wrap draining calls in a timeout and a circuit breaker

Release It! names timeouts and circuit breakers as the most effective defenses against cascading failure. Any outbound call whose failure could use up the caller's threads or pools needs both, and the breaker must count timeouts as failures, or a slow dependency never trips it. [RI-T17]

- **Do:** Put a breaker around each such call, configured to count timeouts as well as errors. When the breaker is open, fail calls at once with an exception type distinct from a timeout, without invoking the dependency. After the cool-off period, admit one trial call in a half-open state, close the breaker if it succeeds and reopen it if it fails. [RI-T17, RI-T24, RI-T71]
- **Check:** Each such call has a timeout and a breaker that counts timeouts (or a named equivalent mechanism), the open path throws its own exception type without calling out, and a half-open state exists. [RI-T17, RI-T24, RI-T71]

```java
Response call(Request r) {
    State s = breaker.state();                 // every transition is logged and exported
    if (s == OPEN && !breaker.coolOffElapsed())
        throw new BreakerOpenException();      // not a TimeoutException, no remote call
    if (s != CLOSED && !breaker.claimTrialCall())
        throw new BreakerOpenException();      // half-open admits one trial call only
    try { Response res = client.send(r, timeout); breaker.onSuccess(); return res; } // success closes
    catch (TimeoutException | RemoteException e) { breaker.onFailure(); throw e; }  // timeouts count, failed trial reopens
}
```

Keep the breaker's own state from serializing calls behind one lock. That concurrency detail is in [performance and concurrency](performance-and-concurrency.md). [RI-T20]

### 8. Make breaker state visible and resettable

Operators and monitoring need to see when a breaker trips, resets or tests recovery, and they need a way to return an integration to service once the fault clears. [RI-T25, RI-T40]

- **Do:** Log every breaker state change, export the current state as a metric, offer a state query, and add a breaker reset operation to the admin API. [RI-T25, RI-T40, RI-P5]
- **Not when:** A service with no circuit breakers has nothing to reset, so the control does not apply. [RI-T40]
- **Check:** State transitions emit log entries or metrics, a state query exists, and the admin API includes a reset. [RI-T25, RI-T40]

Other admin controls that are hazardous in production are covered in [security](security.md).

### 9. Partition shared capacity with bulkheads

A failure that spreads across a system is a cascade. Giving each caller group or traffic class its own pool, instance set or deployment means one group's failure leaves the others running. The same idea inside one process separates the threads that accept requests from the threads that block on outbound calls, so a request thread can time out and answer while the outbound call is still stuck. [RI-P3, RI-T29]

- **Do:** Configure separate server and thread pools for different callers or traffic types. Run blocking outbound or library calls on an executor separate from the request-handling threads, with a timeout on the caller side. [RI-P3, RI-T29]
- **Not when:** Groups that fail in the same way gain nothing from separation. A partition does not protect the callers of a failed partition, which still need circuit breakers. Wrapping calls on a separate executor can grow into a reactive wrapper around a whole client library, so watch for that cost. [RI-P3, RI-T29]
- **Check:** Pools for different callers are configured separately in code or deployment, and blocking outbound calls run on their own executor with a timeout. [RI-P3, RI-T29]

### 10. Keep must-work features off optional dependencies

Name the features the business cannot lose during a partial failure, and keep optional components out of their request paths, so a failure in an optional part cannot stop them. For optional features that do depend on something fragile, a runtime-adjustable pool maximum gives an incident switch: setting it to zero disables the feature without a code change or deployment. [RI-T10, RI-T30]

- **Do:** List the must-work features, and check that their request code calls no optional component. Make the pool maximum of each non-essential dependent feature adjustable at runtime, and show a fallback when that dependency is unavailable. [RI-T10, RI-T30]
- **Not when:** Do not set the limit to zero for a feature that must stay available under heavy load: zero disables it fully, while a limit of one keeps it available. [RI-T30]
- **Check:** Request code for each named feature calls no optional component, and optional features have a runtime pool limit and a visible fallback. [RI-T10, RI-T30]

### 11. Fix the defect behind a repeating chain reaction

When one defect keeps crashing servers one after another under the same load, limits and partitions only slow the spread, and the defect stays in place to restart the chain. Release It! asks for a fix to the code path itself. [RI-T16]

- **Do:** Change the code path named in the incident record, and add limits only as a complement. [RI-T16]
- **Not when:** Partitioning alone does not stop the reaction: it turns one chain reaction into two that run at different rates. [RI-T16]
- **Check:** The fix alters the faulty code path, not only limit settings. [RI-T16]

Finding the defect is covered in [debugging](debugging.md).

## Core rules: bounded resources and overload

### 12. Bound every cache, queue, session and result set

Anything that can grow without limit eventually exhausts memory or pushes response times past target. Release It! asks for a configured bound on each cache and queue, small session contents, row limits in queries over tables that can grow, and size-based rotation for local log files. [RI-P4, RI-T18, RI-T68, RI-T73]

- **Do:** Give every new cache and queue an explicit size limit. Store only identifiers or scalar values in server-side sessions, not lists or full result sets. Put a row limit or paging in every hand-written query that can return unbounded rows, because a client-side timeout is only a stopgap for that. Configure size-based rotation with a maximum number of retained files for every log written to local disk. Serve 404s and static assets without creating a session, since error-only traffic such as crawlers should not cost memory on servers carrying real users. [RI-P4, RI-T18, RI-T68, RI-T73, RI-T54]
- **Check:** Cache and queue constructors set a bound, session writes hold IDs or scalars, queries on growable tables carry LIMIT, TOP or paging, and log settings define a size limit and a retention count. [RI-P4, RI-T18, RI-T68, RI-T73]

Placing a queue in front of an unavoidable shared resource is covered in [performance and concurrency](performance-and-concurrency.md). [RI-T21]

### 13. Reject excess load fast

Serving every request slowly misses the service level for all of them, while a quick refusal frees the caller sooner and lets an overloaded server recover instead of growing its backlog. Release It! triggers shedding on latency measured against the service-level target or on full queues. DDIA triggers it as queueing or resource use nears the limit, and adds per-client caps on shared resources. [RI-T28, RI-T37, DDIA-T12]

- **Do:** Add an admission check that returns an immediate error, without blocking, when queues are full or measured response time exceeds the target. Cap each client's share of shared resources with quotas. Answer temporary overload that the service expects to recover from soon with HTTP 503, and make overload responses tell clients to slow down. When load passes what servers can serve without saturating, admit only a configured share of new sessions at the gateway, as a setting operators can lower without a deploy. [RI-T37, RI-T28, DDIA-T12, RI-T26, RI-T55]
- **Not when:** Many clients treat any non-success status as fatal, so a 503 may not help them. [RI-T26]
- **Check:** The overload path returns at once with 503 or an equivalent, the trigger reads measured latency or queue depth, and per-client quotas exist. [RI-T37, RI-T28, RI-T26, DDIA-T12]

## Core rules: observability

### 14. Make health checks and metrics show real state

Operators must be able to diagnose a running system without adding code. Release It! asks for health checks that exercise the real service or a real dependency, and metrics that expose internal state such as pools, breakers and integrations. [RI-P5]

- **Do:** Make health endpoints run a real transaction or call a real dependency. Export metrics for pool usage, breaker state and each integration. [RI-P5, RI-T25]
- **Check:** Health endpoints call a real dependency, and metrics export pool and breaker state. [RI-P5]

### 15. Measure tail latency as residence time

A median can look fine while the slowest requests stay bad, so DDIA tracks high percentiles, writes service level objectives as a percentile latency target plus a success-rate target, and measures load before any scaling decision. Release It! adds that latency must include time spent waiting in queues, not only the service's own processing time. [DDIA-T09, DDIA-T10, DDIA-P7, RI-T75]

- **Do:** Record p95, p99 and p999 latency, and aggregate fleet-wide percentiles by summing histogram buckets. Write each SLO with a latency percentile and an error-rate target. Start the latency clock when the request reaches the server socket. Have client applications report timing and failures to a central collector, since instance metrics only infer what users experience. [DDIA-T09, DDIA-T10, RI-T75, RI-T39]
- **Not when:** Stop at the 99.9th percentile unless a 99.99th percentile goal clearly justifies its cost. Averages still suit estimating throughput limits. [DDIA-T09, DDIA-P7]
- **Check:** Monitoring defines percentile series above the median, SLO config lists a percentile target and an error-rate target, and the latency metric includes queue time. [DDIA-T09, DDIA-T10, RI-T75]

Using these numbers to find bottlenecks is covered in [performance and concurrency](performance-and-concurrency.md).

### 16. Carry one request identifier through logs and calls

Without a shared identifier, nobody can follow a failed request from end to end across tiers. A client-generated ID also lets downstream stages recognize a retried request. [RI-T70, DDIA-T55]

- **Do:** Put one request or transaction ID in every log message tied to the request, and pass it on every downstream call and event. [RI-T70, DDIA-T55]
- **Check:** Log statements and outbound calls carry the same correlation ID. [RI-T70]

### 17. Gate diagnostics behind per-user switches

Turning on extra diagnostics for every user adds noise and can expose internal state, so Pragmatic Programmer puts diagnostics, and unfinished features, behind a switch configurable per user or group. [PP-T63]

- **Do:** Guard extra diagnostic output with a configurable switch scoped to selected users or groups. [PP-T63]
- **Not when:** Do not enable diagnostics where end users or unauthorized people could see them. [PP-T63]
- **Check:** Diagnostic code paths check a per-user or per-group switch. [PP-T63]

## Core rules: deployment and runtime operations

### 18. Ship small changes through staged rollouts

Large batches carry more risk, and a small first stage limits the damage a faulty change does before checks catch it. Release It!, DDIA and SWE at Google all release to a small share first (a canary, a few nodes, or a small user percentage) and widen only when metrics show no harm. Release It! and DDIA also keep a way back at each stage. [RI-P7, DDIA-T16, SWE-T20, SWE-T21]

- **Do:** Keep each release small. Send it first to a canary, a few nodes or a small share of users, and advance each stage only after health checks and guardrail metrics (measures that must not worsen) show no harm. Keep a switch-back path at every stage, and give config changes the same review as code. Upgrade a cluster one node at a time, checking health before each next restart. [RI-P7, DDIA-T16, SWE-T20, DDIA-T15]
- **Not when:** Old and new builds must be able to coexist during the canary (rule 24). A product with too small a user base cannot reach statistically meaningful results from percentage stages. Client apps whose users dislike frequent updates and pay data costs for each one are poor fits for a fast cadence. [RI-P7, SWE-T20, SWE-T21]
- **Check:** The pipeline defines stages with metric gates and a switch-back path, and rolling upgrades check health between nodes. [RI-P7, DDIA-T16, DDIA-T15, SWE-T20]

Commit and release cadence, and rolling back a culprit change, are covered in [change workflow](change-workflow.md). [SWE-T31]

### 19. Flip feature flags through dynamic configuration

Reversing a flag is faster and safer than a rollback, which must itself succeed. SWE at Google keeps flag values in dynamic configuration so a problem can be undone without shipping a binary, and uses flags to separate deploying code from releasing a feature. [SWE-T19, SWE-P6]

- **Do:** Keep flag values in a dynamic configuration source, guard unfinished features with a flag, and make flipping a flag need no deployment. [SWE-T19, SWE-P6]
- **Not when:** Static settings that never change still belong in version control with the code. Flags do not hide sensitive features, since shipped code can be scraped, and some flags add too much complexity. [SWE-T19, SWE-P6]
- **Check:** Flag values are read from dynamic config, and no flag change requires a code deploy. [SWE-T19]

### 20. Verify that a runtime change actually took effect

A configuration change the running component never applied gives a false sense of control during an incident. [RI-T31]

- **Do:** After a live configuration change, read the setting back or observe the new behavior. [RI-T31]
- **Not when:** Settings read only at startup need a restart before they apply, so restart first and check afterwards. [RI-T31]
- **Check:** The change procedure includes a read-back or behavior check, after any needed restart. [RI-T31]

### 21. Script deployments from versioned definitions

Hand-run steps vary between runs and people, while a versioned script repeats the same way on every machine. Release It! and Pragmatic Programmer both keep installation definitions and repeated release steps in source control, and run them as scripts or pipeline stages. [RI-T34, RI-T45, PP-T17, PP-T18, PP-P7]

- **Do:** Keep the definition that creates a new installation in source control, and replace each repeated manual release step with a script or pipeline stage. Keep credentials out of those files. [RI-T34, RI-T45, PP-T17, PP-T18]
- **Check:** Deployment and installation steps live in versioned files, not in manual runbooks. [RI-T34, RI-T45, PP-P7]

Keeping secrets and environment values out of release artifacts is covered in [security](security.md).

### 22. Cap what one automation run may change

Automation that changes many resources at once can disrupt the whole system in a single run. Release It! asks automated changes to carry limits and leaves large changes to a person's judgment. [RI-P6]

- **Do:** Set a maximum number of changes per run, keep each subsystem above its minimum size, and require a person's confirmation before exceeding the maximum. [RI-P6]
- **Not when:** The right threshold depends on the system's spare burst capacity, so there is no universal number. [RI-P6]
- **Check:** Automation has a maximum change count or an approval gate. [RI-P6]

### 23. Make processes disposable and reachable by name

A container that keeps durable data outside itself can be replaced without loss, and a process that shuts down gracefully on termination signals finishes the work in flight instead of cutting it off. Dependencies addressed by service name stay reachable while the instances behind them come and go. [RI-T32, RI-T33, RI-T57]

- **Do:** Write durable files, data and caches to external storage, not container-local paths. Set a startup time goal, and on termination signals finish in-flight work before exiting. Reach other clusters through a virtual IP or DNS name, and have long-running clients re-resolve it. Where sessions are bound to an instance, keep session failover working so a customer mid-checkout can finish on another instance. [RI-T32, RI-T33, RI-T57, RI-T56]
- **Check:** No durable data goes to container-local paths, shutdown handles termination signals, config holds no instance address lists, and failover restores cart and checkout state. [RI-T32, RI-T33, RI-T57, RI-T56]

## Core rules: versioning and migrations

### 24. Let old and new versions run side by side

During a rolling deployment both versions serve traffic until the rollout finishes, so each must read the other's data and calls. DDIA asks for compatibility in both directions, and for old readers to skip fields that a newer writer added instead of rejecting the record. [RI-T46, DDIA-P5, DDIA-T26, DDIA-T24]

- **Do:** Make every code and data change tolerate both versions at once. Test old clients against new services and new clients against old services, and decode records with unknown fields in tests. [RI-T46, DDIA-T26, DDIA-T24]
- **Not when:** Clients outside your control may not upgrade, so their old requests must keep working. [DDIA-P5, DDIA-T26]
- **Check:** Compatibility tests cover each client and server version pair that can coexist, and decoding tolerates unknown fields. [DDIA-T26, DDIA-T24]

Encoding and schema evolution in storage are covered in [data systems](data-systems.md).

### 25. Order schema changes around the code rollout

A schema change that the running code cannot handle breaks the old instances still serving traffic. Release It! orders the work so that each step is readable by every version running at that moment: additive changes first, new code next, migrations old code cannot read after that, and tightening and cleanup last. [RI-P7, RI-T47, RI-T48, RI-T49]

- **Do:** Apply additive schema changes, and data copies that old code can read, before the new code rolls out. Deploy the new application before any data migration old instances cannot read. Add NOT NULL and foreign key constraints only in a release after the code is fully rolled out. Remove temporary sync triggers in their own later migration, once no old instance remains. [RI-P7, RI-T47, RI-T49, RI-T48]
- **Not when:** If old instances can still read the migrated data, the copy may run before rollout. Triggers are safe to add only if they are unconditional and cannot throw errors. [RI-T47, RI-P7]
- **Check:** The release plan lists the migrations in this order, constraint migrations ship in a later release than the code that needed them, and trigger removal is a separate migration. [RI-T47, RI-T49, RI-T48]

```sql
-- Release N   (before code):  ALTER TABLE orders ADD COLUMN region TEXT;      -- additive, nullable
--                             CREATE TRIGGER sync_region ...;                 -- unconditional, cannot throw
-- Release N   (code rollout): new code writes region, still reads old shape
-- After rollout:              UPDATE ... backfill region;                     -- old instances gone
-- Release N+1:                ALTER TABLE orders ALTER COLUMN region SET NOT NULL;
-- Release N+2:                DROP TRIGGER sync_region;                       -- own migration
```

### 26. Treat stricter request rules as breaking

Old consumers cannot send a field that did not exist when they were built, so a new required field, or any rule that rejects input an earlier version accepted, breaks them. A version number in every message lets readers dispatch to the right translator as formats evolve, and consumer-side contract tests catch provider changes that would break what consumers rely on. [RI-T50, RI-T52, RI-T51]

- **Do:** Add new request fields as optional, and check new validation against prior accepted inputs. Put a format version in every request and response message. When consuming another team's API or format, write contract tests in the consumer repository for every provider behavior your code relies on, run against the provider's staging system. [RI-T50, RI-T52, RI-T51]
- **Check:** The schema diff adds no required field, prior test inputs still pass validation, each message schema has a version field, and consumer contract tests exist. [RI-T50, RI-T52, RI-T51]

How to structure contract tests is covered in [testing](testing.md).

## Core rules: readiness and chaos experiments

### 27. Judge readiness by production conditions

QA tests cover an artificial setting, and operators live with the system after its builders move on. Release It! judges readiness by load, failure and operations checks, and expects operations staff to be able to run and recover the system without its developers. Long steady-load runs reveal leaks and growth that short tests cannot show. [RI-T02, RI-T01, RI-T09]

- **Do:** Put load, failure and operations checks into the release criteria, beside feature tests. Provide runbooks, deployment steps and alerts written for operations staff. When a spare machine is available, run a steady load for days, with scheduled idle periods, and log uptime and memory. [RI-T02, RI-T01, RI-T09]
- **Check:** Release criteria name load and failure checks, runbooks and alerts exist for operators, and a longevity job with idle periods exists. [RI-T02, RI-T01, RI-T09]

### 28. Keep a steady, bounded level of injected faults

Recovery paths that rarely run stay unproven until a large failure reaches them. Release It! keeps a continuous low level of controlled breakage running, and DDIA injects faults such as killed processes and severed networks in an environment that resembles production. Each experiment needs its rejection evidence fixed in advance and must leave enough redundancy alive that it cannot become a real outage. [RI-T61, DDIA-T13, RI-T62, RI-T63]

- **Do:** Schedule a fault-injection job that targets recovery paths. Before each experiment, write down what evidence rejects its hypothesis and how large a change counts. Skip injection targets that would remove a cluster's last instance or every fallback of a call. [RI-T61, DDIA-T13, RI-T62, RI-T63]
- **Not when:** Outside causes, such as aborted mobile connections, can produce failures too, so exclude known external error sources from the rejection evidence. [RI-T62]
- **Check:** A scheduled fault-injection job exists in repository or infrastructure config, each experiment states a rejection threshold, and injection rules keep at least one instance or fallback alive. [RI-T61, RI-T62, RI-T63]

### 29. Test for missing people as well as missing machines

A critical role or piece of knowledge held by one person is a single point of failure that goes home every evening. Release It! simulates that person's absence to find the gap. [RI-T64]

- **Do:** Run exercises where key people are unavailable, and fill the gaps they expose. [RI-T64]
- **Check:** Runbooks name a backup for each critical role or procedure. [RI-T64]

Owners and backup owners for projects are covered in [project and team](project-and-team.md).

## Playbooks

### When you add a call to a new dependency
1. List how the call can fail, including no response, slow response, and malformed or oversized replies. [RI-T12]
2. Decide whether this dependency is optional, and if so keep the call off the request path of every must-work feature. [RI-T10]
3. Set an explicit timeout on the call, read and write timeouts on its socket or HTTP client, and a maximum wait on the pool checkout. [RI-T22, RI-T14, RI-T13]
4. Check that the timeout fits the caller's overall budget together with the other calls in sequence. [RI-T69]
5. Run the call on an executor separate from request threads if it blocks, and give it its own pool if its callers differ. [RI-T29, RI-P3]
6. Wrap it in a circuit breaker that counts timeouts, fails fast when open and tests recovery half-open. [RI-T17, RI-T24, RI-T71]
7. Check status and content type before parsing, and keep timeouts distinct from confirmed failures. [RI-T15, DDIA-P2]
8. If you retry, make the operation idempotent first, then retry only transient errors with jittered backoff and a cap. [DDIA-P3, DDIA-T11, DDIA-T35]
9. Export breaker and pool metrics, log state changes, and test at least one failure through the path. [RI-P5, RI-T25, SWE-T53]

### When you change a schema that running code reads
1. Write the migration as additive: new nullable columns, new tables, and data copies old code can still read. [RI-P7]
2. Add any sync trigger only if it is unconditional and cannot throw. [RI-P7]
3. Roll out the new code, which must work with both the old and new shape. [RI-T46, RI-T47]
4. Run migrations that old instances cannot read only after every instance runs the new code. [RI-T47]
5. Add NOT NULL and foreign key constraints in a later release. [RI-T49]
6. Drop the temporary triggers in their own later migration. [RI-T48]

### When you roll out a risky change
1. Keep the change small, and put risky behavior behind a flag held in dynamic configuration. [RI-P7, SWE-T19]
2. Confirm old and new builds can serve traffic together. [RI-T46, DDIA-T26]
3. Name the guardrail metrics and their limits before the first stage. [SWE-T20, DDIA-T10]
4. Release to a canary, a few nodes or a small user share, with a switch-back path ready. [DDIA-T16, RI-P7]
5. Advance a stage only when health checks and guardrails show no harm, and stop when they degrade. [SWE-T20, RI-P7, DDIA-T15]
6. If the change misbehaves, flip the flag off first, and roll back if no flag covers it. If the rollback does not apply cleanly to mainline, fix forward, knowing that is riskier. [SWE-T19, SWE-T31]

### When a service is overloaded or a dependency is failing
1. Restore service before investigating the cause, as described in [debugging](debugging.md). [RI-T03]
2. Shed excess load quickly with 503 responses, and lower the gateway's admission percentage for new sessions. [RI-T37, RI-T26, RI-T55]
3. Disable non-essential features that depend on the failing system, through a runtime pool limit or a flag. For a feature that must stay available under heavy load, set the pool limit to one rather than zero. [RI-T30, SWE-T19]
4. Read every live setting back, or observe the new behavior, after changing it. [RI-T31]
5. Once the fault clears, reset the affected circuit breakers through the admin control. [RI-T40]
6. If one defect is felling node after node, fix that code path rather than only tightening limits. [RI-T16]

### When you change an API or message format
1. Keep every new request field optional, and accept every input earlier versions accepted. [RI-T50]
2. Carry a format version in each message. [RI-T52]
3. Make readers skip unknown fields. [DDIA-T24]
4. Test old clients against the new server and new clients against the old server. [DDIA-T26, DDIA-P5]
5. As a consumer of another team's format, keep contract tests for each behavior you rely on. [RI-T51]

### When you prepare a service for production
1. Bound every cache, queue, session and unbounded query, and rotate local logs. [RI-P4, RI-T68, RI-T73]
2. Put a timeout on every integration point, and a breaker on each call whose failure could drain the caller's threads or pools. [RI-P2, RI-T17]
3. Add health checks that touch a real dependency, metrics for pools and breakers, percentile latency measured as residence time, and a correlation ID in logs. [RI-P5, DDIA-T09, RI-T75, RI-T70]
4. Write SLOs as a percentile latency target and an error-rate target. [DDIA-T10]
5. Store durable state outside the container, start fast and shut down gracefully. [RI-T32, RI-T33]
6. Script the installation and release from versioned definitions. [RI-T34, RI-T45]
7. Check readiness with load and failure runs, add a longevity run when a spare machine is available, and hand operators runbooks and alerts. [RI-T02, RI-T09, RI-T01]

### When you plan a chaos experiment
1. Pick a recovery path that rarely runs in production. [RI-T61, DDIA-T13]
2. State the hypothesis and the evidence that rejects it, with the size of change that counts. [RI-T62]
3. Exclude known external error sources from that evidence. [RI-T62]
4. Constrain targets so at least one instance and one fallback survive. [RI-T63]
5. Keep it running as a continuous low level of controlled breakage, in an environment that resembles production. [RI-T61, DDIA-T13]
6. Include people in the exercise: simulate the absence of a key person. [RI-T64]

## Where the books disagree

### Is a timeout a failure?
- **Release It!:** A circuit breaker must count timeouts as failures, so a slow dependency trips it. [RI-T17]
- **DDIA:** A timeout leaves the outcome unknown, and a timed-out write must not be reported as failed. [DDIA-P2]
- **Decide:** Use both, for different questions. Count the timeout as a failure of the dependency's health, for the breaker. Treat it as an unknown outcome of the operation, for the caller and the user, and make the operation idempotent before retrying it. [RI-T17, DDIA-P2, DDIA-P3]

### Retry, or fail fast?
- **Release It!:** Fail fast when a breaker is open or the server is overloaded, and wait before retrying inside a data center, since problems there tend to persist. [RI-T24, RI-T37, RI-T23]
- **DDIA:** Retry with exponential, jittered delays and a cap, and retry aborted transactions only for transient errors. [DDIA-T11, DDIA-T35]
- **Decide:** Do not retry permanent errors, and do not call through an open breaker. For transient errors, retry with growing randomized delays and a cap. A prompt retry may clear transient network loss such as dropped packets over a WAN. [DDIA-T35, RI-T24, DDIA-T11, RI-T23]

### What should trigger load shedding?
- **Release It!:** Response time measured against the service-level target, full queues, or a gateway admission percentage for new sessions. [RI-T28, RI-T37, RI-T55]
- **DDIA:** Queueing or resource use approaching its limit, plus per-client quotas on shared resources. [DDIA-T12]
- **Decide:** The triggers do not conflict. Use latency against the SLA when the service can observe its own latency, queue depth or resource use when those near their limits, and quotas where clients share resources. The entries give no rule for choosing one when several apply, so follow the service's existing convention. [RI-T28, DDIA-T12]

### Contain a chain reaction, or fix it?
- **Release It!, bulkheads:** Partition capacity so one group's failure leaves the others running. [RI-P3]
- **Release It!, chain reactions:** Fix the defect, because partitioning only splits the reaction into two running at different rates. [RI-T16]
- **Decide:** Partition against failures that differ between caller groups. When the same defect keeps failing servers one after another under the same load, change that code path, and treat limits as a complement. [RI-P3, RI-T16]

### Automate the change, or keep a person in the loop?
- **Pragmatic Programmer and Release It!, deployment:** Replace manual steps with versioned scripts and pipelines. [PP-P7, RI-T45]
- **Release It!, automation:** Bound what one automation run can change, and require a person's confirmation beyond that bound. [RI-P6]
- **Decide:** Script the steps, and put a maximum change count on each run. Ask a person before exceeding it, with the threshold set from the system's spare burst capacity. [RI-T45, RI-P6]

### Which number describes latency?
- **DDIA:** High percentiles describe what users feel. Averages still suit estimating throughput limits. [DDIA-T09, DDIA-P7]
- **Release It!:** Measure residence time including queue wait, and measure users directly with real-user monitoring. [RI-T75, RI-T39]
- **Decide:** Use percentiles of residence time for SLOs, client-side reports for actual user experience, and means for throughput capacity estimates. [DDIA-T10, RI-T75, RI-T39, DDIA-P7]

### Roll out by nodes or by users?
- **DDIA:** Release to a few nodes or a small share of traffic, and upgrade clusters node by node. [DDIA-T16, DDIA-T15]
- **SWE at Google:** Release to growing user percentages gated by guardrail metrics. [SWE-T20]
- **Decide:** Use user percentages when the user base is large enough for significant results, and node or traffic stages otherwise. In both forms keep health checks between stages and a switch-back path. [SWE-T20, DDIA-T16]

## Review checklist

- [ ] Every remote call, socket, lock wait and pool checkout in the diff passes an explicit timeout. [RI-P2, RI-T13, RI-T14, RI-T22]
- [ ] Sequential calls fit the caller's overall time budget, and parallel provider calls each have their own timeout. [RI-T69, RI-T59]
- [ ] Calls that could drain threads or pools sit behind a breaker that counts timeouts, fails fast with its own exception, and has a half-open state. [RI-T17, RI-T24, RI-T71]
- [ ] Breaker transitions are logged and exported, and a reset control exists. [RI-T25, RI-T40]
- [ ] Response parsing checks status and content type first. [RI-T15]
- [ ] Write paths handle failover errors, and cleanup cannot skip a connection close. [RI-T38, RI-T72]
- [ ] Timeouts are handled apart from confirmed failures, and mutating endpoints skip repeated request IDs. [DDIA-P2, DDIA-P3]
- [ ] Retries wait with jittered exponential backoff, stop at a configured cap, and fire only on transient errors. [DDIA-T11, RI-T23, DDIA-T35]
- [ ] Blocking outbound calls run on an executor separate from request threads. [RI-T29]
- [ ] Must-work request paths call no optional component, and optional features have a runtime pool limit and a fallback. [RI-T10, RI-T30]
- [ ] New caches and queues have size bounds, sessions hold only IDs or scalars, and 404s and static assets create no session. [RI-P4, RI-T18, RI-T54]
- [ ] Queries over growable tables carry a row limit or paging, and local logs rotate by size with a retention count. [RI-T68, RI-T73]
- [ ] Overload returns an immediate 503 or equivalent, and per-client quotas exist. [RI-T37, RI-T26, DDIA-T12]
- [ ] Health endpoints touch a real dependency, and pool and breaker metrics are exported. [RI-P5]
- [ ] Latency metrics include queue time and report high percentiles, and SLOs pair a percentile target with an error-rate target. [RI-T75, DDIA-T09, DDIA-T10]
- [ ] Log lines and outbound calls carry one correlation ID. [RI-T70]
- [ ] The rollout has small stages with metric gates and a switch-back path. [RI-P7, DDIA-T16, SWE-T20]
- [ ] Flags live in dynamic configuration, and diagnostic switches are scoped to selected users. [SWE-T19, PP-T63]
- [ ] Code and data changes work with old and new versions running together, in both directions. [RI-T46, DDIA-T26]
- [ ] Migrations follow the order: additive first, code, unreadable migrations, constraints, then trigger removal. [RI-P7, RI-T47, RI-T49, RI-T48]
- [ ] Request schemas add no required field, and every message carries a version. [RI-T50, RI-T52]
- [ ] Deployment and installation steps are versioned scripts, and automation runs have a change cap or approval gate. [RI-T34, RI-T45, RI-P6]
- [ ] Durable data lives outside the container, shutdown drains in-flight work, and dependencies are addressed by service name. [RI-T32, RI-T33, RI-T57]
- [ ] Fault-injection experiments state a rejection threshold and keep an instance and a fallback alive. [RI-T62, RI-T63]

## More entries in this area

- `RI-T03` — Restore service before root-cause analysis: during a customer-facing outage; see [debugging](debugging.md).
- `RI-T04` — Script diagnostic capture before incidents: preparing incident tooling; see [debugging](debugging.md).
- `RI-T07` — Write a targeted test for the diagnosed failure: after a root cause is found; see [testing](testing.md).
- `RI-T19`, `RI-T20`, `RI-T21` — Library concurrency primitives, no remote calls under locks, a queue in front of a shared resource: see [performance and concurrency](performance-and-concurrency.md).
- `RI-T27` — Emulate the remote end with a harness: testing failure handling without the real dependency; see [testing](testing.md).
- `RI-T41` — Omit schema and reseed endpoints from production admin: designing admin controls; see [security](security.md).
- `RI-T53` — Replace a stack in several cutover steps: replacing a whole system; see [legacy code](legacy-code.md).
- `RI-P8` — Keep secrets and environment values out of artifacts: building images and configs; see [security](security.md).
- `DDIA-T14` — Test failure paths as thoroughly as normal paths: writing error-handling tests; see [testing](testing.md).
- `SWE-T21` — Release in small, frequent batches: setting a release cadence; see [change workflow](change-workflow.md).
- `PP-T34` — Externalize values that change between environments: hosts, ports and limits come from configuration, not literals.
