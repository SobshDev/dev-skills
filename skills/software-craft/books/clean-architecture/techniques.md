# Clean Architecture — techniques

### CA-T03: Write tests before new code

Write the tests first when building new functions, modules or features from scratch.

- **Why:** Test-first work keeps new code cleanable from the first line.
- **When:** Starting new functions, modules or features with no existing code to protect.
- **Check:** Commits for new code add tests before the implementation they exercise.
- **Source:** ch. 1

### CA-T05: Scale change effort with change size

Plan each change's effort by its own size, not by the shape of the existing system.

- **Why:** When small changes need large effort, the architecture is spreading costs that the change does not cause.
- **When:** Estimating a requested change, or designing for requests whose shape is unknown.
- **Not when:** Full shape agnosticism is impractical, so aim for the practical degree.
- **Check:** Changes of similar scope need similar effort in different parts of the code.
- **Source:** ch. 2

### CA-T06: Cross boundaries with polymorphism

Call across an architectural boundary through an interface, never a concrete class on the other side.

- **Why:** Polymorphism lets the boundary hold while the implementation behind it changes.
- **When:** Code in one component must call behavior implemented in another component.
- **Not when:** Templates decouple code but still force recompilation of their dependents.
- **Check:** Cross-boundary calls use an interface type, not a concrete class or a table of function pointers.
- **Source:** ch. 3, 5, 18

### CA-T07: Hide data behind operations

Expose behavior as operations and keep object data private.

- **Why:** Private data limits which code breaks when the internal data layout changes.
- **When:** Deciding which members of a class or module clients may see.
- **Not when:** Languages such as C++ must declare member data in the class header, so keep it private there.
- **Check:** Public declarations show operations, not private data members.
- **Source:** ch. 5, 23

### CA-T08: Invert dependencies through interfaces

Insert an interface so that a high-level module calls a low-level module through it.

- **Why:** The source dependency then points toward policy, so low-level changes do not reach the policy.
- **When:** A high-level module must call code in a lower-level module.
- **Not when:** The two components already depend on each other (CA-T31).
- **Check:** The high-level module imports an interface that the low-level module implements, and the interface lives with the high-level module.
- **Source:** ch. 5, 22, 25

### CA-T09: Confine mutable state to named components

Limit mutable data to a few identified components that control its writes and access.

- **Why:** Race conditions and concurrent update defects come from mutable variables, so fewer of them means fewer defects.
- **When:** Components run on several threads or processors, or several components share data.
- **Check:** Shared mutable variables are counted and confined to a few named components.
- **Source:** ch. 3, 6

### CA-T10: Store changes as transactions with periodic snapshots

Append each change as a stored transaction, with periodic snapshots.

- **Why:** The stored history preserves what happened, and snapshots keep replay from growing without limit.
- **When:** The history of changes matters to the application, and replaying all of it would become too slow.
- **Check:** Writes append new records, and state reads start from the latest snapshot.
- **Source:** ch. 6

### CA-T11: Separate code that different actors share

Keep code that serves different stakeholder groups in separate modules.

- **Why:** Shared code couples the groups, so one group's edit can break another group's behavior.
- **When:** A helper is reused by logic serving different stakeholders, or teams edit the same file.
- **Check:** A shared helper is not called from modules owned by different actors.
- **Source:** ch. 7

### CA-T12: Separate responsibilities that change for different reasons

Split parts that change for different reasons into distinct components.

- **Why:** A change made for one reason then touches one component, leaving unrelated code untouched.
- **When:** A new output format would force edits across unrelated code.
- **Check:** A change made for one reason touches only one component.
- **Source:** ch. 8, 13

### CA-T13: Depend toward stability

Make each dependency point toward a component more stable than the one depending on it.

- **Why:** Volatile components then absorb change without forcing edits in stable components.
- **When:** Adding a dependency between two components.
- **Check:** Every dependency arrow points toward a component with lower instability, as CA-T33 defines it.
- **Source:** ch. 8, 14

### CA-T14: Depend only on modules you use

Declare only the modules and classes that the code uses directly.

