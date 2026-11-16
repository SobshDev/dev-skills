# Clean Code — techniques

### CC-T01: Finish a working version before restructuring
Get a first version working, then restructure it with its tests still passing.

- **Why:** Separate steps keep each failure traceable to one kind of change.
- **When:** A feature built without test-first work has a working first version. Test-first work uses CC-T03.
- **Check:** Refactoring commits keep existing tests passing without changing their assertions.
- **Source:** ch. 2 § (chapter opening); ch. 7 § Reading Code from Top to Bottom: The Stepdown Rule; ch. 8 § This Is Too Much to Constantly Keep in Mind; ch. 9 § Make It Right; ch. 28 § Tests

### CC-T02: Clean each mess when you meet it
Clean a mess when you create it or find it, instead of postponing the cleanup.

- **Why:** Each later change in that area pays the cost of the mess again.
- **When:** You notice a workaround you added or a messy area beside your change.
- **Not when:** Code no current change touches is left alone for now, and a deadline may defer cleanup, which still needs a later pass (CC-P3).
- **Check:** Each workaround you added or touched is removed or fixed in the same diff.
- **Source:** ch. 1 § Bad Code; ch. 1 § Productivity; ch. 9 § Make It Right; ch. 13 § Should We Do Anything Now?

### CC-T03: Refactor after each passing test
Once a test passes, clean the code that satisfies it before writing the next test.

- **Why:** Each cleanup then starts from a state known to pass.
- **When:** Inside a test-first cycle, right after a test turns green.
- **Check:** Each refactoring commit follows a commit where a test turned green.
- **Source:** ch. 9 § Make It Right; ch. 21 § Doing Work; ch. 29 § Eisenhower’s Matrix

### CC-T04: Revert a cleanup step that breaks tests
Undo only the cleaning step that broke an existing test, and leave other edits alone.

- **Why:** Reverting keeps the last working state instead of patching failures.
- **When:** A refactoring step makes an existing test fail.
- **Check:** Failing cleanup edits are reverted, not patched over the failing tests.
- **Source:** ch. 9 § Make It Right; ch. 14 § Discipline 2: Test && Commit || Revert (TCR)

### CC-T05: Write a failing test before production code
Write a test for new behavior and watch it fail before writing the production code.

- **Why:** A test that requires the code keeps untested production code from appearing.
- **When:** Starting any new behavior in a test-driven workflow.
- **Not when:** A throwaway design sketch that will not ship is exempt.
- **Check:** Each production change in a diff follows a test that failed before it.
- **Source:** ch. 9 § Example; ch. 14 § The First Law; ch. 21 § When Should We Ensure Confirmability?; appendix § Test-Driven Development

### CC-T06: Write just enough test to fail, then code
Write only as much test as makes it fail, then only the code that makes it pass.

- **Why:** Small steps keep each failure close to the change that caused it.
- **When:** Adding a test during a test-first cycle, before its production code exists.
- **Not when:** The unit's overall design is still unsettled, and a narrow test focus can hide it.
- **Check:** Each new test fails before its production code exists, including by failing to compile.
- **Source:** ch. 9 § Example; ch. 14 § The Second Law; ch. 14 § The Third Law; appendix § Test-Driven Development

### CC-T07: Give test fixtures sensible defaults
Let test helpers fill omitted fields with defaults, and set only what each test checks.

- **Why:** A production signature change then touches only a few tests.
- **When:** Tests build input objects with many fields they do not care about.
- **Check:** Each test sets only the fields that its assertion depends on.
- **Source:** ch. 9 § Example; ch. 15 § Test Design

### CC-T08: Wrap repeated test steps in named helpers
Move repeated setup and assertion lines into a named helper that each test calls.

- **Why:** Test bodies then show only the facts the behavior depends on.
- **When:** Several tests repeat the same setup and assertion lines.
- **Check:** Repeated multi-line test bodies are replaced by one named helper call.
- **Source:** ch. 9 § Example; ch. 15 § Domain-Specific Testing Language; ch. 15 § Composed Assertions

### CC-T09: Arrange, act, and assert with one action
Arrange the data, perform one action, then assert one logical fact about the result.

- **Why:** A single action means a failing test points to one behavior.
- **When:** Writing a new test or reviewing an existing one.
- **Check:** Each test body has one action call, and its assertions support one logical claim.
- **Source:** ch. 15 § (chapter opening); ch. 15 § The Single Assert Rule; ch. 15 § The Single Act Rule

