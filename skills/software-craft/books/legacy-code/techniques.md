# Working Effectively with Legacy Code — techniques

### WELC-T01: Run unit tests after each refactoring
Run the unit tests after every small refactoring step.

- **Why:** Mistakes surface within a minute, not at an overnight run.
- **When:** Refactoring code that already has tests.
- **Not when:** The code has no tests yet, so cover it first (WELC-P1).
- **Check:** Each refactoring commit has a test run recorded in its message or CI log.
- **Source:** ch. 2 p. 34

### WELC-T02: Test each new behaviour
Add a test case for each new behaviour in code that already has tests.

- **Why:** Each addition is covered as it lands.
- **When:** Adding behaviour to a tested area of legacy code.
- **Check:** The diff adds a test case for every new behaviour.
- **Source:** ch. 2 p. 34

### WELC-T03: Keep the unit test set fast
Keep unit tests fast, and move slow ones to a separate set.

- **Why:** Slow tests get skipped, which removes their feedback.
- **When:** Adding tests that pull in many collaborators or heavy setup.
- **Not when:** Database or file tests still belong in a separate set.
- **Check:** No test in the unit set takes as long as a tenth of a second.
- **Source:** ch. 2 p. 35

### WELC-T04: Test most logic below the UI
Write most unit tests against classes or functions, not screens or commands.

- **Why:** Such tests point a failure at one cause, not a whole screen.
- **When:** Deciding where tests for a feature should attach.
- **Check:** Most test files call classes or functions, not UI widgets or pages.
- **Source:** ch. 2 p. 33, 35, ch. 5 p. 71

### WELC-T05: Make the first dependency breaks conservative
Limit the first breaks to signature changes and new interfaces, and remove workarounds once tests cover the code.

- **Why:** Without tests, logic changes are the main risk.
- **When:** Breaking dependencies before the surrounding code has tests.
- **Check:** The first dependency-breaking commit changes signatures or adds interfaces only.
- **Source:** ch. 2 p. 40-41

### WELC-T06: Commit dependency breaks before their tests
Make the dependency-breaking commit first, then the commit that adds tests.

- **Why:** Dependency breaks exist to make the first tests possible.
- **When:** Getting a class or method into a test harness for the first time.
- **Check:** The dependency-breaking commit precedes the test commit for the same class.
- **Source:** ch. Introduction p. 22, ch. 25 p. 348

### WELC-T07: Fake a collaborator to record calls
Replace a collaborator with a fake that records the calls the class sends it.

- **Why:** Outgoing effects become readable, and such tests are real tests.
- **When:** The class's effects are visible only through a collaborator it calls.
- **Check:** The fake implements the collaborator's interface, and the test holds its concrete type.
- **Source:** ch. 3 p. 49-50, ch. 10 p. 166

### WELC-T08: Keep test fakes slim
Give each fake only the behaviour tests need, and store only the values they assert on.

- **Why:** Test fakes never run in production, so they may skip production rules.
- **When:** Writing a fake for a collaborator method that tests must observe.
- **Not when:** Production code constructs or calls the fake. Then use a real implementation or a seam (WELC-T05).
- **Check:** Fake classes sit in test sources, and production code never references them.
- **Source:** ch. 3 p. 48, ch. 9 p. 133

### WELC-T09: Wrap a global in a delegating member
Wrap a global function in a member with the same signature that forwards to it.

- **Why:** Tests override the member while production keeps the original global.
- **When:** A global call must be suppressed in tests but kept in production.
- **Check:** The production wrapper only forwards to the original global.
- **Source:** ch. 4 p. 55

### WELC-T10: Substitute preprocessor definitions in C
Define test-only macros or headers that replace the dependency in C or C++ test builds.

- **Why:** The swap happens without editing production call sites.
- **When:** A C or C++ call cannot be overridden any other way.
- **Not when:** Heavy preprocessing makes production code hard to maintain.
- **Check:** Test-only macros sit behind a define that production builds never set.
- **Source:** ch. 4 p. 58-59, ch. 19 p. 255

### WELC-T11: Use an existing mock library
Use a maintained mock library for the test doubles a test needs.

- **Why:** A maintained library is less code for the project to own.
- **When:** A test needs several mock objects for its dependencies.
- **Not when:** No mock library exists, so hand-write simple recording fakes (WELC-T07).
- **Check:** Test doubles come from a maintained library, not hand-copied classes.
- **Source:** ch. 3 p. 51, ch. 5 p. 70

