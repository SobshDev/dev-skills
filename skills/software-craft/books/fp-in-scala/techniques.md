# Functional Programming in Scala — techniques

### FPS-T01: Keep computing functions free of effects
Move console, file, network and service calls out of the computing function, and call them from a thin function that only performs effects.

- **Why:** The book says pure logic can be reasoned about on its own, without the outside world.
- **When:** A function both computes a value and prints, reads, writes or calls a service.
- **Check:** The computing function's body has no console, file, network or service calls.
- **Source:** ch. 13

### FPS-T02: Return a description of the effect
Have logic return a value that describes the external action, and let a single place perform it.

- **Why:** The book says the description can be tested before anything runs.
- **When:** Logic must trigger an external action but should stay pure and testable.
- **Check:** Only the interpreter or outer entry code calls side-effecting methods.
- **Source:** ch. 1, 13

### FPS-T03: Pass external collaborators as parameters
Pass a service such as a payment client into a function as an argument instead of constructing it inside.

- **Why:** The book says the function can then run in tests without contacting the real service.
- **When:** A function depends on an external service that tests should not contact.
- **Not when:** Test doubles of the passed interface are awkward to write, as the book notes.
- **Check:** The service appears in the function signature, and the body does not construct the client.
- **Source:** ch. 1

### FPS-T04: Take every input through parameters
Pass each value a function needs as an argument rather than reading a field of its enclosing object, a global or an environment value.

- **Why:** The result then depends only on the arguments, so a call can be replaced by its value.
- **When:** A function would otherwise read hidden state such as a field, a global or the environment.
- **Check:** The body reads no field, global or environment value missing from the parameter list.
- **Source:** ch. 1

### FPS-T05: Name intermediate values with val
Bind each intermediate result with val, and use var only where FPS-T06 allows.

- **Why:** A val cannot be reassigned, so a reader never has to track a changing value.
- **When:** A block needs a name for a value that it uses more than once.
- **Check:** New bindings in the diff use val. A var appears only inside one function and is never returned, stored or captured, as FPS-T06 allows.
- **Source:** ch. 2

### FPS-T06: Keep mutation inside a function's locals
Use a mutable local variable only when no code outside the function can observe it.

- **Why:** The caller still sees a pure result, so the function stays referentially transparent.
- **When:** A function needs scratch state during its own computation.
- **Not when:** A pure version is at least as easy to get right, and a traversal that carries a counter uses FPS-T55 instead.
- **Check:** The mutable variable is declared inside the function and never returned, stored or captured.
- **Source:** ch. 1, 14

### FPS-T07: Write loops as tail-recursive helpers
Write iteration as a local recursive function that carries the loop state in its arguments, and annotate it with tailrec.

- **Why:** Tail calls compile to a loop, so large inputs do not overflow the call stack.
- **When:** An iteration updates state, no library method fits (FPS-T16), and the code must avoid mutating a loop variable.
- **Not when:** The repetition is not a tail call and overflows the stack on large input. Then FPS-T47 applies.
- **Check:** The recursive call is the last expression, each intended loop has tailrec, and no while loop appears unless FPS-T47 applies.
- **Source:** ch. 2

### FPS-T08: Generalize near-identical functions with a parameter
Replace two near-identical functions with one that takes the varying operation as a function parameter.

- **Why:** One generic function keeps the shared logic in a single place.
- **When:** Functions differ only in the operation applied to their input or elements.
- **Check:** The varying operation is a parameter of a function type, and no duplicated body remains.
- **Source:** ch. 2, 3

### FPS-T09: Add type parameters to type-independent functions
Add a bracketed type parameter to a function whose logic is identical for every element type.

- **Why:** The same logic then exists once, instead of once per element type.
- **When:** Several functions share one structure and differ only in their element type.
- **Check:** Per-type copies of one function become a single function with a type parameter.
- **Source:** ch. 2

### FPS-T10: Build one-argument functions by partial application
Create a one-argument function by supplying the first argument of an existing two-argument function.

