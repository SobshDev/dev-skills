# Test-Driven Development: By Example — techniques

### TDD-T01: Write the failing test before the code
Write an automated test for the new behavior before writing any production code for it.

- **Why:** Writing each test first makes defects surface while they are cheapest to fix.
- **When:** Adding or changing any behavior in the code.
- **Not when:** Pure refactorings keep behavior, so existing tests guard them.
- **Check:** The commit history or diff shows a test added before the production change it covers.
- **Source:** ch. intro p. 21, ch. 1 p. 26, ch. 25 p. 149, ch. 32 p. 224, ch. 32 p. 227

### TDD-T02: Run the new test and see it fail
After the test compiles, run it and confirm it fails for the expected reason before writing the implementation.

- **Why:** A test that has never failed does not prove it can detect the missing behavior.
- **When:** The new test and its stubs compile.
- **Check:** The commit message or PR notes record the new test failing on the expected assertion.
- **Source:** ch. 1 p. 27

### TDD-T03: Start a new operation with a trivial test
Start a new operation with a test of its simplest variant, using trivial inputs and an expected output.

- **Why:** A simple first case settles the operation's location and inputs before the complex cases arrive.
- **When:** Adding an operation whose location and inputs are not yet settled.
- **Not when:** Familiar work, where a starter test may cover one or two operations.
- **Check:** The first test for a new operation uses an empty or trivial input and expected output.
- **Source:** ch. 26 p. 156, ch. 1 p. 26

### TDD-T04: Pick the next test that shows visible progress
Choose the next test as the smallest one that shows something new and that you can make pass.

- **Why:** Small visible increments keep each failure easy to locate and keep the work moving.
- **When:** Choosing the next item from the test list while the path to the goal is unclear.
- **Not when:** Step size depends on experience, so no single rule fits. When the path is clear, larger routine steps are sound (see TDD-P2).
- **Check:** The test list or commit history shows each test adding one small visible increment.
- **Source:** ch. preface p. 13, ch. 5 p. 45, ch. 21 p. 127, ch. 26 p. 155

### TDD-T05: Undo a failed big step and retry smaller
When a larger change breaks in a way that is slow to diagnose, undo it and redo the work in smaller steps.

- **Why:** Smaller steps shorten the path from a failure back to its cause.
- **When:** A large change breaks in a way that is slow to diagnose.
- **Not when:** The change is already small, so write a focused test for its cause instead (see TDD-T47).
- **Check:** The history shows the large change reverted, then smaller commits in its place.
- **Source:** ch. 9 p. 64, ch. 21 p. 127

### TDD-T06: Make the test pass before refactoring
Get the failing test passing with the quickest fix, and only then start refactoring the code.

- **Why:** A quick passing change gives a safe baseline, so the cleanup can be checked against it.
- **When:** A quick implementation has just made a test pass.
- **Not when:** The clean implementation is obvious and takes no longer to write.
- **Check:** Refactoring commits follow a state in which all tests pass.
- **Source:** ch. 2 p. 33, ch. 28 p. 174

### TDD-T07: Keep refactoring apart from behavior changes
Work in one mode at a time, and make each refactoring a change that keeps every previously passing test passing.

- **Why:** Mixing a behavior change with a refactoring hides which change broke which test.
- **When:** Switching between adding features and restructuring the design.
- **Not when:** The behavior is not yet covered by any test, so its change cannot be checked as a refactoring (see TDD-T45).
- **Check:** Commits separate feature changes from refactoring changes, and previously passing tests still pass.
- **Source:** ch. 31 p. 203, ch. 6 p. 50, ch. afterword p. 237

### TDD-T08: Return a constant to reach green
When the correct logic is unclear, return a constant to reach green, then replace it with computed logic only when a failing test requires it (see TDD-P4).

