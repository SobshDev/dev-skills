# Refactoring — techniques

### REF-T01: Build a self-checking suite before restructuring

Build an automatic test suite for a section before restructuring it.

- **Why:** Automatic checks catch output changes that a manual review misses.
- **When:** About to restructure code without reliable tests.
- **Check:** Tests assert expected values automatically and cover the restructured code.
- **Source:** ch. 1, 2, 4

### REF-T02: Make new tests fail when behavior breaks

Confirm that each new test fails when its behavior is broken on purpose.

- **Why:** A test that cannot fail gives false confidence.
- **When:** Adding tests to code that already works.
- **Not when:** The judgment is subjective and cannot detect false confidence.
- **Check:** Commit or PR notes record a run where the new test failed after an injected fault.
- **Source:** ch. 4

### REF-T03: Pin legacy behavior with characterization tests

Find a seam in legacy code and pin its current behavior with a characterization test.

- **Why:** Untested legacy code cannot show whether a change altered its behavior.
- **When:** Changing legacy code with few or no automated tests.
- **Not when:** Creating a seam without tests is risky, and placeholder output must be confirmed correct.
- **Check:** Characterization tests pass on current code and fail when a fault is injected.
- **Source:** ch. 2, 4

### REF-T04: Write a failing test before fixing a bug

Write a unit test that exposes the reported bug and watch it fail before changing the code.

- **Why:** A failing test first proves the bug exists before any fix.
- **When:** A bug report arrives, or a feature is built test-first.
- **Check:** Bug-fix changes include a test that fails before the fix.
- **Source:** ch. 4

### REF-T05: Give each test its own fixture

Build each test's starting data in its own setup, sharing only immutable objects.

- **Why:** Shared mutable fixtures let one test distort another's result.
- **When:** Several tests need the same starting data.
- **Not when:** A slow fixture may be shared if a teardown resets it after each test.
- **Check:** Setup builds fresh mutable objects per test, except a slow fixture that a teardown resets.
- **Source:** ch. 4

### REF-T06: Test boundary inputs after ordinary cases

Write the ordinary cases first, then add empty, zero, negative and blank inputs.

- **Why:** Boundary inputs break assumptions that ordinary usage never exercises.
- **When:** Writing tests for collections, numeric inputs or setters fed by forms.
- **Check:** Tests exist for empty, zero, negative and blank inputs, and blank strings assert the result.
- **Source:** ch. 4

### REF-T07: Validate external input and assert internal conditions

Validate outside input with tested checks, and use assertions only for internal programmer errors.

- **Why:** Assertions expose program bugs, not bad outside data.
- **When:** Input arrives from users, files or another system.
- **Not when:** Trusted in-code calls may skip duplicate checks.
- **Check:** Input handlers have validation tests, and assertions guard only internal conditions.
- **Source:** ch. 4, 10

### REF-T08: State required conditions as assertions

Write an assertion for each condition the code assumes, and keep it after the bug that prompted it is fixed.

- **Why:** An assertion fails where a bad value enters and documents the assumed state.
- **When:** A section only works if some condition holds.
- **Not when:** Data from external sources needs real validation rather than assertions.
- **Check:** Assertion expressions hold no required assignments or state-changing calls.
- **Source:** ch. 3, 4, 10

### REF-T09: Take very small steps with tests after each

Take very small steps, run the tests after each, and follow a named refactoring's written steps in order.

- **Why:** A failure then points to a few changed lines.
- **When:** Performing any refactoring, especially one you have not done recently.
- **Check:** Commits or notes show each small edit followed by a passing test run.
- **Source:** ch. 1, 2, 4, 5, Preface

### REF-T10: Revert and retry in smaller steps

Revert to the last passing state and redo the change in smaller steps.

- **Why:** A known passing state is cheaper than debugging several unverified edits.
- **When:** A test breaks after a step you expected to be safe.
- **Check:** The working tree returns to the last passing state before a smaller retry.
- **Source:** ch. 1, 2, 5

### REF-T11: Commit each passing refactoring step

Commit each refactoring step once its tests pass, keeping the code runnable at every commit.

- **Why:** Each commit is a safe point where work can stop.
- **When:** Completing any refactoring step.
- **Check:** The commit log holds one passing, building commit per refactoring step.
- **Source:** ch. 1, 2

### REF-T12: Keep refactoring commits free of behavior changes

