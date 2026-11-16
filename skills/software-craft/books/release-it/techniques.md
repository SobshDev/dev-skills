# Release It! — techniques

### RI-T01: Confirm operations can run the system alone
Confirm that operations staff can run and recover the system without its developers.
- **Why:** Operators live with the system after release, so they must keep it running without its builders.
- **When:** Before handing a system to operations or releasing it to production.
- **Check:** Runbooks, deployment steps, and alerts exist for operations staff, not only for developers.
- **Source:** ch. 1 p. 15

### RI-T02: Judge release readiness by production conditions
Judge release readiness with load, failure, and operations checks, not QA test results alone.
- **Why:** QA tests cover an artificial setting, and only production conditions show whether a system survives.
- **When:** Deciding whether a system is ready to release.
- **Check:** Release criteria include load, failure, and operations checks beyond feature test results.
- **Source:** ch. 1 p. 16

### RI-T03: Restore service before root-cause analysis
During a customer-facing outage, restore service first and investigate the cause afterwards.
- **Why:** Diagnosis while customers are down extends the outage that customers feel.
- **When:** During a live outage that affects customers.
- **Not when:** Collecting postmortem data is acceptable only if it does not lengthen the outage.
- **Check:** The incident runbook lists service restoration as its first step, before log collection or analysis. (Verify in runbook files.)
- **Source:** ch. 2 p. 25

### RI-T04: Script diagnostic capture before incidents
Script the capture of thread dumps and database state so responders do not improvise during incidents.
- **Why:** Capture that does not prolong an outage still gives the postmortem evidence it needs.
- **When:** Preparing runbooks and tooling for production services.
- **Not when:** Capture that would lengthen a live outage waits until service is restored (RI-T03).
- **Check:** Incident scripts collect thread dumps and database state without manual steps.
- **Source:** ch. 2 p. 25

### RI-T05: Read thread dumps for blocked calls
When a Java application hangs, read a thread dump for pool threads blocked in calls.
- **Why:** A dump shows which call each thread is stuck in while the application hangs.
- **When:** Diagnosing a Java application that hangs or stops responding.
- **Not when:** Dumps wait while a live outage still needs service restored first (RI-T03).
- **Check:** The dump notes name each blocked pool thread and its blocking stack frame.
- **Source:** ch. 2 p. 29

### RI-T06: Do not trust connections that report open
Handle statement errors on pooled connections even when the connection reports open.
- **Why:** An open status does not prove the connection can run statements after a failover.
- **When:** Using a pooled connection after network or failover events.
- **Check:** Statement calls on pooled connections have error handling, and the code does not skip it based on connection status.
- **Source:** ch. 2 p. 33

### RI-T07: Write a targeted test for the diagnosed failure
After diagnosing a failure, write a test that exercises that exact failing path.
- **Why:** Regression tests stop a diagnosed failure from returning unnoticed.
- **When:** A root cause is identified and the regular tests missed it.
- **Check:** A regression test covers the diagnosed exception path.
- **Source:** ch. 2 p. 34

### RI-T08: Choose the design that behaves better under failure
When both designs meet the functional requirements, choose the one that behaves better under failure.
- **Why:** The book says the stable option usually costs about the same to build.
- **When:** Choosing between designs that both meet the functional requirements.
- **Check:** Design records compare how each option behaves under failure, not only its features.
- **Source:** ch. 3 p. 36

### RI-T09: Run steady longevity load on a spare machine
Run a steady load for days on a spare machine, with scheduled idle periods, to expose longevity bugs.
- **Why:** Long runs reveal leaks and growth that short tests cannot show.
- **When:** Testing for longevity bugs before release, when a spare machine is available.
- **Check:** A long-running load job with idle periods and logged uptime and memory figures exists.
- **Source:** ch. 3 p. 38

### RI-T10: Keep must-work features off optional calls
Name the features that must keep working during partial failures, and keep their request paths free of calls to optional components.
- **Why:** Failures in optional parts then cannot stop the features the business cannot lose.
- **When:** Deciding which features must keep working during partial failures.
- **Check:** Request code for each named feature has no calls to optional components.
- **Source:** ch. 3 p. 39

