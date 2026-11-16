# Designing Data-Intensive Applications — techniques

### DDIA-T01: Choose each data system by workload fit

Compare each candidate data system against the workload, and record the downsides of the option you choose.

- **Why:** Every data system trades one property against another, so no option is best for every workload.
- **When:** Selecting a database, cache, search index, or processing tool for a feature.
- **Check:** Design notes name the workload and list the downsides of the chosen tool.
- **Source:** ch. 1.

### DDIA-T02: Combine systems when one cannot meet every need

Combine several data systems in application code, with explicit integration code between them.

- **Why:** A single system rarely serves every access pattern well, so the design composes specialized stores.
- **When:** A feature needs a capability that no single tool provides well.
- **Check:** Architecture shows separate stores connected by explicit integration code.
- **Source:** ch. 1.

### DDIA-T03: Keep analytical queries off operational databases

Run analytical queries against one separate store that every operational database feeds, and keep open-ended SQL off operational databases.

- **Why:** Analytical scans slow transactional work, and open-ended queries can reach data in ways the application never planned for.
- **When:** Analysts or users want arbitrary SQL or heavy reports against production data.
- **Not when:** Occasional maintenance or troubleshooting queries may still be run by hand.
- **Check:** Analyst tools connect to a warehouse or replica, and production exposes no open SQL endpoint.
- **Source:** ch. 1.

### DDIA-T04: Remove single points of failure from the architecture

Find each component whose single fault would fail the whole system, and give it a replica or failover path.

- **Why:** A component without redundancy turns one machine fault into a failure of the whole system.
- **When:** Reviewing an architecture for availability or planning a highly available service.
- **Check:** The architecture review lists no component without redundancy, and replicas span separate machines or datacenters.
- **Source:** ch. 1, 2.

### DDIA-T05: Keep residency-bound data in its jurisdiction

Store and process each user's data in the jurisdiction whose residency law applies, and map each tenant to a permitted region.

- **Why:** Residency laws bind where personal data may be stored and processed.
- **When:** Residency laws apply to some or all of your users' data, or a tenant's data must stay in one jurisdiction.
- **Not when:** The applicable residency law covers only medical or financial data.
- **Check:** Storage locations or shard placement are configured per user or tenant jurisdiction.
- **Source:** ch. 1, 7.

### DDIA-T06: Move computation to where large data lives

Ship the computation to the machine that already stores a large input, rather than copying the data to workers.

- **Why:** Moving a large dataset costs more than shipping small task code, so locality keeps the job fast.
- **When:** A job processes large volumes of data stored on a distributed filesystem or other machines.
- **Check:** The job ships code to storage nodes and does not copy the full dataset to workers.
- **Source:** ch. 1, 11.

### DDIA-T07: Give each service its own database and API

Give each service its own database, and expose only its API so its internal storage can change freely.

- **Why:** A shared database couples services, so one team cannot change storage or schema without the others.
- **When:** Services must change and deploy independently of one another.
- **Check:** No two services connect to the same database schema, and clients call only public APIs.
- **Source:** ch. 1.

### DDIA-T08: Checkpoint long jobs against node failure

Write periodic checkpoints during long computations or stream jobs, and resume from the latest one after a failure.

- **Why:** Without checkpoints a failure forces the job to restart from its beginning and repeat all completed work.
- **When:** A long batch or stream job runs on a cluster where any node may fail.
- **Not when:** Continuously serving systems cannot simply pause the whole cluster this way.
- **Check:** The job writes checkpoints, and its restart path loads the latest one instead of the first input.
- **Source:** ch. 1, 11, 12.

### DDIA-T09: Track high percentiles to expose outliers

Track the 95th, 99th, and 99.9th percentiles to see how slow the worst requests are.

- **Why:** A median can look acceptable while the slowest requests stay bad, and percentiles expose them.
- **When:** A service's median looks acceptable but users still report slow responses.
- **Not when:** Stop at the 99.9th percentile unless a 99.99th percentile goal clearly justifies its cost.
- **Check:** Monitoring defines percentile series above the median, such as p95, p99, and p999, and fleet-wide percentiles sum histogram buckets.
- **Source:** ch. 2.