Keep restructuring commits free of behavior changes.

- **Why:** Switching between kinds of work keeps each change easy to judge.
- **When:** A change mixes restructuring with new behavior.
- **Check:** Refactoring-only commits contain no feature changes.
- **Source:** ch. 2

### REF-T13: Integrate with the mainline at least daily

Integrate your branch with the mainline at least once a day, pushing your result back.

- **Why:** Long-lived branches make restructuring conflict with the mainline.
- **When:** Working on any branch that will merge into the mainline.
- **Not when:** The project's documented policy allows longer-lived branches.
- **Check:** Feature branches merge at least daily. Compare each branch's age with its last merge.
- **Source:** ch. 2

### REF-T14: Let the IDE perform renames and signature changes

Use the IDE's refactoring commands for renames and signature changes, then run the tests.

- **Why:** Tools find every reference, while manual replace misses some.
- **When:** Renaming or changing parameters in a statically typed codebase.
- **Not when:** Without static typing, check matches by hand. Mature tools handle reflective calls well.
- **Check:** Renames come from IDE commands, related comments update, and tests run afterward.
- **Source:** ch. 2, 6

### REF-T15: Rename one identifier per step

Rename one identifier at a time, and keep a rename separate from a parameter change.

- **Why:** A failing test then points to exactly one rename.
- **When:** Several identifiers inside one function need new names.
- **Check:** Each rename commit changes exactly one identifier and no parameters.
- **Source:** ch. 1, 6, 9

### REF-T16: Encapsulate a widely used name before renaming it

Put accessor functions in front of a widely used field before renaming it.

- **Why:** The rename then happens behind accessors, not at every direct reference.
- **When:** The field is referenced from many functions or modules.
- **Not when:** Outside code needs a forwarder (REF-T18), or the record has limited scope.
- **Check:** Accessor functions exist in a commit before the rename commit.
- **Source:** ch. 6, 9

### REF-T17: Let old and new names coexist

Let the old and new names coexist, reading the new one first, until every caller has moved.

- **Why:** Callers move one at a time, so the code between steps keeps working.
- **When:** Callers, accessors or stored fields still use the old name.
- **Check:** The new name is read first, and a new field is added before the old one is removed.
- **Source:** ch. 2, 7, 9

### REF-T18: Keep a forwarder for renamed published functions

Keep the old declaration forwarding to the new name, and mark it deprecated.

- **Why:** Clients you do not control cannot be updated in the same change.
- **When:** Renaming a function that other teams or customers call.
- **Not when:** Callers you control can be updated together, and some interfaces must stay forever.
- **Check:** The old name carries a deprecation marker and is removed once no known caller uses it.
- **Source:** ch. 2, 6

### REF-T19: Name functions for intent, even for one call

Name each function after what it does, and extract even a single call when the new name is clearer.

- **Why:** Readers can skip the body and trust the name.
- **When:** A call or fragment has a purpose a clearer name would show.
- **Check:** Each new function name states a purpose rather than the steps it runs.
- **Source:** ch. 1, 6

### REF-T20: Rename a function when a better name appears

Rename a function, variable or field once you understand it better than its name suggests.

- **Why:** Names that no longer match the body mislead later readers.
- **When:** A name has confused you or no longer matches what the code does.
- **Check:** Each function name matches its body, and once callers move (REF-T17), no old name remains except a deprecated forwarder (REF-T18).
- **Source:** ch. 1, 3, 6

### REF-T22: Extract a fragment into a named function

Move a fragment that takes effort to read into a function named for its purpose.

- **Why:** The name records the fragment's purpose, so readers stop re-deriving it.
- **When:** A block needs effort to understand, or a comment introduces it.
- **Check:** Blocks that comments used to introduce appear as named function calls.
- **Source:** ch. 1, 3, 6

### REF-T23: Extract large loops and switch branches

Move a loop with its body, or a large switch branch, into a named function that does one task.

- **Why:** The loop or branch then reads as a single step.
- **When:** A loop or branch hides its purpose, or a comment flags it.
- **Check:** Such loops and branches in the diff appear as named calls.
- **Source:** ch. 3

### REF-T24: Extract complex conditions into named functions

Replace a hard-to-read condition and its branches with named function calls.

- **Why:** The condition's intent then shows at the point of decision.
- **When:** A conditional expression is hard to read.
- **Check:** Complex conditions in the diff are named function calls.
- **Source:** ch. 3, 10

