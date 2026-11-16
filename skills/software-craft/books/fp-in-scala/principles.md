# Functional Programming in Scala — Paul Chiusano and Rúnar Bjarnason (1st edition, 2014)

## Summary
The book argues that functional programs are easier to reason about, test and combine when functions are pure, meaning their only observable effect is their return value. It shows how to keep effects at the edges, how to represent failure, state and laziness as ordinary values, and how to design libraries by stating their operations and laws first. Its examples are in Scala, and the guidance applies whenever a Scala codebase is written, changed or reviewed.

## Principles

### FPS-P1: Keep effects at the edges of the program
Keep a pure core of functions, and push I/O and external calls into a thin layer at the program's edge. The book says this separation keeps the logic testable and reasonable, because the core never touches the outside world.

- **Apply:** Move each console, file, network or service call out of business logic, and let one entry function call the pure core.
- **Limits:** Tracking an effect in a type costs more than it gains for debug logging or memory allocation.
- **Check:** Core functions in the diff contain no console, file, network or service calls.
- **See:** FPS-T01, FPS-T02, FPS-T56
- **Source:** ch. 1, 13, 14

### FPS-P2: Use immutable values and pass state explicitly
Return new values instead of changing existing ones, and pass state through results. The book says a call that changes shared data can no longer be replaced by its result, which breaks reasoning about the program.

- **Apply:** Return the next state together with each result, and give data types operations that return new values. For several steps sharing state, use a State action (FPS-T36).
- **Limits:** Copying a large state on every call is costly, so efficient persistent structures help.
- **Check:** Data type fields are vals, and stateful methods return a result paired with the next state.
- **See:** FPS-T05, FPS-T13, FPS-T33, FPS-T36
- **Source:** ch. 1, 3, 6

### FPS-P3: Represent failure and absence as values
Make a recoverable failure visible in the return type, as Option or Either, instead of hiding it in an exception or a sentinel value. The book reserves exceptions for failures that no caller could recover from.

- **Apply:** Return Option or Either from a function that can fail for a reason a caller may handle, and throw only for unrecoverable failures.
- **Limits:** Some failures are unrecoverable, and the book reserves exceptions for those cases.
- **Check:** Failing functions declare the failure in their return type, and no null or NaN stands for failure.
- **See:** FPS-T19, FPS-T20, FPS-T25
- **Source:** ch. 4, 15

### FPS-P4: Start from the interface, then revise the representation
Write the public operations and their laws first, then choose the data representation. The book says the representation constrains which interface functions are practical, so the two are revised together.

- **Apply:** Write public signatures and laws first, and keep executor, thread or parser internals out of them.
- **Check:** Public signatures in the diff name no executor, thread or parser-state types.
- **See:** FPS-T44
- **Source:** ch. 7, 8, 9

### FPS-P5: Factor repeated structure into named combinators
When the same traversal or state handoff repeats, move it into one named combinator and reuse it. The book treats repeated state-passing as a sign of a missing abstraction.

- **Apply:** When two helpers repeat a traversal or a state handoff, move the shared part into one combinator that both call.
- **Check:** Near-identical helpers in a diff are replaced by one shared combinator.
- **See:** FPS-T14, FPS-T35, FPS-T55
- **Source:** ch. 5, 6, 11, part 3

### FPS-P6: Describe lazily and evaluate only what is needed
Build a description of a computation and force only the results a consumer reads. The book says laziness separates describing an expression from evaluating it, so unused work is never done.

- **Apply:** Return lazy streams or parallel values from pure builders, force them only in a terminal step such as toList or run, and return effect values for file reads (FPS-T60).
- **Limits:** A consumer that needs every element of an infinite stream never finishes, and one that needs every intermediate result must keep reading the stream.
- **Check:** Pipelines pass lazy values and force them only in a terminal step such as toList or run.
- **See:** FPS-T32, FPS-T38, FPS-T60, FPS-T63
- **Source:** ch. 5, 7

### FPS-P7: Test laws and properties, not single examples
Check each operation against the laws it must satisfy, using generated inputs that compare two results. The book's reason is that the compiler does not enforce interface laws, so tests must check them.

- **Apply:** Write law tests that generate values and compare two expressions, instead of one fixed literal input.
- **Check:** Test code for a law or property uses a generator and compares two results, not only fixed literal inputs, and parallel law tests also run under fixed-size executors.
- **Source:** ch. 7, 8, 10, 11