### DDIA-T10: Write SLOs as percentile and error targets

Write each SLO as a percentile latency target and a target share of successful requests.

- **Why:** Percentile and error targets bound the slow and failed requests that users actually see.
- **When:** Writing service level objectives or a service level agreement for a user-facing service.
- **Check:** SLO configuration lists a latency percentile target and an error-rate target.
- **Source:** ch. 2.

### DDIA-T11: Space retries with growing randomized delays

Retry with exponentially growing, randomized delays, and cap the attempts so failures do not multiply the load.

- **Why:** Immediate retries multiply the load that caused the failure and can keep an overloaded system down.
- **When:** Clients retry requests after errors or timeouts.
- **Check:** The retry loop uses growing delays with jitter, and a configured maximum attempt count caps retries.
- **Source:** ch. 2.

### DDIA-T12: Reject requests before overload builds up

Reject excess requests quickly when a server nears overload, and cap each client's share of shared resources.

- **Why:** A fast refusal lets an overloaded server recover, while queued requests let the backlog keep growing.
- **When:** A server's queueing or resource use approaches its limit.
- **Check:** Admission checks reject excess requests fast, overload responses tell clients to reduce their request rate, and per-client quotas exist.
- **Source:** ch. 1, 2.

### DDIA-T13: Inject faults to exercise recovery code

Inject faults such as killed processes, disk corruption, and network loss on purpose, in an environment that resembles production.

- **Why:** Recovery code runs rarely in normal operation, so it stays untested until a real failure reaches it.
- **When:** Recovery code runs rarely and may be untested.
- **Check:** Chaos experiments or tests kill processes and sever dependencies in an environment that mirrors production.
- **Source:** ch. 2, 9.

### DDIA-T14: Test failure paths as thoroughly as normal paths

Write tests for each error branch, and check the response to each failure as carefully as the success path.

- **Why:** Poor error handling causes many critical bugs, so untested failure branches let such bugs ship.
- **When:** Writing code that handles failures, exceptions, or timeouts.
- **Check:** Tests exercise each error branch, assert the response to each failure, and include concurrent-write bursts.
- **Source:** ch. 2, 8, 13.

### DDIA-T15: Upgrade a cluster one node at a time

Upgrade a multi-node system by restarting one node at a time while the others keep serving requests.

- **Why:** Rolling restarts keep the service available during maintenance, because the remaining nodes keep answering.
- **When:** Applying operating system patches or new versions to a cluster.
- **Check:** The upgrade procedure restarts nodes one by one and checks health before each next restart.
- **Source:** ch. 2, 9.

### DDIA-T16: Roll out changes to a small share first

Release a new version to a few nodes or a small share of traffic, check each stage, and keep a switch-back path before widening.

- **Why:** A small first stage limits the damage a faulty change can do before health checks catch it.
- **When:** Deploying a change to a production system with many users or many nodes.
- **Check:** The pipeline supports staged rollouts with health checks and a switch-back path, and config changes get the same review as code.
- **Source:** ch. 2, 5.

### DDIA-T17: Store tree-shaped data as one document

Store one-to-many data that the application reads together as a single nested document.

- **Why:** One read returns the whole tree, which avoids joins and extra round trips for data read together.
- **When:** The data is a tree that the application usually loads as a whole.
- **Not when:** Related items are numerous, or only small parts of a large document are read at a time.
- **Check:** The document nests child arrays with a fixed, documented upper bound on length.
- **Source:** ch. 3.

### DDIA-T18: Keep unbounded child collections in separate records

Store very large sets of related items as separate records, so each parent document stays small.

- **Why:** Frequent small edits to one large document are costly, and separate records avoid them.
- **When:** A parent record may have many thousands of related items.
- **Check:** The parent document has no embedded array that can grow without bound.
- **Source:** ch. 3.

### DDIA-T19: Treat duplicated values as derived data

Treat each duplicated value as derived data, and update every copy in the same transaction or in a replayable consumer.

