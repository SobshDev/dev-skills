# Data-intensive systems: storage, replication, transactions, streams

This guide covers code and designs that store or move data: picking stores, shaping records, evolving encodings, replicating, partitioning, writing transactions, surviving network and clock faults, and feeding derived data from logs and jobs. The central idea is that each fact has one system of record, every other copy is rebuildable from it through an ordered log, and every remote call or retry may already have happened, so writes must be idempotent.

**Read this when:** choosing a database, cache, index or stream tool, designing a schema or document shape, changing a stored format or an API that several versions read, configuring replication, failover or sharding, writing a transaction that reads and then writes, handling timeouts or retries against a store, using leases or locks across machines, publishing events after a database change, writing a stream consumer or batch job, building caches, search indexes or read models from a source database.

**Entry IDs** such as `WELC-T12` point to `../books/<book>/techniques.md` (T) or `principles.md` (P);
the prefix table is in [SKILL.md](../SKILL.md).

## Contents
- [Rules: choosing and placing data systems](#rules-choosing-and-placing-data-systems)
- [Rules: data models and storage engines](#rules-data-models-and-storage-engines)
- [Rules: encoding and compatibility](#rules-encoding-and-compatibility)
- [Rules: replication and partitioning](#rules-replication-and-partitioning)
- [Rules: transactions and isolation](#rules-transactions-and-isolation)
- [Rules: faults, clocks and consistency](#rules-faults-clocks-and-consistency)
- [Rules: logs, streams, batch and derived data](#rules-logs-streams-batch-and-derived-data)
- [Playbooks](#playbooks)
- [Where the books disagree](#where-the-books-disagree)
- [Review checklist](#review-checklist)
- [More entries in this area](#more-entries-in-this-area)

## Rules: choosing and placing data systems

### 1. Keep one system of record and derive every copy

Give each fact one authoritative home, and compute caches, indexes, search documents and views from it. When derived data can be rebuilt, a stale or buggy copy costs only a rebuild, and a rule or fact changed in one place does not drift in others. [DDIA-P1, PP-P3]

- **Do:** Write each new fact to the system of record first. Feed each copy through a process you can rerun. Treat a value duplicated into many records for faster reads as derived data, and update every copy in the same transaction as the source or through a replayable consumer. [DDIA-P1, DDIA-T19]
- **Not when:** Duplicated copies are acceptable only when some process updates every one of them. Identical-looking facts may encode different rules that change separately, so check before merging them. [DDIA-P1, PP-P3]
- **Check:** Each derived store names its source and a command that rebuilds it. Code that changes a source field also updates every duplicate in one transaction or in a replayable consumer. [DDIA-P1, DDIA-T19]

### 2. Choose each store by workload and write down its downsides

No data system is best for every workload, because each one buys some property by giving up another. Compare candidates against the actual access pattern of the feature and record what the chosen tool does badly. When no single tool serves every access pattern well, compose several specialized stores and make the integration between them explicit code. [DDIA-T01, DDIA-T02]

- **Do:** In the design note, name the workload (reads, writes, queries, volume) and list the downsides of the chosen database, cache, index or processing tool. When combining stores, write the integration as visible code, preferably fed from one log (rule 29). [DDIA-T01, DDIA-T02, DDIA-P8]
- **Not when:** Early in development, before storage needs are known, the books prefer deferring the choice behind an interface (see the tension on deferring the database). [CA-P4, CC-T54]
- **Check:** Design notes name the workload and the chosen tool's downsides. Separate stores are connected by explicit integration code. [DDIA-T01, DDIA-T02]

### 3. Stay on one machine until a requirement forces distribution

A single machine is simpler to build and operate than a cluster, so each distributed component needs a concrete reason. Fault tolerance is one such reason: a component without redundancy turns one machine fault into a failure of the whole system. [DDIA-P6, DDIA-T04]

- **Do:** Name the requirement behind each distributed component. Choose a single machine when it suffices. When availability is the requirement, find every component whose single fault fails the system and give it a replica or failover path on a separate machine or datacenter. [DDIA-P6, DDIA-T04]
- **Not when:** Fault tolerance, scale, latency or legal requirements can force distribution. Simplicity is subjective, so compare options by how much detail each one exposes rather than by taste. [DDIA-P6]
- **Check:** Each distributed component has a named requirement in its design or a code comment. An availability review lists no component without redundancy. [DDIA-P6, DDIA-T04]

### 4. Measure load and tail latency before changing the architecture

Scaling work chosen without measurements often attacks the wrong bottleneck. Record current throughput, peaks and percentile latency, and benchmark engines on your own workload at larger data volumes before adding nodes. Medians hide the slowest requests, so track high percentiles too. [DDIA-P7, DDIA-T09]

- **Do:** Capture throughput, peak load and p95, p99 and p999 latency. Run a single-node benchmark on the real workload at a larger data volume before proposing a cluster. [DDIA-P7, DDIA-T09]
- **Not when:** Averages are fine for estimating throughput limits, where mean response time is the useful figure. Stop at the 99.9th percentile unless a 99.99th percentile goal clearly justifies its cost. [DDIA-P7, DDIA-T09]
- **Check:** Capacity notes give load and percentile latency beside a single-node benchmark. [DDIA-P7]

For SLOs, load shedding and monitoring, see [production reliability](production-reliability.md). For profiling and concurrency tuning, see [performance and concurrency](performance-and-concurrency.md).

### 5. Give each service its own database behind its API

A shared database couples services, so no team can change its storage or schema without coordinating with the others. Each service owns a private database and exposes data only through its public interface. [DDIA-T07, DDD-T70]

- **Do:** Keep each service's tables private, and make other services call its API instead of reading its tables. [DDIA-T07, DDD-T70]
- **Not when:** During a strangler migration, old and new contexts may temporarily share a database when splitting the data would need distributed transactions. [DDD-T70, DDD-T58]
- **Check:** No two services connect to the same schema, and clients call only public APIs. [DDIA-T07, DDD-T70]

Service boundaries themselves are covered in [architecture](architecture.md) and [domain modeling](domain-modeling.md).

### 6. Keep analytical and ad hoc queries off operational databases

Analytical scans slow transactional work, and open-ended SQL can reach data in ways the application never planned for. Feed one separate analytical store from every operational database, and point analysts at it. When other teams consume an analytical output, publish it with a versioned schema and a watched service level, built from outputs rather than operational tables. [DDIA-T03, DDD-T66]

- **Do:** Connect reporting and analyst tools to a warehouse or replica. Give each published analytical output a versioned schema file and monitoring against its SLA. [DDIA-T03, DDD-T66]
- **Not when:** Occasional maintenance or troubleshooting queries may still be run by hand against production. [DDIA-T03]
- **Check:** Production exposes no open SQL endpoint, and analyst tools connect to a warehouse or replica. [DDIA-T03]

## Rules: data models and storage engines

### 7. Nest data read as a whole, and split unbounded children out

When the data is a tree that the application usually loads together, one nested document returns it in one read without joins or extra round trips. When a parent can have many thousands of related items, keep them as separate records, because frequent small edits to one huge document are costly. [DDIA-T17, DDIA-T18]

- **Do:** Nest one-to-many children whose count has a fixed, documented upper bound. Move collections that can grow without bound into their own records that reference the parent. [DDIA-T17, DDIA-T18]
- **Not when:** Do not nest when related items are numerous, or when only small parts of a large document are read at a time. [DDIA-T17]
- **Check:** Every embedded array in a document schema has a documented upper bound on its length. No parent document embeds an array that can grow without bound. [DDIA-T17, DDIA-T18]

### 8. Default to a B-tree index, and benchmark before choosing LSM

The index choice depends on the workload, so the default needs a measurement to be overturned. A B-tree is the default for key lookups and range queries on a relational OLTP table. Choose an LSM engine only when a benchmark on your own workload favors it, and then choose its compaction strategy by the measured read and write mix. [DDIA-T22, DDIA-T21]

- **Do:** Keep the B-tree default without further justification. For an LSM table, pick size-tiered compaction for write-heavy loads and leveled compaction for read-heavy loads. [DDIA-T22, DDIA-T21]
- **Not when:** A write-heavy workload whose benchmarks favor LSM overturns the B-tree default. Avoid size-tiered compaction when free disk space cannot absorb the temporary space its merges need. [DDIA-T22, DDIA-T21]
- **Check:** An LSM choice cites a benchmark run on the application's own workload. The compaction setting matches the table's measured read-to-write ratio. [DDIA-T22, DDIA-T21]

### 9. Flush the log before acknowledging a write

Data held only in memory disappears in a crash, so only logged and flushed data counts as durable. Append to the write-ahead log and fsync it before reporting a write or commit as successful. [DDIA-T23]

- **Do:** Order the commit path as append, fsync, then acknowledge. Make an in-memory store reload its state from a log or a replica at startup. [DDIA-T23]
- **Check:** No success response is sent before the fsync returns, and startup code restores in-memory state from a log or replica. [DDIA-T23]

### 10. Checksum data end to end in the application

Checksums in Ethernet, TCP, TLS and disk protocols miss corruption that software bugs introduce along the path. Compute a checksum where the application first holds the data, store it with the data, and verify it on every read. [DDIA-T57]

- **Do:** Apply this to data that crosses many components or is stored for a long time. [DDIA-T57]
- **Not when:** Lower-layer checksums do not replace this check, so their presence is no reason to skip it. [DDIA-T57]
- **Check:** Stored records carry an application checksum, and the read path verifies it. [DDIA-T57]

## Rules: encoding and compatibility

### 11. Keep stored data and APIs readable in both directions

During a rolling upgrade, old and new code run side by side, so each version must read the other's data and calls. Old readers skip fields that a newer writer added instead of rejecting the record. Servers keep accepting older request formats, because clients and servers deploy at different times. [DDIA-P5, DDIA-T24, DDIA-T26, RI-T46]

- **Do:** Make decoders ignore unknown fields. Test old readers on new data and new readers on old data. Run compatibility tests for every client-version and server-version pair that can coexist. Make code and data changes tolerate old and new versions running together for the length of the rollout. [DDIA-P5, DDIA-T24, DDIA-T26, RI-T46]
- **Not when:** Clients outside your control, such as those owned by other organizations, may not upgrade, so their old requests must keep working. [DDIA-P5, DDIA-T26]
- **Check:** Compatibility tests decode old fixtures with new code and the reverse, including records with unknown fields. [DDIA-P5, DDIA-T24]

### 12. Store a schema version with every record and message

A version tag lets a reader pick the right decoder when records written under different schemas share one store or travel between processes. Keep every schema version in a shared table. For stored events, add new versions beside old ones rather than rewriting history. [DDIA-T25, RI-T52, DDD-T33]

- **Do:** Put a version field in each stored record and in each request and response message. Register every version in a shared schema table, and have each connection agree on a version before sending data. When an event's shape changes, handle it with a new schema version. [DDIA-T25, RI-T52, DDD-T33]
- **Not when:** A controlled event-store migration may change stored events as an exception. [DDD-T33, DDD-T28]
- **Check:** Records and messages carry a version field, a shared table lists every version, and no code updates stored event records to fit a new schema. [DDIA-T25, RI-T52, DDD-T33]

## Rules: replication and partitioning

### 13. Make one follower synchronous and the others asynchronous

One synchronous follower protects acknowledged writes. Making every follower synchronous lets any single follower outage block all writes. [DDIA-T27]

- **Do:** Mark exactly one follower synchronous and the rest asynchronous when a database has several followers. [DDIA-T27]
- **Check:** Replication configuration shows exactly one synchronous follower. [DDIA-T27]

### 14. Fence stale leaders and leaseholders at the storage layer

After failover the old leader may still be running and accepting writes, and a paused process may resume after its lease expired. Two writers must never succeed at once, and only the storage layer can reliably refuse the stale one. Attach a token that increases with each lock grant, and have storage reject any token lower than the highest it has seen. [DDIA-T28, DDIA-T42, DDIA-T43]

- **Do:** Promote the replica with the most recent changes. Block the old leader's writes, and make a rejoining node check current leadership before accepting writes. Take fencing tokens from the lock service's counter. Recheck the lease immediately before the critical action. [DDIA-T28, DDIA-T42, DDIA-T43]
- **Not when:** If storage cannot compare tokens, recheck the lease immediately before the critical action instead. [DDIA-T43, DDIA-T42]
- **Check:** The storage write path rejects lower tokens. Tests inject pauses between the lease check and the action. Failover code fences the old leader. [DDIA-T43, DDIA-T42, DDIA-T28]

### 15. Route a user's reads after their own write to a fresh copy

Asynchronous followers and derived views lag, so users can see stale data right after their own update. For a short window after a write, send that user's reads to the leader, or to a replica that has reached the user's last write position. Track the position, not a wall-clock time. [DDIA-T29]

- **Do:** Have clients carry their last write position. Exclude followers past a set lag threshold, and make reads wait or redirect when a replica is behind the client's position. [DDIA-T29]
- **Check:** Read routing compares replication positions, not timestamps, for users who just wrote. [DDIA-T29]

### 16. Order concurrent writes by versions, not wall clocks

Machine clocks disagree, so timestamps can reverse the real order of writes. Order writes with logical counters, versions or causal metadata. Last-write-wins picks a winner arbitrarily and silently drops the losing write, so use it only where that loss is harmless. [DDIA-P4, DDIA-T30, DDD-T19]

- **Do:** Store a version on each record or aggregate and reject an update whose expected version no longer matches. Set the conflict policy per dataset, and give critical datasets a policy other than last-write-wins. Break equal-timestamp ties by a fixed value comparison. Use wall-clock values only for display and for event-time windows. [DDIA-P4, DDIA-T30, DDD-T19, DDIA-T51]
- **Not when:** Last-write-wins by timestamp is acceptable where losing some concurrent writes does not matter. It is not acceptable when the application cannot tolerate lost updates. [DDIA-P4, DDIA-T30]
- **Check:** Conflict and ordering code compares counters or versions, not raw timestamps. A stale update fails with a conflict error. [DDIA-P4, DDD-T19]

### 17. Choose the partition key on purpose

Records that share a key land on one shard, and any query without the key must search every shard. Declare the key explicitly for each sharded table, collection or key-value namespace, and hash it unless range queries need the original order. [DDIA-T32]

- **Do:** Declare a partition key per table. Send each object's log updates to the shard for its object ID. Do not start a range key with a timestamp. [DDIA-T32]
- **Not when:** When range queries need the original key order, keep the key unhashed. [DDIA-T32]
- **Check:** The schema names the partition key, keys are hashed unless a range query needs order, and no range key leads with a timestamp. [DDIA-T32]

## Rules: transactions and isolation

### 18. Put writes that must succeed together in one transaction

Partial completion of dependent writes leaves data inconsistent, while a transaction applies all of them or none. In a domain model, the data that must stay strongly consistent belongs inside one aggregate, and each transaction saves one aggregate. [DDIA-T33, DDD-P5, DDD-T20]

- **Do:** Wrap dependent statements in one BEGIN and COMMIT instead of separate autocommit calls. Keep external calls and user waits outside the transaction. When an operation seems to need two aggregates in one transaction, revisit the aggregate boundaries first. [DDIA-T33, DDD-T20]
- **Not when:** A single document update already covers the write, or a derived index or view can update after the commit. Writes spanning several systems follow rule 29 instead. A multi-aggregate process may use a saga, but a saga must never split operations that need strong consistency. [DDIA-T33, DDIA-P8, DDD-P5]
- **Check:** Related statements share one transaction with no remote call inside it. Each command handler saves a single aggregate. [DDIA-T33, DDD-P5]

### 19. Name the anomalies your isolation level allows

Levels weaker than serializable run faster but permit specific race conditions, so the application's tolerance for those races decides the level. Vendors use the same names for different guarantees, so record the vendor's meaning too. [DDIA-T34]

- **Do:** Before choosing a level weaker than serializable, list the races it allows and review each against the risk. Record each race you accept. [DDIA-T34]
- **Check:** Design notes state the chosen level, the vendor's definition of it, and each accepted anomaly. [DDIA-T34]

### 20. Guard every read-modify-write cycle

A separate read and write lets a concurrent update slip in between and be overwritten. Protect each cycle with an atomic operation, a lock, a conditional write, or lost-update detection, and do not count repeatable read as a guard. [DDIA-T36, DDD-T19]

- **Do:** Use a single statement for counters. Use a conditional write or an expected-version check for edits that atomic operations cannot express. [DDIA-T36, DDD-T19]
- **Not when:** Free-text edits such as wiki pages do not fit atomic operations, so guard them with a conditional write. [DDIA-T36]
- **Check:** Each read-modify-write path names its guard. [DDIA-T36]

```sql
-- Unguarded: read balance, compute in code, write it back (loses concurrent updates).
-- Atomic: let the database compute.
UPDATE accounts SET balance = balance + :delta WHERE id = :id;
-- Conditional: write only if nobody changed the row since it was read.
UPDATE pages SET body = :new_body, version = version + 1
 WHERE id = :id AND version = :version_read;   -- 0 rows updated means conflict
```

### 21. Protect decisions over several rows against write skew

Under snapshot isolation, two transactions can both pass the same check and then write different rows, which breaks the rule the check enforced. When a transaction reads several rows and writes other rows based on what it read, run it at serializable isolation or lock the rows the check reads. [DDIA-T37]

- **Do:** Identify checks that read several rows before writing others, and either raise the isolation level or lock the rows read. [DDIA-T37]
- **Check:** The transaction runs at serializable isolation or explicitly locks the rows its check reads. [DDIA-T37]

### 22. Enforce uniqueness with a constraint or a single decider

Two requests can both pass a "does it exist" check before either one inserts, so only the database can stop both. Declare a uniqueness constraint and handle its violation error. When several asynchronous leaders or shards can accept writes for the same value, route every request for that value to the one node or shard that decides it. [DDIA-T38, DDIA-T54]

- **Do:** Add a unique index and catch the violation instead of checking first. When several asynchronous leaders or shards may accept writes for unique usernames, emails, request IDs or limited quantities, give each key exactly one deciding node or shard. [DDIA-T38, DDIA-T54]
- **Not when:** Loose constraints that can be fixed later may tolerate multi-leader replication instead of a single decider. [DDIA-T54]
- **Check:** The schema has a unique index on the field and code handles the violation. Each unique key or limited quantity has one node or shard that accepts or rejects it. [DDIA-T38, DDIA-T54]

### 23. Retry aborted transactions only for transient errors

Permanent errors cannot succeed on retry, and unbounded retries under contention add load to a system that is already failing. Retry transient errors such as deadlocks and failovers with capped attempts and growing randomized delays. [DDIA-T35, DDIA-T11]

- **Do:** Classify errors as transient or permanent. Retry only the transient ones, with exponential backoff, jitter and a maximum attempt count. Handle overload separately. Add retries yourself where the framework does not. Make the retried operation idempotent (rule 31). [DDIA-T35, DDIA-T11, DDIA-P3]
- **Not when:** Do not retry permanent errors such as constraint violations. [DDIA-T35]
- **Check:** Retry logic distinguishes error classes, caps attempts and backs off with jitter. [DDIA-T35, DDIA-T11]

## Rules: faults, clocks and consistency

### 24. Treat a timeout as an unknown outcome

A timeout does not reveal whether the remote side applied the request, and a transport acknowledgment only shows that bytes arrived. A write reported as failed may still have taken effect. Count a request as successful only on a positive reply from the application that handled it, and never report a timed-out write as failed. [DDIA-P2, DDIA-T39]

- **Do:** Separate confirmed failures from timeouts in error handling. Pass an explicit timeout to every remote call, lock wait and pool checkout. Retry a timed-out write only with the same client request ID, so a repeat is recognized. [DDIA-P2, DDIA-T39, RI-P2, RI-T22, DDIA-T55]
- **Check:** Success is detected from an application-level reply, not a socket acknowledgment. Each remote call in the diff passes a timeout. Timed-out writes are not surfaced as failures. [DDIA-T39, RI-P2, DDIA-P2]

See [errors and contracts](errors-and-contracts.md) for how to represent the unknown outcome in code.

### 25. Specify and test the behavior for each network fault

Untested fault paths can deadlock or destroy data, so decide in advance how software behaves during each network fault, and test that it recovers once the network is repaired. Every dependency eventually fails, so each one needs a handled error, timeout and recovery path. [DDIA-T40, RI-P1]

- **Do:** Derive timeouts from measured round-trip times. Declare a node dead only after retries. Write fault tests that partition and heal the network and assert recovery. [DDIA-T40]
- **Not when:** Foreseeable failures should still be prevented where that is practical, rather than only handled. [RI-P1]
- **Check:** Fault tests assert recovery after a partition heals, and each dependency call in the diff has an error, timeout or fallback path. [DDIA-T40, RI-P1]

Fault injection and failure-path testing are covered in [testing](testing.md) [DDIA-T13, DDIA-T14].

### 26. Measure durations with a monotonic clock

Time-of-day clocks can jump backward when time synchronization corrects them, which makes subtracted readings wrong. Measure timeouts and elapsed time with a monotonic clock API. [DDIA-T41]

- **Do:** Read the monotonic clock for elapsed time on one machine, and keep its readings on that machine. [DDIA-T41]
- **Not when:** Use the wall clock when you need a calendar date or time of day to show users. [DDIA-T41]
- **Check:** Duration code never subtracts wall-clock readings, and no monotonic reading is sent to another machine. [DDIA-T41]

### 27. Send linearizable operations to the current leader

Serializable isolation alone can still return stale reads, and a deposed node may not know it lost leadership. Route linearizable reads and writes to the leader, and make a node without a current lease or epoch refuse leader-only operations. [DDIA-T45]

- **Do:** Make a new leader apply all committed entries before it serves. Make a deposed node refuse leader-only work. [DDIA-T45]
- **Not when:** This does not work when clients cannot know for sure who the leader is. Quorum overlap alone does not give linearizability either. [DDIA-T45, DDIA-T31]
- **Check:** Linearizable paths route only to the leader, and leadership is checked by lease or epoch. [DDIA-T45]

### 28. Coordinate synchronously only where a mistake cannot be repaired

Strong consistency needs fast, reliable links between replicas, and coordination lowers availability. Choose strong consistency for well-connected replicas, and spend synchronous cross-region coordination only on constraints with irreversible effects. Elsewhere, accept that you will sometimes apologize and repair afterwards. Within a domain model, test whether logic would give wrong results under eventual consistency, and keep that data in one aggregate if it would. [DDIA-T44, DDIA-T56, DDD-T22]

- **Do:** Tie each strong-consistency choice to measured link latency and reliability. For each constraint, record whether it can be repaired later, the expected rate of apologies, and the availability cost of coordinating. [DDIA-T44, DDIA-T56]
- **Not when:** Strong consistency costs performance, and over slow or unreliable links it turns faults that eventual consistency would absorb into outages. When corrupted data would be a business showstopper, relaxing consistency is not an option. [DDIA-T44, DDD-T22]
- **Check:** Synchronous cross-region calls appear only on paths with irreversible effects, and each relaxed choice has a written risk assessment. [DDIA-T56, DDD-T22]

## Rules: logs, streams, batch and derived data

### 29. Integrate stores through one ordered change log

Distributed transactions are costly and fragile. Instead, write each change to one system of record, let it decide the order of all writes, and feed every other store from its change log in log order. One ordering point gives every derived representation the same history to reproduce. [DDIA-P8, DDIA-T49, DDIA-T53]

- **Do:** Route all user input through one system that decides a total order. Feed search indexes, caches and views from the database's log rather than from direct application writes. [DDIA-T53, DDIA-T49, DDIA-P8]
- **Not when:** Distributed transactions remain an option where the environment accepts their cost. Events from different shards, regions or services share no global order, so causal dependencies across objects need a causal mechanism such as versions. [DDIA-P8, DDIA-T53, DDIA-P4]
- **Check:** Outside a strict global index, no XA or two-phase commit coordinator spans the stores. Derived stores receive changes from a log and apply them in log order. [DDIA-P8, DDIA-T49]

### 30. Publish events through an outbox written with the change

A crash between saving state and publishing an event either loses the event or announces a change that never committed. Write the event to an outbox table in the same transaction as the domain change, and let a relay or CDC process publish it afterwards. Give the outbox its own schema so internal tables can change while consumers stay stable. [DDIA-T50, DDD-P7, DDD-T46, DDD-T47]

- **Do:** Insert the outbox row in the domain write's transaction. Mark or delete each outbox row only after the relay has published it. Keep publish calls out of aggregate methods. [DDIA-T50, DDD-T46, DDD-T47, DDD-P7]
- **Not when:** Skip the separate outbox schema when maintaining its transformation and the extra writes costs more than stable consumers are worth. Published events cannot be cancelled, so reversals need compensating commands. [DDIA-T50, DDD-P7]
- **Check:** The outbox insert shares a transaction with the domain write, CDC or the relay reads the outbox, and rows are marked published only after a successful publish. [DDIA-T50, DDD-T47]

### 31. Make every repeatable write idempotent

Retries and redeliveries repeat work after failures, so each operation must give the same result when it runs twice. Idempotence is the practical route to exactly-once effects. Generate a request ID at the client, carry it through every layer and event, store it under a unique constraint, and skip repeats. For log consumers, store the source offset with each written value. [DDIA-P3, DDIA-T55, DDIA-T52]

- **Do:** Give each mutating endpoint, consumer and task an operation ID. Write the offset or request ID in the same transaction as the effect. Commit consumer offsets in batches after processing, and deduplicate the messages replayed since the last commit. Put the same identifier in logs and downstream calls so a request can be traced. [DDIA-P3, DDIA-T55, DDIA-T52, DDIA-T48, RI-T70]
- **Not when:** Idempotence holds only with replays in original order, a deterministic handler and one writer per key. Operations that are not naturally idempotent need extra metadata and fencing during failover. [DDIA-P3, DDIA-T52]
- **Check:** Mutating endpoints and consumers store operation IDs or offsets and skip repeats, and design notes list the replay, determinism and single-writer assumptions. [DDIA-P3, DDIA-T52]

```python
def handle(msg, db):
    with db.transaction() as tx:
        last = tx.scalar("SELECT last_offset FROM sink_progress WHERE shard = %s", msg.shard)
        if last is not None and msg.offset <= last:
            return                      # replayed after a restart: already applied
        tx.execute("INSERT INTO totals ...", msg.value)
        tx.execute("UPSERT sink_progress (shard, last_offset) VALUES (%s, %s)",
                   msg.shard, msg.offset)
```

### 32. Window stream events by their event timestamps

Processing-time windows change when a job reruns or catches up on a backlog, while event-time windows give the same result every time. Assign events to windows using the timestamp embedded in each event. [DDIA-T51]

- **Do:** Read the window key from the event's timestamp field. [DDIA-T51]
- **Not when:** Processing time is fine when processing delay is negligible. When device clocks cannot be trusted, use the server's receive time instead. [DDIA-T51]
- **Check:** Window assignment reads the event field, not the clock at arrival. [DDIA-T51]

### 33. Treat batch output as rebuildable: new output, rerun to repair

Unchanged inputs let a bad run be repeated, and a full rebuild avoids patching stale output. Read inputs without modifying them, write results to a new location, and regenerate the whole output each run. When deployed batch code writes wrong output, roll back or fix the code and rerun it from the retained inputs. [DDIA-T46, DDIA-T47]

- **Do:** Write each task to a fresh output path and delete earlier partial output on retry. Keep deployable earlier job versions. For long jobs on clusters where any node may fail, write periodic checkpoints and resume from the latest. Ship computation to the nodes that hold large inputs instead of copying data to workers. [DDIA-T46, DDIA-T47, DDIA-T08, DDIA-T06]
- **Not when:** Rerunning does not repair output that the buggy job wrote into an operational database. Continuously serving systems cannot pause the whole cluster to checkpoint this way. [DDIA-T47, DDIA-T08]
- **Check:** Tasks never overwrite their inputs, output goes to a new location, and restart paths load the latest checkpoint. [DDIA-T46, DDIA-T08]

### 34. Validate commands before appending events

In an event-sourced system every view replays the log, so an invalid event poisons every view. Check business rules in the command handler before the append, and make every view consumer accept every event that was logged. Keep the event store append-only, and on a stale expected version inspect the newer events before rejecting. [DDIA-T20, DDD-T28]

- **Do:** Reject bad commands before the append. Rebuild views from stored inputs and skip side effects during rebuilds. Expose only fetch and append on the event store. [DDIA-T20, DDD-T28]
- **Not when:** A controlled data migration may change the event store as an exception. [DDD-T28]
- **Check:** Rules run before the append, view consumers never reject logged events, and rebuilds trigger no side effects. [DDIA-T20]

### 35. Append corrections, and design erasure through every copy

When data must be recoverable after bugs or analysts need its history, record corrections and raw inputs as new appended records, because the originals are the evidence for both. Append-only logs and derived datasets keep old copies, though, so personal-data erasure must reach every copy, not just the primary row. [DDIA-T60, DDIA-T61, DDD-T31]

- **Do:** Write corrections as inserts. Keep personal fields out of events and reference people by ID, or encrypt personal event fields with a per-aggregate key that can be deleted. Make erasure rewrite logs and derived datasets. [DDIA-T60, DDIA-T61, DDD-T31]
- **Not when:** Erasure requests override append-only history and follow the erasure design instead. [DDIA-T60]
- **Check:** Outside erasure, no update or delete changes a logged input. Erasure rewrites stored records in logs and derived datasets, and events hold IDs instead of personal fields. [DDIA-T60, DDIA-T61]

Privacy and data-residency obligations are covered in [security](security.md).

## Playbooks

### When you change a stored format, schema or API that several versions read
1. Make the change additive: add fields that old readers can skip. [DDIA-T24]
2. Put a version tag on the record or message and register the new version in the shared schema table. [DDIA-T25, RI-T52]
3. Add compatibility tests that decode old fixtures with new code and new fixtures with old code, for every client and server version pair that can coexist. [DDIA-P5, DDIA-T26]
4. For stored events, add a new event version beside the old one instead of rewriting stored events. [DDD-T33]
5. Apply additive schema changes first, then roll out the application, then run any data migration that old instances cannot read. [RI-T47, RI-T46]
6. Roll the release out to a small share first and keep a switch-back path, as described in [production reliability](production-reliability.md). [DDIA-T16]

### When a write must also reach a cache, search index or another service
1. Write the fact to its system of record first. [DDIA-P1]
2. In the same transaction, insert an outbox row with its own stable schema. [DDIA-T50, DDD-T46]
3. Publish from the outbox with a relay or CDC, and mark rows published only after success. [DDD-T47]
4. Have each derived store consume the change log in log order, never through a second direct write from the application. [DDIA-T49, DDIA-T53]
5. Make each consumer idempotent by stored offset or event ID, and commit offsets in batches after processing. [DDIA-T52, DDIA-T48]
6. If users must see their own change immediately, route their reads to a copy that has reached their write position. [DDIA-T29]
7. Write down the command that rebuilds each derived store from the source. [DDIA-P1]

### When you add an endpoint, task or consumer that may be retried
1. Have the client generate a request ID and carry it through every layer, event and log line. [DDIA-T55, RI-T70]
2. Store the ID under a unique constraint with the effect, and skip IDs already handled. [DDIA-T55, DDIA-T38]
3. Set an explicit timeout on each remote call, and treat a timeout as an unknown outcome, never as a confirmed failure. [RI-P2, DDIA-P2]
4. Confirm success only from the remote application's reply. [DDIA-T39]
5. Retry transient errors only, with capped, jittered exponential backoff. [DDIA-T11, DDIA-T35]
6. Test a duplicate delivery and a timeout after the effect was applied. [DDIA-T14]

### When code reads data, decides, and then writes
1. Put the dependent writes in one transaction with no remote call inside, or in one aggregate if you use a domain model. [DDIA-T33, DDD-T20]
2. If one row is read and written back, guard it with an atomic statement, a conditional write or a version check. [DDIA-T36, DDD-T19]
3. If the decision reads several rows and writes others, run at serializable isolation or lock the rows read. [DDIA-T37]
4. If the rule is uniqueness, use a unique constraint, or a single deciding shard when several leaders accept writes. [DDIA-T38, DDIA-T54]
5. Record the isolation level, the vendor's definition and the anomalies you accept. [DDIA-T34]
6. Retry transient errors such as deadlocks and failovers with capped backoff, and surface constraint violations. [DDIA-T35]
7. Add a test with a burst of concurrent writes. [DDIA-T14]

### When you configure replication, failover or sharding
1. Name the requirement that forces distribution, and remove single points of failure for availability. [DDIA-P6, DDIA-T04]
2. Make one follower synchronous and the rest asynchronous. [DDIA-T27]
3. On failover, promote the most up-to-date replica and fence the old leader with increasing tokens checked by storage. [DDIA-T28, DDIA-T43]
4. Route linearizable operations to the leader, and make deposed nodes refuse them. [DDIA-T45]
5. Set a conflict policy per dataset, and keep last-write-wins off critical data. [DDIA-T30, DDIA-P4]
6. For quorum stores, configure W plus R greater than N for reads that need fresh values. [DDIA-T31]
7. Declare partition keys, hashed unless ranges need order. [DDIA-T32]
8. Test partitions and their healing, and inject faults in a production-like environment. [DDIA-T40, DDIA-T13]

### When you build or fix a batch or stream job
1. Read inputs without changing them and write each run's output to a new location. [DDIA-T46]
2. Ship the computation to the nodes that hold large inputs. [DDIA-T06]
3. Checkpoint long jobs and restart from the latest checkpoint. [DDIA-T08]
4. Window by event timestamps unless delay is negligible or device clocks are untrusted. [DDIA-T51]
5. Make writes to external stores idempotent with stored offsets. [DDIA-T52]
6. To repair bad output, roll back or fix the code and rerun from retained inputs, and repair operational databases separately. [DDIA-T47]

### When you pick storage for a new feature
1. If storage needs are still unknown, build against an in-memory implementation behind a data interface. [CC-T54, CA-T45]
2. Once the workload is known, compare candidates by fit and record the chosen tool's downsides. [DDIA-T01]
3. Prefer a single machine unless a named requirement forces distribution. [DDIA-P6]
4. Shape documents by access: nest bounded trees read together, and split unbounded children. [DDIA-T17, DDIA-T18]
5. Keep the B-tree default unless a benchmark on your workload favors LSM. [DDIA-T22]
6. Place residency-bound data in its permitted region, and send analytics to a separate store. [DDIA-T05, DDIA-T03]

## Where the books disagree

### Group related writes in one transaction, or change one aggregate per transaction?
- **DDIA:** Put writes that must succeed or fail together in one transaction, so dependent records never diverge. [DDIA-T33]
- **Learning DDD:** Save one aggregate per transaction, and when an operation seems to need two, redraw the boundary so the strongly consistent data lives in one aggregate. [DDD-T20, DDD-P5, DDD-T22]
- **Decide:** The books agree that data which must change together needs one transaction. They differ on where to fix it. In code organized as aggregates, move data that would give wrong results under eventual consistency into one aggregate, and connect the rest with a saga. In code without aggregates, wrap the dependent statements in one transaction. In both cases, a derived index or view may update after the commit. [DDD-T22, DDD-P5, DDIA-T33]

### Distributed transaction, ordered log, or saga for writes that span systems?
- **DDIA:** Avoid direct multi-system writes. Write to one system of record and feed the others from its log. Distributed transactions suit only environments that accept their cost. [DDIA-P8, DDIA-T49]
- **Learning DDD:** Model a process across several transactions as a saga with a compensating command for each step, store the saga's history as events, and treat its participants as eventually consistent. [DDD-T49, DDD-T50]
- **Learning DDD (migration):** During a strangler migration, keep a shared database temporarily rather than split data in a way that needs distributed transactions. [DDD-T58]
- **Decide:** When other stores only need to mirror or index a change, feed them from the log. When a business process spans several transactions and a later step may fail, use a saga with compensations, unless a later step depends on earlier results, and never to split operations that need strong consistency. Choose a distributed transaction only when the environment accepts its cost. [DDIA-P8, DDD-T49, DDD-P5]

### Strong consistency, or eventual consistency with repairs?
- **DDIA:** Choose strong consistency where replicas are well connected, and coordinate synchronously only on constraints that cannot be repaired. Loose constraints can tolerate multi-leader replication. [DDIA-T44, DDIA-T56, DDIA-T54]
- **Learning DDD:** Keep data that would give wrong results under eventual consistency in one aggregate. Relaxing consistency is not an option when corruption would be a business showstopper. [DDD-T22]
- **Decide:** Ask whether a violation can be repaired later and what it would cost. If it cannot, or corruption would be a showstopper, coordinate. If it can, and the links are slow or unreliable, accept eventual consistency and record the expected apologies. [DDIA-T56, DDD-T22, DDIA-T44]

### Choose the database now, or defer the choice?
- **DDIA:** Select each store by comparing it against the workload, and record its downsides. [DDIA-T01]
- **Clean Architecture and Clean Code:** Keep the database choice open behind a boundary, and start with in-memory or stubbed storage until use cases settle the decision. [CA-P4, CA-T45, CC-T54]
- **Decide:** The conditions separate them. In early development, before storage needs are known, build behind a data interface with an in-memory implementation. When the workload is known and a feature needs a real store, compare candidates by fit. [CC-T54, CA-P4, DDIA-T01]

### Keep stored history forever, or erase it?
- **DDIA and Learning DDD:** Append corrections instead of editing originals, and keep event stores append-only. [DDIA-T60, DDD-T28, DDD-T33]
- **DDIA and Learning DDD (erasure):** Personal data must be erasable on request from logs and derived datasets, either by rewriting stored records or by deleting a per-aggregate encryption key. [DDIA-T61, DDD-T31]
- **Decide:** Erasure requests for personal data take precedence over append-only history. Where possible, keep personal fields out of events and reference people by ID, or encrypt them with a per-aggregate key so erasure deletes the key. Change stored events by controlled migration only as the exception. [DDIA-T60, DDIA-T61, DDD-T31, DDD-T28]

### When is an event-sourced history worth it, and when do you add snapshots?
- **DDIA:** Record changes and raw inputs as appended records when data must be recoverable after bugs or analysts need history. [DDIA-T60]
- **Learning DDD:** Store an aggregate as events only where the business needs full history, audit or very complex logic, because event sourcing costs training and ongoing effort. Add snapshots only after a benchmark at realistic event counts shows slow replay. [DDD-T26, DDD-T30]
- **Clean Architecture:** Store changes as transactions with periodic snapshots when history matters and full replay would become too slow. [CA-T10]
- **Decide:** Adopt append-only history when recovery or history is a stated need, and budget for its cost. Add snapshots when replay is measured to be slow at realistic counts, which satisfies both Clean Architecture's condition and Learning DDD's. [DDIA-T60, DDD-T26, DDD-T30, CA-T10]

### Update read models synchronously or from an asynchronous log?
- **Learning DDD:** For a new CQRS system, build a synchronous projection first, and add an asynchronous one only on top of it, because asynchrony brings disorder. [DDD-T39]
- **DDIA:** Feed derived stores from the source database's change log in log order, and handle the lag it introduces with read-your-writes routing. [DDIA-T49, DDIA-T29]
- **Decide:** For read models inside one new CQRS service, start synchronous. When several separate stores must match one source, feed them from the log, and route a user's reads to a copy that has caught up with their write. [DDD-T39, DDIA-T49, DDIA-T29]

### Retry with backoff, or retry at once?
- **DDIA:** Retry with growing, randomized, capped delays, so retries do not multiply the load that caused the failure. [DDIA-T11]
- **Release It!:** Inside a data center, wait or back off before retrying, but transient problems over a WAN, such as dropped packets, may clear with a prompt retry. [RI-T23]
- **Decide:** Back off by default. A prompt retry is supported only for transient faults across a WAN, and it still needs a bounded count. [DDIA-T11, RI-T23]

## Review checklist

- [ ] Each new cache, index or view names its source store and a rebuild command. [DDIA-P1]
- [ ] Duplicated fields are updated in the source's transaction or by a replayable consumer. [DDIA-T19]
- [ ] Outside a temporary strangler-migration share, no service reads another service's tables. [DDIA-T07, DDD-T70]
- [ ] Every embedded array in a document has a documented bound. [DDIA-T17, DDIA-T18]
- [ ] Decoders tolerate unknown fields, and tests cover old-to-new and new-to-old decoding. [DDIA-T24, DDIA-P5]
- [ ] Stored records and messages carry a schema version. [DDIA-T25, RI-T52]
- [ ] Data migrations that old instances cannot read run after the application rollout. [RI-T47]
- [ ] Dependent writes share one transaction, with no remote call inside it. [DDIA-T33]
- [ ] Each read-modify-write path uses an atomic statement, lock, conditional write or version check. [DDIA-T36, DDD-T19]
- [ ] Multi-row checks run at serializable isolation or lock the rows they read. [DDIA-T37]
- [ ] Uniqueness is enforced by a unique index whose violation is handled, not by check-then-insert, or by one deciding shard when several leaders accept writes. [DDIA-T38, DDIA-T54]
- [ ] The isolation level and its accepted anomalies are written down. [DDIA-T34]
- [ ] Transaction retries are limited to transient errors, capped and backed off with jitter. [DDIA-T35, DDIA-T11]
- [ ] Every remote call has a timeout, and timed-out writes are not reported as failed. [RI-P2, DDIA-P2]
- [ ] Ordering and conflict code compares versions or counters, not wall-clock timestamps. [DDIA-P4]
- [ ] Elapsed time is measured with a monotonic clock. [DDIA-T41]
- [ ] Writes guarded by a lease carry a fencing token that storage checks. [DDIA-T43, DDIA-T42]
- [ ] Events are published through an outbox row in the domain transaction, not by a publish call beside the commit. [DDIA-T50, DDD-T46]
- [ ] Mutating endpoints and consumers store request IDs or offsets and skip repeats. [DDIA-P3, DDIA-T55, DDIA-T52]
- [ ] Stream windows use event timestamps. [DDIA-T51]
- [ ] Batch jobs write to new output locations and never overwrite inputs. [DDIA-T46]
- [ ] The commit path fsyncs the log before acknowledging. [DDIA-T23]
- [ ] Long-lived data, or data that crosses many components, carries an application checksum verified on read. [DDIA-T57]

## More entries in this area

- `DDIA-T05` — Keep residency-bound data in its jurisdiction: map each user or tenant to a permitted region when residency law applies, except where the law covers only medical or financial data.
- `DDIA-T31` — Make W plus R exceed N: for quorum stores serving reads that need fresh values, knowing overlap does not give linearizability.
- `DDD-T29` — Build several projections from one event stream: when a feature needs a view of an aggregate that its state does not provide.
- `DDD-T32` — Keep audit history in persisted events: when an audit trail must reflect operations that change the database.
- `DDD-T52` — Notify, then query for sensitive or fresh data: when consumers must read the latest write or the payload is sensitive.
- `DDD-T65` — Validate records against a schema on ingestion: for data lake ingestion feeding several analytical models.
- `RI-T41` — Omit schema and reseed endpoints from production admin: when designing admin controls over a production store.
