# A Philosophy of Software Design — techniques

### POSD-T01: Measure complexity by the effort a change needs

Judge a design by how much work a small change takes, not by its size.

- **Why:** Small changes that take large effort reveal complexity that size and feature counts hide.
- **When:** Deciding whether a module or subsystem has become too complicated.
- **Check:** A small change in this area edits one module, or its description says why it needs more.
- **Source:** ch. 2 p. 18

### POSD-T02: Count reader difficulty as real complexity

Treat a reader's confusion as a complexity problem, even when the author finds the code clear.

- **Why:** Complexity is more apparent to readers than to writers, so the author's view understates it.
- **When:** A reviewer or teammate finds code hard that its author considers simple.
- **Check:** If a reviewer says code is hard to follow, the diff changes the code or adds a comment, not only the reply.
- **Source:** ch. 2 p. 18

### POSD-T03: Keep public interfaces much smaller than implementations

Make the public methods and types of any unit, from a class to a method, few and simple, and keep the hard work internal.

- **Why:** A small interface limits what every caller must learn, and the implementation can absorb the complexity.
- **When:** Designing the public surface of a class, subsystem, method, or service.
- **Check:** The change adds only the public methods and types a caller in this codebase needs.
- **Source:** ch. 4 p. 31

### POSD-T04: Remove pass-through methods that only forward calls

Delete or redistribute a method whose body only passes its arguments to another method.

- **Why:** Forwarding methods add an interface that teaches nothing and hides no decisions.
- **When:** A method's body is a single call with the same arguments.
- **Not when:** An external interface must stay unchanged, so the forwarding wrapper is right (POSD-T43).
- **Check:** No method body is only a call that forwards the same arguments, unless it keeps an external interface unchanged.
- **Source:** ch. 7 p. 62

### POSD-T05: Add interface elements only when they add functionality

Create a new class or public method only when it provides real functionality that callers need.

- **Why:** More interface elements increase what readers must learn, without making the module more useful.
- **When:** Adding a new method, parameter, or small class to an existing design.
- **Check:** Each new public method or class adds behavior beyond what existing methods provide.
- **Source:** ch. 4 p. 34

### POSD-T06: Keep each format or rule in one module

Place each data format, encoding rule, or parsing logic in one owning module, and treat the same knowledge spread across modules as a major red flag.

- **Why:** A design decision reflected in several modules must be changed in all of them.
- **When:** Two modules both need knowledge of the same format or rule.
- **Check:** The same format parsing or encoding logic does not appear in two or more files.
- **Source:** ch. 5, 9 p. 42

### POSD-T07: Find back-door leakage between classes

Look for shared knowledge that appears in no interface, such as a file format two classes both read, and move it into one owning module (POSD-T06).

- **Why:** Leakage through back doors stays invisible in interfaces, so the shared knowledge is easy to miss.
- **When:** Two classes work with the same format or protocol without either interface showing it.
- **Check:** Two classes that read the same file format or protocol do not both encode it, and the second one calls the owning module (POSD-T06).
- **Source:** ch. 5 p. 42

### POSD-T08: Let the allocating module release its resources

Make the module that allocates a memory block or handle also responsible for releasing it.

- **Why:** Each caller that must release a resource carries the ownership rule, and the module could handle that rule itself.
- **When:** An API returns memory or a handle that callers must release.
- **Check:** Each returned resource has no caller duty to release it, and a resource a caller must hold has a comment naming its releaser.
- **Source:** ch. 2, 13 p. 19

### POSD-T09: Provide defaults so common calls stay simple

Give each parameter a default that the common use needs, so typical callers pass nothing extra.

- **Why:** Most callers should not need knowledge that only rare cases require.
- **When:** Designing defaults and the main entry points of an API.
- **Not when:** The module can derive the value itself, so no key or parameter is exposed (POSD-T39).
- **Check:** Typical usage needs no extra objects, flags, or setup calls, and each configuration key has a default in code.
- **Source:** ch. 4, 8 p. 38

### POSD-T10: Redefine operations so some errors cannot occur

Change an operation's goal so that a state it already reaches counts as success, not as an error.

- **Why:** Simpler semantics mean fewer validation branches, and simpler code contains fewer bugs.
- **When:** A failure happens only because the requested state already holds.
- **Not when:** Callers that need to know about the special case must still be informed.
- **Check:** The operation returns success when its outcome already holds, with no error branch.
- **Source:** ch. 10 p. 91