### REF-T25: Confirm an extracted expression is side-effect free

Check that an expression has no side effects before moving it into a variable.

- **Why:** Moving a state-changing expression changes when and how often it runs.
- **When:** About to extract an expression into a new variable.
- **Check:** The new variable's initializer contains no assignments or state-changing calls.
- **Source:** ch. 6

### REF-T26: Declare extracted and split variables as immutable

Declare each variable created by an extraction or split as read-only.

- **Why:** A read-only declaration makes any later reassignment a visible error.
- **When:** A variable is created to name an expression or hold one purpose.
- **Check:** Such variables use a constant or read-only declaration.
- **Source:** ch. 6, 7, 9

### REF-T27: Replace a temporary variable with a query function

Compute a temporary's value in a query function and read the query wherever the temporary was used.

- **Why:** The value is computed from current data, with no stale copy.
- **When:** A temporary is computable, set in several places, or blocks a split.
- **Not when:** Snapshot variables stay variables. Top-level queries need many parameters.
- **Check:** The temporary is gone, and the query computes from the inputs the assignments used.
- **Source:** ch. 1, 7

### REF-T28: Keep value-returning functions free of side effects

Make a value-returning function avoid writes, sends and other state changes.

- **Why:** Callers can then call it freely without changing observable state.
- **When:** Writing or reviewing a function that returns a value.
- **Not when:** A strong default, not an absolute rule. Caching a query result is acceptable.
- **Check:** A value-returning function contains no writes, sends or state-changing calls, apart from caching.
- **Source:** ch. 3, 7, 8, 11

### REF-T29: Split functions that compute and change state

Move the pure calculation into a query and leave the state change in a separate modifier.

- **Why:** Separate queries and modifiers stay predictable and can be tested apart.
- **When:** A function both returns a value and causes observable side effects.
- **Check:** The query contains no writes, and the modifier returns nothing callers depend on.
- **Source:** ch. 3, 11

### REF-T30: Replace a stored derived variable with a query

List every assignment, add a query that computes the value, assert it matches, and switch readers to it.

- **Why:** A calculated value cannot go stale when its source data changes.
- **When:** The stored value can be recalculated from its source data.
- **Check:** No code reads the stored variable after the switch, and no assignments remain.
- **Source:** ch. 9

### REF-T31: Derive totals instead of storing them

Compute the total from its source records on read, after splitting out a non-zero initial value.

- **Why:** Adding a record then updates one place.
- **When:** A stored total must change with every update to its records.
- **Not when:** The source data is immutable, so the result can be immutable too.
- **Check:** The stored total is gone, and a test adds a record and asserts the computed total.
- **Source:** ch. 3, 9

### REF-T32: Split a loop that builds two unrelated results

Split a loop into one loop per result, so each updates only its own accumulator.

- **Why:** Each loop then has one purpose and can be tested alone.
- **When:** A single loop accumulates two different values in one pass.
- **Not when:** Profiling shows a real bottleneck, and side-effect-free duplicates may stay.
- **Check:** Each resulting loop updates only its own accumulator, with duplicated side effects removed.
- **Source:** ch. 1, 3, 8

### REF-T33: Replace loops with filter and map pipelines

Replace a filtering or mapping loop with filter and map calls, one behavior at a time.

- **Why:** A pipeline states what happens to each item without an accumulator.
- **When:** A loop filters or maps a collection in a language with first-class functions.
- **Not when:** The loop body has side effects or exits early.
- **Check:** Loops that only filter or map are replaced, with the collection in its own variable.
- **Source:** ch. 3, 8

### REF-T35: Split a variable that holds several purposes

Give each separate purpose of a reused variable its own variable, splitting in stages.

- **Why:** Readers must otherwise track which value the variable holds.
- **When:** A variable is assigned repeatedly for different responsibilities.
- **Not when:** A collecting variable that accumulates a running total is not split.
- **Check:** Each resulting variable is assigned in one place within the function.
- **Source:** ch. 3, 9

### REF-T36: Pass read-only locals in, return the change

When extracting, pass in the locals the code only reads and return the one variable it changes.

- **Why:** A single returned value keeps the extracted function's effects visible.
- **When:** Extracted code uses locals from the surrounding function.
- **Not when:** Two or more locals change, so simplify them first (REF-T35, REF-T27).
- **Check:** The new function takes read-only values as parameters and returns its changed value.
- **Source:** ch. 1, 6

