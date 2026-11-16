# Software Engineering at Google — techniques


### SWE-T01: Upgrade dependencies in small regular increments
Upgrade libraries and runtimes in small, regular steps, and script any upgrade step you repeat.

- **Why:** Accumulated change makes each later upgrade larger and riskier, and a never-upgraded codebase costs most to move first.
- **When:** Scheduling dependency or runtime upgrades for a long-lived project.
- **Not when:** The upgrade costs more than the value it gives over the code's lifespan.
- **Check:** Dependency update commits are frequent, and each one touches a small set of files.
- **Source:** ch. 1


### SWE-T02: Compare options by every cost they impose
Count financial, personnel, opportunity and societal costs, plus lost focus, and allow for status quo bias, before choosing.

- **Why:** Leaving out hidden costs makes the apparently cheaper option look better than it is.
- **When:** Comparing two engineering options, such as a build change or a new service.
- **Check:** A decision record lists the costs of each option, not only the cost of the chosen one.
- **Source:** ch. 1


### SWE-T03: Automate repeated mechanical edits with tooling
Generate a large mechanical change with a tool, using syntax-aware transforms for big edits and text tools for small ones, and split it into independent shards.

- **Why:** Beyond a few hundred edits, learning a tool costs less than making every edit by hand.
- **When:** A repeated edit touches hundreds of files, or fewer when the maintainers are experienced with the tools.
- **Check:** The change comes from a recorded tool input, and rejected generated changes are regenerated, not hand-patched.
- **Source:** ch. 22


### SWE-T04: Remove code that delivers no current value
Delete dead or obsolete code when you find it, because each unused line still adds upkeep.

- **Why:** Code is a maintenance liability, so removing unused code lowers the cost of later changes.
- **When:** Reading code that no caller reaches or that a replacement has superseded.
- **Not when:** The code still delivers more value than its upkeep costs. If its purpose is unclear, learn why first (SWE-T62).
- **Check:** The diff deletes unreachable code, and a search finds no remaining references.
- **Source:** ch. 9, 15


### SWE-T05: Label every test with its size
Mark each test small, medium or large by the resources it uses, separately from its scope.

- **Why:** Size tells the test infrastructure how isolated and how costly a test is.
- **When:** Adding a new test or reviewing a test suite that has no size labels.
- **Check:** Each test declares a size matching its resources, and the runner enforces the limits.
- **Source:** ch. 11


### SWE-T06: Keep small tests in one process
Run small tests in one process, replacing slow databases, networks and disks with in-process doubles.

- **Why:** Small tests stay fast and deterministic when they avoid blocking I/O and sleeps.
- **When:** Writing a unit test with a slow or nondeterministic out-of-process database, network or disk (SWE-T46).
- **Not when:** The file access uses a hermetic, in-memory filesystem substitute.
- **Check:** A small test has no sleeps, no real file or network calls, and no live-service imports, except an in-memory filesystem.
- **Source:** ch. 11


### SWE-T07: Treat only outside-facing interfaces as public API
Count as public API only what outside teams may use without asking owners, and document its guarantees.

- **Why:** Tests and callers that rely on internals block changes the owners need to make.
- **When:** Deciding what a test should exercise, or what a change may safely alter.
- **Check:** Public APIs are usable by other teams without owner approval, and their docs list the guarantees.
- **Source:** ch. 1, 12


### SWE-T08: Test a narrow helper through its callers
Test a helper used by only one or two classes through those classes, and general libraries directly.

- **Why:** Testing a narrow helper alone duplicates coverage and ties the test to an internal detail.
- **When:** Writing tests for a helper class that serves only a few callers.
- **Check:** A helper used by one or two classes has no separate test, and its callers cover its behavior.
- **Source:** ch. 12


### SWE-T09: Make each test independent of shared state
Give each test its own setup and teardown, and control the clock, thread scheduling and network latency.

- **Why:** Tests that share data or depend on order fail intermittently and hide real defects.
- **When:** Writing or reviewing a test that touches global state, a shared database or timing.
- **Check:** Each test builds its own fixtures, and the suite passes when run in a random order.
- **Source:** ch. 11


