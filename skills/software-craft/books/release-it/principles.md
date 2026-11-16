# Release It! — Michael T. Nygard (2nd edition, 2018)

## Summary
Nygard argues that software is judged in production, not by QA tests. Production brings unpredicted failures, load spikes, and years of uptime, so failure is the normal case a design must handle. The book covers the antipatterns that cause outages, the patterns that contain them, and the deployment, operations, security, and versioning practices that keep a system recoverable. Apply this advice to any system that serves real traffic. Each principle below gives a habit, the book's reason for it, and a check a diff can show. Concrete moves for specific situations are in techniques.md.

## Principles

### RI-P1: Design every component to survive failure
Every component and integration point will eventually fail, often in unanticipated ways. The goal is to contain each failure and recover from it.

- **Apply:** Write a handled failure path for each dependency, covering error, timeout, and recovery.
- **Limits:** Foreseeable failures should still be prevented where that is practical.
- **Check:** Each dependency call in the diff has an error, timeout, or fallback path, and a test exercises it.
- **See:** RI-T12, RI-T22.
- **Source:** ch. 1, 4, 5, 6

### RI-P2: Put a time limit on every wait
A call with no time limit can hold its caller forever, and one stalled dependency can exhaust every thread. The book asks for an explicit limit on each remote call and pool wait, because many defaults wait forever.

- **Apply:** Pass an explicit timeout to every remote call, lock wait, and pool checkout that the change adds or touches.
- **Check:** Each remote call, lock wait, and pool acquire in the diff passes a timeout.
- **See:** RI-T13, RI-T14, RI-T22.
- **Source:** ch. 3, 4, 6

### RI-P3: Contain failures with partitions and bulkheads
A failure that spreads across a system is a cascade. Nygard recommends partitioning shared capacity by caller or traffic class.

- **Apply:** Give each caller group or traffic class its own pool, instance set, or deployment, so one group's failure leaves the others running.
- **Limits:** Groups that fail alike gain nothing. Callers of a failed partition need circuit breakers, since partitions do not protect them.
- **Check:** Server and thread pools for different callers or traffic types are configured separately in deployment or code.
- **See:** RI-T10, RI-T17, RI-T29.
- **Source:** ch. 3, 4, 5

### RI-P4: Bound every cache, queue, and session
Unbounded growth eventually exhausts memory or pushes response times past target. The book asks for a configured bound on each cache, a finite bound on each queue, and small session contents.

- **Apply:** Give each new cache or queue an explicit size limit, and store only identifiers or scalar values in sessions.
- **Check:** Cache and queue constructors in the diff set a bound, and session writes hold only identifiers or scalar values.
- **See:** RI-T18, RI-T21.
- **Source:** ch. 4, 5, 15

### RI-P5: Make production observable
Operators must diagnose a running system without adding code. The book asks for health checks that exercise the real service, and metrics that expose internal state.

- **Apply:** Add health checks that run a real transaction or dependency, and export metrics for pools, breakers, and integrations.
- **Check:** Health endpoints call a real dependency, and metrics export pool or breaker state.
- **See:** RI-T25, RI-T40.
- **Source:** ch. 2, 4, 7, 10

### RI-P6: Bound automation and keep judgment with people
Automation that changes many resources at once can disrupt the whole system in one run. Automated changes need limits, and large changes need human confirmation.

- **Apply:** Name a maximum number of changes per run, keep each subsystem above its minimum, and confirm with a person before exceeding the maximum.
- **Limits:** The right threshold depends on the spare burst capacity in the system.
- **Check:** Automation has a maximum change count or an approval gate.
- **See:** none.
- **Source:** ch. 4, 5, 10

### RI-P7: Ship small changes that can be rolled back
Nygard prefers small deployments, since large batches carry more risk. He recommends canary rollouts that stop when metrics degrade, and additive schema changes before new code ships.

- **Apply:** Keep each release small, send it to a canary first, and ship additive schema changes and data copies old code can read before the new code rolls out.
- **Limits:** Old and new builds must coexist during the canary. Triggers are safe to add only if they are unconditional and cannot throw errors.
- **Check:** Release plans show small change sets, a canary stage with metric gates, and additive migrations before code rollout.
- **See:** RI-T46, RI-T47, RI-T48.
- **Source:** ch. 10, 13, 16

### RI-P8: Keep secrets and environment values out of artifacts
Secrets and environment values belong outside the release artifact.

- **Apply:** Supply credentials and environment values at startup or from an override location outside the release artifact, and keep them out of images, source, and install directories.
- **Check:** Images, source, and build outputs contain no production passwords, hostnames, or ports.
- **See:** RI-T43, RI-T44.
- **Source:** ch. 7, 8, 11, 15
