# Design Patterns — techniques

### GOF-T01: Describe each design by name, problem, solution, consequences
Write each reusable design entry with its name, problem, solution and consequences.
- **Why:** Uniform sections make designs comparable side by side.
- **When:** Writing a catalog entry or design note that others will reuse.
- **Check:** Each pattern entry in the docs has name, problem, solution and consequences sections.
- **Source:** ch. 1, 6

### GOF-T02: Read applicability and consequences first
Before adopting a pattern, read its applicability (situations it fits) and consequences (trade-offs).
- **Why:** Those parts show quickly whether the pattern fits.
- **When:** Deciding whether to adopt a pattern for a concrete design decision.
- **Check:** The PR description states which applicability conditions the change meets.
- **Source:** ch. 1, 6

### GOF-T03: Compare candidate patterns by intent, not shape
Compare patterns that share a goal, and choose by the intent each one serves.
- **Why:** Similar diagrams can serve different intents, so shape misleads.
- **When:** Two patterns with similar goals or class shapes compete for one problem.
- **Check:** The PR description names the closest alternative pattern and why it was rejected.
- **Source:** ch. 1

### GOF-T04: Keep data, presentation and input handling apart
Put application data, its presentation and its input handling in separate objects.
- **Why:** Input behavior can change while presentation stays the same.
- **When:** Building a user interface over application data that can change.
- **Check:** Model classes hold no references to view or controller classes.
- **Source:** ch. 1

### GOF-T05: Put algorithm variants behind strategy objects
Encapsulate each algorithm variant in a strategy object that shares one interface.
- **Why:** Variants can be replaced statically or at run time without touching clients.
- **When:** Many algorithm variants exist, or the algorithm must change at run time.
- **Check:** Each variant is its own class behind a shared interface, and adding one changes neither it nor the context.
- **Source:** ch. 1, 2, 5

### GOF-T06: Wrap objects behind the same interface
Make each decorator or proxy expose the same interface as the object it wraps.
- **Why:** Clients use wrapped and plain objects interchangeably.
- **When:** Adding behavior around an object or controlling access to it.
- **Not when:** A protection proxy may refuse operations, so its interface can be a subset.
- **Check:** Decorators match the wrapped operation signatures, and a protection proxy may omit operations it refuses.
- **Source:** ch. 1, 2, 4

### GOF-T07: Inherit C++ interfaces publicly, implementations privately
In C++, inherit interface bases publicly and implementation bases privately.
- **Why:** Public inheritance exposes only the interface, and private inheritance hides reused code.
- **When:** Writing C++ interface inheritance, or implementation inheritance chosen over composition (GOF-P3).
- **Not when:** Smalltalk, where inheritance means only implementation sharing.
- **Check:** Interface bases contain only pure virtual functions, and implementation bases use private inheritance.
- **Source:** ch. 1, 4

### GOF-T08: Keep interface inheritance separate from code reuse
Make each base class interface-only or a deliberate code-sharing base.
- **Why:** Subclasses that hide parent operations break the interface callers rely on.
- **When:** Designing a class hierarchy or extending a base class.
- **Not when:** The parent's internal representation may change (GOF-P3).
- **Check:** Each base class is either interface-only or a deliberate code-sharing base.
- **Source:** ch. 1

### GOF-T09: Split class variation from object variation
Fix compile-time variation with subclasses or type parameters, and hold run-time variation in references.
- **Why:** Subclasses are fixed at compile time, but referenced objects can be swapped.
- **When:** Deciding whether a variation should be fixed by a class or changed by an object.
- **Check:** Behavior that must change at run time is held in an object reference, not a subclass.
- **Source:** ch. 1

### GOF-T10: Delegate to a swappable object that refers back
Forward operations to a delegate and pass the receiver along so the delegate can refer back to it.
- **Why:** Replacing the delegate changes behavior without editing the receiver's class.
- **When:** Behavior must change at run time, as in State or Strategy.
- **Not when:** Forwarding that follows no standard pattern complicates the design more than it simplifies it.
- **Check:** Delegate operations receive the receiver, and each delegate is a State or Strategy object.
- **Source:** ch. 1

### GOF-T11: Create and release owned parts with their owner
Create owned sub-objects with their owner and release them when the owner is released.
- **Why:** Without garbage collection, each owned part must be freed exactly once by its owner.
- **When:** No garbage collector exists, and each part belongs to one composite or aggregate.
- **Not when:** Shared, immutable leaf objects must not be deleted with one parent.
- **Check:** The owner's release routine frees each child it owns, but not objects it merely refers to.
- **Source:** ch. 1, 4