- **Why:** The original definition is reused, so the new function cannot drift from it.
- **When:** A caller has one argument ready and needs a function for the remaining one.
- **Not when:** The task is to write the combining function itself, as in a learning exercise.
- **Check:** The new function is defined in terms of the original function, not rewritten.
- **Source:** ch. 2

### FPS-T11: Model fixed alternatives as a sealed trait
Declare a sealed trait with one case class or case object per alternative, all in the same file.

- **Why:** The book uses ADTs where the set of cases is closed and known to be fixed.
- **When:** A data type can take only a known, fixed set of forms.
- **Not when:** The set of forms is open or expected to grow over time.
- **Check:** Every alternative extends the sealed trait and is declared in the same file.
- **Source:** ch. 3

### FPS-T12: Match ADT cases from specific to general
Order the cases of a match from the most specific pattern to the most general, and cover each constructor.

- **Why:** The first matching case wins, so a general case placed first hides the specific ones.
- **When:** Several patterns in one match could match the same value.
- **Check:** A catch-all pattern appears last, and each match lists the data constructors it handles.
- **Source:** ch. 3

### FPS-T13: Reuse an immutable list tail
Build a new list by pointing it at an existing immutable tail instead of copying that tail.

- **Why:** Lists are immutable, so the shared tail can be reused without a copy.
- **When:** Adding to the front of a list or removing its first element.
- **Not when:** The change is at the end of the list, where a List copies every earlier cell. Vector fits better.
- **Check:** The new value references the existing list, and no full copy is made.
- **Source:** ch. 3

### FPS-T14: Generalize duplicated recursion into a fold
Turn the base value and combining operation of two similar recursive list functions into parameters of one fold.

- **Why:** The shared traversal structure is written once instead of in each function.
- **When:** Two recursive list functions share a structure and differ only in base value and operator.
- **Check:** Duplicated recursive list functions become one fold call with different arguments.
- **Source:** ch. 3

### FPS-T15: Use foldLeft for large inputs
Reduce a potentially large list with a tail-recursive foldLeft rather than a recursive foldRight.

- **Why:** A foldRight is not stack-safe, so long lists can overflow the stack.
- **When:** Reducing a list of unbounded length on one thread, without parallel combining.
- **Check:** Large-input list reductions call foldLeft, and foldRight appears only on bounded lists or in the stream searches of FPS-T31.
- **Source:** ch. 3

### FPS-T16: Check library list methods before writing recursion
Look for an existing standard library list method, such as take, forall or exists, before writing an explicit recursive function.

- **Why:** The standard library may already provide the operation, so checking first avoids new recursion.
- **When:** You need a list operation that may already exist in the standard library.
- **Check:** New list recursion is reviewed against the List methods for an existing equivalent.
- **Source:** ch. 3

### FPS-T17: Express transforms with map, filter and flatMap
Write element-wise changes with map, conditional selection with filter, and one-to-many expansion with flatMap.

- **Why:** Each standard operation names its purpose, so the code needs no hand-written recursion.
- **When:** Transforming each element, keeping matching elements, or expanding each element into several.
- **Check:** Element-wise transforms are map calls, selections are filter calls, and expansions are flatMap calls.
- **Source:** ch. 3

### FPS-T18: Use one fold for tree recursion
Define size, maximum, depth and map on a tree through a single fold over its Leaf and Branch cases.

- **Why:** Defining everything through one fold keeps the traversal logic in a single definition.
- **When:** Several recursive tree functions share the same traversal structure.
- **Check:** Tree functions are defined through a single fold over the Leaf and Branch cases.
- **Source:** ch. 3

### FPS-T19: Reserve exceptions for unrecoverable failures
Throw an exception only when no reasonable caller could recover, and return a value for every recoverable case.

- **Why:** Some callers may recover, so they need a value they can handle.
- **When:** Deciding how to report a failure that callers cannot handle usefully.
- **Not when:** Some callers may recover, so return Option or Either instead.
- **Check:** Thrown exceptions appear only where recovery is impossible, and recoverable cases return values.
- **Source:** ch. 4