### SWE-T10: Assert on returned values and resulting state
Verify outcomes by checking returned values or the state the system left behind, not the calls it made.

- **Why:** State checks survive changes to the internal call sequence when behavior stays the same.
- **When:** Writing a test for a method that returns a value or changes stored state.
- **Not when:** The call itself is the behavior. Then an interaction check is needed too (see SWE-T11).
- **Check:** Assertions compare returned values or stored data, not only mock call records.
- **Source:** ch. 13


### SWE-T11: Verify call counts only when they matter
Check call counts or call order only when that count is the behavior, such as a cache that must reduce reads.
- **Why:** Verifying every call couples tests to internals that the behavior does not depend on.
- **When:** A requirement says a dependency is called a specific number of times or in a specific order.
- **Check:** Interaction assertions appear only where count or order is a requirement, or calls have outside side effects.
- **Source:** ch. 13


### SWE-T12: Use a fake that matches the real contract
Use a lightweight working implementation when the real one cannot run in a test, and match its outputs and state changes except where the contract leaves details open.
- **Why:** A fake that follows the contract keeps tests meaningful, while a guessing stub can silently drift.
- **When:** A real dependency is too slow, flaky or unavailable for a test.
- **Not when:** Real-implementation contract tests are too slow, so only the fake's owners run them.
- **Check:** Each fake has tests that run against the real contract, and it raises errors for unsupported paths.
- **Source:** ch. 13


### SWE-T13: Let the API owner write its fake
Ask the owners of an API to provide and maintain its fake before writing one yourself.
- **Why:** The owners know the contract best, so their fake is less likely to drift.
- **When:** A test needs a fake for an API owned by another team.
- **Not when:** The owners decline, in which case wrap the API in one class and fake that wrapper.
- **Check:** The fake lives with the owning team's code and is updated alongside behavior changes.
- **Source:** ch. 13


### SWE-T14: Keep each change focused on one concern
Limit each change to one issue and its tests, about 200 changed lines or fewer, and keep it atomic for safe rollback.
- **Why:** A focused change is easier to review and can be rolled back without undoing unrelated work.
- **When:** Preparing a hand-written change for review, not a generated one (SWE-T03).
- **Not when:** A large feature cannot be split well. Then flag it, or branch if flags add too much complexity (see SWE-P6).
- **Check:** The diff addresses one indicated problem, and each file change serves that problem.
- **Source:** ch. 9


### SWE-T15: Run checks at commit time
Run the project's listed checks, such as formatting, analysis, coverage and tests, before a change is sent for review or lands.
- **Why:** Checks at commit time catch problems before they reach shared trunk.
- **When:** Setting up the workflow that gates a change before it is committed to trunk.
- **Not when:** Slow or unstable suites go post-submit (SWE-T24).
- **Check:** Commit hooks or presubmit jobs run the listed checks, and the project's contributing doc names them.
- **Source:** ch. 9, 16


### SWE-T16: Block commits on presubmit analysis findings
Add presubmit checks that stop a change from being committed while analysis findings in a blocking category remain.
- **Why:** A blocking gate keeps known problem categories from reaching the shared codebase.
- **When:** A category of analyzer findings is reliable enough to treat as an error.
- **Not when:** Violations of a new check still exist. Clean them up before enabling it.
- **Check:** The presubmit configuration names blocking categories and fails on their findings, and compiler checks never warn.
- **Source:** ch. 19, 20


### SWE-T17: Analyze only the files a change touches
Run analyzers on the lines a pending change modifies, and warn mainly on problems the change introduces.
- **Why:** Reviewing only new problems keeps analyzer output actionable instead of burying it in old issues.
- **When:** Configuring an analyzer to run during review of a change.
- **Not when:** Important existing issues, such as security problems, are worth highlighting even in untouched code.
- **Check:** Analyzer output in a review mainly refers to lines changed by that review.
- **Source:** ch. 20