- **Why:** A crash between two writes leaves copies that disagree, so an atomic update keeps them consistent.
- **When:** A human-readable field is copied into many records to speed up reads.
- **Check:** Code that changes the source field also updates every duplicate, in one transaction or a replayable consumer.
- **Source:** ch. 3.

### DDIA-T20: Validate commands before they become events

Check business rules in the command handler before appending an event, and make every view consumer accept every logged event.

- **Why:** Rejecting a bad command before logging keeps invalid events out of the history that every view replays.
- **When:** Handling user requests that change state in an event-sourced system.
- **Check:** The command handler checks rules before the append, view consumers never reject logged events, and rebuilds use stored inputs and skip side effects.
- **Source:** ch. 3.

### DDIA-T21: Choose compaction by read or write load

Choose size-tiered compaction for write-heavy loads and leveled compaction for read-heavy loads.

- **Why:** Each compaction strategy trades write cost against read cost, so the workload decides which cost to pay.
- **When:** Selecting an LSM compaction strategy for a table.
- **Not when:** Free disk space cannot absorb the temporary space that size-tiered merges need.
- **Check:** The compaction setting matches the table's measured read-to-write ratio on its own workload.
- **Source:** ch. 4.

### DDIA-T22: Use B-trees as the default key index

Use a B-tree by default for key lookups and range queries, and choose an LSM structure only when a benchmark on your workload favors it.

- **Why:** The index choice depends on the workload, so a default needs measurement to be overturned.
- **When:** Choosing an index structure for a relational OLTP table.
- **Not when:** The workload is write-heavy and benchmarks on it favor an LSM engine.
- **Check:** A default B-tree needs no benchmark, and an LSM choice cites a benchmark run on the application's own workload.
- **Source:** ch. 4.

### DDIA-T23: Fsync the write-ahead log before confirming writes

Flush the write-ahead log to disk with fsync before reporting a write or commit as successful.

- **Why:** Data held only in memory is lost in a crash, so only logged and flushed data counts as durable.
- **When:** A committed change must survive a crash, or an in-memory database must survive restarts.
- **Check:** Commit appends and fsyncs the log before acknowledging, and in-memory stores reload state from a log or replica at startup.
- **Source:** ch. 4, 8.

### DDIA-T24: Let old readers skip newly added fields

Make older readers skip fields that a newer writer adds, rather than rejecting the record.

- **Why:** Skipping unknown fields lets old code keep reading records that a newer writer produced.
- **When:** Older code reads records produced by a newer version of the code.
- **Check:** Tests decode records with unknown fields and assert that decoding succeeds.
- **Source:** ch. 5.

### DDIA-T25: Store a schema version with each record

Store a schema version with each record, and keep every schema version in a shared table.

- **Why:** A version tag lets readers choose the right decoder for records written under different schemas.
- **When:** Records written at different times with different schemas share one database, or two processes exchange data.
- **Check:** Stored records carry a version field, a shared table lists every version, and each connection agrees on one version before sending data.
- **Source:** ch. 5.

### DDIA-T26: Check API compatibility in both call directions

Test older clients against newer services and newer clients against older services, and make servers accept older request formats.

- **Why:** Clients and servers deploy at different times, so both directions coexist during a rollout.
- **When:** Changing an API whose clients and servers deploy at different times.
- **Not when:** Clients are outside your control, such as clients owned by other organizations. Then old requests must still work (DDIA-P5).
- **Check:** Compatibility tests run every client-version and server-version pair that can coexist.
- **Source:** ch. 5.

### DDIA-T27: Make one follower synchronous and the rest asynchronous

Configure exactly one follower as synchronous, and configure the other followers as asynchronous.

- **Why:** One synchronous follower protects acknowledged writes, while making all followers synchronous lets one outage block every write.
- **When:** Choosing replication modes for a database with several followers.
- **Check:** Replication configuration marks exactly one follower as synchronous and the rest as asynchronous.
- **Source:** ch. 6.

### DDIA-T28: Fence the old leader after failover

Block the old leader's writes once a new leader is chosen, and promote the replica with the most recent changes.