### RI-T11: Give request-reply messages an expiry path
Give request-reply exchanges over message queues a timeout or expiry path.
- **Why:** Without an expiry, a reply that never arrives leaves the requester waiting indefinitely.
- **When:** Using message queues for request-reply interaction.
- **Check:** Reply-waiting code has a timeout or expiry path.
- **Source:** ch. 3 p. 40

### RI-T12: List each failure mode of external calls
List how each external call or I/O can fail, including no response and slow response.
- **Why:** No response and slow response are failures that must be listed too, not only error results.
- **When:** Writing or reviewing code that calls an external system or I/O.
- **Not when:** Exhaustive enumeration is impractical, except in life-critical systems, where it is expected.
- **Check:** Error handling and tests cover refusal, timeouts, missing, malformed, reset, and oversized responses.
- **Source:** ch. 3, 5 p. 41

### RI-T13: Give pool waits a time limit
Give every wait for a pooled resource a maximum time, and handle the timeout path.
- **Why:** Unlimited waits let blocked threads accumulate behind one exhausted pool.
- **When:** Configuring connection or thread pools, or checking out from them.
- **Check:** Pool checkout calls pass a maximum wait time, and their timeout path is handled.
- **Source:** ch. 3 p. 39, ch. 4 p. 63

### RI-T14: Set explicit read and write timeouts on sockets
Set explicit timeouts for reading responses and for sending request bodies on every socket.
- **Why:** Socket reads and writes otherwise block for as long as the peer stays silent, often indefinitely.
- **When:** Writing code that reads from or writes to sockets or remote protocols.
- **Check:** Socket and HTTP client code sets read and request-write timeouts explicitly, not the infinite default.
- **Source:** ch. 4 p. 49

### RI-T15: Branch on status and content type before parsing
Check the status and content type of each remote response before reading its fields.
- **Why:** A reply in an unexpected form breaks code that assumes the success format.
- **When:** Parsing responses from HTTP or other external services.
- **Check:** Response handling branches on status and content type before deserializing the body.
- **Source:** ch. 4 p. 55

### RI-T16: Fix the defect behind a chain reaction
When one defect repeatedly crashes nodes under load, fix that defect in code instead of only adding limits.
- **Why:** Limiting spread leaves the defect in place, so the same chain reaction can restart.
- **When:** The same defect keeps failing servers one after another under the same load.
- **Not when:** Partitioning only splits one chain reaction into two that run at different rates.
- **Check:** The change alters the code path named in the incident record, not only limit settings.
- **Source:** ch. 4 p. 59

### RI-T17: Wrap dependency calls in timeouts and breakers
Wrap every outbound call whose failure could drain caller threads or pools in a timeout and a circuit breaker that counts timeouts as failures.
- **Why:** The book names timeouts and circuit breakers as the most effective defenses against cascading failure.
- **When:** Any call whose failure could drain the caller's threads or resource pools.
- **Check:** Each such call has a timeout and a breaker that counts timeouts, or a named equivalent mechanism.
- **Source:** ch. 4, 5 p. 62

### RI-T18: Keep in-memory session contents small
Keep in-memory session attributes small, holding identifiers or scalar values rather than full result sets.
- **Why:** Every session lives in server memory, so each session should hold as little as possible.
- **When:** Storing user data in server-side web sessions.
- **Check:** Session attributes hold identifiers or scalar values, not lists or full result sets. Checkout state is referenced by ID, not copied (RI-T56).
- **Source:** ch. 4 p. 64

### RI-T19: Build shared concurrency on library primitives
Build shared concurrency code from a library class, not from a home-built pool or queue.
- **Why:** A small set of well-known primitives used in known patterns is safer than custom concurrency code.
- **When:** Writing pools, queues, or other shared concurrency code.
- **Check:** Shared concurrency code uses a library class rather than a home-built pool or queue.
- **Source:** ch. 4 p. 76

### RI-T20: Keep remote calls out of locked sections
Keep remote calls out of synchronized sections, and never let one lock serialize every call through a breaker.
- **Why:** A remote call made while holding a lock keeps every other waiting thread blocked for its duration.
- **When:** Implementing a cache, registry, or breaker that calls a remote system.
- **Check:** No synchronized method or lock wraps a remote call, and breaker state does not serialize calls.
- **Source:** ch. 4, 5 p. 78