### SWE-T18: Start each new project with owners and CI
Add an owners file that names a primary and a backup owner, and set up continuous integration, when a project is created.
- **Why:** Owners and CI make the project's responsibility and verification explicit from its first commit.
- **When:** Creating a long-lived repository, service or library (SWE-P1).
- **Check:** A new project's first commit includes an owners file naming two owners and a CI configuration.
- **Source:** ch. 2, 6, 9


### SWE-T19: Change feature flags without a binary release
Update flag values through dynamic configuration, so a problem can be reversed without shipping a new binary.
- **Why:** Reversing a flag is faster and safer than rolling back a release that must succeed first.
- **When:** A feature guarded by a flag shows a problem in production.
- **Not when:** Static settings that never change still belong in version control with the code.
- **Check:** Flag values live in dynamic configuration, and changing one needs no code deployment.
- **Source:** ch. 24


### SWE-T20: Roll out changes to growing user percentages
Release a change to slowly increasing user percentages, and advance a stage only when guardrail metrics (measures that must not worsen) show no harm.
- **Why:** Limited exposure keeps a bad change small while its effects are still unknown.
- **When:** Shipping a risky change to a large user base.
- **Not when:** Products with too small a user base to reach statistically significant results.
- **Check:** The rollout configuration defines percentage stages, and each stage reads its guardrail metrics first.
- **Source:** ch. 24


### SWE-T21: Release in small, frequent batches
Ship small batches on a short, regular cadence.
- **Why:** Smaller batches of change tend to have fewer defects and are faster to diagnose.
- **When:** Planning the release cadence for a product that deploys frequently.
- **Not when:** Client apps whose users dislike frequent updates and pay data costs for each one.
- **Check:** Release tags or deploy records show short intervals between releases of small size.
- **Source:** ch. 24


### SWE-T22: Cut release candidates from validated changes only
Assemble release candidates from the latest change that passed the continuous build, and build releases only from validated changes.
- **Why:** Releasing unverified head can ship a change that no test ever ran against.
- **When:** Preparing a release candidate from a branch or trunk.
- **Not when:** An emergency push may cut from true head and run a minimal test set.
- **Check:** The release pipeline records the commit that passed the build, and a cherry-picked fix is retested before shipping.
- **Source:** ch. 11, 23


### SWE-T23: Scope broad refactorings to trunk, not pending work
Apply a broad rename or refactoring to trunk, so it does not chase every developer's unsubmitted changes.
- **Why:** Scoping to trunk keeps a sweeping change from creating a conflict backlog for everyone.
- **When:** Planning a codebase-wide rename or restructuring.
- **Check:** The refactoring change is generated against trunk and not applied to pending workspaces.
- **Source:** ch. 16


### SWE-T24: Keep presubmit limited to fast reliable tests
Run only fast and reliable tests before a change is submitted, and move slower or less stable suites to post-submit.
- **Why:** Slow or unstable presubmit tests delay every engineer and train people to ignore failures.
- **When:** Choosing which tests gate a change at presubmit.
- **Not when:** Post-submit can absorb longer or less stable runs when it handles them properly.
- **Check:** Presubmit lists only fast suites, every suite moved out runs post-submit, and no quality check is dropped for speed.
- **Source:** ch. 7, 23


### SWE-T25: Make larger tests hermetic before presubmit
Make larger-scoped tests hermetic and independent of the user who runs them before they gate changes at presubmit.
- **Why:** Hermetic tests are less unstable, and anyone can reproduce their results.
- **When:** Moving a larger test into presubmit only when fast (SWE-T24).
- **Not when:** Hermetic setup is too costly, though teams then often mix in live backends.
- **Check:** The test declares its dependencies and produces the same result under different users.
- **Source:** ch. 23


### SWE-T26: Run costly tests after submission and at release
Run end-to-end, flaky or resource-heavy tests in a post-submit or release job when they add too much friction to presubmit.
- **Why:** Post-submit runs keep those tests from blocking every change while still catching their failures.
- **When:** A test is too slow, flaky or costly to gate each change, or needs accounts presubmit cannot safely use.
- **Not when:** A broken change must be caught before it reaches the shared codebase.
- **Check:** The test appears in a post-submit or release pipeline and not in the presubmit list.
- **Source:** ch. 23, 14


