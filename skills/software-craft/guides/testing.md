# Testing: test-first, test design, test doubles, suites

This guide covers writing tests before code, choosing and shaping each test, deciding what to assert, choosing between real objects and test doubles, sizing and isolating tests, and gating changes in CI. The single most important idea is that a test is evidence only when it checks observable behavior, could have failed, and runs fast and reliably enough that people keep running it.

**Read this when:** adding a behavior or a new module, fixing a reported defect, writing or reviewing a test file, deciding whether to mock or fake a dependency, a test is slow, flaky or order-dependent, a test needs long setup, integrating with another team's API, testing an operation that must obey laws, setting up or changing CI test gates, reviewing a diff that touches tests.

**Entry IDs** such as `WELC-T12` point to `../books/<book>/techniques.md` (T) or `principles.md` (P);
the prefix table is in [SKILL.md](../SKILL.md).

## Contents

- [Rules: writing tests first](#rules-writing-tests-first)
- [Rules: test structure and naming](#rules-test-structure-and-naming)
- [Rules: what to assert](#rules-what-to-assert)
- [Rules: test doubles and testable design](#rules-test-doubles-and-testable-design)
- [Rules: test sizes, isolation and scope](#rules-test-sizes-isolation-and-scope)
- [Rules: keeping the suite fast and trusted](#rules-keeping-the-suite-fast-and-trusted)
- [Rules: CI gating](#rules-ci-gating)
- [Playbooks](#playbooks)
- [Where the books disagree](#where-the-books-disagree)
- [Review checklist](#review-checklist)
- [More entries in this area](#more-entries-in-this-area)

## Rules: writing tests first

### 1. Write a failing test before new behavior

Before you write production code for a new or changed behavior, write an automated test that requires it. TDD, Clean Code and Clean Architecture all start new work this way, because the test then specifies the behavior instead of guessing at it, defects show up while they are cheapest to fix, and no untested production code appears. In code that already has tests, Legacy Code asks for one new test case per new behavior, and SWE at Google rejects changes that add behavior without tests. [TDD-P1, TDD-T01, CC-T05, CA-T03, WELC-T02, SWE-T56]

- **Do:** Add the test first, then the smallest production change that satisfies it. Add one test case for each new behavior in an area that already has tests.
- **Not when:** A pure refactoring keeps behavior the same, so the existing tests guard it instead. A throwaway design sketch that will never ship is exempt.
- **Check:** In the commit history or diff, each production change follows a test that covers it, and each new behavior has its own test case.

### 2. Watch every new test fail for the expected reason

Run each new test before the implementation exists and confirm it fails on the expected assertion. A test that has never failed does not prove it can catch the missing behavior, and when tests are added to working code, break the behavior on purpose to see the test go red. When a test you expected to fail passes, find out why before trusting it. Coverage only shows that lines ran, not that results were checked, so use it to find untested code rather than as proof. [TDD-P8, TDD-T02, CC-T06, REF-T02, TDD-T17, SWE-T54]

- **Do:** Run the new test once it compiles and note the failure. For tests added after the fact, inject a fault and confirm some test fails. Investigate any surprise pass.
- **Not when:** When the check is a subjective judgment, an injected fault cannot reveal false confidence. Passing unit tests alone do not establish security or concurrency correctness. Coverage does not explain a surprise pass, so do not accept it as the reason. Swapping one constant for another is not a meaningful injected defect.
- **Check:** The PR notes or commits record the new test failing on its expected assertion, or failing after an injected fault.

### 3. Choose the smallest next test that shows progress

Start a new operation with its most trivial case, then pick each following test as the smallest one that shows something new and that you can make pass. Small visible increments keep each failure close to the change that caused it. Write the test with the call you wish callers had, and when the new test does not compile, remove the errors one at a time with the least code, starting from the interface. [TDD-P2, TDD-T03, TDD-T04, TDD-T23, TDD-T24, CC-T06]

- **Do:** Keep a list of planned tests, pick the smallest visible step, and write only as much test as makes it fail. Let the test shape the signature, and revise both together when a better shape appears. [TDD-T25]
- **Not when:** Familiar work may need only one starter test for one or two operations. When the path is clear, larger routine steps are sound, and step size depends on experience, so no single rule fits. When the unit's overall design is still unsettled, a narrow test focus can hide it.
- **Check:** The first test for a new operation uses a trivial input. Each stub added in the diff answers one compile error. Signature changes arrive with the test changes that use them.

### 4. Reach green fast, then generalize only on evidence

Make a failing test pass with the quickest code, even a constant, and generalize only when another failing test demands it. A constant is the least code that satisfies the test, so the real design waits for evidence. When you are unsure how to generalize, add a second example with different inputs first. TDD calls this triangulation. Copying a working test and its code to reach green on a new variant is also allowed, as long as the copy is merged afterwards. [TDD-P4, TDD-T06, TDD-T08, TDD-T09, TDD-T32]

- **Do:** Pass with a constant or a copy, commit green, then replace the constant or merge the copy only in steps driven by a new failing test or by duplication removal.
- **Not when:** The clean implementation is obvious and quick to type, so write it directly. Use a second example only when truly unsure, since triangulation can loop without end, and generalize directly when the duplication is already visible. Some teams wait for three or four uses before merging a copy, and the author accepts undoing early refactorings.
- **Check:** Generalized code is backed by at least two tests with different inputs. Constants in production code are replaced only in commits driven by a failing test. Copied code is merged before the work is shared.

### 5. Clean up after green, as a separate step

Once the test passes, remove duplicated logic and literals between the code and its tests before writing the next test, and keep that cleanup apart from behavior changes. Mixing the two hides which change broke which test. Make near-identical code identical in small steps before merging it, because merging too early hides a real difference. The mechanics of the cleanup belong to the [refactoring](refactoring.md) guide. [TDD-T06, TDD-T07, TDD-T10, TDD-T11]

- **Do:** Refactor only from a state where all tests pass, and commit refactorings separately from feature changes.
- **Not when:** Behavior not covered by any test cannot be checked as a refactoring, so cover it first (rule 29). Quick-copy duplication may wait until the work is shared. Near-identical code is reconciled before it is merged.
- **Check:** Commits separate feature and refactoring changes, previously passing tests still pass, and no repeated expression or literal remains in shared production code.

### 6. Let a hard-to-write test change the design

A test that needs long setup, private state or the whole system is evidence about the design. Change the design rather than working around the test. When one assertion needs a long setup, split the tangled object into smaller ones that set up quickly. When an edit in one part breaks a test in another part, remove the hidden dependency behind it or merge the two parts. Writing the test as the first caller of a new interface exposes hard-to-use parameters and hidden hooks early. [TDD-P6, TDD-T12, TDD-T49, PP-T40]

- **Do:** Treat setup that outgrows the behavior under test, global setup, or cross-module test breakage as a design task.
- **Not when:** When no better design has appeared yet, a test may check private state for now, with a note that the design needs work (rule 13). A hard test may reveal a problem with the testing approach as well as with the design.
- **Check:** Each test's setup builds only the objects its assertion uses. Tests call code through its public parameters, with no global state or hidden hooks.

## Rules: test structure and naming

### 7. Give each test one action and one behavior

Shape each test as setup, one stimulus, then assertions about one behavior. TDD, Clean Code and SWE at Google agree on this three-part shape, because a fixed shape makes cause and effect easy to read and a failing single-behavior test points straight at the broken behavior. Several assertions are fine when together they support one logical claim. [TDD-T35, CC-T09, SWE-T38, SWE-T39]

- **Do:** Separate the arrange, act and assert blocks visibly. Split a test that asserts several unrelated outcomes.
- **Not when:** Trivial tests can separate the parts with whitespace instead of comments. A multistep process can alternate action and expectation blocks.
- **Check:** Each test body has one action call and assertions that support one claim, in that order, unless it is a multistep test.

### 8. Name each test after its action and expected outcome

Name each test for the rule or case it checks, so a failing name states what broke without opening the body. A name that needs the word "and" covers two behaviors and should be split. When code shows behavior you did not design for, including surprising behavior of external code, record it as a test whose name states the rule. Rename vague tests and fixtures once understanding improves. [SWE-T40, CC-T16, TDD-T31]

- **Do:** Use names of the form action plus expected outcome, and name fixtures for their scenario.
- **Check:** No test name joins two behaviors with "and", and names describe a business rule or case rather than a label such as `test1`.

### 9. Keep test bodies straight-line code

Write tests without loops, conditionals or computed expected values. A test without logic is obviously right on inspection, and it cannot hide a bug in its own control flow. [SWE-T41]

- **Do:** Write each case as its own straight-line test instead of looping over cases inside one test.
- **Check:** Test bodies contain no `if`, `for` or `while` statements.

### 10. Show the inputs that matter and hide the rest

Keep the values the assertion depends on visible in the test, and move construction details it does not depend on into helpers. Let fixture builders fill omitted fields with sensible defaults so that each test sets only what it checks, which also means a production signature change touches only a few tests. Repeated multi-line setup or assertion steps can become one named helper. Shared objects that several tests build the same way can move into the per-test setup method, and a new fixture deserves a new test class. [SWE-T44, CC-T07, CC-T08, TDD-T33, TDD-T37]

- **Do:** Add a builder with defaults for wide objects. Extract incidental setup into named helpers, and keep influential values inline.
- **Not when:** Setup must not hide values that individual tests depend on. Keep setup in place when it is short enough to read, or when readers need to see each allocation. See the tension on [duplication in tests](#should-test-code-remove-duplication-or-repeat-itself-for-clarity).
- **Check:** Each test sets only the fields its assertion depends on, and those values appear in the test body, not only in a shared helper.

### 11. Hold test code to the production standard

Give test names, helpers and setup the same care as production code, and refactor brittle or slow tests. Tests that rot get ignored, which removes the protection the suite was meant to give. Treat tests as the outermost component: test code imports production code, and production code never imports tests. [CC-T17, SWE-T58, CA-T69]

- **Do:** Review and lint test code like production code. Simplify any test complex enough to need its own test.
- **Not when:** Edit assertions only when documented behavior changes, and leave tests untouched during a pure refactoring (rule 28).
- **Check:** Test code passes the same review and lint rules as production code, and no production module imports a test package.

## Rules: what to assert

### 12. Assert exact expected values, written as literals worked out by hand

Compare each result with one specific expected value rather than a weak condition such as non-zero. Write the expectation as a literal in the test, worked out by hand, not assembled from variables or produced by calling the code under test. A test that reuses the production calculation or lookup cannot catch that calculation's errors. [TDD-T16, SWE-T42, CC-T78]

- **Do:** Work out expected values by hand, and write them inline. Put the expected value first in equality assertions where the framework expects that order.
- **Check:** Assertions compare results to literals in the test body. No test calls the production lookup or formula to build its expected value, and each test holds its own assertions rather than one shared validation call.

```python
# Circular: reuses the production lookup, so it cannot catch its errors.
assert price_with_tax(100, rate=0.2) == 100 * (1 + TAX_TABLE["std"])

# Exact, hand-computed literal.
assert price_with_tax(100, rate=0.2) == 120
```

### 13. Test observable behavior through the public interface

Call code through its public API and assert on returned values or resulting state, not on the calls it made internally. Such tests survive refactoring of the internals, and SWE at Google adds that every observable behavior gets depended on, so a change in ordering, timing or log format counts as breaking even when the signature stays the same. Count as public only what outside callers may use without asking the owners. Test a helper that serves one or two classes through those classes, and test general libraries directly. [SWE-P5, SWE-T07, SWE-T08, SWE-T10, CC-T15, TDD-T13]

- **Do:** Import the public API in the test, assert on results or stored state, and test every behavior you want to keep.
- **Not when:** When the call itself is the behavior, such as a cache that must reduce reads, add an interaction check (rule 18). Test a private detail directly only when no public test can reach it. When no better design has appeared yet, a test may read a private variable for now, with a note that the design needs work. Many tests legitimately combine result checks and interaction checks. See the tension on [private state](#may-a-test-reach-private-state-or-a-helper-directly).
- **Check:** Assertions call public methods or read stored results, not private fields or mock call records. A helper used by one or two classes has no separate test of its own.

### 14. Make each failure explain itself

Give each assertion a failure message that names the expected value, the actual value and the relevant inputs. In a batch run no debugger is open, so the message is the only record of the cause. When properties are combined in a library that supports labels, label each part so that the failure report shows which part failed. [TDD-T46, SWE-T43, FPS-T43]

- **Do:** Prefer assertion helpers that print expected and actual values, and add a message where the helper cannot.
- **Not when:** A team that has tried both ways and found messages add no value may drop them. Languages without such helpers need the key details written into the message by hand.
- **Check:** Failure output shows expected and actual values, not only `false`, and combined properties carry labels that appear in the failure output.

### 15. Test boundaries, bad input and failure paths, not only the happy path

After the ordinary cases, add empty, zero, negative, blank, minimum and maximum inputs, plus inputs the contract rejects. Happy-path tests miss the inputs that cause real failures, and error handlers seldom run, so their bugs stay hidden for a long time. Simulate errors and latency from each dependency on purpose: exceptions at unit level, RPC faults at integration level. DDIA asks that each error branch get the same care as the success path. [REF-T06, PP-T41, PP-T42, WELC-T41, POSD-T20, SWE-T53, DDIA-T14]

- **Do:** Derive cases from the documented contract: rejected inputs, boundary values and promised results. Add at least one failing call per dependency that can fail, and one input per type conversion on the path. When zipping two effectful streams whose lengths may differ, test inputs of unequal length, since the zip stops at the shorter one. [FPS-T65]
- **Check:** Tests exist for empty, zero, negative and blank inputs, for unavailable resources, and for each error branch, and they assert the response, not only that no crash happened.

For process kills, network partitions and harness servers that fail like real peers, see [production reliability](production-reliability.md). [DDIA-T13, DDIA-T40, RI-T27]

## Rules: test doubles and testable design

### 16. Use the real object when it is fast and deterministic

Prefer the production implementation of a dependency whenever the test can build it directly and it runs fast and deterministically. A real implementation tests real behavior, while a double only tests what it was told to do. Keep using the real code until its cost forces a switch, then move only the affected tests to a double. [SWE-T46, SWE-T47, WELC-T22]

- **Do:** Construct plain collaborators directly. Use a real collaborator that is cheap to build and only reads data.
- **Not when:** Replace real objects that are slow, nondeterministic, take long to build or write data. When a real dependency's failure reveals a production bug, keep the real code and fix the bug.
- **Check:** Doubles appear only where the real code is too slow, flaky or unavailable, or where a stub forces a rare state.

### 17. Replace slow or nondeterministic dependencies with in-process fakes

Swap databases, disks, network, clock and UI for fakes in unit tests, so the tests stay fast and give the same result everywhere. A fake is a lightweight working implementation. It must match the real contract's outputs and state changes except where the contract leaves details open, and the same tests should run against the real implementation once it exists, because a fake can drift. Ask the API's owners to provide and maintain its fake, since they know the contract best. [CC-T11, SWE-T06, SWE-T12, SWE-T13, TDD-T39]

- **Do:** Write one contract test suite and run it against both the fake and the real implementation. Have the fake raise errors on paths it does not support. If owners decline to provide a fake, wrap their API in one class and fake that wrapper.
- **Not when:** An in-memory filesystem substitute is acceptable inside a small test. When contract tests against the real implementation are too slow, only the fake's owners run them.
- **Check:** Unit tests touching a database, disk, network or clock use a fake or a data-returning stub. Each fake has tests that also run against the real contract, and the fake lives with the owning team's code.

```python
class StoreContract:            # shared cases, written once
    def make_store(self): raise NotImplementedError
    def test_saved_item_reads_back(self):
        s = self.make_store(); s.put("k", 1)
        assert s.get("k") == 1

class TestFakeStore(StoreContract):    # fast, in-process fake
    def make_store(self): return InMemoryStore()

class TestRealStore(StoreContract):    # same cases, real implementation
    def make_store(self): return PostgresStore(test_dsn())
```

### 18. Stub only to force a state, and check calls only when they are the behavior

Use a stub only to return a value or error that puts the system into a state the test needs, such as an error the real dependency rarely produces. Verify call counts or order only when that count or order is itself a requirement, or when the call has an outside side effect. Verifying every call couples tests to internals the behavior does not depend on. When a class's effects are visible only through a collaborator, a recording fake that captures the calls makes them observable. Back each interaction-only unit test with a larger test that checks the real resulting state. [SWE-T49, SWE-T11, SWE-T50, WELC-T07, WELC-P6]

- **Do:** Stub only the few functions the assertions depend on. Use a maintained mock library when a test needs several doubles, or hand-write slim recording fakes when none exists, storing only the values the tests assert on. [WELC-T11, WELC-T08]
- **Not when:** Do not stub when the system relies on the real contract, or when the test must read back data it saved, and use a fake instead. Production code must never construct or call a test fake, so use a real implementation or a seam where production needs one.
- **Check:** Interaction assertions appear only where count or order is a requirement. Each interaction-only test has a companion that asserts the real outcome. Fakes sit in test sources.

### 19. Do not mock APIs that their owners may change

Do not mock a library or service whose owners may change it, and do not replace every collaborator with a double. A mock of a changing API keeps passing while real behavior moves away from it. Use the owner's fake, your own wrapper if the owners decline to provide one, or an integration test instead. [SWE-T48, SWE-T13, SWE-T51, RI-T51]

- **Do:** Stub only APIs your own team owns, and test other teams' APIs through their fake, your own wrapper, or a contract test (rule 22).
- **Check:** Test code mocks only same-team APIs, and no test mocks every collaborator of the class under test.

### 20. Pass collaborators in, and keep hard-to-test code thin

Give each unit its collaborators and expensive resources as constructor or method parameters, not as objects it creates or reaches through globals and singletons. Tests can then substitute a fake without touching production code or global state that other tests read. Put code that touches a screen, socket, hardware or framework behind a thin forwarding layer, and move formatting and branching logic out of the hard-to-test part into a testable one. A program written as a description of effects can run in tests through a pure interpreter that feeds scripted input and collects output. [CC-T12, TDD-T40, CC-T13, CA-T63, FPS-T64]

- **Do:** Inject dependencies, and split a humble wrapper from the logic it forwards to. Module-level design of seams and interfaces is covered in [module design](module-design.md), and effect interpreters in [functional style](functional-style.md).
- **Check:** No global variable or singleton holds a resource tests must replace. The thin wrapper contains only forwarding calls, with no branches or loops. Effect programs are tested through the pure interpreter.

## Rules: test sizes, isolation and scope

### 21. Keep most tests small, hermetic and below the UI

Write most tests small: one process, no sleeps, no real network or file I/O, and each test building its own state. Label every test small, medium or large by the resources it uses, separately from its scope, so the runner can enforce limits. Attach most tests to classes and functions rather than screens or commands, since such a test points a failure at one cause. Business rules and domain models should be testable without a UI, web server, database or device running, by building aggregates and value objects directly and using stub gateways. [SWE-P4, SWE-T05, SWE-T06, WELC-T04, CA-P5, CC-T14, DDD-T55]

- **Do:** Declare a size on each test. Test policy and domain code against in-memory fakes, and keep database or file tests in a separate set. [WELC-T03]
- **Not when:** Larger tests remain necessary for behavior that small tests cannot reach (rule 22).
- **Check:** Size labels match resources and the runner enforces them. The rule test suite runs with no server, database, GUI or device started, and most test files call classes or functions, not widgets or pages.

### 22. Use integration and end-to-end tests for contracts and emergent behavior

Write integration tests for the interaction between a few components, especially where different teams own them, because contracts between owners are where unit tests stop seeing failures. In the consumer's repository, write contract tests for every provider behavior your code relies on and run them against the provider's staging system. Reserve end-to-end tests for behavior that appears only when several parts work together, and drive them through the public entry point. When you replace a module with another that shares its interface, test the substitute through the exact calls its parent makes. [SWE-T51, RI-T51, SWE-T52, RI-T60]

- **Do:** Assert on the shared contract, not on either side's internals. Before code depends on a new or uncertain library method, write a small learning test that pins the behavior you rely on, so an upgrade reveals changed assumptions. [TDD-T30]
- **Not when:** A learning test is unnecessary when the external code is trusted and its behavior does not matter to your code.
- **Check:** Each cross-team integration has a test that runs both sides together or a consumer contract test. Substitute-module tests cover every interface method the parent calls.

For compatibility tests across rolling upgrades, decoding old fixtures with new code and the reverse, see [data systems](data-systems.md). [DDIA-P5]

### 23. Test business rules through the API, not through screens

Test business rules through the application's normal API, and keep rule tests away from volatile screens and navigation, which break with every UI change even when the rules are unchanged. When a test needs a state that normal operation does not offer easily, give tests a dedicated testing API that sets state directly and bypasses slow or secured steps, reusing the interactors the UI calls. [CA-T70, CA-T71]

- **Do:** Keep the testing API out of production builds.
- **Not when:** The testing API's powers would be dangerous in the production system, so it must not ship there.
- **Check:** Rule tests call application APIs and never navigate GUI screens, and the testing API is absent from production artifacts.

### 24. Give each test its own state and control time

Make every test build its own fixtures and leave no shared mutable state another test reads, so it passes alone and in any order. Release files and connections that setup opens in a single teardown. Control the clock, thread scheduling and network latency, and wait for asynchronous work by polling for the expected state with a timeout or subscribing to an event, not with fixed sleeps, which are either too slow or flaky. [TDD-T34, CC-T10, SWE-T09, REF-T05, TDD-T36, SWE-T55]

- **Do:** Share only immutable objects between tests. Run the suite in a random order to expose hidden dependencies. For threaded code with rare bugs, a swappable timing hook that tests make sleep or yield randomly can expose rare orderings, bound to a no-op in production. [CC-T61]
- **Not when:** A slow fixture may be shared if a teardown resets it after each test, and when object creation is too slow, make sure one test's failure cannot change another's result. Teardown does not run after a failed setup, so do not rely on it for resources setup never finished allocating.
- **Check:** The suite passes in shuffled order. Test code contains no fixed sleep calls. Every resource opened in setup has a matching release in teardown.

```python
# Flaky or slow: guesses how long the worker needs.
time.sleep(2); assert job.status == "done"

# Bounded wait on the observable state (event or poll helper).
done = wait_until(lambda: job.status == "done", timeout_s=5)
assert done, f"status={job.status} after 5s"
```

### 25. Check laws with generated inputs, not single examples

For an operation that must satisfy laws, such as associativity or an identity value, generate inputs and compare two expressions, rather than checking one fixed literal case. The compiler does not enforce interface laws, so tests must. When the property's predicate can throw, evaluate it inside an exception handler that reports the exception as a failure naming the input, so one exception does not crash the run. [FPS-P7, FPS-T42, FPS-T43]

- **Do:** Write law tests with a generator and an equality between two results, and label each combined property. Run parallel law tests under fixed-size executors as well.
- **Check:** Law and property tests use a generator, compare two results, and report exceptions as labelled failures.

## Rules: keeping the suite fast and trusted

### 26. Keep the suite fast enough to run after every change

Run the tests after each small change, and keep the suite fast enough that people do. Clean Code treats test speed as a design requirement, Refactoring wants the suite runnable with one command, and slow tests get skipped, which removes their feedback. A passing suite is strong evidence, not proof. The books give different numbers for different scopes, which the tension on [speed](#how-fast-must-the-tests-be) sorts out. [CC-P4, REF-P2, TDD-P7, TDD-T14, WELC-T03]

- **Do:** Document one command that runs the full suite. Move slow tests out of the unit set into a separate set rather than deleting them.
- **Not when:** Under very high stress the habit of running tests often can still break down.
- **Check:** One documented command runs the suite, and the unit set holds no test that takes a tenth of a second or longer.

### 27. Do not make a run green by skipping or deleting tests

Keep every test passing when code goes into a shared branch, and do not disable, skip or delete a failing test just to get there. A skipped test hides the defect its failure was reporting. Fix the test, or remove it on purpose with a stated reason. [TDD-T15, PP-T73, CC-T69]

- **Do:** Fix the code or the test. If a test must be set aside, add a reason and an open ticket at the skip marker.
- **Not when:** A solo session may end on a deliberately failing test that waits until work resumes, and a known gap may be recorded beside a test that cannot pass yet, but neither applies to a shared check-in. [TDD-T48] Clean Code allows disabling a slow or broken test with a message saying why, except an intermittent threaded test. See the tension on [skipping](#may-a-failing-test-ever-be-skipped).
- **Check:** The diff adds no commented-out or disabled test without a reason and a ticket, and the PR shows the full suite passing.

### 28. Leave existing tests alone during a refactoring

When a change preserves behavior, leave the existing tests untouched and investigate any test edit it seems to need. An untouched test is the proof that behavior survived. Edit an existing test only when documented behavior or the contract changes, and add new tests for new behavior. [SWE-T60, REF-T82, SWE-T61]

- **Do:** Split a change that needs both test edits and restructuring into a behavior commit and a pure refactoring commit. [TDD-T07]
- **Not when:** An interface change forces a mechanical edit to the tests, or the refactoring reveals a case nobody tested, which earns a new test.
- **Check:** A pure refactoring diff edits no existing test file except where a signature changed. A fix to a failing test records whether the code or the test was wrong.

### 29. Build a self-checking suite before restructuring code

Before restructuring a section, or before any large structural change, strengthen its tests and keep them passing. Behavior is protected only once automatic tests cover it. In legacy code, find a seam and pin current behavior with characterization tests, which assert what the code does today rather than what it should do. The full procedure lives in the [legacy code](legacy-code.md) and [refactoring](refactoring.md) guides. [REF-T01, POSD-T47, TDD-T45, REF-T03]

- **Do:** Write tests for the existing behavior first, confirm they fail on an injected fault, then refactor.
- **Not when:** Creating a seam without tests is itself risky, so keep that step minimal. Placeholder output in a characterization test must be confirmed before it is treated as correct.
- **Check:** Tests covering the restructured behavior land before the refactoring commit, and they fail when a fault is injected.

### 30. Add a failing regression test for each defect

When a defect is reported or found by hand, write the smallest test that fails because of it, watch it fail, then fix. The failing run proves the test catches the defect, and the kept test stops it from returning unnoticed. TDD adds a second regression test that runs the whole application, and Pragmatic Programmer turns each ad hoc check that exposed the defect into an automated test. The hunt for the cause belongs to the [debugging](debugging.md) guide. [TDD-T42, REF-T04, PP-T20, PP-T62, RI-T07, SWE-T57, POSD-T20]

- **Do:** Reproduce the failing input in a test, see it red, fix, see it green, and keep it in the shared suite.
- **Check:** Every bug-fix diff includes a test that fails without the fix and exercises the reported failure path.

## Rules: CI gating

### 31. Gate each change on fast, reliable checks, and run slow ones after submit

Run the project's listed checks, such as formatting, analysis, coverage and tests, before a change lands, since defects are cheaper the earlier they are found. Keep presubmit to fast and reliable tests, because slow or unstable gates delay everyone and teach people to ignore failures. Move end-to-end, flaky or resource-heavy suites to a post-submit or release job rather than dropping them, and make a larger test hermetic and independent of the user who runs it before it gates presubmit. [SWE-P3, SWE-T15, SWE-T24, SWE-T26, SWE-T25]

- **Do:** Name the gating checks in the contributing doc. List every suite moved out of presubmit in a post-submit or release pipeline.
- **Not when:** A change that must be caught before it reaches the shared codebase needs a presubmit gate even if the test is slow. When hermetic setup is too costly, teams often mix in live backends, which then stay out of presubmit.
- **Check:** Presubmit lists only fast suites, every suite moved out runs post-submit, and no quality check is dropped for speed.

### 32. Run every test the change can affect

For a change to shared code, select tests from the build dependency graph and run every test transitively affected. Changes often break distant dependents, so testing only the touched project misses real breakage. Clean Code asks for the full build and tests on every push. Put each new test where the suite's standard discovery finds it, since a test outside the shared suite protects only its author's machine. [SWE-T32, CC-T68, SWE-T59]

- **Do:** Configure CI to trigger on each push and to expand the test set to dependents of the changed files.
- **Not when:** When only one project's own code changed, that project's tests may gate it. Slow affected tests may run post-submit (rule 31).
- **Check:** CI triggers on each push, the selected test set includes targets that depend on the changed files, and new test files appear in the CI run.

## Playbooks

### When you add a new behavior test-first
1. Write the planned cases on a test list, including boundary and failure cases, and park side ideas on it. [TDD-T25, REF-T06, PP-T42]
2. Pick the most trivial case, and write the test with the call you wish callers had. [TDD-T03, TDD-T23]
3. Remove compile errors one at a time with the least code, then run the test and see it fail on the expected assertion. [TDD-T24, TDD-T02]
4. Make it pass with the quickest code, a constant if the logic is unclear. [TDD-T06, TDD-T08]
5. Remove duplication between the code and the test, as a separate step from the next behavior. [TDD-T10, TDD-T07]
6. Pick the next smallest visible case. When unsure how to generalize, add a second example first. [TDD-T04, TDD-T09]
7. Run the tests after each small change, and before sharing, make sure the whole suite is green. [TDD-T14, TDD-T15]

### When you fix a reported defect
1. Reproduce the defect and keep the manual check that exposed it. Finding the cause is covered in [debugging](debugging.md). [PP-T62]
2. Write the smallest test that fails because of the defect, and watch it fail. [TDD-T42, REF-T04, PP-T20]
3. Fix the code, see the test pass, and add a regression test that runs the whole application. [TDD-T42, RI-T07]
4. If the fix breaks other tests in a way they do not explain, write a focused test for that cause before retrying. If the fix was a large step, undo it and redo it in smaller steps instead. [TDD-T47, TDD-T05]
5. Check that the fix diff carries the new tests into the shared suite. [SWE-T57, SWE-T59, POSD-T20]

### When the code under test reaches a database, network, clock or another team's service
1. If the real object is fast, deterministic and only reads data, use it. [SWE-T46, WELC-T22]
2. If it is slow or nondeterministic, pass it in as a parameter, and use an in-process fake for unit tests. [CC-T12, TDD-T40, CC-T11, SWE-T06]
3. Get the fake from the API's owners, or wrap their API in one class and fake the wrapper. [SWE-T13]
4. Run one contract suite against both the fake and the real implementation. [SWE-T12, TDD-T39]
5. Use a stub only to force a rare state such as an error. [SWE-T49, SWE-T53]
6. Verify calls only when the call is the requirement, and pair each interaction-only test with a state test at larger scope. [SWE-T11, SWE-T50]
7. Assert on results and state, not on internal call sequences. [SWE-T10, CC-T15]

### When you must restructure code that has weak tests
1. Find where the change lands and a seam near it, using the [legacy code](legacy-code.md) guide for dependency breaking. [REF-T03]
2. Write characterization tests that pin today's behavior, and confirm they fail on an injected fault. [REF-T01, REF-T02, TDD-T45]
3. Add boundary and conversion inputs for the paths you will touch. [WELC-T41, REF-T06]
4. Keep the suite passing through the restructuring, and leave the tests unchanged except where an interface change forces an edit. [POSD-T47, SWE-T60, REF-T82]
5. Add new tests only for cases the work revealed. [REF-T82]

### When a test is slow, flaky or fails for unrelated edits
1. Check for shared state, ordering and real time. Give the test its own fixtures and run the suite shuffled. [SWE-T09, CC-T10, TDD-T34]
2. Replace fixed sleeps with bounded polls or event waits. [SWE-T55]
3. If an edit elsewhere broke it, remove the hidden coupling or merge the two parts. [TDD-T49]
4. If a real dependency made it slow, move only that test to a double. If the real dependency revealed a production bug, fix the bug instead. [SWE-T47]
5. If it is still slow, move it to a separate set or to post-submit rather than deleting it. [WELC-T03, SWE-T24, SWE-T26]
6. Do not skip it to go green. A skip needs a reason and a ticket. [PP-T73, CC-T69]

### When you integrate with an API another team owns
1. Write learning tests for the library or API behavior you rely on. [TDD-T30, TDD-T31]
2. Do not mock it. Use the owner's fake, or wrap their API in one class and fake the wrapper if they decline to provide one. [SWE-T48, SWE-T13]
3. Write consumer contract tests that run against the provider's staging system. [RI-T51]
4. Add an integration test that runs both components and asserts the shared contract. [SWE-T51]
5. Test each failure the integration can produce, with injected faults or a harness that fails like the real peer. [SWE-T53, RI-T27, DDIA-T14]

### When you set up test gating for a project
1. Add CI from the first commit of a long-lived project. [SWE-T18]
2. Label tests by size and let the runner enforce the limits. [SWE-T05]
3. Run the listed checks on every push, before the change lands. [SWE-T15, CC-T68]
4. Gate presubmit on fast, reliable, hermetic tests, and select every transitively affected test. [SWE-T24, SWE-T25, SWE-T32]
5. Put slow, flaky or costly suites in post-submit or release jobs. [SWE-T26]
6. Make sure new tests are found by standard discovery. [SWE-T59]

## Where the books disagree

### Should a test use the real dependency or a double?
- **SWE at Google:** Prefer the real implementation whenever it is fast and deterministic, keep it until its cost forces a switch, and do not mock APIs owners may change. [SWE-T46, SWE-T47, SWE-T48]
- **Legacy Code:** Use a cheap, read-only real collaborator, but fake a collaborator to record calls when effects show only through it, and use a mock library when several doubles are needed. [WELC-T22, WELC-T07, WELC-T11]
- **Clean Code and TDD:** Replace databases, disks, network, clock and UI with fakes in unit tests, and run the same cases against the real object. [CC-T11, TDD-T39]
- **Decide:** Use the real object when it is fast, deterministic, cheap to build and writes no data. Use a fake when it is slow, nondeterministic or unavailable, and keep the fake honest with contract tests against the real one. Use a stub only to force a rare state, and use a recording fake only when the effect is visible solely through the collaborator. For APIs another team owns, use their fake or your wrapper rather than a mock. [SWE-T46, WELC-T22, CC-T11, SWE-T12, SWE-T49, WELC-P6, SWE-T48, SWE-T13]

### Should a test check outcomes or interactions?
- **Clean Code and SWE at Google:** Assert results and state, not internal calls or ordering, so refactoring leaves tests unchanged. [CC-T15, SWE-T10, SWE-P5]
- **Legacy Code:** Recording fakes that capture outgoing calls are real tests when effects are visible only through a collaborator. [WELC-T07, WELC-P6]
- **TDD:** When you must verify that setup, the test method and teardown run in sequence, append each called method's name to a log and assert the whole string, which checks both which methods ran and their order. [TDD-T41]
- **Decide:** Check interactions only when count or order is the requirement, when the call has an outside side effect, or when no state is observable otherwise. Pair each interaction-only test with a larger test of the real outcome. Use a set rather than an ordered log when order does not matter. [SWE-T11, SWE-T50, WELC-T07, WELC-P6, TDD-T41]

### Should test code remove duplication or repeat itself for clarity?
- **TDD:** Move setup that several tests share into the setup method, and remove repeated literals and expected values right after green. [TDD-T33, TDD-T10]
- **Clean Code:** Wrap repeated setup and assertion steps in named helpers and fill fixtures with defaults. [CC-T08, CC-T07]
- **SWE at Google:** Accept some repetition when it keeps each test clearer, write expected values as literals in each test, and hide only setup the assertion does not depend on. [SWE-T45, SWE-T42, SWE-T44]
- **Decide:** Extract what the assertion does not depend on into helpers, defaults or setup. Keep the influential inputs and the expected values visible in each test. Apply TDD's removal of repeated literals to shared production code, which is where its check looks, and keep each expected value as a literal in its test. Keep setup in place when it is short enough to read. [SWE-T44, CC-T07, SWE-T42, TDD-T10, TDD-T33]

### May a test reach private state or a helper directly?
- **TDD:** Assert through public methods, but when no better design has appeared yet, check the private variable for now and note that the design needs work. [TDD-T13]
- **Clean Code:** Test private details directly only when public tests cannot reach them. [CC-T15]
- **SWE at Google:** Test only through public API, and test a helper used by one or two classes through those classes, while general libraries get direct tests. [SWE-P5, SWE-T08]
- **Legacy Code:** In legacy code, effects that no interface exposes are sensed with temporary flags or recording fakes. [WELC-P6]
- **Decide:** Go through the public interface by default. Reach inside only when no public path can observe the behavior, mark it as a design debt, and remove temporary sensing points when the refactoring finishes. A narrow helper is tested through its callers, and a general library is tested directly. [TDD-T13, CC-T15, SWE-T08, WELC-P6]

### Must the whole suite run on every change?
- **TDD and Clean Code:** Run the full suite after each small change and on every push. [TDD-T14, CC-T68]
- **SWE at Google:** Gate presubmit on fast, reliable tests and every transitively affected test, and run costly or flaky suites after submit or at release. [SWE-T24, SWE-T32, SWE-T26]
- **Legacy Code:** Keep slow tests out of the unit set, in a separate set. [WELC-T03]
- **Decide:** Gate every change on the fast, reliable tests, including every test the change transitively affects. Move a test out of the gate only when it is too slow, flaky or costly, or needs accounts presubmit cannot safely use, and then run it after submit. Keep it in presubmit when a broken change must be caught before it reaches the shared codebase. [SWE-T24, SWE-T32, SWE-T26, WELC-T03]

### May a failing test ever be skipped?
- **TDD:** Never disable a failing test to reach a passing check-in. A solo session may end on a failing test, and a known limitation can be recorded beside a test only outside shared check-ins. [TDD-T15, TDD-T48]
- **Pragmatic Programmer:** Fix a failing test or remove it on purpose, and do not skip or delete one just to go green. [PP-T73]
- **Clean Code:** A slow or broken test may be disabled with a message stating why, except an intermittent threaded test, which signals a probable threading defect. [CC-T69, CC-T60]
- **Decide:** Do not skip a test to make a shared run green. If a slow or broken test must be set aside, state the reason at the marker and link an open ticket. Do not set aside an intermittent failure in threaded code. Investigate it instead. [CC-T69, CC-T60, PP-T73, TDD-T15]

### How fast must the tests be?
- **Legacy Code:** No single unit test should take a tenth of a second. [WELC-T03]
- **Clean Code:** Build and test after a small edit should take a minute or two at most. [CC-P4]
- **TDD:** Run the suite about once a minute while coding, and keep the full suite under about ten minutes. [TDD-T14, TDD-P7]
- **Decide:** The numbers measure different scopes: one unit test, the feedback loop after an edit, and the full suite before sharing. Apply each to its own scope. The books give no deciding condition beyond that, so follow the codebase's existing limits where they exist. [WELC-T03, CC-P4, TDD-P7]

### Must every change start with a failing test?
- **TDD, Clean Code and Clean Architecture:** Write the test first for new behavior and new modules. [TDD-T01, CC-T05, CA-T03]
- **Refactoring and Legacy Code:** For existing code without tests, first write tests that pin what the code does today. [REF-T03, REF-T01]
- **Decide:** Test-first applies to new or changed behavior. Pure refactorings rely on existing tests, untested code gets characterization tests before it changes, and throwaway sketches are exempt. When the unit's design is unsettled, step back from narrow tests long enough to see it. [TDD-T01, CC-T05, TDD-T45, CC-T06]

## Review checklist

- [ ] Each behavior change in the diff comes with a test that exercises it, and the PR notes show that test failing first. [SWE-T56, TDD-T02, CC-T05]
- [ ] Every bug fix adds a test that fails without the fix. [TDD-T42, REF-T04, POSD-T20]
- [ ] Each test has one action, asserts one behavior, and its name states action and outcome without "and". [CC-T09, SWE-T39, SWE-T40]
- [ ] Test bodies contain no `if`, `for` or `while`. [SWE-T41]
- [ ] Expected values are hand-computed literals, not calls to the production code. [SWE-T42, CC-T78, TDD-T16]
- [ ] Assertions read public results or stored state, not private fields. [TDD-T13, SWE-P5]
- [ ] Interaction assertions appear only where count or order is a requirement, and each has a companion state test. [SWE-T11, SWE-T50]
- [ ] No test mocks an API owned by another team. [SWE-T48]
- [ ] Each fake has contract tests that also run against the real implementation. [SWE-T12, TDD-T39]
- [ ] Tests set only the fields their assertions depend on, and influential values are visible inline. [CC-T07, SWE-T44]
- [ ] Boundary, invalid-input and dependency-failure cases are present, and they assert the response. [REF-T06, PP-T42, SWE-T53, DDIA-T14]
- [ ] No fixed sleep appears in test code. [SWE-T55]
- [ ] The suite passes in random order, and no test reads another test's leftovers. [CC-T10, SWE-T09]
- [ ] Small tests make no real network, file or database calls, except through an in-memory filesystem, and tests carry size labels. [SWE-T06, SWE-T05]
- [ ] Rule tests start no UI, server or database and never navigate screens. [CA-P5, CA-T70]
- [ ] No production module imports test code or test fakes, and any testing API is absent from production builds. [CA-T69, WELC-T08, CA-T71]
- [ ] A pure refactoring diff edits no existing test except for forced signature changes. [SWE-T60, REF-T82]
- [ ] No skip, ignore or disable marker is added without a reason and an open ticket. [PP-T73, CC-T69, TDD-T15]
- [ ] New test files are found by standard discovery and run in CI. [SWE-T59]
- [ ] Presubmit runs only fast, reliable suites, and every suite moved out appears in post-submit. [SWE-T24, SWE-T26]
- [ ] Law-governed operations have generator-based tests that compare two expressions. [FPS-P7]

## More entries in this area

- `TDD-T38` — Assert the expected exception type: when code should throw, fail the test if nothing is thrown and catch only the named type, so an unrelated error cannot pass.
- `TDD-T43` — Count test results from runner events: when writing a test runner, increment the run count at each test start instead of storing a number.
- `TDD-T44` — Report run and failure counts with names: when designing runner output, report runs, failures and failed names, keeping assertion failures apart from other errors, unless the framework is too new for that.
- `TDD-T50` — Count setUp and test exceptions as failures: when writing a runner, guard both setup and the test method and count each exception as a failure.