- **Why:** Each unused dependency still forces rebuilds and changes when it changes.
- **When:** Adding an import or dependency to a module.
- **Check:** Each dependency is named directly in the module's own source code.
- **Source:** ch. 8, 13

### CA-T15: Keep subtypes substitutable for their base

Make each subtype behave like its base type for the same calls.

- **Why:** Callers then behave the same with any subtype and need not know which one they hold.
- **When:** Creating a subclass or an alternative implementation of a base type.
- **Check:** Tests written for the base type pass unchanged against each subtype, and callers contain no type tests for specific subtypes.
- **Source:** ch. 9

### CA-T16: Keep provider differences in configuration

Put each provider's format differences in configuration keyed by its endpoint, not in code branches.

- **Why:** Shared code then has no provider-specific branches that would break the common interface.
- **When:** One provider cannot implement the shared interface exactly.
- **Check:** Shared code has no branch on a provider name, and format strings are read from configuration.
- **Source:** ch. 9

### CA-T18: Clients depend only on operations they call

Give each client an interface that declares only the operations that client calls.

- **Why:** Clients then do not need rebuilds or changes caused by operations they never use.
- **When:** One class serves several clients that each call different operations.
- **Not when:** Dynamically typed languages have no declared dependencies to manage.
- **Check:** Each client's declared imports list only the interfaces it calls.
- **Source:** ch. 10

### CA-T19: Create volatile objects through a factory

Create objects of a volatile concrete class through an abstract factory that clients call through an interface.

- **Why:** Clients then never name the volatile class, so changing it leaves their source unchanged.
- **When:** Client code needs an instance of a class that changes often.
- **Check:** Client source never names the concrete class being instantiated.
- **Source:** ch. 11, 26

### CA-T20: Gather unavoidable concrete dependencies into one component

Collect the concrete dependencies that cannot be removed into one small component, Main, which is the startup code that creates the factories and globals.

- **Why:** Concrete names then stay in one place instead of spreading into the design.
- **When:** Some concrete dependencies cannot be removed from the design.
- **Check:** Concrete class names and string-literal configuration lists appear only in the designated component.
- **Source:** ch. 11, 26

### CA-T21: Create the factory in Main

Let Main create the concrete factory and store it behind an abstract factory type.

- **Why:** The rest of the application then depends only on the abstract factory type.
- **When:** Wiring the application together at startup, before high-level code takes control.
- **Check:** Startup code assigns a concrete factory to a variable of the abstract factory type.
- **Source:** ch. 11, 26

### CA-T22: Derive only from abstract or stable types

Derive new classes from abstract types or stable classes, never from a volatile concrete class.

- **Why:** Subclasses inherit the churn of their base class, and an overridable concrete method ties them to it.
- **When:** Creating a subclass of an existing class that changes often.
- **Not when:** Dynamically typed languages, where inheritance is less of a problem though still a dependency.
- **Check:** New subclasses extend abstract types or stable classes only, and no subclass overrides a concrete method of a volatile base.
- **Source:** ch. 11

### CA-T23: Build independently deployable components

Make each component produce its own deployable artifact, such as a jar or DLL.

- **Why:** Teams can then develop, release and redeploy a component without waiting for the rest of the system.
- **When:** Dividing a system into deployment units or among several teams, or when components change at different rates.
- **Not when:** Components that always change and ship together belong in one bundle, as CA-T75 describes.
- **Check:** Each component builds to its own artifact and ships without rebuilding the others.
- **Source:** ch. 5, 12, 18

### CA-T24: Load optional components as runtime plugins

Build optional components that the application loads at runtime through a defined interface.

- **Why:** The core then stays unchanged when optional parts are added or removed.
- **When:** Extensions must ship independently of the core, or the core cannot know them in advance.
- **Check:** The core loads optional components through a defined interface at runtime.
- **Source:** ch. 12, 17

### CA-T25: Publish release notes with each reusable component

Give every reusable component a version number and release notes that say what changed and which dependents it affects.

- **Why:** Other teams can then decide when to adopt a release instead of absorbing changes unknowingly.
- **When:** A component is shared with other teams or projects.
- **Check:** The component has a version number and release notes naming the changes and dependents.
- **Source:** ch. 13

### CA-T26: Group classes that share one purpose