### SWE-T27: Split a failing batch to find the culprit
When a batch of changes fails, rerun the tests on each change alone, or use binary search over the batch, to find the cause.
- **Why:** Isolating the failing change turns a batch failure into one specific, fixable change.
- **When:** A batch of changes fails its tests and the cause is unclear.
- **Not when:** The changes are broad, behavior-changing, or likely to interact with one another.
- **Check:** The build log records which individual change failed in isolation.
- **Source:** ch. 23, 22


### SWE-T28: Start removal only after a replacement exists
Begin removing an old system only once a replacement provides the same or better functionality, and review each migrated use against it.
- **Why:** Removing a system without a replacement strands its users with no working path.
- **When:** Planning the removal of an old library, service or API.
- **Check:** The removal change follows a commit or release that introduces the replacement.
- **Source:** ch. 15


### SWE-T29: Migrate callers with large-scale change tooling
Find every code-level dependent on a deprecated system with static analysis, and migrate them with tooling that generates reviewable updates.
- **Why:** Static analysis usually finds every code-level dependent, and tooling makes the migration consistent.
- **When:** Moving callers off a deprecated system across a large codebase.
- **Check:** A static search and production logging for the deprecated symbol both find no remaining callers before it is removed.
- **Source:** ch. 15


### SWE-T30: Flag new uses of deprecated symbols at review
Flag a new use of a deprecated symbol during review and suggest its replacement. After a compulsory deprecation, make the check block it.
- **Why:** Without a check at review, new code reintroduces the system that migration is removing.
- **When:** A symbol or system has been deprecated but not yet removed.
- **Check:** A presubmit or review check names the deprecated symbol and points to its replacement.
- **Source:** ch. 15, 22


### SWE-T31: Roll back the culprit before fixing forward
When a change is identified as the cause of a failure, roll it back first to restore a known good state.
- **Why:** A rollback quickly restores known behavior while the fix is still being worked out.
- **When:** A recent change is confirmed as the cause of a production or test failure.
- **Not when:** The rollback does not apply cleanly to mainline, so the fix goes forward, though that is riskier.
- **Check:** Reverting the culprit applies cleanly to the current mainline.
- **Source:** ch. 23


### SWE-T32: Run every test transitively affected by a change
Select tests from the build dependency graph, and run every test transitively affected by a change to shared code.
- **Why:** Changes often break distant dependents, so a test set limited to the touched project misses real breakage.
- **When:** Choosing which tests to run before submitting a change to a shared library.
- **Not when:** Only one project's own code changed, and that project's tests gate it. Slow affected tests may run post-submit (SWE-T24).
- **Check:** The selected test set covers targets that depend on the changed files.
- **Source:** ch. 22, 23


### SWE-T33: Review documentation changes like code
Send documentation changes through code review, update docs in the same change as behavior, and file doc errors in the same tracker.
- **Why:** Review keeps documentation accurate in the same way it keeps code accurate.
- **When:** Changing a document that describes a shipped behavior.
- **Check:** Doc edits appear in code review and link to a tracked issue when fixing a reported error.
- **Source:** ch. 10


### SWE-T34: Write reference docs as comments beside declarations
Keep reference documentation as comments beside each declaration, in the header for C++, and generate reference pages from those comments.
- **Why:** Comments next to the declaration stay close to the code they describe and change with it.
- **When:** Documenting a public API in source code.
- **Check:** Public declarations carry doc comments, and generated reference output reads from the same comments.
- **Source:** ch. 10


### SWE-T35: Name each option's trade-offs explicitly
Name each option's trade-offs, quantify them with measurements where possible, and explain them to everyone affected.
- **Why:** Stating trade-offs makes the choice visible and lets others challenge it.
- **When:** Presenting a design or technical choice to a team.
- **Check:** A design document lists the trade-offs of each option, not only the chosen one.
- **Source:** ch. 6