- **Why:** The old leader may still run and accept writes, so two leaders must never accept writes at once.
- **When:** Failover is complete and the old leader might still be running, or it rejoins the cluster.
- **Check:** Failover blocks the old leader's writes, rejoin checks current leadership before accepting writes, and promotion picks the newest replica.
- **Source:** ch. 6.

### DDIA-T29: Read your own writes from the leader briefly

After a user writes, route that user's reads to the leader for a short window, or to a replica past their last write position, not a wall-clock time.

- **Why:** Asynchronous followers and derived views may lag, so a user could read stale data after their own update.
- **When:** Users view data they have just submitted or updated.
- **Check:** Clients carry their last write position, followers past a set lag threshold are excluded, and reads wait or redirect when a replica is behind it.
- **Source:** ch. 6, 13.

### DDIA-T30: Use last-write-wins for harmless concurrent losses

Use last-write-wins only where silently discarding some concurrent writes is acceptable, and avoid it for critical updates.

- **Why:** The winner is picked arbitrarily, so the losing concurrent write leaves no trace.
- **When:** A replicated database resolves concurrent writes to one record by last-write-wins.
- **Not when:** Lost updates are not acceptable to the application.
- **Check:** The replication configuration shows the conflict policy per dataset, critical datasets use another policy, and equal timestamps break ties by a fixed value comparison.
- **Source:** ch. 6, 8.

### DDIA-T31: Make W plus R exceed N

Choose read and write replica sets that overlap for reads that need fresh values, and use W plus R greater than N to guarantee overlap.

- **Why:** Every read set then shares a replica with every successful write set, so a read reaches the latest successful write.
- **When:** Configuring a quorum store for reads that need fresh values.
- **Not when:** Overlap does not make concurrent operations linearizable, so use DDIA-T45 for that.
- **Check:** Configuration validates that W plus R is greater than N for each read that needs fresh values.
- **Source:** ch. 6, 10.

### DDIA-T32: Choose the partition key deliberately

Declare an explicit partition key for each sharded table, and send each object's log updates to the shard for its object ID.

- **Why:** Records sharing a key land in one shard, and a query without the key must search every shard.
- **When:** Defining the partition key for a sharded table, collection, or key-value namespace.
- **Not when:** Range queries need the original key order.
- **Check:** The schema declares a partition key per table, hashes keys unless range queries need their order, and range keys never lead with a timestamp.
- **Source:** ch. 7, 13.

### DDIA-T33: Group related writes into one transaction

Put writes that must succeed or fail together inside one transaction.

- **Why:** Partial completion of related writes leaves data inconsistent, while a transaction applies all of them or none.
- **When:** An operation changes several records that depend on each other.
- **Not when:** A single document update covers the write, or a derived index or view can update after the commit. Writes spanning several systems follow DDIA-P8.
- **Check:** Related statements sit between one BEGIN and COMMIT, not in separate autocommit calls, and no external call or user wait sits inside.
- **Source:** ch. 8, 13.

### DDIA-T34: Choose isolation by the anomalies it allows

Choose an isolation level weaker than serializable only after naming the race conditions it allows, and review them against the risks.

- **Why:** Weaker levels are cheaper to run but allow specific races, so the application's tolerance decides the level.
- **When:** Serializable isolation costs too much throughput, or an isolation level is set for transactions.
- **Check:** Design notes write down the anomalies the chosen level allows and the vendor's meaning of its name, recording each accepted race.
- **Source:** ch. 8.

### DDIA-T35: Retry aborted transactions only for transient errors

Retry aborted transactions only for transient errors such as deadlock or failover, with capped attempts and exponential backoff.

- **Why:** Permanent errors cannot succeed on retry, and unbounded retries under contention add load to a failing system.
- **When:** A transaction fails with an error that the application can classify.
- **Not when:** The error is permanent, such as a constraint violation.
- **Check:** Retry logic separates transient from permanent errors, caps attempts with backoff, handles overload separately, and adds retries where the framework does not.
- **Source:** ch. 8.

### DDIA-T36: Guard every read-modify-write cycle

Protect every read-modify-write cycle with an atomic operation, a lock, a conditional write, or lost-update detection.

