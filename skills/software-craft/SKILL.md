---
name: software-craft
description: Engineering judgment distilled from 14 classic software books (Clean Code, Refactoring, A Philosophy of Software Design, Tidy First?, TDD by Example, Working Effectively with Legacy Code, The Pragmatic Programmer, Clean Architecture, Design Patterns, Learning DDD, FP in Scala, Release It!, Designing Data-Intensive Applications, Software Engineering at Google) — core rules, step-by-step workflows, decision rules where the books disagree, and 17 topic guides. Use this skill whenever you write or modify non-trivial code, fix a bug, refactor or clean up, add or fix tests, review a diff or pull request, design a module, API, schema, architecture or data pipeline, change legacy or untested code, touch production behavior (timeouts, retries, deploys, migrations, security), or weigh a design trade-off — even when the user does not mention design, quality or best practices.
---

# Software craft

This skill turns 14 books on software design and engineering into rules an agent can apply
while it works. The books mostly agree on a small core: change code in small verified
steps, keep structure and behavior changes apart, protect changes with trusted tests, hide
complexity behind small interfaces, keep each fact in one place, and assume every remote
call can fail. Where they disagree, this file gives the condition that decides.

## How to use this skill

1. **Read this file first.** It holds the core rules, the workflow for each kind of task, and
   the main disagreements between the books.