### CC-T10: Keep each test independent of the others
Make every test set up its own state, so it runs alone and in any order.

- **Why:** Hidden ordering makes failures depend on which tests happened to run first.
- **When:** A test's setup depends on state that an earlier test created.
- **Check:** The suite passes when run in shuffled order.
- **Source:** ch. 15 § Isolated

### CC-T11: Replace slow dependencies with fakes in tests
Replace databases, disks, network, clock, and UI with fakes in unit tests.

- **Why:** Fake dependencies keep tests fast and the same in every environment.
- **When:** Unit tests run real queries, wait on peripherals, or need the network or clock.
- **Check:** Unit tests touching a database, disk, network, or clock use a fake, or a mock returning data without verifying calls (CC-T15).
- **Source:** ch. 15 § Repeatable; ch. 33 § Testing

### CC-T12: Pass collaborators in as parameters
Give each unit its collaborators as parameters, not as objects it creates internally.

- **Why:** Tests can then substitute fakes without changing the production code.
- **When:** A module is hard to test because it reaches external resources directly.
- **Check:** Units receive their dependencies as parameters instead of constructing them, grouped into one object past three (CC-T25).
- **Source:** ch. 14 § Design; ch. 21 § When Should We Ensure Confirmability?; ch. 22 § Make Your Threaded Code Pluggable; ch. 26 § UI/Application Boundary

### CC-T13: Keep framework and hardware calls in thin layer
Put code that touches a screen, socket, or framework behind a call-forwarding layer.

- **Why:** Logic outside the thin layer stays testable without hardware.
- **When:** Code must touch a hardware boundary or a hard-to-test framework.
- **Check:** The wrapper class contains only forwarding calls and no branches or loops.
- **Source:** ch. 14 § Complications and Loopholes

### CC-T14: Test policy modules without a UI or database
Run policy-module tests against in-memory fakes, without a UI, web server, or database.

- **Why:** Fast rule tests keep policy checkable from project start.
- **When:** Writing tests for core use cases or early business logic.
- **Check:** Policy-module tests run without starting a UI, web server, or database.
- **Source:** ch. 25 § Case Study: FitNesse; ch. 27 § The Clean Architecture

### CC-T15: Assert outcomes, not internal steps
Test each behavior's result, not the internal calls or ordering that produce it.

- **Why:** Internal refactoring then leaves the tests unchanged.
- **When:** Writing tests for a class's behavior.
- **Not when:** Private details are tested directly only when public tests cannot reach them.
- **Check:** Tests assert results and do not verify internal method calls or ordering.
- **Source:** ch. 13 § Simpler Testing

### CC-T16: Name tests and data after their intent
Name each test for the rule or case it checks, and fixtures for their scenario.

- **Why:** A failing test name then states the broken rule without reading the body.
- **When:** Understanding improves after tests were written with vague labels.
- **Check:** Test names describe a business rule or case, not a vague label.
- **Source:** ch. 9 § Example; ch. 10 § What Are Large Functions Anyway?

### CC-T17: Clean test code to the production standard
Hold test names, helpers, and setup to the same quality bar as production code.

- **Why:** Dirty tests slow maintenance and weaken the safety net.
- **When:** Writing or reviewing test code.
- **Check:** Test helpers and setup are named and structured as production code is.
- **Source:** ch. 14 § Keeping Tests Clean

### CC-T18: Name for readers without your context
Choose names that a reader without the implementation understands, even if they are long.

- **Why:** Such names carry meaning without the reader opening the code behind them.
- **When:** Naming elements after you have worked out the logic yourself.
- **Not when:** A frequently called function may need a short, memorable name (CC-T20).
- **Check:** Each new name, read without its implementation, says what the element is for.
- **Source:** ch. 3 § Everything Small, Well Named, Organized, and Ordered; ch. 7 § Descriptive

### CC-T19: Replace comments with named methods or variables
Move a commented condition or sub-expression into a method or variable named for its meaning.

- **Why:** A name stays accurate as the code changes, while a comment can drift.
- **When:** A comment is needed to explain a conditional or unnamed sub-expression.
- **Not when:** A comment recording why a surprising choice was made stays, since no name carries that reason.
- **Check:** Explanatory comments sit beside a conditional that could be a named query method.
- **Source:** ch. 5 § Lying Comments; ch. 5 § Explain Your Intent in Code; ch. 5 § Use a Function or a Variable Instead of a Comment; ch. 5 § Explanation of Intent; ch. 13 § Fixing the Problem; appendix § Comments

