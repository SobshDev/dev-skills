# Design patterns: when and which

This guide covers choosing and applying object-oriented design patterns (creational, structural and behavioral), what each one costs, and the simpler event, callback and state-machine designs that often do the job. The most important idea: a pattern buys flexibility with indirection, so add one only for a variation the code uses now or a requirement names, and write down the trade-off when you do.

**Read this when:** you are about to add an interface, factory, wrapper or class hierarchy, a type switch keeps growing, an object's behavior depends on its state, you need undo, redo, queuing or logging of requests, objects must react to another object's changes, you are wiring callbacks or event handlers, you are modeling a multi-step workflow driven by events, or a reviewer asks whether a pattern is worth it.

**Entry IDs** such as `WELC-T12` point to `../books/<book>/techniques.md` (T) or `principles.md` (P);
the prefix table is in [SKILL.md](../SKILL.md).

## Contents

- [Core rules: deciding whether to use a pattern](#core-rules-deciding-whether-to-use-a-pattern)
- [Rules: creating objects](#rules-creating-objects)
- [Rules: wrapping and structuring objects](#rules-wrapping-and-structuring-objects)
- [Rules: varying behavior](#rules-varying-behavior)
- [Rules: events, callbacks and state machines](#rules-events-callbacks-and-state-machines)
- [Playbooks](#playbooks)
- [Where the books disagree](#where-the-books-disagree)
- [Review checklist](#review-checklist)
- [More entries in this area](#more-entries-in-this-area)

## Core rules: deciding whether to use a pattern

### 1. Add a pattern only for a variation you need

Every pattern adds a layer of indirection, which costs understanding and sometimes speed. Design Patterns applies one only when clients actually need the flexibility it gives, and starts with the simplest structure that fits current needs. TDD, Clean Code, Refactoring, Pragmatic Programmer and Learning DDD agree from their own angles: an abstraction added before a need is a guess, unused extension points cost reading time, and speculative hooks and abstract classes should be deleted. Learning DDD asks the same of its advanced patterns, such as a domain model, event sourcing or CQRS: each must justify itself with a stated requirement. [GOF-P4, GOF-P6, TDD-P9, TDD-T18, CC-T77, REF-T85, PP-T71, DDD-T56]

- **Do:** Before adding a pattern, name the variation it absorbs and the requirement, caller or failing test that needs it. Put that sentence in a comment or the PR description. Build the plain version when no such variation exists yet.
- **Not when:** Long-lived systems still need changes they can foresee planned in advance (GOF-P6). Clean Code accepts an extension point when growth is a confirmed business direction or the hook is very likely to be needed (CC-T77). A design choice that shapes the whole system deserves careful reasoning before code (TDD-P9). Structure the agreed value still needs is not a guessed future need (PP-T71). An abstraction with a single implementation can still be worth it when clients must avoid recompiling, and a pattern should not expose choices clients must study before they can use it (GOF-P4).
- **Check:** Each new pattern class, interface or hook in the diff has a current caller, and the PR names the variation and the requirement behind it.

### 2. Choose the pattern by the aspect that must vary

Pick a pattern by first naming the part of the design you need to change later without redesigning, then find the pattern that isolates exactly that part. Patterns with similar class diagrams can serve different intents, so compare candidates by intent, not shape, and read each one's applicability and consequences before committing. [GOF-T13, GOF-P2, GOF-T03, GOF-T02]

- **Do:** List the likely changes. For each, put the part that varies behind its own object or interface so callers depend only on the stable side, and stop callers from branching on its concrete variants. Name the closest rival pattern and why it lost.
- **Check:** The PR lists each likely change with the pattern chosen to absorb it, the applicability conditions the change meets, and the nearest rejected alternative.

### 3. Record consequences and rejected alternatives

Class diagrams rarely show what a design costs. Design Patterns compares designs by their effects on space, time, flexibility and portability, and asks for the rejected alternatives to be written down. POSD asks you to compare at least two radically different designs for a major interface, and Pragmatic Programmer asks which modules a likely change would touch under each option. [GOF-P5, POSD-P5, PP-T68, GOF-T12]

- **Do:** Next to any pattern-based structure, record its trade-offs and the alternatives you considered. For a design that composes many objects at run time, also document which instances collaborate, where the indirection sits and where the configuration points are, because the class code does not show that network. When writing reusable design notes, give each one a name, the problem, the solution and its consequences (GOF-T01).
- **Not when:** POSD notes that its principles may not single out one best design, so the comparison informs a judgment rather than replacing it (POSD-P5).
- **Check:** The PR description or design note lists alternatives with their effects on space, time or flexibility, and the modules a likely change would touch.

### 4. Name participants with a domain term plus the role

A pattern is abstract, so each application class plays one of its roles inside your domain. Name each class with an application term and its pattern role, so a reader sees both what it is about and how it collaborates. [GOF-T14, PP-T26]

- **Do:** Use names such as `LayoutStrategy`, `PricingRuleVisitor` or `OrderCommand`, with the domain part taken from the project's glossary.
- **Check:** Pattern classes combine a domain term with the role name, and the domain term appears in the glossary or requirements.

### 5. Depend on interfaces and name concrete classes only at creation

Declare fields, parameters and return values with abstract types, so objects that share an interface can stand in for each other. Concrete class names then appear only where objects are created. Clean Architecture applies the same rule across component boundaries, and Pragmatic Programmer prefers interfaces to subclassing for interchangeable behavior. [GOF-P1, PP-T33, CA-T06, GOF-T22]

- **Do:** Type collaborators by interface. In a library others use, publish only abstract product and factory types and keep concrete product names inside the factories.
- **Not when:** A product class that never changes needs no abstract type, so building it directly is fine (GOF-P1). Stable platform classes such as strings may stay concrete (CA-P1). C++ templates decouple code but still force dependents to recompile (CA-T06).
- **Check:** Declarations name interfaces, concrete class names appear only in creation code, and client sources name no concrete product class.

See [architecture](architecture.md) for dependency direction across components and [module-design](module-design.md) for sizing the interfaces themselves.

### 6. Reuse behavior by composition before inheritance

A subclass depends on its parent's internals, and one subclass per combination of behaviors multiplies classes. Hold a collaborator in a field instead, and select behavior by assigning a different one. Fix variation that is settled at compile time with subclasses or type parameters, and hold variation that must change at run time in object references. [GOF-P3, GOF-T09, GOF-T10, REF-T70]

- **Do:** For behavior that changes at run time, forward the operation to a delegate and pass the receiver along so the delegate can call back. Keep each base class either interface-only or a deliberate code-sharing base, so subclasses do not hide parent operations callers rely on (GOF-T08). Replace a subclass that refuses parent methods with a delegate (REF-T71).
- **Not when:** Inheritance still helps when new components must combine with existing ones, heavy composition makes a design harder to follow, and static multiple inheritance helps independent libraries combine (GOF-P3). Forwarding that follows no standard pattern, such as State or Strategy, complicates more than it simplifies (GOF-T10). Do not make a code-sharing base when the parent's internal representation may change (GOF-T08). Refactoring is fine with starting from inheritance until it causes problems (REF-T70), and a subclass used for reuse may stay if it confuses no one (REF-T71).
- **Check:** Run-time variation is selected by assigning a collaborator, not by a subclass per combination, and each delegate is a State or Strategy object.

## Rules: creating objects

### 7. Send varying creation through a factory

When creation is complex or the product kind varies at run time, create objects through a factory instead of naming concrete classes at each call site. Clean Code and Clean Architecture add that the switch choosing the type belongs in that one factory, and that Main should build the concrete factory and hand it out behind its abstract type. [GOF-T20, CA-T19, CA-T21, CC-T39]

- **Do:** Put each creation decision in a factory, or in a dedicated creation operation that subclasses can override (GOF-T24). Let startup code pick the concrete factory and store it in a variable of the abstract type.
- **Not when:** Fixed, simple products may be built directly (GOF-T20). Clean Code does not push the type switch into a factory when behavior changes far more often than the data types do (CC-T39). A dedicated overridable creation operation is the wrong tool when products must come from one family (rule 8) or classes are chosen at run time (rule 9) (GOF-T24).
- **Check:** Varying products come from a factory, the type switch lives only in a factory or main module, and client source never names the volatile concrete class.

### 8. Choose one concrete factory per product family

When a system is configured with one of several families of related products, pick one concrete factory in one place and create every product of that family through it, so products from different families never mix. [GOF-T21, GOF-T31]

- **Do:** Select the factory once at startup or per deployment, and have constructors obtain platform implementations from that well-known factory. In a dynamically typed language where product kinds change often, one make operation whose argument names the kind means a new kind needs only a new identifier (GOF-T23).
- **Not when:** The single parameterized make operation does not suit a statically typed language where products cannot be safely cast to their concrete types (GOF-T23).
- **Check:** Each client gets its products from one factory instance chosen in one place, and no constructor hard-codes a platform class.

### 9. Clone registered prototypes when classes are known only at run time

When the classes to create are known only at run time, or a creator hierarchy would mirror the product hierarchy class for class, register prototype instances and clone them. [GOF-T25]

- **Do:** Keep a registry of prototypes keyed by kind, and create new objects by cloning the registered one.
- **Not when:** A make operation keyed by kind name already suffices (GOF-T23).
- **Check:** Creation code clones a registered instance, and no creator subclass exists per product subclass.

### 10. Give a true sole instance one accessor

When exactly one instance must exist and clients need one access point, make the class own that instance and expose it through a single static accessor, which controls access better than a global variable. Pragmatic Programmer pulls the other way for code that uses such services, so read the tension on [singletons](#should-shared-services-be-singletons-or-parameters) before adding one. [GOF-T26, PP-T27]

- **Do:** Keep the constructor non-public, expose one accessor, and keep the instance out of global variables. Expose no public mutable fields on it.
- **Check:** One static accessor returns the instance, the constructor is not public, no global holds it, and it has no public mutable fields.

## Rules: wrapping and structuring objects

### 11. Pick the wrapper by what it does to the interface

A wrapper that keeps the wrapped interface is a decorator, one that converts it to another interface is an adapter, and one that offers a new, simpler interface over a whole subsystem is a facade. A wrapper that controls access stays a proxy. Decorators and proxies expose the same operations as the object they wrap, so clients can use wrapped and plain objects alike. [GOF-T57, GOF-T06, GOF-T55]

- **Do:** Decide which of the four you are building, and name it as that. Match the wrapped operation signatures in decorators.
- **Not when:** A protection proxy may refuse some operations, so its interface can be a subset (GOF-T06).
- **Check:** A decorator has the same operations as its component, an adapter changes them, a facade offers a new subsystem interface, and access control lives in a proxy.

### 12. Adapt existing code narrowly at one boundary

When a reusable class does what you need but its interface does not match, wrap it in an adapter that exposes the interface your code expects, leaving the class untouched. Adapt only the few operations the target needs. The same move applies to platform and vendor APIs: Design Patterns, Pragmatic Programmer and Clean Code all confine those calls to one layer you own, so a platform or vendor change stays in one place. [GOF-T19, GOF-T41, GOF-T17, PP-T12, PP-T13, CC-T51]

- **Do:** Implement the expected interface in a new class that delegates to the existing one with single-call forwarding methods. Keep endpoint paths, error codes and vendor types inside the adapter.
- **Not when:** When you write the reusable class yourself, build adaptation into it instead (GOF-T19). Give it abstract adaptation operations that each application subclass implements when every application can subclass it (GOF-T42). Give it hooks or per-request callables when it must work with unrelated, unforeseen classes (GOF-T43). Those hooks are unnecessary when the class serves only one application (GOF-T43).
- **Check:** The adapter depends on few adaptee operations, its forwarding methods are single calls, and platform or vendor calls appear only inside the adapter layer.

The wider case for wrapping volatile dependencies is in [architecture](architecture.md) and [module-design](module-design.md).

### 13. Add optional responsibilities with small decorators

To add a responsibility to some objects but not others, enclose them in a decorator instead of changing their class. Keep the base component lean and put each optional feature in its own decorator, which can be added or removed at run time. POSD warns against decorators that forward most calls without adding behavior, so check the tension on [forwarding wrappers](#is-a-forwarding-wrapper-worth-its-layer). [GOF-T30, GOF-T47, GOF-T58, POSD-T43]

- **Do:** Make the decorator hold a component reference, conform to the component interface, and call the wrapped operation before adding its own work. When the set of features is known only at run time, assemble the chain from a list of decorators.
- **Not when:** With only one optional feature, a single concrete decorator is simpler (GOF-T47). A proxy fits better for one fixed relationship between wrapper and subject (GOF-T58). POSD prefers adding a broadly useful feature to the base class, or building it standalone, when the decorator would forward most methods unchanged (POSD-T43).
- **Check:** The base class holds core behavior only, each optional feature is its own decorator, and no decorator forwards most of its methods unchanged without a reason.

### 14. Give a large subsystem one simple entry point

When most clients need only routine operations from a subsystem with many classes, give it a facade that offers those operations. The subsystem's classes can then change behind one stable entry. [GOF-T48]

- **Do:** Route common client code through the facade, and keep implementation classes out of client sources.
- **Check:** Common client code calls one facade class, and subsystem implementation classes do not appear in client sources.

### 15. Split a hierarchy that varies in two directions

When a class hierarchy grows along two independent dimensions, such as kind of window and platform, the leaves multiply. Split it into an abstraction hierarchy and an implementor hierarchy linked by a reference, so each can evolve without changing the other. [GOF-T44, GOF-T32]

- **Do:** Give the abstraction a reference to an implementor. When binary compatibility must survive changes to the implementation library, declare implementors in a private header that clients never include (GOF-T45).
- **Check:** Two hierarchies replace one, and changing a platform implementation class requires no edit to any abstraction class.

### 16. Treat leaves and containers through one component type

When clients must handle single objects and groups alike, define one abstract component for both, so clients need no type tests. Decide where child operations live: on the root for uniformity, with leaves failing loudly, or only on composites when compile-time safety matters more. [GOF-T16, GOF-T46, GOF-P5]

- **Do:** If Add and Remove sit on the root, make them fail or report an error in leaves and make child access return nothing, since a silent no-op hides misuse. Reach children through child, insert and remove operations so storage can change (GOF-T29). Store a parent reference in each child when its size or appearance depends on its position, and set it only in Add and Remove (GOF-T28).
- **Not when:** Skip operation-based child access when children sit in a plain array and integer indexing is enough (GOF-T29). Children shared between composites cannot hold a single parent reference (GOF-T28).
- **Check:** Leaves and containers share one base, clients contain no type checks, base Add and Remove fail or report failure, and parent references change only in Add and Remove.

### 17. Give each proxy one access concern

Choose the proxy kind by the problem: virtual for costly creation, remote for another address space, protection for access rights, and smart reference for bookkeeping. One proxy that mixes concerns is hard to understand. [GOF-T55, GOF-T54]

- **Do:** For a costly object that may never be used, create the real subject inside the first request that needs it, and answer metadata requests from stored values. In a dynamically typed language, a generic proxy can route undefined calls through the language's catch-all forwarding hook (GOF-T56).
- **Not when:** The catch-all hook is slow, and identity tests and some built-in messages bypass it (GOF-T56).
- **Check:** Each proxy class addresses one concern, and a virtual proxy creates its subject lazily.

### 18. Share small objects only when their state is context-free

When huge numbers of small objects strain memory, share them, but only if the state they hold does not depend on where or by whom they are used. Keep that intrinsic state inside, pass context such as position or style in as arguments, and get shared objects only from a factory table keyed by the intrinsic state. [GOF-T49, GOF-T50, GOF-T51]

- **Do:** In a composite, share leaves only and pass each leaf its parent as an argument (GOF-T52). Implement State and Strategy objects that hold no per-context data as shared instances (GOF-T53).
- **Not when:** Do not share state objects whose instance variables differ per context (GOF-T53).
- **Check:** Shared classes hold no location, parent or client fields, no code compares them by reference, and the factory creates entries only for unseen keys.

## Rules: varying behavior

### 19. Put client-chosen algorithms behind strategy objects

When a class holds several branches that pick an algorithm, or the algorithm must change at run time, move each variant into its own strategy class behind one interface and delegate to the chosen one. Clean Code and Refactoring make the same move for type switches that repeat across functions, so a new type adds one class instead of editing every switch. [GOF-T05, GOF-T64, CC-T38, REF-T58]

- **Do:** Delegate from the context to the strategy. Make strategies stateless where many contexts would otherwise each create one, keeping per-use data in the context (GOF-T65). When replacing a type switch, first create the classes and a factory that selects them, then move each branch into its class (REF-T59).
- **Not when:** Use State instead when the branches follow the object's own changing state rather than a client's choice (GOF-T64). Keep the switch when it covers few cases unlikely to grow, or when behavior changes more often than the set of types (CC-T38). Refactoring keeps the conditional when only one function uses the type field or when no behavior varies by type, and it uses a delegate instead of subclasses when the type changes during an object's life (REF-T58, REF-T69, REF-T70). A strategy that must keep state across calls cannot be shared (GOF-T65).
- **Check:** Each variant is its own class, adding one changes neither the others nor the context, and no context subclass differs only in its algorithm.

The step-by-step refactoring from a switch to classes is in [refactoring](refactoring.md).

### 20. Give each state of an entity its own object

When an entity's behavior depends on its own state, which changes over time, represent each state as an object carrying that state's behavior. Transitions then show up as replacing one state object with another, not as hidden field assignments. [GOF-T18, GOF-T62]

- **Do:** Delegate state-dependent operations to the current state object. When transition criteria should be easy to extend, let each state choose its successor through a context setter.
- **Not when:** With few states and little logic, the extra classes are less compact than a branch (GOF-T18). Keep fixed transition criteria in the context or in a table (GOF-T62, rule 29).
- **Check:** State-specific behavior lives in state classes, not in branches on one field, and states reach each other only through the context.

### 21. Make a request an object when it needs memory

Represent a user operation as a command object with an Execute operation when one operation is reachable from several controls, when the invoker must not know the receiver, or when the request must remember state such as its target. Pass commands to menu items and buttons instead of bare functions in those cases. [GOF-T33, GOF-T34, GOF-T37]

- **Do:** Let callers invoke only Execute, and let the command delegate to whichever receivers it needs. When a request must run later or elsewhere, keep the command alive and store in it everything it needs, so it can be queued, logged or sent (GOF-T75).
- **Not when:** A command cannot travel to another process or program run if its receiver cannot be identified there (GOF-T75).
- **Check:** UI code calls Execute and never calls target classes directly, controls may share one command, and a deferred command holds what it needs without the caller's context.

Refactoring's command object for untangling a long function is a different use, listed under [More entries](#more-entries-in-this-area).

### 22. Build undo from saved state, not guessed inverses

An undoable command saves the prior state during Execute and restores it in Unexecute, which returns objects exactly to where they were. Keep executed commands in one ordered history with a current position, moving back to undo and forward to redo. When reversing a change cannot restore connected or constrained objects exactly, store a snapshot in a memento that only the originator can read. [GOF-T35, GOF-T36, GOF-T72, GOF-T71]

- **Do:** Set the saved-state fields inside Execute. Keep commands that change nothing, and save-and-quit commands, out of the history. Let the caretaker that holds mementos only keep and return them.
- **Not when:** Reversal by stored prior values fails when connected objects cannot be restored exactly, so use a snapshot (GOF-T35). Snapshots are a poor fit when saving and restoring is expensive relative to how often they are taken (GOF-T71, GOF-T72).
- **Check:** Undoable commands set saved-state fields in Execute and read them in Unexecute, undo and redo move one position in one list, and the change records snapshot size and frequency against copy cost.

### 23. Fix an algorithm's skeleton and expose named hooks

When subclasses share an algorithm but differ in some steps, write the fixed order once in a base-class template method that calls overridable operations. Call hook operations at chosen points so subclasses can extend only there, and so no subclass has to remember to call its parent. Legacy Code reaches the same shape when it keeps each subclass to its constructor data and one hook. [GOF-T66, GOF-T67, GOF-T68, WELC-T52]

- **Do:** Keep control flow in the base class, and let subclasses override only hooks.
- **Check:** A base-class method calls overridable operations in a fixed order, subclasses override only hook methods, and none must call a parent operation itself.

### 24. Separate traversal from per-element work

Put traversal loops in iterator classes and per-element analysis in separate objects, so traversal code is written once. Add each new traversal order or filter as its own iterator. When many analyses must treat element kinds differently over a stable structure, put each analysis in a visitor that elements accept. [GOF-T38, GOF-T39, GOF-T40, GOF-T74]

- **Do:** Have the aggregate only create iterators that hold traversal state. For visitors, have each element's Accept call the visit method for its own class, passing the visitor in as a parameter.
- **Not when:** Use visitors only when analyses treat element kinds differently, and iterators alone when every element is handled alike (GOF-T38). Avoid visitors when the element class hierarchy changes often, since each new element class touches every visitor (GOF-T40). The Accept double-dispatch step is unnecessary in a language with double or multiple dispatch (GOF-T74).
- **Check:** Analysis classes contain no traversal loops, traversal variants are iterator classes, and visitors declare one operation per element class while elements hold no analysis logic.

### 25. Pass a request along a chain when its handler is unknown

When several objects might handle a request and the sender should not know which, pass it along a chain of handlers until one takes it. Reuse an existing parent link as the successor when it already orders objects the way handling needs. [GOF-T59, GOF-T60]

- **Do:** Give the end of the chain a defined outcome, make each handler forward what it declines, and test each request type sent to the head.
- **Not when:** Do not reuse parent links that do not match the needed chain, because extra redundant links would then be required (GOF-T60).
- **Check:** The chain end has a defined result, handlers forward declined requests, and the successor comes from an existing field where one fits.

### 26. Route tangled peer interactions through a mediator

When peers interact in well-defined but complex ways, or one component depends on many collaborators, let a mediator coordinate them so each colleague refers only to the mediator. [GOF-T61]

- **Do:** Move each cross-colleague rule into the mediator, and remove direct references between colleagues.
- **Not when:** One change that fans out to many dependents is an observer problem, not a mediator one (rule 27). Watch for the mediator growing into a monolith with each new colleague rule (GOF-T61).
- **Check:** Each colleague links to the mediator and to no other colleague, and the mediator has not absorbed unrelated rules.

## Rules: events, callbacks and state machines

### 27. Start notifications with the simplest mechanism that fits

For a few in-process listeners, a plain list of callback functions in the event source is enough and needs no library or shared bus. When one object's change must update many dependents, let the subject notify registered observers through one abstract observer interface. When several interdependent subjects change in one operation, route their updates through one change manager that holds the subject-to-observer mapping. [PP-T28, GOF-T15, GOF-T70]

- **Do:** Pass the subject and the changed aspect in each notification, and keep per-observer logic out of Notify. Use a command object instead of a bare callback when the request needs state, undo or reuse (rule 21). State in each handler's interface comment when it is called and from which thread (POSD-T56).
- **Not when:** A callback list couples and blocks the source when observers are many or callbacks are slow (PP-T28). A change manager is for several interdependent subjects, and a single subject uses a plain observer list (GOF-T70).
- **Check:** The notification mechanism matches the listener count and speed, Notify carries the subject and aspect, and handler comments name trigger and calling thread.

### 28. Make subject state consistent before notifying

Observers read the subject while they update, so a notification sent halfway through a change shows them a state that never really existed. Finish every field change first, then notify. [GOF-T69]

- **Do:** Make Notify the last step of each subject operation, and document which methods notify.

```python
def move(self, x, y):
    self.x = x
    self.y = y
    self.notify("position")   # last: observers see x and y together
```

- **Check:** No Notify call sits between field assignments in a subject method.

### 29. Model ordered event handling as a state machine

When code parses ordered message sequences or runs a multi-step workflow driven by events, describe it as a finite state machine with a transition table, which shows exactly which event sequences it accepts. Design Patterns uses a table when transitions are fixed data, and FP in Scala models each step as a pure function from state and input to new state and output. [PP-T29, GOF-T63, FPS-T37]

- **Do:** Map each pair of current state and event to a next state, plus an action where the workflow needs one. Keep the transition logic free of mutation where possible, returning the next state and output.
- **Not when:** State machines sequence events but do not solve every event problem (PP-T29). Design Patterns does not use a table when transitions need attached actions or when lookup speed is critical (GOF-T63), so see the tension on [tables versus state objects](#transition-table-or-state-objects).
- **Check:** One table or pure transition function defines every allowed transition, and state classes, if any, hold only behavior.

### 30. Send unlisted events to a named error state

An event with no defined transition should move the machine to an explicit error state, not leave it where it was, so unexpected input is never silently ignored. This matches Pragmatic Programmer's advice to stop on impossible states. [PP-T30, PP-T16]

```python
TRANSITIONS = {
    ("waiting", "start"): ("running", start_job),
    ("running", "done"):  ("finished", report),
}
def step(state, event):
    next_state, action = TRANSITIONS.get((state, event), ("error", log_unexpected))
    action(state, event)
    return next_state
```

- **Do:** Give the lookup a default that leads to the error state, and test an unlisted event.
- **Check:** Missing transitions lead to a named error state, and a test sends an event the table does not list.

### 31. Store long workflow state outside the process

A workflow that spans many steps, such as a sign-up with several form stages, loses its place if the process restarts and its state lives only in memory. Save the current state to external storage so the next event can resume it. [PP-T31]

- **Do:** Persist the state after each transition, and load it when the next event arrives.
- **Check:** Current workflow state is written to storage, not kept only in memory.

For event delivery between services and durable event logs, see [data-systems](data-systems.md) and [domain-modeling](domain-modeling.md).

## Playbooks

### When you are tempted to add a pattern

1. Name the variation the pattern would absorb, and the caller, requirement or failing test that needs it now. If there is none, go to step 2, and build the plain version unless an exception there applies. [GOF-P4, TDD-P9, CC-T77, PP-T71]
2. Check the exceptions: a confirmed growth direction or a hook that is very likely to be needed, a long-lived system with a foreseeable change, or clients that must avoid recompiling. If the choice shapes the whole system, reason it through carefully before coding. [CC-T77, GOF-P6, GOF-P4, TDD-P9]
3. List the aspects that must vary and shortlist patterns that isolate each one. [GOF-T13, GOF-P2]
4. Read each candidate's applicability and consequences, and compare the closest two by intent, not diagram shape. [GOF-T02, GOF-T03]
5. Name the classes with a domain term plus the role. [GOF-T14]
6. Write the trade-offs, the rejected alternative and the modules a likely change touches into the PR. [GOF-P5, POSD-P5, PP-T68]

### When a type switch keeps growing

1. Decide whether the branches follow a client's choice of algorithm, the object's own changing state, or a fixed type of the object. [GOF-T64, GOF-T18, REF-T58]
2. Keep the switch if it has few cases unlikely to grow, behavior changes more often than types, or only one function uses it. [CC-T38, REF-T58, REF-T69]
3. Otherwise create the variant classes and one factory that selects them, keeping any unavoidable switch inside that factory. [REF-T59, CC-T39]
4. Move each branch into its class, keeping the shared rule and default in the base. [REF-T60, GOF-T05]
5. Use delegation rather than subclasses if the variant changes during the object's life or a second axis of variation appears. [REF-T70, GOF-T09]
6. Share stateless strategy or state objects across contexts. [GOF-T65, GOF-T53]

### When you add undo and redo

1. Make each user operation a command with Execute and Unexecute, invoked through Execute only. [GOF-T33, GOF-T37]
2. In Execute, save the prior values the command changes, and restore them in Unexecute. [GOF-T35]
3. Where reversing cannot restore connected objects exactly, capture a memento the caller holds unread. [GOF-T72, GOF-T71]
4. Weigh snapshot size and frequency against copy cost, and record the result. [GOF-T72]
5. Keep executed commands in one ordered list with a current position, leaving out no-op and save-and-quit commands. [GOF-T36]
6. Check that undo and redo each move one position in that one list. [GOF-T36]

### When you wrap an existing class or third-party API

1. Decide whether the interface stays (decorator), changes (adapter), becomes a new simple subsystem entry (facade), or gains access control (proxy). [GOF-T57]
2. For a vendor or platform API, put every call behind one adapter layer you own. [PP-T12, GOF-T17, CC-T51]
3. Expose only the operations your code needs, each forwarded in a single call, with vendor types and error codes kept inside. [GOF-T41, PP-T13]
4. If the wrapper forwards most calls unchanged, keeps no external interface unchanged and isolates no vendor or platform API, apply the decision rule on [forwarding wrappers](#is-a-forwarding-wrapper-worth-its-layer). [POSD-T43, POSD-T04]
5. Record what you assume about the wrapped code's behavior at the call site. [PP-T67]

### When objects must react to another object's changes

1. Count listeners and estimate how slow their work is. A few fast in-process listeners can use a callback list. [PP-T28]
2. For many dependents, define an abstract observer interface on the subject. [GOF-T15]
3. Make each subject operation finish its state changes before notifying. [GOF-T69]
4. When several interdependent subjects change together, add one change manager. [GOF-T70]
5. When peers interact in complex two-way ways rather than one change fanning out, use a mediator instead. [GOF-T61]
6. Document each handler's trigger and calling thread. [POSD-T56]

### When you model an event-driven workflow

1. List the states and events, and write the transitions as a table or a pure transition function. [PP-T29, FPS-T37]
2. Route every unlisted event to a named error state. [PP-T30]
3. If transitions need growing criteria or rich per-state behavior, move behavior into state objects that choose their successors. [GOF-T62, GOF-T18]
4. Persist the current state if the workflow spans more than one request or process lifetime. [PP-T31]
5. Test at least one unlisted event and confirm it reaches the error state. [PP-T30]

## Where the books disagree

### When is a pattern worth adding before it is needed?

- **TDD, Clean Code, Refactoring, Pragmatic Programmer:** Add a class, interface or hook only when a failing test, a current caller or a stated requirement needs it, and delete speculative machinery. [TDD-P9, TDD-T18, CC-T77, REF-T85, PP-T71]
- **Design Patterns:** Start simple too, but long-lived systems still need foreseeable changes planned ahead, and an abstraction for one implementation can be right when clients must avoid recompiling. [GOF-P6, GOF-P4]
- **POSD:** When a feature first needs an abstraction, design its core operations together for several uses rather than piecemeal, still adding no operation without a caller. This does not apply when only quick working code matters, or when the class would be so general that current needs become hard to meet. [POSD-T46]
- **Decide:** With no caller, test or requirement for the variation, do not add the pattern. Add it ahead of use only when growth is a confirmed direction or very likely, the system is long-lived and the change is foreseeable, or clients must avoid recompiling. When the choice shapes the whole system, reason it through carefully before coding. Once an abstraction is needed, design its core operations together but keep every operation tied to a caller, unless only quick working code matters. [CC-T77, GOF-P6, GOF-P4, TDD-P9, POSD-T46]

### Should shared services be singletons or parameters?

- **Design Patterns:** When exactly one instance must exist, the class should own it and expose one static accessor, which is better controlled than a global. Its change manager is reached through a global accessor. [GOF-T26, GOF-T70]
- **Pragmatic Programmer:** Give routines their configuration, state and services as parameters, not through globals or singletons, because explicit parameters expose links and make tests easy to set up. [PP-T27]
- **Legacy Code:** Existing singletons get a static setter or a reset method so tests can control them. [WELC-T25, WELC-T26]
- **Decide:** Use a singleton only when one instance is a real requirement. In new code, pass that instance to the routines that use it as a parameter rather than having them call the accessor, and give it no public mutable fields. For singletons already in code you must test, use the setter when the singleton depends on external resources or lacks state-setup methods, and the reset when its public methods can set up any state tests need. [GOF-T26, PP-T27, WELC-T25, WELC-T26] See [legacy-code](legacy-code.md) and [testing](testing.md).

### Is a forwarding wrapper worth its layer?

- **Design Patterns, Clean Code, Pragmatic Programmer:** Adapters forward with single-call methods, decorators wrap a component without changing its class, and vendor APIs live behind your own wrapper. [GOF-T41, GOF-T30, GOF-T47, CC-T51, PP-T12]
- **POSD:** Remove methods that only pass their arguments on, and avoid a decorator that forwards most calls unchanged. Add a broadly useful feature to the base class or build it standalone. [POSD-T04, POSD-T43]
- **Decide:** Keep a forwarding wrapper when an external interface must stay unchanged, when it isolates a vendor or platform API, or when it carries one optional feature that only some objects need and that may be combined at run time. Otherwise, if it forwards most methods without adding behavior and the feature is broadly useful, fold the feature into the base class or a standalone module. If an existing decorator already wraps the same object, add the feature there. [POSD-T04, POSD-T43, GOF-T47, GOF-T58, PP-T12] More on shallow modules is in [module-design](module-design.md).

### Subclass the variant or delegate to it?

- **Design Patterns, Pragmatic Programmer:** Favor composition, select run-time behavior by assigning a collaborator, and prefer interfaces to subclassing for interchangeable behavior. [GOF-P3, GOF-T09, PP-T33]
- **Legacy Code, Refactoring, Design Patterns:** A subclass that overrides one differing method is a quick, testable variant. Type-code switches can become subclasses, and the template method uses inheritance on purpose. [WELC-T20, REF-T58, GOF-T66]
- **Decide:** Subclass when the variation runs along one axis, is fixed for the object's life, and overrides only the method that differs. Do not subclass when several subclasses would each need that same override. Move to a delegate when several variations must combine, the variant must change at run time, the subclass depends on parent internals, or it refuses parent operations in a way that causes real confusion. Refactoring accepts starting with inheritance and switching once it causes problems. [WELC-T20, REF-T70, REF-T71, GOF-T09, GOF-P3]

### Replace a conditional with objects or keep it?

- **Design Patterns, Clean Code, Refactoring:** Many behavior-selecting conditionals signal strategies or polymorphic classes, so a new type adds a class instead of edits to every switch. [GOF-T64, CC-T38, REF-T58]
- **The same books' caveats:** Few states with little logic are more compact as branches, and a switch with few stable cases, or one used by a single function, can stay. [GOF-T18, CC-T38, REF-T58, REF-T69]
- **Decide:** Replace the conditional when the same switch appears in several places, new types keep arriving, or many behaviors differ by type. Keep it when it has few cases unlikely to grow, appears in one function, or when behavior changes more often than the types. [CC-T38, REF-T58, REF-T69, GOF-T18]

### Transition table or state objects?

- **Pragmatic Programmer:** Describe event workflows with a transition table that maps each state and event to a next state and an action. [PP-T29]
- **Design Patterns:** Use a table only for fixed transitions edited as data with no actions, and not where lookup speed is critical. Use state objects that choose their successors when criteria must grow. [GOF-T63, GOF-T62]
- **FP in Scala:** Model the machine as a pure function from state and input to new state and output. [FPS-T37]
- **Decide:** For fixed transitions with no actions, use a table, unless table lookup speed is critical. For transition criteria that must keep growing, or rich behavior per state, use state objects. For an event-sequence workflow whose transitions trigger actions, the books part ways and give no deciding condition, so follow the codebase's existing convention, and in either form route unlisted events to an error state. [GOF-T63, GOF-T62, PP-T29, PP-T30]

### Bare callback or object?

- **Pragmatic Programmer:** A plain list of callback functions is enough for a few in-process listeners. [PP-T28]
- **Design Patterns:** Use command objects instead of bare functions when a request needs state, undo or reuse, and an abstract observer interface for many dependents. [GOF-T34, GOF-T15]
- **Decide:** Use bare callbacks for a few fast in-process listeners whose requests need no state, undo or reuse. Use command objects when the request must remember its target, be undone or be shared, and an observer interface when there are many dependents. For slow callbacks, the books say only that a plain list blocks the source, and they name no replacement. [PP-T28, GOF-T34, GOF-T15]

## Review checklist

- [ ] Each new pattern, interface or hook has a current caller, and the PR names the variation and requirement behind it. [GOF-P4, CC-T77, REF-T85]
- [ ] The PR names the closest rejected pattern and the trade-offs in space, time or flexibility. [GOF-T03, GOF-P5]
- [ ] Pattern classes are named with a domain term plus the role. [GOF-T14]
- [ ] Fields, parameters and return types use interfaces, and concrete classes appear only in creation code. [GOF-P1, GOF-T22]
- [ ] Run-time variation is held in a collaborator reference, not a subclass per combination. [GOF-P3, GOF-T09]
- [ ] Any type switch that picks a concrete class lives in one factory or in Main. [CC-T39, CA-T21]
- [ ] A singleton has one accessor, a non-public constructor and no public mutable fields, and new code receives it as a parameter. [GOF-T26, PP-T27]
- [ ] Each wrapper is clearly a decorator, adapter, facade or proxy, and none forwards most methods without a stated reason. [GOF-T57, POSD-T43]
- [ ] Vendor and platform calls appear only inside one adapter layer. [GOF-T17, PP-T12]
- [ ] Where child operations are declared on the component root, composite leaves fail loudly on Add and Remove, and clients contain no leaf-or-container type checks. [GOF-T46, GOF-T16]
- [ ] Shared flyweight, state or strategy objects hold no per-context mutable fields. [GOF-T49, GOF-T53, GOF-T65]
- [ ] Each proxy class handles one access concern. [GOF-T55]
- [ ] Undoable commands save prior state in Execute, and the history excludes no-op commands. [GOF-T35, GOF-T36]
- [ ] Template-method subclasses override only hooks and never need to call the parent. [GOF-T67]
- [ ] Visitors are used only over an element hierarchy that rarely changes. [GOF-T40]
- [ ] Every handler chain has a defined outcome at its end, and a test sends each request type to the head. [GOF-T59]
- [ ] Each mediator colleague references only the mediator. [GOF-T61]
- [ ] Notify is called only after all state changes in the subject method. [GOF-T69]
- [ ] Event handlers document their trigger and calling thread. [POSD-T56]
- [ ] Each state machine lists its transitions in one place, sends unlisted events to a named error state, and has a test for one unlisted event. [PP-T29, PP-T30]
- [ ] Multi-step workflow state is persisted, not held only in memory. [PP-T31]

## More entries in this area

- `GOF-T04` — Keep data, presentation and input handling apart: when building a user interface over changing application data, keep model classes free of view and controller references.
- `GOF-T07` — Inherit C++ interfaces publicly, implementations privately: C++ only, and not in Smalltalk-style languages where inheritance means only implementation sharing.
- `GOF-T11` — Create and release owned parts with their owner: without garbage collection, the owner frees each part it owns once, but not shared immutable leaves.
- `GOF-T27` — Give glyphs draw, bounds and hit-test operations: for document or drawing element trees, resolve clicks by asking each element.
- `GOF-T73` — Map grammar rules to classes for small grammars: one class per rule for a simple language, and a parser generator when the grammar is complex.
- `REF-T81` — Turn a complex function into a command object: when tangled locals block extraction, though plain functions usually suffice; see [refactoring](refactoring.md).
- `REF-T67` — Replace a sentinel with a special-case object: when many clients check the same marker value and respond alike.
- `POSD-T42` — Give several variants one shared interface: when several implementations do the same job, such as drivers.
- `CA-T08` — Invert dependencies through interfaces: when high-level policy must call low-level code; see [architecture](architecture.md).