- **Why:** A constant gives the least code that satisfies the failing test, so the real design can wait for evidence.
- **When:** A test is red and the correct implementation is not yet clear.
- **Not when:** The correct implementation is obvious and quick to type.
- **Check:** A constant return in the diff is replaced by computed values only in commits driven by a failing test.
- **Source:** ch. 1 p. 28, ch. 2 p. 35, ch. appendix ii: fibonacci p. 233

### TDD-T09: Add a second example before generalizing
When one example fits many general forms, add a second test with different inputs before writing the general code. The book calls this triangulation.

- **Why:** A second example shows which parts of the code must vary, so the abstraction matches real need.
- **When:** You are unsure how to generalize from a single test case.
- **Not when:** The duplication is already visible, so generalize directly. Second examples can loop endlessly, so use them only when truly unsure.
- **Check:** Generalized code is backed by at least two tests with different inputs.
- **Source:** ch. 2 p. 38, ch. 28 p. 175

### TDD-T10: Remove duplicated logic right after green
Once a test passes, remove any repeated expression, literal or expected value from the code and tests before writing the next test.

- **Why:** Duplication left in place keeps two places that must change together, which makes later changes unsafe.
- **When:** Right after a test passes and the implementation repeats logic or data.
- **Not when:** Quick-copy duplication may wait until the work is shared (see TDD-T32). Near-identical code is reconciled first (see TDD-T11).
- **Check:** In the diff, no copied expression, repeated literal or expected value appears in shared production code.
- **Source:** ch. preface p. 11, ch. 1 p. 30, ch. 28 p. 174

### TDD-T11: Reconcile near-identical code before merging it
Make two similar methods or loops identical in small steps, and merge them only when every line matches.

- **Why:** Merging near-identical code early hides a real difference that a later test would expose.
- **When:** Two parts of the code differ only slightly.
- **Check:** The two versions are identical in the diff before one is removed.
- **Source:** ch. 6 p. 52, ch. 10 p. 67, ch. 31 p. 203, ch. 31 p. 204

### TDD-T12: Split objects when setup grows long
When a single assertion needs a long setup, split the large object into smaller objects that each set up quickly.

- **Why:** Long setup shows that the objects are too tangled, so smaller objects make the design easier to test and change.
- **When:** One test needs more setup code than the behavior it checks, to create the objects it asserts on.
- **Check:** A test's setup creates only the objects the assertion uses, not many large ones.
- **Source:** ch. 32 p. 216

### TDD-T13: Assert public behavior, not private state
Check results through public methods of an object, not by reading its private fields.

- **Why:** Tests on public behavior survive changes to the internal representation.
- **When:** A test would otherwise read an object's private fields or representation.
- **Not when:** No better design has appeared yet. Check the private variable for now, and note that it needs a better design later.
- **Check:** Test assertions call public methods rather than reading private fields.
- **Source:** ch. 29 p. 180

### TDD-T14: Run the tests after every small change
Run the full test suite after each small change, roughly once a minute while coding.

- **Why:** Frequent runs keep the cause of any red bar close to the change that produced it.
- **When:** Actively programming with TDD.
- **Not when:** Under very high stress, the habit can still break down.
- **Check:** The commit message or CI record shows a test run after each small change.
- **Source:** ch. 17 p. 105, ch. 25 p. 146, ch. 25 p. 147

### TDD-T15: Keep every test passing at check-in
Make sure every test passes before code goes into a shared branch, and never disable a failing test to get there.

- **Why:** Checking in a red bar breaks the shared work for everyone who integrates with it.
- **When:** Checking code into a team project.
- **Not when:** Solo sessions, where a deliberately failing test can wait until resumed.
- **Check:** The check-in or pull request shows the full suite passing, and the diff adds no commented-out or disabled test.
- **Source:** ch. 27 p. 171, ch. 27 p. 172

### TDD-T16: Assert exact expected values
Write each assertion to compare the result with one specific expected value.

- **Why:** A specific expected value detects defects that a weak condition such as non-zero would miss.
- **When:** Writing any check of an expected result.
- **Check:** Assertions compare results to specific values, and equality assertion calls list the expected value first.
- **Source:** ch. 29 p. 179