### CC-T20: Scale name length with scope
Give widely visible names short forms, and give private helpers longer, more specific names.

- **Why:** Short names read cleanly at many sites, and long names state purpose at few.
- **When:** Naming a variable, function, or class whose visibility is narrow or wide.
- **Not when:** A function called once can keep a long name, and teams that prefer short names with comments keep that convention.
- **Check:** Public names stay short, and a private helper called once has a descriptive name.
- **Source:** ch. 4 § Variable Names; ch. 4 § Function Names; ch. 7 § Descriptive; ch. 7 § Convenient; appendix § Comments

### CC-T21: Name functions with verbs and modules with nouns
Name each function as an action, and each module or class as a domain noun.

- **Why:** Calls then read as sentences in the vocabulary of the domain.
- **When:** Designing function names or the vocabulary of a module or system.
- **Not when:** Teams that name getters after the value they return keep their convention.
- **Check:** Module and class names are nouns, and function names are verbs matching domain actions.
- **Source:** ch. 3 § Functions; ch. 4 § Method Names; ch. 7 § Descriptive; ch. 8 § Conclusion

### CC-T22: Use one word per concept across the code
Pick one term for each business concept and use it in every module.

- **Why:** Synonyms make readers wonder whether two names mean two things.
- **When:** One concept appears under several names in one module or across modules.
- **Check:** The diff uses two names for one business value, within or across modules.
- **Source:** ch. 4 § Pick One Word per Concept

### CC-T23: Leave type prefixes out of names
Name variables and fields without type prefixes, interface I prefixes, or member markers.

- **Why:** Compilers and editors track types, so prefixes go stale after a type change.
- **When:** Naming variables or fields in a language with a rich type system.
- **Not when:** Languages with very short identifier limits still need encodings.
- **Check:** In a rich-type language, the diff adds a type prefix, I prefix, or m_ marker.
- **Source:** ch. 4 § Avoid Encodings; ch. 4 § Member Prefixes; ch. 4 § Interfaces and Implementations

### CC-T24: Name constants for codes, positions, and magic numbers
Replace status numbers, fixed array positions, and unexplained numbers with named constants.

- **Why:** A name tells readers what the number means at every use.
- **When:** Code compares against literal status codes, reads fixed positions, or uses unexplained numbers.
- **Not when:** Only when helper calls would cost unacceptable time on a critical path.
- **Check:** The diff adds a bare status number, index, or unexplained number.
- **Source:** ch. 2 § The Cleaning Process; ch. 4 § Build a System of Names; ch. 7 § Homogenous

### CC-T25: Pass an object when values travel together
Group values that always travel together into one object or data structure.

- **Why:** The signature shrinks, and the group gains a name readers can see.
- **When:** A parameter list has grown past three values that belong together.
- **Check:** Four or more parameters are passed together at every call site.
- **Source:** ch. 4 § Add Meaningful Context; ch. 7 § Insulated; ch. 8 § More Than Three?

### CC-T26: Keep parameter lists to three or fewer
Limit each function to at most three parameters, and prefer zero or one.

- **Why:** Each extra argument makes calls harder to read and to get right.
- **When:** You design a signature or extend an existing one.
- **Not when:** A function that genuinely needs several inputs keeps them, in an obvious order.
- **Check:** A signature in the diff takes more than three parameters, or gains one.
- **Source:** ch. 7 § Insulated; ch. 8 § Function Arguments

### CC-T27: Return results instead of output arguments
Return the result, or store it in an object, not in an argument.

- **Why:** Callers read the outcome directly instead of tracking side effects.
- **When:** A function must provide more than one result.
- **Not when:** Languages without objects or multiple returns may need output arguments.
- **Check:** In a language with objects or multiple returns, a function writes to a parameter that callers read.
- **Source:** ch. 8 § Output Arguments

### CC-T28: Separate commands from queries
Make each method either change state or return information, not both.

- **Why:** Callers can ask a question without causing a side effect.
- **When:** A method changes state and also returns a value that callers use.
- **Not when:** An atomic query-and-change, such as a stack pop, may stay.
- **Check:** A method both changes state and returns a value that callers use.
- **Source:** ch. 8 § Command Query Separation

### CC-T29: Report failures with exceptions
Report failures with exceptions, and keep normal steps free of status checks.