Put classes in one component only when they form a cohesive group serving one stated purpose.

- **Why:** A component with one purpose can be reused and released as a whole.
- **When:** Deciding which classes belong together in a component.
- **Check:** Every class in a component serves the same stated purpose.
- **Source:** ch. 13

### CA-T27: Favor develop-ability over reuse early

Shape the components of an ordinary or young application for ease of change, and leave reuse for later.

- **Why:** Early reuse concerns guess at needs that only real change patterns reveal.
- **When:** The project is young or the application is ordinary, with few dependents.
- **Not when:** Other projects already draw from the component and depend on its reuse.
- **Check:** Changes to one feature are confined to one component in the commit history.
- **Source:** ch. 13

### CA-T28: Keep the component graph acyclic

Break any dependency cycle as soon as it appears, so no component reaches itself through its dependencies.

- **Why:** A cycle makes its members release and test as one large component.
- **When:** A new dependency would connect two components in a loop.
- **Check:** Build tooling reports every component cycle as an error.
- **Source:** ch. 14

### CA-T29: Depend on pinned released versions

Keep dependencies on a named release of each component, and adopt newer releases on your own schedule.

- **Why:** A moving latest version lets another team's work in progress break your build.
- **When:** A new release of a component appears while your team is mid-work.
- **Check:** Dependency declarations pin a release rather than a moving latest version.
- **Source:** ch. 14

### CA-T31: Break a cycle by inverting or extracting

Break a cycle either by defining an interface in the used component or by moving the shared classes into a new component.

- **Why:** The cycle-closing dependency disappears, so both components can be released and tested alone.
- **When:** Two components depend on each other, and one needs only a few methods or both need the same classes.
- **Check:** Neither original component imports the other after the change.
- **Source:** ch. 14

### CA-T32: Derive components from classes

Derive the component structure from classes that exist, not from a plan made before the code.

- **Why:** Components designed before any classes exist usually miss how the code really changes.
- **When:** Starting a system or reviewing its component dependency diagram.
- **Check:** Every component contains real classes, and no placeholder component exists before its classes.
- **Source:** ch. 14

### CA-T33: Measure stability by counting dependencies

Compute each component's instability as its outgoing dependencies divided by all its dependencies, not from how often it changes.

- **Why:** Stability then reflects how many components depend on the component, which is what makes change hard.
- **When:** Judging whether a component is stable enough to be depended on.
- **Check:** A report lists fan-in, fan-out and instability for each component, with instability between 0 and 1.
- **Source:** ch. 14

### CA-T34: Keep components near the main sequence

Keep each component near the main sequence, the line where abstractness (the share of interfaces and abstract classes) plus instability equals one.

- **Why:** Components far from the line are either rigid and hard to change, or hold abstractions nothing uses.
- **When:** A component's stability and abstractness seem mismatched.
- **Not when:** The metric is imperfect, so judge flagged components on design reasons too.
- **Check:** Each component's distance from the main sequence stays small and is tracked per release.
- **Source:** ch. 14

### CA-T35: Avoid components that are stable, concrete and volatile

Avoid components that are stable, concrete and changing often at once, because they are rigid and hard to change.

- **Why:** Many dependents make a volatile concrete component expensive to change.
- **When:** A widely used concrete component, such as a database schema, is also changing often.
- **Not when:** A concrete component that rarely changes, such as a common string library, is harmless.
- **Check:** Volatile components with many dependents and no interfaces are listed for review.
- **Source:** ch. 14

### CA-T36: Keep stable components mostly abstract

Make stable components consist mainly of interfaces and abstract classes, and keep volatile components concrete.

- **Why:** Stable abstractions let high-level policy be extended without modifying it.
- **When:** Deciding what a stable component should contain, or where core policy lives.
- **Not when:** Not every component should be stable: volatile parts stay unstable, depending on stable ones with no dependents.
- **Check:** Stable components hold mainly interfaces and abstract classes, while unstable components hold concrete classes.
- **Source:** ch. 14

### CA-T37: Show use cases at the top

Name top-level modules after the system's use cases and features, and keep framework layouts out of the top level.