- **Why:** A separate read and write lets a concurrent update be overwritten, so one change is lost.
- **When:** Code reads a value, changes it in the application, and writes it back.
- **Not when:** Free-text edits, such as wiki page changes, do not fit atomic operations, so guard them with a conditional write.
- **Check:** Each path names its guard, counters use one statement such as value = value + 1, and repeatable read is no guard.
- **Source:** ch. 8.

### DDIA-T37: Check decisions over several rows for write skew

Run a decision that reads several rows at serializable isolation, or lock the rows its check reads.

- **Why:** Snapshot isolation lets two transactions pass the same check and write different rows, which breaks the rule.
- **When:** A transaction reads several rows and then writes other rows based on that check.
- **Check:** The transaction runs at serializable isolation or explicitly locks the rows its check reads.
- **Source:** ch. 8.

### DDIA-T38: Enforce unique values with uniqueness constraints

Enforce unique values with a uniqueness constraint and handle its violation error, instead of a check followed by an insert.

- **Why:** Two requests can both pass a check before either inserts, so only a database constraint stops both.
- **When:** Two users might claim the same value at the same time, such as a username.
- **Not when:** Several asynchronous leaders or shards may accept writes for the same value, so DDIA-T54 applies instead.
- **Check:** The schema has a unique index on the field, and code handles the constraint violation error.
- **Source:** ch. 8.

### DDIA-T39: Confirm success with an application-level reply

Treat a request as successful only when the application that handled it returns a positive reply, not when TCP acknowledges the data.

- **Why:** A transport acknowledgment shows that bytes arrived, not that the remote application processed them.
- **When:** Deciding whether a remote request was processed successfully.
- **Check:** Success is detected from an application-level reply, not from a socket or TCP acknowledgment.
- **Source:** ch. 9.

### DDIA-T40: Define and test handling for each network fault

Specify how software behaves during each network fault, and test that it recovers after the network is repaired.

- **Why:** Untested fault paths can deadlock or destroy data, so each response must be defined in advance.
- **When:** Software depends on other nodes or networked components.
- **Check:** Fault tests assert recovery after a partition heals, timeouts come from measured round-trip times, and nodes are declared dead only after retries.
- **Source:** ch. 9.

### DDIA-T41: Measure durations with a monotonic clock

Measure timeouts and response times with a monotonic clock, not by subtracting wall-clock readings.

- **Why:** Time-of-day clocks can jump backward when time sync resets them, which makes durations wrong.
- **When:** Calculating elapsed time between two events on one machine.
- **Not when:** You need a calendar date or a time of day to show users.
- **Check:** Duration code reads a monotonic clock API, never subtracts wall-clock readings, and never sends monotonic readings to other machines.
- **Source:** ch. 9.

### DDIA-T42: Recheck a lease at the point of action

Recheck lease validity immediately before the critical action, because a thread can pause between the check and the action.

- **Why:** A paused process can resume after its lease expired, so a check before the action is not enough.
- **When:** A lease check happens shortly before a critical action.
- **Check:** The critical action revalidates the lease or uses a fencing token, and tests inject pauses between steps.
- **Source:** ch. 9.

### DDIA-T43: Fence writes with increasing tokens

Attach a token that increases with each lock grant, take it from the lock service counter, and have storage reject older tokens.

- **Why:** A former leaseholder may still write, and only the storage layer can refuse its stale token.
- **When:** Protecting a shared resource from a former leaseholder.
- **Not when:** Storage cannot compare tokens. Then recheck the lease at the point of action (DDIA-T42).
- **Check:** The storage write path rejects tokens lower than the highest seen, and tokens come from the lock service counter.
- **Source:** ch. 9.

### DDIA-T44: Choose consistency from replica connectivity

Choose strong consistency for replicas in well-connected datacenters.

- **Why:** Strong consistency needs fast, reliable links between replicas, which slow or unreliable links cannot provide.
- **When:** Picking a consistency model for replicas.
- **Not when:** Strong consistency costs performance, and faults that eventual consistency tolerates would then cause outages.
- **Check:** Design notes tie a strong-consistency choice to measured link latency and reliability.
- **Source:** ch. 10.

### DDIA-T45: Send linearizable operations to the leader