- **Why:** Normal steps then read straight through without per-step error tests.
- **When:** A function can fail and its caller must handle the failure.
- **Not when:** The language has no exceptions, or its exception handling is not reliable.
- **Check:** In a language with exceptions, callers check error codes after every call.
- **Source:** ch. 8 § Prefer Exceptions to Returning Error Codes; ch. 8 § Caveat Emptor

### CC-T30: Move try and catch bodies into functions
Move a multi-statement try or catch body into its own named function.

- **Why:** The main function then shows its steps apart from its failure handling.
- **When:** A try block mixes normal steps with error handling.
- **Check:** A try or catch block holds more than one statement.
- **Source:** ch. 8 § Extract Try/Catch Blocks

### CC-T31: Name conditions and loop bodies as predicates
Extract an if condition or loop body into a function whose name states its meaning.

- **Why:** The control statement then reads as one sentence about the domain.
- **When:** A conditional or loop body holds multi-step logic or checks a state.
- **Check:** Such a conditional reads as one named predicate call, such as shouldDeleteRecord(r).
- **Source:** ch. 7 § Well-Written Prose; ch. 10 § Extract Method Refactoring; ch. 13 § Fixing the Problem; appendix § Comments

### CC-T32: Keep functions short: a dozen lines, two levels
Keep each function near a dozen lines, with at most two indentation levels.

- **Why:** A reader takes a short function in at once, on one screen.
- **When:** A function grows past about a dozen lines or reaches three indentation levels.
- **Not when:** Some functions read better undivided, and switch statements or formatting code run longer.
- **Check:** Function bodies in a diff run past a dozen lines or reach three indentation levels.
- **Source:** ch. 1 § What Is Clean Code?; ch. 7 § Small!; ch. 7 § Well-Written Prose; ch. 10 § Extract Method Refactoring

### CC-T33: Extract a helper only where its name abstracts
Extract a block only when the helper's name is more abstract than the code it hides.

- **Why:** A helper that restates one statement adds reading cost and hides nothing.
- **When:** A function performs several distinct steps that a name can abstract.
- **Not when:** Independent steps with clear names deserve helpers, and a forwarder that only moves code elsewhere does not, except a vendor adapter (CC-T51).
- **Check:** Each extracted helper is named for its purpose and does more than forward one call.
- **Source:** ch. 2 § (chapter opening); ch. 7 § Entanglement; ch. 10 § Extract Method Refactoring; ch. 10 § 5. Entanglement

### CC-T34: Order helpers in the order they are called
List helper functions below their caller, in the order the caller first calls them.

- **Why:** Readers follow the flow downward without jumping back and forth.
- **When:** One function calls several helpers in sequence within one file.
- **Not when:** Declaration-first languages reverse this order, and ordering cannot fix entanglement.
- **Check:** Where helper order is free, helpers appear in the order of their first calls.
- **Source:** ch. 2 § The Cleaning Process; ch. 6 § Dependent Functions; ch. 7 § Reading Code from Top to Bottom: The Stepdown Rule; ch. 10 § 4. Bouncing Around; appendix § Method Length

### CC-T35: Share working state through fields
Promote locals that several extracted helpers need into fields of one object.

- **Why:** Helpers then drop long argument lists that repeat the same values.
- **When:** Extraction is blocked because a block modifies two or more locals.
- **Not when:** Static fields shared by several threads can break the helpers.
- **Check:** Extracted methods share state through instance fields instead of extra parameters.
- **Source:** ch. 2 § The Cleaning Process; ch. 4 § Add Meaningful Context; ch. 8 § Function Arguments; ch. 8 § Similar Code; ch. 10 § What Are Large Functions Anyway?

### CC-T36: Merge duplicates that change together for one actor
Consolidate similar code whose copies change for the same reasons into one place.

- **Why:** One shared copy means one place to fix when the shared rule changes.
- **When:** Copies serve one actor and are edited together in recent changes.
- **Not when:** Copies serve different actors, or the repeat is two or three stable lines.
- **Check:** Copies of the same logic change in the same commit.
- **Source:** ch. 8 § DRY: Don’t Repeat Yourself; ch. 8 § Simple Repeated Code; ch. 8 § Accidental versus Essential Duplication; ch. 18 § Minimize Duplication; ch. 19 § Accidental Duplication

### CC-T37: Traverse a structure once and vary the action
Keep the traversal in one place, and pass the varying work in as a function.

- **Why:** Repeated loops then change in one place only.
- **When:** Several features walk the same nested structure in the same way.
- **Not when:** Languages without lambdas need a strategy, command, or template method instead.
- **Check:** Identical nested loops appear in several classes with only the loop body changed.
- **Source:** ch. 8 § Loop Duplication; ch. 18 § Minimize Duplication