### REF-T38: Replace similar copies with calls

After an extraction passes its tests, replace each identical or equivalent copy with a call.

- **Why:** Copies drift apart, so one fix would miss others.
- **When:** An extraction is complete, or a bug fix reveals the copies behind it.
- **Not when:** Near-copies that differ only in literals belong to REF-T39.
- **Check:** No copy of the extracted logic remains.
- **Source:** ch. 2, 6

### REF-T39: Parameterize a near-copy instead of copying it

Add a parameter for each literal that differs between near-identical functions, and pass it at every caller.

- **Why:** One parameterized function keeps shared logic in a single place.
- **When:** A function does almost what a new feature needs but has fixed values.
- **Not when:** Ordinary duplicates wait for a third similar case (REF-P4).
- **Check:** No copied function differs from its original only in literal values.
- **Source:** ch. 2, 11

### REF-T40: Slide related statements together before moving them

Move related statements toward each other one step at a time, and reorder side-effect-free statements freely.

- **Why:** Adjacent statements can then move as one block.
- **When:** Related statements are scattered among unrelated ones.
- **Not when:** A statement the move passes assigns data the fragment uses, or side effects are unclear.
- **Check:** Fragments are contiguous before extraction, and a breaking move is undone.
- **Source:** ch. 3, 8

### REF-T41: Inline a badly split group, then re-extract

Inline a badly split group of functions into one, then extract functions along better boundaries.

- **Why:** Boundaries drawn wrongly are hard to fix while the pieces stay separate.
- **When:** A group of functions mixes purposes and its boundaries need redesign.
- **Not when:** A small change needs only moving statements to callers.
- **Check:** Each new function serves one purpose its name states.
- **Source:** ch. 3, 6, 8

### REF-T42: Skip inlining overridden or recursive functions

Do not inline a method that is overridden, recursive, has several returns, or reads hidden fields.

- **Why:** Inlining changes which code runs when a subclass overrides or the function calls itself.
- **When:** Considering inlining a method with one of these properties.
- **Check:** The target body has a self-call, several returns, an overriding subclass, or reads hidden fields.
- **Source:** ch. 6

### REF-T44: Inline functions as clear as their names

Inline a function whose body reads as clearly as its name, removing the extra indirection.

- **Why:** Needless indirection makes calls hard to trace.
- **When:** A function is named just like its body, or a class wraps one function.
- **Check:** The diff deletes single-call wrapper functions and classes whose bodies are no clearer than their names.
- **Source:** ch. 3, 6

### REF-T45: Inline forwarding functions that add no logic

Replace calls to functions that only forward to another function with calls to the target.

- **Why:** Chains of pure forwarders make calls hard to trace.
- **When:** Every function in a chain merely forwards to the next.
- **Not when:** Overridden forwarders stay (REF-T42). REF-T49 or REF-T18 may keep a delegate.
- **Check:** Call chains contain no pure forwarding functions, that is, functions with no logic beyond forwarding.
- **Source:** ch. 3, 6

### REF-T46: Remove a middle man that mostly forwards calls

Let clients call the object that does the work, and remove the delegate accessor once unused.

- **Why:** Forwarding dominates, so the middle man adds coupling only.
- **When:** Most methods of a class only delegate to another class.
- **Not when:** Some delegation is good encapsulation.
- **Check:** Callers reach the working object directly, and no middle-man behavior remains.
- **Source:** ch. 3, 7

### REF-T48: Move a function to its data's module

Move a function into the module holding most of its data, after checking it neither overrides nor is overridden.

- **Why:** Data and the behavior that changes with it usually change together.
- **When:** A function makes many calls to another module's data or getters.
- **Not when:** Behavior varying independently of its data may fit Strategy or Visitor.
- **Check:** The function calls more members of another object than its own, and none overrides.
- **Source:** ch. 3, 8

### REF-T49: Move a function in copy-delegate-redirect steps

Copy the function to its new home, make the original delegate to it, then redirect callers one at a time.

- **Why:** The original keeps working until every caller reaches the new home.
- **When:** Relocating logic that depends on its surrounding context.
- **Not when:** The source function may stay indefinitely as a delegate.
- **Check:** Tests pass against the new home, and callers reach it directly.
- **Source:** ch. 1, 8

