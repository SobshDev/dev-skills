# The Pragmatic Programmer — techniques

### PP-T01: Confirm a new project builds and runs first

Start a new project with minimal code, and confirm it builds and runs before adding features.

- **Why:** Confirming the build first gives later features a known-working base.
- **When:** Starting a new project or service from an empty repository.
- **Check:** The first commit includes build and run steps that succeed.
- **Source:** ch. 2

### PP-T02: Build a thin end-to-end path early

Connect one feature through every layer early as a runnable path, with full error checks, structure and documentation, before widening any layer.

- **Why:** Integration problems and gaps in the target only appear when all the layers meet.
- **When:** Requirements are vague, or the algorithms, libraries or environment are unfamiliar.
- **Not when:** A throwaway prototype answers one narrow question better.
- **Check:** One feature runs through the interface, logic, data and storage in a single path.
- **Source:** ch. 2, 9

### PP-T03: Prototype risky parts in disposable code

Build a throwaway prototype to answer one specific question about a risky part, then build the chosen design properly.

- **Why:** Disposable code lets you learn the answer cheaply without committing production code to an unproven choice.
- **When:** An unproven component, data format or performance concern affects the design.
- **Check:** Prototype code sits outside the production tree, and a clean implementation replaces it.
- **Source:** ch. 2

### PP-T04: Survey the project for known broken windows

Review the project regularly for known defects and poor areas, and keep one backlog entry per known defect with a name and an owner.

- **Why:** A named, owned list keeps known problems from being forgotten.
- **When:** The team reviews project health or a new member joins the project.
- **Check:** The backlog holds a named, owned item for each known problem area.
- **Source:** ch. 1

### PP-T05: Contain defects with a visible stopgap

When a proper fix must wait, contain the damage now with a stub or message that is visibly marked as temporary.

- **Why:** A visible stopgap limits the damage while keeping the unfinished work known to everyone.
- **When:** There is not enough time to repair a defect properly right now.
- **Not when:** The proper fix is possible now, so make that fix instead.
- **Check:** Stopgap code carries a visible marker, such as a not-implemented message or a named TODO.
- **Source:** ch. 1

### PP-T06: Change code in small, reversible steps

Make each change small enough that a mistake is easy to find and reverse.

- **Why:** Small changes keep the cost of each mistake low and make reversal simple.
- **When:** You develop or change code, whatever the size of the task.
- **Check:** Commits or pull requests are small, focused changes.
- **Source:** ch. 4

### PP-T07: Run tests after each refactoring step

Take short restructuring steps, and run the automated tests after each one.

- **Why:** A failing test right after a small step points to exactly the change that caused it.
- **When:** You restructure existing code that already has tests.
- **Check:** Commit history shows small steps, each followed by a passing test run.
- **Source:** ch. 7

### PP-T08: Generate repeated facts from one source

Generate code, docs and interface descriptions from one authoritative source instead of writing each copy by hand.

- **Why:** Hand-written copies of one fact drift apart as the source changes.
- **When:** The same API, schema or model must appear in several places.
- **Check:** Client code, mocks and docs are generated from a single specification file.
- **Source:** ch. 2

### PP-T09: Derive dependent values instead of storing them

Compute a value from the fields it depends on, and store only independent fields.

- **Why:** A stored copy of a derived value can drift from the fields it came from.
- **When:** A field, such as a total or a line length, can be computed from other data.
- **Not when:** A derived value is expensive and read often, in which case cache it privately.
- **Check:** The data class stores only independent fields and computes the dependent ones.
- **Source:** ch. 2

### PP-T10: Give each component one clear responsibility

Design each component around one well-defined purpose, and state that purpose in its documentation.

- **Why:** A component with one purpose can be changed and tested alone.
- **When:** You design a new module or split an existing one.
- **Check:** Each module's doc comment states a single responsibility.
- **Source:** ch. 2

### PP-T11: Ask objects to act instead of reaching inside

Ask an object to change its own state through a method, not from outside.

