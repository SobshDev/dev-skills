# Design Patterns: Elements of Reusable Object-Oriented Software — Gamma, Helm, Johnson and Vlissides (1st edition, 1994)

## Summary
The book argues that object-oriented designs recur, and that naming their proven solutions lets designers reuse them. Each pattern in its catalog states a problem, a solution and its consequences, and the catalog groups the patterns as creational, structural and behavioral. Patterns add indirection, so the book applies them only where variation is expected, and it weighs every choice by its consequences. Use the catalog as a shared vocabulary and a shortlist, not as a procedure to run in sequence. Concurrency, distribution, real-time and user-interface design are outside its scope.

## Principles

### GOF-P1: Program to interfaces, not implementations
Declare collaborators by abstract interface, so objects with the same interface can replace one another. The book defines an interface as the requests an object accepts, apart from its class.
- **Apply:** Type fields, parameters and return values with abstract interfaces, and name concrete classes only at creation.
- **Limits:** A product class that never changes needs no abstract type, so direct construction is acceptable.
- **Check:** Declarations name interfaces or abstract types, and concrete class names appear only in creation code.
- **See:** GOF-T05, GOF-T20, GOF-T22, GOF-T41
- **Source:** ch. 1, 3, 4

### GOF-P2: Encapsulate what varies
Put the part of a design most likely to change behind its own object or interface, so clients depend only on the stable side. The book also hides object representations and algorithms that are expected to change.
- **Apply:** Find the part expected to change, put it behind an interface, and keep callers unaware of variants.
- **Check:** Changeable behavior sits behind one interface, and callers do not branch on its concrete variants.
- **See:** GOF-T05, GOF-T17, GOF-T29, GOF-T45, GOF-T48
- **Source:** ch. 1, 2, 5, 6

### GOF-P3: Favor composition over inheritance
Reuse behavior by holding collaborator objects, not by subclassing a parent whose internal representation may change. The book notes that subclasses depend on parent internals, and that run-time composition avoids class explosion.
- **Apply:** Reuse behavior through a field that holds a collaborator, and do not subclass only to reuse code.
- **Limits:** Inheritance still helps when new components must combine with existing ones. Heavy composition hurts understanding, and static multiple inheritance helps independent libraries combine.
- **Check:** Varying behavior is selected by assigning a collaborator, not by a subclass per combination.
- **See:** GOF-T08, GOF-T10, GOF-T30, GOF-T47
- **Source:** ch. 1, 2, 4, 6

### GOF-P4: Use a pattern only where flexibility is needed
A pattern adds indirection, which costs complexity and sometimes speed. The book applies a pattern only when its flexibility is actually needed, and prefers simpler creation until a real variation appears.
- **Apply:** Adopt a pattern only when the variation it handles matters to clients and a requirement needs it.
- **Limits:** Skip an abstraction for one implementation unless clients must avoid recompiling, and do not expose choices clients must study first.
- **Check:** The change names, in a comment or its description, each pattern's variation and the requirement behind it.
- **See:** GOF-T03, GOF-T13, GOF-T20
- **Source:** ch. 1, 3, 4, 5

### GOF-P5: Record consequences and trade-offs
The book compares designs by consequences, which structure diagrams rarely show. It asks designers to record effects on space, time, flexibility and portability, and the alternatives rejected.
- **Apply:** Write the trade-offs and rejected alternatives next to every pattern-based structure.
- **Limits:** When compile-time safety matters more than uniformity, child operations belong only on composites.
- **Check:** The PR description lists alternatives considered and their effects on space, time, or flexibility.
- **See:** GOF-T01, GOF-T02, GOF-T12, GOF-T16, GOF-T46
- **Source:** ch. 1, 2, 4, 6

### GOF-P6: Start simple and let variation drive change
Expect reuse to revise a design, and begin with a structure that fits current needs. The book balances specific fit against future generality, and applies heavier patterns only for variation the design uses or expects.
- **Apply:** Build the simplest structure that fits today's needs, and add a heavier pattern only for a variation the code uses or expects.
- **Limits:** Long-lived systems still need anticipated changes planned in advance.
- **Check:** The change names expected future changes, in a comment or its description, and the code meant to absorb each.
- **See:** GOF-T13, GOF-T20
- **Source:** ch. 1, 3, 6