### REF-T51: Encapsulate a field before moving it

Route reads and writes of a field through accessor methods before moving it to another object.

- **Why:** Accessors make the field's readers and writers replaceable during the move.
- **When:** A field is about to move to another object.
- **Not when:** Routine self-use is a sign the class is too big, and bare records make the move trickier.
- **Check:** The field is read and written only through getter and setter methods.
- **Source:** ch. 6, 8

### REF-T54: Move repeated statements into the called function

Slide the repeated statements beside the call and move them in. With several callers, extract one call site first.

- **Why:** Removing duplication keeps the behavior in one place.
- **When:** Each call to a function is followed by the same statements.
- **Not when:** The repeated statements do not fit the called function.
- **Check:** Callers no longer repeat the statements, and the function body contains them.
- **Source:** ch. 8

### REF-T55: Move varying statements out to the callers

Move statements that vary between callers into those callers, and cut a simple first line into one or two callers.

- **Why:** The shared function then holds only the behavior all callers need.
- **When:** Common behavior must differ in some calls but not in others.
- **Check:** The shared function is identical for all callers, and varying code sits in callers.
- **Source:** ch. 8

### REF-T56: Replace hand-written code with an existing call

Replace hand-written code that does what an existing function does with a call to it.

- **Why:** One implementation then serves every use.
- **When:** Hand-written code duplicates an existing function or library call.
- **Not when:** The name reads poorly at the call site, or the similarity is coincidental.
- **Check:** The hand-written block is replaced by one call, and tests pass.
- **Source:** ch. 8

### REF-T57: Remove dead code instead of commenting it out

Delete unreachable code, search for callers first, and rely on version control to restore it.

- **Why:** Commented-out code confuses readers and goes stale.
- **When:** Code can no longer be reached, or only tests call it.
- **Not when:** Readers cannot see history and must know the code existed, so leave a one-line comment naming it.
- **Check:** No commented-out code remains, and only a one-line comment may name deleted code.
- **Source:** ch. 3, 8

### REF-T58: Replace type-code conditionals with subclasses

Replace a type-code switch with overriding subclasses, and client type checks with a superclass method.

- **Why:** Each type's behavior then lives in one place.
- **When:** Several functions switch on one type code, and behavior differs by type.
- **Not when:** Only one function uses the type field, no behavior varies (REF-T69), or the type changes during an object's life (REF-T70).
- **Check:** Type-code switches become overrides, and no client uses instanceof on a subclass.
- **Source:** ch. 1, 3, 10, 12

### REF-T59: Create subclasses and a factory before removing branches

Create a subclass per type and a factory that selects it, before removing the conditionals.

- **Why:** Callers then reach the subclasses through one selection point.
- **When:** Type conditionals are about to become polymorphic.
- **Not when:** Indirect inheritance may keep the selection logic in the constructor.
- **Check:** A factory selects each subclass from the type value, and callers use it.
- **Source:** ch. 1, 10, 11, 12

### REF-T60: Override each conditional leg in its subclass

Override each leg of the former switch in its own subclass, keeping the common calculation and default case in the base.

- **Why:** Keeping the shared rule in the base avoids copies in every override.
- **When:** Each subclass has its own type-specific behavior, or most types share one rule.
- **Not when:** The superclass should be abstract, so declare the method abstract.
- **Check:** Each subclass overrides one leg, the base holds the common rule, and no switch remains.
- **Source:** ch. 1, 10

### REF-T63: Make base methods throw when subclasses override

Make a base method throw an error naming the missing responsibility, when every subclass must provide it.

- **Why:** A forgotten override then fails at once.
- **When:** The base class defines a method that should never run directly.
- **Not when:** In a static language, declare an abstract member instead. A shared default belongs in the base (REF-T60).
- **Check:** The base method throws an error that names the missing responsibility.
- **Source:** ch. 1, 12

### REF-T65: Use guard clauses for unusual cases

Return early for an unusual case or pre-check, using a guard that negates the nested condition.

- **Why:** Unusual cases stop cluttering the normal path.
- **When:** One leg of a conditional is unusual or a pre-check.
- **Not when:** Both legs are normal, or a single exit point is clearer.
- **Check:** Unusual cases return at the top, guards have no outer not, and no result variable remains.
- **Source:** ch. 10

### REF-T66: Combine checks that lead to the same result