2. **Open one to three guides** that match the task (see the [router](#which-guide-to-read)).
   Each guide merges what all 14 books say about one area, with playbooks and a review checklist.
3. **Open a book entry** when you need the full detail behind a citation. Entry IDs look like
   `POSD-T35` (technique) or `CC-P2` (principle). T entries are in `books/<book>/techniques.md`,
   P entries in `books/<book>/principles.md`. Every entry has a Why, When, Not when and Check.
4. **Size the process to the code.** Long-lived code that others depend on deserves the full
   treatment. Short-lived or narrow code may skip heavy practices [SWE-P1]. A throwaway
   prototype answers one question and is then rebuilt properly [PP-T03].
5. **Follow the codebase.** When a rule conflicts with a clear existing convention in the
   repository, follow the shape of similar existing code and mention the trade-off instead of
   mixing styles. If a better convention is justified, migrate every use and remove the old one [POSD-T31].

Entry IDs are for you, not for your reader. In replies, code reviews, commit messages and
comments meant for people, give the reason in plain words and name the book only when that
helps. Do not paste IDs such as `PP-T74` that a reader cannot look up, unless the user asks for
your sources.

### Book prefixes

| Prefix | Book | Folder |
|---|---|---|
| TF | Tidy First? — Kent Beck (2023) | [books/tidy-first](books/tidy-first/) |
| CC | Clean Code, 2nd ed. — Robert C. Martin (2025) | [books/clean-code-2e](books/clean-code-2e/) |
| GOF | Design Patterns — Gamma, Helm, Johnson, Vlissides (1994) | [books/design-patterns](books/design-patterns/) |
| POSD | A Philosophy of Software Design, 2nd ed. — John Ousterhout (2021) | [books/philosophy-of-software-design](books/philosophy-of-software-design/) |
| REF | Refactoring, 2nd ed. — Martin Fowler (2018) | [books/refactoring](books/refactoring/) |
| WELC | Working Effectively with Legacy Code — Michael Feathers (2004) | [books/legacy-code](books/legacy-code/) |
| TDD | Test-Driven Development: By Example — Kent Beck (2002) | [books/tdd-by-example](books/tdd-by-example/) |
| PP | The Pragmatic Programmer, 20th anniv. ed. — Thomas & Hunt (2019) | [books/pragmatic-programmer](books/pragmatic-programmer/) |
| CA | Clean Architecture — Robert C. Martin (2017) | [books/clean-architecture](books/clean-architecture/) |
| DDD | Learning Domain-Driven Design — Vlad Khononov (2021) | [books/learning-ddd](books/learning-ddd/) |
| FPS | Functional Programming in Scala — Chiusano & Bjarnason (2014) | [books/fp-in-scala](books/fp-in-scala/) |
| RI | Release It!, 2nd ed. — Michael T. Nygard (2018) | [books/release-it](books/release-it/) |
| DDIA | Designing Data-Intensive Applications, 2nd ed. — Kleppmann & Riccomini (2026) | [books/ddia-2e](books/ddia-2e/) |
| SWE | Software Engineering at Google — Winters, Manshreck & Wright (2020) | [books/swe-at-google](books/swe-at-google/) |

## Core rules

These are the ideas that several books share. Each one names its sources, and the guides
expand them.

### 1. Change code in small steps, and verify each one

Make each step small enough that a failure points to the last edit. Run the tests after
each step, and take larger steps only when the path is clear. When a step goes wrong, revert
to the last passing state and redo the work in smaller steps rather than debugging a large
broken change. [TF-P2, REF-P1, REF-T09, REF-T10, TDD-P2, TDD-T05, WELC-P2, PP-P2, PP-T06, SWE-P2, CC-P3]

- **Check:** Each commit is small enough to review and revert on its own, and the tests pass at every commit [REF-T11, TDD-T15].

### 2. Keep structure changes and behavior changes apart

A refactoring or tidying changes how code is organized without changing what it computes.
Mixing it with a behavior change means the existing tests can no longer tell you the
restructuring was safe, and reviewers cannot judge either part. Put each kind in its own
commit, and tidyings in their own pull request when the team works that way. If you notice a
bug while refactoring, leave it in place and fix it in a separate change. [TF-P1, TF-T23, WELC-P3, REF-T12, REF-P1, PP-T44, TDD-T07]

- **Check:** A structure-only commit changes no computed results and needs no test edits, except edits forced by an interface or signature change [REF-T82, SWE-T60].

### 3. Get trusted tests in place before you change code

Untested code gives no warning when you break it, so pin its current behavior with tests
before you edit it, even when that behavior looks wrong [WELC-P1, WELC-T37, CC-T75, REF-T01, PP-T43].
A test is evidence only if it can fail: watch each new test fail first, and confirm it fails
when you break the behavior on purpose [TDD-T02, REF-T02, TDD-P8]. Never skip, disable or
delete a failing test just to get a green run. Disable a slow or broken test only with a
stated reason or an open ticket, and never an intermittent threaded test [CC-T69, PP-T73, TDD-T15].

- **Not when:** Code that will never change again does not repay the cost of new tests, and some dependency breaking must come before the first test [WELC-P1].
- **Check:** Test commits for an area come before, or with, the commits that change it.

### 4. Write the test first, and test behavior through public interfaces

For new behavior, write a failing test, make it pass with the simplest code, then clean up
while the tests stay green [TDD-P1, TDD-P3, CC-T05, CC-T03, CA-T03]. Assert outcomes
(returned values and resulting state) through the public API, not internal calls or private
fields, so tests survive refactoring [SWE-P5, SWE-T10, CC-T15, TDD-T13]. Keep most tests
small, fast, hermetic and independent of each other [SWE-P4, CC-T10, TDD-T34].

- **Not when:** Unit tests alone do not establish security or concurrency correctness [TDD-P8]. Check call counts only when the call itself is the behavior, such as a cache that must reduce reads [SWE-T11].
- **Detail:** [guides/testing.md](guides/testing.md).

### 5. Judge a design by what the next change costs

Complexity is whatever makes code hard to understand and change. It is not size or feature
count, and a reader's confusion counts even when the author finds the code clear
[POSD-P1, POSD-T02]. Compare design options by the modules a likely change would touch and
the effort it would need [PP-T68, CA-P7, TF-P5]. Design never finishes: each change should
leave the code it touches a little better [POSD-P7, CC-P6, WELC-P8].

- **Check:** A typical rule or format change touches one owning module [POSD-P1, PP-P3].

### 6. Keep each piece of knowledge in one place

Each fact, rule, format or calculation should have one authoritative home. Copies drift, and
a missed copy becomes a defect [PP-P3, REF-P4, POSD-P3, POSD-T06]. Derive dependent values
instead of storing them, unless a value is expensive and read often, in which case cache it
privately [PP-T09, REF-T31], and generate repeated artifacts from one source
[PP-T08]. In data systems this becomes one system of record with rebuildable derived copies [DDIA-P1].

- **Not when:** Code that looks the same may encode different rules that change separately, so merge copies only when they change together for the same reason [PP-P3, CA-T42, CC-T36]. Test code may stay somewhat repetitive when that keeps each test clear [SWE-T45].
- **Check:** Changing one business rule edits exactly one location [PP-P3].

### 7. Hide complexity behind small, deep interfaces

A module is valuable when its interface is much simpler than what it hides. Keep the
public surface small, handle hard conditions and defaults inside the module, and remove
layers that only forward calls, unless the layer keeps an external interface unchanged
[POSD-P2, POSD-P4, POSD-T03, POSD-T04, POSD-T09, POSD-T43]. Put the part
most likely to change behind its own interface, so callers depend only on the stable side
[GOF-P2, POSD-P3]. Keep each module coupled to as few others as it needs [PP-P4], but decouple only where removing
a coupling costs less than keeping it, because each separation adds its own cost [TF-P6, TF-T32].

- **Not when:** Some shallow classes are unavoidable and still useful [POSD-P2]. Do not pull unrelated application logic into one class [POSD-P4].
- **Detail:** [guides/module-design.md](guides/module-design.md).

### 8. Point dependencies toward stable policy, and keep details at the edge

Business rules should not import UI, database, web or framework code. Those are details
that plug into the rules [CA-P1, CA-P2, CC-P5, CC-T53]. Wrap vendors, SDKs, databases and
platform APIs in an adapter you own, so a vendor change stays in one module
[PP-P5, PP-T12, CC-T51, GOF-T17]. Keep effects such as I/O at the edges, with a pure core
that is easy to test [FPS-P1, CA-P5, CC-T14]. Create concrete objects in the entry point and
pass them inward [CC-T49, CA-T20].

- **Not when:** Stable platform classes such as strings may stay concrete [CA-P1]. Do not add interfaces everywhere: add one when a second implementation or an inverted dependency needs it [CC-P5].
- **Detail:** [guides/architecture.md](guides/architecture.md).

### 9. Add abstractions for a real need, not a guess

An abstraction, extension point, option or pattern added before anything needs it is a
guess that costs indirection now [TDD-P9, CC-T77, PP-T71, REF-T85, GOF-P4]. Build the
simplest structure that fits today's needs, and add the heavier design when a failing test or
a variation the code uses or expects calls for it [GOF-P6, TDD-T18, TF-T32]. When a feature does
need a new abstraction, design its core operations cleanly and somewhat generally, adding
no operation that no caller needs [POSD-T46, POSD-T05]. The same applies at system scale:
distribute only for a named requirement [DDIA-P6, CA-T39, DDD-T69].

- **Not when:** Long-lived systems still need anticipated changes planned in advance [GOF-P6]. A hook may come early when growth is a confirmed business direction or the odds of needing it are high [CC-T77]. A system-shaping design choice deserves careful reasoning before code [TDD-P9].
- **Check:** Each new interface, pattern or service names the variation or requirement behind it [GOF-P4, DDIA-P6].

### 10. Make the code state its intent

Name things for their purpose and in the domain's terms [CC-P1, REF-P3, PP-T51, DDD-T09].
Keep each function to one idea at one level of abstraction, and extract a named piece where
a comment would otherwise explain a block [CC-P2, CC-T19, TF-P7]. Write comments for what
code cannot say: rationale, units, conditions for calling, and the behavior callers depend
on [POSD-P6, POSD-T15, POSD-T16, POSD-T17, SWE-T37]. Delete comments that only restate the code [CC-T80, TF-T22].

- **Detail:** [guides/readable-code.md](guides/readable-code.md). The books disagree on function length and on interface comments; see [the disagreements](#where-the-books-disagree).

### 11. Make failure explicit, and decide where it is handled

Validate external input once at the boundary, assert conditions you believe cannot occur,
and stop early on impossible states [PP-P6, PP-T14, PP-T15, PP-T16]. Throw only for
conditions a caller can act on, recover from recoverable failures in the lowest layer that
can, and redefine operations so some errors cannot happen, unless callers need to know about
the failure [POSD-T10, POSD-T11, POSD-T12].
Restore consistent state before reporting a failure [POSD-T53]. Release every resource on
every path [PP-T38, PP-T39, CC-T79].

- **Detail:** [guides/errors-and-contracts.md](guides/errors-and-contracts.md). Exceptions versus returned errors is a real disagreement; see below.

### 12. Assume every remote call can fail, hang or repeat

Every integration point will eventually fail. A timeout does not tell you whether the
remote side applied the request [RI-P1, DDIA-P2]. Put an explicit timeout on every remote
call, lock wait and pool checkout [RI-P2, RI-T22, RI-T13]. Wrap calls that could drain
threads in a circuit breaker [RI-T17], retry only transient errors, with capped, randomized
backoff [DDIA-T11, RI-T23], and make repeatable operations idempotent with a request or operation
ID [DDIA-P3, DDIA-T55]. Keep must-work features off calls to optional components [RI-T10].

- **Detail:** [guides/production-reliability.md](guides/production-reliability.md) and [guides/data-systems.md](guides/data-systems.md).

### 13. Bound every resource and make production observable

Give every cache, queue and result set an explicit bound, and keep sessions small
[RI-P4, RI-T68]. Partition capacity so one caller's failure leaves the others running
[RI-P3]. Expose health checks that exercise real dependencies and metrics for pools and
breakers [RI-P5]. Carry one request ID through logs and calls [RI-T70, DDIA-T55].

### 14. Ship small, reversible changes on trunk

Integrate small changes to the main line often, and hide unfinished work behind a flag
rather than a long-lived branch [SWE-P6, CC-T70, REF-T13]. The exceptions are a project policy that
allows longer branches, a flag that would add too much complexity, and a sensitive feature,
since flagged code can still be scraped [SWE-P6, REF-T13]. Roll out to a canary or a small
share of traffic first, with metric gates [RI-P7, DDIA-T16, SWE-T20]. Keep data and APIs
readable by both old and new versions during a rollout [DDIA-P5, RI-T46]. Ship additive schema
changes before the code that needs them [RI-P7], and run data migrations that old code cannot
read only after the new code is fully rolled out [RI-T47]. When a change is confirmed as the
cause of a failure, roll it back first if the revert applies cleanly, and fix forward later [SWE-T31]. Give irreversible decisions more scrutiny than reversible ones [SWE-P8, TF-T31].

### 15. Measure before you optimize or scale

Profile before tuning, across several input sizes, and back out a performance change that
shows no measured gain unless it also simplifies the code [PP-T46, REF-T87, POSD-T48]. Change the algorithm or data structure
before tuning constants [POSD-T50]. Record real load and tail-latency percentiles before
changing architecture for scale [DDIA-P7, DDIA-T09]. Include benchmark results with any optimization change [SWE-T64].

- **Detail:** [guides/performance-and-concurrency.md](guides/performance-and-concurrency.md).

### 16. Debug from evidence, not hunches

Reproduce the defect and record exact observations before you form a hypothesis. Read the
whole error message first, suspect your own recent change before the platform, and fix the
root cause rather than the symptom [PP-P8, PP-T57]. Write a test that fails because of the
bug before you fix it, and keep it as a regression test [PP-T20, REF-T04, TDD-T42].

- **Detail:** [guides/debugging.md](guides/debugging.md).

## Workflows

Follow the workflow that matches the task. Each step names its sources; the linked guides
hold the detail and the exceptions.

### Adding a feature to code that has tests

1. Check that the requirement needs software at all, and ask about the edge cases hidden in a simple-sounding request [PP-T69, PP-T53].
2. Find the code the feature touches. If its structure makes the change hard, tidy that structure first, in separate commits, and only as far as the change needs [TF-T01, TF-T16, REF-T88, TF-P3].
3. Write the call you wish existed as a failing test, and watch it fail for the expected reason [TDD-T23, TDD-T01, TDD-T02].
4. Make it pass with the quickest code. Generalize when a second test demands it, or directly when the general form is obvious or the duplication is already visible [TDD-T06, TDD-T08, TDD-T09].
5. Clean up while the tests stay green: remove duplication, name the concepts, keep functions at one level [TDD-T10, CC-T03, PP-T65].
6. Add boundary, invalid-input and failure-path tests [PP-T42, REF-T06, DDIA-T14].
7. Keep the change to one concern, review your own diff, and integrate it [SWE-T14, SWE-T63, POSD-T54, CC-T70].

Guides: [testing](guides/testing.md), [change-workflow](guides/change-workflow.md), [module-design](guides/module-design.md).

### Fixing a bug

1. Reproduce it, ideally as one command or test, and read the full error before touching code [PP-T21, PP-T57, PP-P8].
2. Write a test that fails because of the defect [PP-T20, REF-T04, TDD-T42, POSD-T20].
3. Find the root cause: bisect versions when it is a regression, and confirm the bad value in a debugger [PP-T22, PP-T58].
4. Fix it with a small diff containing no unrelated edits or hacks [PP-T72].
5. Remove workarounds trial and error added, such as retries or sleeps, unless a test or comment justifies them [PP-T66].
6. If the fix no longer fits the design, restructure the affected code rather than adding a patch, in a separate structural commit. When a deadline blocks that, record the cleanup as a follow-up [POSD-T33, POSD-T18, TF-P1].

Guide: [debugging](guides/debugging.md).

### Changing code that has no tests

1. Name the change points and the test points that can observe them [WELC-P7, WELC-T34, WELC-T35].
2. Break the dependencies that keep the code out of a test harness, at seams, with the smallest and most conservative edits [WELC-P5, WELC-T05, WELC-T60].
3. Write characterization tests that pin what the code does today [WELC-T37, CC-T75, REF-T03].
4. Put new behavior in new, tested code (sprout or wrap), so the legacy method changes only by a call [WELC-P4, WELC-T12, WELC-T13, WELC-T14].
5. Change in small verified steps, and improve only the area you touch [WELC-P2, WELC-P8].
6. Prefer gradual replacement of large legacy parts, for example behind a strangler facade or in several cutover steps, over a big-bang rewrite. Large restructurings suit parts the team has already chosen to rewrite [DDD-T58, WELC-P8, RI-T53].

Guide: [legacy-code](guides/legacy-code.md).

### Refactoring or cleaning up

1. Name the pending change, confusion or list item the cleanup serves, and choose its timing: first, after, later or never [TF-P3, TF-P4].
2. Make sure a fast, self-checking test suite covers the code [REF-T01, POSD-T47, PP-T43].
3. Take one named move at a time, using automated refactoring tools for renames and extractions, and run the tests after each move [REF-T09, REF-T14, TF-T18].
4. Commit each passing step, with no behavior change and no test edits beyond those an interface change forces [REF-T11, REF-T12, REF-T82].
5. Set a boundary and stop when the planned change can be made [TF-T16, TF-T26].

Guides: [refactoring](guides/refactoring.md), [change-workflow](guides/change-workflow.md).

### Designing a module, API or class

1. Write the public signatures, contracts and interface comments before the bodies [POSD-T21, PP-T36, FPS-P4].
2. For a major interface, data structure or module split, sketch at least two radically different designs, compare them by how easily callers can use them, and record the rejected one [POSD-P5, POSD-T13, POSD-T14].
3. Keep the interface small and deep, with defaults for the common case [POSD-T03, POSD-T09, POSD-T38].
4. Keep each design decision, format or rule inside one module [POSD-P3, POSD-T06].
5. Add patterns and extension points only for a variation you can name [GOF-P4, GOF-T13, CC-T77].
6. Use the domain's words in names, and plain value types for concepts such as money or identifiers [DDD-P2, DDD-T13, PP-T52].

Guides: [module-design](guides/module-design.md), [design-patterns](guides/design-patterns.md), [domain-modeling](guides/domain-modeling.md).

### Designing a system, service boundary or data flow

1. Name the workload, the system of record, and the downsides of each data system you choose [DDIA-P1, DDIA-T01]. List how each integration can fail, and treat a timeout as an unknown outcome [RI-T12, DDIA-P2].
2. Start simple: one machine and one deployable until a named requirement forces more [DDIA-P6, CA-T39, DDD-T69].
3. Draw boundaries where parts change for different reasons, around one consistent model [CA-P3, DDD-P3].
4. Point source dependencies at the business rules, and pass plain data across boundaries [CA-P1, CA-P6].
5. Integrate stores through one ordered log or an outbox rather than distributed transactions, unless the environment accepts the cost of distributed transactions [DDIA-P8, DDD-P7, DDIA-T50].
6. Make every consumer idempotent and tolerant of duplicates and disorder [DDIA-P3, DDD-T48].

Guides: [architecture](guides/architecture.md), [data-systems](guides/data-systems.md), [domain-modeling](guides/domain-modeling.md).

### Touching production paths: integrations, deploys, migrations

1. List how each external call can fail, including no response and slow response [RI-T12].
2. Give each call a timeout, and consider a circuit breaker and a fallback [RI-P2, RI-T17, RI-P1].
3. Bound new caches, queues and queries [RI-P4, RI-T68].
4. Ship schema changes additively first, roll out the code, then run data migrations that old code cannot read, and add NOT NULL and foreign-key constraints only after the rollout completes [RI-P7, RI-T47, RI-T49].
5. Treat any new required field or stricter validation as a breaking change, and version messages [RI-T50, RI-T52].
6. Keep secrets and environment values out of the artifact [RI-P8, PP-T35].

Guides: [production-reliability](guides/production-reliability.md), [security](guides/security.md).

### Reviewing a change, yours or someone else's

1. Confirm that structure and behavior changes are separate and each commit has one concern [TF-P1, SWE-T14].
2. Confirm that new or changed behavior comes with tests that would fail without it [SWE-T56, TDD-P8].
3. Look for knowledge duplicated across files, leaked formats and pass-through layers [POSD-T06, POSD-T07, POSD-T04].
4. Look for remote calls without timeouts, unbounded collections, and input concatenated into queries [RI-P2, RI-P4, PP-T74].
5. Check that comments add what the code cannot say and still match it [POSD-P6, CC-T71].
6. Ask the author why before judging an approach wrong, and suggest an alternative only when it is a real improvement [SWE-T36].

Each guide ends with a review checklist for its area.

## Where the books disagree

The books disagree on a few points that agents meet daily. Use the deciding condition, and
follow the codebase's settled convention when the condition does not settle it. The guides
cover more of these disagreements, in more detail.

### How long should a function be?

- **Clean Code:** keep functions near a dozen lines with at most two indentation levels, though some functions read better undivided [CC-T32], and split until each holds one level of steps [CC-P2].
- **Philosophy of Software Design:** split a method only when callers become simpler and each part reads on its own, never for length alone [POSD-T35].
- **Refactoring and Tidy First:** inline helpers that are no clearer than their bodies, and re-extract along better lines [REF-T44, TF-T19, REF-T41].
- **Decide:** Extract a block when its new name is more abstract than the code it hides [CC-T33]. Do not extract helpers that merely restate one statement or that must be read together to make sense [CC-P2, POSD-T35]. Clean Code itself allows longer functions that read better undivided, such as switch statements or formatting code [CC-T32], and leaves what counts as meaningful to judgment [CC-P2].

### Should every method have a comment?

- **Clean Code:** a comment explaining unclear code marks intent the code failed to express, so rename or extract instead. Write doc comments for APIs that other teams or projects use; within one team, clear names and signatures often suffice [CC-P1, CC-T19, CC-T72].
- **Philosophy of Software Design:** give every class, method and class variable an interface comment, written before the code, except trivial getters and setters [POSD-T22, POSD-T21].
- **Decide:** Both books reject comments that restate the code [CC-T80, POSD-P6]. Document interfaces used by other teams or projects with what a caller needs: behavior, side effects, units, ordering and conditions for calling [POSD-T15, CC-T72]. For interfaces inside one team, the books split: follow the codebase's convention, and add the interface comment whenever the name and signature leave a caller guessing [POSD-T22, CC-T72]. Inside bodies, prefer a better name to a comment, and comment only what the code cannot show, such as the reason or the overall idea of an algorithm [CC-T19, TF-T20, CC-T80].

### Exceptions or returned errors?

- **Clean Code:** report failures with exceptions, and keep normal steps free of status checks [CC-T29].
- **FP in Scala:** return recoverable failures as values (Option, Either), and reserve exceptions for failures no caller could recover from [FPS-P3, FPS-T19].
- **Philosophy of Software Design:** throw only for conditions a caller can act on, and reduce the number of error cases by redefining operations [POSD-T12, POSD-T10].
- **Decide:** Follow the codebase's existing error style. In either style, keep a recoverable failure visible to the caller that can handle it, and avoid null, NaN or sentinel values that stand for failure [FPS-P3]. In both, first ask whether the error case can be defined away or handled lower down [POSD-T10, POSD-T11].

### When should I introduce an interface?

- **Design Patterns and Clean Architecture:** program to interfaces, and invert dependencies so policy does not depend on detail [GOF-P1, CA-T08].
- **Clean Code, TDD and Pragmatic Programmer:** add no interface, option or extension point until a current caller or failing test needs it, unless growth is a confirmed direction or the odds of needing the hook are high [CC-T77, TDD-P9, PP-T71].
- **Decide:** Add an interface when there is a second implementation, an architectural boundary between policy and a volatile detail, a vendor or platform dependency, a dependency that does not exist yet, or a test that needs to pass a fake for a parameter [CC-P5, PP-P5, WELC-T17, CC-T52, WELC-T61]. A class that never changes needs no abstract type [GOF-P1].

### When should I remove duplication?

- **TDD:** remove duplication right after the test passes, because duplication signals a missing concept, though a quick copy may wait until the work is shared [TDD-P5, TDD-T10, TDD-T32].
- **Refactoring:** wait for the third similar case before unifying, unless a bug or feature exposes the copies sooner [REF-P4].
- **Clean Architecture and Clean Code:** merge copies only when they change together for the same reason [CA-T42, CC-T36].
- **Decide:** Merge when the copies encode the same knowledge and would change together. Leave look-alike code apart when it serves different actors or rules [PP-P3, CA-T42]. In tests, clarity beats removing repetition, but extract helpers for setup details the test does not depend on [SWE-T45, SWE-T44].

### Fakes, mocks or real objects in tests?

- **Clean Code and TDD:** replace databases, disks, network, clock and UI with fakes in unit tests [CC-T11]. TDD also runs the same tests against the real object once it exists, because a fake can drift [TDD-T39].
- **SWE at Google:** use the real implementation when it is fast and deterministic, prefer a fake maintained by the API's owners, and do not mock APIs whose owners may change them [SWE-T46, SWE-T13, SWE-T48].
- **Decide:** Use the real object when it is fast, deterministic and writes no data [SWE-T46, WELC-T22]. Otherwise use a fake that honors the real contract [SWE-T12]. Use a stub only to force a specific return value or error [SWE-T49]. Use interaction checks only when the call is the behavior, and back them with a larger test of the real resulting state [SWE-T11, SWE-T50].

### How much cleanup belongs in a change?

- **Clean Code and Pragmatic Programmer:** clean the code you touch as part of every change, fix broken windows in that code, and report other problems with a next step [CC-P6, PP-P1].
- **Philosophy of Software Design:** make one small design improvement in each area a change touches [POSD-P7].
- **Tidy First, Pragmatic Programmer and SWE at Google:** tidy only what the next change needs, keep a bug fix's diff to the defect, and keep each change to one concern [TF-P3, PP-T72, SWE-T14].
- **Decide:** Clean only code the change already touches, and put the cleanup in its own commits, or its own pull request when the team works that way [CC-P6, TF-T23, POSD-P7]. Keep bug-fix diffs minimal [PP-T72]. Record larger messes for later instead of widening the change [TF-T29, PP-T04].

### Small classes or deep classes?

- **Clean Code:** keep classes small and cohesive, one concern each [CC-T43, CC-T44].
- **Philosophy of Software Design:** prefer deep classes, and merge small classes that share leaked knowledge [POSD-P2, POSD-T37, POSD-T36].
- **Decide:** Split by reason to change [CC-T43, CA-P3]. Merge pieces that share a format, a message or a hidden detail, or that cannot be understood apart [POSD-T36, POSD-T37]. A split that leaves shallow pieces exposing most of what they hide adds complexity [POSD-P2, DDD-T60].

## Which guide to read

| If the task involves… | Read |
|---|---|
| sequencing a change, commits, pull requests, CI, trunk, rollback, self-review | [change-workflow](guides/change-workflow.md) |
| writing or fixing tests, TDD, test doubles, flaky or slow suites | [testing](guides/testing.md) |
| changing code without tests, seams, characterization tests, monster methods | [legacy-code](guides/legacy-code.md) |
| renaming, extracting, inlining, moving code, replacing conditionals, removing duplication | [refactoring](guides/refactoring.md) |
| naming, function shape, parameters, comments, formatting | [readable-code](guides/readable-code.md) |
| exceptions, validation, assertions, contracts, cleanup of resources | [errors-and-contracts](guides/errors-and-contracts.md) |
| module and API design, coupling, information hiding, when to abstract | [module-design](guides/module-design.md) |
| choosing or applying a design pattern, state machines, events and callbacks | [design-patterns](guides/design-patterns.md) |
| layers, dependency direction, frameworks, components, monolith versus services | [architecture](guides/architecture.md) |
| business modeling, bounded contexts, aggregates, events, sagas, CQRS | [domain-modeling](guides/domain-modeling.md) |
| pure functions, effects, immutability, Option/Either, folds, laziness | [functional-style](guides/functional-style.md) |
| databases, replication, partitioning, transactions, consistency, streams, schemas | [data-systems](guides/data-systems.md) |
| timeouts, retries, circuit breakers, load, health checks, rollouts, migrations | [production-reliability](guides/production-reliability.md) |
| injection, secrets, authorization, passwords, personal data | [security](guides/security.md) |
| speed, profiling, hot paths, threads, locks, shared state | [performance-and-concurrency](guides/performance-and-concurrency.md) |
| a bug, a failing build, an incident or outage | [debugging](guides/debugging.md) |
| new projects, requirements, demos, dependencies, deprecation, docs, decisions | [project-and-team](guides/project-and-team.md) |

## Before you finish

Run through this list before you hand back a change. Each item points to the rule behind it.

- [ ] The tests pass, and the change adds tests for each new or changed behavior [SWE-T56, TDD-T15].
- [ ] Each new test was seen failing, and it asserts outcomes through the public interface [TDD-T02, SWE-T10].
- [ ] Structure and behavior changes sit in separate commits, and refactoring commits change no tests beyond edits an interface change forces [TF-P1, REF-T82].
- [ ] The diff holds one concern, with no unrelated edits, and a bug fix holds only the fix [SWE-T14, PP-T72].
- [ ] No rule, format or constant is now defined in two places [PP-P3, POSD-T06].
- [ ] New abstractions, options and patterns each serve a current caller or a named variation [CC-T77, GOF-P4].
- [ ] Business rules import no framework, database or UI code, and vendor calls stay in adapters [CA-P2, PP-P5].
- [ ] Every new remote call, lock wait and pool checkout has a timeout, and every new cache or queue has a bound [RI-P2, RI-P4].
- [ ] External input is validated at the boundary and bound as parameters in queries and commands [PP-T14, PP-T74].
- [ ] No credentials or environment values are written into source or build artifacts [PP-T35, RI-P8].
- [ ] Names state purpose in domain terms, and comments explain only what code cannot [CC-P1, POSD-P6].
- [ ] Schema and API changes stay readable by old and new versions during rollout [DDIA-P5, RI-T46].
- [ ] Performance changes come with measurements [SWE-T64, POSD-T48].
- [ ] You read your own diff before calling the work done, and the docs reflect the change [SWE-T63, POSD-T54].

## Scope and limits

- The rules come only from these 14 books, so the skill says nothing about topics they do not
  cover, such as user-interface design or specific frameworks. Design Patterns, for
  instance, leaves out concurrency, distribution and real-time design (see the summary in
  [books/design-patterns/principles.md](books/design-patterns/principles.md)).
- The FP in Scala entries use Scala vocabulary. The ideas transfer to any language with
  first-class functions, but follow the idioms of the codebase's own language.
- Several books mark their strictest rules as defaults to weigh against context, such as Clean Code
  on method length [CC-T32] and test-first rules for throwaway sketches [CC-T05], and Tidy First on
  timing [TF-P4]. Treat the rules
  as strong defaults, and state the reason when you depart from one.