### SWE-T36: Ask why before judging an approach wrong
Ask the author why before deciding an approach is wrong, and suggest an alternative only when it is a real improvement.
- **Why:** The author may have a reason the reviewer cannot see from the diff alone.
- **When:** A reviewer finds an approach that differs from what they would have written.
- **Not when:** The author's approach is deficient, so a better alternative is warranted.
- **Check:** Review comments on an unusual approach ask a question before proposing a replacement.
- **Source:** ch. 9


### SWE-T37: Record why non-obvious code exists
Explain non-obvious choices in comments, and update those comments in the same change when logic changes.
- **Why:** Readers see what the code does, but only the comment explains why.
- **When:** Writing code whose correct form is not obvious from reading it.
- **Check:** Non-obvious branches, workarounds or constants carry a comment that gives their reason.
- **Source:** ch. 3, 8, 10


### SWE-T38: Structure each test as given, when, then
Split each test into setup, one action, and the expected result, so the three parts stay distinct.
- **Why:** Separating the parts lets a reader find the input, action and expectation without tracing the test.
- **When:** Writing a test that sets up state, calls the system, and checks an outcome.
- **Not when:** Trivial tests can use whitespace instead of comments, or a multistep process needs alternating when and then blocks.
- **Check:** A test body shows one setup block, one action and one expectation, in that order, unless it is multistep.
- **Source:** ch. 12


### SWE-T39: Test one behavior per test
Limit each test to a single behavior, with one action and one block of expected results.
- **Why:** A failing single-behavior test points directly at the broken behavior.
- **When:** A test would otherwise assert several outcomes of one method.
- **Check:** Each test has one action and asserts outcomes of that single behavior.
- **Source:** ch. 12, 11


### SWE-T40: Name each test after its action and outcome
Name each test for the action taken and the outcome it expects, and split any name needing the word "and".
- **Why:** A name stating action and outcome tells the reader what broke without opening the body.
- **When:** Naming a new test or renaming an existing one.
- **Check:** Test names state an action and an expected outcome, and none joins two behaviors with "and".
- **Source:** ch. 12


### SWE-T41: Keep test bodies free of logic
Write tests as straight-line code, without loops, conditionals or computed expected values.
- **Why:** A test without logic is obvious on inspection and cannot hide a bug in its own control flow.
- **When:** Tempted to add a loop, conditional or clever computation to a test.
- **Check:** Test bodies contain no if, for or while statements.
- **Source:** ch. 12, 11


### SWE-T42: Write expected values out as literals
Write expected values in the test as literals instead of assembling them from variables or concatenation.
- **Why:** A literal expectation is readable on its own, and a computed one can match a bug.
- **When:** Asserting on a value that a test would otherwise build with helper variables.
- **Check:** Assertions compare literal values in the test body, and each test holds its own assertions, not a shared validation call.
- **Source:** ch. 12


### SWE-T43: Make failure messages state expected and actual values
Write assertion failure messages that name the expected outcome, the actual outcome and the relevant inputs.
- **Why:** A failure that names both values can be triaged without rerunning the test under a debugger.
- **When:** Writing an assertion or a custom check whose failure must explain itself.
- **Not when:** Languages without such helpers must put the key details into the message by hand.
- **Check:** Failure output includes the expected and actual values, not only a boolean.
- **Source:** ch. 12


### SWE-T44: Hide setup the assertion does not depend on
Move construction details the assertion does not depend on into helpers, keeping influential inputs visible.
- **Why:** Hidden incidental setup keeps the test short while the influential inputs stay readable.
- **When:** A test needs many objects built only to satisfy a constructor.
- **Not when:** Setup must not hide values that individual tests depend on.
- **Check:** Helper calls build incidental objects, and the influential values appear inline in the test.
- **Source:** ch. 12


### SWE-T45: Accept some duplication when tests stay clear
Keep test code descriptive and somewhat repetitive when it makes each test clearer than a shared abstraction would.
- **Why:** Tests are read in isolation, so clarity of each test matters more than removing repetition.
- **When:** Shared helper code would hide what a test asserts.
- **Not when:** Helpers still help when they hide details the behavior under test does not depend on.
- **Check:** Each test states its own expectations, even when the arrange steps look alike.
- **Source:** ch. 12