### FPS-T20: Return Option for partial functions
Return Option from a function that is undefined for some inputs, such as an empty list, so every input yields a value of the declared type.

- **Why:** The type then shows the missing case, so no path needs to throw.
- **When:** A function is undefined for some inputs that its parameter types allow.
- **Check:** Partial function signatures return Option, and no path throws for missing input.
- **Source:** ch. 4

### FPS-T21: Chain Option steps with map and flatMap
Use map for steps that return a plain value and flatMap for steps that return an Option.

- **Why:** Each step runs only if the previous one produced a value, so no nested matches are needed.
- **When:** Dependent steps may each produce no value.
- **Check:** Steps that return Option are chained with flatMap, and the chain ends with getOrElse (FPS-T22) or one match on the final result.
- **Source:** ch. 4

### FPS-T22: Resolve Option with getOrElse at the end
Convert an Option to a plain value with getOrElse once the chain is complete.

- **Why:** The fallback is applied once, at the end, instead of at each intermediate step.
- **When:** A default value is an acceptable outcome when the value is absent.
- **Not when:** The absence must be reported with its reason. Return Either instead (FPS-T25).
- **Check:** getOrElse appears once, at the end of an Option chain, with a fallback value.
- **Source:** ch. 4

### FPS-T23: Combine independent Options with map2
Combine two independent Option values with a binary function that yields None when either input is None.

- **Why:** The combination needs no nested matches, and any missing input yields None.
- **When:** Two independent optional values feed one computation.
- **Check:** Two optional inputs are combined with map2, not nested matches, nested flatMap or a for-comprehension over independent values (FPS-T51).
- **Source:** ch. 4

### FPS-T24: Pass a costly fallback by name
Declare a fallback parameter with a by-name type, so it is evaluated only when the body needs it.

- **Why:** A costly or failing default is then never computed when the caller does not need it.
- **When:** A default is costly to compute, or it can throw when it is not needed.
- **Check:** A fallback parameter that may go unused has a by-name type, such as => B, and the body evaluates it only when needed.
- **Source:** ch. 4, 5

### FPS-T25: Return Either when callers need failure reasons
Use Either with Left for the failure and Right for success, and put a caught exception inside Left.

- **Why:** Typed failure values let callers branch on each kind of failure.
- **When:** Callers must know what went wrong, not only that something did.
- **Not when:** Knowing that a failure occurred is enough, in which case Option is simpler.
- **Check:** Failure types carry a message or exception, and catch clauses return Left with the exception.
- **Source:** ch. 4

### FPS-T26: Validate domain values in Either constructors
Create domain values through constructor functions that return Either and reject invalid input.

- **Why:** Invalid values are rejected at the boundary, before the rest of the code can use them.
- **When:** Building domain values from unchecked input, such as user data.
- **Check:** Domain values built from unchecked input come only from the Either-returning function, not from a direct call to the case class constructor.
- **Source:** ch. 4

### FPS-T27: Stop Either sequencing at the first error
Use sequence and traverse on Either so they return the first Left they encounter.

- **Why:** Once one step has failed, the remaining steps cannot change the outcome.
- **When:** Several Either results are combined, and the first error is enough.
- **Check:** Sequence and traverse on Either stop at the first Left.
- **Source:** ch. 4

### FPS-T28: Collect all validation errors with applicative
Validate independent fields with map3 over an applicative, a type built from map2 and unit, whose errors accumulate instead of stopping at the first (FPS-T27).

- **Why:** The user sees all the problems at once, not one error per attempt.
- **When:** Validating a form whose fields do not depend on each other.
- **Not when:** Later checks need values produced by earlier checks.
- **Check:** Validation returns the errors from all failing fields, not just the first, and map2 over Either alone is not used for it.
- **Source:** ch. 4, 12