### POSD-T11: Mask recoverable exceptions inside the module

Detect and recover from a low-level failure in the lowest layer, so higher layers never see it.

- **Why:** Recovering locally prevents each caller from repeating the same recovery logic.
- **When:** A failure such as packet loss can be recovered without caller input.
- **Not when:** Callers need the information, such as whether messages were lost or a peer actually failed.
- **Check:** The public interface declares no exception for conditions the module recovers from itself.
- **Source:** ch. 10 p. 93

### POSD-T12: Throw only for conditions callers can act on

Throw an exception only for conditions a caller can act on, and abort with diagnostics on conditions nothing can recover from.

- **Why:** Exception handling adds more complexity than its share of the code suggests, and each thrown exception joins the class interface.
- **When:** A value looks suspicious but may be harmless, or an unrecoverable failure such as out-of-memory occurs.
- **Not when:** Replicated systems must recover lost data rather than abort on an I/O error.
- **Check:** Each thrown exception has a documented caller response, and unrecoverable paths log and terminate.
- **Source:** ch. 10 p. 87

### POSD-T13: Sketch several radically different designs

Draft at least two radically different alternatives before committing to a major interface, data structure, or module split, and combine their strengths when none fits.

- **Why:** Even a design that seems obviously right has weaknesses that only a different alternative reveals.
- **When:** Starting a major new public interface, internal structure, or module split.
- **Check:** The PR description or design note lists at least two alternatives with different shapes and says which parts of the final design came from which.
- **Source:** ch. 11 p. 101

### POSD-T14: Compare alternatives by caller effort first

Rank interface alternatives first by how easily higher-level code can use them, then by simplicity, generality, and efficiency.

- **Why:** Higher-level code pays the cost of every interface, so ease of use for callers comes first.
- **When:** Comparing candidate interfaces for a module.
- **Check:** The PR description states, for each interface option, what a caller must write to use it.
- **Source:** ch. 11 p. 101

### POSD-T15: Document behavior callers depend on in interfaces

Document each public method's behavior, ordering, side effects, and constraints so callers can use it without reading the body.

- **Why:** Callers need behavior and usage rules that a method's signature cannot express.
- **When:** A public method has behavior, ordering, or constraints beyond what its types show.
- **Check:** Public method docs state call ordering, side effects, and units.
- **Source:** ch. 4, 12, 13 p. 32

### POSD-T16: Record design intent that code cannot express

Write comments that give the rationale for a design choice and the conditions for calling a method.

- **Why:** Intent and call conditions are lost to future readers when they live only in the code.
- **When:** A design decision or calling rule would otherwise be forgotten.
- **Check:** Non-obvious rationale and call conditions appear in comments next to the relevant code.
- **Source:** ch. 12, 13, 16 p. 105

### POSD-T17: Document units, bounds, and null meaning

State each variable's units, whether its bounds are inclusive, and what null means.

- **Why:** These facts are invisible in the code and cause errors when callers guess them.
- **When:** Declaring a field, parameter, or return value.
- **Check:** Field and parameter comments state units, bound inclusivity, and null meaning.
- **Source:** ch. 13 p. 113

### POSD-T18: Fix discovered design flaws instead of wrapping them

When a change exposes a design flaw, change its structure in the same change instead of wrapping it.

- **Why:** Small structural fixes made during changes stop complexity from accumulating.
- **When:** Modifying existing code and finding that its structure is flawed.
- **Not when:** A deadline blocks the fix, and then the cleanup is recorded as a follow-up (POSD-T19).
- **Check:** The diff changes the flawed structure instead of only wrapping it.
- **Source:** ch. 3 p. 26

### POSD-T19: Schedule cleanup within the same work

Plan cleanup as scheduled work with an owner, and reserve about 10 to 20 percent of development time for it.

- **Why:** Complexity is cheap to remove while it is small, and removing it later rarely changes much.
- **When:** Planning a sprint, a release, or a deadline-driven change.
- **Check:** Cleanup not done in this change is listed as a follow-up with an owner in the change description or tracker.
- **Source:** ch. 1, 2, 3, 16 p. 15

### POSD-T20: Unit-test error handlers and changed behavior