- **Why:** Reaching into another object's parts couples the caller to details the owner may change.
- **When:** Code needs to change state that belongs to another object.
- **Not when:** Stable language library types may be chained, but treat third-party APIs as volatile.
- **Check:** Callers do not chain through another object's internal parts to change data.
- **Source:** ch. 2, 5

### PP-T12: Wrap third-party APIs in your own layer

Put each third-party database, service or SDK behind an abstraction that you own.

- **Why:** A vendor change then needs edits in one wrapper.
- **When:** You adopt a database, service or SDK from a vendor.
- **Check:** Vendor SDK calls appear only inside the wrapper layer.
- **Source:** ch. 2

### PP-T13: Keep vendor-specific knowledge in one adapter

Keep endpoint paths, schema names, error codes and framework rules inside one adapter module that translates them.

- **Why:** External knowledge spread across modules multiplies the work of each change.
- **When:** Your code calls an external service, library or data source.
- **Check:** Endpoint paths and error codes of an external system appear in one adapter module.
- **Source:** ch. 2

### PP-T14: Validate external input once at the boundary

Check each external value once where it enters, naming any invalid value. Routine preconditions (PP-T36) flag caller bugs, not bad input.

- **Why:** Validation repeated in every layer adds noise, and bad data still travels far before it fails.
- **When:** Data arrives from users, networks or other modules.
- **Check:** Each external value is validated at one documented entry point.
- **Source:** ch. 3, 4

### PP-T15: Assert conditions you believe cannot occur

Add an explicit assertion wherever you are sure a value or state is impossible, with a message that names the failed condition.

- **Why:** An assertion turns a silent wrong assumption into an immediate, visible failure.
- **When:** You are sure a value or state can never occur.
- **Not when:** Expected bad input needs real error handling, and an extra full pass on a hot path may be too costly.
- **Check:** Assertions guard assumptions and verify output properties, contain no state-changing calls, and stay enabled in release builds unless measured as too costly.
- **Source:** ch. 4

### PP-T16: Crash early on impossible states

Stop soon after detecting an impossible condition, rather than continuing with suspect state.

- **Why:** Continuing from a state that should not exist spreads the damage and hides the original fault.
- **When:** Code reaches a state that should be impossible.
- **Check:** Impossible-state branches raise an error or exit, and switch statements have a default branch that raises.
- **Source:** ch. 4

### PP-T17: Keep build and deploy definitions in version control

Store every file needed to build, configure and deploy the project in the repository, except credentials (PP-T35).

- **Why:** A recorded history makes every release reproducible and reviewable.
- **When:** You set up build machines, pipelines or deployment configuration.
- **Check:** Build and deployment configuration files are tracked in the repository.
- **Source:** ch. 9

### PP-T18: Script each recurring build and release task

Replace written step lists for builds, releases, tests and setup with a script or pipeline definition, even for one-time steps.

- **Why:** A script runs the same way every time, while written steps depend on someone following them correctly.
- **When:** A routine task still depends on someone following written steps.
- **Check:** Recurring tasks exist as scripts or pipeline definitions, not as written instructions.
- **Source:** ch. 3, 9

### PP-T19: Store lasting project knowledge as plain text

Keep requirements, designs, test data and configuration as readable text files that outlast their tools.

- **Why:** Plain text stays readable as tools change, and diffs and grep work on it.
- **When:** You choose a format for project knowledge that must outlive its software.
- **Check:** Requirements, designs and test data are text files, not opaque binary blobs.
- **Source:** ch. 3

### PP-T20: Write a failing test before fixing a bug

Write a test that fails because of the defect, and only then change the code that fixes it.

- **Why:** The failing run proves that the test really catches the defect.
- **When:** You have a reproducible bug and are about to change code.
- **Check:** The fix commit adds a test that failed before the change.
- **Source:** ch. 3, 9

### PP-T21: Reduce each bug to one reproducing command

Reduce a bug that needs several manual steps to one test or script command.

- **Why:** A one-command reproduction lets anyone rerun the same check.
- **When:** A bug needs several manual steps to appear.
- **Check:** The repository has a test or script that reproduces the bug in one command.
- **Source:** ch. 3

### PP-T22: Bisect releases to find a regression

Test a version halfway between the last good version and the current one, and repeat until the change that broke it is found.