### TDD-T17: Investigate tests that pass unexpectedly
When a test you expected to fail passes, find out why before trusting it.

- **Why:** A test that passes for the wrong reason gives false confidence in code that may still be broken.
- **When:** A test you expected to fail passes.
- **Not when:** Coverage alone is not sufficient proof, so do not accept coverage as the explanation.
- **Check:** Notes or commits explain why the passing test is correct.
- **Source:** ch. 17 p. 104, ch. 17 p. 108

### TDD-T18: Add classes only when a test needs them
Introduce a new class, parameter or concept only when a failing test requires it, and pass a value in only where the behavior uses it.

- **Why:** Concepts added ahead of need are guesses that cost design effort and can turn out wrong.
- **When:** You are tempted to add a class, parameter or concept before any failing test asks for it.
- **Not when:** Current behavior requires the parameter, so add it now.
- **Check:** Each new class and parameter in the diff is required by a failing test.
- **Source:** ch. 7 p. 56, ch. 12 p. 85

### TDD-T19: Use a plain value for new concepts
Represent a new concept with a simple value, such as a string, until it needs behavior of its own.

- **Why:** A plain value answers the immediate need and keeps the concept cheap to change later.
- **When:** A concept such as currency is needed only for identity right now.
- **Not when:** The concept needs behavior of its own, so it should become an object.
- **Check:** The new concept is a plain string or number until a richer type exists in the code.
- **Source:** ch. 9 p. 61

### TDD-T20: Replace long reasoning with a runnable experiment
Make the change and run the tests when reasoning about the design would take longer than the experiment.

- **Why:** A test run answers the question directly, and it is cheaper than long reasoning about the same question.
- **When:** You spend minutes reasoning about whether two designs behave the same.
- **Not when:** No tests exist, so reasoning is the only option.
- **Check:** The test run answers the question, and the commit or notes record that run.
- **Source:** ch. 10 p. 68

### TDD-T21: Work through hard problems with runnable experiments
Learn a difficult problem in small concrete steps, and seek concrete feedback from runnable code.

- **Why:** A frightening problem shrinks when each small step gives a concrete answer.
- **When:** A problem is difficult, and its path is unclear.
- **Check:** Work on a hard change shows runnable experiments and tests, not long stretches of untested code.
- **Source:** ch. preface p. 13

### TDD-T22: Prepare tests and modules before a risky change
Build tests and modules that make the large change safe before you start that change.

- **Why:** Tests and modules that are prepared let a large change proceed without losing track of what it broke.
- **When:** Facing a large change that seems too risky to attempt.
- **Not when:** Stable parts of the system, which may keep looser tests.
- **Check:** Tests covering the code the large change will modify exist before that change begins.
- **Source:** ch. intro p. 21, ch. 17 p. 103

### TDD-T23: Write the call you wish existed first
Write the test using the operation signature you would like callers to have, then update it when a better shape appears.

- **Why:** The caller's view of the interface comes first, so the design fits how the code will be used.
- **When:** Designing how callers will use a new operation.
- **Check:** Signature changes in a diff come with the test changes that use the new signature.
- **Source:** ch. 1 p. 26, ch. 2 p. 34, ch. 28 p. 177

### TDD-T24: Count down compile errors one at a time
When a new test or a changed type breaks many declarations, remove compile errors one at a time with the least code, starting from the interface.

- **Why:** Tracking the remaining errors shows progress and keeps each stub as small as possible.
- **When:** A new test refers to classes, constructors, or methods that do not exist yet.
- **Check:** Each stub added in the diff matches one compile error in the build output.
- **Source:** ch. 1 p. 27, ch. 31 p. 212, ch. 15 p. 95

### TDD-T25: Keep planned tests on a visible list
Write planned tests and open design questions on a list, and mark each item as started or finished.

