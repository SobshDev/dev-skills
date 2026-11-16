# Errors, contracts, validation and resource cleanup

This guide covers how code should fail. It says where to check input, how to state and enforce a routine's contract, when to throw and when to return an error, how to shrink the number of error cases, and how to leave data and resources clean after a failure. The central idea is that outside data is checked once at the boundary, a broken internal assumption is a bug that should stop the program loudly, and good design leaves callers with as few error cases as possible.

**Read this when:** writing a handler that accepts user, file or network data, adding a check or an assertion, deciding whether a function throws or returns an error, writing a catch block or a switch default, seeing callers test for null or a marker value, writing code that opens files, sockets, locks, connections or transactions, an operation can fail halfway through an update, reviewing the error paths of a diff.

**Entry IDs** such as `WELC-T12` point to `../books/<book>/techniques.md` (T) or `principles.md` (P);
the prefix table is in [SKILL.md](../SKILL.md).

## Contents

- [Rules: validating input](#rules-validating-input)
- [Rules: contracts and assertions](#rules-contracts-and-assertions)
- [Rules: reporting failures](#rules-reporting-failures)
- [Rules: fewer error cases](#rules-fewer-error-cases)
- [Rules: consistent state and resource cleanup](#rules-consistent-state-and-resource-cleanup)
- [Playbooks](#playbooks)
- [Where the books disagree](#where-the-books-disagree)
- [Review checklist](#review-checklist)
- [More entries in this area](#more-entries-in-this-area)

Neighbouring topics live elsewhere. Timeouts, circuit breakers and retries against remote systems are in [production reliability](production-reliability.md). Composing optional and result values is in [functional style](functional-style.md). Value objects and aggregate invariants are in [domain modeling](domain-modeling.md). Injection and hostile input are in [security](security.md). Writing the tests themselves is in [testing](testing.md), and hunting a leak or a crash is in [debugging](debugging.md).

## Rules: validating input

### 1. Validate each external value once, where it enters

Check data from users, networks, files and other modules at one documented entry point, and make the rejection name the invalid value. Repeating the same check in every layer adds noise, and bad data that is not stopped at entry travels far before it fails. Refactoring wants real, tested validation at this point rather than assertions, and Pragmatic Programmer agrees that expected bad input needs real error handling. [PP-T14, PP-P6, REF-T07, PP-T15]

- **Do:** Choose the entry point for each external value, such as the request handler, parser or adapter. Check types and ranges there, name the value and the broken rule in the error, and write tests for the validation code.
- **Not when:** Calls between trusted parts of your own code may skip a duplicate check (REF-T07). A routine's preconditions are a different matter: they flag caller bugs, not bad input, so they belong to contracts and assertions (rules 5 and 6) [PP-T14].
- **Check:** Each external value is validated at one documented entry point, entry points check types and ranges, input handlers have validation tests, and no rejection path fails silently [PP-T14, PP-P6, REF-T07].

### 2. Make invalid domain values impossible to construct

Put the parsing and validation of a concept inside the type that represents it, and build that type from unchecked input only through a function that can reject the input. Every place that accepts the concept then enforces the same rule, and no caller can skip it. [DDD-T14, FPS-T26, PP-T52, DDD-T12, DDD-T13]

- **Do:** Give concepts such as an email address, an amount or a percentage their own type, with a validating constructor or factory that returns an error for bad input [DDD-T14, FPS-T26, PP-T52, DDD-T13]. Keep the invariant fields of domain objects closed to outside assignment, and change them through methods that enforce the rule [DDD-T12]. [Domain modeling](domain-modeling.md) covers value objects in depth.
- **Not when:** A supporting area with simple logic may not need its own domain types (DDD-T13).
- **Check:** Validation for a concept lives in one type and callers do not repeat it, values built from unchecked input come only from the rejecting factory, and parameters for amounts, percentages and bounded ranges use defined types rather than bare numbers [DDD-T14, FPS-T26, PP-T52].

### 3. Report every independent field error in one pass

When the fields being checked do not depend on each other, as in a form, collect the errors from all of them so the user sees every problem at once. When a later check needs a value that an earlier check produces, stop at the first error, because the remaining steps cannot change the outcome. [FPS-T28, FPS-T27]

- **Do:** Use an accumulating validation for independent fields and a short-circuiting sequence for dependent steps. [Functional style](functional-style.md) shows how to build both.
- **Not when:** Later checks need values produced by earlier checks, so errors cannot be accumulated [FPS-T28].
- **Check:** Validation of independent fields returns the errors of all failing fields, not only the first, and a dependent sequence stops at its first failure [FPS-T28, FPS-T27].

### 4. Treat a stricter input rule as a breaking change

A new required request field, or a rule that rejects input an earlier version accepted, breaks consumers that were built before it existed. Release It! asks that such a change be handled as a breaking change, not as a quiet fix. [RI-T50]

- **Do:** Before tightening validation on an interface that consumers already call, run the inputs that earlier versions accepted through the new rule, and follow your process for breaking changes if any are rejected. [Production reliability](production-reliability.md) covers versioning and rollout.
- **Check:** The schema diff adds no new required field, and the new validation accepts the prior test inputs [RI-T50].

## Rules: contracts and assertions

### 5. Write the contract before writing the routine

Before coding a routine, state its input domain, preconditions, boundary conditions and what it does not promise. A written contract tells callers what they must supply and what they may rely on. Philosophy of Software Design (POSD) adds the facts a signature cannot carry: ordering, side effects, constraints, units, whether bounds are inclusive, and what null means. [PP-T36, POSD-T15, POSD-T17]

- **Do:** Put preconditions, postconditions and non-promises in the doc comment of each public routine, along with units, bound inclusivity and null meaning [PP-T36, POSD-T15, POSD-T17]. Test the routine against that contract, including rejected inputs, boundary values and promised results [PP-T41].
- **Check:** Public routines document preconditions, postconditions and non-promises, parameter docs state units, bound inclusivity and null meaning, and tests cover rejected inputs and boundary values [PP-T36, POSD-T17, PP-T41].

### 6. Assert the conditions you are sure cannot occur

Wherever code relies on a condition, or you are sure a value or state is impossible, write an assertion whose message names that condition. An assertion turns a silent wrong assumption into an immediate failure where the bad value appears, and it records the assumed state for readers. Keep the assertion after the bug that prompted it is fixed. [PP-T15, REF-T08, PP-P6]

- **Do:** Assert internal assumptions and properties of your output. Reserve assertions for programmer errors: if a correct program could receive the value from outside, validate it and handle the error instead (rule 1) [REF-T07, REF-T08]. Treat a failed assertion as a bug to fix, not as a normal path [PP-P6]. Put no assignment or state-changing call inside an assertion, and leave assertions on in release builds unless a measurement shows them to be too costly [PP-T15, REF-T08].
- **Not when:** Expected bad input needs real error handling, not an assertion [PP-T15, REF-T08]. An extra full pass over data on a hot path may cost too much [PP-T15].
- **Check:** Assertion expressions hold no required assignments or state-changing calls, assertions guard only internal conditions, and they stay enabled in release builds unless measured as too costly [PP-T15, REF-T08, REF-T07].

Keep the work outside the assertion expression, and assert on its result:

```python
# Wrong: the pop happens inside the check
assert queue.pop() is not None

# Right: do the work, then assert on its result
item = queue.pop()
assert item is not None, "queue empty although size check passed"
```

### 7. Stop soon after detecting an impossible state

Continuing from a state that should not exist spreads the damage and hides the original fault, so raise an error or exit soon after detecting it. A state machine that receives an event with no defined transition should move to a named error state instead of staying where it is. POSD adds that a failure nothing can recover from, such as running out of memory, should abort with diagnostics rather than be thrown at callers. [PP-T16, PP-T30, POSD-T12]

- **Do:** Make impossible-state branches raise or exit, give every switch a default branch that raises, send unlisted state-machine events to an explicit error state, and make unrecoverable paths log diagnostics and terminate [PP-T16, PP-T30, POSD-T12].
- **Not when:** Replicated systems must recover lost data rather than abort on an I/O error [POSD-T12].
- **Check:** Impossible-state branches raise or exit, switch statements have a raising default, missing transitions lead to an error state, and unrecoverable paths log and terminate [PP-T16, PP-T30, POSD-T12].

### 8. Make a forgotten override fail at once

When every subclass must supply a method, make the base version throw an error that names the missing responsibility. A forgotten override then fails the first time it runs instead of quietly doing nothing. [REF-T63]

- **Do:** Write the base method as a single throw whose message says which responsibility the subclass failed to provide.
- **Not when:** In a static language, declare an abstract member instead. A default that most subclasses share belongs in the base as real code (REF-T60) [REF-T63].
- **Check:** Such base methods throw an error naming the missing responsibility [REF-T63].

### 9. Keep base contracts in force in every override

An override that drops the base method's checks can break callers that rely on the contract. Repeat the base preconditions and invariant checks in the override, and make each subtype behave like its base so callers never need to branch on the concrete type. [PP-T37, CC-T46]

- **Do:** When you override a method that carries assertions or contract checks, copy those checks into the override, and keep the override's behavior within what the base promised.
- **Not when:** The language propagates contracts to overrides automatically [PP-T37].
- **Check:** Overrides repeat base preconditions and invariant checks, and callers use the base type without testing for a concrete subtype [PP-T37, CC-T46].

### 10. Write down what you assume about code you do not control

When your code relies on undocumented or edge-case behavior of a routine you did not write, record that assumption where you call it. An assumption that is not written down is hard to recheck when the library changes. Release It! gives one such trap: a pooled connection that reports itself open may still fail statements after a failover, so statement errors need handling whatever the status says. [PP-T67, RI-T06]

- **Do:** Add a comment or a test at the call site that states the assumed behavior [PP-T67]. Handle statement errors on pooled connections without first trusting the connection's open status [RI-T06].
- **Not when:** Relying on undocumented behavior cannot always be avoided, and then the assumption needs careful documentation [PP-T67].
- **Check:** Call sites that rely on undocumented behavior carry a comment or test stating it, and statement calls on pooled connections have error handling that no status check skips [PP-T67, RI-T06].

## Rules: reporting failures

### 11. Throw only for conditions a caller can act on

POSD warns that exception handling adds more complexity than its share of the code suggests, and that every exception a class throws becomes part of its interface. Throw only when some caller has a meaningful response, and treat failures nothing can handle as unrecoverable (rule 7). FP in Scala agrees that a caller who can recover must see the failure, but carries it in the return type instead; [Where the books disagree](#where-the-books-disagree) settles the mechanism. [POSD-T12, FPS-P3, FPS-T19]

- **Do:** For each exception or error type you add, write down the response a caller is expected to make. If you cannot name one, the failure is unrecoverable or should be removed by the rules under [fewer error cases](#rules-fewer-error-cases).
- **Not when:** Replicated systems recover lost data rather than abort on an I/O error [POSD-T12].
- **Check:** Each thrown exception has a documented caller response, and recoverable cases reach the caller in a form it can handle [POSD-T12, FPS-T19].

### 12. Keep per-step error checks off the normal path

Clean Code reports failures with exceptions so that the normal steps read straight through, without a status test after every call. Pragmatic Programmer and FP in Scala reach the same result with values: each step returns either a result or an error, and an error skips the remaining steps so nothing runs on bad data. Either way, the success path stays readable and later steps never see a failed result. [CC-T29, CC-T30, PP-T32, FPS-T21, FPS-T27]

- **Do:** With exceptions, throw instead of returning a status that each caller must test, and move any multi-statement try or catch body into its own named function [CC-T29, CC-T30]. With result values, chain the steps through a shared helper that runs the next step only on success and passes errors through unchanged [PP-T32, FPS-T21].
- **Not when:** The language has no exceptions, or its exception handling is not reliable. Clean Code's advice then does not apply, and returned results chained as above are the alternative [CC-T29, PP-T32].
- **Check:** In a language with exceptions, callers do not check error codes after every call, try and catch blocks hold a single statement, and in result pipelines later steps run only on values while errors pass through unchanged [CC-T29, CC-T30, PP-T32].

### 13. Carry the reason in a returned failure when callers need it

When failure is returned as a value, pick the shape by what the caller needs. An optional result fits when knowing that there is no value is enough, and a result that carries an error, including any exception caught underneath, fits when callers must branch on what went wrong. Apply a default for a missing value once, at the end of the chain, rather than at each step. [FPS-T20, FPS-T25, FPS-T22]

- **Do:** Return an optional type from a function that is undefined for some inputs its parameter types allow [FPS-T20]. Return a result type whose failure side holds a message or the caught exception when callers need the reason [FPS-T25]. Resolve an optional value with its fallback in one place at the end [FPS-T22].
- **Not when:** If knowing that a failure occurred is enough, the optional type is simpler than a result with a reason [FPS-T25]. If the absence must be reported with its reason, a default value hides it, so return a result with the reason [FPS-T22].
- **Check:** Partial functions declare the missing case in their return type, failure values carry a message or exception, and a fallback appears once at the end of each chain [FPS-T20, FPS-T25, FPS-T22].

### 14. Retry only failures that a retry can fix

When a transaction aborts, a permanent error such as a constraint violation cannot succeed on retry, and unbounded retries under contention add load to a system that is already failing. Retry an aborted transaction only for transient errors such as a deadlock or a failover, with a cap on attempts and growing delays, and handle overload separately. Pragmatic Programmer adds that retries and sleeps added by trial and error hide the real cause. [DDIA-T35, PP-T66]

- **Do:** Classify a transaction's error before retrying it, cap attempts, back off exponentially, and keep any retry or sleep only if a comment or test explains why it is needed [DDIA-T35, PP-T66]. Remote-call retries, jitter and timeouts are in [production reliability](production-reliability.md).
- **Not when:** The error is permanent, so do not retry it [DDIA-T35].
- **Check:** Transaction retry logic separates transient from permanent errors, caps attempts with backoff and handles overload separately, and each remaining retry or sleep has a documented reason or a test that needs it [DDIA-T35, PP-T66].

## Rules: fewer error cases

### 15. Redefine the operation so the error cannot occur

Some failures happen only because the requested state already holds, such as deleting something that is already gone. Change the operation's goal so that reaching that state counts as success. Simpler semantics need fewer validation branches, and simpler code holds fewer bugs. [POSD-T10]

- **Do:** State the operation's postcondition, for example "the key is absent afterwards", and return success whenever it already holds.
- **Not when:** Callers that need to know about the special case must still be told [POSD-T10].
- **Check:** The operation returns success when its outcome already holds, with no error branch for it [POSD-T10].

```python
# Error case the caller must handle
def remove(key):
    if key not in table:
        raise KeyError(key)
    del table[key]

# Defined away: success means "key is not in the table afterwards"
def remove(key):
    table.pop(key, None)
```

### 16. Recover inside the module when callers need nothing

When a low-level failure can be detected and fixed without caller input, such as a lost packet that can be resent, recover in the lowest layer that can resolve it. Higher layers then never see the failure and do not each repeat the same recovery. This is one case of POSD's broader advice that the module owning a complexity should absorb it. [POSD-T11, POSD-P4]

- **Do:** Handle the recoverable condition inside the module, and leave it out of the public interface.
- **Not when:** Callers need the information, such as whether messages were lost or whether a peer really failed [POSD-T11]. Move only logic that is closely related to the module, and do not pull all application functionality into one class [POSD-P4].
- **Check:** The public interface declares no exception for a condition the module recovers from itself, and callers do not handle complexity the module hides [POSD-T11, POSD-P4].

### 17. Let the normal path handle empty and absent states

Write the main logic so that an empty collection or a missing optional part needs no extra check, and keep structural invariants that rule out the excluded cases. Every special-case branch is one more path readers must follow. [POSD-T30]

- **Do:** Prefer code where an empty input naturally yields an empty or short result, and document short results as normal returns.
- **Not when:** The path is hot and has several rare conditions that the normal path cannot handle safely. Then combine them into one guard tested once at the start (POSD-T51) [POSD-T30].
- **Check:** The code has no checks for empty or missing states that the normal path already handles, and short results are documented as normal [POSD-T30].

### 18. Replace repeated marker checks with a type callers cannot miss

When many clients test for the same marker value, such as null or a sentinel string, and then do the same thing, return a special-case object instead. Make it immutable and give it methods for the common responses, so clients stop repeating the check. For records that arrive as plain data, add a transform that swaps the sentinel for the special case. FP in Scala makes the same point for failure in general: null or NaN should not stand for failure. [REF-T67, REF-T68, FPS-P3]

- **Do:** Introduce the special-case object, move clients to it one at a time, and keep the old check while both forms still reach a client [REF-T67, REF-T68]. Where a null must remain, document what it means [POSD-T17].
- **Not when:** One client needs a different response to the special value, so it keeps an explicit check [REF-T67].
- **Check:** No client compares against the marker, nested properties return special cases rather than null, transformed records hold no sentinel strings, and no null or NaN stands for failure [REF-T67, REF-T68, FPS-P3].

## Rules: consistent state and resource cleanup

### 19. Restore consistent state before reporting a failure

If an operation fails partway through changing data structures, undo or complete the partial changes before it reports the failure or carries on. Otherwise callers act on half-updated data after the failure. [POSD-T53]

- **Do:** Identify every structure the operation changes before its last possible failure point, and on each failure path either roll those changes back or finish them. Test the path by forcing a failure midway and asserting the resulting state (rule 22).
- **Check:** Failure paths undo or complete partial updates before reporting upward [POSD-T53].

### 20. Release files, sockets and locks on every path

Garbage collection reclaims memory only, so release files, sockets and similar resources yourself. Acquire the resource just before a try block and release it in the finally clause or through scope-based cleanup, so the release runs on exceptions as well as normal returns. FP in Scala uses the same shape for streams: one combinator acquires, uses and releases, so release runs on normal end, on error and on early halt. [CC-T79, PP-T38, FPS-T62]

- **Do:** Use scope-based cleanup or a finally clause for each file, connection, lock or transaction [PP-T38, CC-T79]. In stream libraries, pair each opened handle with its release in one resource call [FPS-T62]. In JDBC cleanup code, guard each close so that a statement close that throws cannot skip the connection close [RI-T72].
- **Check:** Each acquisition in the diff has a matching release, each try starts after its acquisition with a finally or scope that releases it, and each JDBC close is guarded so one failure cannot skip the next [CC-T79, PP-T38, FPS-T62, RI-T72].

```java
Connection conn = pool.acquire();     // acquire before the try
try {
    Statement st = conn.createStatement();
    try {
        st.execute(sql);
    } finally {
        st.close();                   // may throw...
    }
} finally {
    conn.close();                     // ...and this still runs
}
```

### 21. Give each resource one owner that releases it

Make one routine or class responsible for closing each resource on every path, rather than adding special-case closes in branches. POSD goes further: the module that allocates a memory block or handle should also release it, so callers do not each carry the ownership rule. One owner with one cleanup point stops a rarely taken branch from skipping the release. [PP-T39, POSD-T08]

- **Do:** Move scattered close calls into the owner's single cleanup point. Design APIs so that returned resources need no release by the caller, and where a caller must hold one, name its releaser in a comment.
- **Check:** Cleanup for each resource happens in one place for all paths, and each resource a caller must hold has a comment naming who releases it [PP-T39, POSD-T08].

### 22. Test every error handler and rejected input

Error handlers seldom run, so their bugs stay hidden for a long time, and Designing Data-Intensive Applications (DDIA) notes that poor error handling causes many critical bugs. Write tests that force each failure on purpose, including invalid, boundary and unavailable-resource cases, and check the response as carefully as the success path. [POSD-T20, DDIA-T14, SWE-T53, PP-T42]

- **Do:** Inject failures from each dependency that can fail, using exceptions in unit tests and faults in integration tests [SWE-T53]. In a test that expects an exception, fail the test if nothing is thrown and catch only the named exception type [TDD-T38]. [Testing](testing.md) covers test design.
- **Check:** Tests exercise each error branch and assert its response, at least one failing call per fallible dependency is covered, suites include invalid, boundary and unavailable-resource cases, and exception tests call fail after the operation and catch a named type [DDIA-T14, SWE-T53, PP-T42, TDD-T38].

## Playbooks

### When you add an entry point that accepts outside data

1. Name the one place where this data enters, and plan to validate it only there [PP-T14].
2. Parse each concept into its own type through a factory that rejects bad input [DDD-T14, FPS-T26, PP-T52].
3. For independent fields, collect all errors in one pass. For dependent steps, stop at the first [FPS-T28, FPS-T27].
4. Make each rejection name the value and the rule it broke, and make sure no rejection path is silent [PP-T14, PP-P6].
5. Inside the trusted code behind the boundary, express remaining assumptions as assertions, not as repeated validation [REF-T07, REF-T08, PP-T15].
6. Test rejected inputs, boundary values such as empty, zero, negative and blank, and the promised results [PP-T41, PP-T42, REF-T06].
7. If the entry point already has consumers, check that the new rules still accept what earlier versions accepted [RI-T50].

### When you decide how a new routine reports failure

1. Write the contract first: input domain, preconditions, postconditions and non-promises [PP-T36, POSD-T15].
2. For each failure that happens only because the requested state already holds, redefine the goal so that this state counts as success, unless a caller needs to know about it [POSD-T10].
3. For each remaining failure the module can fix without caller input, recover inside the module, unless callers need the information [POSD-T11].
4. Split what is left into conditions a caller can act on and conditions nothing can recover from [POSD-T12, FPS-T19].
5. Report the actionable ones either as exceptions or as returned results that carry a reason when callers need it, and choose between them with the first tension under [Where the books disagree](#where-the-books-disagree) [CC-T29, FPS-T25, FPS-T20].
6. Make the unrecoverable ones log diagnostics and stop [POSD-T12, PP-T16].
7. Document each reported failure with the caller response it expects, and write a test that forces it [POSD-T12, POSD-T20].

### When an operation can fail halfway through changing state

1. List each structure the operation changes, and each point after the first change where it can fail [POSD-T53].
2. On every failure path, roll back or complete the partial changes before throwing, returning or continuing [POSD-T53].
3. If the change is a user-level undoable command, save the prior state in the command when it executes and restore it on undo. Where an inverse cannot restore connected objects exactly, store a snapshot instead, unless snapshots cost too much for how often they are taken [GOF-T35, GOF-T72]. [Design patterns](design-patterns.md) covers Command and Memento.
4. Release any resources the operation acquired in finally or scope cleanup, so the failure does not also leak them [PP-T38].
5. Write a test that injects a failure at the midpoint and asserts that the data is consistent afterwards [SWE-T53, DDIA-T14].

### When code opens files, sockets, locks, connections or transactions

1. Decide which routine or class owns the resource, preferably the module that allocated it [PP-T39, POSD-T08].
2. Acquire it immediately before a try block or scoped construct, and release it in the finally clause or scope exit [PP-T38, CC-T79].
3. When several resources are closed together and a close can throw, as with JDBC statements, guard each close so later ones still run [RI-T72].
4. In tests, release resources that setUp allocated in tearDown, and remember that tearDown does not run when setUp itself fails [TDD-T36].
5. If a leak is suspected, log every open and close with a matching identifier and look for opens without a close [PP-T61]. [Debugging](debugging.md) has the rest of that hunt.

### When callers keep testing for null or a marker value

1. Count the clients that test for the marker and note what each one does next [REF-T67].
2. If most do the same thing, introduce an immutable special-case object with methods for those responses. For plain records, add a transform that replaces the sentinel [REF-T67, REF-T68].
3. Move clients one at a time, keeping the old check while both forms can still reach a client [REF-T68].
4. Leave an explicit check in any client that needs a different response [REF-T67].
5. If the function is undefined for some inputs its parameter types allow, return an optional type instead, or a result with a reason when callers must know what went wrong [FPS-T20, FPS-T25].
6. If an empty result is simply a short normal result, let the normal path handle it and document it as normal [POSD-T30].

### When you review code that continues after a "cannot happen" condition

1. Replace a silent fallthrough with an assertion that names the condition, or a raise or exit if the state is impossible [PP-T15, PP-T16].
2. Give each switch over a closed set a default branch that raises [PP-T16].
3. In a state machine, route every event without a defined transition to a named error state [PP-T30].
4. Where a base method must be overridden, make it throw an error naming the missing responsibility, or declare it abstract in a static language [REF-T63].
5. Check that overrides keep the base preconditions and invariant checks, unless the language propagates them [PP-T37].

## Where the books disagree

### Should a recoverable failure be thrown or returned?

- **Clean Code:** Report failures with exceptions, so normal steps carry no status checks [CC-T29].
- **POSD:** Throw, but only for conditions a caller can act on, because each exception adds complexity and joins the interface [POSD-T12].
- **FP in Scala:** Return an optional or result value for every recoverable case, so the failure shows in the type, and throw only where no caller could recover [FPS-P3, FPS-T19, FPS-T25].
- **Pragmatic Programmer:** In a pipeline, give each step a value-or-error result and let errors skip the remaining steps [PP-T32].
- **Decide:** The books agree that a caller who can act must be able to see the failure, and that the normal path should not test a status after every step [CC-T29, PP-T32, FPS-T21]. The entries give two deciding conditions. If the language has no exceptions or its exception handling is not reliable, return results [CC-T29]. If the code is a pipeline whose steps may fail and whose later steps need the earlier results, forward result values through it [PP-T32]. Beyond those conditions the entries do not pick a winner, so follow the codebase's existing convention, and in either mechanism keep the number of failure kinds small [POSD-T12, POSD-T10].

### How should an unrecoverable failure surface?

- **POSD:** Abort with diagnostics rather than throw something no caller can handle [POSD-T12].
- **Pragmatic Programmer:** Crash early rather than continue with suspect state [PP-T16].
- **FP in Scala:** Use an exception for failures no caller could recover from [FPS-T19, FPS-P3].
- **Decide:** All three keep such failures off the paths callers are expected to handle. POSD says abort and FP in Scala says throw, but neither gives a condition for choosing, so follow the codebase's convention, and make sure the path logs diagnostics and stops instead of continuing [POSD-T12, PP-T16]. In a replicated system that must recover lost data, do not abort on an I/O error [POSD-T12].

### Should a module hide a failure or make it loud?

- **POSD:** Remove error cases where possible: redefine the operation, mask recoverable failures in the lowest layer, and let the normal path handle empty states [POSD-T10, POSD-T11, POSD-T30].
- **Pragmatic Programmer:** Treat every error as meaningful, let failures be loud, crash on impossible states, and remove retries or sleeps nobody can justify [PP-P6, PP-T16, PP-T66].
- **Decide:** Mask a failure only when the module can recover without caller input and no caller needs the information [POSD-T11]. Define an error away only when it arises because the requested state already holds and callers need not be told [POSD-T10]. Stop on a state that should be impossible [PP-T16]. Report everything else, and never through a silent path [PP-P6]. A mask that works by retrying needs a documented reason or a test, and a retried aborted transaction should target transient errors only [PP-T66, DDIA-T35].

### Should code behind the boundary re-check values the boundary already validated?

- **Pragmatic Programmer:** Validate once at entry, because checks repeated in every layer add noise [PP-T14]. Still assert what you believe cannot occur, and state preconditions [PP-T15, PP-T36].
- **Refactoring:** Trusted internal calls may skip duplicate validation, but each condition the code assumes deserves an assertion [REF-T07, REF-T08].
- **Learning DDD and FP in Scala:** Validation inside the value type's constructor means every place that accepts the type gets the same rule [DDD-T14, FPS-T26].
- **Decide:** Do not repeat input validation with error handling inside trusted code [PP-T14, REF-T07]. Express internal assumptions as side-effect-free assertions, and drop one only when a measurement shows it is too costly on a hot path [PP-T15, REF-T08]. Where a value arrives as a validated type, the type already carries the check [DDD-T14, FPS-T26].

### Special-case object or optional type for a missing value?

- **Refactoring:** Return a special-case object when many clients test for the same marker and respond the same way [REF-T67].
- **FP in Scala:** Return an optional type from a function that is undefined for some inputs, so the type shows the missing case, or a result with a reason when callers need it [FPS-T20, FPS-T25].
- **POSD:** Let the normal path handle empty or absent states without extra checks [POSD-T30].
- **Decide:** If many clients respond to the missing value in the same way, use a special-case object, and let any one client that needs a different response keep an explicit check [REF-T67]. If the function is undefined for some inputs its parameter types allow, return an optional type, or a result with a reason when callers must know what went wrong [FPS-T20, FPS-T25]. If an empty result is just a short normal result, return it and document it as normal [POSD-T30].

## Review checklist

- [ ] Each external value in the diff is validated at one documented entry point, and the rejection names the value [PP-T14, PP-P6].
- [ ] Input handlers have tests for rejected, boundary and blank inputs [REF-T07, PP-T42, REF-T06].
- [ ] Domain values built from unchecked input come only from a factory that can reject it [FPS-T26, DDD-T14].
- [ ] Amounts, percentages and bounded ranges use defined types, not bare numbers [PP-T52].
- [ ] No new required field or stricter rule rejects input that the previous version accepted, or the change is handled as a breaking change [RI-T50].
- [ ] New public routines document preconditions, postconditions, non-promises, units and null meaning [PP-T36, POSD-T17].
- [ ] No assertion is the only check on data from users, files or other systems [REF-T07, REF-T08].
- [ ] No assertion expression contains an assignment or a state-changing call [PP-T15, REF-T08].
- [ ] Assertions are not disabled in release builds without a measurement [PP-T15].
- [ ] Every switch has a default branch that raises, and impossible-state branches raise or exit [PP-T16].
- [ ] State-machine events with no defined transition lead to a named error state [PP-T30].
- [ ] Overrides keep the base preconditions and invariant checks, and callers do not test for concrete subtypes [PP-T37, CC-T46].
- [ ] Each newly thrown exception has a documented caller response [POSD-T12].
- [ ] In a language with exceptions, callers do not check an error code after every call, and try or catch blocks hold one statement [CC-T29, CC-T30].
- [ ] In result pipelines, later steps run only on values and errors pass through unchanged [PP-T32].
- [ ] No null or NaN stands for failure, and no client compares against a marker that a special-case object could replace [FPS-P3, REF-T67].
- [ ] An operation whose outcome already holds returns success instead of an error [POSD-T10].
- [ ] The public interface declares no exception for a condition the module recovers from itself [POSD-T11].
- [ ] Each transaction retry targets transient errors only and caps attempts with backoff, and each retry or sleep has a stated reason or a test that needs it [DDIA-T35, PP-T66].
- [ ] Failure paths roll back or complete partial updates before reporting [POSD-T53].
- [ ] Each file, socket, lock, connection or transaction acquired in the diff is released in finally or scope cleanup [CC-T79, PP-T38].
- [ ] Each resource has one cleanup point, and any resource a caller must hold names its releaser [PP-T39, POSD-T08].
- [ ] Each new error branch has a test that forces it and asserts the response [POSD-T20, DDIA-T14, SWE-T53].
- [ ] Tests that expect an exception fail when nothing is thrown and catch only the named type [TDD-T38].

## More entries in this area

- `DDIA-T38` — Enforce unique values with uniqueness constraints: when two users may claim the same value at once, rely on a unique constraint and handle its violation error instead of check-then-insert, unless several asynchronous leaders or shards accept writes for the value. See [data systems](data-systems.md).
- `DDIA-T20` — Validate commands before they become events: in an event-sourced system, reject bad commands before appending, since every view replays the log.
- `DDD-T65` — Validate records against a schema on ingestion: check records against a declared schema before they enter a data lake.
- `RI-T49` — Add NOT NULL and foreign keys after rollout: tighten database constraints only once no old instance still makes the writes they would reject.
- `RI-T12` — List each failure mode of external calls: include no response, slow response, malformed and oversized replies when writing error handling for a dependency, as far as is practical outside life-critical systems. See [production reliability](production-reliability.md).
- `DDIA-P2` — Treat every remote call as possibly failed: a timed-out write may still have taken effect, so error handling must keep confirmed failures apart from timeouts.
- `FPS-T23` — Combine independent Options with map2: join two optional inputs without nested matches.
- `FPS-T24` — Pass a costly fallback by name: evaluate a default only when it is needed, which matters when the default can itself throw.
- `FPS-T44` — Put error labels and locations in parser interface: when a parser must explain malformed input, attach a label and position to each error.
- `FPS-T42` — Catch exceptions and report them as failures: in a property-test runner, turn a thrown exception into a reported failure naming the input.
- `TDD-T50` — Count setUp and test exceptions as failures: when writing a test runner, guard setUp with the same handler as the test.
- `PP-T61` — Log every resource open and close: the tool for finding a suspected leak.
- `POSD-T51` — Check special cases once at hot path start: on a hot path with several rare conditions, one combined guard at the top keeps the common path clear.