- **Why:** Each test halves the range, so the breaking change needs few checks.
- **When:** Code that worked earlier now fails across releases or commits.
- **Check:** A bisect log or history names the commit that introduced the failure.
- **Source:** ch. 3

### PP-T23: Show progress with a working demo

Show users and sponsors a working, end-to-end demo early and often, rather than describing progress in documents.

- **Why:** Running code gives users feedback that signed documents cannot.
- **When:** Sponsors or users ask for a demo or progress update.
- **Check:** A demo script or branch runs the full path successfully.
- **Source:** ch. 2

### PP-T24: Build small slices and get feedback each time

Build small slices of working functionality through every layer, riskiest first, and report each one to the customer before starting the next.

- **Why:** Feedback from each slice shows whether the team understands the problem.
- **When:** You start work on a problem you do not yet fully understand, once PP-T69 confirms software is needed.
- **Check:** Each change delivers something a user can exercise end to end.
- **Source:** ch. 2, 7

### PP-T25: Measure progress by finished use cases

Report progress as use cases that work end to end, rather than as modules that are mostly complete.

- **Why:** Modules reported as mostly complete can hide integration work that is still missing.
- **When:** You report progress on a multi-month build.
- **Check:** Progress reports list each use case as working end to end or not started.
- **Source:** ch. 2

### PP-T26: Name domain concepts in the domain's words

Use the application domain's terms for types, functions and tests, with one glossary.

- **Why:** Shared vocabulary keeps developers and users talking about one concept.
- **When:** You name types, functions or tests for a specific business area.
- **Check:** Identifiers and test names use terms from the project glossary or requirements.
- **Source:** ch. 2, 7, 8

### PP-T27: Pass dependencies as parameters, not globals

Give a routine the configuration, state and services it needs as parameters, and do not share them through globals or singletons.

- **Why:** Explicit parameters keep hidden links out of the code and make tests easy to set up.
- **When:** A module needs configuration, state or services from elsewhere.
- **Check:** New code takes its dependencies as parameters, and singletons expose no public mutable fields.
- **Source:** ch. 2, 5

### PP-T28: Use a callback list for simple notifications

Keep a plain list of callback functions in the event source when a few in-process listeners need an event.

- **Why:** A plain list gives notifications without adding a library or a shared event bus.
- **When:** A few in-process listeners must learn about an event.
- **Not when:** Many observers or slow callbacks, since they couple the source and block it.
- **Check:** The event source holds a plain list of callbacks, with no event library.
- **Source:** ch. 5

### PP-T29: Model event workflows as state machines

Describe ordered event handling as a finite state machine with a transition table.

- **Why:** A transition table shows exactly which event sequences the workflow accepts.
- **When:** Parsing ordered message sequences or running multi-step workflows driven by events.
- **Not when:** State machines sequence events but do not solve every event problem.
- **Check:** A transition table maps each current state and event to a next state and an action.
- **Source:** ch. 5

### PP-T30: Send unlisted events to an explicit error state

Make any event without a defined transition move the state machine to a named error state.

- **Why:** An explicit error state stops unexpected input from being silently ignored.
- **When:** Writing transition logic for a state machine that receives unexpected input.
- **Check:** Missing transitions lead to an explicit error state, not to staying in place.
- **Source:** ch. 5

### PP-T31: Store workflow state outside the process

Save the current state of a multi-step workflow to external storage, so it can resume between events.

- **Why:** Memory-only state is lost when the process restarts mid-workflow.
- **When:** A workflow spans many steps, such as a sign-up with several form stages.
- **Check:** Current workflow state is saved to storage rather than kept only in memory.
- **Source:** ch. 5

### PP-T32: Forward errors through each pipeline stage

Give each pipeline step a result that is either a value or an error, and let errors skip the remaining steps.

- **Why:** Errors then travel to the caller without later steps running on bad data.
- **When:** A pipeline step may fail, and later steps need its result to run.
- **Check:** Later steps run only on values, errors pass through unchanged, or a shared helper runs each step only on success.
- **Source:** ch. 5

### PP-T33: Use interfaces for polymorphism instead of subclassing