### GOF-T12: Document run-time collaboration apart from class structure
Document the collaborating object instances that interact at run time, not only the classes.
- **Why:** Class code does not reveal the run-time network of collaborating objects.
- **When:** Explaining a running system, or composing many objects into one behavior.
- **Check:** The change documents collaborating object instances, indirection patterns, and run-time configuration points.
- **Source:** ch. 1

### GOF-T13: Choose a pattern by the aspect to vary
Pick a pattern by naming the design aspect you need to change without redesigning.
- **Why:** Naming the likely change shows what the pattern must absorb.
- **When:** You know what must stay changeable but not which pattern fits.
- **Check:** The PR description lists each likely change and the pattern chosen to absorb it.
- **Source:** ch. 1

### GOF-T14: Name participants after application terms
Name each pattern participant with an application term plus its pattern role.
- **Why:** A pattern is abstract, so each application class adapts its roles.
- **When:** Turning pattern roles into application classes.
- **Check:** Class names combine an application term with the pattern role, such as LayoutStrategy.
- **Source:** ch. 1, 6

### GOF-T15: Notify dependents through an abstract observer interface
Let a subject notify registered observers through one abstract observer interface.
- **Why:** Dependents update without the changed object knowing their details.
- **When:** One object's state change must update many dependent objects.
- **Check:** Notify passes the subject and changed aspect, and holds no observer count or per-observer logic.
- **Source:** ch. 1, 5

### GOF-T16: Use one component type for leaves and containers
Define one abstract component class for leaves and containers, and let clients call it uniformly.
- **Why:** Clients need no type tests to separate single objects from groups.
- **When:** Clients must handle individual objects and groups through one interface.
- **Check:** Leaves and containers share one abstract base, clients have no type checks, and Add rejects disallowed children.
- **Source:** ch. 1, 4

### GOF-T17: Confine platform API calls to one adapter layer
Put operating system and platform API calls behind your own abstraction layer.
- **Why:** Platform dependence stays in one layer, so the rest ports more easily.
- **When:** Code calls platform or operating system APIs directly across many modules.
- **Check:** Platform API calls appear in one layer or adapter module, not throughout the code.
- **Source:** ch. 1, 2

### GOF-T18: Represent each entity state as its own object
Represent each state of an entity as a separate object that carries that state's behavior.
- **Why:** Transitions become visible object replacements, not hidden data assignments.
- **When:** An entity's behavior depends on its own state, which changes over time.
- **Not when:** Few states with little logic, since the extra classes are then less compact.
- **Check:** State-specific behavior sits in separate state classes, not in branches on one state field.
- **Source:** ch. 1, 5

### GOF-T19: Adapt a class to the interface you need
Wrap an existing class in an adapter that exposes the interface your code expects.
- **Why:** The existing class stays unchanged, even when its source cannot be modified.
- **When:** A reusable class fits your needs except that its interface does not match.
- **Not when:** You write the reusable class yourself (GOF-T42, GOF-T43).
- **Check:** A new class implements the expected interface and delegates to the existing class.
- **Source:** ch. 1, 4

### GOF-T20: Create objects through a factory, not class names
Create objects through a factory object instead of naming concrete classes at each call site.
- **Why:** Creation then depends on abstract types, not class names.
- **When:** Object creation is complex, or the product kind varies at run time.
- **Check:** Varying product kinds go through a factory, and fixed, simple products may be built directly.
- **Source:** ch. 1, 2, 3

### GOF-T21: Select one concrete factory before creating products
Choose one concrete factory before creating products, and create each family's products through it.
- **Why:** Products from different families are then never mixed.
- **When:** A system is configured with one of several families of related products.
- **Check:** Each client obtains its products from a single factory instance, chosen in one place.
- **Source:** ch. 2, 3

### GOF-T22: Expose product interfaces, not implementation classes
Expose only abstract product and factory types, and keep concrete product names inside factories.
- **Why:** Implementations can change without breaking library users.
- **When:** A class library is provided to others, or clients use a product family.
- **Check:** Public headers expose abstract product types, and client sources name no concrete product class.
- **Source:** ch. 3