- **Why:** A list keeps future work out of the current change while still recording it.
- **When:** The work has several known requirements or open design questions.
- **Check:** The repository or task tracker lists each planned test, with finished items marked.
- **Source:** ch. 1 p. 26, ch. 25 p. 148

### TDD-T26: Park side ideas on the list
Add each newly noticed test or design concern to the list, and return to the current task.

- **Why:** Acting on a tangent during a planned change mixes unrelated work and blurs the cause of failures.
- **When:** A side idea appears during a planned task, and it is not a reported defect (see TDD-T42).
- **Not when:** The tangent is a breakthrough that the current work depends on.
- **Check:** The new item appears in the list, and the current change contains no unrelated fix.
- **Source:** ch. 1 p. 26, ch. 22 p. 133, ch. 26 p. 159

### TDD-T27: Keep value objects immutable and return new ones
Make value objects (objects whose meaning is their value, such as money) unchangeable, and return a new object from each operation.

- **Why:** An unchangeable value cannot be altered through another reference, so sharing it is safe.
- **When:** An operation would change a value that other code may still hold, or objects are shared widely.
- **Not when:** Allocation costs prove slow with realistic data, so measure before optimizing.
- **Check:** Value classes have no setters, and their fields are assigned only in constructors.
- **Source:** ch. 2 p. 34, ch. 3 p. 37, ch. 30 p. 189

### TDD-T28: Compare value objects by their values
Implement equality by comparing every value field, so that equal values can be used interchangeably.

- **Why:** Value equality lets equal amounts stand in for one another in lookups and assertions.
- **When:** Defining a value object that will be compared or asserted on.
- **Check:** The equals method compares every value field of the class.
- **Source:** ch. 3 p. 37

### TDD-T29: Keep hash codes consistent with equality
Override the hash code (hashCode in Java) consistently with equals for any value object used as a map key or set member.

- **Why:** Hashing that disagrees with equality makes equal keys fail to match in lookups.
- **When:** A class that overrides equals might serve as a map key or set member.
- **Not when:** The class is not yet used as a hash key, so defer it.
- **Check:** Each class in the diff used as a map key or set member overrides hash code and equals together.
- **Source:** ch. 3 p. 38, ch. 14 p. 91, ch. 30 p. 191

### TDD-T30: Check library assumptions with learning tests
Write a small test that calls a new or uncertain library method directly before application code depends on it.

- **Why:** A test on the library shows its real behavior, so later upgrades reveal changed assumptions.
- **When:** Using a library method for the first time, or unsure how it compares values.
- **Not when:** The external code is trusted and its behavior does not matter to your code.
- **Check:** The suite contains a learning test that confirms the library behavior the code relies on.
- **Source:** ch. 14 p. 91, ch. 26 p. 158, ch. 26 p. 159, ch. 32 p. 216

### TDD-T31: Record surprising behavior as a named test
Write a test whose name states a surprising rule you find, including unusual behavior of external code you depend on.

- **Why:** A named test keeps an unexpected rule visible to readers and to later refactoring.
- **When:** Code shows unexpected behavior that you did not design for.
- **Check:** A test name states the surprising rule, for example the book's own case that identical currencies convert at rate one.
- **Source:** ch. 14 p. 92, ch. 32 p. 216

### TDD-T32: Copy a test, then remove duplication
Copy an existing test and its code to reach green on a new case, then remove the duplication in the commits that follow.

- **Why:** Copying keeps progress quick, and merging afterward reveals the shared shape.
- **When:** A new variant of a working class looks too big to write in one leap.
- **Not when:** Some teams wait for three or four uses before merging, and the author accepts undoing early refactorings.
- **Check:** The copied code is merged or removed in the commits that follow the green bar, and before the work is shared.
- **Source:** ch. 5 p. 45, ch. 20 p. 124

### TDD-T33: Move repeated test setup into setUp
Turn the objects that several tests build the same way into instance fields created in setUp, the method that runs before each test.