Express interchangeable behavior with interfaces or protocols, and check the alternatives before adding a subclass.

- **Why:** Interfaces let unrelated classes share a contract without coupling them to a common ancestor.
- **When:** Different classes must be handled interchangeably, or you are about to subclass to add behavior.
- **Check:** Collections and parameters use interface types, and no subclass exists only to share code.
- **Source:** ch. 5

### PP-T34: Externalize values that change between environments

Keep hosts, ports, limits and policy values that vary by environment or release in configuration or data, read through a thin accessor passed as a parameter (PP-T27).

- **Why:** Values kept outside the code change without editing the code.
- **When:** A value differs by deployment environment, customer or release.
- **Not when:** Values that never vary, such as protocol limits, stay in code.
- **Check:** Hosts, ports and environment-specific limits come from configuration, not inline literals.
- **Source:** ch. 5, 8

### PP-T35: Keep credentials in external configuration

Read keys, passwords and license values at runtime from external configuration, and never write them into source code.

- **Why:** A key committed to version control stays readable in every copy and its history.
- **When:** Code needs database passwords, third-party API keys or license checks.
- **Check:** Source files contain no credential or license literals, and values are read at runtime.
- **Source:** ch. 5, 7

### PP-T36: Write each routine's contract before coding it

Before writing a routine, state its input domain, preconditions, boundary conditions and what it does not promise.

- **Why:** A written contract tells callers what they must supply and what they can rely on.
- **When:** You design any function, method or component interface.
- **Check:** Public routines document preconditions, postconditions and non-promises.
- **Source:** ch. 4

### PP-T37: Restate base contracts in overriding methods

When an override replaces a method with a contract, repeat the base checks in the override, unless the language already propagates them.

- **Why:** An override that skips the base checks can break callers that rely on the contract.
- **When:** You subclass a class whose methods carry assertions or contract checks.
- **Not when:** The language propagates contracts to overrides automatically.
- **Check:** Overrides repeat base preconditions and invariant checks.
- **Source:** ch. 4

### PP-T38: Release resources in finally or scope cleanup

Acquire a resource before a try block, and release it in the finally clause or through scope-based cleanup.

- **Why:** Cleanup then runs on exceptions as well as normal returns.
- **When:** Code opens files, connections, locks or transactions that must be closed on every path.
- **Check:** Each try block starts after its acquisition, and a finally or scope releases that resource.
- **Source:** ch. 4

### PP-T39: Give each resource one owner that closes it

Make one routine or class responsible for closing each resource on every path, instead of adding special-case closes.

- **Why:** One owner with one cleanup point stops rarely taken branches from skipping the release.
- **When:** A rarely taken branch skips the cleanup step, or several places close the same resource.
- **Check:** Cleanup for each resource happens in one place for all execution paths.
- **Source:** ch. 4

### PP-T40: Write tests as first callers of interfaces

Write each test as the first caller of a new interface, and let the test shape the parameters and dependencies.

- **Why:** Tests needing global setup or hidden hooks reveal hard-to-use interfaces.
- **When:** You design a function's parameters or dependencies.
- **Check:** Tests call the code through its public parameters, with no global state or hidden hooks.
- **Source:** ch. 7

### PP-T41: Test each unit against its documented contract

Test each unit against its documented contract, including rejected inputs, boundary values and promised results.

- **Why:** Tests written from the contract check the promises callers actually rely on.
- **When:** You write unit tests for a function with a documented contract.
- **Check:** Tests cover rejected inputs, boundary values and promised results.
- **Source:** ch. 7

### PP-T42: Test bad and boundary inputs with every feature

Include invalid, boundary and failure-mode cases in the tests, not only the successful path.

- **Why:** Happy-path tests miss the inputs that cause real failures.
- **When:** A feature consumes external data, or works only on normal, expected input.
- **Check:** Test suites include invalid, boundary and unavailable-resource cases.
- **Source:** ch. 3, 4, 7

### PP-T43: Refactor only code that automated tests cover

Restructure code only after automated tests check its current behavior, and add tests first where none exist.