### GOF-T23: Use one parameterized make operation for kinds
Replace per-product operations with one make operation whose parameter names the product kind.
- **Why:** A new product kind then needs only a new identifier.
- **When:** Product kinds change often and the language is dynamically typed.
- **Not when:** The language is statically typed and products cannot be safely coerced to their concrete types.
- **Check:** The factory exposes one make operation whose parameter selects the product kind.
- **Source:** ch. 3

### GOF-T24: Create products in a dedicated overridable operation
Put each product creation in its own operation that subclasses can override.
- **Why:** Subclasses can then change how objects are created without changing other methods.
- **When:** A creator instantiates classes that subclasses or the application may change.
- **Not when:** Products must come from one family (GOF-T21), or classes are chosen at run time (GOF-T25).
- **Check:** Creation happens inside a dedicated operation, not inline in other methods.
- **Source:** ch. 3

### GOF-T25: Clone registered prototypes for run-time classes
Create objects by cloning a registered prototype instead of calling a constructor for a named class.
- **Why:** Cloning avoids a parallel creator class per product.
- **When:** Classes are specified only at run time, or a factory hierarchy would mirror the product hierarchy.
- **Not when:** A make operation keyed by kind name suffices (GOF-T23).
- **Check:** Creation code clones a registered instance, and no creator subclass exists for each product subclass.
- **Source:** ch. 3

### GOF-T26: Give the sole instance one well-known accessor
Make the class responsible for its only instance, reached through one static accessor.
- **Why:** Access is controlled at one point, unlike with globals.
- **When:** Exactly one instance must exist and clients need a single access point.
- **Check:** One static accessor returns the instance, the constructor is not public, and no global holds it.
- **Source:** ch. 3

### GOF-T27: Give glyphs draw, bounds and hit-test operations
Give every glyph, the base interface all document elements share, draw, bounds and point-intersection operations.
- **Why:** Clicks are resolved by asking each element, not by recomputing geometry.
- **When:** Defining the base interface of elements, or mapping a click to the element behind it.
- **Check:** The base glyph interface declares draw, bounds and point-intersection operations, and click handling calls them.
- **Source:** ch. 2

### GOF-T28: Give each child a reference to its parent
Store a parent reference in each child so it can inspect its surroundings.
- **Why:** Simple traversal and deletion then start from the child.
- **When:** A child's appearance or size depends on its position within its parent.
- **Not when:** Children shared between composites cannot hold one parent reference.
- **Check:** Parent references are assigned only in Add and Remove, and each child exposes its container.
- **Source:** ch. 2, 4

### GOF-T29: Reach children through operations, not storage
Reach children through child, insert and remove operations, so the storage can change.
- **Why:** Arrays or lists can change without touching callers.
- **When:** Parent elements store children in arrays, linked lists, or other structures.
- **Not when:** Children live in a plain array and integer index access is adequate.
- **Check:** Drawing and layout code iterates children through element operations, not container types or indexes.
- **Source:** ch. 2

### GOF-T30: Add responsibilities by enclosing objects in wrappers
Add a responsibility to one object by enclosing it in a decorator, not by changing its class.
- **Why:** The wrapped class stays unchanged, and wrappers can be added or removed at run time.
- **When:** Objects need added behavior, such as borders or scrolling, that others lack.
- **Check:** A decorator holds a component reference, conforms to its interface, and calls the wrapped operation first.
- **Source:** ch. 2, 4

### GOF-T31: Platform implementations come from a known factory
Obtain each window's platform implementation from a well-known factory, not from a hard-coded class.
- **Why:** The window system can change without rebuilding windows.
- **When:** The window system must be selectable at run time or per deployment.
- **Check:** Window constructors obtain implementations from a factory, not from a hard-coded class name.
- **Source:** ch. 2, 4

### GOF-T32: Develop abstraction and implementation hierarchies separately
Keep the abstraction hierarchy and its implementation hierarchy separate, linked by a reference.
- **Why:** Each hierarchy can then evolve without changing the other.
- **When:** Both the abstraction and its platform variants are expected to change over time.
- **Check:** Changing a platform implementation class requires no edit to any abstraction class.
- **Source:** ch. 2, 4

### GOF-T33: Encapsulate each request as a command object
Represent each user operation as a command object with an Execute operation.
- **Why:** Buttons, menus and keys then share one invocation path.
- **When:** One operation is reachable from several controls, or invokers must not know the receiver.
- **Check:** Menu items and buttons hold command objects, may share one, and call Execute with no per-operation menu subclass.
- **Source:** ch. 1, 2, 5