### RI-T21: Put a queue before a shared resource
Put a queue or buffer between callers and a shared resource that cannot be avoided.
- **Why:** The buffer absorbs bursts, so the shared resource sees a steadier demand.
- **When:** A shared resource cannot be avoided.
- **Check:** Calls to the shared resource pass through a queue or buffering component.
- **Source:** ch. 4 p. 82

### RI-T22: Set explicit timeouts on every integration call
Give every call to another system an explicit timeout so that the caller eventually stops waiting.
- **Why:** A caller without a timeout can wait forever for a response that never comes.
- **When:** Code calls a remote service, API, database, or other integration point.
- **Check:** Each outbound client call in the diff passes a timeout, and none can wait indefinitely.
- **Source:** ch. 5 p. 103

### RI-T23: Wait before retrying a failed remote operation
Wait, back off, or defer before retrying a failed remote operation.
- **Why:** A remote problem inside a data center tends to persist, so an immediate retry usually fails too.
- **When:** A remote call fails or times out inside a data center.
- **Not when:** Transient problems such as dropped packets over a WAN may clear with a retry.
- **Check:** Retry code waits before each attempt, and retries only documented transient errors with a bounded count.
- **Source:** ch. 4, 5 p. 105

### RI-T24: Fail calls at once when breaker open
While a circuit breaker is open, fail calls immediately with an exception type distinct from timeouts, without executing the real operation.
- **Why:** Skipping the failing operation spares the caller the wait and the dependency the load.
- **When:** A breaker has tripped after too many failures.
- **Check:** The open-state path throws a distinct exception type, without invoking the dependency.
- **Source:** ch. 5 p. 108

### RI-T25: Log and expose breaker state changes
Log every circuit breaker state change, and expose the current state for queries.
- **Why:** Operators and monitoring need to see when a breaker trips, resets, or tests recovery.
- **When:** A breaker trips, resets, or moves to half-open, or monitoring queries it.
- **Check:** State transitions emit log entries or metrics, and a state query method exists.
- **Source:** ch. 5 p. 109

### RI-T26: Return 503 for temporary overload
Return HTTP 503 when a web service is temporarily overloaded and expects to recover soon.
- **Why:** A 503 tells clients the condition is temporary, unlike a generic error code.
- **When:** A web service is busy and expects to recover soon.
- **Not when:** Many clients treat any non-success status as fatal, so a 503 may not help them.
- **Check:** Overload responses use status 503, not a generic error code.
- **Source:** ch. 5 p. 123

### RI-T27: Emulate the remote end with a harness
Build a separate test server that stands in for the remote end of each integration point.
- **Why:** A stand-in that fails the way a real peer fails shows how the system copes with those failures.
- **When:** Testing local failure handling without the real dependency.
- **Check:** Test configuration points the integration client at a harness endpoint.
- **Source:** ch. 5 p. 126

### RI-T28: Shed load when response times exceed the SLA
Measure response times against the service-level target (SLA), and refuse new requests while they exceed it.
- **Why:** Serving every request slowly misses the service level for all of them.
- **When:** A service can observe its own latency and must protect its service level.
- **Check:** Load shedding triggers on latency measured against the SLA target.
- **Source:** ch. 5 p. 132

### RI-T29: Separate inbound and outbound thread pools
Accept inbound requests on one thread pool, and run blocking outbound or library calls on another with a caller-side timeout.
- **Why:** The request thread can time out and reply while the outbound call is still blocked.
- **When:** An inbound request depends on a blocking outbound call.
- **Not when:** Wrapping calls can grow into a reactive wrapper around the whole client library.
- **Check:** Blocking outbound calls run on an executor separate from request-handling threads, with a timeout.
- **Source:** ch. 4, 5 p. 134

### RI-T30: Disable a feature with a zero pool limit
Set a non-essential dependent feature's pool maximum to zero to disable it during an incident.
- **Why:** A runtime pool limit disables the dependency without a code change or deployment.
- **When:** Disabling a non-essential dependency during an incident.
- **Not when:** Do not use zero when the feature must stay available under heavy load, since zero disables it fully and one keeps it available.
- **Check:** The pool maximum is runtime-adjustable, and callers show a fallback for an unavailable dependency.
- **Source:** ch. 6 p. 147