### CC-T38: Replace repeated type switches with polymorphism
Replace a repeated type switch with polymorphic classes chosen by a factory.

- **Why:** A new type then adds one class instead of edits to every switch.
- **When:** The same switch appears in several places, or new types keep arriving.
- **Not when:** The switch covers few cases unlikely to grow, or behavior changes more often than types.
- **Check:** Adding one new item type in a diff touches more than one switch or lookup.
- **Source:** ch. 3 § A More Significant Example; ch. 7 § Switch Statements; ch. 10 § What Are Large Functions Anyway?

### CC-T39: Keep each switch in one factory behind interface
Keep an unavoidable switch in one module that creates objects, hidden behind an interface.

- **Why:** The rest of the system depends on the interface, not on type codes.
- **When:** A switch on type cannot be avoided in the design.
- **Not when:** Behavior changes far more often than the data types do.
- **Check:** The switch appears only in a factory or main module, not in general logic.
- **Source:** ch. 7 § Switch Statements; ch. 12 § The OO/Procedural Trade-off

### CC-T40: Hide mutable state in classes with behavior
Keep mutable state private, and expose one public method that performs the work.

- **Why:** Callers cannot disturb the state between internal steps.
- **When:** A class with behavior changes internal state to compute a result.
- **Not when:** Multithreaded use requires locks or per-caller instances to protect the state.
- **Check:** Public methods hide private steps that change fields.
- **Source:** ch. 7 § Contextual; ch. 8 § Object-Oriented Languages

### CC-T41: Give each class either data or behavior
A class with behavior keeps private fields (CC-T40), and a data-only class may use public fields.

- **Why:** Mixing both in one class makes it awkward to extend in either direction.
- **When:** Designing a new class or record-like type.
- **Check:** Each class has private fields with methods, or public fields with no methods.
- **Source:** ch. 12 § Data/Object Antisymmetry; ch. 12 § Hybrids

### CC-T42: Call methods only on immediate collaborators
Ask an object to act through its own collaborators, not through chained calls.

- **Why:** Callers then depend on one step instead of the structure beneath it.
- **When:** Code chains calls through objects returned by other calls.
- **Not when:** Chains through plain data structures are harmless, since those expose their fields anyway.
- **Check:** Code contains chained calls such as a.b().c().d() across object boundaries.
- **Source:** ch. 12 § The Law of Demeter; ch. 12 § Hiding Structure

### CC-T43: Give each concern its own class
Move each concern into a class named for it, with one reason to change.

- **Why:** Changes for one concern then leave unrelated code alone.
- **When:** Logic for one concern sits in a large function or in an unrelated class.
- **Not when:** A very small system can stay in one class, and tiny classes need not be split.
- **Check:** Each class name states a single concern, and its methods serve that concern.
- **Source:** ch. 9 § Considering the Design and Architecture; ch. 10 § What Are Large Functions Anyway?; ch. 13 § What Should a Class Contain?; ch. 13 § Heuristics and Characteristics; ch. 13 § When Is a Class Too Large?

### CC-T44: Keep classes small and cohesive
Make each class small, with methods that share its data and a covering name.

- **Why:** Cohesive classes stay easy to name, test, and change.
- **When:** Creating a new class or renaming an existing one.
- **Check:** The class name summarizes every public method, and the methods share the same data.
- **Source:** ch. 13 § Heuristics and Characteristics; ch. 13 § Is This Overengineering?

### CC-T45: Add new behavior as new classes
Put new behavior in its own single-purpose class, not in a branch of an existing one.

- **Why:** Working modules stay unchanged and free of new regression risk.
- **When:** A new case would extend a switch or conditional in an existing class.
- **Check:** New behavior arrives as new classes, and the factory edit is one registration line (CC-T39).
- **Source:** ch. 3 § A More Significant Example; ch. 13 § An Overly Open Implementation; ch. 19 § OCP: The Open–Closed Principle

### CC-T46: Keep subtypes substitutable for their callers
Make each subtype behave like its base type, so callers never branch on its concrete type.

- **Why:** Substitutes then keep existing callers working unchanged.
- **When:** Creating subclasses or alternatives, such as a REST service with the same contract.
- **Check:** Callers use the base type and never test for a concrete subtype.
- **Source:** ch. 19 § LSP: The Liskov Substitution Principle; ch. 19 § LSP and Design