- **Why:** Tests show whether a restructuring changed behavior.
- **When:** You are about to restructure existing code.
- **Not when:** The change must alter behavior or interfaces, which makes it a feature change.
- **Check:** The area being restructured has automated tests covering its behavior.
- **Source:** ch. 7

### PP-T44: Keep new behavior out of refactoring commits

Put restructuring and new behavior in separate commits, so each change can be reviewed on its own terms.

- **Why:** Mixed commits make each change harder to review on its own.
- **When:** You restructure code that also needs new behavior.
- **Check:** New behavior arrives in separate commits from the restructuring.
- **Source:** ch. 7

### PP-T45: Multiply nested loop bounds to estimate cost

Estimate how a loop or recursion over variable input grows, and multiply nested loop limits to find quadratic cost.

- **Why:** Estimating growth flags risks, which measurement then confirms (PP-T46).
- **When:** A loop sits inside another loop over input, or you write recursion over variable input.
- **Check:** Nested loops and recursion over collections are reviewed for quadratic growth.
- **Source:** ch. 7

### PP-T46: Confirm a bottleneck before optimizing it

Measure the code with profiling data across several input sizes before you invest in tuning it.

- **Why:** Measured hot spots show whether tuning would actually pay off.
- **When:** You consider tuning an algorithm for speed.
- **Check:** Optimization changes cite profiling or benchmark data that shows the hot spot.
- **Source:** ch. 7

### PP-T47: Use the library's sort and search routines

Use the standard library's sort and search routines, and write custom code only when a benchmark justifies it.

- **Why:** Library routines are tested and tuned, so custom versions rarely win.
- **When:** You need to sort or search a collection.
- **Not when:** Beating the library routine would take substantial effort, so benchmark first.
- **Check:** Custom sort or search code is justified by a benchmark.
- **Source:** ch. 7

### PP-T48: Allow long passwords with any characters

Accept passwords of at least 64 characters, including spaces and Unicode, and avoid composition rules and forced timed changes.

- **Why:** Truncated or restricted input blocks strong passphrases that users would otherwise choose.
- **When:** You implement password entry, validation or expiry.
- **Check:** Password limits are at least 64 characters, and no code truncates or forces a character mix.
- **Source:** ch. 7

### PP-T49: Minimize exposed endpoints and data entry points

Expose only the endpoints and data entry points that have a current, documented need, and require authentication on those that read or change data.

- **Why:** Every entry point adds an attack surface, so fewer entry points give attackers fewer routes in.
- **When:** You design interfaces, endpoints or services.
- **Check:** Each exposed endpoint or port has a current, documented need, and data endpoints verify credentials before acting.
- **Source:** ch. 7

### PP-T50: Use least privilege for the shortest time

Request the rights a task needs, use them in a short scope, and drop them afterward.

- **Why:** Rights held for less time leave less room for a bug or attacker to misuse them.
- **When:** A task needs elevated rights such as root or administrator.
- **Check:** Privileged calls sit in short scopes, and the process drops rights afterward.
- **Source:** ch. 7

### PP-T51: Name each element after the role it plays

Name each new variable, function or module after the role it plays in the domain.

- **Why:** A role-based name tells why the element exists, while a generic name such as data does not.
- **When:** You create variables, functions, modules or applications.
- **Check:** Names describe a domain role, not generic words such as data.
- **Source:** ch. 7

### PP-T52: Use dedicated types for units and ranges

Use a dedicated type for a value whose unit or range is easy to misread, such as a percentage or an amount.

- **Why:** A typed value stops a percentage from being passed where an amount is expected.
- **When:** A parameter carries a percentage, an amount or another unit-bearing value.
- **Check:** Parameters for percentages, amounts or bounded ranges use defined types, not bare numbers.
- **Source:** ch. 7

### PP-T53: Ask about edge cases hidden in simple requirements

Ask the user what happens at the edges of a requirement that sounds simple, and record the answers in its ticket.

- **Why:** Edge cases cost far more to discover after the code is written.
- **When:** A requirement sounds simple and self-contained.
- **Check:** Requirement tickets list edge-case questions with recorded answers.
- **Source:** ch. 8