### FPS-T29: Cache by-name arguments in a lazy val
Bind a by-name argument to a lazy val before the body uses it more than once.

- **Why:** A by-name argument is recomputed on every use, and a lazy val evaluates it once.
- **When:** A by-name argument is costly to compute and the function refers to it repeatedly.
- **Check:** Functions that use a costly by-name parameter several times assign it to a lazy val first.
- **Source:** ch. 5

### FPS-T30: Memoize stream cells through a smart constructor
Create stream cells through one helper that stores the by-name head and tail in lazy vals.

- **Why:** Each cell's head and tail are computed at most once, so a stream never repeats work.
- **When:** Defining a lazy stream whose cells take by-name head and tail arguments.
- **Check:** Stream cells are created by one lowercase helper beside the capitalized case class, not by calling the case class directly with thunks.
- **Source:** ch. 5

### FPS-T31: Write stream searches with a lazy foldRight
Write exists and forAll with foldRight, passing a combining function whose second parameter is by-name.

- **Why:** The fold stops reading the stream as soon as the answer is decided.
- **When:** Searching a stream for a matching element or checking that every element matches.
- **Not when:** The stream may be long with no match, since this form can then overflow the stack.
- **Check:** Stream predicate methods call foldRight with a combining function whose second parameter is by-name.
- **Source:** ch. 5

### FPS-T32: Generate streams with unfold
Generate a stream by passing an initial state and a step function that returns an Option of an element and the next state to unfold.

- **Why:** The generator stays productive, so consumers take only the elements they demand.
- **When:** A stream repeats a rule that advances an explicit state, such as a counter.
- **Check:** Generators call unfold with an initial state and a step returning Option. Each step is bounded, and no logic relies on shared cells.
- **Source:** ch. 5

### FPS-T33: Pass each returned state into the next call
Feed the state returned by one call into the next call, and return the new state with each result instead of updating state as a side effect.

- **Why:** The state stays explicit, so each call is referentially transparent and repeatable.
- **When:** Calling a pure stateful function several times in a row.
- **Not when:** Steps inside one stateful procedure use FPS-T36 instead.
- **Check:** Successive calls take the state from the previous result, and stateful API methods return a result with the next state.
- **Source:** ch. 6

### FPS-T34: Retry draws that land in the biased range
Redraw a random non-negative integer when it falls above the largest multiple of n, where n is the size of the target range, and only then take the remainder.

- **Why:** Without the redraw, the remainder maps some results from more raw draws, which biases the outcome.
- **When:** Mapping a random non-negative integer into a range using the remainder operator.
- **Check:** Range-limited generators compare the draw against the largest multiple of n and retry above it.
- **Source:** ch. 6

### FPS-T35: Combine state actions with map, map2 and flatMap
Build state actions from map for one result, map2 for two independent results, and flatMap for a later step that depends on an earlier result.

- **Why:** The state passing is written once in these combinators, not in each generator.
- **When:** A value needs results from generators, which are independent or dependent on one another.
- **Check:** Derived generators call map, map2 or flatMap rather than threading state by hand.
- **Source:** ch. 6

### FPS-T36: Write stateful logic with get, set and modify
Write a stateful procedure as a for-comprehension over get, set and modify of a State type (a wrapper of a state-to-result function), not with state arguments.

- **Why:** The procedure reads like an imperative sequence while keeping its state pure.
- **When:** A stateful procedure reads and updates state in several steps.
- **Check:** Stateful code calls get, set or modify inside a for-comprehension rather than taking state arguments.
- **Source:** ch. 6

### FPS-T37: Model a state machine as pure transitions
Model a state machine as a pure function from its current state and an input to a new state and an output.

- **Why:** Each transition returns its next state and output without mutation, so behavior follows from the inputs alone.
- **When:** Designing logic driven by a sequence of inputs, such as a candy dispenser.
- **Check:** Machine logic takes the inputs and returns the final state and results without mutation.
- **Source:** ch. 6