### CC-T47: Depend only on the operations a client calls
Split broad interfaces so that each client sees only the operations it calls.

- **Why:** Changes to unrelated operations then leave this client's code untouched.
- **When:** A class exposes operations that some of its clients never use.
- **Not when:** Dynamically typed languages have no declarations that force recompilation.
- **Check:** Each client's declarations reference only the operations it calls.
- **Source:** ch. 19 § ISP: The Interface Segregation Principle; ch. 19 § ISP and Language

### CC-T48: Put interfaces between policy and detail
Declare an interface in the high-level policy, and have the low-level module implement it.

- **Why:** Interfaces change less often than implementations, so policy stays stable.
- **When:** High-level code calls low-level code directly, and the dependency must reverse.
- **Not when:** Stable platform classes such as String may remain concrete dependencies.
- **Check:** The low-level module imports an interface that the high-level policy declares.
- **Source:** ch. 19 § DIP: The Dependency Inversion Principle; ch. 19 § Stable Abstractions

### CC-T49: Wire concrete implementations in the outermost layer
Construct concrete objects in the entry point or composition code, and pass them inward.

- **Why:** The policy then depends only on interfaces and stays testable.
- **When:** A policy module needs collaborators supplied at startup or in tests.
- **Check:** Policy classes receive collaborators as constructor arguments and never create them.
- **Source:** ch. 9 § Considering the Design and Architecture; ch. 19 § Factories; ch. 19 § Concrete Components; ch. 26 § UI/Application Boundary

### CC-T50: Break dependency cycles by inverting one dependency
Break a cycle with an interface the calling component declares and the other implements.

- **Why:** An acyclic graph keeps a valid build order and stops components from merging.
- **When:** Two classes or components depend on each other.
- **Check:** The diff adds no dependency that closes a loop between components.
- **Source:** ch. 9 § Considering the Design and Architecture; ch. 20 § The Acyclic Dependencies Principle (ADP); ch. 20 § Breaking the Cycle

### CC-T51: Wrap third-party code in your own adapter
Wrap vendor APIs in an adapter whose interface follows your application's needs.

- **Why:** Vendor types then stay out of application code, so a vendor change touches one place.
- **When:** Application code calls a vendor API or framework.
- **Check:** Vendor types appear only inside an adapter whose methods only delegate.
- **Source:** ch. 26 § Clean Boundaries; ch. 26 § SOLID and Hexagonal Architecture

### CC-T52: Define your own interface for a missing dependency
Define a local interface for an unfinished dependency, and test clients against a fake.

- **Why:** Client code can finish without waiting for the unfinished design.
- **When:** Code depends on hardware or a service whose design is not finished.
- **Check:** Client code depends on a local interface, not on any unfinished vendor type.
- **Source:** ch. 26 § Using Code That Does Not Yet Exist

### CC-T53: Keep policy modules free of framework types
Keep policy code free of framework, SQL, and HTML types, and use adapters at the edge.

- **Why:** Rules stay testable and unaffected by changing frameworks.
- **When:** Business rules sit alongside storage, presentation, or framework code.
- **Check:** Policy-module files import no SQL, HTML, or framework types.
- **Source:** ch. 18 § (chapter opening)

### CC-T54: Store data in memory behind an interface first
Start with in-memory storage behind a data interface, and defer the database choice.

- **Why:** Policy can be built and tested while the storage decision stays open.
- **When:** Early development, before storage needs are known.
- **Check:** Early builds use an in-memory or file implementation of the data interface.
- **Source:** ch. 25 § What Lines Do You Draw, and When?; ch. 25 § Case Study: FitNesse

### CC-T55: Keep queue and thread calls out of logic
Keep queue, thread, and lock calls in small boundary functions, away from policy classes.

- **Why:** Business rules then run and test without a thread or process.
- **When:** You add a queue, thread, process, or lock, or business logic calls one.
- **Check:** Policy modules contain no queue, thread, or process calls.
- **Source:** ch. 22 § Single Responsibility Principle; ch. 26 § UI/Application Boundary

### CC-T56: Hold one lock across a multi-step sequence
Put a sequence of calls on one shared object under one lock.

- **Why:** Separately locked calls can interleave with other threads and break the sequence.
- **When:** Clients must call several methods on one shared object in order.
- **Not when:** Some designs need several calls on one shared object. If you can change the server, add one locking method.
- **Check:** Each multi-step operation on a shared object runs inside one lock scope.
- **Source:** ch. 22 § Beware Dependencies between Synchronized Methods