- **Why:** The structure then reveals what the system does rather than which tools it uses.
- **When:** Organizing the top-level structure of a new or existing system.
- **Check:** Top-level names identify features or use cases, not only technical layers or frameworks.
- **Source:** ch. 15, 16, 21

### CA-T38: Plan deployment units during initial design

Decide the deployable units, their startup order and their configuration while the architecture is chosen.

- **Why:** Deployment shapes the architecture, so late deployment planning forces rework.
- **When:** Choosing an architecture during initial development, planning deployable units while component structure follows the code (CA-T32).
- **Check:** Design notes list the deployable units, startup order and configuration, and deployment needs no manual setup beyond the build output.
- **Source:** ch. 15, 16, App. A

### CA-T39: Count services before adopting microservices

Count the services to deploy and their connections before splitting the system, and add services only where an operational need justifies them.

- **Why:** Services are expensive to deploy and connect, and they tend to be too coarse.
- **When:** A proposal would split the system into many small services.
- **Not when:** Operational needs already require separate servers or independent services.
- **Check:** The deployment plan lists each service with its startup and connection configuration.
- **Source:** ch. 15, 16

### CA-T40: Write logic against abstract input and output

Write program logic against abstract input and output operations, so the physical device can change without touching the logic.

- **Why:** Device-specific instructions in business logic make a device change expensive and error-prone.
- **When:** Code reads or writes data through an external device or medium.
- **Check:** Business-logic files contain no device-specific instructions or device names.
- **Source:** ch. 15

### CA-T41: Use one entry point to wire components

Build a single top-level entry point, Main as defined in CA-T20, that starts, connects and supervises the other components without depending on their internals.

- **Why:** Start order and wiring then live in one place, so other components need no knowledge of each other.
- **When:** Several components must start in the right order and find each other.
- **Check:** A single entry point starts and wires together all the components.
- **Source:** ch. 16, App. A

### CA-T42: Merge duplicate code only when users change together

Merge duplicated code only when every change to one copy would require the same change to the others.

- **Why:** Look-alike code that serves different use cases tends to diverge, and a shared module then couples them.
- **When:** Two code sections look alike but may evolve along different paths.
- **Check:** Shared code is extracted only where all of its users change for the same reasons.
- **Source:** ch. 16

### CA-T43: Give each screen its own view model

Build a separate view model for each screen instead of passing database records to the user interface.

- **Why:** Passing records to the UI makes it depend on storage types.
- **When:** A database record's structure closely resembles a screen's data.
- **Check:** UI code receives view-model types, not persistence records, and presenters turn output into display-ready strings and flags.
- **Source:** ch. 16, 22

### CA-T45: Stub or keep data in memory before persistence

Stub the data access methods, or implement them in memory, so features that need stored data can be built before storage exists.

- **Why:** Feature work and tests then proceed without waiting for a database or schema.
- **When:** Early development of features that do not yet need real persistence.
- **Check:** Early tests use a stub or in-memory implementation of the data interface.
- **Source:** ch. 17

### CA-T46: Add each storage option as a new implementation

Hide data access behind an interface, and add each storage technology as a new implementation of that interface.

- **Why:** Business rules stay unchanged when storage changes, because they never touch the storage mechanism.
- **When:** Business rules need to load or store data, or a storage technology is added or switched.
- **Check:** The new storage module implements the existing interface, declared with the business rules, and no core class changes.
- **Source:** ch. 17

### CA-T47: Let the database depend on business rules

Let the database component depend on the business rules, and define the data access interface inside the business-rule component.

- **Why:** The query translation then lives in the database component, and the database becomes a replaceable tool.
- **When:** Drawing the dependency between the business-rule component and the database component.
- **Check:** Business-rule components import no database classes, and the interface file lives with the rules.
- **Source:** ch. 17

### CA-T48: Let the GUI depend on business rules

Point the UI's dependencies at the business rules, never the reverse, and keep it replaceable so another interface can take its place.

- **Why:** Business rules can then run with no display, and a new front end needs no change to them.
- **When:** Designing the boundary between a user interface and the business model.
- **Check:** Business-rule components import no GUI classes and run in tests without a GUI.
- **Source:** ch. 17