### FPS-T38: Define lazyUnit as fork over unit
Define lazyUnit(a) as fork(unit(a)), where unit wraps a value and fork delays a computation and runs it concurrently.

- **Why:** The constructor then uses only the public primitives, not the representation details.
- **When:** You need a constructor that delays its argument and runs it concurrently.
- **Check:** lazyUnit is written as fork(unit(a)) and uses no representation details.
- **Source:** ch. 7

### FPS-T39: Combine parallel results with map2
Merge two independent parallel results with a map2 combinator that takes a binary function.

- **Why:** The merge is expressed through the library's own type, so no thread handling leaks into callers.
- **When:** Two independent parallel computations must be merged into one result.
- **Check:** Merging code calls a map2-style combinator that takes a function, not a hand-written join.
- **Source:** ch. 7

### FPS-T40: Avoid blocking on tasks in the same pool
Do not have a pool task submit another task to the same pool and block on its result.

- **Why:** On a bounded pool, every thread can end up waiting, so the program deadlocks.
- **When:** Forking work on a bounded thread pool where tasks depend on other tasks.
- **Not when:** Pools that grow without bound avoid this deadlock.
- **Check:** No task body calls a blocking get on a future it submitted to the same executor.
- **Source:** ch. 7

### FPS-T41: Return futures and leave waiting to callers
Have run return a future, so each caller decides how long to wait or whether to cancel.

- **Why:** The waiting policy belongs to the caller, not to the parallel library.
- **When:** Designing the run function for a deferred parallel computation.
- **Check:** run returns a future, timeout or cancellation decisions appear at call sites, and callback failures reach the run caller.
- **Source:** ch. 7

### FPS-T42: Catch exceptions and report them as failures
Wrap user code evaluated during a property check, a test over generated inputs, in an exception handler that returns a failure naming the input.

- **Why:** One thrown exception then reads as a reported failure, not as a crash of the whole run.
- **When:** Evaluating a property whose predicate can throw an exception.
- **Check:** Property evaluation wraps user code in an exception handler that returns a failure result.
- **Source:** ch. 8

### FPS-T43: Label composed properties to locate failures
Give each combined property a label, so a failure report shows which part of the combination failed.

- **Why:** A failure in a combined check is otherwise hard to trace to its part.
- **When:** Combining properties with and or or operators, in a library that supports labels.
- **Check:** Combined property values carry labels that appear in failure output.
- **Source:** ch. 8

### FPS-T44: Put error labels and locations in parser interface
Give the parser interface labelling combinators from the start, and record a location with each parse error.

- **Why:** Error messages then describe the expectation at a position, instead of raw inner failures.
- **When:** Designing a parser that must explain malformed input to a user.
- **Check:** The parser interface includes labelling combinators, and parse errors carry a location.
- **Source:** ch. 9

### FPS-T45: Commit a branch once it consumes input
Treat a parser that has consumed input as committed, so its failure does not fall through to the next alternative.

- **Why:** A parser cannot rewind consumed input unless wrapped in attempt, so another branch cannot restart from the same point.
- **When:** Choosing between alternatives where the first has already read input.
- **Not when:** Alternatives share a prefix that must be read before they differ.
- **Check:** The choice combinator checks a committed flag before trying the second alternative.
- **Source:** ch. 9

### FPS-T46: Wrap a shared prefix in attempt
Wrap a branch in attempt, which lets it fail without committing the input it read, when it must read a shared prefix before it can be ruled out.

- **Why:** Without attempt, the committed branch would fail on input the other alternative still needs.
- **When:** Two alternatives begin with the same tokens and differ only later.
- **Check:** Such alternatives in the grammar are wrapped in an attempt call before the choice.
- **Source:** ch. 9

### FPS-T47: Use a loop for repetition over long inputs
Implement a repetition that would overflow the stack as an explicit loop instead of recursion, and test it on a list of many thousands of elements.