### GOF-T34: Use commands instead of bare callbacks
Parameterize UI items with command objects, not bare functions, when a request needs state, undo or reuse.
- **Why:** A command object does the job of a callback, in object-oriented form.
- **When:** A request must remember its target, such as which font it applies to.
- **Check:** Stateful or undoable requests are command classes, not free functions passed to widgets.
- **Source:** ch. 2, 5

### GOF-T35: Store undo state inside the command during Execute
Have each undoable command save its prior state during Execute and restore it in Unexecute.
- **Why:** Restoring saved values returns objects to their exact original state, avoiding undo drift.
- **When:** A command modifies document content that users may want to revert.
- **Not when:** Reversing the change cannot restore connected objects exactly (GOF-T72).
- **Check:** Each undoable command saves prior state in fields set during Execute and reads them in Unexecute.
- **Source:** ch. 2, 5

### GOF-T36: Keep executed commands in one ordered history
Record executed commands in one ordered list, with a current position that moves back to undo and forward to redo.
- **Why:** Undo and redo then walk one sequence both ways.
- **When:** Users need undo and redo across a sequence of operations.
- **Check:** Undo and redo move one position in one list, and no-op or save-and-quit commands never enter it.
- **Source:** ch. 2, 5

### GOF-T37: Let callers invoke only a command's Execute
Let a command delegate some or all of its work, while callers invoke only Execute.
- **Why:** A sender depends on the command interface, not the receiver's class.
- **When:** One request spans many classes, or a sender must work with several receivers.
- **Check:** UI code calls the command's Execute and never calls the target classes directly.
- **Source:** ch. 2, 5

### GOF-T38: Separate traversal from per-element analysis
Keep traversal loops in iterator classes, and put per-element analysis in separate objects.
- **Why:** Traversal code is written once, not in each analysis.
- **When:** Several analyses need the same traversal, treating every element alike (GOF-T40 otherwise).
- **Check:** The aggregate only creates iterators holding traversal state, analysis classes contain no loops, and iterators serve several analyses.
- **Source:** ch. 2, 5

### GOF-T39: Add each traversal order as an iterator subclass
Implement each new traversal order or filter as its own iterator subclass.
- **Why:** Element classes and enumerations then stay unchanged.
- **When:** A collection needs forward, reverse, or filtered traversal.
- **Check:** Traversal variants are iterator classes, not aggregate methods or new traversal enum cases.
- **Source:** ch. 2, 5

### GOF-T40: Put analysis logic in visitors, not elements
Put each analysis in a visitor class that elements accept, rather than in element methods.
- **Why:** New analyses need no edits to stable element classes.
- **When:** Many analyses must treat element kinds differently over a stable structure.
- **Not when:** The element class hierarchy changes often, since each change touches every visitor.
- **Check:** Analysis logic lives in visitors that declare an operation per element class, and elements have none.
- **Source:** ch. 1, 2, 5

### GOF-T41: Adapt only the adaptee operations you need
Adapt only the smallest subset of adaptee operations that the target needs, and forward the ones the adaptee already has.
- **Why:** A narrow adapter depends on few adaptee operations.
- **When:** An adaptee has many operations, but the target needs only a few of them.
- **Check:** The adapter depends on a few adaptee operations, and forwarding methods are single calls.
- **Source:** ch. 4

### GOF-T42: Plug adaptation in through abstract operations
Declare abstract adaptation operations in a generic class, and have each application subclass implement them.
- **Why:** Subclasses supply adaptation, so the generic class depends only on abstract operations.
- **When:** A generic class needs an adapter, and each application can define a subclass.
- **Check:** The generic class declares abstract adaptation operations that each concrete subclass overrides.
- **Source:** ch. 4

### GOF-T43: Give reusable classes adaptation hooks
Put adaptation hooks or per-request callables inside a reusable class, not in shared base classes.
- **Why:** Applications then need not match the reusable class's interface.
- **When:** A reusable class must work with classes whose interfaces are unrelated and unforeseen.
- **Not when:** The class serves one application, where one interface is reasonable, or each application can subclass it (GOF-T42).
- **Check:** The reusable class exposes hooks or callables, and applications do not subclass a shared base.
- **Source:** ch. 4

