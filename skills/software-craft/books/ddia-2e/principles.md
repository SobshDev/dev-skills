# Designing Data-Intensive Applications — Martin Kleppmann and Chris Riccomini (2nd edition, 2026)

## Summary
Kleppmann and Riccomini argue that no data system fits every workload, so each design is a set of trade-offs. A design must name its workload, its system of record, its expected failures, and the guarantees each component gives. Networks, clocks, and retries cause partial failure, and logs and rebuildable derived data are the book's main defenses. Apply these rules when designing, changing, or reviewing any system that stores or moves data. Most detail stays in reference.md.

## Principles

### DDIA-P1: Keep one authoritative record and derive copies

Each fact should have one authoritative home, and caches, indexes, and views should be computed from it. Rebuildable derived data means a stale or buggy copy costs only a rebuild.

- **Apply:** Write each new fact to the system of record first, and derive each copy through a rerunnable process.
- **Limits:** Duplicated copies are acceptable only when a process updates every copy.
- **Check:** Each derived store names its source and a command that rebuilds it.
- **See:** DDIA-T19, DDIA-T49, DDIA-T47.
- **Source:** ch. 1, 3, 13.

### DDIA-P2: Treat every remote call as possibly failed

A timeout does not show whether a remote request was applied, so its outcome is unknown. A write reported as failed may still have taken effect. The book asks designs to handle that unknown state.

- **Apply:** Handle each timeout as possibly completed, and never report a timed-out write as failed.
- **Check:** Error handling separates confirmed failures from timeouts.
- **See:** DDIA-T39, DDIA-T40, DDIA-T11, DDIA-T55.
- **Source:** ch. 1, 5, 6, 9.

### DDIA-P3: Make repeatable operations idempotent

Retries and redeliveries repeat work after failures, so an operation must give the same result when it runs twice. The book treats idempotence as the practical route to exactly-once effects.

- **Apply:** Give each write endpoint, consumer, or task an operation ID, and ignore repeats by it.
- **Limits:** Idempotence needs replays in original order, a deterministic handler, and one writer per key. Operations that are not naturally idempotent need extra metadata and fencing during failover.
- **Check:** Mutating endpoints and consumers store operation IDs and skip repeats.
- **See:** DDIA-T55, DDIA-T52, DDIA-T48.
- **Source:** ch. 5, 8, 12, 13.

### DDIA-P4: Order concurrent events by version, not clocks

Wall clocks differ between machines, so their timestamps can reverse the real order of writes. The book orders events with logical counters and causal metadata.

- **Apply:** Order writes with logical counters or versions, never by wall-clock timestamps. Wall-clock values serve display and event-time windows (DDIA-T51).
- **Limits:** Last-write-wins by timestamp fits only where losing concurrent writes is acceptable (DDIA-T30).
- **Check:** Conflict and ordering code compares counters or versions, not raw timestamps.
- **See:** DDIA-T41, DDIA-T30, DDIA-T51.
- **Source:** ch. 6, 9, 10.

### DDIA-P5: Keep data and APIs readable in both directions

Old and new code run side by side during rolling upgrades, so each version must read the other's data and calls. The book asks for compatibility in both directions.

- **Apply:** Test each changed encoding and API with old readers on new data and new readers on old data.
- **Limits:** Clients outside your control may not upgrade, so old requests must keep working.
- **Check:** Compatibility tests decode old fixtures with new code and the reverse.
- **See:** DDIA-T24, DDIA-T25, DDIA-T26.
- **Source:** ch. 3, 5, 6.

### DDIA-P6: Keep designs simple and distributed only when needed

A single machine is simpler to build and run than a cluster, so distribution needs a concrete reason. The book warns against building for scale not yet needed.

- **Apply:** Name the requirement behind each distributed component, and choose a single machine when one suffices.
- **Limits:** Fault tolerance, scale, latency, or legal requirements can force distribution. Simplicity is subjective, so compare options by the detail each one exposes.
- **Check:** Each distributed component has a named requirement in its design or code comment.
- **See:** DDIA-T04, DDIA-T02.
- **Source:** ch. 1, 2, 13.

### DDIA-P7: Measure real load and tail latency before scaling

Scaling chosen without measurements often targets the wrong bottleneck. The book asks for current load and percentile latency before any architecture change.

- **Apply:** Record throughput, peaks, and percentile latency. Benchmark engines on your own workload at larger data volumes before adding nodes.
- **Limits:** Averages suit estimating throughput limits, where mean response time is useful.
- **Check:** Capacity notes give load and percentile latency beside a single-node benchmark.
- **See:** DDIA-T09.
- **Source:** ch. 1, 2, 4.

### DDIA-P8: Integrate systems through ordered logs, not transactions

Distributed transactions are costly and fragile, and the book advises against direct multi-system writes. The book prefers one ordered change log that other systems consume.

- **Apply:** Write each change to one system of record, and feed other stores from its log.
- **Limits:** Distributed transactions suit environments accepting their cost.
- **Check:** Outside a strict global index, no XA or two-phase commit coordinator spans the stores.
- **See:** DDIA-T50, DDIA-T48, DDIA-T49.
- **Source:** ch. 1, 5, 7, 12, 13.
