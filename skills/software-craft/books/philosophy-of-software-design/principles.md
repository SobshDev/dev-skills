# A Philosophy of Software Design — John Ousterhout (2nd edition, 2021)

## Summary
The book argues that the main cost of large software is complexity, meaning anything that makes a system hard to understand and change. Complexity comes from dependencies and obscurity, and it accumulates through small compromises. The remedy is deep modules with simple interfaces, each design decision kept in one place, and design treated as continuous work.

## Principles

### POSD-P1: Judge complexity by how hard change is

The book defines complexity as anything that makes a system hard to understand and modify, not as size or feature count. A reviewer's verdict that code is not obvious counts as evidence of complexity, even when the author sees it as clear.

- **Apply:** Judge a design by the effort and risk a typical change needs, and by how hard readers find it.
- **Limits:** Fewer lines do not mean simpler code when a longer version lowers reader effort.
- **Check:** A rule or format change touches one owning module, and if a typical change spans several, the design needs work.
- **See:** POSD-T01, POSD-T02
- **Source:** ch. 2, 13, 18

### POSD-P2: Build deep modules with simple interfaces

A module's value is the functionality it hides behind its interface, and this test applies to any unit with an interface, including a function or a service. Interfaces should be much simpler than the implementations behind them, and shallow wrappers that expose nearly as much as they hide add little.

- **Apply:** Give each module few entry points and keep the hard logic inside it.
- **Limits:** Some shallow classes, such as linked-list nodes, are unavoidable and still useful.
- **Check:** The public surface is small relative to the internal code, and wrappers that only forward calls are removed unless they keep an external interface unchanged (POSD-T43).
- **See:** POSD-T03, POSD-T04, POSD-T05
- **Source:** ch. 1, 4, 8

### POSD-P3: Hide design decisions inside one module

Information leakage happens when one design decision is reflected in several modules. Each decision should live in one module, so that changing it touches only that module. When knowledge has already leaked, move it into one owning class, because a new class that still exposes most of it adds little value.

- **Apply:** Keep format, encoding, and representation knowledge in one owning module.
- **Limits:** A new class that merely re-exposes the leaked knowledge adds little value.
- **Check:** The same format or rule does not appear in two or more files.
- **See:** POSD-T06, POSD-T07, POSD-T37
- **Source:** ch. 1, 5, 21

### POSD-P4: Pull complexity downwards into the module

When complexity is unavoidable, the module that owns it should absorb it, even if that module's developer must do more work. Callers then need less knowledge and fewer special cases, so the module should resolve hard conditions itself and handle a failure at the lowest layer that can resolve it.

- **Apply:** Handle hard conditions, ordering rules, and defaults inside the module that owns them.
- **Limits:** Do not pull all application functionality into one class, and move logic only when it is closely related to that class.
- **Check:** Callers do not handle complexity that the module hides internally.
- **See:** POSD-T08, POSD-T09, POSD-T11
- **Source:** ch. 2, 5, 8, 21

### POSD-P5: Design it twice before committing

Before committing to a major interface or structure, compare at least two radically different alternatives. Use the principles to guide that comparison, not as a fixed recipe.

- **Apply:** Write down two or more alternatives and say why the chosen one wins.
- **Limits:** The principles alone may not identify one best design.
- **Check:** For each new public interface, the PR description or design note names one rejected alternative and the factor that ruled it out.
- **See:** POSD-T13, POSD-T14
- **Source:** ch. 1, 3, 11

### POSD-P6: Write comments for the reader's missing knowledge

Code cannot express intent or the conditions for calling a method. Comments should supply those facts, written during development while the author still knows them, and each comment should add meaning that the code does not show.

- **Apply:** Document interface behavior and rationale, and skip what the code already says.
- **Limits:** Comments that describe implementation detail on a public interface signal a shallow design.
- **Check:** New public declarations arrive with comments that add facts absent from the code.
- **See:** POSD-T15, POSD-T16, POSD-T22
- **Source:** ch. 12, 13, 15

### POSD-P7: Keep the design improving with every change

Design is continuous work, not a separate phase. Expect the first design to change, and make one small design improvement in the code area each change touches.

- **Apply:** Make one small design improvement in the code area each change touches. When the change conflicts with the current structure, restructure the affected code instead (POSD-T33).
- **Check:** The diff holds at most one unrelated cleanup, in files the change already touches.
- **See:** POSD-T18, POSD-T19, POSD-T33
- **Source:** ch. 1, 3, 16