### WELC-T12: Sprout a method for distinct logic
Write the new logic as its own method, test it, then enable its call in the legacy method.

- **Why:** The legacy method changes by one call, so the untested risk stays small.
- **When:** New logic is distinct, and its class builds in a test harness.
- **Not when:** The class cannot be built in a harness, so use WELC-T14.
- **Check:** A unit test targets the new method, and the legacy call is enabled afterward.
- **Source:** ch. 6 p. 82-85

### WELC-T13: Wrap a method to add behaviour
Rename the old method, then give its name to a wrapper that adds behaviour around its steps.

- **Why:** The original body stays unchanged, so the legacy method does not grow.
- **When:** Behaviour must run on every call and the legacy method cannot be tested yet.
- **Not when:** The code is simple, an extract-method tool gives better names, or behaviour interleaves with old steps.
- **Check:** The original method body is unchanged apart from its new name.
- **Source:** ch. 6 p. 91-93

### WELC-T14: Sprout a class for untestable code
Put the new behaviour in a new class, and let the legacy class create and call it.

- **Why:** The new rule gets its own tests, and the tangled class stays untouched.
- **When:** A class is too tangled to instantiate, but the change is small.
- **Not when:** The class can be built in a harness, so sprout a method instead (WELC-T12).
- **Check:** The legacy class only creates and calls the new class.
- **Source:** ch. 6 p. 86, 89

### WELC-T15: Build and test each class alone
Structure each class to compile and run its tests without unrelated modules.

- **Why:** Edit-to-test loops under about ten seconds keep each change cheap.
- **When:** Each change in a compiled project waits on long builds.
- **Not when:** Interpreted languages usually give near-instant feedback.
- **Check:** A class's test target compiles without unrelated production modules.
- **Source:** ch. 7 p. 101

### WELC-T16: Test a cluster through one entry point
Find one narrow entry point into the area, and test the cluster through it.

- **Why:** Breaking dependencies class by class is impractical across a large area.
- **When:** A large area of code is hard to test as a whole.
- **Check:** Tests target that entry point, not each class in the area.
- **Source:** ch. 7 p. 103

### WELC-T17: Put interfaces at volatile dependencies
Place an interface between a class and a dependency whose implementation changes often.

- **Why:** Implementation edits then do not force recompiles of the dependent class.
- **When:** A class depends on a concrete class whose implementation changes often.
- **Check:** The class's imports or includes name the interface, not the implementation.
- **Source:** ch. 7 p. 105, 107-108

### WELC-T18: Add features with test-driven development
Write a failing test, add a compiling stub, make the test pass, then remove duplication.

- **Why:** Each new behaviour is pinned by a test before its logic exists.
- **When:** Adding a new method or behaviour to code that can be tested.
- **Check:** Each new method has its test in the same change.
- **Source:** ch. 8 p. 111-112

### WELC-T19: Get the class under test first
Before a test-driven change to a legacy class, get at least one passing test.

- **Why:** Otherwise each feature is bolted on around untested code.
- **When:** Applying the test-driven cycle to a legacy class.
- **Check:** The class has a passing test before the new feature's test is added.
- **Source:** ch. 8 p. 110, 117

### WELC-T20: Add a variant by subclassing
Add the variant as a subclass that overrides only the method whose behaviour differs.

- **Why:** A single override gives a quick test, and a separate type avoids a flag.
- **When:** A class needs a variant and a quick passing test matters.
- **Not when:** Several variations must combine, or several subclasses each need the method (WELC-T21).
- **Check:** The new subclass overrides only the method that differs.
- **Source:** ch. 8 p. 118-120, ch. 20 p. 274

### WELC-T21: Make parent methods abstract instead of overriding
Declare the parent method abstract, and let each subclass implement it.

- **Why:** No subclass overrides a concrete body, so callers keep the parent's contract.
- **When:** Several subclasses each need a different version of the same method.
- **Not when:** A few concrete overrides are acceptable if they keep substitutability and call the parent.
- **Check:** The parent declares the method abstract, and no subclass overrides a concrete body.
- **Source:** ch. 8 p. 125-126

### WELC-T22: Use a cheap read-only real collaborator
Use the real collaborator in the test when it builds quickly and writes no data.