### PP-T54: Pair or mob on hard problems

On a hard or unfamiliar problem, ask the user for a second person to review or pair with.

- **Why:** A second view catches what one developer misses on a problem the team does not know well.
- **When:** A problem is tricky or unfamiliar, or the team codes mostly in isolation.
- **Check:** Pairing or review sessions appear in PR notes or commit trailers.
- **Source:** ch. 8

### PP-T55: Timebox a dreaded task, then decide

Give a task you keep avoiding a fixed time box, set in attempts or minutes, then decide whether to keep or delete the work.

- **Why:** A fixed time box makes an intimidating task finite.
- **When:** A task feels scary or difficult and you keep avoiding it.
- **Check:** The branch or files show a keep-or-delete decision after the time box.
- **Source:** ch. 7

### PP-T56: Step away and write down the problem

When stuck, set the problem aside briefly, then write down what was tried and the next untested idea.

- **Why:** Stepping away lets ideas surface, and explaining exposes hidden assumptions.
- **When:** Repeated attempts make no progress, or you cannot see the cause of a problem.
- **Check:** Problem notes record what was tried before the eventual fix.
- **Source:** ch. 7, 8

### PP-T57: Read the full error message before editing code

Read the complete error message and the location it names before you touch any code.

- **Why:** The full message usually names the failing location and cause that a guess would miss.
- **When:** An exception or crash occurs.
- **Check:** Notes or the commit message quote the complete error message and name the location it reports, before the first edit.
- **Source:** ch. 3

### PP-T58: Confirm the bad value in a debugger

Confirm in a debugger that a value is really wrong, then walk up the call stack to find where it first becomes wrong.

- **Why:** Checking the value first prevents a long analysis of behavior that is not actually wrong.
- **When:** The program returns a bad result without crashing.
- **Check:** Investigation notes record the observed value and name the first wrong frame.
- **Source:** ch. 3

### PP-T59: Keep notes on each clue you chase

Write down where you started, each clue you chase and each finding.

- **Why:** Writing a finding out exposes wrong ideas.
- **When:** An investigation involves many leads.
- **Check:** Notes or PR comments list the leads checked and abandoned.
- **Source:** ch. 3

### PP-T60: Use one format for trace statements

Format trace and log messages in one consistent, parseable format, with a fixed prefix and labeled fields.

- **Why:** A uniform format lets scripts follow state over time, which timing and concurrency bugs require.
- **When:** Bugs depend on timing, concurrency or event order.
- **Check:** Trace calls share one format, such as a fixed prefix and labeled fields.
- **Source:** ch. 3, 7

### PP-T61: Log every resource open and close

When a leak is suspected, log every resource open and close with a matching identifier, then find the unmatched ones.

- **Why:** Unmatched opens reveal a leak that code review often misses.
- **When:** A resource leak is suspected.
- **Check:** Logging wraps open and close calls and records a matching identifier.
- **Source:** ch. 3

### PP-T62: Turn ad hoc debugging checks into unit tests

Keep each manual check that exposed the defect as an automated test, a unit test where the project has one, otherwise the PP-T21 script.

- **Why:** A kept check guards against the same defect returning after later changes.
- **When:** A manual check during debugging exposed a defect.
- **Check:** Bug fixes add a test that reproduces the failing input.
- **Source:** ch. 7

### PP-T63: Use feature switches for diagnostics and unfinished features

Turn on extra diagnostics or unfinished features for selected users or groups with a configurable switch.

- **Why:** Diagnostics for every user add noise and can expose internal state.
- **When:** Only some users need extra diagnostics, or a feature must ship before every user is ready.
- **Not when:** Do not enable diagnostics where end users or unauthorized people could see them.
- **Check:** Diagnostic and feature code paths are guarded by a configurable switch per user or group.
- **Source:** ch. 7, 9

### PP-T64: Restructure code that blocks the next step

Change existing code that blocks the next step you need, in small steps that each pass their tests (PP-T43).

- **Why:** Work built on an unfit structure accumulates workarounds with each feature.
- **When:** The current structure constrains what you need to build next.
- **Not when:** The schedule impact outweighs the cost of keeping the old design.
- **Check:** Restructuring commits come before the features that needed the new structure.
- **Source:** ch. 7