Move each assignment or state-changing call out of the conditions, then join checks with the same result.

- **Why:** One condition states the rule once.
- **When:** Several checks return the same value.
- **Not when:** Truly independent checks should not be merged.
- **Check:** Adjacent checks with identical returns become one condition, with no assignments in it.
- **Source:** ch. 10

### REF-T67: Replace a sentinel with a special-case object

Return a special-case object for a marker value, make it immutable, and give it methods for common responses.

- **Why:** Clients stop repeating checks for the marker.
- **When:** Many clients test for the same special value before doing the same thing.
- **Not when:** One client needs a different response, so it keeps an explicit check.
- **Check:** No client compares the marker, and nested properties return special cases, not null.
- **Source:** ch. 10

### REF-T68: Replace sentinel values in records with a transform

Add a transform that swaps sentinel values for special-case objects, and move clients over one at a time.

- **Why:** Clients stop repeating raw marker checks.
- **When:** Input arrives as plain records and no class holds the special case.
- **Check:** Transformed records contain no sentinel strings, and the old check stays while both forms reach a client.
- **Source:** ch. 10

### REF-T69: Subclass a type code only when behavior varies

Keep a plain type code unless behavior varies by type, then subclass it and move type behavior onto the type class.

- **Why:** Subclasses pay off only when types behave differently.
- **When:** Deciding whether a type code needs subclasses.
- **Not when:** No behavior varies by type, so the plain code stays.
- **Check:** Subclasses exist only where behavior varies, and type-specific formatting sits on its type class.
- **Source:** ch. 12

### REF-T70: Replace a subclass with a delegate when needed

Switch to delegation when behavior must vary on two axes or the variant changes at runtime.

- **Why:** Inheritance varies an object along only one axis.
- **When:** Behavior varies on two axes, the variant switches, or subclasses depend on parent internals.
- **Not when:** Starting with inheritance is fine until it causes problems.
- **Check:** Code swaps a live object's variant, or a second independent axis of variation appears.
- **Source:** ch. 3, 12

### REF-T71: Replace a refusing subclass with a delegate

Replace a subclass that inherits parent methods it does not support with a delegate.

- **Why:** The subclass should not inherit methods that make no sense for its role.
- **When:** A subclass refuses its superclass interface, and the confusion is real.
- **Not when:** Subclassing for reuse causes no confusion.
- **Check:** The former subclass no longer inherits interface methods it would refuse.
- **Source:** ch. 3, 12

### REF-T72: Forward superclass members, then drop the link

Write a forwarder for each superclass member the subclass uses, and remove the inheritance link last.

- **Why:** The link stays valid until every member is forwarded.
- **When:** Replacing a superclass with delegation.
- **Check:** Each group of forwarders is tested before the next, and getter and setter pairs only after both are forwarded.
- **Source:** ch. 12

### REF-T74: Move subclass methods one at a time

Move one subclass method at a time to the delegate, testing after each, and dispatch to the delegate when present.

- **Why:** Each step leaves the program working, and a failure points at one method.
- **When:** Converting a subclass into a delegate.
- **Not when:** A delegate override that calls super must not recurse, so extract the base calculation first.
- **Check:** Each commit moves one method, and the subclass is deleted once empty.
- **Source:** ch. 12

### REF-T75: Merge a subclass into its parent when alike

Merge a subclass and its parent that no longer differ enough to justify two classes.

- **Why:** A hierarchy with no real difference adds indirection.
- **When:** A class and its parent became similar through refactoring.
- **Not when:** Neither name fits well, so pick one arbitrarily.
- **Check:** The removed class has no members left, and the survivor's name fits all members.
- **Source:** ch. 3, 12

### REF-T76: Share one catalog item by reference

Link copies of a catalogue entry to one shared object instead of each copy holding its own data.

- **Why:** Updates reach every copy at once.
- **When:** Several objects hold copies of one catalogued item.
- **Not when:** A per-object component is enough when the data is never shared.
- **Check:** Each object reads one shared object for matching data and stores its own ID.
- **Source:** ch. 12

### REF-T77: Look up shared items through a repository

Retrieve each shared item by its identifier from a repository that holds one instance per entity.

- **Why:** One instance per entity keeps updates consistent for every caller.
- **When:** Objects must reference shared objects by identifier.
- **Not when:** The shared data never changes, so separate copies are reasonable.
- **Check:** Constructors take the item ID from the input record and no longer take arguments the item supplies.
- **Source:** ch. 9, 12