- **Why:** The test uses the object production uses, with no fake to keep in step.
- **When:** A constructor parameter is cheap to build and only reads a file.
- **Not when:** The collaborator writes data or takes long to build.
- **Check:** The test uses the real object for a read-only, file-based dependency.
- **Source:** ch. 9 p. 131

### WELC-T23: Override one problem method in a test subclass
Subclass the class in the test, overriding only the method that reaches the dependency.

- **Why:** The rest of the class runs unchanged, so the test runs real code.
- **When:** One method opens a connection or calls a resource tests must avoid.
- **Not when:** The overridden method is under test. Return empty results only if tests never check them.
- **Check:** The test subclass overrides only the method that reaches the dependency.
- **Source:** ch. 9 p. 135, 152, 158, ch. 25 p. 426

### WELC-T24: Stub a heavy method in tests
Give the heavy method an empty definition linked only by the test program, deleted once the class has tests.

- **Why:** Its real work never runs, so construction stays fast in tests.
- **When:** In a compiled language with a linker, a construction-time method does unneeded work.
- **Not when:** Other test files need the original. Use this only for the worst initial dependencies.
- **Check:** The test program links a stub body for that method instead of the original.
- **Source:** ch. 9 p. 152, ch. 25 p. 360-361

### WELC-T25: Replace a singleton through a static setter
Add a static setter that stores a test instance in place of the singleton.

- **Why:** Production code keeps normal access while tests supply a replacement.
- **When:** A singleton depends on external resources or lacks state-setup methods.
- **Not when:** Its public methods let tests set up all needed state.
- **Check:** The static setter is called only from test setup code.
- **Source:** ch. 9 p. 144, ch. 25 p. 395

### WELC-T26: Reset singletons between tests
Add a reset method to the singleton, and call it in setup and teardown.

- **Why:** Leftover singleton state would change the results of other tests.
- **When:** The singleton's public methods let tests set up any state they need.
- **Not when:** Its state depends on external resources, or one replacement serves every test.
- **Check:** Test setup and teardown both call the reset method.
- **Source:** ch. 9 p. 145, ch. 25 p. 398

### WELC-T27: Expose a private method as protected
Change one private method to protected, and reach it from a test subclass.

- **Why:** The test reaches the method without splitting the class yet.
- **When:** A method must be tested and splitting the class is not affordable now.
- **Not when:** First test through public callers. Avoid reflection, and move logic to its own class when affordable.
- **Check:** Only the method's access changed, and widened access is later narrowed.
- **Source:** ch. 10 p. 163

### WELC-T28: Make a stateless method static
Make a method static when it reads no instance fields and calls no instance methods.

- **Why:** Tests call it without building a hard-to-create instance.
- **When:** A method reads no instance fields, calls no instance methods, and needs direct tests.
- **Not when:** It reads instance state, a test subclass overrides it, or the language warns about static calls.
- **Check:** The static method body references no instance fields or methods.
- **Source:** ch. 4 p. 65, ch. 10 p. 160, ch. 25 p. 368

### WELC-T29: Override extracted methods in a subclass
Extract the calls to collaborators into methods, then override them in a test subclass.

- **Why:** Tests capture outward calls while the remaining logic runs for real.
- **When:** Extraction has isolated collaborators or components behind overridable methods.
- **Not when:** An existing method can be overridden directly, so nothing needs extracting.
- **Check:** The test subclass overrides the methods that touch collaborators.
- **Source:** ch. 10 p. 171, ch. 22 p. 319, ch. 25 p. 426

### WELC-T30: Skin and wrap a sealed library class
Extract an interface mirroring the library members you use, and write a wrapper that delegates to it.

- **Why:** Production code depends on a project interface tests can fake.
- **When:** Code needs a sealed or final library class that tests cannot fake.
- **Not when:** The library has interfaces, or the API is large, so split by responsibility instead.
- **Check:** Production code depends on the project's interface, and only the wrapper references the library.
- **Source:** ch. 10 p. 166, ch. 14 p. 220

### WELC-T31: Let the compiler find affected call sites
Change the declaration, fix each compiler error, then search by hand for shadowed and inherited uses.

- **Why:** The compiler finds every use that a text search could miss.
- **When:** A parameter type changes to a new interface or subclass.
- **Not when:** Slow builds make searching for uses more practical.
- **Check:** Changed declarations leave no compile errors when the change is committed.
- **Source:** ch. 10 p. 165, ch. 19 p. 263, ch. 23 p. 338