### RI-T31: Verify a runtime configuration change took effect
After a runtime configuration change, read the setting back or confirm the new behavior.
- **Why:** A change the running component never applied gives a false sense of control during an incident.
- **When:** Applying a live configuration change to a running component.
- **Not when:** Settings read only at startup need a component restart before they apply.
- **Check:** The change procedure reads the setting back or observes the new behavior, and any restart comes before that check.
- **Source:** ch. 6 p. 148

### RI-T32: Keep container state in external storage
Write durable files, data, and caches outside the container.
- **Why:** Data kept outside the container lets the container be replaced without losing it.
- **When:** Designing a service that runs in containers.
- **Check:** Durable data is written to external storage, not to container-local paths.
- **Source:** ch. 7 p. 158

### RI-T33: Start quickly and shut down gracefully
Design the process to start within a set time goal and to shut down gracefully on termination signals.
- **Why:** Graceful shutdown finishes work already in flight, rather than cutting it off.
- **When:** Writing startup and shutdown handling.
- **Check:** Shutdown handles termination signals and finishes in-flight work.
- **Source:** ch. 7 p. 160

### RI-T34: Automate deployments from a versioned definition
Keep the deployment definition in source control, and create new installations from it.
- **Why:** A versioned definition repeats the same way on every machine, unlike hand-run steps.
- **When:** Defining how a new installation is created on a machine. Repeated release steps are RI-T45.
- **Check:** Deployment steps live in a versioned file, not in manual runbooks.
- **Source:** ch. 8 p. 165

### RI-T35: Name the exact unit that a restart affects
Name in each restart instruction whether it restarts a process, an instance, or a whole machine.
- **Why:** Operators act on the wording, so an unclear unit changes what actually gets restarted.
- **When:** Writing runbooks or asking someone to restart something.
- **Check:** Runbook steps name the process, instance, or machine they act on.
- **Source:** ch. 8 p. 166

### RI-T36: Find the first queue that backs up
Identify the first queue that backs up when a system slows down.
- **Why:** Queue depth shows where a slowdown begins, so the first backed-up queue locates the failure.
- **When:** A system slows down and you need to find where it starts failing.
- **Check:** Monitoring exposes queue depth for each tier of the request path.
- **Source:** ch. 9 p. 191

### RI-T37: Reject overload quickly instead of timing out
Reject overloaded requests immediately instead of letting callers wait for a timeout.
- **Why:** A quick rejection frees the caller sooner than a slow timeout would.
- **When:** Queues are full or response times exceed the service objective.
- **Check:** The overload path returns an immediate error without blocking.
- **Source:** ch. 9 p. 193

### RI-T38: Handle failed writes after a failover
Catch and handle database errors on writes that fail during a failover.
- **Why:** Drivers do not repeat updates, inserts, or stored procedure calls automatically.
- **When:** Database calls go through a failover virtual IP.
- **Check:** Write paths catch and handle the database error raised during a failover.
- **Source:** ch. 9 p. 199

### RI-T39: Measure user experience with real-user monitoring
Measure user experience directly with real-user monitoring, not only with instance metrics.
- **Why:** Instance metrics infer user experience, while client-side measurement records it directly.
- **When:** Deciding how to learn whether users are well served.
- **Check:** Client applications report timing and failures to a central collector.
- **Source:** ch. 10 p. 208

### RI-T40: Expose a runtime control that resets breakers
Expose a runtime control that resets circuit breakers.
- **Why:** A reset returns an integration to service once the fault has cleared.
- **When:** Operators must restore an integration after a fault clears.
- **Not when:** The service has no circuit breakers, so no reset control applies.
- **Check:** The admin API includes a breaker reset operation.
- **Source:** ch. 10 p. 218

### RI-T41: Omit schema and reseed endpoints from production admin
Leave schema-change, delete-and-reseed, and whole-cache flush controls out of the production admin API, though breaker resets (RI-T40) stay allowed.
- **Why:** The book calls such operations hazardous in production.
- **When:** Designing admin controls for a production service.
- **Check:** The production admin API has no endpoints that alter schema, delete data, or flush a whole cache.
- **Source:** ch. 10 p. 218