### PP-T65: Tidy code right after its test passes

Clean up the code you just wrote once its new test passes.

- **Why:** Cleanup is cheapest while the code is small and the test still guards its behavior.
- **When:** A small addition has just made a test pass.
- **Check:** Cleanup commits follow a commit that has a passing test run.
- **Source:** ch. 7

### PP-T66: Remove calls that only seem to work

Remove workarounds that trial and error added, such as retries or sleeps, unless a comment or test justifies them.

- **Why:** Calls added by trial and error hide the real cause of the behavior.
- **When:** A working change still contains calls nobody can justify.
- **Check:** Each remaining call has a documented reason or a test that needs it.
- **Source:** ch. 7

### PP-T67: Document assumptions about routines you do not control

Write down each assumption your code makes about behavior it does not control.

- **Why:** Assumptions that are not written down are hard to recheck when the library changes.
- **When:** Your code relies on undocumented or boundary-case behavior of a routine you did not write.
- **Not when:** Undocumented behavior cannot always be avoided, so document the assumption carefully.
- **Check:** A comment or test at the call site states the assumed behavior.
- **Source:** ch. 7

### PP-T68: Judge designs by how easily they change

For each design option, list the modules a likely future change would touch, and prefer the option with fewer.

- **Why:** Ease of change is what the design must deliver over the life of the software.
- **When:** You compare design options.
- **Check:** The design note lists the modules touched by the likely change under each option.
- **Source:** ch. 8

### PP-T69: Check whether the requirement needs software at all

Before building a requested feature, check whether a non-software option meets the need, and ask the user before building if one does.

- **Why:** The cheapest way to meet a need is often one that involves no new code.
- **When:** You are about to implement a requested feature.
- **Check:** The reply to the user lists the alternatives considered, including non-software ones.
- **Source:** ch. 8

### PP-T70: Use vetted libraries for cryptography and login

Use established libraries and authentication providers for encryption, hashing and login, not code you write yourself.

- **Why:** Established libraries and providers avoid security errors that custom code would make.
- **When:** You need encryption, hashing, secure tokens, passwords or social sign-in.
- **Not when:** An expert with peer review and field trials may write primitives. A provider must suit your users.
- **Check:** Login and crypto calls use a vetted library or provider SDK, with no custom hashing, cipher or login storage code.
- **Source:** ch. 7

### PP-T71: Build only what current requirements need

Build only the structure, options and features that current requirements and callers need, and stop once they are met.

- **Why:** Guessed extensions and extra polish add code that serves no stated requirement.
- **When:** Deciding whether to add flexibility, polish or process beyond the agreed scope.
- **Not when:** Structure that the agreed value still needs is not a guessed future need.
- **Check:** Extension points and later changes trace back to a stated requirement or caller.
- **Source:** ch. 1, 4, 9

### PP-T72: Keep a bug fix's diff small

Keep a bug fix to the defect's own change, with no hacks, dead code or unrelated edits.

- **Why:** Under pressure, extra hacks and sprawling edits leave messes and break unrelated behavior.
- **When:** You fix a bug under deadline pressure, or the fix needs changes in many places.
- **Check:** The diff adds no workaround, dead code or unrelated edits beyond the fix, or the PR explains why more modules changed.
- **Source:** ch. 1, 2

### PP-T73: Do not skip or delete failing tests

Fix a failing test or remove it on purpose, and never skip or delete one just to get a green run.

- **Why:** A skipped or deleted test hides the real defect that its failure was reporting.
- **When:** A test keeps failing, or the team is ignoring it.
- **Check:** No test is skipped or ignored without an open ticket explaining why.
- **Source:** ch. 7

### PP-T74: Bind external input into queries and commands

Pass external input to databases and shell commands as bound parameters or escaped values, never by string concatenation.

- **Why:** Concatenated input lets an attacker change the query or command that runs.
- **When:** Code builds a database query, view or shell command from user, file or system data.
- **Check:** Database queries bind parameters, and shell calls avoid interpolated input.
- **Source:** ch. 7
