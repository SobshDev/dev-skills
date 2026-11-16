# Functional style: purity, effects, immutability, failure as values

This guide covers writing and reviewing code in a functional style: a pure core with effects at the edges, immutable data and explicit state, failure carried in return types, folds and combinators, laziness, algebraic data types, libraries designed from their laws, and interpreters for effect descriptions. The examples come from FP in Scala, and the rules apply wherever a codebase is written in this style. The single most important idea is that a function whose only observable result is its return value can be tested and reasoned about on its own, so computation and effects belong in different functions.

**Read this when:** writing or reviewing Scala or other functional code, pulling logic out of a function that also does I/O, replacing null, sentinels or thrown exceptions with Option or Either, threading state through a computation, writing a recursion, fold or stream pipeline, modelling a closed set of cases, designing a combinator library (parallelism, parsing, property testing), or building an interpreter for effect descriptions.

**Entry IDs** such as `WELC-T12` point to `../books/<book>/techniques.md` (T) or `principles.md` (P);
the prefix table is in [SKILL.md](../SKILL.md).

## Contents

- [Core rules](#core-rules)
- [Rules: immutable data and explicit state](#rules-immutable-data-and-explicit-state)
- [Rules: failure and absence as values](#rules-failure-and-absence-as-values)
- [Rules: folds, combinators and iteration](#rules-folds-combinators-and-iteration)
- [Rules: laziness and resources](#rules-laziness-and-resources)
- [Rules: algebraic data types and state machines](#rules-algebraic-data-types-and-state-machines)
- [Rules: library design and effect interpreters](#rules-library-design-and-effect-interpreters)
- [Playbooks](#playbooks)
- [Where the books disagree](#where-the-books-disagree)
- [Review checklist](#review-checklist)
- [More entries in this area](#more-entries-in-this-area)

## Core rules

### 1. Keep computation pure and push effects to a thin edge

Put the logic in functions that only compute a value, and let one thin entry function do the console, file, network and service calls around them. FP in Scala says a core that never touches the outside world can be reasoned about and tested alone. Clean Architecture asks for business rules that import no UI, database or framework code and can be tested with none of them running, and Legacy Code recommends the same split for new code that sits right before an external call. [FPS-P1, FPS-T01, CA-P2, CA-P5, WELC-T44]

- **Do:** Move each effect out of the computing function into a caller that only performs effects and calls the core once. When one function both returns a value and changes observable state, split it into a query that computes and a modifier that changes state. [FPS-T01, REF-T29, CC-T28, REF-T28]
- **Not when:** Tracking an effect in a type costs more than it gains for debug logging or memory allocation. Thin wrappers stop being practical when dependencies are too pervasive. Caching inside a query is an accepted exception, and an atomic query-and-change such as a stack pop may stay one method. [FPS-P1, WELC-T44, REF-T28, CC-T28]
- **Check:** Core functions in the diff contain no console, file, network or service calls, and a value-returning function writes nothing apart from a cache. [FPS-P1, FPS-T01, REF-T28]

```scala
// Pure core: a value in, a value out.
def totalDue(lines: List[Line], taxRate: BigDecimal): BigDecimal =
  lines.map(_.amount).sum * (1 + taxRate)

// Thin edge: performs the effects and calls the core once.
def showTotal(store: InvoiceStore, id: InvoiceId): Unit = {
  val inv = store.load(id)
  println(totalDue(inv.lines, inv.taxRate))
}
```

### 2. Pass every input, including collaborators, as a parameter

A function should read what it needs from its arguments, not from a field of its enclosing object, a global or the environment. Its result then depends only on its arguments, so any call can be replaced by the value it returns. External services such as a payment client are passed in the same way rather than constructed inside, so tests can run the function without contacting the real service. [FPS-T04, FPS-T03]

- **Do:** Add each hidden input to the parameter list, and take the service client as an argument instead of building it in the body. [FPS-T04, FPS-T03]
- **Not when:** FP in Scala notes that passing the service in is weaker when test doubles of the passed interface are awkward to write. [FPS-T03]
- **Check:** The body reads no field, global or environment value missing from its parameters, and it constructs no service client. [FPS-T04, FPS-T03]

### 3. Return a description of the effect and run it in one place

When logic must trigger an external action, have it return a value that describes the action, and let a single interpreter or entry function carry it out. The description can be tested before anything runs, and the effects then happen only at the program's edge. [FPS-T02, FPS-T63]

- **Do:** Return an effect value or instruction from the logic, and keep the calls that actually perform side effects in one runner. [FPS-T02, FPS-T63]
- **Check:** Only the interpreter or the outer entry code calls side-effecting methods. [FPS-T02, FPS-T63]

## Rules: immutable data and explicit state

### 4. Make bindings and data immutable, and return new values

Bind intermediate results with val, give data types read-only fields, and have operations return a new value instead of changing the old one. FP in Scala says a call that changes shared data can no longer be replaced by its result. Learning DDD, Refactoring and TDD all make value objects unchangeable after construction, and TDD adds that sharing them is then safe because no other reference can alter them. Learning DDD and Refactoring also compare value objects by their fields. [FPS-P2, FPS-T05, REF-T26, DDD-T15, REF-T84, TDD-T27]

- **Do:** Declare new bindings with val and variables created by an extraction as read-only. Make value types setter-free, return a new instance from each change, and base equality and hash on every field. [FPS-T05, REF-T26, DDD-T15, REF-T84]
- **Not when:** Copying a large state on every call is costly, and FP in Scala points to efficient persistent structures for that case. TDD warns to measure allocation cost with realistic data before optimizing it. Refactoring keeps a shared reference object that callers update in place out of this rule. [FPS-P2, TDD-T27, REF-T84]
- **Check:** New bindings use val, data type fields are vals, and value classes have no setters. [FPS-T05, FPS-P2, TDD-T27]

### 5. Confine any mutation where no caller can see it

A mutable local is acceptable when nothing outside the function can observe it, because the caller still receives a pure result. Refactoring treats mutable data as a large source of defects and asks that changing variables keep the narrowest scope, and Clean Architecture confines shared mutable variables to a few named components because races come from them. Where the compiler should guarantee that local mutable cells never escape, FP in Scala runs the mutation inside a scoped type whose token only a private runner can supply. [FPS-T06, REF-P5, CA-T09, FPS-T59]

- **Do:** Declare scratch variables inside the function, and never return, store or capture them. Route any remaining shared mutable data through one update function. [FPS-T06, REF-P5, CA-T09]
- **Not when:** Prefer the pure version when it is at least as easy to get right, and use State for a traversal that carries a counter (rule 7). The scoped type costs efficiency and convenience, so use it only where the guarantee matters. Mutable data often cannot be removed, and data used by one small function may stay local. [FPS-T06, FPS-T55, FPS-T59, REF-P5]
- **Check:** Every var is declared inside one function and never escapes it, and in scoped code mutable cells are built only inside the block the non-public runner passes. [FPS-T05, FPS-T06, FPS-T59]

### 6. Return the next state with each result

A stateful function should take the current state and return its result together with the new state, and the caller feeds that state into the next call. The state stays explicit, so each call is repeatable and referentially transparent. Philosophy of Software Design adds that a method returning several related values should return a named type rather than a generic pair (see the tension below). [FPS-P2, FPS-T33, POSD-T28]

- **Do:** Change a method that updates hidden state into one that returns its result paired with the next state, and thread the returned state into the following call. [FPS-T33]
- **Not when:** Steps inside one stateful procedure use a State action instead (rule 7). The named-type advice of Philosophy of Software Design does not cover stored state that callers change separately. [FPS-T33, POSD-T28]
- **Check:** Successive calls take their state from the previous result, and stateful API methods return a result together with the next state. [FPS-T33, FPS-P2]

### 7. Write multi-step state logic with State combinators

When the same state handoff repeats across generators or procedures, write it once in map, map2 and flatMap over a State type, a wrapper of a state-to-result function. Use map for one result, map2 for two independent results and flatMap when a later step depends on an earlier one. A procedure that reads and updates state in several steps then reads as a for-comprehension over get, set and modify while staying pure, and a traversal that must carry a counter or accumulator uses State as its effect instead of a mutable variable. [FPS-P5, FPS-T35, FPS-T36, FPS-T55]

- **Do:** Derive new generators with map, map2 or flatMap, write stateful procedures with get, set and modify, and label or collect elements during a traversal through State. [FPS-T35, FPS-T36, FPS-T55]
- **Check:** Derived generators do not thread state by hand, and traversal code reads and writes its state through get and set rather than mutable variables. [FPS-T35, FPS-T36, FPS-T55]

## Rules: failure and absence as values

### 8. Put recoverable failure in the return type

Make a failure that a caller might handle visible in the signature, as Option or Either, instead of hiding it in an exception, a null or a sentinel such as NaN. FP in Scala keeps exceptions for failures that no reasonable caller could recover from, and Pragmatic Programmer likewise stops at once on a state that should be impossible rather than continuing with suspect data. A function undefined for some inputs its types allow, such as the maximum of an empty list, returns Option so every input yields a value of the declared type. [FPS-P3, FPS-T19, FPS-T20, PP-T16]

- **Do:** Return Option or Either from each function that can fail for a reason a caller may handle, and throw or stop only where recovery is impossible. [FPS-P3, FPS-T19, PP-T16]
- **Not when:** Some failures are unrecoverable, and these keep their exceptions. A failure that the module can recover from without the caller is masked inside the module instead, unless callers need to know that it happened. Clean Code instead reports failures with exceptions unless the language lacks reliable exceptions, which is the first tension below. [FPS-P3, FPS-T19, POSD-T11, CC-T29]
- **Check:** Failing functions declare the failure in their return type, no path throws for a missing input, and no null or NaN stands for failure. [FPS-P3, FPS-T20]

### 9. Choose Option or Either by whether callers need the reason

Use Option when knowing that a value is absent is enough, and Either when callers must know what went wrong so they can branch on each kind of failure. Put the failure in Left and the success in Right, and when catching an exception, return it inside Left. [FPS-T25, FPS-T20]

- **Do:** Give failure values a message or the caught exception, and make catch clauses return Left. [FPS-T25]
- **Not when:** Either is more than needed when the caller only has to know that a failure occurred. [FPS-T25]
- **Check:** Failure types carry a message or exception, and catch clauses return Left with the exception. [FPS-T25]

### 10. Chain fallible steps and resolve the result once

Chain dependent steps that may produce no value with map for plain-value steps and flatMap for steps that return an Option or Either, so each step runs only if the previous one succeeded. Apply the fallback with getOrElse once, at the end of the chain, rather than at every step. Pragmatic Programmer describes the same shape for pipelines whose stages each return a value or an error, letting errors skip the remaining stages. Sequence and traverse over Either stop at the first Left, since later steps can no longer change the outcome. [FPS-T21, FPS-T22, PP-T32, FPS-T27]

- **Do:** Replace nested matches with a flatMap chain, and end the chain with a single getOrElse or one match on the final result. [FPS-T21, FPS-T22]
- **Not when:** A default value is wrong when the absence must be reported with its reason, so return Either instead of resolving with getOrElse. Stopping at the first error is wrong when every error must be shown (rule 12). [FPS-T22, FPS-T27, FPS-T28]
- **Check:** getOrElse appears once at the end of an Option chain, later stages run only on successful values, and sequence over Either stops at the first Left. [FPS-T21, FPS-T22, PP-T32, FPS-T27]

### 11. Validate domain values in Either-returning constructors

Create domain values from unchecked input through a function that returns Either and rejects invalid data, so bad values stop at the boundary. Learning DDD puts the same validation inside the value object, so every place that accepts the concept enforces one rule, and Pragmatic Programmer validates each external value once where it enters. [FPS-T26, DDD-T14, PP-T14]

- **Do:** Add a constructor function returning Either for each domain type built from user or external data, and route callers through it. [FPS-T26, DDD-T14]
- **Check:** Domain values built from unchecked input come only from the Either-returning function, not from a direct case class constructor call, and callers do not repeat the validation. [FPS-T26, DDD-T14]

### 12. Collect every error when validations are independent

When the fields of a form do not depend on each other, validate them with map2 or map3 over an applicative whose errors accumulate, so the user sees all problems at once. Either stops at its first Left, so map2 over Either alone cannot do this. [FPS-T28, FPS-T27]

- **Do:** Use an accumulating validation type for independent fields, and keep Either sequencing for checks where the first error is enough. [FPS-T28, FPS-T27]
- **Not when:** Later checks need values produced by earlier checks, which requires the stop-at-first-error chain. [FPS-T28]
- **Check:** Validation of independent fields returns the errors from every failing field, not just the first. [FPS-T28]

```scala
// Independent fields: map2 says neither waits for the other.
val person = map2(parseName(rawName), parseAge(rawAge))(Person(_, _))

// Dependent step: which plan to load depends on the parsed age.
val plan = parseAge(rawAge).flatMap(age => loadPlanFor(age))

// To report both name and age errors at once, the map2 above must run
// over an accumulating validation type, not over Either (FPS-T28).
```

## Rules: folds, combinators and iteration

### 13. Use library operations before writing recursion

Before writing an explicit recursive function, look for an existing standard operation such as take, forall or exists. Write element-wise changes as map, selection as filter and one-to-many expansion as flatMap, because each names its purpose and needs no hand-written recursion. Refactoring turns loops that only filter or map into such pipelines, one behavior at a time. [FPS-T16, FPS-T17, REF-T33]

- **Do:** Check the collection's methods for an equivalent first, then express the transform as a map, filter or flatMap pipeline. [FPS-T16, FPS-T17, REF-T33]
- **Not when:** Refactoring keeps the loop when its body has side effects or exits early. [REF-T33]
- **Check:** New list recursion has been compared against the library methods, and loops that only filter or map are pipelines. [FPS-T16, FPS-T17, REF-T33]

### 14. Factor repeated traversals into folds and function parameters

When two functions share a structure and differ only in the operation they apply, make the operation a function parameter, and when they differ only in element type, add a type parameter. Two recursive list functions that differ only in base value and operator become one fold, and size, maximum, depth and map on a tree all come from one fold over its cases. Clean Code makes the same move for several features that walk one nested structure. To get a one-argument function from an existing two-argument one, supply the first argument instead of rewriting it, so the two cannot drift apart. [FPS-P5, FPS-T08, FPS-T09, FPS-T14, FPS-T18, CC-T37, FPS-T10]

- **Do:** Pull the shared traversal into one generic function or fold that takes the varying parts as arguments, and define derived functions by partial application. [FPS-T08, FPS-T14, FPS-T18, FPS-T10]
- **Not when:** Languages without lambdas need a strategy, command or template method instead. Copies that look identical may encode different rules, so compare them before merging, and code that never changes may keep its copies. Partial application does not apply when the task is to write the combining function itself. When to merge is the third tension below. [CC-T37, PP-P3, REF-P4, FPS-T10]
- **Check:** Duplicated recursive functions become one fold call with different arguments, per-type copies become one function with a type parameter, and no duplicated body remains. [FPS-T14, FPS-T09, FPS-T08]

### 15. Make iteration over unbounded input stack-safe

Recursion that is not a tail call, such as foldRight on a list, is not stack-safe, so long inputs can overflow the stack. Write an iteration as a local helper that carries its state in arguments and mark it tailrec, so it compiles to a loop. Reduce lists of unbounded length with foldLeft rather than foldRight. A repetition that cannot be written as a tail call becomes an explicit loop tested on many thousands of elements, and a deep chain of composed or recursive calls returns a trampoline, a type whose steps a loop runs, chained with flatMap. [FPS-T07, FPS-T15, FPS-T47, FPS-T57]

- **Do:** Use a library method when one fits. Otherwise use a tailrec helper or foldLeft, an explicit loop with a long-input test for a repetition that cannot be a tail call, or a trampoline for a deep chain of composed calls. [FPS-T16, FPS-T07, FPS-T15, FPS-T47, FPS-T57]
- **Not when:** foldRight stays acceptable on bounded lists and in the lazy stream searches of rule 19. Trampolining is slower than direct calls, so skip it when depth is bounded, and use an explicit loop for a repetition over input elements. [FPS-T15, FPS-T57]
- **Check:** Each recursive call meant as a loop is in tail position and annotated tailrec, large-input reductions call foldLeft, no while loop appears unless a non-tail repetition required it, and that loop has a long-input test. [FPS-T07, FPS-T15, FPS-T47]

```scala
import scala.annotation.tailrec

// xs.count(p) already exists (FPS-T16); this shows only the shape.
def countMatching[A](xs: List[A])(p: A => Boolean): Int = {
  @tailrec
  def go(rest: List[A], acc: Int): Int = rest match {
    case Nil    => acc
    case h :: t => go(t, if (p(h)) acc + 1 else acc)
  }
  go(xs, 0)
}
```

### 16. Combine independent results with map2, dependent ones with flatMap

Use map2 when two results do not depend on each other, and flatMap only when a later step's value or structure depends on an earlier result. Nested flatMap calls imply that one step waits for the other, while map2 states that no ordering is needed, and it avoids nested matches for optional inputs. A description built only from map2 or product has a fixed structure that a runner can inspect and optimize before running it. [FPS-T51, FPS-T23, FPS-T52, FPS-T53, FPS-T35]

- **Do:** Merge independent lookups, optional values or parallel results with one map2 call, and build a later parser or computation inside a flatMap continuation only when it depends on an earlier result, such as choosing a row format after reading a header. [FPS-T51, FPS-T23, FPS-T39, FPS-T52]
- **Not when:** Validation that must report every error needs the accumulating type of rule 12. A fixed-structure description is impossible when a later step must depend on an earlier result. [FPS-T51, FPS-T53]
- **Check:** Independent steps are combined in one map2 call, not in nested flatMap calls or a for-comprehension over independent values, and descriptions meant for inspection contain no flatMap. [FPS-T51, FPS-T23, FPS-T53]

### 17. Use traverse to keep the shape and a fold to summarize

When later code needs each position of the original structure, use traverse, which returns the same container shape with an effect around it. When one summary value is enough, fold. A summary loses the positions, so choose by what the next step reads. [FPS-T54]

- **Do:** Return, for example, an Option of Tree from a structure-preserving pass, and a single value from a summarizing pass. [FPS-T54]
- **Check:** Structure-preserving code returns the same container type it was given, wrapped in the effect. [FPS-T54]

### 18. Fold through monoids and Foldable instances

When an element type has a monoid, an associative operation with an identity value, reduce a collection by passing that operation and identity to a fold, so one fold works for any monoid. For a large sequence whose halves can be combined in parallel, split it, combine each half and then combine the two results. Give each new collection type a Foldable instance and derive its other folds from one of them, so generic code works on it. [FPS-T48, FPS-T49, FPS-T50]

- **Do:** Replace custom combining code with a monoid's operation and identity, and add a Foldable instance for each new multi-element type. [FPS-T48, FPS-T50]
- **Not when:** A balanced fold gains nothing when each combine has a fixed cost and no parallel work is available, so use foldLeft then. [FPS-T49, FPS-T15]
- **Check:** Fold calls take a monoid's operation and identity, parallel reductions split the sequence in halves, and each new collection type has a Foldable instance with any slow derived fold replaced by a direct one. [FPS-T48, FPS-T49, FPS-T50]

## Rules: laziness and resources

### 19. Describe lazily and force only in a terminal step

Build a lazy description of a computation, such as a stream or a parallel value, and force it only in a final step such as toList or run, so work no consumer reads is never done. Generate streams with unfold from an initial state and a step that returns an Option of the next element and state, which keeps the generator productive. Write searches such as exists and forAll with a lazy foldRight whose combining function takes its second argument by name, so the traversal stops once the answer is known. [FPS-P6, FPS-T32, FPS-T31]

- **Do:** Return lazy values from pure builders, pass them through the pipeline unforced, and force them once at the end. [FPS-P6, FPS-T32]
- **Not when:** A consumer that needs every element of an infinite stream never finishes, and one that needs every intermediate result must keep reading. The lazy foldRight search can overflow the stack on a long stream with no match. File reads do not use lazy streams (rule 21). [FPS-P6, FPS-T31, FPS-T60]
- **Check:** Pipelines pass lazy values and force them only in a terminal step, generators call unfold with bounded steps and no shared cells, and stream predicates use foldRight with a by-name second parameter. [FPS-P6, FPS-T32, FPS-T31]

### 20. Pass costly arguments by name and evaluate them once

Declare a fallback parameter by name, as in `=> B`, when it may go unused, so a costly or throwing default is computed only if the body needs it. A by-name argument is recomputed on each use, so bind it to a lazy val before using it more than once. Lazy stream cells follow the same idea: create them through one smart constructor that stores the head and tail in lazy vals, so each is computed at most once. [FPS-T24, FPS-T29, FPS-T30]

- **Do:** Give optional fallbacks a by-name type, cache by-name arguments used several times in a lazy val, and build stream cells only through the memoizing helper. [FPS-T24, FPS-T29, FPS-T30]
- **Check:** A fallback that may go unused has a by-name type, a costly by-name parameter used several times is assigned to a lazy val first, and no code builds stream cells by calling the case class directly with thunks. [FPS-T24, FPS-T29, FPS-T30]

### 21. Release resources on every exit, without lazy I/O

Return explicit effect values from file reads instead of lazily read streams, because a lazy stream closes its file only when traversal reaches the end and an early exit leaks the handle. When a library stream opens a file or connection, acquire, use and release it through one resource combinator, so release runs on normal end, on error and on early halt. Release It! adds, for JDBC cleanup code in finally blocks, that the connection must still be closed when closing its statement throws. [FPS-T60, FPS-T62, RI-T72]

- **Do:** Pair each opened handle with its release step inside the same resource call, and in JDBC cleanup guard the statement close so its failure cannot skip the connection close. [FPS-T62, RI-T72]
- **Check:** File read operations return effect values, not lazy collections, and each opened handle is released inside the same resource call on every termination path. [FPS-T60, FPS-T62]

## Rules: algebraic data types and state machines

### 22. Model a closed set of alternatives as a sealed trait

When a data type can take only a known, fixed set of forms, declare a sealed trait with one case class or case object per form, all in one file. Match its cases from the most specific pattern to the most general, because the first matching case wins and an early catch-all hides the cases after it. [FPS-T11, FPS-T12]

- **Do:** Declare every alternative in the sealed trait's file, list each constructor in a match, and put any catch-all last. [FPS-T11, FPS-T12]
- **Not when:** The set of forms is open or expected to grow, which is the second tension below. [FPS-T11, CC-T38]
- **Check:** Every alternative extends the sealed trait in the same file, and catch-all patterns come last. [FPS-T11, FPS-T12]

### 23. Model a state machine as a pure transition function

Write a state machine as a pure function from the current state and an input to the next state and an output, so its behavior follows from the inputs alone. Pragmatic Programmer describes the same structure as a transition table from state and event to next state and action, and adds that an event with no defined transition should move the machine to a named error state rather than be silently ignored. [FPS-T37, PP-T29, PP-T30]

- **Do:** Make each transition return its next state and output, fold the input sequence through it, and send unlisted events to an explicit error state. [FPS-T37, PP-T30]
- **Not when:** Pragmatic Programmer notes that a state machine sequences events but does not solve every event problem. [PP-T29]
- **Check:** Machine logic takes the inputs and returns the final state and outputs without mutation, and missing transitions lead to an error state. [FPS-T37, PP-T30]

## Rules: library design and effect interpreters

### 24. Write the operations and their laws before the representation

Design a library by writing its public operations and the laws they must obey first, then choose a data representation and revise both together, since the representation limits which operations are practical. Keep executor, thread and parser-state types out of the public signatures. FP in Scala defines lazyUnit as fork over unit, so the derived constructor uses only public primitives and no representation details. The compiler does not enforce these laws, so FP in Scala checks them with generated-input tests, as described in [testing](testing.md). [FPS-P4, FPS-T38, FPS-P7]

- **Do:** Write the signatures and laws, define derived constructors such as lazyUnit from the public primitives, and add a generated-input test for each law. [FPS-P4, FPS-T38, FPS-P7]
- **Check:** Public signatures name no executor, thread or parser-state types, and derived operations use no representation details. [FPS-P4, FPS-T38]

### 25. Leave waiting to callers and avoid blocking the pool

Have a parallel library's run return a future, so each caller decides how long to wait and whether to cancel, and make callback failures reach the run caller. Release It! asks for an explicit time limit on every remote call, lock wait and pool checkout that a change adds or touches, which those call sites then set. A task on a bounded pool should not submit another task to the same pool and block on its result, because every thread can end up waiting and the program deadlocks. Combine two independent parallel results with a map2 combinator so no thread handling leaks to callers. See [performance and concurrency](performance-and-concurrency.md) for pools beyond this. [FPS-T41, RI-P2, FPS-T40, FPS-T39]

- **Do:** Return futures from run, put timeouts at the call sites, and merge parallel results with map2 rather than a hand-written join. [FPS-T41, RI-P2, FPS-T39]
- **Not when:** Pools that grow without bound avoid the blocking deadlock. [FPS-T40]
- **Check:** No task body calls a blocking get on a future it submitted to the same executor, and timeout or cancellation decisions appear at call sites. [FPS-T40, FPS-T41, RI-P2]

### 26. Separate instructions from their interpretation

When one program must run under several strategies, such as blocking or parallel, express it over a closed set of instruction cases and build the monad with Free, a structure that makes a monad from any instruction type. Write each interpreter as one translation from instructions to a target monad, a type with unit and flatMap, and pass it to a generic runner. The interpreter then decides how each instruction runs, and a pure interpreter that scripts input and collects output can run the same program in tests. [FPS-T58, FPS-T56, FPS-T64]

- **Do:** Define the instruction cases as a sealed type, write one translation per target, and test programs through a pure translation instead of the real console or files. [FPS-T58, FPS-T11, FPS-T56, FPS-T64]
- **Check:** Program types are Free over a closed instruction set rather than monads with ad hoc effects, and each interpreter is one translation function passed to a runner that works for any target monad. Scala does not enforce the closed set, so check it in the diff. [FPS-T58, FPS-T56]

### 27. Model stream transformations as processes run by one driver

Represent a reusable element-by-element transformation as a state machine that awaits input, emits output or halts, so the same transformation works on lists, streams or files because a driver supplies the input. Run an effectful process through one interpreter at the program's edge that performs each request and collects what the process emits. [FPS-T61, FPS-T63]

- **Do:** Give the transformation type Emit, Await and Halt cases, attach cleanup through the resource combinator of rule 21, and execute the process in a single runner. [FPS-T61, FPS-T62, FPS-T63]
- **Check:** One runner function executes the requests and collects the outputs, and no transformation reads its source directly. [FPS-T63, FPS-T61]

## Playbooks

### When you make an effectful function testable
1. If the code has no tests, pin its current behavior first, following [legacy code](legacy-code.md), unless some dependency breaking must come before the tests. [WELC-P1]
2. Mark which lines compute a value and which ones print, read, write or call a service. [FPS-T01]
3. Move the computation into its own function that calls no external API, leaving a thin wrapper that calls it and then the dependency. [WELC-T44, FPS-T01]
4. Turn every field, global or environment read in the new function into a parameter, and pass service clients in rather than constructing them. [FPS-T04, FPS-T03]
5. If a function still both returns a value and changes state, split it into a query and a modifier. [REF-T29, CC-T28]
6. Where the logic decides that an action must happen, return a description of the action and let the entry function perform it. [FPS-T02, FPS-T63]
7. Test the pure core with plain values, and test any effect program through a pure interpreter, with no server, database or console running. [CA-P5, FPS-T64]

### When you replace exceptions, null or sentinels with failure values
1. Classify each failure: the module can recover alone, a caller may recover, or nobody can. [POSD-T11, FPS-T19]
2. Mask failures the module recovers from itself unless callers need to know about them, and keep exceptions or a crash for failures nobody can recover from or states that should be impossible. [POSD-T11, FPS-T19, PP-T16]
3. For the rest, return Option when absence is enough and Either when callers need the reason, wrapping caught exceptions in Left. [FPS-T20, FPS-T25]
4. Remove every null or NaN that stood for failure. [FPS-P3]
5. Rewrite call sites as map and flatMap chains, and combine independent optional inputs with map2. [FPS-T21, FPS-T23]
6. Resolve the result once at the end with getOrElse or a single match. [FPS-T22]
7. For independent input fields, switch to an accumulating validation so every error is reported. [FPS-T28]
8. Add tests for the failure paths, since handlers that rarely run hide bugs; see [errors and contracts](errors-and-contracts.md). [POSD-T20]

### When you write an iteration over a collection
1. Look for a library method that already does it. [FPS-T16]
2. Express element-wise changes, selections and expansions as map, filter and flatMap. [FPS-T17, REF-T33]
3. If a summary is needed, fold, and use a monoid's operation and identity when the element type has one. [FPS-T54, FPS-T14, FPS-T48]
4. If the result must keep the structure's shape, use traverse instead of a fold. [FPS-T54]
5. If the traversal must carry a counter or accumulator, use State as its effect. [FPS-T55]
6. If the input can be large, use foldLeft or a tailrec helper, and use an explicit loop with a long-input test for a repetition that cannot be a tail call. [FPS-T15, FPS-T07, FPS-T47]
7. If the halves can be combined in parallel, split and combine them in a balanced fold. [FPS-T49]
8. If a deep chain of composed calls still overflows, return a trampoline. [FPS-T57]

### When you add logic that carries state between calls
1. Write the logic as a pure function from the current state and input to the next state and output. [FPS-T37, FPS-T33]
2. Make callers thread each returned state into the next call. [FPS-T33]
3. Derive new generators or steps with map, map2 and flatMap over a State type rather than by hand. [FPS-T35]
4. Write procedures with several reads and updates as a for-comprehension over get, set and modify. [FPS-T36]
5. For a state machine, send events with no transition to a named error state. [PP-T30]
6. For random numbers mapped into a range, redraw values above the largest multiple of the range size. [FPS-T34]

### When you design a combinator library
1. Write the public signatures and their laws first, with no executor, thread or parser-state types in them. [FPS-P4]
2. Choose a representation, and revise the operations if it makes one impractical. [FPS-P4]
3. Define derived constructors such as lazyUnit from the public primitives, not the representation. [FPS-T38]
4. Provide map2 for independent results and flatMap only where later structure depends on earlier results. [FPS-T39, FPS-T52, FPS-T53]
5. For parallelism, return futures from run, leave timeouts to callers and avoid blocking on the same pool. [FPS-T41, RI-P2, FPS-T40]
6. For parsers, put labelling and error locations in the interface from the start, commit a branch once it consumes input, and wrap shared prefixes in attempt. [FPS-T44, FPS-T45, FPS-T46]
7. Implement repetition combinators as loops and test them on long inputs. [FPS-T47]
8. Write a generated-input law test for each law. [FPS-P7]

## Where the books disagree

### Should a recoverable failure be an exception or a returned value?
- **Clean Code:** Report failures with exceptions so normal steps read straight through without status checks after every call, unless the language has no reliable exceptions. [CC-T29, CC-T30]
- **FP in Scala:** Put any failure a caller may handle in the return type as Option or Either, and keep exceptions for failures no caller could recover from. [FPS-P3, FPS-T19, FPS-T20, FPS-T25]
- **Pragmatic Programmer:** Stop at once on an impossible state, and pass errors through pipeline stages as values that skip the remaining steps. [PP-T16, PP-T32]
- **POSD:** Recover inside the lowest module that can, or redefine the operation so that a state it already reaches counts as success, unless callers need to know about the failure. [POSD-T11, POSD-T10]
- **Decide:** If the module can recover without input from the caller, mask the failure inside it, unless callers need to know that it happened. If the state should be impossible or no caller could recover, throw or stop. If a caller may recover, Clean Code and FP in Scala conflict, and the entries give no deciding condition apart from Clean Code's caveat for languages without reliable exceptions. Follow the convention of the code you are in: return Option or Either chained with flatMap where the codebase does, and throw where it uses exceptions. See [errors and contracts](errors-and-contracts.md). [POSD-T11, PP-T16, FPS-T19, FPS-T21, CC-T29]

### Pattern match on a sealed type, or dispatch polymorphically?
- **FP in Scala:** Model a fixed set of forms as a sealed trait and match on its cases. [FPS-T11, FPS-T12]
- **Clean Code and Refactoring:** Replace a type switch that repeats across functions with polymorphic classes, so a new type adds one class instead of edits to every switch. [CC-T38, REF-T58]
- **Design Patterns:** Represent each state of an entity as its own object carrying that state's behavior. [GOF-T18]
- **Decide:** If the set of cases is closed and known to be fixed, use a sealed trait and matches. If new types keep arriving or the set is expected to grow, use polymorphism. Keep the switch or match when it covers few cases unlikely to grow, when behavior changes more often than types, when only one function uses the type field, or when the type changes during an object's life. Prefer a transition function or match over state objects when there are few states with little logic. See [design patterns](design-patterns.md). [FPS-T11, CC-T38, REF-T58, GOF-T18]

### When should repeated structure become one combinator?
- **FP in Scala:** Once two helpers repeat a traversal or state handoff, move the shared part into one named combinator. [FPS-P5, FPS-T08, FPS-T14]
- **Refactoring:** Wait for the third similar case unless a bug or feature exposes the copies sooner, and compare near-duplicates first. [REF-P4]
- **Clean Code:** Merge copies that change together for one actor, and leave copies that serve different actors or are two or three stable lines. [CC-T36]
- **TDD:** Treat duplication as a sign of a missing concept and remove it, though a quick copy may wait until the work is shared. [TDD-P5]
- **Pragmatic Programmer:** Keep each fact in one place, while noting that identical-looking code may encode different rules. [PP-P3]
- **Decide:** Merge only copies that implement the same rule and change together, and keep copies whose small differences are real, that serve different actors, or that never change. The entries give no condition for choosing between merging at the second or the third case, so follow the codebase's convention, and see [refactoring](refactoring.md). [CC-T36, REF-P4, PP-P3, FPS-P5]

### Share working state through fields, or thread it explicitly?
- **Clean Code:** Promote locals that several extracted helpers need into fields, and hide mutable state behind one public method of the class. [CC-T35, CC-T40]
- **FP in Scala:** Pass every input as a parameter, and return the next state with each result or use a State action. [FPS-T04, FPS-T33, FPS-T36]
- **Refactoring:** When extracting, pass read-only locals in and return the one changed value, simplifying first when two or more locals change. [REF-T36]
- **Decide:** When extracted code changes only one local, pass the read-only locals in and return that value. When two or more locals change, Refactoring simplifies them first and Clean Code promotes them to fields. Clean Code's own caveats rule out fields when static fields are shared by several threads, or when multithreaded use would need locks or per-caller instances. Beyond that the entries give no condition, so in functional code thread state through results or State, and in object-oriented code follow its convention. [REF-T36, CC-T35, CC-T40, FPS-T33, FPS-T36]

### Return a pair of result and state, or a named type?
- **FP in Scala:** Stateful functions return their result paired with the next state. [FPS-T33, FPS-P2]
- **POSD:** A method returning several related values should return a named type, since generic pairs make readers guess what each slot means. [POSD-T28]
- **Decide:** Inside one stateful procedure, FP in Scala uses a State action instead of passing pairs between steps. Philosophy of Software Design's advice does not cover stored state that callers change separately. Otherwise the entries give no condition that separates the cases, so follow the codebase's convention. [FPS-T33, FPS-T36, POSD-T28]

### Model a state machine as a function, a table or state objects?
- **FP in Scala:** A pure function from state and input to next state and output. [FPS-T37]
- **Pragmatic Programmer:** A transition table from state and event to next state and action. [PP-T29]
- **Design Patterns:** One object per state, carrying that state's behavior, when an entity's behavior depends on a state that changes over time. [GOF-T18]
- **Decide:** With few states and little logic per state, use the transition function or table, since separate state classes are then less compact. When much behavior differs per state of an object, Design Patterns supports state objects. Whatever the form, send unlisted events to an explicit error state. [GOF-T18, FPS-T37, PP-T29, PP-T30]

## Review checklist

- [ ] Functions that compute values contain no console, file, network or service calls, and side-effecting calls sit only in the entry code or interpreter. [FPS-T01, FPS-T02]
- [ ] No function body reads a field, global or environment value missing from its parameters, and service clients arrive as arguments. [FPS-T04, FPS-T03]
- [ ] No method both changes state and returns a value its callers use, apart from caching or an atomic pop. [REF-T29, CC-T28, REF-T28]
- [ ] New bindings use val, and every var is local to one function and never returned, stored or captured. [FPS-T05, FPS-T06]
- [ ] Value types have no setters, return new instances from changes and compare by all fields. [DDD-T15, REF-T84, TDD-T27]
- [ ] Stateful APIs return their result with the next state, and callers thread it into the next call. [FPS-T33]
- [ ] Functions that can fail recoverably return Option or Either, and no null or NaN signals failure. [FPS-P3, FPS-T20]
- [ ] Thrown exceptions appear only where no caller could recover, and catch clauses return Left with the exception. [FPS-T19, FPS-T25]
- [ ] getOrElse appears once at the end of each Option chain, not at intermediate steps. [FPS-T22]
- [ ] Domain values from unchecked input are built only through their Either-returning constructor. [FPS-T26, DDD-T14]
- [ ] Validation of independent fields reports every failing field. [FPS-T28]
- [ ] Independent steps are combined with map2, not nested flatMap. [FPS-T51, FPS-T23]
- [ ] New explicit recursion has been checked against library methods, and duplicated traversals were merged into a fold or a function parameter. [FPS-T16, FPS-T14, FPS-T08]
- [ ] Large-input reductions use foldLeft or a tailrec helper, and any explicit loop or trampoline comes with a long-input test or a deep-chain reason. [FPS-T15, FPS-T07, FPS-T47, FPS-T57]
- [ ] Lazy values are forced only in a terminal step such as toList or run. [FPS-P6]
- [ ] Fallback parameters that may go unused are by-name, and by-name values used more than once are cached in a lazy val. [FPS-T24, FPS-T29]
- [ ] File reads return effect values, and every opened handle is released inside the same resource call. [FPS-T60, FPS-T62]
- [ ] Each sealed trait's alternatives live in its file, and catch-all match cases come last. [FPS-T11, FPS-T12]
- [ ] State machine transitions are pure and route unlisted events to an error state. [FPS-T37, PP-T30]
- [ ] Public library signatures name no executor, thread or parser-state type. [FPS-P4]
- [ ] No pool task blocks on a future it submitted to the same bounded executor, and run returns a future with timeouts set by callers. [FPS-T40, FPS-T41, RI-P2]
- [ ] Each interpreter is one translation function, and effect programs are tested through a pure interpreter. [FPS-T56, FPS-T64]

## More entries in this area

- `FPS-T13` — Reuse an immutable list tail: when adding to or removing from the front of a list, point at the existing tail, and use Vector when changes happen at the end.
- `FPS-T34` — Retry draws that land in the biased range: when mapping random integers into a range with the remainder operator.
- `FPS-T44` — Put error labels and locations in parser interface: when a parser must explain malformed input to a user.
- `FPS-T45` — Commit a branch once it consumes input: when a parser chooses between alternatives and the first has already read input, unless they share a prefix.
- `FPS-T46` — Wrap a shared prefix in attempt: when two grammar alternatives start with the same tokens and differ later.
- `FPS-T42` — Catch exceptions and report them as failures: when a property check's predicate can throw; see [testing](testing.md).
- `FPS-T43` — Label composed properties to locate failures: when combining properties in a library that supports labels.
- `FPS-T65` — Expect tee zips to halt at shorter input: when zipping two effectful streams of possibly different lengths.
- `FPS-P7` — Test laws and properties, not single examples: when testing any operation with laws, including parallel ones under fixed-size executors; see [testing](testing.md).