### WELC-T32: Trace callers, state, parameters, statics
For each changed method, list its callers, state, parameters, and statics, then follow callers to a system boundary.

- **Why:** Effects reach other code through these four paths.
- **When:** Starting effect analysis from a changed method.
- **Not when:** Callers that never reach the changed method need no tracing.
- **Check:** The commit message or PR lists each changed method's callers, fields, parameters, and statics.
- **Source:** ch. 11 p. 174-188

### WELC-T33: Start with higher-level group tests
Cover the group with one characterization test (WELC-T37) that enters through a public point.

- **Why:** One public entry point pins behaviour while the classes change.
- **When:** Covering a group of classes before breaking their dependencies.
- **Not when:** The class already has unit tests that enter it directly.
- **Check:** One characterization test exercises the cluster through a single public entry point.
- **Source:** ch. 12 p. 196-202

### WELC-T34: Test each change near its change point
Test each change at its own method, or at the nearest method whose results show its effect (a test point).

- **Why:** A nearby test points straight at the change, not a distant effect.
- **When:** Choosing where to write tests for a planned change.
- **Not when:** The change point is the test point, or a distant point is much easier to set up.
- **Check:** Each change has a test at its own method, and distant tests fail when the change is broken.
- **Source:** ch. 12 p. 201-204

### WELC-T35: Find a pinch point for every change
Choose a narrow pinch point all planned changes pass through, or two methods together if none exists.

- **Why:** One narrow test point covers many changes with fewer tests.
- **When:** Several classes have changes and need one place to test them.
- **Not when:** Only one change is planned, so test it at its own method (WELC-T34).
- **Check:** Tests at that point fail if any planned change is wrongly applied.
- **Source:** ch. 12 p. 203-204

### WELC-T36: Extract hidden classes from field clusters
Move methods and their only-used fields into a new class, leaving overriding methods and shadowing fields in place.

- **Why:** The cluster is a responsibility hiding inside the large class.
- **When:** A few fields are read or written only by a few methods.
- **Check:** The new class holds the fields that only its own methods reference.
- **Source:** ch. 12 p. 206, ch. 20 p. 273-275

### WELC-T37: Characterize actual behaviour with tests
Write tests that assert what the code does today, not what it should do.

- **Why:** Characterization tests record real behaviour, not a specification.
- **When:** Adding tests to legacy code with no specification to check against.
- **Check:** Expected values match today's output, often copied from a deliberately failing first run.
- **Source:** ch. 13 p. 209-211

### WELC-T38: Mark suspicious characterization results
Mark a surprising characterization test as suspicious, and link it to a follow-up.

- **Why:** A fix may change behaviour that deployed users already depend on.
- **When:** A characterization test shows behaviour that might be a bug.
- **Check:** The test carries a marker such as `// SUSPICIOUS: <reason> <follow-up ID>`.
- **Source:** ch. 13 p. 211-213

### WELC-T39: Use sensing variables for tangled logic
Add a flag that the tangled branch sets, then assert on it in tests of both states.

- **Why:** The flag shows whether tangled code runs when its effects are invisible.
- **When:** Tangled logic is unclear, or a nested condition is about to be extracted.
- **Check:** Test pairs assert the flag in both states, and the flag is removed when refactoring ends.
- **Source:** ch. 13 p. 217, ch. 22 p. 322-324

### WELC-T40: Test the branches the change will alter
Write tests that reach each branch whose lines the planned change will alter.

- **Why:** Branches the change touches carry the risk, so cover them first.
- **When:** A branch's code will change within the planned edit.
- **Not when:** The branch stays unchanged, where tests are optional.
- **Check:** Tests reach each branch whose lines appear in the diff.
- **Source:** ch. 13 p. 213-214

### WELC-T41: Test extreme and conversion inputs
Test minimum, maximum, and boundary inputs, plus one input per type conversion on the path.

- **Why:** Silent conversions such as truncation show only at particular values.
- **When:** Characterizing a wide input range, or extracting a conversion.
- **Check:** Inputs include minimum, maximum, and boundary values, and reach each conversion on the path.
- **Source:** ch. 13 p. 212-217

### WELC-T42: Peel core logic away from API calls
Move logic that does not call the service into classes that depend on an interface to it.