- **Why:** An explicit loop keeps long inputs from exhausting the stack.
- **When:** A repetition is not a tail call and overflows the stack on large input, such as a long array.
- **Check:** The repetition combinator iterates, and a test parses a list of many thousands of elements.
- **Source:** ch. 9

### FPS-T48: Fold lists using a monoid op and zero
Reduce a list whose element type has a monoid (an associative operation with an identity value) by passing both to a fold.

- **Why:** The fold works for any monoid, because only its operation and identity are used.
- **When:** Combining a list whose element type has a monoid instance.
- **Check:** Fold calls take a monoid's op and zero rather than custom combining code.
- **Source:** ch. 10

### FPS-T49: Balance folds for parallel combining
Combine a sequence by splitting it in halves, combining each half, then combining the two results.

- **Why:** The halves can be combined in parallel, which a left-to-right walk cannot do.
- **When:** Reducing a large sequence whose halves can be combined in parallel.
- **Not when:** Each combine has a fixed cost and no parallel work is available. Then use foldLeft (FPS-T15).
- **Check:** The fold splits the sequence and combines the two halves, rather than walking it left to right.
- **Source:** ch. 10

### FPS-T50: Implement Foldable for each new collection
Implement the fold operations for each new collection type as a Foldable instance, the interface that generic code folds through, and derive the other folds from one of them.

- **Why:** Generic code then works on the new type, and only the hot paths need a direct fold.
- **When:** Adding a new data type that holds several elements.
- **Check:** The new collection type has a Foldable instance, and any slow fold is replaced by a direct one.
- **Source:** ch. 10

### FPS-T51: Combine independent steps with map2
Combine independent results with map2 instead of nesting flatMap calls.

- **Why:** Independent steps need no ordering, and map2 says so, while nested flatMap calls imply one step waits for the other.
- **When:** Two lookups or computations do not depend on each other's results.
- **Not when:** Validation must report every error (FPS-T28).
- **Check:** Independent steps are combined in one map2 call, not in nested flatMap calls.
- **Source:** ch. 12

### FPS-T52: Use flatMap when structure depends on results
Choose a later parser or computation inside a flatMap continuation when its structure depends on an earlier result.

- **Why:** Only flatMap lets a later step's structure depend on an earlier value.
- **When:** A parser must pick its row format after reading a header.
- **Check:** The later parser is built inside a flatMap continuation.
- **Source:** ch. 12

### FPS-T53: Avoid flatMap when structure is known upfront
Describe a computation with map2 or product when no later step needs an earlier result, so a runner sees its whole structure.

- **Why:** A description with a fixed structure can be inspected and optimized before it runs.
- **When:** Designing a parser or effect description that a runner will later interpret.
- **Not when:** A later step must depend on an earlier result.
- **Check:** The description uses map2 or product and contains no flatMap.
- **Source:** ch. 12

### FPS-T54: Use traverse to keep shape, fold to summarize
Use traverse, which keeps each position of the structure, when the result must keep the original structure, and fold when one summary value is enough.

- **Why:** A summary value loses the positions, so a structure-preserving pass is needed when later code still needs them.
- **When:** Choosing between a structure-preserving pass and a single summary value.
- **Check:** Structure-preserving code returns the same container type, such as Option of Tree.
- **Source:** ch. 12

### FPS-T55: Thread state through a traversal with State
Use State (FPS-T36) as the effect when a traversal must carry a counter or accumulator.

- **Why:** The state is passed by the effect, so the traversal needs no mutable variables.
- **When:** Labeling elements with positions, or collecting elements during a traversal.
- **Check:** Traversal code reads and writes its state through get and set, not mutable variables.
- **Source:** ch. 12

### FPS-T56: Interpret instructions by translating to a target monad
Write each interpreter as a translation from instructions to a target monad (a type with unit and flatMap that sequences steps), then run the program in that monad.

- **Why:** The interpreter, not the program, decides how each instruction runs.
- **When:** One program must run under several strategies, such as blocking or parallel.
- **Check:** Each interpreter is one translation function passed to a generic runner that works for any target monad.
- **Source:** ch. 13