### SWE-T46: Use real objects when fast and deterministic
Prefer the production implementation of a dependency in tests whenever it is fast and deterministic.
- **Why:** A real implementation tests real behavior, while a double tests only what the double was told to do.
- **When:** A dependency is a plain, fast component that the test can construct directly.
- **Not when:** Real objects that are slow or nondeterministic should be replaced.
- **Check:** Tests construct production classes directly where no slow or random dependency is involved.
- **Source:** ch. 12, 13


### SWE-T47: Keep real code until it becomes too slow
Keep the real implementation until its cost forces a switch, then move only those tests to a double.
- **Why:** Staying with the real code keeps tests honest for as long as their cost is acceptable.
- **When:** A real implementation begins to make the suite noticeably slow.
- **Not when:** A real dependency's failure reveals a production bug, so keep the real code and fix the bug.
- **Check:** Doubles appear only where the real code is too slow, flaky or unavailable, or a stub forces a rare state.
- **Source:** ch. 13


### SWE-T48: Avoid mocking APIs owners may change
Do not mock an API whose owners may change it, and do not replace every collaborator with a double.
- **Why:** A mock of a changing API keeps passing while real behavior moves away from it.
- **When:** Writing a test that would stub a library or service owned by another team.
- **Check:** Test code stubs only APIs owned by the same team, or uses the real owner's fake.
- **Source:** ch. 13


### SWE-T49: Stub only to force a specific return
Use a stub only to return a value or error that puts the system into a state the test needs.
- **Why:** A stub that forces one state keeps the test focused on what that state should cause.
- **When:** A test needs an error path that the real dependency rarely produces.
- **Not when:** The system relies on the real contract, or the test must read back data it saved (use a fake, SWE-T12).
- **Check:** Each stub returns a value the scenario needs, and a test stubs only the few functions its assertions depend on.
- **Source:** ch. 13


### SWE-T50: Pair interaction checks with a larger state test
Back a unit test that relies on interaction checks with a larger-scope test that checks the real resulting state.
- **Why:** Interaction checks confirm that a call happened but not that the behavior is correct.
- **When:** A unit test verifies calls to a double and nothing else.
- **Check:** Each interaction-only unit test has a companion test that asserts the real outcome.
- **Source:** ch. 13


### SWE-T51: Use integration tests for component contracts
Write integration tests for the interactions between a few components, especially where different teams own them.
- **Why:** Contracts between owners are where unit tests stop seeing failures.
- **When:** Two components owned by different teams exchange data or calls.
- **Check:** An integration test runs both components together and asserts on the contract they share.
- **Source:** ch. 11


### SWE-T52: Use end-to-end tests for emergent behavior
Write large-scope tests for behavior that appears only when several parts of the system work together.
- **Why:** Emergent behavior cannot be verified by testing each part alone.
- **When:** A behavior depends on several services or components interacting in real conditions.
- **Check:** An end-to-end test drives the system through its public entry point and asserts the combined outcome.
- **Source:** ch. 11, 14


### SWE-T53: Inject failures into tests on purpose
Write tests that simulate errors and latency, using exceptions at unit level and RPC faults at integration level.
- **Why:** Failure paths are rarely exercised by normal inputs and are where defects often hide.
- **When:** Code handles errors, timeouts or retries from a dependency.
- **Check:** Tests cover at least one failing call per dependency that can fail, and internal timeouts surface as failures.
- **Source:** ch. 11, 14


### SWE-T54: Use coverage to find untested code
Use code coverage to locate untested code, remembering that it shows lines ran, not that results were checked.
- **Why:** Coverage is a search aid for gaps, not evidence that behavior is verified.
- **When:** Reviewing a suite for areas that no test exercises.
- **Check:** Coverage reports are used to find gaps, and new tests assert on results rather than only execution.
- **Source:** ch. 11