- **Why:** One shared setup keeps every test starting from the same known state.
- **When:** Several test methods build the same objects.
- **Not when:** Each test's setup is short enough to read in place, or readers need the allocation visible in each test.
- **Check:** Objects shared by several tests are created in setUp rather than in each test method.
- **Source:** ch. 17 p. 106, ch. 29 p. 180, ch. 23 p. 138

### TDD-T34: Give each test fresh, independent state
Create the objects each test needs in setUp, and make sure no test changes shared state that another test reads.

- **Why:** A test that depends on another test's leftovers fails for reasons unrelated to its own behavior.
- **When:** Several tests run together in one suite.
- **Not when:** Object creation is too slow and sharing matters more. Then make sure one test's failure cannot change another test's result.
- **Check:** No test reads state left behind by another test, and no test changes shared mutable state another test reads.
- **Source:** ch. 19 p. 120, ch. 19 p. 121, ch. 25 p. 147

### TDD-T35: Arrange, act and assert in every test
Structure each test as setup, one stimulus call, then assertions.

- **Why:** A fixed three-part shape makes each test's cause and expected effect easy to read.
- **When:** Writing any new test method.
- **Check:** Each test method shows setup, one stimulus call and its assertions, in that order.
- **Source:** ch. 19 p. 119

### TDD-T36: Release external resources in tearDown
Close or release every external resource that setUp allocates, inside tearDown, the method that runs after each test, rather than in each test.

- **Why:** A single release point prevents leaked files or connections when a test fails midway.
- **When:** A test allocates files, connections, or similar resources in setUp.
- **Not when:** setUp itself fails, because tearDown is not called after a failed setUp.
- **Check:** Every resource opened in setUp has a matching release in tearDown.
- **Source:** ch. 20 p. 123, ch. 29 p. 183

### TDD-T37: Group test classes by fixture
Start a new test class when a set of tests needs a different fixture, the starting objects they use, instead of one class per model class.

- **Why:** Grouping by fixture keeps each class's setup shared and matches how the tests are written.
- **When:** A test needs a different fixture from the existing ones.
- **Check:** Each test class's setUp creates one fixture that its test methods use.
- **Source:** ch. 29 p. 182

### TDD-T38: Assert the expected exception type
Call the code that should throw, fail the test if nothing is thrown, and catch only the named exception type.

- **Why:** Catching a named type stops an unrelated error from passing as the expected failure.
- **When:** A test expects the code to throw a specific error.
- **Check:** The test calls fail after the operation and catches a named exception type.
- **Source:** ch. 27 p. 170, ch. 29 p. 185

### TDD-T39: Replace costly resources with fakes, then test both
Use a fake object with fixed answers in place of an expensive or unreliable resource, and run the same tests against the real object once it exists.

- **Why:** A fake keeps tests fast and reliable, and the real-object run confirms the fake behaves like it.
- **When:** A test depends on a database, a remote server, or a similar resource.
- **Not when:** The fake may drift from the real resource's behavior, so keep the real-object run.
- **Check:** Tests construct a fake in place of the service client, and the same cases run against the real class.
- **Source:** ch. 27 p. 166, ch. 27 p. 167

### TDD-T40: Pass expensive resources in as parameters
Give objects their shared resources through constructor or method parameters, not through global variables or singletons.

- **Why:** Parameters let tests substitute a resource without changing global state that other tests read.
- **When:** Tests need to substitute a resource that the code uses.
- **Check:** No global variable or singleton holds a resource that the tests must replace.
- **Source:** ch. 27 p. 166, ch. 30 p. 201, ch. 14 p. 89

### TDD-T41: Log called methods to assert their order
Append each called method's name to a log string, then assert the complete string against the expected sequence.

- **Why:** One string checks both which methods ran and the order in which they ran.
- **When:** You must verify that setup, the test method, and teardown run in sequence.
- **Not when:** Order does not matter, so compare a set of strings instead.
- **Check:** A test asserts one log string that lists the calls in their expected order.
- **Source:** ch. 20 p. 123, ch. 27 p. 168