### GOF-T44: Split objects that vary along two dimensions
Split an object into an abstraction and an implementor linked by a reference, not inheritance.
- **Why:** Two hierarchies replace one whose leaves combine both variations.
- **When:** A class hierarchy grows in two directions and multiplies its classes.
- **Check:** Two hierarchies replace one, and the abstraction holds an implementor reference.
- **Source:** ch. 4

### GOF-T45: Keep implementor classes behind the abstraction
Keep implementor classes behind the abstraction, in a private header that clients never include.
- **Why:** Changing implementors then does not force client recompilation.
- **When:** Binary compatibility must survive changes to an implementation library, as with separate C++ headers.
- **Check:** Client sources include only abstract headers, and implementors are declared in a private header.
- **Source:** ch. 4

### GOF-T46: Give leaves safe defaults for child operations
Give leaves safe child defaults: Add and Remove fail, and child access returns nothing.
- **Why:** Silent no-ops would hide misuse of a leaf.
- **When:** Child operations are declared on the component root and a leaf receives one.
- **Check:** Base-class Add and Remove throw or report failure, and leaves return an empty child list.
- **Source:** ch. 4

### GOF-T47: Build optional features from small decorators
Keep the base component lean, and put each optional feature in its own decorator.
- **Why:** Unused features add no weight to the core.
- **When:** A component class would otherwise accumulate features that most clients never use.
- **Not when:** Only one optional feature exists, and a single concrete decorator is simpler.
- **Check:** The base class holds core behavior only, and optional features live in separate decorator classes.
- **Source:** ch. 1, 4

### GOF-T48: Give a subsystem one simplified entry point
Give a complex subsystem one facade class that offers a simplified interface.
- **Why:** Subsystem classes can then change behind one stable entry.
- **When:** Most clients need only routine operations from a subsystem with many classes.
- **Check:** Common client code calls one facade class, and implementation classes stay out of client sources.
- **Source:** ch. 1, 4

### GOF-T49: Share only objects whose state is context-free
Share fine-grained objects from a pool, but only when their state does not depend on context.
- **Why:** Sharing saves memory when huge numbers of small objects strain it.
- **When:** Considering sharing objects that will appear in several places at once.
- **Check:** The shared class has no fields varying by location, parent, or client, and no code compares them by reference.
- **Source:** ch. 1, 4

### GOF-T50: Separate intrinsic from extrinsic state
Keep context-independent state in the shared object, and pass context-dependent state in from outside.
- **Why:** Per-object context data would otherwise block sharing.
- **When:** Objects hold position, style, or other context data that prevents sharing.
- **Check:** Shared objects hold only intrinsic fields, and position or style arrives as a parameter.
- **Source:** ch. 4

### GOF-T51: Obtain flyweights from a keyed factory table
Obtain shared objects only from a factory that keeps them in a table keyed by intrinsic state.
- **Why:** Clients then reuse existing entries instead of creating duplicates.
- **When:** A small set of intrinsic keys, such as character codes, identifies the shared objects.
- **Check:** The factory returns existing table entries and creates new ones only for unseen keys.
- **Source:** ch. 4

### GOF-T52: Share leaves only and pass parents as arguments
Share leaf flyweights only, and have callers pass each leaf's parent in as an argument.
- **Why:** A shared leaf cannot keep one parent pointer, because it appears in several places.
- **When:** Flyweight leaves are combined with Composite into one hierarchy.
- **Check:** The factory caches leaf types only, and shared leaf methods receive their parent as an argument.
- **Source:** ch. 4

### GOF-T53: Implement stateless state and strategy objects as flyweights
Implement State and Strategy objects as shared flyweights when they hold no per-context data.
- **Why:** Stateless behavior objects can be reused across contexts.
- **When:** State or strategy objects define behavior and hold little per-context data.
- **Not when:** The state object holds instance variables that differ per context.
- **Check:** State or strategy classes have no mutable fields and are reused across contexts.
- **Source:** ch. 4, 5

### GOF-T54: Create the real subject only on first use
Replace an expensive object with a proxy that creates the real subject on first use.
- **Why:** Metadata requests need not load the real subject.
- **When:** Creating the object up front is costly, and it may never be needed.
- **Check:** The proxy creates the real subject inside the first request that needs it, and metadata getters return stored values.
- **Source:** ch. 4