### FPS-T57: Trampoline deep function chains
Change deep compositions and recursive calls to return a trampoline, a type whose steps a loop runs instead of the call stack, and chain them with flatMap.

- **Why:** The stack use stays predictable, so long compositions do not overflow.
- **When:** A deep chain of composed or recursive calls risks StackOverflowError.
- **Not when:** Trampolining is slower than direct calls, so skip it when depth is bounded. A repetition over input elements uses FPS-T47 instead.
- **Check:** Deep-path functions return a trampolined type and chain with flatMap, not plain values.
- **Source:** ch. 13

### FPS-T58: Use Free to separate instructions from interpretation
Parameterize a program by an instruction type with Free, a structure that builds a monad over any instruction type.

- **Why:** A monad then comes from the instruction type without giving that type monad structure.
- **When:** Defining a little language whose effects are a chosen set of instructions.
- **Check:** Program types are Free over a closed set of instruction cases, not monads with ad hoc effects, and Scala does not enforce the closed set.
- **Source:** ch. 13

### FPS-T59: Scope mutable state with a type-level token
Run local mutation through a scoped type, a phantom type parameter that only the runner can supply, so mutable cells cannot escape.

- **Why:** The type system stops a mutable reference from leaking into pure code.
- **When:** You want the compiler to guarantee that local mutable cells never leave their computation.
- **Not when:** The scoping type costs efficiency and convenience, so use it only where the guarantee matters.
- **Check:** Mutable cells are constructed only inside the block the runner passes, and the runner is not public.
- **Source:** ch. 14

### FPS-T60: Avoid lazy I/O streams for file reads
Return explicit effect values from file reads instead of lazily read streams.

- **Why:** A lazy stream closes its file only when traversal reaches the end, so early exits leak resources.
- **When:** Designing a file API whose results are consumed as collections or streams.
- **Check:** File read operations return explicit effect values, not lazy collections.
- **Source:** ch. 15

### FPS-T61: Model transformations as await-emit-halt processes
Represent a stream transformation as a state machine that awaits input, emits output or halts.

- **Why:** The same transformation then works with lists, streams or files, because a driver supplies the input.
- **When:** You need a reusable transformation that works element by element, independent of its data source.
- **Check:** The transformation type has Emit, Await and Halt cases that a driver interprets.
- **Source:** ch. 15

### FPS-T62: Attach cleanup with a resource combinator
Acquire, use and release a resource through one resource combinator, a function that takes those three steps, so release runs on every termination path.

- **Why:** Release then runs on normal end, on error and on early halt, not only when the program exits.
- **When:** A library stream definition opens a file, connection or similar handle.
- **Check:** Each opened handle is paired with its release step inside the same resource call.
- **Source:** ch. 15

### FPS-T63: Interpret effectful processes in one runner
Run an effectful process through a single interpreter that performs each request and collects the emitted values.

- **Why:** The effects then happen at the program's edge, and the process itself stays a value.
- **When:** A program needs the collected output of a process that performs I/O.
- **Check:** One runner function executes the requests and collects the outputs at the program's edge.
- **Source:** ch. 15

### FPS-T64: Test effect programs with a pure interpreter
Run an effect program in tests through a pure translation that simulates its input and output, not the real console or files.

- **Why:** A pure interpreter feeds scripted input and collects output, so no real console is needed.
- **When:** A console or other effect program must be tested without real I/O.
- **Check:** Tests run programs through a pure interpreter, not through the real console.
- **Source:** ch. 13

### FPS-T65: Expect tee zips to halt at shorter input
Expect a zip built from a tee to halt as soon as either input runs out, and test it with unequal lengths.

- **Why:** The zipped stream ends with the shorter input, so the longer input's remaining elements are not produced.
- **When:** Zipping two effectful streams whose lengths may differ.
- **Check:** A zip test covers inputs of unequal length.
- **Source:** ch. 15
