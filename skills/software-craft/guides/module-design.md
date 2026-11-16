# Module design: complexity, interfaces, coupling, abstraction

This guide covers how to shape modules, classes, functions and APIs so that the next change stays cheap: how to judge complexity, how much to expose, where knowledge lives, how modules depend on each other, and when an abstraction earns its place. The single most important idea is that a design is judged by the effort a typical change needs, so each module should hide a decision behind an interface much simpler than what it hides, and no fact should need edits in more than one place.

**Read this when:** designing a new class, module, service or public API, adding a method or parameter to an existing interface, adding a dependency on a library or vendor service, deciding whether to add an interface, extension point or option, splitting or merging classes, finding the same format or rule in several files, reviewing a diff where a small change touched many modules, adding a subclass or new variant.

**Entry IDs** such as `WELC-T12` point to `../books/<book>/techniques.md` (T) or `principles.md` (P);
the prefix table is in [SKILL.md](../SKILL.md).

## Contents

- [Core rules](#core-rules)
- [Rules: interfaces and depth](#rules-interfaces-and-depth)
- [Rules: information hiding](#rules-information-hiding)
- [Rules: one place per piece of knowledge](#rules-one-place-per-piece-of-knowledge)
- [Rules: coupling and cohesion](#rules-coupling-and-cohesion)
- [Rules: volatile dependencies and configuration](#rules-volatile-dependencies-and-configuration)
- [Rules: abstraction, variants and subtypes](#rules-abstraction-variants-and-subtypes)
- [Playbooks](#playbooks)
- [Where the books disagree](#where-the-books-disagree)
- [Review checklist](#review-checklist)
- [More entries in this area](#more-entries-in-this-area)

## Core rules

### 1. Judge a design by the cost of a typical change

Complexity is whatever makes a system hard to understand and modify, not its size or feature count. Measure it by asking how much work and risk a small, typical change takes, and by listing the modules that a likely future change would touch under each option. Tidy First treats the cost of software as roughly the cost of changing it, and Clean Architecture judges architecture by the effort needed to change it, so prefer the design that keeps likely changes local. [POSD-P1, POSD-T01, PP-T68, TF-P5, CA-P7]

- **Do:** For each design option, write down the likely next change and the modules it would edit, and prefer the option that touches fewer. Name the future behaviors a design change makes possible, and spend the least effort that secures each one. [PP-T68, TF-P5]
- **Not when:** Do not equate fewer lines with less complexity, since a longer version can be simpler when it lowers the effort a reader needs. [POSD-P1]
- **Check:** A small change in the area edits one owning module, or its description says why it needs more. The PR or design note names the modules each option would touch and the future behaviors the change enables. [POSD-T01, PP-T68, TF-P5]

### 2. Treat a reader's confusion as a design defect

A reader sees complexity that the author no longer notices, so a reviewer's report that code is hard to follow is evidence of complexity even when the author finds it clear. Respond by changing the code or adding a comment, not only by replying in the review thread. [POSD-T02, POSD-P1]

- **Do:** Restructure or explain the code a reviewer found hard, using [readable code](readable-code.md) for naming and comments.
- **Check:** A review comment about unclear code is answered by a code or comment change in the diff, not only by a reply. [POSD-T02]

## Rules: interfaces and depth

### 3. Keep each interface much smaller than its implementation

A module is valuable in proportion to the functionality it hides behind its interface, and this holds for a function, a class, a subsystem or a service. A small interface limits what every caller must learn, while the implementation absorbs the hard work. A new public method, parameter or class is justified only when it adds behavior callers need and makes some caller simpler. [POSD-P2, POSD-T03, POSD-T05, POSD-T45]

- **Do:** Before adding a public method, parameter or small class, name the caller it simplifies. [POSD-T05, POSD-T45]
- **Not when:** Some shallow classes, such as the nodes of a linked list, cannot be avoided and are still useful. [POSD-P2]
- **Check:** The change adds only the public methods and types that a caller in this codebase needs, each adds behavior that existing methods do not provide, and the public surface stays small compared with the internal code. [POSD-T03, POSD-T05, POSD-P2]

### 4. Make the common call simple and hide rare options

Most callers should not need knowledge that only rare cases require. Give parameters defaults that fit the common use, keep rarely needed options out of the main API behind separate and clearly marked methods, and expose a tuning value only when callers know a better value than the module can work out itself. [POSD-T09, POSD-T38, POSD-T39]

- **Do:** Supply a default in code for each configuration key and parameter. Move options used by only a few callers into separate methods. Let the module derive values such as cache sizes or retry intervals from measurements or fixed logic. [POSD-T09, POSD-T38, POSD-T39]
- **Not when:** If the module can derive the value itself, expose no key or parameter at all rather than a defaulted one. Keep a detail visible when callers must inspect it to use a method correctly. Expose a setting when users know domain priorities the module cannot see, such as which requests are time-critical. [POSD-T09, POSD-T38, POSD-T39]
- **Check:** Typical usage needs no extra objects, flags or setup calls, the common API does not mention the rare option, and each configuration key is one the module could not derive. [POSD-T09, POSD-T38, POSD-T39]

### 5. Shape operations around the units callers manipulate

When callers must split, join or loop over internal pieces to perform one user-level operation, that logic gets repeated in every caller. Design operations at the unit callers work with. In a text or content API, prefer general operations, such as insert and delete at a position, over methods named after one user action, because action-named methods serve one caller and leave the others to rebuild the same logic. Keep feature-specific and user-interface behavior in top-level code so that lower layers stay reusable. [POSD-T55, POSD-T40, POSD-T41]

- **Do:** Give editing, collection and text APIs operations in caller units, give text and content APIs general insert and delete operations over positions or ranges, and push feature names up into feature code. [POSD-T40, POSD-T55, POSD-T41]
- **Check:** Callers do not split, join or loop over internal units for one user operation, methods take general positions rather than user-action names, and general or low-level modules contain no names or behavior belonging to one feature. [POSD-T55, POSD-T40, POSD-T41]

### 6. Pull unavoidable complexity down into the owning module

When some complexity cannot be removed, let the module that owns it absorb it, even if that means more work for the module's author. Callers then need less knowledge and handle fewer special cases. The module should resolve hard conditions, ordering rules and defaults itself, and deal with a failure at the lowest layer that can recover from it. [POSD-P4, POSD-T09, POSD-T11]

- **Do:** Handle ordering rules, defaults and recoverable low-level failures inside the module, so higher layers never see them. See [errors and contracts](errors-and-contracts.md) for which failures to mask and which to report. [POSD-P4, POSD-T11]
- **Not when:** Do not pull all of the application into one class, and move logic down only when it is closely related to that module. Do not mask a failure when callers need the information, such as whether messages were lost or a peer really failed. [POSD-P4, POSD-T11]
- **Check:** Callers do not handle complexity that the module could hide, and the public interface declares no exception for a condition the module recovers from itself. [POSD-P4, POSD-T11]

### 7. Remove layers that only forward calls

A method whose body passes its arguments straight to another method adds an interface that teaches nothing and hides no decision. The same holds for a class whose methods mostly delegate, and for a decorator that forwards most of its calls unchanged. Callers should reach the object that does the work, and a broadly useful feature belongs in the base class or in a standalone module rather than in a forwarding wrapper. [POSD-T04, POSD-T43, REF-T45, REF-T46, POSD-P2]

- **Do:** Inline pass-through methods, let clients call the working object, and remove the delegating accessor once unused. The [refactoring](refactoring.md) guide has the mechanics. [POSD-T04, REF-T45, REF-T46]
- **Not when:** Keep a forwarding wrapper or decorator when an external interface must stay unchanged, and add a feature to an existing decorator of the same object when one exists. Keep forwarders that are overridden, and keep a delegate left in place on purpose while callers move or while a renamed published function stays available. Some delegation is good encapsulation. A wrapper that isolates a vendor or hardware boundary is a different case (rule 24). [POSD-T04, POSD-T43, REF-T45, REF-T46]
- **Check:** No method body is only a call that forwards the same arguments, unless it keeps an external interface unchanged, and no decorator forwards most of its methods unchanged. [POSD-T04, POSD-T43]

### 8. Count as public only what outside teams may use

Callers or tests that rely on internals block changes the owners need to make. Decide explicitly which interfaces are public API, meaning outside teams may use them without asking the owners, and document their guarantees. Everything else is internal and can change. [SWE-T07]

- **Do:** Mark the outside-facing interface, document what it guarantees, and give implementation types the narrowest visibility the language allows. See [architecture](architecture.md) for enforcing component visibility. [SWE-T07, CA-T77]
- **Check:** Public APIs are usable by other teams without owner approval, and their documentation lists the guarantees. [SWE-T07]

## Rules: information hiding

### 9. Keep each design decision inside one module

Information leaks when one design decision, such as a file format, an encoding or a protocol, is reflected in several modules, because changing it then means changing all of them. Leakage can also run through a back door: two classes that both read the same file format share knowledge that neither interface shows. Put each format, encoding rule or parsing routine in one owning module, and have everyone else call it. [POSD-P3, POSD-T06, POSD-T07]

- **Do:** Look for formats and protocols shared outside any interface, move each into one owner, and make the other module call it. [POSD-T06, POSD-T07]
- **Not when:** A new class that still re-exposes most of the leaked knowledge adds little, so the owner must actually hide it. [POSD-P3]
- **Check:** The same parsing, encoding or format logic does not appear in two or more files, and a second reader of a format calls the owning module. [POSD-T06, POSD-T07]

### 10. Merge code that shares knowledge

Splitting code that shares knowledge scatters that knowledge across files that readers must track together. Combine pieces into one module when they read the same data format or when each needs the other to be understood, and merge small classes that are tied to the same internal detail into one class that owns it. [POSD-T36, POSD-T37, POSD-P3]

- **Not when:** One-way use alone does not justify combining code. Merging so far that one class holds the whole application goes too far. [POSD-T36, POSD-T37]
- **Check:** Each merge in the diff joins pieces that read the same format or need each other to be understood, and no two small classes both reference the same internal detail. [POSD-T36, POSD-T37]

### 11. Hide data behind operations, including in accessors

Exposing operations and keeping data private limits which code breaks when the internal layout changes. Private fields are hidden only if their getters and setters do not hand out the representation, so give callers operations and single values, never the internal collection itself. Where a getter must return mutable data, return a copy. [CA-T07, POSD-T52, REF-T86, CC-T40]

```python
class Roster:
    def __init__(self):
        self._members = []

    def members(self):            # leaks: callers can mutate the list
        return self._members      # and come to depend on it being a list

    def add(self, person):        # hides: callers ask for what they need
        self._members.append(person)

    def count(self):
        return len(self._members)
```

- **Do:** Replace getters that return internal collections with operations or single values, and return a copy from any getter of mutable data. Keep mutable state private, with one public method that performs the work so callers cannot disturb the state between internal steps. [POSD-T52, REF-T86, CC-T40]
- **Not when:** In languages such as C++ that require member data in the class header, keep that data private there. Private members still stop direct access from outside the class, so keep them private even where accessors exist. Callers that change shared data on purpose break when they receive a copy, so tests must catch them. Multithreaded use needs locks or per-caller instances to protect the hidden state. [CA-T07, POSD-T52, REF-T86, CC-T40]
- **Check:** Public declarations show operations, not data members, and no getter or setter returns or accepts the internal representation or collection unchanged. [CA-T07, POSD-T52]

### 12. Make each class either an object with behavior or plain data

A class with behavior keeps its fields private, while a data-only class may expose public fields and have no methods. Mixing both makes the class awkward to extend in either direction. Plain data structures are also the right shape for data crossing a boundary. [CC-T41, CC-T40, CA-P6]

- **Check:** Each class has private fields with methods, or public fields with no methods. [CC-T41]

### 13. Ask an object to act instead of reaching through it

Code that chains through objects returned by other calls depends on the whole structure beneath the first object, and that structure belongs to its owner, who may change it. Ask the immediate collaborator to do the work or to change its own state. [CC-T42, PP-T11]

- **Do:** Replace a chain such as `a.b().c().d()` with a method on the immediate collaborator that performs the work. [CC-T42, PP-T11]
- **Not when:** Chains through plain data structures are harmless, since those expose their fields anyway. Stable language library types may be chained, but treat third-party APIs as volatile. [CC-T42, PP-T11]
- **Check:** Code contains no chained calls across object boundaries, and callers do not chain through another object's parts to change its data. [CC-T42, PP-T11]

### 14. Confine mutable state to a few named owners

Race conditions and concurrent update defects come from mutable variables, so fewer of them means fewer defects. Limit mutable data to a few identified components that control who writes it, and route updates to shared mutable data through one function. [CA-T09, REF-P5]

- **Do:** Count the shared mutable variables, confine them to a few named components, and keep changing variables in the narrowest scope. See [performance and concurrency](performance-and-concurrency.md) for locking. [CA-T09, REF-P5]
- **Not when:** Immutable data needs no accessor wrapper, and a copy protects only its top level. Mutable data often cannot be removed, and data that one small function uses may stay local. [REF-P5]
- **Check:** Shared mutable variables are counted and confined to a few named components, and direct writes to shared fields go through one update function. [CA-T09, REF-P5]

## Rules: one place per piece of knowledge

### 15. Give each fact one authoritative representation

Copies of one fact in code, docs, schemas or configuration drift apart, so one business rule should need one edit. When the same API, schema or model must appear in several places, generate the copies from one source instead of writing each by hand. [PP-P3, PP-T08, DDIA-P1]

- **Do:** Consolidate duplicated knowledge when you find it. Generate client code, mocks and docs from a single specification. See [data systems](data-systems.md) for derived stores. [PP-P3, PP-T08]
- **Not when:** Code that looks identical may encode different rules that change separately, so check before merging (rule 17). Duplicated copies of stored data are acceptable only when a process updates every copy. [PP-P3, DDIA-P1]
- **Check:** Changing one business rule edits exactly one location, and repeated interface descriptions are generated from one specification file. [PP-P3, PP-T08]

### 16. Compute dependent values instead of storing them

A stored copy of a value that can be computed from other fields, such as a total, can drift away from the fields it came from. Store only the independent fields, and replace a stored derived field with a query its readers call instead. [PP-T09, REF-T30]

- **Not when:** If the derived value is expensive and read often, cache it privately inside the module. [PP-T09]
- **Check:** The data class stores only independent fields and computes the dependent ones. [PP-T09]

### 17. Merge duplicates only when they change together

Look-alike code serving different use cases tends to diverge, and a shared module then couples those use cases. Merge duplicated code only when every change to one copy would require the same change to the others, which in practice means the copies serve the same actor and change for the same reasons. The timing of a merge is contested, so see the tension below. [CA-T42, CC-T36, PP-P3]

- **Do:** Before extracting shared code, check that all its users change for the same reasons, for example by looking at whether the copies were edited in the same recent commits. [CA-T42, CC-T36]
- **Not when:** Leave copies apart when they serve different actors, or when the repeat is only two or three stable lines. [CC-T36]
- **Check:** Shared code is extracted only where all of its users change for the same reasons. [CA-T42]

## Rules: coupling and cohesion

### 18. Give each module one stated responsibility

A component with one well-defined purpose can be changed and tested alone, and a change made for one concern then leaves unrelated code untouched. Move each concern into a class named for it, keep classes small, and make their methods share the class's data under a name that covers all of them. Group code by the cause that would make it change. [PP-T10, CC-T43, CC-T44, CA-P3]

- **Do:** State the module's single responsibility in its doc comment. Before placing a class, ask which stakeholder or cause would make it change. When logic for one concern sits in a large function or an unrelated class, move it into a class of its own. [PP-T10, CA-P3, CC-T43]
- **Not when:** A very small system can stay in one class, and tiny classes need not be split. See the tension on class size below before splitting a deep module. [CC-T43]
- **Check:** Each module's doc comment states one responsibility, its name summarizes every public method, and its methods share the same data. [PP-T10, CC-T44, CC-T43]

### 19. Add a dependency only when the module truly uses it

Coupling makes unrelated parts change together, and indirect dependencies count as coupling too. Each declared dependency, even an unused one, still forces rebuilds and changes when it changes. Declare only what the code uses directly, and count indirect dependents when judging the impact of a change. [PP-P4, CA-T14]

- **Check:** Each dependency is named in the module's own source, a change to one module's internals touches no other module's files, and new imports point to only a few modules. [CA-T14, PP-P4]

### 20. Give each client only the operations it calls

When one class serves several clients that each call different operations, a broad interface makes every client depend on operations it never uses, so their changes ripple into it. Split the interface so each client sees only what it calls. [CA-T18, CC-T47]

- **Not when:** Dynamically typed languages have no declared dependencies that force rebuilds, so the split buys little there. [CA-T18, CC-T47]
- **Check:** Each client's declarations and imports reference only the operations and interfaces it calls. [CA-T18, CC-T47]

### 21. Put coupled elements together and group what changes together

Elements that one change must touch should sit next to each other. When a change touches scattered spots, move each element beside its peers. When decoupling is not feasible now, group the elements that always change together into one helper or submodule, so a coupled change touches fewer places. Coupling is not always visible in the source, so look at which files change together in commit history. [TF-T11, TF-T12, TF-T36]

- **Do:** Read commit history to see which files change together, then move one element per commit beside the peers it is coupled with, or group always-co-changed functions into one helper. [TF-T36, TF-T11, TF-T12]
- **Not when:** If grouping would need a new object, it is beyond a tidying and needs a design change instead. [TF-T12]
- **Check:** The elements a change must touch are adjacent, a new helper holds only elements edited together, and coupling notes cite co-change history. [TF-T11, TF-T12, TF-T36]

### 22. Decouple only while it costs less than the coupling

Coupling is costly when a change to one element forces edits to others, but every separation adds its own cost in indirection. Decouple when removing a coupling costs less than keeping it, add interfaces only where changes are expected, and stop when the indirection outweighs what it removes. [TF-P6, TF-T32]

- **Do:** For each decoupling, name the cross-module dependency it removes, any new dependency it adds, and the planned change that motivates each new interface. [TF-P6, TF-T32]
- **Not when:** Skip decoupling when the team lacks the skill, time or capacity for it. Decoupling may also add coupling elsewhere, which the book admits it cannot prove either way. [TF-P6]
- **Check:** The decoupling diff adds only the interfaces the PR names for a specific planned change, and the commit message names the dependency removed. [TF-T32, TF-P6]

### 23. Pass collaborators and settings in explicitly

A unit that creates its own collaborators, or reaches for globals and singletons, hides its links and is hard to test with substitutes. Give each unit the configuration, state and services it needs as parameters, and read every input through its signature rather than deep inside the code. [CC-T12, PP-T27, TDD-T40, TF-T14]

- **Do:** Accept collaborators as constructor or method parameters, grouped into one object once there are more than three. Move environment and map reads up to the entry point and pass the values down. For settings shared system-wide, see the tension below on context objects. [CC-T12, TF-T14, PP-T27]
- **Check:** Units receive their dependencies instead of constructing them, no global or singleton holds a resource tests must replace, singletons expose no public mutable fields, and no environment read sits below the entry point. [CC-T12, TDD-T40, PP-T27, TF-T14]

## Rules: volatile dependencies and configuration

### 24. Wrap third-party APIs in an interface you own

Put each vendor database, service, SDK, platform API or file system behind an abstraction you own, so a vendor change stays inside one module. Keep endpoint paths, schema names, error codes and framework rules inside that one adapter, which translates them, and shape the adapter's interface around your application's needs rather than the vendor's. [PP-P5, PP-T12, PP-T13, CC-T51, GOF-T17]

```python
class PaymentGateway(Protocol):          # owned by the application
    def charge(self, order_id: str, cents: int) -> bool: ...

class AcmeGateway:                       # the only module importing the SDK
    def __init__(self, client):
        self._client = client
    def charge(self, order_id, cents):
        resp = self._client.payments.create(ref=order_id, amount=cents)
        return resp.status == "succeeded"   # vendor codes stop here
```

- **Do:** Create the adapter when you adopt the dependency, keep vendor types out of application code, and pass the adapter in as a parameter (rule 23). Prefer decisions you can reverse later. See [architecture](architecture.md) for placing adapters at component boundaries. [PP-T12, CC-T51, PP-P5]
- **Check:** Vendor SDK and HTTP calls, endpoint paths and error codes appear only inside the wrapper module. [PP-T12, PP-T13, PP-P5]

### 25. Move values that vary by environment into configuration

Hosts, ports, limits and policy values that differ by environment, customer or release belong in configuration or data, so they change without editing code. Read them through a thin accessor that is passed in as a parameter. [PP-T34, PP-T27]

- **Do:** Replace inline environment-specific literals with values read from configuration, and give each key a default in code where the common case has one. [PP-T34, POSD-T09] For credentials, see [security](security.md).
- **Not when:** Values that never vary, such as protocol limits, stay in code. Do not expose a tuning value the module can derive itself (rule 4). [PP-T34, POSD-T39]
- **Check:** Hosts, ports and environment-specific limits come from configuration, not inline literals. [PP-T34]

## Rules: abstraction, variants and subtypes

### 26. Add an abstraction only when a current caller needs it

An extension point, option, interface, class or parameter added ahead of need is a guess. It costs reading time, adds code with no caller, and may turn out wrong. Add one when a failing test, a real variation or a current caller requires it, and represent a new concept as a plain value until it needs behavior of its own. Delete hooks and abstract classes built for needs no code has. [CC-T77, PP-T71, TDD-P9, TDD-T18, TDD-T19, REF-T85]

- **Do:** Before adding an interface, option or hook, name its current caller. Use a plain string or number for a new concept, such as a currency, that is needed only for identity right now. Remove speculative hooks, special cases and delegation layers that have no caller. [CC-T77, TDD-T19, REF-T85]
- **Not when:** Add the hook when growth is a confirmed business direction or the odds of needing it are high. Structure that the agreed value still needs is not a guessed future need. Add a parameter now when current behavior requires it, and make a concept an object once it needs its own behavior. A design choice that shapes the whole system deserves careful reasoning before code. [CC-T77, PP-T71, TDD-T18, TDD-T19, TDD-P9]
- **Check:** Each extension point, option, interface, hook and abstract class in the diff has a current caller or traces to a stated requirement, and each new class and parameter is required by a test. [CC-T77, PP-T71, REF-T85, TDD-T18]

### 27. When an abstraction is needed, design its core together

Once a feature really needs an abstraction that does not exist yet, design its core operations together and somewhat generally, so it serves several uses, rather than adding methods one caller at a time. Piecemeal interfaces accumulate gaps, while early design effort pays back when the module is reused. Still add no operation that no caller needs. [POSD-T46, POSD-T05]

- **Not when:** Skip the general design when only quick working code matters, and do not make the class so general that current needs become hard to meet. [POSD-T46]
- **Check:** The first change's interface covers the abstraction's core operations, designed together, with no unused extras. [POSD-T46]

### 28. Design a major interface twice

Even a design that seems obviously right has weaknesses that only a different alternative reveals. Before committing to a major public interface, data structure or module split, sketch at least two radically different alternatives, compare them first by how easily callers can use them and then by simplicity, generality and efficiency, and combine their strengths when neither fits. [POSD-P5, POSD-T13, POSD-T14]

- **Do:** In the PR description or design note, list the alternatives, what a caller must write under each, which was rejected and why, and each option's trade-offs. [POSD-T14, POSD-P5, SWE-T35]
- **Not when:** The principles alone may not pick one best design, so use them to guide the comparison rather than as a recipe. [POSD-P5]
- **Check:** For each new public interface, the PR or design note names at least two differently shaped alternatives, what a caller writes for each, and the factor that ruled out the rejected one. [POSD-T13, POSD-T14, POSD-P5]

### 29. Put variants of one job behind one substitutable interface

When several implementations do the same job, such as disk and network drivers, put them behind one shared interface so developers learn one contract, and keep variant-specific commands inside each implementation. Each subtype must behave like its base for the same calls, so callers never need to know which one they hold. Add a new variant as a new class rather than as another branch in existing code. [POSD-T42, CA-T15, CC-T46, CC-T45, PP-T33]

- **Do:** Run the base type's tests against every subtype. Add new behavior as a new single-purpose class registered in one factory line. See [design patterns](design-patterns.md) for strategy and factory choices. [CA-T15, CC-T45]
- **Not when:** When only format or settings differ between variants, use configuration instead of new code. [CA-T78]
- **Check:** Variant classes implement one shared interface and do not call each other, tests for the base type pass unchanged against each subtype, and callers contain no type tests for concrete subtypes. [POSD-T42, CA-T15, CC-T46]

### 30. Derive only from abstract or stable types

A subclass inherits the churn of its base class, and overriding a concrete method ties it to that method. Express interchangeable behavior with interfaces or protocols, check the alternatives before adding a subclass, and derive new classes only from abstract types or stable classes. [CA-T22, PP-T33, GOF-P3]

- **Do:** Type collections and parameters with interfaces, reuse behavior by holding a collaborator rather than subclassing only for code, and never subclass a volatile concrete class. [PP-T33, GOF-P3, CA-T22]
- **Not when:** Dynamic typing makes inheritance a smaller problem, although the subclass still depends on its base. Inheritance still helps when new components must combine with existing ones, and heavy composition also hurts understanding. The tension on inheritance below says when a subclass is acceptable. [CA-T22, GOF-P3]
- **Check:** New subclasses extend abstract or stable types only, no subclass overrides a concrete method of a volatile base, and no subclass exists only to share code. [CA-T22, PP-T33]

## Playbooks

### When you design a new module, class or public API
1. Write down the typical changes the module must absorb and the decision it will hide. [POSD-P1, POSD-P3, TF-P5]
2. Sketch two radically different interfaces and write, for each, the code a caller would need. [POSD-T13, POSD-T14]
3. Write the call you wish existed from the caller's side, in a test if the project works test-first, and let that shape the signature. See [testing](testing.md). [TDD-T23, TF-T09, PP-T40]
4. Keep only operations a current caller needs, designed together as the core of the abstraction, at the units callers use. [POSD-T05, POSD-T46, POSD-T55]
5. Give parameters defaults, move rare options to separate methods, and expose no setting the module can derive. [POSD-T09, POSD-T38, POSD-T39]
6. Keep data private and expose operations, with no getter handing out internal collections. [CA-T07, POSD-T52]
7. Take collaborators as parameters and wrap any vendor dependency in your own adapter. [CC-T12, PP-T27, PP-T12]
8. Record the rejected alternative and the reason in the PR description. [POSD-P5, SWE-T35]

### When the same format, rule or fact appears in several places
1. List every site, including back-door sharing such as two classes reading the same file format. [POSD-T07]
2. Confirm the copies encode one piece of knowledge, meaning every change to one would require the same change to the others. If they serve different actors, stop and leave them apart. [CA-T42, CC-T36, PP-P3]
3. Pick one owning module, move the knowledge there, and make the other sites call it. [POSD-T06, POSD-P3]
4. If the sites are small classes tied to the same detail, merge them into the owner instead. [POSD-T37]
5. If the fact must appear in several artifacts, such as a schema, client code and docs, generate the copies from one specification. [PP-T08]
6. Replace stored values that can be derived with computations. [PP-T09]
7. Confirm that changing the rule now edits one location. [PP-P3]

### When you adopt a library, SDK or external service
1. Define an interface shaped by what your application needs from the dependency. [CC-T51, PP-P5]
2. Implement it in one adapter that holds all vendor types, endpoint paths, schema names and error codes. [PP-T12, PP-T13]
3. Pass the adapter in as a parameter so tests can substitute it. [CC-T12, PP-T27]
4. Move hosts, ports and limits that vary by environment into configuration read through a thin accessor. [PP-T34]
5. Check that no vendor call appears outside the adapter. [PP-T12]

### When you are about to add an interface, option or extension point
1. Name the current caller, failing test or real variation that needs it. If there is none, growth is not a confirmed direction, the odds of needing it are not high, and the agreed scope does not need it, do not add it. [CC-T77, PP-T71, TDD-P9, TDD-T18]
2. If the need is a new concept used only for identity, use a plain value for now. [TDD-T19]
3. If there is a single implementation, add an interface only when clients must avoid recompiling, or when a second implementation or an inverted dependency needs it. [GOF-P4, CC-P5]
4. If it is needed, design the abstraction's core operations together and add no extras. [POSD-T46, POSD-T05]
5. Name in the PR the planned change each new interface serves, and stop when further indirection would outweigh it. [TF-T32]
6. While there, delete hooks and abstract classes elsewhere in the touched code that have no caller. [REF-T85]

### When a small change touched many modules
1. Record which modules the change touched and why, as evidence of the design's cost. [POSD-T01, PP-T68]
2. Look for leaked knowledge: the same format or rule in several of those modules. Move it into one owner. [POSD-T06, POSD-T07]
3. Check commit history for files that change together, and move coupled elements beside each other one per commit. [TF-T36, TF-T11]
4. Where decoupling is not feasible now, group the always-co-changed elements into one helper. [TF-T12]
5. Where a module depends on operations it never calls, split the interface per client, and remove unused imports. [CA-T18, CA-T14]
6. Decouple further only while each step costs less than the coupling it removes. [TF-P6, TF-T32]
7. When the current structure makes the behavior change hard, commit the structural moves before the behavior change, unless they would not ease it. See [change workflow](change-workflow.md). [TF-T01]

### When you add a new variant or subtype
1. If only format or settings differ, use configuration instead of new code. [CA-T78]
2. Otherwise implement the shared interface of the existing variants, or create one when several variants do the same job and no shared interface exists yet. [POSD-T42, PP-T33]
3. Add the variant as a new class, with one registration line in the factory. [CC-T45]
4. Run the base type's tests against the new subtype unchanged. [CA-T15]
5. Check that no caller tests for the concrete type and that the new class extends only an abstract or stable type. [CC-T46, CA-T22]

## Where the books disagree

### When should an interface or extension point be added?
- **Clean Code, Pragmatic Programmer, Refactoring, TDD:** add no extension point, option, interface, class or parameter until a current caller, requirement or failing test needs it, and remove speculative ones. [CC-T77, PP-T71, REF-T85, TDD-P9, TDD-T18]
- **Tidy First:** add interfaces only where changes are expected, and stop when indirection outweighs the coupling removed. [TF-T32]
- **Design Patterns:** use a pattern only where its flexibility is needed, but long-lived systems still need anticipated changes planned in advance. [GOF-P4, GOF-P6]
- **POSD:** when a feature first needs an abstraction, design it cleanly and somewhat generally for several uses rather than piecemeal. [POSD-T46]
- **Decide:** With no current caller and no confirmed direction, do not add it. [CC-T77, PP-T71] Add it ahead of a caller only when growth is a confirmed business direction, the odds of needing it are high, or the system is long-lived and the change is anticipated, and reason carefully when the choice shapes the whole system. [CC-T77, GOF-P6, TDD-P9] With one implementation, add an interface only when clients must avoid recompiling, a second implementation exists, or a dependency must be inverted, and do not expose choices that clients must study before they can use the module. [GOF-P4, CC-P5] Once a current need exists, design the core operations together, without operations no caller needs, unless only quick working code matters. [POSD-T46, POSD-T05]

### When should duplicated code be merged?
- **Pragmatic Programmer, POSD:** each fact needs one authoritative home, and the same knowledge in several modules is a major red flag. [PP-P3, POSD-T06]
- **TDD:** remove duplication right after each test passes, since it marks a dependency or a missing concept. [TDD-T10, TDD-P5]
- **Refactoring:** wait for the third similar case before unifying, unless a bug or feature exposes the copies sooner. [REF-P4]
- **Clean Architecture, Clean Code:** merge only copies that change together for one actor, because look-alike code for different use cases diverges. [CA-T42, CC-T36]
- **Decide:** First decide whether the copies are one piece of knowledge: merge only when every change to one would require the same change to the others, and keep copies that serve different actors apart. [CA-T42, CC-T36, PP-P3] Then decide timing: in a test-first cycle, remove duplication in your own new code before the work is shared, and reconcile near-identical code until it matches before merging. [TDD-T10, TDD-T11] For copies in existing code, merge at the third case or when a bug or feature exposes them, and compare near-duplicates first because small differences may be real. [REF-P4] Two or three stable lines, and code that never changes, may stay duplicated. [CC-T36, REF-P4] The [refactoring](refactoring.md) guide has the mechanics.

### Should classes be small or deep?
- **Clean Code, Pragmatic Programmer:** move each concern into its own small, cohesive class with one reason to change. [CC-T43, CC-T44, PP-T10]
- **POSD:** value lies in deep modules with simple interfaces, so merge code that shares a format or needs each other to be understood, and split a method only when each part reads alone. [POSD-P2, POSD-T36, POSD-T37, POSD-T35]
- **Decide:** Split where parts change for different reasons and each part can be understood on its own. [CC-T43, CA-P3, POSD-T35] Merge where parts read the same data format, share an internal detail, or each needs the other to make sense, but one-way use alone is no reason to merge, and do not merge into one class holding the whole application. [POSD-T36, POSD-T37] A very small system, a tiny class, or a long method whose blocks are independent behind a simple signature can stay whole. [CC-T43, POSD-T35] Shallow classes such as list nodes are acceptable where unavoidable. [POSD-P2]

### Should a wrapper that only forwards calls stay?
- **POSD, Refactoring:** remove pass-through methods, middle men and forwarding decorators, since they add interface without hiding anything. [POSD-T04, POSD-T43, REF-T45, REF-T46]
- **Pragmatic Programmer:** put each third-party database, service or SDK behind a layer you own. [PP-T12]
- **Clean Code:** wrap vendor APIs and hardware or framework boundaries in a thin adapter whose methods only delegate. [CC-T51, CC-T13]
- **Decide:** Keep a forwarding layer when it keeps an external interface unchanged, or when it isolates a vendor, framework or hardware boundary behind an interface shaped by your application. [POSD-T04, CC-T51, CC-T13, CC-T33] Remove one that only relays calls between your own modules, except overridden forwarders and delegates kept on purpose during a migration or rename. [REF-T45, REF-T46] Some delegation is good encapsulation, so judge by whether the layer hides a decision. [REF-T46, POSD-P2]

### Decorator or a feature in the base class?
- **POSD:** add a broadly useful feature to the base class, or build it standalone, rather than a decorator that forwards most calls. [POSD-T43]
- **Design Patterns:** add responsibilities to individual objects by wrapping them, and keep the base lean with each optional feature in its own decorator. [GOF-T30, GOF-T47]
- **Decide:** If most clients want the feature, put it in the base class or a standalone module. [POSD-T43] If only some objects need it, it must be added or removed at run time, or several optional features would otherwise bloat a class most clients use plainly, use decorators. [GOF-T30, GOF-T47] With only one optional feature, a single concrete decorator is simpler than a decorator family, and when the external interface cannot change or a decorator of the same object already exists, a decorator is right. [GOF-T47, POSD-T43] See [design patterns](design-patterns.md).

### When is inheritance acceptable?
- **Clean Architecture, Pragmatic Programmer, Design Patterns:** derive only from abstract or stable types, use interfaces for interchangeable behavior, and favor composition over subclassing for reuse. [CA-T22, PP-T33, GOF-P3]
- **Refactoring:** starting with inheritance is fine until it causes problems, then switch to delegation. [REF-T70]
- **Decide:** Do not subclass a volatile concrete class, and do not subclass only to share code. [CA-T22, PP-T33] A subclass of an abstract or stable base is acceptable, and inheritance still helps when new components must combine with existing ones. [CA-T22, GOF-P3] Switch to delegation once behavior varies on two axes, the variant changes at run time, or subclasses depend on parent internals. [REF-T70] Heavy composition also hurts understanding, and static multiple inheritance helps independent libraries combine, so do not replace every subclass by reflex. [GOF-P3] The [refactoring](refactoring.md) guide covers the move.

### How should shared settings reach the code that uses them?
- **POSD:** gather system-wide settings into one context object passed to constructors, so method signatures do not grow settings parameters that intermediate layers only forward. [POSD-T44]
- **Pragmatic Programmer, Tidy First:** pass configuration, state and services as explicit parameters, and read every input through the signature rather than from globals or the environment. [PP-T27, TF-T14]
- **Decide:** Pragmatic Programmer rules out globals and singletons, and POSD passes its context object to constructors. [PP-T27, POSD-T44] Use one context object when many components share system-wide settings, keep its variables immutable, and watch that it does not become a grab-bag or cause thread-safety issues. [POSD-T44] Pass routine-specific inputs as their own parameters, gathered at the entry point. [TF-T14, CC-T12]

### Should a value be configurable?
- **Pragmatic Programmer:** move values that change by environment, customer or release into configuration. [PP-T34]
- **POSD:** expose a setting only when callers know a better value than the module can derive, and default every key. [POSD-T39, POSD-T09]
- **Decide:** Configure values that vary between deployments, and keep values that never vary in code. [PP-T34] Do not expose a tuning value the module can derive, unless users know domain priorities it cannot see. [POSD-T39] Give every exposed key a default in code. [POSD-T09]

## Review checklist

- [ ] The PR names the modules a likely next change would touch, and a small change in this area edits one owning module or explains why not. [POSD-T01, PP-T68]
- [ ] Each new public method, parameter or class has a caller that becomes simpler, and the public surface stays small relative to the implementation. [POSD-T05, POSD-T45, POSD-P2]
- [ ] Each configuration key has a default in code and is one the module could not derive, and the common API does not mention rare options. [POSD-T09, POSD-T39, POSD-T38]
- [ ] Callers do not split, join or loop over internal units to perform one user operation. [POSD-T55]
- [ ] No method body only forwards the same arguments, and no decorator forwards most methods unchanged, unless it keeps an external interface or wraps a vendor boundary. [POSD-T04, POSD-T43, CC-T51]
- [ ] The same format, encoding or parsing logic does not appear in two or more files. [POSD-T06, POSD-T07]
- [ ] No getter or setter returns or accepts an internal collection or representation unchanged. [POSD-T52, CA-T07]
- [ ] Each class is either private fields with methods or public fields without methods. [CC-T41]
- [ ] No chained calls cross object boundaries, except through plain data or stable library types. [CC-T42, PP-T11]
- [ ] Shared mutable variables are few and confined to named components. [CA-T09]
- [ ] Changing one business rule edits one location, and repeated interface descriptions are generated from one source. [PP-P3, PP-T08]
- [ ] Newly extracted shared code has users that all change for the same reasons. [CA-T42, CC-T36]
- [ ] Each module states one responsibility, and its name covers every public method. [PP-T10, CC-T44]
- [ ] Each import is used directly, and each client depends only on the operations it calls. [CA-T14, CA-T18, CC-T47]
- [ ] Each new interface added for decoupling is tied to a named planned change. [TF-T32]
- [ ] Units receive collaborators as parameters, and no global or singleton holds a replaceable resource. [CC-T12, PP-T27, TDD-T40]
- [ ] Vendor SDK calls, endpoint paths and error codes appear only inside one adapter. [PP-T12, PP-T13]
- [ ] Every extension point, hook, option and abstract class has a current caller or a stated requirement. [CC-T77, REF-T85, PP-T71]
- [ ] New public interfaces come with at least one rejected alternative and the reason in the PR. [POSD-P5, POSD-T13]
- [ ] Subtypes pass the base type's tests unchanged, and callers contain no type tests for concrete subtypes. [CA-T15, CC-T46]
- [ ] New subclasses extend only abstract or stable types and do not override concrete methods of a volatile base. [CA-T22]

## More entries in this area

- `POSD-T29` — Keep two related values in separate objects: when two related values are stored state that callers still read and change one at a time, store them in separate objects rather than in one object with a flag that only says which value is which.