Route linearizable reads and writes to the leader, and refuse leader-only operations on a node that lacks a current lease or epoch.

- **Why:** Serializable isolation alone can return stale reads, and a deposed node may not know it lost leadership.
- **When:** Single-leader replication must give linearizable access to a dataset.
- **Not when:** Clients cannot know for sure who the leader is.
- **Check:** Linearizable paths route only to the leader, a deposed node refuses leader-only operations, and a new leader applies all committed entries before serving.
- **Source:** ch. 10.

### DDIA-T46: Write batch output to new locations, then regenerate

Read batch inputs without changing them, write results to new output, and rebuild that output fully on every run.

- **Why:** Untouched inputs let a bad run be repeated, and full rebuilds avoid patching stale output.
- **When:** Designing a job that transforms an existing dataset, or deciding whether to patch previous output.
- **Check:** Tasks write only to a new output location, never overwrite inputs, and a retry deletes earlier partial output.
- **Source:** ch. 11.

### DDIA-T47: Repair bad batch output by rerunning fixed code

Roll back buggy batch code, fix the transformation or its upstream job, and rerun the job to repair its output.

- **Why:** Batch output is derived, so a rerun from retained inputs replaces bad output with correct output.
- **When:** A deployed batch job wrote wrong output, or an ETL output has wrong or missing fields.
- **Not when:** The buggy job wrote to an operational database, which rollback does not repair.
- **Check:** Deployment history allows redeploying an earlier job version, and the rerun regenerates affected output from retained inputs.
- **Source:** ch. 11.

### DDIA-T48: Commit consumer offsets periodically

Record a log consumer's offset in batches rather than per message, and make processing after a restart idempotent.

- **Why:** Per-message commits cost throughput, so consumers accept reprocessing the messages since the last commit.
- **When:** Consuming a log shard sequentially at high throughput.
- **Check:** Consumers commit offsets in batches, acknowledgments follow processing, and post-restart processing is idempotent or deduplicates by offset.
- **Source:** ch. 12.

### DDIA-T49: Let the database order writes for derived systems

Make the source database the order of all writes, and feed each derived store from its change log in log order.

- **Why:** One ordering point means derived stores apply changes in the same order as the original writes.
- **When:** Several derived stores must match one source database.
- **Check:** Derived stores receive changes from the database log, not direct application writes, and apply them in log order.
- **Source:** ch. 12.

### DDIA-T50: Publish events through an outbox row

Publish events through an outbox table with its own schema, written in the same transaction as the domain change.

- **Why:** A row committed with the domain change means no event is lost or sent for an uncommitted change.
- **When:** Internal schemas must change freely while downstream consumers stay stable.
- **Not when:** Maintaining the transformation and the extra writes is too costly.
- **Check:** An outbox table exists, the insert shares a transaction with the domain write, and CDC reads the outbox.
- **Source:** ch. 12.

### DDIA-T51: Window stream events by event timestamps

Assign events to windows using their embedded timestamps, not the processing machine's clock.

- **Why:** Event time gives the same windows on a rerun or a backlog replay, while processing time does not.
- **When:** Stream analytics groups events by time, including replays of a backlog or historical reruns.
- **Not when:** Processing delay is negligible, or device clocks cannot be trusted and the server receive time is used instead.
- **Check:** Window assignment reads the event's timestamp field, not the clock at arrival.
- **Source:** ch. 12, 13.

### DDIA-T52: Make writes idempotent with stored input offsets

Store the source offset with each written value so duplicates are detected, and verify replay order and single writers first.

- **Why:** Replays after a failure repeat writes, and a stored offset lets the writer recognize and skip them.
- **When:** Writing from a log-based broker to an external database.
- **Check:** Stored rows include the last applied offset, and design notes list the replay, determinism, and single-writer assumptions.
- **Source:** ch. 12.

### DDIA-T53: Route all user input through one ordering point

Send all user input through one system that decides a total order.

- **Why:** A single decided order gives every derived representation the same history to reproduce.
- **When:** Several storage systems must hold consistent representations of the same data.
- **Not when:** Events from different shards, regions, or services share no global order, and causal dependencies across objects need a causal mechanism (DDIA-P4).
- **Check:** Each derived store is fed from a change log or event stream, not from direct application writes.
- **Source:** ch. 13.