### CA-T49: Expose only interfaces between components in a monolith

Keep disciplined separation inside one executable by letting components depend only on each other's interfaces.

- **Why:** Teams can then build components independently, and components can later be extracted as services.
- **When:** The system deploys as one executable but several teams or components work on it.
- **Check:** Internal components expose interfaces, and other components depend only on those interfaces.
- **Source:** ch. 18, 34

### CA-T50: Keep service addresses out of high-level code

Keep the names, addresses and locations of lower-level processes and services out of higher-level source code.

- **Why:** Hard-coded addresses bind higher-level code to deployment details that change.
- **When:** A higher-level process or service must start or reach a lower-level one.
- **Check:** Service endpoints come from configuration supplied at startup, not from source code.
- **Source:** ch. 18

### CA-T51: Minimize messages across process and service boundaries

Reduce the number of messages and calls that cross a process or service boundary for each use case.

- **Why:** Each crossing costs marshalling, context switches or network latency that adds up per request.
- **When:** Designing communication between processes on one machine or between services.
- **Check:** The number of interprocess or service calls per use case is counted and kept low.
- **Source:** ch. 18

### CA-T52: Design each boundary for its own cost

Design each kind of boundary, whether monolith, library, process or service, for the cost that crossing it imposes.

- **Why:** Each boundary kind has a different cost, so one design rule fits none of them.
- **When:** Choosing deployment boundaries for a system that spans several servers.
- **Check:** Deployment documentation lists each boundary kind, what crosses it, and its setup and upkeep cost.
- **Source:** ch. 18, 24

### CA-T53: Point dependencies up levels against the data flow

Arrange source dependencies by policy level, even where that direction opposes the flow of data or control.

- **Why:** Policy then stays independent of the input and output details that change more often.
- **When:** Data or control flows one way, but policy level implies a dependency in the opposite direction.
- **Check:** Dependency arrows point toward the higher-level component, even where data flows the other way.
- **Source:** ch. 19, 22, 33

### CA-T54: Keep policy free of device I/O

Have high-level policy read and write through interfaces, never by calling device input and output functions or naming hardware registers directly.

- **Why:** Policy then stays unchanged when the device changes, and only the adapter behind the interface changes.
- **When:** A core transformation needs data from or sends data to a device.
- **Check:** The core module has no device calls or register names, and device I/O components depend on it, not the reverse.
- **Source:** ch. 19, 29

### CA-T55: Model critical concepts as entities

Model each central business concept as an entity that holds its critical data and exposes its critical rules.

- **Why:** Keeping data and the rules that act on it together keeps business logic in one reusable place.
- **When:** A concept is central to the business and would exist without any software.
- **Check:** Entity classes expose business operations, such as calculating interest, rather than screens or queries.
- **Source:** ch. 20

### CA-T56: Put application-specific rules in use cases

Put rules that exist only because the software automates a process into use case objects, which direct the entities.

- **Why:** Entities then keep only rules that hold in any system, which lets them be reused.
- **When:** A rule exists only because software automates a process, such as gating screens.
- **Check:** Use case objects call entity methods and hold the order of the workflow steps.
- **Source:** ch. 20, 22

### CA-T57: Describe use cases by input, output and steps

Describe each use case by its input, its output and its processing steps, without naming screens or delivery technology.

- **Why:** A description free of screens stays valid when the user interface changes.
- **When:** Writing or reviewing a use case specification or the interface to a use case.
- **Check:** Use case specifications name data and steps but no screens, widgets or delivery technology.
- **Source:** ch. 20, 31

### CA-T58: Treat frameworks as tools, not architecture

Use frameworks as tools you control, and keep their base classes and annotations in outer modules.

- **Why:** A framework that dictates the structure makes the framework's authors, not your needs, shape the system.
- **When:** A framework suggests its own project layout or asks business objects to inherit from it.
- **Check:** Framework base classes and annotations appear only in outer modules.
- **Source:** ch. 21, 32

### CA-T59: Evaluate each framework by its exit cost

Assess each framework skeptically and record which parts depend on it and how that dependence is contained.