- **Why:** The logic can be tested with a fake service and no real messages.
- **When:** Most useful logic sits alongside library calls.
- **Not when:** Logic still using library data types cannot be fully freed.
- **Check:** Core logic classes import no library service classes.
- **Source:** ch. 15 p. 227

### WELC-T43: State the core computation before splitting
Describe a chunk's core computation in a sentence or two before splitting.

- **Why:** Naming the core job separates real work from input, output, and calls.
- **When:** A chunk of code mixes input, output, and real work.
- **Check:** Notes or comments state the core job of the chunk.
- **Source:** ch. 15 p. 226

### WELC-T44: Move pure logic out of call-heavy code
Move dependency-free computation into its own function, with a thin wrapper calling it and then the dependency.

- **Why:** The computation runs without the external call, so tests reach it easily.
- **When:** Writing a function whose logic sits right before an external call.
- **Not when:** Dependencies are too pervasive for thin wrappers.
- **Check:** Computation lives in a function that calls no external API.
- **Source:** ch. 19 p. 260-261, ch. 22 p. 317

### WELC-T45: Sprout a named method for new code
Put new code into a new, well-named method, not the body of a large method.

- **Why:** The large method gains a name, not more inline logic.
- **When:** A small addition belongs in a large class, and no separate class fits yet.
- **Not when:** The addition is a distinct sequence of steps (WELC-T12), or its class cannot be built in a harness (WELC-T14).
- **Check:** The diff adds a method whose name states the new responsibility.
- **Source:** ch. 20 p. 269

### WELC-T46: Extract MOVING copies from untested code
Copy each moved method to a MOVING-prefixed copy, point callers at it, then delete the original and rename it.

- **Why:** The original methods keep untested callers working during the move.
- **When:** Extracting a class from untested code with no refactoring tool.
- **Not when:** Tests can be put in place first, so extract the class then.
- **Check:** No MOVING-prefixed method names remain in the final diff.
- **Source:** ch. 20 p. 290-291

### WELC-T47: Extract a side group when modifying it
Extract a side group of methods into its own class when the next change touches it.

- **Why:** The extraction lands with real work, limiting the rework.
- **When:** A group of methods lies off to the side of the class's purpose.
- **Not when:** Every method name must be sorted into a new class.
- **Check:** The extracted class appears in a change that also modifies one of its methods.
- **Source:** ch. 20 p. 273

### WELC-T48: Delegate through client-specific interfaces
Give each client group an interface with only its methods, and delegate from a new client-facing class.

- **Why:** Each client then depends on a narrow subset, not the whole class.
- **When:** Clients use only some of a large class's methods.
- **Not when:** Clients lack tests, so changing them is risky.
- **Check:** The large class no longer declares the methods the new class holds.
- **Source:** ch. 20 p. 286-287

### WELC-T49: Name the main responsibility in one sentence
Describe a large class's primary responsibility in one sentence, then list its other duties.

- **Why:** One stated purpose shows which duties belong elsewhere.
- **When:** Deciding which responsibilities belong in a large class.
- **Not when:** Not one method per class, since methods can express responsibilities.
- **Check:** The class comment states one main purpose, and other duties are listed apart.
- **Source:** ch. 20 p. 269, 283

### WELC-T50: Remove duplication in small steps
Remove small duplicated fragments during feature work, running tests between steps.

- **Why:** Small removals keep each step safe and reveal larger duplication.
- **When:** Repeated similar code shows up while changing a system.
- **Check:** Feature diffs include small de-duplication edits, not one large rewrite.
- **Source:** ch. 21 p. 292-296

### WELC-T51: Extract differing steps of similar methods
Pull the differing steps of two similar methods into separate methods, then declare abstract hooks.

- **Why:** Once the bodies match, the shared code can move to one place.
- **When:** Two methods share a shape but differ in some steps.
- **Check:** The bodies differ only in calls, and the shared method moves up once it uses only shared data and hooks.
- **Source:** ch. 21 p. 298-301

### WELC-T52: Keep subclasses thin with a hook method
Leave each subclass with its constructor data and one overridden hook method.

- **Why:** Shared behaviour stays in the base class, and a variant adds only its hook.
- **When:** Subclasses differ only in one varying step after shared code moves up.
- **Check:** Each subclass holds a constructor and one overridden hook method.
- **Source:** ch. 21 p. 305, 308

### WELC-T53: Sprout instead of restructuring a monster
Add new behaviour in a sprouted method or class, called from one line of the long method.