### RI-T42: Bind every query value as a placeholder
Pass user-supplied values to queries as bound placeholders, never as concatenated text.
- **Why:** The book says SQL injection has no excuse today, so query values must never be concatenated.
- **When:** Building any database query that includes a value from users or from stored data.
- **Check:** Query code contains no string concatenation of variables, and values are bound as parameters.
- **Source:** ch. 11 p. 224

### RI-T43: Replace default credentials before production
Replace every default password on databases, consoles, and base images before production use.
- **Why:** The book says a default password must never remain on a production server.
- **When:** Installing servers, databases, admin consoles, or container base images.
- **Check:** Deployment config or scripts set new admin credentials, and no default logins remain.
- **Source:** ch. 11 p. 233

### RI-T44: Send credentials only over TLS
Send credentials over TLS, never over plain HTTP.
- **Why:** Credentials sent in the clear can be read by anyone who can see the traffic.
- **When:** Exposing web services or connecting services that exchange credentials.
- **Check:** Credential-bearing clients and endpoints use https URLs only.
- **Source:** ch. 11 p. 227

### RI-T45: Replace manual deployment steps with scripts
Replace repeated manual deployment steps with scripts or pipeline stages kept in version control.
- **Why:** Hand-run steps vary between runs and people, while scripted steps repeat the same way each time.
- **When:** A release relies on people repeating manual steps on machines already set up. Installation definitions are RI-T34.
- **Check:** Repeated deployment steps appear as scripts or pipeline stages in version control.
- **Source:** ch. 12 p. 246

### RI-T46: Let old and new versions run together
Make code and data changes tolerate old and new versions running at the same time.
- **Why:** During a rolling deployment, both versions serve traffic until the rollout finishes.
- **When:** Changing the system through a rolling deployment.
- **Check:** Code and data changes tolerate both old and new versions running at the same time.
- **Source:** ch. 13 p. 248

### RI-T47: Roll out the application before its data migration
Deploy the new application version before any data migration that old instances cannot read, with additive schema changes applied earlier (RI-P7).
- **Why:** Old instances must keep working while documents are migrated.
- **When:** Migrating documents while old instances are still running.
- **Not when:** Old instances can still read the migrated data, since such copies may run before rollout (RI-P7).
- **Check:** The deployment order runs the application rollout before the migration job.
- **Source:** ch. 13 p. 260

### RI-T48: Remove temporary sync triggers only after full rollout
Remove the temporary database triggers that keep old and new schemas in sync, in a later migration, after every instance runs the new code.
- **Why:** A temporary trigger keeps old and new schemas in sync, so it is needed until no old instance remains.
- **When:** Starting the cleanup phase of a deployment.
- **Check:** Trigger removal sits in its own later migration.
- **Source:** ch. 13 p. 265

### RI-T49: Add NOT NULL and foreign keys after rollout
Add NOT NULL and foreign key constraints only after the new code is fully rolled out.
- **Why:** A constraint added earlier would reject writes that old instances still make.
- **When:** Tightening a schema after a change set has rolled out.
- **Check:** Constraint migrations appear in a later release than the code that needed them.
- **Source:** ch. 13 p. 266

### RI-T50: Treat stricter request rules as breaking changes
Treat any new required request field, or any rule that rejects input earlier versions accepted, as a breaking change.
- **Why:** Old consumers cannot supply a field that did not exist when they were built.
- **When:** Changing a request format that consumers already send.
- **Check:** The schema diff shows no new required field, and new validation accepts prior test inputs.
- **Source:** ch. 14 p. 271

### RI-T51: Write contract tests for used provider behavior
Write contract tests in the consumer repository for every provider behavior your code relies on.
- **Why:** Contract tests catch provider changes that would break what consumers depend on.
- **When:** Consuming a shared data format or API owned by another team.
- **Check:** The consumer repository has contract tests that run against the provider's staging system.
- **Source:** ch. 14 p. 273

### RI-T52: Put a format version in every message
Put a format version number in every request and response message.
- **Why:** A version field lets readers dispatch to the right translator as formats evolve.
- **When:** Designing request and response message formats.
- **Check:** Each message schema includes a version field.
- **Source:** ch. 14 p. 274

### RI-T53: Replace a stack in several cutover steps
Replace the components of a system in several cutover steps, each moving traffic or data to a new component, not all at once.
- **Why:** Nobody can be sure how a new stack behaves in production, so a whole-stack cutover multiplies the risk.
- **When:** A project plans to replace all components of a system at the same time.
- **Check:** The release plan contains more than one step where traffic or data moves to the new component.
- **Source:** ch. 15 p. 283