### DDIA-T54: Enforce uniqueness at one decision point

Route every request for one unique value or limited quantity to a single node or shard that decides it.

- **Why:** Uniqueness needs one place that decides, because independent leaders can accept conflicting values.
- **When:** Enforcing unique usernames, email addresses, or request IDs.
- **Not when:** Loose constraints that can be fixed later tolerate multi-leader replication.
- **Check:** Each unique key or limited quantity has exactly one node or shard that accepts or rejects writes for it.
- **Source:** ch. 10, 13.

### DDIA-T55: Carry a client request ID end to end

Generate a request ID at the client, pass it through every layer and event, and ignore repeats of it.

- **Why:** A retry after a timeout otherwise looks like a new request, so only the carried ID reveals the repeat.
- **When:** A user operation may be submitted again after a timeout or lost response, across a multi-stage pipeline.
- **Check:** Write requests carry a client-generated ID that the database stores under a unique constraint, and processors skip handled IDs.
- **Source:** ch. 13.

### DDIA-T56: Coordinate only where recovery is impossible

Add synchronous coordination only to constraints that cannot be repaired afterward, and weigh apologies against outage risk.

- **Why:** Coordination reduces availability, so it is worth paying only where no later repair exists.
- **When:** Designing constraints in a system that spans several datacenters, or choosing how strictly to enforce one.
- **Check:** Synchronous cross-region calls appear only on paths with irreversible effects, and the design records expected apologies beside availability cost.
- **Source:** ch. 13.

### DDIA-T57: Checksum data across the whole path

Compute a checksum where the application first has the data, store it with the data, and verify it on every read.

- **Why:** Lower-layer checksums in network and disk protocols miss corruption introduced by software bugs along the path.
- **When:** Data crosses many components or is stored for long periods.
- **Not when:** Lower-layer checksums in Ethernet, TCP, and TLS do not replace end-to-end checks.
- **Check:** The application stores a checksum with the data and verifies it when reading.
- **Source:** ch. 13.

### DDIA-T58: Check who bears the cost of wrong rejections

Weigh how a wrong rejection harms the person it excludes, and state who pays for each kind of error when setting a threshold.

- **Why:** A decision threshold moves errors onto people, so the harm of a false rejection must be counted beside accuracy.
- **When:** Building models that gate jobs, loans, insurance, travel, or housing, or choosing accept-or-reject thresholds.
- **Check:** Model risk review names the excluded groups, and threshold configuration states how false accepts and false rejects are weighted.
- **Source:** ch. 14.

### DDIA-T59: Inspect training inputs for systematic bias

Inspect training inputs for systematic bias, and treat past decisions used as labels as possibly discriminatory until reviewed.

- **Why:** Models learn and amplify bias in their inputs, and past decisions often carry the same bias as their labels.
- **When:** Training models on records about people, or on past decisions about people.
- **Check:** Dataset docs include a bias analysis of inputs, and feature review checks postal code and IP address for correlation with protected traits.
- **Source:** ch. 14.

### DDIA-T60: Append corrections instead of overwriting history

Record every change, correction, and raw input as a new appended record, never by editing or deleting the original.

- **Why:** Original records are the evidence needed to recover from bugs or study change over time.
- **When:** Data must be recoverable after application bugs, or analysts need its history over time.
- **Not when:** Erasure of personal data on request follows DDIA-T61 instead.
- **Check:** Outside erasure requests, no update or delete statement changes a logged or stored input, and corrections are inserts.
- **Source:** ch. 1, 3, 13.

### DDIA-T61: Plan erasure through every copy of personal data

Design erasure so every copy of personal data, including logs and derived datasets, can be deleted on request.

- **Why:** Append-only logs and derived datasets keep old copies, so deleting only the primary record fails the request.
- **When:** Personal data must be erased on request from an append-only or derived store.
- **Check:** Erasure rewrites stored records in logs and derived datasets, and events hold IDs instead of personal fields.
- **Source:** ch. 1, 3, 12.