### CC-T57: Keep shared fields private and guarded
Keep shared fields private, and let only a few guarded methods write them.

- **Why:** Limiting who writes shared data limits where races can happen.
- **When:** A field or collection is reachable from more than one thread.
- **Not when:** Shared resources such as database connections often cannot be removed.
- **Check:** Shared fields are private and written only from a few guarded methods.
- **Source:** ch. 22 § Corollary: Limit the Scope of Data

### CC-T58: Use thread-safe types for shared state
Use concurrent collections and atomic counters for data that threads share.

- **Why:** Plain types can lose updates or corrupt data under concurrent access.
- **When:** Several threads read or write the same collection or counter.
- **Check:** Shared collections and counters use concurrent or atomic types.
- **Source:** ch. 22 § Thread-Safe Collections; ch. 22 § Challenges

### CC-T59: Make blocked threads able to stop
Give every blocked thread a path to receive a stop signal and finish.

- **Why:** Threads that cannot stop hang at exit and lose work.
- **When:** A parent waits on child threads, or a producer and consumer must stop together.
- **Check:** A test stops all threads and confirms that shutdown completes.
- **Source:** ch. 22 § Writing Correct Startup and Shutdown Code Is Hard

### CC-T60: Treat spurious failures as threading defects
Investigate every unexplained or intermittent failure in threaded code as a probable threading defect.

- **Why:** One-off labels hide races that return under load.
- **When:** A threaded test fails once in many runs, or passes only on rerun.
- **Check:** The diff does not mark an intermittent threaded test as skipped, retried, or one-off.
- **Source:** ch. 22 § Treat Spurious Failures as Candidate Threading Issues

### CC-T61: Use a jiggle hook for thread timing
Define one swappable jiggle hook at thread interleaving points, which tests make sleep or yield randomly.

- **Why:** Random timing can expose rare orderings without slowing production code.
- **When:** Testing threaded code whose bugs appear rarely.
- **Not when:** Manual yield or sleep calls left in production slow the code down.
- **Check:** Production builds bind the jiggle hook to a no-op, and tests repeat with random timing.
- **Source:** ch. 22 § Automated

### CC-T62: Render async views only after loading finishes
Gate rendering of an asynchronously loaded view on a loaded flag.

- **Why:** Rendering before data arrives can crash the view.
- **When:** A view depends on data that loads asynchronously.
- **Check:** The render path checks a loaded flag before creating the view.
- **Source:** ch. 22 § Double-Deleting of Resources on Rerender Using a 2D Library in React Native

### CC-T66: Shorten the feedback loop and measure it
Measure building, testing, and deploying, and shorten each step that slows a change.

- **Why:** Long loops push developers into bigger, riskier batches.
- **When:** A build or test takes minutes after a small edit, or delivery feels slow.
- **Check:** Build and test timings are recorded per change, within a minute or two.
- **Source:** ch. 31 § Continuous Integration; ch. 33 § Viscosity; ch. 33 § Building

### CC-T67: Fix a failing build before other work
Repair a failing build or acceptance test before making any other change.

- **Why:** A red main line blocks everyone's integration.
- **When:** The continuous build or acceptance suite fails after a push.
- **Check:** The fix commit lands before further feature commits on the branch.
- **Source:** ch. 16 § The Continuous Build; ch. 31 § Continuous Build

### CC-T68: Run the full suite on every push
Run the full build and tests automatically on each push.

- **Why:** Problems surface on the change that caused them.
- **When:** Setting up or changing the continuous build pipeline.
- **Check:** CI configuration triggers a build and test run on each push.
- **Source:** ch. 31 § Continuous Build

### CC-T69: Never disable failing tests to go green
Fix a failing test instead of skipping, ignoring, or disabling it to pass the build.

- **Why:** Disabled tests stop guarding the behavior and become lies.
- **When:** A test fails and fixing it is deferred to later.
- **Not when:** A slow or broken test may be disabled with a message stating why, except an intermittent threaded test (CC-T60).
- **Check:** The diff adds a skip, ignore, or disable marker with no reason stated.
- **Source:** ch. 5 § Warning of Consequences; ch. 31 § Continuous Build

### CC-T70: Integrate often on short-lived branches
Merge work to the main line within hours or a day, and keep branches short.

- **Why:** Small merges stay trivial, while long branches delay everyone's integration.
- **When:** Work is held on a separate line for days or weeks.
- **Check:** Branches stay open for hours or a day, and pushes arrive several times daily.
- **Source:** ch. 31 § Continuous Integration; ch. 31 § Branches versus Toggles