Write or update unit tests for each changed path, and start a bug fix with a test that fails without the fix.

- **Why:** Error handlers seldom execute, so their bugs stay hidden for a long time.
- **When:** Writing a handler for a rare condition, or changing any code path.
- **Check:** A bug-fix diff contains a regression test that fails without the fix, and a changed path has a test that covers it.
- **Source:** ch. 10, 19 p. 89

### POSD-T21: Write interface comments before the implementation

Write a class's interface comment and key public method signatures before writing their bodies.

- **Why:** Writing the comments first exposes design problems while changing them is still cheap.
- **When:** Starting a new class or a new public method.
- **Check:** A new class arrives with its signatures and interface comments, and method bodies may be stubbed while the interface is reviewed.
- **Source:** ch. 15 p. 140

### POSD-T22: Comment every class, method, and class variable

Give each class and method an interface comment, and each class variable a comment at its declaration.

- **Why:** Undocumented declarations force readers to read implementations to use them correctly.
- **When:** Adding a class, method, or class variable.
- **Not when:** Trivial getters and setters whose declaration already says everything a comment would add.
- **Check:** Each new class, public method, and class variable has a comment that adds at least one fact its declaration does not show.
- **Source:** ch. 13, 15 p. 112

### POSD-T23: Start each major block with a summarizing comment

Put a short summary comment at the narrowest block it describes, such as before each phase of a long method.

- **Why:** A block summary lets readers skip the detail and find the part they need.
- **When:** A method has several phases, or a loop whose purpose is not clear from its first lines.
- **Not when:** Short methods that do one thing are already described by their interface comment.
- **Check:** Each phase of such a method starts with a summary comment, and inline comments state intent or a reason, not the next line.
- **Source:** ch. 13, 16, 18 p. 125

### POSD-T24: Link dependent code sites to one shared note

Record a cross-module decision at the shared declaration, and add pointer comments at each dependent site.

- **Why:** A decision spread over several modules is easy to break when only one site is updated.
- **When:** A change requires coordinated edits in several modules that no single owner can hold, such as a new value other code must register.
- **Not when:** One module can own the decision, so it belongs there (POSD-T06). Otherwise a design notes file serves, though notes drift.
- **Check:** The shared declaration lists every place that must change, and each dependent site has a pointer.
- **Source:** ch. 2, 13, 16 p. 22

### POSD-T25: Give each identifier exactly one meaning

Use a separate name for each kind of value, and never reuse a name for a second purpose.

- **Why:** One identifier that holds two concepts forces readers to guess which meaning applies.
- **When:** Adding a variable where an existing name could be reused.
- **Check:** No identifier holds values for unrelated concepts within the same scope.
- **Source:** ch. 2, 14 p. 22

### POSD-T26: Name values by unit and counted items

Choose names that state the unit or the items counted, and name the specific quantity rather than a broad word.

- **Why:** Generic names hide units and counted items, so callers guess and make mistakes.
- **When:** Naming a number, time value, or counter.
- **Check:** Count names state the items counted, and time names state their unit.
- **Source:** ch. 2, 14 p. 22

### POSD-T27: Name parameters by their general role

Name each parameter for the role it plays for any value of its type, and check that a reader's guess from the name alone is right.

- **Why:** A role-based name keeps the parameter accurate for every caller, present and future.
- **When:** A method accepts any value of a type, not only the value currently selected.
- **Check:** The parameter name fits every existing call site.
- **Source:** ch. 14 p. 131

### POSD-T28: Return named types instead of generic containers

Define a specific named class or structure for a method that returns several related values.

- **Why:** Named types show readers what each value means, while generic pairs force readers to guess.
- **When:** A method must return several related values.
- **Not when:** The values are stored state that callers change separately, which POSD-T29 covers.
- **Check:** Return types are named types, not generic containers read through generic getters.
- **Source:** ch. 18 p. 159

### POSD-T29: Keep two related values in separate objects

Store two related values in separate objects when callers read and change each one on its own.

- **Why:** A flag inside one combined object exists only to say which value is which, and it adds confusion.
- **When:** Two related values are stored state that change together, but callers still need each one on its own.
- **Check:** No flag inside one object exists only to tell which of two combined values is which.
- **Source:** ch. 9 p. 81