### REF-T78: Compare near-duplicate methods before pulling them up

Compare near-duplicate subclass methods, align them, and pull up the members they use first.

- **Why:** Small differences may hide behavior that tests do not cover.
- **When:** Subclass methods look alike but their bodies are not identical.
- **Check:** Methods that play the same role share one name and signature. Aligning means matching names and parameter order.
- **Source:** ch. 12

### REF-T80: Extract a superclass from shared data first

Pull shared fields up through a new superclass constructor, then move matching accessors and methods one at a time.

- **Why:** Shared data is the stable core, so methods follow it safely.
- **When:** Classes duplicate data and behavior, and inheritance unifies them more simply than delegation.
- **Not when:** Delegation fits shared behavior better, and classification can hint at inheritance.
- **Check:** The superclass constructor stores the shared fields, and subclasses drop matching accessors.
- **Source:** ch. 12

### REF-T81: Turn a complex function into a command object

Move a tangled function into a command class with one method, storing its arguments and locals as fields.

- **Why:** Shared fields let helper steps be split without passing locals.
- **When:** Locals and arguments tangle the function and block its extraction.
- **Not when:** Plain functions usually suffice. Split changing locals first (REF-T35, REF-T27).
- **Check:** The original function only creates the command and calls it, and the class is named after the function.
- **Source:** ch. 11

### REF-T82: Keep existing tests unchanged during refactoring

Leave existing tests unchanged unless an interface change forces the edit, and add tests for newly understood cases.

- **Why:** Editing tests to match refactored code removes the check that behavior held.
- **When:** Refactoring code that already has tests.
- **Not when:** An interface change forces the edit, or the refactoring reveals a missed case.
- **Check:** Existing test files change only where a signature changed.
- **Source:** ch. 2, 4

### REF-T83: Replace flag arguments with named functions

Replace a flag argument with one explicitly named function for each value it selects.

- **Why:** Named functions keep each behavior separate.
- **When:** A boolean, enum or string argument chooses between behaviors.
- **Not when:** The argument is computed at runtime, not a call-site literal.
- **Check:** Flag arguments are gone from signatures, and call sites use named functions.
- **Source:** ch. 3, 11

### REF-T84: Make value objects immutable with value equality

Set a value object's fields only at construction, and compare instances by their fields, not identity.

- **Why:** Fixed fields keep methods predictable, and identity equality breaks equal values.
- **When:** A class becomes a value object, or a fixed field is exposed to a setter.
- **Not when:** Callers update a shared reference object in place.
- **Check:** The class has no setters, and its equality and hash methods use every field.
- **Source:** ch. 9, 11

### REF-T85: Remove hooks and abstractions with no current caller

Delete hooks, special cases, abstract classes and delegation layers built for needs no code currently has.

- **Why:** Speculative machinery adds structure with no present use.
- **When:** Code adds a hook or abstract class for a need no caller has.
- **Check:** Every hook, special case and abstract class in the diff has a current caller.
- **Source:** ch. 3

### REF-T86: Copy data before changing or exposing it

Copy a collection or record before changing it, and return copies from getters of mutable data.

- **Why:** A change to shared data reaches every reader.
- **When:** Code changes data it did not create, or a getter exposes mutable data.
- **Not when:** Callers that change shared data on purpose break, so tests must catch them.
- **Check:** In-place sorts and added fields run on a copy, and mutable getters return a clone.
- **Source:** ch. 1, 6, 7

### REF-T87: Measure before tuning for speed

Measure with a profiler before changing code for speed, and tune only after the structure is clean.

- **Why:** Changing code that is not the hot spot harms readability for no gain.
- **When:** Someone suspects the code is slow.
- **Not when:** A significant slowdown may justify reversing a refactoring.
- **Check:** Performance changes cite profiler output and sit in their own commits.
- **Source:** ch. 1, 2

### REF-T88: Restructure just before adding a feature

Restructure the code a feature touches just before adding the feature.

- **Why:** Forcing a feature into an unsuitable structure makes the code harder to change.
- **When:** Existing code almost fits a new feature but needs structural changes first.
- **Not when:** A very small feature does not justify large restructuring, but preparatory changes still belong.
- **Check:** A structural change lands before the feature change.
- **Source:** ch. 2