### GOF-T55: Choose the proxy kind for the access problem
Pick the proxy kind by concern: virtual for costly creation, remote for another address space, protection for access rights, smart reference for bookkeeping.
- **Why:** Mixed concerns make one proxy's behavior unclear.
- **When:** A bare pointer cannot express the needed location, creation, access, or housekeeping behavior.
- **Check:** Each proxy class addresses one concern, such as remote location or access rights, not several.
- **Source:** ch. 4

### GOF-T56: Forward unknown method calls in dynamic languages
In a dynamically typed language, send each undefined method call through the forwarding hook, a catch-all, to the subject.
- **Why:** The proxy then needs no per-message methods.
- **When:** Writing a generic proxy in a dynamically typed language that has such a hook.
- **Not when:** Identity tests and some built-in messages bypass the hook, and the hook is slow.
- **Check:** A forwarding hook handles undefined calls by ensuring the subject exists, then calling it.
- **Source:** ch. 4

### GOF-T57: Tell facade, adapter and decorator apart by interface
Use a decorator when the interface stays, an adapter when it changes, and a facade for a new interface.
- **Why:** Keeping or changing the wrapped interface decides which wrapper pattern fits.
- **When:** Deciding which pattern a wrapper over existing objects represents.
- **Check:** Same operations make a decorator, changed operations an adapter, and a new subsystem interface a facade, but access control stays a proxy (GOF-T55).
- **Source:** ch. 4

### GOF-T58: Assemble wrapper chains from a varying decorator list
Assemble wrapper chains at run time from a varying list of decorators.
- **Why:** Responsibilities unknown at compile time need run-time assembly.
- **When:** The full set of responsibilities varies and is unknown until run time.
- **Not when:** A proxy suits a single, fixed relationship between the proxy and its subject.
- **Check:** Wrapper chains are assembled at run time from the decorator list.
- **Source:** ch. 4

### GOF-T59: Pass unhandled requests along a handler chain
Pass each request along a chain of handlers until one of them handles it.
- **Why:** The sender then needs no reference to a specific handler.
- **When:** Several objects might handle a request, and its handler is unknown in advance.
- **Check:** The chain end has a defined outcome, handlers forward declined requests, and a test sends each request type to the head.
- **Source:** ch. 5

### GOF-T60: Use parent links as chain successors
Use an existing parent reference as the successor link when it already forms the chain that handling needs.
- **Why:** No extra successor field has to be added and kept consistent.
- **When:** The object structure already links objects in the order that handling requires.
- **Not when:** The existing links do not match the chain, so redundant links are needed.
- **Check:** The successor is read from an existing parent field, not a new link.
- **Source:** ch. 4, 5

### GOF-T61: Route object interactions through a mediator
Let a mediator coordinate objects, so colleagues reference only the mediator.
- **Why:** Tangled mutual links become links to one coordinator.
- **When:** Peers interact in well-defined but complex ways, or a component depends on many collaborators (not one fanned-out change: GOF-T15).
- **Not when:** The mediator grows into a monolith with each new colleague rule.
- **Check:** Each colleague links to the mediator and to no other colleague.
- **Source:** ch. 5

### GOF-T62: Let states choose their successor states
Let each state subclass set its successor through a context operation.
- **Why:** Transition criteria can grow by adding state classes.
- **When:** Transition criteria are not fixed and should be easy to extend.
- **Not when:** Fixed transition criteria are simpler to keep in the context, or in a table (GOF-T63).
- **Check:** State subclasses set their successor by calling a context setter, and no state class names another except through the context.
- **Source:** ch. 5

### GOF-T63: Use transition tables for data-driven transitions
Map each state's inputs to successor states in a table when transitions should be data.
- **Why:** The State pattern models behavior, while a table focuses on transitions.
- **When:** The transitions are a fixed table of (state, input) pairs, edited as data, with no actions.
- **Not when:** Transitions need actions attached, or table lookup speed is critical.
- **Check:** A transition table maps (state, input) pairs to successor states, and state classes hold only behavior.
- **Source:** ch. 5

### GOF-T64: Replace behavior branches with strategy objects
Move each branch that selects behavior into its own strategy class, and delegate to the chosen one.
- **Why:** Many conditionals signal that strategies are needed.
- **When:** One class contains several branches that pick an algorithm the client selects, not the object's own state (GOF-T18).
- **Check:** Operations delegate to strategy objects, not type-code branches, and no context subclass differs only in its algorithm.
- **Source:** ch. 5