### POSD-T30: Let the normal path handle empty states

Write the normal path so empty or absent states need no extra checks, and keep structure invariants that rule out excluded cases.

- **Why:** Each extra check for an empty state adds a branch that readers must follow.
- **When:** An edge case would otherwise add an if statement.
- **Not when:** The path is hot and has several rare conditions, and then POSD-T51 applies.
- **Check:** Code has no checks for empty or missing states the normal path could handle, and short results are documented as normal returns.
- **Source:** ch. 6, 13, 17 p. 59

### POSD-T31: Keep parallel code consistent in layout and naming

Follow the structure, ordering, and naming of similar existing code when adding new code.

- **Why:** Familiar patterns let readers predict behavior correctly without reading every part.
- **When:** Creating a file or making a design decision that similar code already made.
- **Not when:** A better convention is justified, and then every use is upgraded and the old convention removed completely.
- **Check:** A new file uses the same ordering, naming, and layout as its sibling files.
- **Source:** ch. 17, 18 p. 151

### POSD-T32: Keep one findable document of main conventions

Maintain one visible document of the project's main conventions, and link it from the contributor entry point.

- **Why:** Newcomers cannot follow conventions they cannot find.
- **When:** The change adds or changes a project convention.
- **Check:** The convention is written in the one conventions document, and the contributor entry point links to it.
- **Source:** ch. 17 p. 152

### POSD-T33: Refactor when a change outgrows the design

Restructure the affected design when a bug fix or feature no longer fits it, instead of adding a minimal patch.

- **Why:** Each patch in a messy area invites more patches, so the mess grows.
- **When:** A bug fix or feature conflicts with the current structure of the code, and a patch would sit beside the conflict.
- **Not when:** Deadlines or incompatible teams make the refactoring impractical, and then a nearly as clean alternative or a scheduled cleanup (POSD-T19) is used.
- **Check:** The diff restructures the affected code rather than adding special cases beside it.
- **Source:** ch. 3, 16 p. 25

### POSD-T34: Factor a repeated snippet into one shared method

Move a long repeated snippet into one method with a short signature, and call it from each site.

- **Why:** Near-identical repeated code signals a missing abstraction.
- **When:** The same multi-line snippet appears in several places.
- **Not when:** Very short snippets gain little, and snippets needing many arguments lose value.
- **Check:** The repeated snippet is written once, and call sites invoke a helper with a short signature.
- **Source:** ch. 9 p. 77

### POSD-T35: Split a method only when callers gain simplicity

Split a method only when the split makes the system simpler and each half reads on its own, never just because it is long.

- **Why:** A split whose halves must be read together adds shallow methods instead of removing complexity.
- **When:** Considering breaking up a long method or an overly broad one.
- **Not when:** Long methods with independent blocks and a simple signature can stay whole.
- **Check:** Each call site invokes exactly one new method, and no reviewer must open both halves to understand either.
- **Source:** ch. 4, 9 p. 37

### POSD-T36: Merge code that shares a format or message

Combine code into one module when its pieces read the same data format or need each other to be understood.

- **Why:** Splitting code that shares knowledge scatters the knowledge across files readers must track together.
- **When:** Two pieces of code read the same format or depend on each other.
- **Not when:** One-way use alone does not justify combining code.
- **Check:** The two pieces read the same data format, or each needs the other to be understood.
- **Source:** ch. 9 p. 76

### POSD-T37: Merge small classes that share leaked knowledge

Combine small classes that are closely tied to the same internal detail into one class that owns it.

- **Why:** One owner keeps the leaked knowledge out of several interfaces.
- **When:** The affected classes are small and closely tied to the leaked knowledge.
- **Not when:** Making one class hold the whole application goes too far.
- **Check:** Two small classes both reference the same internal detail.
- **Source:** ch. 5 p. 42

### POSD-T38: Hide choices that callers do not need

Keep rarely needed options and internal choices out of the common API, and expose them through separate, clearly marked methods.

- **Why:** Rare options in the common API force every caller to learn them.
- **When:** A feature is needed by only a few callers.
- **Not when:** A detail that callers must inspect to use a method correctly stays visible.
- **Check:** The common-use API does not mention the rarely used option.
- **Source:** ch. 4, 5, 6 p. 38

### POSD-T39: Expose tuning values only callers can choose