- **Why:** The untested long method changes by a single call only.
- **When:** You must add behaviour to a long method you cannot yet test.
- **Check:** New logic lives in a separate method or class, called from one line.
- **Source:** ch. 22 p. 312-313

### WELC-T54: Let a tool extract methods, no hand edits
After tests cover side effects, make all extractions with a safe tool and no hand edits between steps.

- **Why:** The tool checks each extraction, and hand edits escape those checks.
- **When:** Breaking up a long method with an IDE or tool that extracts safely.
- **Not when:** The tool lacks extract-method support or changes behaviour, so edit by hand.
- **Check:** The commit message names the tool, and the diff has no hand edits between extractions.
- **Source:** ch. 5 p. 69-70, ch. 22 p. 317

### WELC-T55: Extract small chunks first
Extract chunks of two to five lines with clear names, and leave large blocks for later.

- **Why:** Few parameters and return values keep extractions safe before tests exist.
- **When:** Shrinking a monster method before any tests exist.
- **Check:** Early extractions are short methods whose names describe one clear action.
- **Source:** ch. 22 p. 324-329

### WELC-T56: Check hand-made extraction signatures
After a hand extraction, check each parameter and return type against its declaration.

- **Why:** A hand extraction can miss variables a tool would pass, and uncovered edits go unchecked.
- **When:** Extracting methods by hand while no tests cover the code.
- **Check:** Each signature passes every variable it needs, matches declared types, and hides no base-class name.
- **Source:** ch. 13 p. 218, ch. 22 p. 320-325

### WELC-T57: Move a monster method into a method object
Move the body into a class whose fields hold its parameters and locals, leaving one call behind.

- **Why:** The former locals become observable fields that tests can check.
- **When:** Locals would make useful sensing points.
- **Not when:** A sensing variable (WELC-T39) suffices, or a small method with no instance data should be static.
- **Check:** The new class holds the parameters and locals as fields, and a run method holds the body.
- **Source:** ch. 22 p. 327, ch. 25 p. 353-359

### WELC-T58: Skeletonize a method into control flow
Extract each condition and its body so the remaining method holds only control flow and calls.

- **Why:** The control structure becomes visible and can be refactored alone.
- **When:** The control structure needs its own refactoring once the logic is clearer.
- **Check:** The parent method holds only conditionals and calls to named methods.
- **Source:** ch. 22 p. 328

### WELC-T59: Pair when breaking dependencies
Flag each dependency-breaking edit for a second reader, and treat it as incomplete until checked.

- **Why:** Mistakes in dependency breaks can go unnoticed, so a second reader catches them.
- **When:** Making dependency-breaking edits to legacy code.
- **Check:** Review or pull-request records show a second person reviewed the change.
- **Source:** ch. 23 p. 340

### WELC-T60: Preserve method signatures when breaking dependencies
Copy the original parameter list into the extracted method and its call, except as WELC-T05 permits.

- **Why:** Matching signatures keep the untested change from altering its callers.
- **When:** Breaking dependencies on code that has no tests yet.
- **Check:** The extracted parameter names and types match the original list, except as WELC-T05 permits.
- **Source:** ch. 23 p. 336, ch. 25 p. 368

### WELC-T61: Extract an interface from a parameter's class
Extract an interface from the parameter's class, and have the method depend on it.

- **Why:** Tests can pass a fake without building the real class.
- **When:** A method parameter's type is hard to create or fake in tests.
- **Not when:** The parameter type is low-level or tied to one implementation technology.
- **Check:** The changed method's parameter is an interface type that tests fake.
- **Source:** ch. 9 p. 131, ch. 25 p. 349

### WELC-T62: Parameterize a constructor for hidden dependency
Move a dependency the constructor creates into a constructor parameter.

- **Why:** Tests can pass a fake instead of the resource built here.
- **When:** A constructor creates or takes a live resource that the test harness cannot create.
- **Not when:** The constructor builds many objects, so the parameter list grows long.
- **Check:** The constructor accepts the dependency as a parameter instead of creating it.
- **Source:** ch. 2 p. 38, ch. 9 p. 137-139, ch. 25 p. 402

### WELC-T63: Keep the old constructor as an overload
Keep the original constructor, and have it call the new one with the default collaborator.

