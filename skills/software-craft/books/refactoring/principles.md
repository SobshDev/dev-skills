# Refactoring — Martin Fowler (2nd edition, 2018)

## Summary
Refactoring changes the internal structure of working code without changing its observable behavior. The book treats it as a discipline of small moves, each checked by tests and committed in small steps. Most refactoring happens alongside feature and bug work rather than in a dedicated phase, and design evolves through it instead of being finished first. The guidance covers naming, duplication and the handling of mutable data, and it favors removing unused machinery over adding it speculatively. The book also treats cleanup as continuous rather than deferred. Speed work starts with a profiler measurement, and tuning waits until the structure is clean.

## Principles

### REF-P1: Change structure in small, behavior-preserving steps

A refactoring changes how code is organized while its observable behavior stays the same. The book builds a large restructuring from a chain of small steps, each simple enough to check.

- **Apply:** Make one small structural move at a time, and confirm outputs match before and after.
- **Limits:** Leave a bug you notice in place, because behavior must stay the same. Fix it separately (REF-T04).
- **Check:** The refactoring diff adds no new behavior, and expected outputs are unchanged.
- **See:** REF-T09, REF-T10, REF-T12
- **Source:** ch. 2, 5, Preface

### REF-P2: Run a self-checking suite after every change

Refactoring relies on tests that catch mistakes made while editing. The book wants that suite fast and runnable with one command.

- **Apply:** Run the suite after each small edit, and commit only when it passes.
- **Check:** Each commit has a passing test run, and one documented command runs the full suite.
- **See:** REF-T01, REF-T02, REF-T09, REF-T11
- **Source:** ch. 1, 2, 4

### REF-P3: Name things for purpose and keep names current

Code should state what it means, so readers need not study the body to learn it. A name that is hard to find signals a design problem. Persistent fields deserve the most care, because they affect the most code.

- **Apply:** Choose names that reveal purpose, and treat a name that resists choosing as a design hint.
- **Check:** Changed identifiers state their purpose, and no name needs the body to decode.
- **See:** REF-T19, REF-T20, REF-T22
- **Source:** ch. 1, 2, 3, 6

### REF-P4: Keep each piece of knowledge in one place

Duplicated code forces every change to be made in several places, and a missed copy becomes a defect. The book waits for a third similar case before it unifies copies, then keeps one shared version as the source.

- **Apply:** Merge copies into one routine at the third similar case, or sooner when a bug or feature exposes them.
- **Limits:** Compare near-duplicates first, since small differences may be real. Code that never changes may keep copies.
- **Check:** No two functions in the changed area implement the same rule or calculation. Search for copies before finishing (REF-T38).
- **See:** REF-T38, REF-T39, REF-T78
- **Source:** ch. 1, 2, 3, 12

### REF-P5: Limit where data changes behind functions

The book treats mutable data as one of the largest sources of software problems. Routing changes through accessors and narrowing variable scope makes each change visible and easier to control.

- **Apply:** Route updates to shared mutable data through one function, and keep changing variables in the narrowest scope.
- **Limits:** Immutable data needs no accessor wrapper, and a copy protects only its top level. Mutable data often cannot be removed, and data one small function uses may stay local.
- **Check:** Direct writes to shared fields move into accessors or one update function, and changing variables have short scopes.
- **See:** REF-T26, REF-T27, REF-T86
- **Source:** ch. 3, 6, 9, 11