### RI-T54: Keep session-free requests off session servers
Route requests that need no session, such as unknown URLs, away from session-creating servers.
- **Why:** Requests that only return errors should not create sessions on servers that carry real users.
- **When:** Crawlers or old links request URLs that will only return errors.
- **Check:** Routing sends 404 responses and static assets without creating server sessions.
- **Source:** ch. 15 p. 288

### RI-T55: Throttle new sessions during overload
Admit only a configured percentage of new sessions through the gateway while servers are overloaded.
- **Why:** The throttle keeps servers from saturating, so the admitted traffic can still be served.
- **When:** Load rises beyond what the servers can serve without saturating.
- **Check:** The percentage is a setting that operators can lower without a deploy.
- **Source:** ch. 15 p. 291

### RI-T56: Keep checkout state through failover
Keep session failover working so a customer mid-checkout can finish after an instance fails.
- **Why:** Without failover, a customer whose instance fails loses the checkout in progress.
- **When:** Sessions are bound to one instance and failover restores them on another.
- **Check:** Failover restores the cart and checkout step on another instance after a failure.
- **Source:** ch. 15 p. 292

### RI-T57: Depend on service names, not instances
Reach another cluster through its virtual IP or DNS name, never through individual instances.
- **Why:** The service name stays stable while the instances behind it come and go.
- **When:** A service configures the address of a dependency.
- **Check:** Config holds no instance address lists, and long-running clients re-resolve service names.
- **Source:** ch. 9, 16 p. 309

### RI-T58: Never fetch arbitrary user-supplied URLs
Fetch only allow-listed hosts, never an arbitrary URL supplied by an external user.
- **Why:** External users control such URLs, so the service would make requests on their behalf.
- **When:** Your service accepts URLs from external callers and fetches them.
- **Check:** Fetch code accepts only allow-listed hosts, never a raw user-supplied URL.
- **Source:** ch. 16 p. 325

### RI-T59: Call independent providers in parallel with timeouts
Call each independent provider in parallel, each with its own timeout.
- **Why:** One failing provider then leaves the other providers working for the feature.
- **When:** A feature depends on several external carriers or vendors.
- **Not when:** Calling providers in sequence, or without timeouts, defeats the split.
- **Check:** The parent calls each provider in parallel, each with its own timeout.
- **Source:** ch. 16 p. 313

### RI-T60: Test substitutes through the parent's calls
Test a substitute module through the exact calls its parent makes.
- **Why:** Subtle bugs often creep in with substitutions, and only the real call pattern reveals them.
- **When:** You replace a module with another that shares its interface.
- **Check:** Substitute tests cover every interface method the parent actually calls.
- **Source:** ch. 16 p. 314

### RI-T61: Inject a steady low level of breakage
Keep a continuous low level of controlled breakage running.
- **Why:** Recovery paths that rarely run stay unproven until a large failure hits them.
- **When:** Recovery paths exist but rarely run in production.
- **Check:** The repository or infrastructure config contains a scheduled fault-injection job that targets recovery paths. (Verify in config files.)
- **Source:** ch. 17 p. 332

### RI-T62: Define rejection evidence before the test
Decide before the experiment what evidence rejects its hypothesis, including how large a change counts.
- **Why:** A threshold set in advance stops a test from being judged after the fact.
- **When:** You define pass or fail before running an experiment.
- **Not when:** Outside causes, such as aborted mobile connections, can produce the failures.
- **Check:** The experiment states a rejection threshold and excludes known external error sources.
- **Source:** ch. 17 p. 335

### RI-T63: Keep some redundancy alive during injections
Skip injection targets that would remove a cluster's last instance or every fallback.
- **Why:** Keeping one instance or fallback alive stops the experiment from becoming a real outage.
- **When:** You choose an injection for an autoscaled cluster or a call that has fallbacks.
- **Check:** Injection rules skip targets that would leave no instance or fallback alive.
- **Source:** ch. 17 p. 338