Make a setting visible only when callers know a better value than the module can derive from measurements or fixed logic.

- **Why:** Each exposed setting burdens callers with a decision, so exposing one must be justified.
- **When:** Considering a tunable value such as a cache size or retry interval.
- **Not when:** Users know domain priorities the module cannot see, such as which requests are time-critical.
- **Check:** Each configuration key is one the module could not derive from measurements or fixed logic.
- **Source:** ch. 5, 8, 21 p. 71

### POSD-T40: Prefer general insert and delete operations

Design text or content operations around general insert and delete at positions, not user-action names, in the units callers use (POSD-T55).

- **Why:** Action-named methods serve one caller and leave other callers to rebuild the same logic.
- **When:** Building a text or content API that UI code will use.
- **Check:** Insert and delete methods take general positions or ranges, not user-action names.
- **Source:** ch. 6, 7 p. 52

### POSD-T41: Keep feature-specific logic out of general classes

Keep feature-specific and user-interface behavior in top-level code, out of general-purpose and low-level classes.

- **Why:** Lower layers stay reusable when they hold only general operations.
- **When:** A lower-level or general class starts to hold feature-specific details.
- **Check:** Lower-level and general modules contain no names or behavior that belong to one feature or user action.
- **Source:** ch. 6, 8, 9 p. 56

### POSD-T42: Give several variants one shared interface

Put implementations of the same job behind one shared interface, and keep device-specific commands inside them.

- **Why:** Shared interfaces let developers learn one contract instead of one per variant.
- **When:** Several variants perform the same job, such as disk or network drivers.
- **Check:** Variant classes implement one shared interface and do not call each other, and device commands appear only in driver modules.
- **Source:** ch. 6, 7, 19 p. 56

### POSD-T43: Avoid decorators that only forward calls

Add a broadly useful feature to the base class, or build it standalone, instead of a decorator that forwards most calls unchanged.

- **Why:** A decorator that forwards most methods adds boilerplate and a layer without adding behavior.
- **When:** A new feature could be introduced as a decorator or wrapper.
- **Not when:** An external interface cannot change, so a decorator is right, and an existing decorator of the same object takes the feature.
- **Check:** A decorator forwards most of its methods unchanged to the wrapped object.
- **Source:** ch. 7 p. 65

### POSD-T44: Store shared settings in a context object

Gather system-wide settings into one context object, pass it to constructors, and add new settings as context fields.

- **Why:** Passing settings through every method adds parameters that intermediate layers only forward.
- **When:** System-wide settings are shared by many components.
- **Not when:** A context can become a grab-bag and cause thread-safety issues, so keep its variables immutable.
- **Check:** Shared settings are fields of one context object, and no method signature gains a settings parameter.
- **Source:** ch. 7 p. 67

### POSD-T45: Justify each design element by complexity removed

Add an interface element, argument, function, or class only when callers become simpler because of it.

- **Why:** A new element that only adds names to learn makes the design more complex, not less.
- **When:** Adding any new design element.
- **Check:** The new element has callers that become simpler, not only new names to learn.
- **Source:** ch. 7 p. 69

### POSD-T46: Design a needed abstraction cleanly and somewhat generally

When a feature first needs an abstraction, design its core operations together for several uses, adding no operation that no caller needs (POSD-T05).

- **Why:** Design effort spent early pays back when the module is later reused, and piecemeal interfaces accumulate gaps.
- **When:** A feature requires an abstraction that does not yet exist.
- **Not when:** Only quick working code matters, or the class is so general that current needs are hard to meet.
- **Check:** The first change's interface covers the core operations of the abstraction, designed together, with no unused extras.
- **Source:** ch. 6, 19, 22 p. 51

### POSD-T47: Build a strong test suite before restructuring

Strengthen the test suite and keep it passing before making major structural changes.

- **Why:** A passing suite shows that a restructuring preserved behavior.
- **When:** Planning a large structural change.
- **Check:** The structural change is accompanied by a passing existing test suite.
- **Source:** ch. 19 p. 164

### POSD-T48: Measure an operation before designing around its cost

Benchmark the operations a design depends on before designing around them, and back out a performance change that shows no measured gain.