### SWE-T55: Poll for state instead of sleeping
Wait for asynchronous work by polling for the expected state with a timeout, or by subscribing, not by sleeping.

- **Why:** Fixed sleeps are either too long and slow the suite or too short and flaky.
- **When:** A test must wait for a background task or an external event.
- **Check:** Test code contains no fixed sleep calls and uses a bounded poll or an event wait.
- **Source:** ch. 11, 14

### SWE-T56: Block changes that add behavior without tests
Reject a change that adds or modifies behavior unless it includes tests for that behavior.
- **Why:** Untested behavior is the main way a suite stops catching regressions.
- **When:** Reviewing a change that alters logic, error handling or public behavior.
- **Check:** A behavior change in the diff is accompanied by test changes that exercise it.
- **Source:** ch. 11


### SWE-T57: Add a regression test for each defect found
Add an automated test whenever a defect is found by hand, through exploratory testing or security testing.
- **Why:** The regression test keeps a defect from returning and runs far more often than manual checks.
- **When:** A defect is reported or found while testing the product manually.
- **Check:** The bug-fix diff includes a test that exercises the reported failure.
- **Source:** ch. 9, 11, 14


### SWE-T58: Treat test code with production-level care
Give test code production-level care: refactor brittle or slow tests, and simplify any test that needs its own test.
- **Why:** Test code that rots is ignored, which removes the protection the suite was meant to give.
- **When:** A test is brittle, slow or hard to read.
- **Not when:** Assertions change (SWE-T61), or a pure refactoring runs (SWE-T60).
- **Check:** Test code passes the same review and lint standards as production code.
- **Source:** ch. 11, 12


### SWE-T59: Keep every new test in the shared suite
Add each test you write to the shared suite, so teammates benefit and CI runs it (SWE-T24, SWE-T26).
- **Why:** A test kept out of the shared suite protects only its author's machine.
- **When:** Writing a new test for a feature or fix.
- **Check:** New test files are picked up by the suite's standard discovery and run in continuous integration.
- **Source:** ch. 11


### SWE-T60: Leave existing tests unchanged during a refactor
When a refactoring preserves behavior, leave the existing tests untouched, and investigate any test edit it appears to need.

- **Why:** An untouched test proves the behavior survived the refactor.
- **When:** Restructuring code without changing what it does.
- **Not when:** The behavior changes, so the tests legitimately need updates.
- **Check:** A pure refactoring diff contains no edits to existing test files.
- **Source:** ch. 12, 11

### SWE-T61: Edit existing tests only when documented behavior changes
Change an existing test only when the system's documented behavior or contract changes, and add new tests for new behavior.
- **Why:** Editing old tests for unrelated reasons hides whether the documented behavior actually changed.
- **When:** A feature or fix adds behavior that existing tests do not cover.
- **Check:** Test edits match a documented behavior change, and a fix to a failing test records whether code or test was wrong.
- **Source:** ch. 12


### SWE-T62: Learn why existing code exists before changing it
Before altering inherited code, learn why it was built that way, and pin its observable behavior with tests.
- **Why:** Inherited code often encodes a reason that is no longer visible in the code itself.
- **When:** Removing or changing code whose purpose is not clear from its surroundings.
- **Not when:** Code that is truly unclear or wrong still needs changing.
- **Check:** Changes to inherited code carry tests of their behavior, and an override states why the old reason no longer holds.
- **Source:** ch. 3, 22


### SWE-T63: Review your own diff before sending it
Read through your own change before requesting review, and look for anything you missed.

- **Why:** Reading your own change first catches oversights before reviewers see them.
- **When:** A change is ready to be sent to reviewers.
- **Check:** The diff contains no leftover debugging code or unfinished placeholders.
- **Source:** ch. 9


### SWE-T64: Include benchmarks with optimization changes
Provide benchmark results or benchmark tests with any change that aims to optimize performance.

- **Why:** Reviewers must judge an optimization, and a measurement is the evidence they can check.
- **When:** Submitting an optimization that reviewers must evaluate.
- **Check:** The optimization change includes benchmark results or benchmark tests.
- **Source:** ch. 9