- **Why:** Changing public signatures first would break many clients at once.
- **When:** A constructor gains a parameter but existing callers must keep working.
- **Not when:** Java and C# chain constructors directly. Elsewhere, move the body to an initialize method both call.
- **Check:** The original constructor's body contains a single call to the new one.
- **Source:** ch. 9 p. 138, ch. 25 p. 402

### WELC-T64: Encapsulate globals in a holder class
Move the globals into a new class, and reach them through one instance.

- **Why:** Globals that tests cannot control become members tests can replace.
- **When:** Code uses global arrays or variables that tests must control.
- **Check:** Globals become members of a new class, reached through one instance.
- **Source:** ch. 25 p. 362-364

### WELC-T65: Route a heavy-use global through a getter
Replace direct uses of a heavily used global with a protected getter.

- **Why:** A test subclass overrides one getter instead of every call.
- **When:** Several methods call the same global or static object.
- **Not when:** Only one call needs replacing, so use WELC-T29 instead.
- **Check:** The class references the global only in its getters.
- **Source:** ch. 25 p. 372, 422

### WELC-T66: Grow an empty interface from errors
Create an empty interface, switch its users to it, and add a method per compiler error.

- **Why:** The interface then declares only the methods the code actually calls.
- **When:** Extracting an interface from a class by hand.
- **Not when:** The design needs an interface that covers every public method.
- **Check:** Interface methods are added only in response to compile errors at the users.
- **Source:** ch. 25 p. 385-389

### WELC-T67: Replace free functions with an interface
Declare one virtual method per free function, and pass the implementation into the class.

- **Why:** Tests pass a fake through the interface instead of relinking the library.
- **When:** The same free functions are called from many methods and several classes.
- **Not when:** All calls sit in one method, so parameterize it by passing the dependency in.
- **Check:** The constructor accepts the interface type, and production passes the real implementation.
- **Source:** ch. 25 p. 365-367

### WELC-T68: Replace a C function with a function pointer
Rename the production function, declare a function pointer under its old name, and assign the function at startup.

- **Why:** The seam needs no build changes, unlike link substitution.
- **When:** Procedural code needs seams, and object or link substitution is impractical.
- **Not when:** The team regards function pointers as too unsafe to use.
- **Check:** The C code calls through a function pointer that startup code assigns.
- **Source:** ch. 25 p. 419-421

### WELC-T69: Push environment dependencies into a subclass
Make the class abstract and move environment-bound members to a subclass that tests override with empty bodies.

- **Why:** The base logic compiles and runs in a harness without the environment.
- **When:** Dependencies are spread through many methods of the class.
- **Not when:** Only a few calls reach the environment, so use WELC-T23 instead.
- **Check:** The original class is abstract, with dependency-heavy members in a subclass.
- **Source:** ch. 25 p. 415-417

### WELC-T70: Delegate static calls through an instance method
Add an instance method that delegates to the static call, and have the class use it via an object tests pass in.

- **Why:** Tests can substitute a fake object, which a static call does not permit.
- **When:** A class calls a static method hard to replace in tests.
- **Not when:** The static method has nothing that is hard to depend on in tests.
- **Check:** Callers use the new instance method, which alone calls the static method.
- **Source:** ch. 25 p. 392-393

### WELC-T71: Use a lazy getter for constructor-created objects
Replace a constructor-created field with a getter that creates the object on first use.

- **Why:** Tests can override the getter to return a fake object.
- **When:** In C++, an object is created only in a constructor and many methods use it.
- **Not when:** Only one method uses it, so override that call instead (WELC-T29).
- **Check:** Code reads the field only through the getter, constructors set it to null, and fakes are freed as production frees objects.
- **Source:** ch. 25 p. 375-377

### WELC-T73: Check for tests before calling legacy code
Before a change calls an existing method, check its tests, and write them first if none exist.

- **Why:** A changed call site otherwise rests on unchecked behaviour.
- **When:** Your change calls an existing method that has no tests.
- **Check:** Each legacy method that a changed call site uses has tests in the change.
- **Source:** ch. 13 p. 212

### WELC-T76: Override a factory method in a subclass
Move object creation out of the constructor into a factory method a testing subclass overrides.

- **Why:** Tests replace the object without changing the constructor's signature.
- **When:** A constructor creates an object that tests must replace or avoid.
- **Not when:** In C++, a constructor calls only the base version of a virtual factory method.
- **Check:** The constructor calls a factory method that the testing subclass overrides.
- **Source:** ch. 9 p. 139, ch. 25 p. 373-374, 429