### CC-T71: Keep comments accurate beside their code
Keep each comment beside its declaration, and fix or remove claims the code no longer supports.

- **Why:** A wrong comment misleads readers more than no comment would.
- **When:** Code changes near an existing comment that describes it.
- **Check:** Comments on lines the diff changes, or that describe them, are updated or removed.
- **Source:** ch. 5 § Hidden or Obscured Comments; ch. 5 § Lying Comments; ch. 5 § Misleading Comments

### CC-T72: Document public API members with doc comments
Write doc comments for public API members, so users need not read the code.

- **Why:** Callers outside the team cannot ask the author what a member promises.
- **When:** Code is exposed as a public API to other teams or projects.
- **Not when:** Code used only within one team, where clear names and signatures often suffice.
- **Check:** Each public member added has a doc comment on its purpose, inputs, and result.
- **Source:** ch. 5 § Javadocs (and Their Ilk) in Public APIs; appendix § Comments; appendix § John’s Rewrite of `PrimeGenerator`

### CC-T73: Keep history out of source comments and commits
Delete commented-out code, change logs, and author or ticket tags from source.

- **Why:** Version control already keeps the history that dead code and comments hold.
- **When:** Code is disabled, or comments carry such history, and you are about to commit.
- **Not when:** Commented-out code used only during local debugging, and never committed, is fine.
- **Check:** The committed change has no commented-out code, change logs, or name and ticket tags.
- **Source:** ch. 5 § Attributions and Bylines; ch. 5 § Journal Comments; ch. 5 § Commented-Out Code

### CC-T74: Format with one team standard via tool
Agree on one simple style, and let an automated formatter enforce it on changed files.

- **Why:** Simple rules applied everywhere make the whole codebase read as one style.
- **When:** Several people contribute to the same code and their habits differ.
- **Check:** Formatter settings are committed, and changed files pass the formatter unchanged.
- **Source:** ch. 6 § Chapter opening; ch. 6 § Team Rules

### CC-T75: Pin current behavior with tests before restructuring
Write tests that pin current behavior before restructuring code that lacks adequate tests.

- **Why:** Without them, nothing shows behavior survived each step.
- **When:** About to restructure code that lacks adequate tests.
- **Check:** Restructuring commits run tests that were written before the change began.
- **Source:** ch. 3 § A More Significant Example

### CC-T76: Evaluate generated code yourself before accepting it
Accept LLM-generated changes only after you can evaluate them yourself.

- **Why:** Responsibility for generated code stays with the person who accepts it.
- **When:** Using an LLM to write or improve code.
- **Check:** Generated changes come with tests covering the cases the reviewer examined.
- **Source:** ch. 2 § Postscript Conclusion

### CC-T77: Add abstractions only when a caller needs them
Add no extension point, option, or interface until a current caller uses it.

- **Why:** Unused room costs reading time and adds code with no caller.
- **When:** Someone proposes extension points or interfaces for features not yet planned.
- **Not when:** Growth is a confirmed business direction, or the odds of needing the hook are high.
- **Check:** Each extension point, option, or interface in a diff has a current caller.
- **Source:** ch. 3 § A More Significant Example; ch. 18 § YAGNI; ch. 20 § The Zone of Uselessness

### CC-T78: Hand-compute expected test values
Enter expected results as values worked out by hand, not by running the code.

- **Why:** A test reusing the code under test cannot catch its errors.
- **When:** Writing tests for a calculation or lookup that production code also performs.
- **Check:** Tests do not call the production lookup to compute expected values.
- **Source:** ch. 9 § Example

### CC-T79: Release files and sockets explicitly
Release files, sockets, and similar resources yourself instead of relying on garbage collection.

- **Why:** Garbage collection reclaims only memory, not files or sockets.
- **When:** Your code acquires an external resource.
- **Check:** Each resource acquisition in a diff has a matching close or release call.
- **Source:** ch. 8 § We Are Bad at This

### CC-T80: Delete comments that only restate the code
Delete a comment that repeats what the code beneath it already shows.

- **Why:** A comment adding nothing the code does not show still costs reading time.
- **When:** A comment is no more informative than the code beneath it.
- **Not when:** A comment that introduces an algorithm's overall idea helps readers, and public API doc comments stay (CC-T72).
- **Check:** A comment in a diff paraphrases the code it precedes.
- **Source:** ch. 5 § Redundant Comments