### TDD-T42: Write a failing test for each reported defect
For each reported defect, first write the smallest test that fails because of it before repairing, and add a regression test that runs the whole application.

- **Why:** The failing test proves the defect exists and guards against its return after the repair.
- **When:** A defect is reported against working code.
- **Check:** The fix adds tests that fail without it, including one at application level.
- **Source:** ch. 26 p. 159, ch. 26 p. 160

### TDD-T43: Count test results from runner events
Count tests by incrementing a counter at each test start, instead of storing a fixed number.

- **Why:** Counting events reports what actually ran, rather than a fixed number that can drift.
- **When:** You are writing a test runner that reports how many tests ran.
- **Check:** The run count is incremented at each test start, not set to a constant.
- **Source:** ch. 21 p. 128

### TDD-T44: Report run and failure counts with names
Report the number of tests run, the number that failed and the failed tests' names, keeping assertion failures apart from other errors.

- **Why:** Names make a failure traceable in a batch run, and counts show whether the run covered what was intended.
- **When:** Designing the output of the test runner.
- **Not when:** The framework is new, and reporting tests that were never counted is too ambitious.
- **Check:** Runner output includes a run count, a failure count, and each failed test's name.
- **Source:** ch. 21 p. 127, ch. 24 p. 141

### TDD-T45: Write missing tests before refactoring untested code
Before refactoring code that has little or no test coverage, write tests for its existing behavior.

- **Why:** Existing behavior is protected only once tests cover it, so a refactoring cannot be checked without them.
- **When:** Refactoring code that lacks adequate tests.
- **Check:** Tests covering the refactored behavior appear in the diff before the refactoring commit.
- **Source:** ch. 6 p. 51

### TDD-T46: Give each assertion a failure message
Give each assertion a message that explains the failure, so that a batch run shows the cause.

- **Why:** In a batch run no debugger is open, so the message is the only record of the cause.
- **When:** Writing assertions in tests that run in batch builds.
- **Not when:** The team finds, after trying both ways, that messages add no value.
- **Check:** Assertion calls include a message argument describing the expected condition.
- **Source:** ch. 29 p. 180

### TDD-T47: Test the cause of an unexplained failure
When a change breaks tests in a way existing tests do not explain, write a focused test for its cause before you retry the change.

- **Why:** A focused test isolates the one cause, so the retry is checked against it.
- **When:** A refactoring or model change breaks tests in a way you did not expect.
- **Not when:** The breaking change is a large step, so undo it and redo it in smaller steps first (see TDD-T05).
- **Check:** A new test in the diff fails only on the specific cause, and the retry follows it.
- **Source:** ch. 10 p. 69, ch. 14 p. 93

### TDD-T48: Record known limitations beside unpassable tests
When a test cannot pass yet because of a known gap, record the limitation beside it as known or future work.

- **Why:** A recorded limitation keeps a real gap visible instead of hiding it.
- **When:** A test you cannot make pass now reflects a real gap.
- **Not when:** The check-in is shared with a team, where every test must pass (see TDD-T15).
- **Check:** The suite or tracker notes the known limitation next to the test.
- **Source:** ch. 17 p. 104

### TDD-T49: Remove hidden coupling behind fragile tests
When an edit in one part breaks a test in another, remove the hidden dependency or merge the two parts.

- **Why:** A hidden dependency makes a test fail for changes that have nothing to do with its behavior.
- **When:** A test fails after an edit confined to a different part of the application.
- **Check:** A failing test in one module follows from an edit in a different module that does not call it.
- **Source:** ch. 32 p. 217

### TDD-T50: Count setUp and test exceptions as failures
Catch exceptions raised by both setUp and the test method, and count each one as a failed test.

- **Why:** Counting an exception as a failure keeps a broken test from passing silently.
- **When:** You are writing a test runner that calls setUp and test methods.
- **Check:** The try block that guards the test method also covers the setUp call, and its handler increments the failure count.
- **Source:** ch. 22 p. 132
