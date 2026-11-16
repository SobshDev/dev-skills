# Test-Driven Development: By Example — Kent Beck (1st edition, 2002)

## Summary
Test-driven development works in very small steps. Each step starts with a failing automated test, adds the quickest code that passes it, and then cleans up the design while the tests stay green. Short feedback loops let the programmer manage fear and make design choices with evidence. It is weaker where tests cannot judge the result, such as some security or concurrency work.

## Principles

### TDD-P1: Write a failing test before production code
Write the test first, so it specifies behavior instead of guessing at it. Add code only to pass a failing test.

- **Apply:** Write the test for new behavior and see it fail before changing production code.
- **Check:** Each production change in a diff has a test that failed first.
- **See:** TDD-T01, TDD-T02, TDD-T03
- **Source:** ch. 23, 32

### TDD-P2: Take steps small enough to correct quickly
Keep each step small enough that a new failure traces to the last change. Use larger steps only when the path is clear.

- **Apply:** Take the smallest next step, and take larger steps only when the path is clear.
- **Limits:** Routine work with a clear path can take larger steps.
- **Check:** Each commit adds one small change, and a commit on a shared branch passes the whole suite (see TDD-T15).
- **See:** TDD-T04, TDD-T05
- **Source:** ch. 1, 9, 32

### TDD-P3: Get to green quickly, then refactor separately
Quick passing code and cleanup are different jobs, so make the bar green first and restore good design separately.

- **Apply:** Make the test pass with the simplest code, then refactor as its own step, unless clean code is obvious (see TDD-T06).
- **Check:** A refactoring commit follows the quick passing commit before the next test starts.
- **See:** TDD-T06, TDD-T07
- **Source:** ch. 5, 28

### TDD-P4: Fake first, then generalize only on evidence
A constant or special case can reach green while the right logic is unclear. Generalize when a new failing test demands it, not before.

- **Apply:** Return a constant to pass the test, then generalize when a failing test requires it.
- **Check:** Constants in production code are replaced only in commits driven by a failing test.
- **See:** TDD-T08, TDD-T09
- **Source:** ch. 21, 28, 32

### TDD-P5: Treat duplication as the design signal
Repeated logic or data means two parts depend on each other, or a concept is missing. Remove it and name the concept that owns it.

- **Apply:** Remove duplicated logic or literals, and name the concept that owns them.
- **Limits:** A quick copy may wait until the work is shared (see TDD-T32).
- **Check:** No repeated expression or literal in shared production code remains in a diff ready to share.
- **See:** TDD-T10, TDD-T11
- **Source:** ch. 1, 5, 23, 32

### TDD-P6: Let test difficulty reveal design problems
A test that needs long setup, private state or the whole system is evidence about the design. Change the design rather than working around the test.

- **Apply:** When a test is hard to write, change the design, such as by adding a public behavior, unless no better design has appeared yet (see TDD-T13).
- **Limits:** A hard test may show a testing problem as well as a design problem.
- **Check:** Tests assert public behavior and build small objects directly.
- **See:** TDD-T12, TDD-T13
- **Source:** ch. 25, 29, 32

### TDD-P7: Keep the suite fast and green before sharing
Integrate working code often, and keep the full suite quick enough to run each time. A failing test may wait only while the work stays solo and resumable.

- **Apply:** Keep the full suite under about ten minutes, and integrate working code every fifteen to thirty minutes.
- **Limits:** A solo session may end on a deliberately failing test.
- **Check:** Shared-branch commits arrive fifteen to thirty minutes apart, and each one passes the suite.
- **See:** TDD-T14, TDD-T15
- **Source:** ch. 27, 32

### TDD-P8: Trust a test only after it can fail
A passing test is not evidence unless it would fail under a plausible defect.

- **Apply:** Introduce defects on purpose, and check that some test fails for each one.
- **Limits:** Passing unit tests alone do not establish security or concurrency correctness, and swapping one constant for another does not change what the program means.
- **Check:** Mutation or manual defect review shows a failing test for each changed line.
- **See:** TDD-T16, TDD-T17
- **Source:** ch. preface, 17

### TDD-P9: Defer new concepts until a test requires them
An abstraction added before a need is a guess. Keep new classes and parameters out until a failing test or a real variation demands them.

- **Apply:** Add a class, parameter or interface only when a failing test or real variation calls for it.
- **Limits:** A system-shaping design choice deserves careful reasoning before code.
- **Check:** A new pattern class appears in the diff only after tests for its variants show the need.
- **See:** TDD-T18, TDD-T19
- **Source:** ch. 12, 32