- **Why:** Frameworks make no commitment to your needs, so the cost of leaving them must be known up front.
- **When:** A framework is proposed for a project.
- **Check:** Design notes record which parts depend on the framework and how that dependence is contained.
- **Source:** ch. 21, 32

### CA-T60: Keep inner circles free of outer names

Keep inner-circle code, the business-rule layers that sit inside the UI, database and framework circles, from naming outer entities.

- **Why:** Outer-circle names would make inner code depend on details it should not know.
- **When:** An inner-circle module needs behavior or data that an outer module provides.
- **Check:** Inner-circle files contain no identifiers or imports from UI, database or framework packages.
- **Source:** ch. 22

### CA-T61: Place controllers, presenters and views in adapters

Place controllers, presenters and views in the interface adapter layer, not in use case code.

- **Why:** Adapters keep presentation details out of the use cases.
- **When:** Building a GUI with an MVC-style structure.
- **Not when:** Top-level package names follow CA-T76, so this rule governs the roles of classes, not folder names.
- **Check:** Controller, presenter and view classes sit on the adapter side, not in use case code.
- **Source:** ch. 22

### CA-T62: Keep SQL and table knowledge in data adapters

Restrict SQL statements and table or row names to the database-facing adapter and the lowest-level data utilities.

- **Why:** Business rules then survive a change of database engine or schema.
- **When:** Code needs to query or update a relational database.
- **Check:** SQL statements and table or column names appear only in data-access files.
- **Source:** ch. 22, 30

### CA-T63: Split GUI code into humble and testable parts

Split behavior into a humble part that is hard to test and a testable part that holds the formatting and branching logic.

- **Why:** Isolated tests catch defects GUI-bound tests cannot reach cheaply, and the split shows where a boundary belongs.
- **When:** Code mixes hard-to-test display behavior with easy-to-test logic.
- **Check:** The hard-to-test class holds no formatting or branching logic.
- **Source:** ch. 23, 25

### CA-T64: Access the database only through gateways

Let interactors reach stored data only through gateway interfaces with one method per operation, and keep gateway implementations free of business rules.

- **Why:** Business rules then stay out of data access code.
- **When:** A use case must create, read, update or delete stored data.
- **Check:** Interactors import gateway interfaces, not SQL or driver types, and gateways hold no business branches.
- **Source:** ch. 23

### CA-T65: Add a boundary once omitting it costs more

Note where a boundary may be needed, and build it once leaving it out costs more than building it.

- **Why:** A missed boundary becomes an expensive refactoring later.
- **When:** Two concerns begin to change at different rates and friction appears.
- **Not when:** No friction has appeared, unless the boundary is an infrastructure line (CA-P4).
- **Check:** Architecture notes record the friction that prompted each boundary decision.
- **Source:** ch. 25

### CA-T66: Keep DI framework references in Main

Use dependency injection annotations and framework calls only in the Main component, and pass the wired dependencies on without the framework.

- **Why:** Business objects then carry no framework dependency and stay portable.
- **When:** The project uses a dependency injection framework to wire components.
- **Check:** Dependency injection framework references appear only in the Main component.
- **Source:** ch. 26, 32

### CA-T67: Express regional differences as configuration

Express regional or variant differences as configuration in one codebase instead of forking the code.

- **Why:** Forked copies drift apart, while configuration keeps one codebase correct for every region.
- **When:** One product must differ by region, and the code is shared between regions.
- **Check:** Regional variation is driven by settings, or by one Main plugin per configuration as its only entry point, not duplicated copies.
- **Source:** ch. 26, App. A

### CA-T68: Do not assume services are decoupled

Do not assume services are decoupled when they share data records, resources or deployment schedules.

- **Why:** Shared records couple services, so a change to one field can break services that read it.
- **When:** Services exchange records, shared resources or network data, or features change shared behavior.
- **Check:** A change to a shared record lists every service that reads the changed field, and plans their releases together.
- **Source:** ch. 27

### CA-T69: Treat test code as the outermost component

Organize tests as the outermost component that depends inward on production code, and keep production code free of test imports.

- **Why:** Tests then exercise the architecture from outside, without shaping production dependencies.
- **When:** Designing or organizing test code alongside production code.
- **Check:** Test packages import production code, production code never imports tests, and unit, acceptance and behavior tests follow this rule.
- **Source:** ch. 28