### RI-T64: Simulate the absence of key people
Simulate the absence of key people to find single points of failure in human roles.
- **Why:** The book asks what happens when a single point of failure goes home each evening.
- **When:** A critical role or piece of knowledge rests with one person.
- **Check:** Runbooks name a backup for each critical role or procedure.
- **Source:** ch. 17 p. 339

### RI-T65: Build HTML with an escaping library
Generate HTML with a library that escapes values automatically, instead of concatenating strings.
- **Why:** The book warns against building structured data by smashing strings together.
- **When:** Generating markup that includes request data or stored values.
- **Check:** HTML generation uses an escaping template or builder API, not string concatenation with variables.
- **Source:** ch. 11 p. 230

### RI-T66: Never build file paths from request input
Never build a file path from a filename or parameter that the caller supplies.
- **Why:** The book warns against paths assembled from filenames in requests.
- **When:** Reading or writing files based on request input.
- **Check:** No file path is concatenated from request parameters or uploaded filenames.
- **Source:** ch. 11 p. 232

### RI-T67: Authorize every request for protected objects
Run an authorization check on every request for a protected resource, however the caller got the URL.
- **Why:** The book says to make that check on every request, not only on the first one.
- **When:** Handling any request that reads or changes protected data.
- **Check:** Each handler for protected objects runs an authorization check on every request.
- **Source:** ch. 11 p. 231

### RI-T68: Bound query result sets in the query
Add a row limit or paging to every hand-written query that can return unbounded rows.
- **Why:** The book calls a client-side timeout a stopgap, not the fix, for result sets that can grow.
- **When:** Writing SQL or an endpoint that can return a result set growing without limit.
- **Check:** SQL for growable tables includes TOP, LIMIT, or rownum clauses, or the endpoint enforces paging.
- **Source:** ch. 4, 5 p. 101

### RI-T69: Check sequential calls against one time budget
Check that the summed waits of a sequence of calls fit the caller's overall time budget.
- **Why:** The book says safety is not a composable property, as concurrency is not.
- **When:** A caller makes several calls in sequence under one overall timeout.
- **Check:** Timeout tests or budget checks cover the summed latency of sequential calls.
- **Source:** ch. 17 p. 330

### RI-T70: Put a request identifier in logs and calls
Include one request or transaction identifier in each log message, and pass it through every downstream call.
- **Why:** Without a shared identifier, a failed request cannot be followed end to end.
- **When:** Logging events tied to one request, or tracing a request across tiers.
- **Check:** Log statements and downstream calls carry the same correlation identifier.
- **Source:** ch. 8, 17 p. 178

### RI-T71: Let one trial call test breaker recovery
After the cool-off period, let one trial call through in a half-open state, closing the breaker on success and reopening it on failure.
- **Why:** The trial call is how the breaker learns whether the dependency has recovered.
- **When:** An open breaker's wait period has elapsed.
- **Check:** The breaker has a half-open state that admits a trial call and transitions on its result.
- **Source:** ch. 5 p. 108

### RI-T72: Release connections even when statement close fails
Close the connection even when closing its statement throws an exception.
- **Why:** The JDBC specification allows statement close to throw, so the code must handle that case.
- **When:** Writing JDBC cleanup code in finally blocks.
- **Check:** Each close call is guarded so a statement close failure cannot skip the connection close.
- **Source:** ch. 2 p. 33

### RI-T73: Rotate log files by size and purge them
Configure size-based log rotation with eventual purging for every log file written to local disk.
- **Why:** Logs that grow unchecked can fill the disk, and rotation takes only minutes to configure.
- **When:** Any service writes log files to a local disk.
- **Check:** Logrotate or framework settings define a size limit and a maximum number of retained files.
- **Source:** ch. 5 p. 116

### RI-T74: Throttle failed logins per account
Limit how many login attempts can be made against one account, using throttling or delays.
- **Why:** Locking accounts after a few failures lets an attacker lock out legitimate users.
- **When:** Implementing login or any credential check.
- **Check:** The login path counts failed attempts per account and applies throttling or delays.
- **Source:** ch. 11 p. 228

### RI-T75: Measure residence time, not only processing time
Measure residence time, which includes queue wait and processing, against response targets.
- **Why:** The book says many people go wrong by measuring only their own processing time.
- **When:** Setting latency metrics or service-level checks.
- **Check:** The latency metric starts when a request arrives at the server socket.
- **Source:** ch. 9 p. 193