- **Why:** Programmers' intuitions about performance are unreliable, so measurements decide.
- **When:** A design decision or performance change depends on the cost of an operation.
- **Not when:** The change also makes the system simpler.
- **Check:** A performance change cites its baseline and post-change measurements, and an unmeasured gain is backed out.
- **Source:** ch. 20 p. 169

### POSD-T49: Avoid per-item remote calls and allocations

Keep frequently executed code free of per-item network calls, disk access, and allocations, since these cost far more than computation.

- **Why:** Remote calls and allocations dominate the time that ordinary computation takes.
- **When:** A path runs often, such as once per item in a loop or once per request, or it performs I/O.
- **Not when:** The path runs rarely and does no I/O, and then the simpler code stays. Measure doubtful cases first (POSD-T48).
- **Check:** Frequently executed code avoids per-item remote calls, disk access, and allocations, and array elements are stored inline rather than as pointers.
- **Source:** ch. 20 p. 169

### POSD-T50: Pick the fundamental fix before tuning details

Change a data structure or algorithm before tuning constants, and redesign around the common case only when no fundamental fix exists.

- **Why:** A fundamental fix removes the work instead of making it slightly faster.
- **When:** Measurement has identified a slow component.
- **Not when:** No fundamental fix exists, and then the redesign around the common case should rarely be necessary.
- **Check:** The fix changes a data structure or algorithm, not only constants or micro-optimizations.
- **Source:** ch. 20 p. 171

### POSD-T51: Check special cases once at hot path start

Combine the rare special cases into one value, test it once at the start, and keep the common path free of further checks.

- **Why:** Repeated checks in the common path add work to every call.
- **When:** Writing a hot path with several rare conditions that the normal path cannot handle safely.
- **Not when:** Special cases matter less for speed, so structure them for simplicity.
- **Check:** The hot function begins with one guard, and rare cases branch to separate code.
- **Source:** ch. 20 p. 172

### POSD-T52: Keep private state private through its accessors

Give callers accessors for single values, and never return the internal collection or representation.

- **Why:** Private fields are hidden only if getters and setters do not expose their representation.
- **When:** Adding accessors to a class with private state that callers read or write.
- **Not when:** Private members still stop direct access from outside the class.
- **Check:** Getters and setters return or accept the internal representation or collection unchanged.
- **Source:** ch. 5 p. 41

### POSD-T53: Restore consistent state before reporting a failure

Before an operation reports a failure or continues after one, restore any partly changed state to a consistent form.

- **Why:** Otherwise callers act on half-updated data after the failure.
- **When:** An operation fails partway through modifying data structures.
- **Check:** Failure paths undo or complete partial updates before reporting upward.
- **Source:** ch. 10 p. 88

### POSD-T54: Scan the whole change before each commit

Scan every change in a commit before committing it, and confirm the documentation reflects each one.

- **Why:** Leftover debugging code and stale documentation survive unless someone checks the whole change.
- **When:** Before committing any change to revision control.
- **Check:** The diff contains no leftover debugging code and no unresolved TODO items it introduced.
- **Source:** ch. 16 p. 150

### POSD-T55: Expose operations at the unit callers use

Design operations around the units callers manipulate, so callers never split, join, or loop for one user operation. Position-based operations (POSD-T40) qualify when their positions use those units.

- **Why:** Callers that repeat the same manipulation for every operation duplicate that logic across the codebase.
- **When:** Designing an editing, collection, or text API that higher-level software uses.
- **Check:** Callers do not split, join, or loop over internal units to perform one user-level operation.
- **Source:** ch. 8, 11 p. 72

### POSD-T56: Document when and by whom event handlers run

State in each event handler's interface comment when it is invoked and which thread calls it.

- **Why:** Without that, a handler's trigger and calling thread stay unknown to readers.
- **When:** Writing a handler that an event module invokes indirectly.
- **Check:** Handler interface comments name the trigger and the calling thread.
- **Source:** ch. 18 p. 158

### POSD-T57: Add a usage example for required call sequences

Add a short usage example to the class comment of any class whose methods must be called in a particular pattern.

- **Why:** Callers who miss the required pattern may call methods in an order the class does not support.
- **When:** Callers must call several methods in a specific sequence.
- **Not when:** The example would only duplicate method comments in a simple class.
- **Check:** Multi-method classes with a required call sequence show that sequence in the class comment.
- **Source:** ch. 13 p. 123