### GOF-T65: Keep shared strategies stateless
Make strategy objects stateless so that contexts share one instance, and keep algorithm data inside the strategy.
- **Why:** One shared instance avoids a strategy object per context.
- **When:** Many contexts would otherwise each create their own strategy object.
- **Not when:** The strategy must keep state across invocations.
- **Check:** Strategy classes have no mutable instance fields, and the context stores per-use state.
- **Source:** ch. 5

### GOF-T66: Fix the algorithm skeleton in a template method
Define the fixed steps of an algorithm in a base-class template method, and leave the varying steps as overridable operations.
- **Why:** The fixed order of steps is kept in one place.
- **When:** Subclasses share an algorithm but differ in some of its steps.
- **Check:** A base-class method calls abstract or overridable operations in a fixed order.
- **Source:** ch. 5

### GOF-T67: Expose hooks that limit subclass extension
Have the template method call hook operations at chosen points, so subclasses extend the algorithm only there.
- **Why:** The base class controls where extension is allowed.
- **When:** You need to control how subclasses extend a base algorithm, or subclasses could forget a parent call.
- **Check:** Subclasses override only hook methods, and no subclass must call a parent operation itself.
- **Source:** ch. 5

### GOF-T68: Let the parent class drive subclass hooks
Let the parent class call subclass operations, while subclasses supply the overrides.
- **Why:** Control stays with the base class, as class libraries need.
- **When:** Designing a class library whose base classes control subclass flow.
- **Check:** The base class controls the flow, and subclasses supply overrides.
- **Source:** ch. 5

### GOF-T69: Finish state changes before calling Notify
Make the subject's state consistent before it notifies observers.
- **Why:** Observers read the subject during update, so a partial state misleads them.
- **When:** A subject operation changes several fields before notifying.
- **Check:** Notify is the last step after all state changes, and subject methods document notification.
- **Source:** ch. 5

### GOF-T70: Route interdependent updates through one change manager
Route updates of interdependent subjects through one change manager, reached through a global accessor.
- **Why:** The manager maps subjects to observers and runs the update in one place.
- **When:** Several interdependent subjects change in one operation. One subject alone uses GOF-T15.
- **Check:** Subjects hold no observer lists, and the change manager holds the mapping.
- **Source:** ch. 5

### GOF-T71: Capture state in a memento clients cannot read
Capture an object's internal state in a memento that clients can store but not read.
- **Why:** Only the originator needs to see the state, so it stays encapsulated.
- **When:** State must be restorable for checkpoints or undo.
- **Not when:** Snapshots are expensive relative to how often they occur (GOF-T72).
- **Check:** Clients hold snapshots unread, and the caretaker, which stores mementos, only keeps and returns them.
- **Source:** ch. 5

### GOF-T72: Snapshot for undo when reversal cannot restore state
Store a snapshot for undo when reversing a change cannot restore the exact earlier layout.
- **Why:** Restoring a stored snapshot avoids the error of applying an imprecise inverse.
- **When:** Connected or constrained objects must return to exactly their prior state.
- **Not when:** Saving and restoring state is expensive relative to how often snapshots occur.
- **Check:** The change records snapshot size and frequency against the cost of copying.
- **Source:** ch. 5

### GOF-T73: Map grammar rules to classes for small grammars
Define one class per grammar rule and represent each sentence as a tree of those classes, but only for a small grammar.
- **Why:** A small grammar's hierarchy stays readable.
- **When:** A recurring problem can be expressed as sentences in a simple language.
- **Not when:** The grammar is complex, where parser generators are a better alternative.
- **Check:** Each grammar rule in the specification has a matching class, and the count stays small.
- **Source:** ch. 5

### GOF-T74: Dispatch each visit through Accept
Have each element's Accept call the visit method for its own class.
- **Why:** The visitor is never part of the objects it visits, so it arrives as a parameter.
- **When:** Adding operations without changing element classes in a single-dispatch language.
- **Not when:** The language supports double or multiple dispatch directly.
- **Check:** Visitors arrive as parameters, and each element's Accept calls its own visit method.
- **Source:** ch. 5

### GOF-T75: Keep commands alive to run later
Keep each command object alive so its execution can be queued, logged, or sent elsewhere.
- **Why:** The command keeps its request beyond the moment of use.
- **When:** A request must run at a different time or in a different process.
- **Not when:** The receiver cannot be identified across separate processes or program runs.
- **Check:** The command stores what it needs to run, without the original caller's context.
- **Source:** ch. 5