### CA-T70: Test rules through the API, not the screens

Test business rules through the application's normal API, and keep rule tests away from volatile screens and navigation.

- **Why:** Tests that navigate screens break with every UI change even when the rules are unchanged.
- **When:** Writing tests for business rules that the user interface exposes.
- **Not when:** A state that normal operation cannot reach easily needs the testing API in CA-T71.
- **Check:** Rule tests call application APIs and never navigate GUI screens.
- **Source:** ch. 28, 31

### CA-T71: Give tests a dedicated testing API

Provide a testing API that reaches specific states and bypasses slow or secured steps, and keep it out of production builds.

- **Why:** Tests then set state directly, while the production system keeps its powers safe.
- **When:** Business rule tests need states or access that normal operation does not offer easily.
- **Not when:** The production system, where the API's powers would be dangerous.
- **Check:** Tests set state through the testing API, which reuses the interactors the UI calls, not through login screens.
- **Source:** ch. 28

### CA-T73: Reach OS services only through an abstraction layer

Let application code reach threads, timers and messaging only through an operating system abstraction layer (OSAL) that wraps the real-time operating system (RTOS).

- **Why:** Replacing the operating system then means rewriting the layer, not the application.
- **When:** Application code needs threads, timers or other operating system primitives.
- **Check:** Application modules call OSAL functions and never call RTOS APIs directly.
- **Source:** ch. 29

### CA-T74: Hide hardware behind a hardware abstraction layer

Hide hardware behind a hardware abstraction layer (HAL) whose functions name application services, not bit-level device behavior.

- **Why:** Application code then stays unchanged when hardware parts change.
- **When:** Software needs a hardware service such as storage, indicators or sensors.
- **Check:** Application code calls HAL functions and never names ports, registers or pins.
- **Source:** ch. 29

### CA-T75: Build components separately and group them for deployment

Build each component separately, and group components that change together into deployable bundles.

- **Why:** Groupings can then change with build configuration, not with component code.
- **When:** Choosing how to package compiled components for delivery, when components change together.
- **Not when:** Components that change at different rates should ship apart, as CA-T23 describes.
- **Check:** Build configuration defines components separately, and deployment bundles combine them.
- **Source:** ch. 33

### CA-T76: Group code by domain feature

Organize packages by domain feature or business area, such as orders or catalog, rather than by technical layer.

- **Why:** Packages named by layer scatter one feature across several folders, while feature packages keep it together.
- **When:** Organizing packages around a business feature.
- **Not when:** A quick start matters more than long-term structure, or feature packages alone leave boundaries unenforced.
- **Check:** Top-level package names are domain concepts, not web, service or repository layers.
- **Source:** ch. 34

### CA-T77: Enforce component visibility with the compiler

Make only component interfaces public, give implementation types the narrowest visibility the language offers (for example package-private in Java), and never make a type public by habit.

- **Why:** Architecture rules then fail at compilation, not in a later review or analysis step.
- **When:** Adding classes to a component inside a monolithic codebase.
- **Not when:** Separate assemblies need their own visibility setup, and types used from outside their package must be public.
- **Check:** Implementation classes lack a public modifier, and only interfaces are public.
- **Source:** ch. 34

### CA-T78: Add variants by adding code, not editing modules

Extend behavior by adding new code for each new variant, and leave the existing modules unchanged.

- **Why:** Keeping existing artifacts closed to modification protects the behavior they already deliver.
- **When:** A new variant of existing behavior is requested.
- **Not when:** Only format or settings differ (CA-T16, CA-T67).
- **Check:** New variants appear as new modules, and existing modules stay unchanged in the diff.
- **Source:** ch. 8

### CA-T79: Name domain types in the ubiquitous language

Name domain types with business terms, such as Orders, not technical suffixes such as Repository.

- **Why:** Business terms keep the domain in the language its users share.
- **When:** Naming interfaces or classes inside the domain package.
- **Not when:** Naming CA-T64 gateway interfaces, which interactors use.
- **Check:** Domain type names use business terms, with no technical suffixes such as Repository.
- **Source:** ch. 34
