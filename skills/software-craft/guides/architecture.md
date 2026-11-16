# Architecture: boundaries, dependencies, components, services

This guide covers the structure of a whole system: which way source dependencies point, where boundaries go and what may cross them, how classes group into components and deployable units, how the program is wired at startup, and when to split into services. The single most important idea is the dependency rule: business policy names nothing about the UI, the database, frameworks or devices, and every detail depends inward on that policy, so details can change, wait or be replaced without touching the rules.

**Read this when:** adding a module, package or service, adding an import that crosses a layer or component, choosing or adopting a framework, database or DI container, wiring startup code, a dependency cycle appears, business rules show up in controllers or SQL, someone proposes microservices, splitting a repository into deployable artifacts, adding a regional or provider variant, reviewing package layout or component metrics.

**Entry IDs** such as `WELC-T12` point to `../books/<book>/techniques.md` (T) or `principles.md` (P);
the prefix table is in [SKILL.md](../SKILL.md).

## Contents

- [Core rules](#core-rules)
- [Rules: what crosses a boundary](#rules-what-crosses-a-boundary)
- [Rules: Main and wiring](#rules-main-and-wiring)
- [Rules: components and their metrics](#rules-components-and-their-metrics)
- [Rules: packaging and visibility](#rules-packaging-and-visibility)
- [Rules: monolith, services and deployment](#rules-monolith-services-and-deployment)
- [Playbooks](#playbooks)
- [Where the books disagree](#where-the-books-disagree)
- [Review checklist](#review-checklist)
- [More entries in this area](#more-entries-in-this-area)

## Core rules

### 1. Point every source dependency toward stable policy

Make each import point toward a more stable, higher-level component or toward an interface, never toward a volatile detail. A component is stable when many others depend on it, and volatile when it changes often, as presentation and reports do. When dependencies point this way, a change in a detail cannot force a change in the policy it serves. Clean Architecture and Clean Code state the same rule, and both apply it across every boundary in the system. [CA-P1, CC-P5, CA-T13]

- **Do:** Before adding an import, ask which side is the policy and which is the detail, and make the arrow point at the policy side. Keep that direction even when data or control flows the other way, for example when the policy produces output that a detail writes to a device. [CA-T53, CA-T13]
- **Not when:** Stable platform classes, such as strings, may stay concrete dependencies. Interfaces added everywhere produce ones nobody needs, so add one when a second implementation or an inverted dependency needs it. [CA-P1, CC-P5, CC-T48]
- **Check:** No high-level or stable module imports a low-level or volatile one, and dependency arrows point at the higher-level component even where data flows outward. [CA-P1, CA-T53]

### 2. Keep business rules free of UI, database, web and framework names

Business-rule modules should contain no imports, identifiers, base classes or annotations from UI, database, web or framework packages. These are details that plug into the rules, and keeping them out is what lets the rules be reused, tested and kept while the details change. Clean Architecture describes the rules as inner circles that must not name anything in the outer circles. Learning DDD gives business rules one home by keeping them out of controllers, views and database scripts, and FP in Scala makes the same split between a pure core and a thin layer of effects at the edge. [CA-P2, CA-T60, CA-T58, CC-T53, DDD-T34, FPS-P1]

- **Do:** Keep SQL, HTML, framework and driver types in outer modules, and move any business condition you find in a controller, view or stored script into the rule layer. [CC-T53, DDD-T34, CA-T62]
- **Not when:** Treating the database as a detail concerns the storage technology, not the data model itself. FP in Scala finds that tracking debug logging or memory allocation as a typed effect costs more than it gains. [CA-P2, FPS-P1]
- **Check:** Inner-circle files import no UI, database or framework packages, and controllers, views and database scripts hold no business-rule conditions. [CA-T60, DDD-T34]

### 3. Invert a dependency with an interface the policy side owns

When high-level code must call low-level code, declare an interface in the high-level module and let the low-level module implement it. The source dependency then points at the policy, and interfaces change less often than implementations, so policy stays stable. Learning DDD calls these interfaces ports, and Clean Architecture calls every call across an architectural boundary a polymorphic call through such an interface. [CA-T08, CC-T48, DDD-T36, CA-T06]

- **Do:** Put the interface file in the policy component, name it for what the policy needs, and implement it in the outer module. [CA-T08, DDD-T36]
- **Not when:** When the two components already depend on each other, break the cycle first (rule 7). Do not use templates in place of the interface, because templates decouple code but still force their dependents to recompile. Stable platform classes such as String may stay concrete. [CA-T08, CA-T06, CC-T48]
- **Check:** The high-level module imports an interface that the low-level module implements, the interface lives with the high-level module, and cross-boundary calls use the interface type rather than a concrete class. [CA-T08, CA-T06, CC-T48]

```java
// policy component: owns the port
public interface Orders { Order find(OrderId id); void save(Order o); }
public class PlaceOrder {
  private final Orders orders;              // depends only on the port
  public PlaceOrder(Orders orders) { this.orders = orders; }
}
// database component: depends inward on the policy
class SqlOrders implements Orders { /* SQL and table names live only here */ }
```

### 4. Make the database and the UI depend on the rules

Arrange the arrows so that storage code and GUI code each depend on the rules, never the reverse. The data access interface lives inside the rule component, and the query translation lives in the database component, which makes storage a replaceable tool. The same holds for the GUI, so the rules run with no display and a new front end needs no change to them. [CA-T47, CA-T48, CA-T46]

- **Do:** Let use cases reach stored data only through gateway interfaces with one method per operation, keep gateway implementations free of business branches, and add each new storage technology as one more implementation of the existing interface. [CA-T64, CA-T46]
- **Do:** Keep SQL statements and table or column names in the data-access adapter and the lowest-level data utilities. [CA-T62]
- **Check:** Business-rule components import no database or GUI classes and run in tests without either, interactors import gateway interfaces rather than SQL or driver types, and a new storage module changes no core class. [CA-T47, CA-T48, CA-T64, CA-T46]

### 5. Treat frameworks and vendor code as tools at the edge

Use frameworks as tools you control, and keep their base classes, annotations and calls in outer modules. A framework that dictates your structure lets its authors, not your needs, shape the system, and it makes no commitment to your needs, so its exit cost must be known before adoption. Clean Code and Pragmatic Programmer both wrap vendor APIs in an adapter you own, so a vendor change touches one place. [CA-T58, CA-T59, CC-T51, PP-P5, PP-T12]

- **Do:** When a framework is proposed, record which parts will depend on it and how that dependence is contained. Do not let business objects inherit from framework classes. [CA-T59, CA-T58]
- **Do:** Give the adapter an interface shaped by your application's needs, and keep the external system's endpoint paths, schema names and error codes inside that one adapter. [CC-T51, PP-T13]
- **Check:** Framework base classes and annotations appear only in outer modules, vendor types appear only inside adapters, and design notes record each framework's dependents and containment. [CA-T58, CC-T51, CA-T59]

For the shape of the adapter itself, see [module-design](module-design.md) and the [design-patterns](design-patterns.md) guide.

### 6. Put devices, hardware and OS services behind abstraction layers

Write logic against abstract input and output operations, and let high-level policy read and write through interfaces instead of calling device functions or naming registers. Device-specific instructions inside business logic make every device change expensive and error-prone. Clean Architecture applies this down to embedded code with an operating system abstraction layer for threads, timers and messaging, and a hardware abstraction layer whose functions name application services rather than bit-level behavior. [CA-T40, CA-T54, CA-T73, CA-T74]

- **Do:** Keep code that touches a screen, socket, hardware port or hard-to-test framework in a thin layer that only forwards calls, so the logic outside it stays testable. [CC-T13]
- **Do:** Make the device I/O component depend on the core module, not the reverse. [CA-T54]
- **Check:** Business-logic files contain no device names, port, register or pin names, or direct real-time OS calls, and the forwarding layer holds no branches or loops. [CA-T40, CA-T74, CA-T73, CC-T13]

### 7. Keep the component dependency graph acyclic

Break a dependency cycle as soon as it appears, so no component reaches itself through its dependencies. Members of a cycle must be released and tested as one large component, and an acyclic graph keeps a valid build order. [CA-T28, CC-T50]

- **Do:** Break the cycle in one of two ways. If one side needs only a few methods, have it declare an interface that the other side implements. If both need the same classes, move those classes into a new component that both depend on. [CA-T31, CC-T50]
- **Check:** Build tooling reports every component cycle as an error, the diff adds no dependency that closes a loop, and after a fix neither original component imports the other. [CA-T28, CC-T50, CA-T31]

### 8. Judge the architecture by the cost of change

Judge a structure by the effort it takes to change, build, deploy and maintain the system over its life, not only by whether today's features work. A system that cannot change eventually becomes useless, so changeability outranks rigid present behavior. POSD defines complexity the same way, as whatever makes change hard, and Tidy First treats the cost of software as roughly the cost of changing it. [CA-P7, POSD-P1, TF-P5]

- **Do:** In each design review, estimate the cost of the changes most likely to come, and name the future behaviors a structural change makes possible. [CA-P7, TF-P5]
- **Check:** Review notes estimate the cost of likely future changes, and a typical rule or format change touches one owning module. [CA-P7, POSD-P1]

### 9. Defer infrastructure decisions behind a boundary

Keep choices of framework, database, web server and view technology open until the use cases and constraints settle them. Put each infrastructure choice behind a boundary, and choose at the latest responsible moment, once the core no longer depends on it. Clean Code builds early features against in-memory storage behind a data interface for the same reason, so policy can be built and tested while the storage question is still open. SWE at Google adds the general preference for reversible options. [CA-P4, CC-T54, CA-T45, SWE-P8]

- **Do:** Stub the data access methods, or implement them in memory or in files, so features that need stored data can be built and tested before a schema exists. [CA-T45, CC-T54]
- **Do:** When a dependency on hardware or a service is not finished, define your own local interface for it and test clients against a fake. [CC-T52]
- **Check:** Early builds and tests use a stub, in-memory or file implementation of the data interface, and database and framework choices are confined to one module the core does not reference. [CA-T45, CC-T54, CA-P4]

## Rules: what crosses a boundary

### 10. Pass plain data structures across boundaries

Data that crosses a boundary should be simple structures, transfer objects or maps, never entities, database rows or framework objects. Each side then stays free of the other side's formats. [CA-P6]

- **Do:** Define a plain request and response structure for each use case, and describe each use case by its input, its output and its processing steps without naming screens or delivery technology. [CA-P6, CA-T57]
- **Do:** Build a separate view model for each screen, even when a database record looks almost the same as the screen's data, and let presenters turn output into display-ready strings and flags. [CA-T43]
- **Check:** Boundary parameters are plain structures, UI code receives view-model types rather than persistence records, and use case specifications name data and steps but no widgets. [CA-P6, CA-T43, CA-T57]

```java
// crosses the boundary: plain data, no entity, no row, no framework type
record PlaceOrderRequest(String customerId, List<String> skus) {}
record PlaceOrderResponse(String orderId, String status) {}
// the controller maps HTTP to the request; the presenter maps the response to a view model
```

### 11. Split business logic into entities and use cases

Model each central business concept, one that would exist without any software, as an entity that holds its critical data and exposes its critical rules. Put rules that exist only because software automates a process into use case objects that direct the entities and hold the order of the workflow steps. Entities then keep only rules that hold in any system, which lets them be reused. [CA-T55, CA-T56]

- **Do:** Keep transaction handling in one in-process service layer that every entry point calls, so controllers and message handlers only translate input and output. [DDD-T35]
- **Not when:** When the business logic is already a transaction script, that script can serve as the service layer. [DDD-T35]
- **Check:** Entity classes expose business operations rather than screens or queries, use case objects call entity methods and own the step order, and service methods own the transaction. [CA-T55, CA-T56, DDD-T35]

How rich the entities should be, aggregates and consistency boundaries belong to [domain-modeling](domain-modeling.md).

### 12. Keep controllers, presenters and views in the adapter layer

Place controllers, presenters and views on the interface-adapter side, not in use case code. The adapters keep presentation details out of the use cases. [CA-T61]

- **Not when:** Top-level package names follow the feature rule (rule 24), so this rule governs the role each class plays, not the folder names. [CA-T61]
- **Check:** Controller, presenter and view classes sit on the adapter side, and none of their logic sits in use case code. [CA-T61]

### 13. Translate foreign models where they enter

Map another system's or context's types into your own types inside one translation layer, so foreign types never reach the domain. The consumer's model then stays simple. [DDD-T40]

- **Not when:** If the supplier's model suits the consumer, conforming to it is simpler. [DDD-T40]
- **Check:** Upstream types are mapped inside one translation module, and domain modules do not import them. [DDD-T40]

Integration patterns between contexts are covered in [domain-modeling](domain-modeling.md).

### 14. Design each boundary for what crossing it costs

A boundary can be a source-level split inside one executable, a library, a local process or a service, and each kind has a different crossing cost. Design each one for that cost rather than applying one rule to all. Each crossing of a process or service boundary costs marshalling, context switches or network latency that adds up per request. [CA-T52, CA-T51]

- **Do:** Count the interprocess or service calls each use case makes, and reduce them. [CA-T51]
- **Check:** Deployment documentation lists each boundary kind, what crosses it, and its setup and upkeep cost, and the call count per use case is known and kept low. [CA-T52, CA-T51]

### 15. Keep service names and addresses out of high-level code

Keep the names, addresses and locations of lower-level processes and services out of higher-level source code, because hard-coded addresses bind that code to deployment details that change. Release It! keeps hostnames, ports and other environment values out of the release artifact altogether. [CA-T50, RI-P8]

- **Do:** Supply endpoints through configuration at startup. [CA-T50, RI-P8]
- **Check:** Service endpoints come from startup configuration, and source and build outputs contain no production hostnames or ports. [CA-T50, RI-P8]

## Rules: Main and wiring

### 16. Gather concrete dependencies in Main

Some concrete dependencies cannot be removed from the design. Collect them in one small component, Main, the startup code that creates the factories, globals and concrete objects and passes them inward. Concrete names then stay in one place instead of spreading into the design, and the policy depends only on interfaces and stays testable. Clean Code calls this wiring in the outermost layer, Learning DDD calls it the composition root, and Design Patterns names concrete classes only at creation. [CA-T20, CC-T49, DDD-T36, GOF-P1]

- **Do:** Make one top-level entry point that starts the components in the right order, connects and supervises them, without depending on their internals. [CA-T41]
- **Do:** Give policy classes their collaborators as constructor parameters instead of constructing them. [CC-T49, CC-T12]
- **Not when:** A class that never changes, such as a stable platform class like String, needs no abstract type and may be constructed directly where it is used. [GOF-P1, CA-P1]
- **Check:** Concrete class names and string-literal configuration lists appear only in Main, a single entry point starts and wires all components, and policy classes never create their collaborators. [CA-T20, CA-T41, CC-T49]

```java
public final class Main {                       // the only place concrete types meet
  public static void main(String[] args) {
    Config cfg = Config.fromEnv();
    Orders orders = new SqlOrders(cfg.dbUrl());
    PlaceOrder placeOrder = new PlaceOrder(orders);
    new HttpServer(cfg.port(), new OrderController(placeOrder)).start();
  }
}
```

### 17. Create volatile objects through a factory that Main supplies

When client code needs an instance of a class that changes often, have it call an abstract factory through an interface instead of naming the concrete class. Main creates the concrete factory and stores it behind the abstract factory type, so the rest of the application depends only on the abstraction. [CA-T19, CA-T21]

- **Do:** Keep an unavoidable switch on type inside that factory or Main, behind an interface. [CC-T39]
- **Not when:** Clean Code does not apply this switch rule when behavior changes far more often than the data types do. [CC-T39]
- **Check:** Client source never names the concrete class it instantiates, and startup code assigns the concrete factory to a variable of the abstract factory type. [CA-T19, CA-T21]

### 18. Keep dependency injection framework references in Main

If the project uses a DI framework, use its annotations and calls only in the Main component, and pass the wired objects on without the framework. Business objects then carry no framework dependency and stay portable. [CA-T66]

- **Check:** DI framework imports and annotations appear only in the Main component. [CA-T66]

### 19. Express variants as configuration or plugins, not forks

Express regional or product-variant differences as configuration in one codebase, or as one Main plugin per configuration, instead of forking the code. Forked copies drift apart. When one provider cannot implement a shared interface exactly, put its format differences in configuration keyed by its endpoint, not in code branches on its name. [CA-T67, CA-T16]

- **Do:** Build optional extensions that ship independently of the core as runtime plugins loaded through a defined interface, so the core stays unchanged when they are added or removed. [CA-T24]
- **Check:** Regional variation is driven by settings or one Main per configuration, shared code has no branch on a provider name, and the core loads optional components only through the defined interface. [CA-T67, CA-T16, CA-T24]

See the tension on configuration versus new code below.

## Rules: components and their metrics

### 20. Group code by reason and rate of change

Put code that changes for the same reason at the same time in one component, and separate code that changes for different reasons. The same test drives single responsibility at class level and component boundaries at system level. Code shared by different stakeholder groups couples them, so one group's edit can break another group's behavior. [CA-P3, CA-T12, CA-T11]

- **Do:** Before placing a class, ask which stakeholder or cause would make it change, and keep logic serving different actors in different modules. [CA-P3, CA-T11]
- **Do:** Put classes in one component only when they serve one stated purpose, so the component can be released and reused as a whole. [CA-T26]
- **Check:** A change made for one reason touches one component, no shared helper is called from modules owned by different actors, and every class in a component serves its stated purpose. [CA-T12, CA-T11, CA-T26]

Whether to merge look-alike code that different actors use is covered in [module-design](module-design.md).

### 21. Derive components from classes that exist

Build the component structure from real classes as they appear, not from a plan drawn before the code. Components designed before any classes exist usually miss how the code really changes. [CA-T32]

- **Check:** Every component contains real classes, and no placeholder component exists ahead of its classes. [CA-T32]

### 22. Measure stability by counting dependencies

Compute instability as fan-out divided by fan-in plus fan-out, a number from 0 (maximally stable) to 1. Stability then reflects how many components depend on a component, which is what makes it hard to change, rather than how often it has changed. Use this number to check that every dependency points toward lower instability. [CA-T33, CA-T13]

- **Check:** A report lists fan-in, fan-out and instability per component, and every dependency arrow points toward a component with lower instability. [CA-T33, CA-T13]

### 23. Make stable components abstract and keep volatile ones concrete

Stable components should consist mainly of interfaces and abstract classes, so high-level policy can be extended without editing it. Keep each component near the main sequence, the line where abstractness plus instability equals one. A component far from that line is either rigid, because it is stable and concrete, or useless, because it holds abstractions nothing uses. Avoid a component that is widely used, concrete and changing often at once, such as a busy database schema, because its many dependents make each change expensive. [CA-T36, CA-T34, CA-T35]

- **Not when:** Not every component should be stable, since volatile parts stay unstable and depend on stable ones. A concrete component that rarely changes, such as a common string library, is harmless. The metric is imperfect, so judge flagged components on design reasons too. [CA-T36, CA-T35, CA-T34]
- **Check:** Stable components hold mainly interfaces, distance from the main sequence is tracked per release, and volatile components with many dependents and no interfaces are listed for review. [CA-T36, CA-T34, CA-T35]

## Rules: packaging and visibility

### 24. Name top-level packages after features and use cases

Organize the top level by domain feature or business area, such as orders or catalog, so the structure shows what the system does rather than which framework it uses. Packages named by technical layer scatter one feature across several folders. Learning DDD makes the same move inside one large bounded context, giving each subdomain its own module with an explicit interface, because horizontal layers spread one subdomain's rules across the whole context. [CA-T37, CA-T76, DDD-T68]

- **Do:** Name domain types with business terms, such as Orders, rather than technical suffixes such as Repository. [CA-T79]
- **Not when:** A quick start can matter more than long-term structure, and feature packages alone can leave boundaries unenforced (rule 25). The business-term naming rule does not apply to gateway interfaces that interactors use. [CA-T76, CA-T79]
- **Check:** Top-level names are domain concepts, not web, service or repository layers, each subdomain has its own module reached through its interface, and domain type names carry no technical suffixes. [CA-T76, CA-T37, DDD-T68, CA-T79]

### 25. Let the compiler enforce component visibility

Make only a component's interfaces public, give implementation types the narrowest visibility the language offers, such as package-private in Java, and do not make a type public by habit. Architecture rules then fail at compilation instead of in a later review. [CA-T77]

- **Not when:** Separate assemblies need their own visibility setup, and types used from outside their package must be public. [CA-T77]
- **Check:** Implementation classes lack a public modifier, and only interfaces are public. [CA-T77]

## Rules: monolith, services and deployment

### 26. Keep components behind interfaces inside a monolith

A system that deploys as one executable can still keep disciplined separation by letting its components depend only on each other's interfaces. Teams can then build components independently, and a component can later be extracted as a service. [CA-T49, DDD-T68]

- **Check:** Internal components expose interfaces, and other components depend only on those interfaces. [CA-T49]

### 27. Count services and integration calls before splitting

Before splitting a system into services, count the services to deploy, their connections and the integration calls each one adds, and add a service only where an operational need justifies it. Services are expensive to deploy and connect, they tend to be too coarse, and distributed services carry integration work a single codebase never does. DDIA agrees that a single machine is simpler to build and run, so each distributed component needs a named requirement. [CA-T39, DDD-T69, DDIA-P6]

- **Not when:** Operational needs may already require separate servers or services. Fault tolerance, scale, latency or legal requirements can force distribution. [CA-T39, DDIA-P6]
- **Check:** The split proposal lists each new service with its startup and connection configuration and the integration calls it adds, and each distributed component names its requirement. [CA-T39, DDD-T69, DDIA-P6]

### 28. Keep each service deep with a small interface

Give each service a small public interface that hides complex logic, and stop splitting once services turn shallow. A shallow service adds integration cost without hiding complexity. POSD applies the same depth test to every unit with an interface, services included. [DDD-T60, POSD-P2]

- **Check:** A service's public interface lists few operations, no service mostly forwards calls, and no boundary needs data from most other services. [DDD-T60, POSD-P2]

### 29. Give each service its own private database

Keep each service's database private, and let other services reach its data only through its public API. Services that read another's tables bypass its interface and couple the teams, so that service can no longer change its storage or schema freely. [DDIA-T07, DDD-T70]

- **Not when:** During a strangler migration, old and new contexts may share a database for a time when splitting the data would need distributed transactions. [DDD-T70, DDD-T58]
- **Check:** No two services connect to the same schema, and clients call only public APIs. [DDIA-T07, DDD-T70]

See [data-systems](data-systems.md) for how data moves between services.

### 30. Do not assume separate services are decoupled

Services that share data records, resources or deployment schedules are coupled, whatever their process boundaries suggest. A change to one field of a shared record can break every service that reads it. Keep the rules for one entity in one module of one context, because rules spread across services, stored procedures or teams drift apart. [CA-T68, DDD-T71]

- **Check:** A change to a shared record lists every service that reads the changed field and plans their releases together, and each rule for one entity is implemented once. [CA-T68, DDD-T71]

### 31. Plan deployment units while choosing the architecture

Decide the deployable units, their startup order and their configuration during initial design, because deployment shapes the architecture and late planning forces rework. The component structure inside those units still follows the code as it appears. [CA-T38, CA-T32]

- **Check:** Design notes list the deployable units, their startup order and configuration, and deployment needs no manual setup beyond the build output. [CA-T38]

Rollout, canaries and runtime configuration are in [production-reliability](production-reliability.md).

## Playbooks

### When you add a feature that needs storage or an outside service
1. Describe the use case by input, output and steps, with no screens or technology named. [CA-T57]
2. Put the application-specific steps in a use case object, and any rule that would exist without software in an entity. [CA-T56, CA-T55]
3. Declare the port interface the use case needs inside the rule component, named for the need, with one method per operation. [CA-T08, CA-T64, DDD-T36]
4. Implement the port in memory or as a stub first, and test the use case against it without a database or server. [CA-T45, CC-T54, CC-T14]
5. Add the real adapter as a new implementation in the outer module, keeping SQL, vendor types and endpoint details inside it. [CA-T46, CA-T62, CC-T51, PP-T13]
6. Define plain request and response structures for the controller, and a view model for any screen. [CA-P6, CA-T43]
7. Wire the adapter into the use case in Main, and read endpoints and credentials from startup configuration. [CA-T20, CC-T49, CA-T50, RI-P8]

### When a dependency cycle appears between components
1. Find the dependency that closes the loop, ideally from build tooling that fails on cycles. [CA-T28]
2. If one side needs only a few methods, declare an interface in the calling component and let the other implement it. [CA-T31, CC-T50]
3. If both sides need the same classes, move those classes into a new component that both depend on. [CA-T31]
4. Recompute instability for the components involved, and check that every arrow now points toward lower instability. [CA-T33, CA-T13]
5. Confirm that neither original component imports the other. [CA-T31]

### When someone proposes a framework or a DI container
1. Record which parts would depend on the framework and how that dependence would be contained, so the exit cost is known. [CA-T59]
2. Keep framework base classes and annotations in outer modules, and do not let business objects inherit from it. [CA-T58]
3. For a DI container, confine its annotations and calls to Main, and pass the wired objects on as plain constructor arguments. [CA-T66, CC-T49]
4. Wrap any vendor API in an adapter whose interface follows your needs. [CC-T51, PP-T12]
5. Check that rule modules still import no framework package. [CA-P2, CC-T53]

### When someone proposes splitting a monolith into services
1. Name the operational need behind each proposed service, such as fault tolerance, scale, latency or a legal constraint. Without one, keep it in the monolith. [CA-T39, DDIA-P6]
2. List each new service with its startup and connection configuration and the integration calls it adds, and weigh that cost. [CA-T39, DDD-T69]
3. Before extracting, make the component depend only on interfaces inside the monolith, with compiler-enforced visibility. [CA-T49, CA-T77]
4. Check depth: the service should hide complex logic behind a small interface, and should not need data from most other services. [DDD-T60]
5. Count the calls each use case would make across the new boundary, and redesign the interface to keep that number low. [CA-T51, CA-T52]
6. Give the service its own database and expose its data only through its API, apart from a temporary shared database during a strangler migration. [DDIA-T07, DDD-T70]
7. List every shared record and resource, and plan releases of the services that read it together. [CA-T68]

### When business rules are leaking into controllers, SQL or framework code
1. Find the rule conditions sitting in controllers, views, stored scripts or framework callbacks. [DDD-T34]
2. Move transaction orchestration into one service layer that every entry point calls, leaving controllers to translate input and output. [DDD-T35]
3. Move each rule into an entity or use case, and replace direct storage calls with a gateway interface the rule side owns. [CA-T55, CA-T56, CA-T64]
4. Push SQL and table names down into the data adapter. [CA-T62]
5. Do this in small, tested steps, as the [legacy-code](legacy-code.md) and [refactoring](refactoring.md) guides describe.

### When you need a regional, provider or customer variant
1. If only formats or settings differ, drive the difference from configuration keyed by region or endpoint, in one codebase. [CA-T67, CA-T16]
2. If whole configurations differ, give each its own Main plugin as its only entry point. [CA-T67]
3. If behavior differs, add the variant as new code, such as a new class, and leave existing modules unchanged. [CA-T78, CC-T45]
4. If the variant is an optional extension that ships on its own schedule, load it as a runtime plugin through a defined interface. [CA-T24]
5. Check that no shared code branches on a provider or region name. [CA-T16]

### When you split a codebase into components or artifacts
1. Start from the classes that exist, and group them by reason and rate of change and by the actor they serve. [CA-T32, CA-P3, CA-T11]
2. Decide per group whether it ships on its own or in a bundle, using the change-rate condition in the tension below. [CA-T23, CA-T75]
3. Keep the graph acyclic and pointing toward stability. [CA-T28, CA-T13]
4. For a component other teams will use, give it a version number and release notes, and have dependents pin released versions. [CA-T25, CA-T29]
5. Track instability and distance from the main sequence per release. [CA-T33, CA-T34]

## Where the books disagree

### Should a boundary or interface go in now, or wait?
- **Clean Architecture:** Put each infrastructure choice, such as the database, framework or UI, behind a boundary early, so the decision can stay open. Other boundaries are noted when foreseen and built once leaving them out costs more than building them, which shows as two concerns changing at different rates with friction between them. [CA-P4, CA-T65]
- **Clean Code:** Add no interface, extension point or option until a current caller uses it, and add a policy interface when a second implementation or an inverted dependency needs it. Exceptions are growth that is a confirmed business direction, or high odds of needing the hook. [CC-T77, CC-P5]
- **TDD and Design Patterns:** Add an abstraction only when a failing test or a real variation calls for it, and skip an abstraction for one implementation unless clients must avoid recompiling. A system-shaping choice still deserves careful thought before code. [TDD-P9, GOF-P4]
- **Decide:** For the infrastructure lines named in rule 9 (framework, database, web server and view technology), the inverted dependency itself is the need, so declare the port now and back it with a stub or in-memory implementation. [CA-P4, CA-T65, CC-P5, CC-T54] For any other boundary, wait until friction appears, a second implementation exists, a test needs it, clients must avoid recompiling, or growth in that direction is confirmed or highly likely, and record the reason in the architecture notes. [CA-T65, CC-T77, TDD-P9, GOF-P4]

### One deployable or several?
- **Clean Architecture, independent components:** Make each component its own deployable artifact when teams divide the work or components change at different rates, so each can be released without the rest. [CA-T23]
- **Clean Architecture, bundles:** Build components separately but ship those that change together in one bundle, so groupings change through build configuration alone. [CA-T75]
- **Clean Architecture, Learning DDD and DDIA, on services:** Services are expensive and add integration work, and a single machine is simpler. [CA-T39, DDD-T69, DDIA-P6]
- **Decide:** Use the rate of change. Components that always change and ship together go in one bundle, and components that change at different rates, or belong to different teams, ship apart. [CA-T23, CA-T75] Separate deployable artifacts are not separate services. Go to a separate service only when an operational requirement names it, and otherwise keep the separation as interfaces inside the monolith. [CA-T52, CA-T39, CA-T49, DDIA-P6]

### Shape components for reuse or for ease of change?
- **Clean Architecture, reuse side:** Group classes into one cohesive component that can be released and reused as a whole, with version numbers, release notes and pinned dependencies for its users. [CA-T26, CA-T25, CA-T29]
- **Clean Architecture, change side:** In a young or ordinary application with few dependents, shape components for ease of change and leave reuse for later, since early reuse guesses at needs. [CA-T27]
- **Decide:** If other projects already draw on the component, design for reuse and release it with versions and notes. Otherwise shape it so one feature's change stays inside one component. [CA-T27, CA-T25]

### Configuration or new code for a new variant?
- **Clean Architecture, open-closed side:** Add a new variant as new code and leave existing modules unchanged, which protects the behavior they already deliver. Clean Code agrees and adds new behavior as new classes. [CA-T78, CC-T45]
- **Clean Architecture, configuration side:** Express regional differences and provider formats as configuration in one codebase rather than code branches or forks. [CA-T67, CA-T16]
- **Decide:** When only formats or settings differ, use configuration. When behavior differs, add a new implementation. [CA-T78, CA-T16, CA-T67]

### Is a forwarding adapter around a vendor or device worth having?
- **Clean Code:** Wrap vendor APIs and framework or hardware calls in a thin layer whose methods only delegate, so vendor types stay in one place and the logic outside stays testable. A vendor adapter is the stated exception to the rule against forwarding helpers. [CC-T51, CC-T13, CC-T33]
- **Pragmatic Programmer:** Wrap each vendor API in an abstraction you own, and keep its endpoint paths, schema names and error codes in that one adapter. [PP-T12, PP-T13]
- **POSD:** Wrappers that only forward calls add little and are removed, unless they keep an external interface unchanged. [POSD-P2, POSD-T43]
- **Decide:** At a vendor, framework, hardware or OS edge, keep the adapter, since it is the one place the external interface appears. [CC-T51, CC-T33, PP-T13] Between your own modules, do not add a layer that only forwards. Details are in [module-design](module-design.md). [POSD-P2]

### Layers or features at the top of the source tree?
- **Clean Architecture and Learning DDD, features:** Name the top level after features and use cases, and split a large context into one module per subdomain. [CA-T37, CA-T76, DDD-T68]
- **Clean Architecture, layer roles:** Controllers, presenters and views belong to the adapter layer, and use cases and entities to the inner layers. [CA-T61, CA-T56]
- **Decide:** These rules do not conflict, because the entry for layer roles says it governs class roles, not folder names. Use features for top-level packages and keep the layer roles inside each feature. Use layer-named top-level packages only when a quick start matters more than long-term structure, and add compiler-enforced visibility where feature packages alone leave boundaries unenforced. [CA-T61, CA-T76, CA-T77]

## Review checklist

- [ ] No new import in the diff runs from policy or a stable component to a detail or a more unstable component. [CA-P1, CA-T13]
- [ ] Business-rule files import no UI, database, web, framework or DI package and name no outer-circle identifier. [CA-P2, CA-T60, CC-T53, CA-T66]
- [ ] Controllers, views and database scripts contain no business-rule conditions. [DDD-T34]
- [ ] Each new port interface lives in the policy component, and its implementation lives in an outer module. [CA-T08, CC-T48, DDD-T36]
- [ ] SQL statements and table or column names appear only in data-access files. [CA-T62]
- [ ] Gateway implementations contain no business branches. [CA-T64]
- [ ] Vendor and framework types appear only inside adapters, and framework base classes only in outer modules. [CC-T51, CA-T58]
- [ ] Logic files name no device, port, register, pin or real-time OS call. [CA-T40, CA-T73, CA-T74]
- [ ] Boundary signatures take and return plain structures, and UI code receives view models, not records or entities. [CA-P6, CA-T43]
- [ ] Volatile concrete classes are created only in Main or in a factory that Main supplies, and policy classes receive collaborators through constructors. [CA-T20, CA-T19, CC-T49, GOF-P1]
- [ ] Service endpoints and environment values come from startup configuration, not source. [CA-T50, RI-P8]
- [ ] The build reports no component cycle, and the diff closes no loop. [CA-T28, CC-T50]
- [ ] Implementation classes are not public, and only component interfaces are. [CA-T77]
- [ ] Top-level package names are features or use cases, not technical layers. [CA-T76, CA-T37]
- [ ] Shared code has no branch on a provider or region name, and variants arrive as configuration or new modules. [CA-T16, CA-T67, CA-T78]
- [ ] Each new interface or boundary has a current caller, a second implementation, an infrastructure line, or recorded friction behind it. [CC-T77, CA-T65, CC-P5]
- [ ] A new service names its operational requirement and lists the integration calls it adds. [CA-T39, DDD-T69, DDIA-P6]
- [ ] No service connects to another service's database or tables. [DDIA-T07, DDD-T70]
- [ ] A change to a shared record lists every service that reads the field. [CA-T68]
- [ ] Reusable components carry a version and release notes, and dependents pin a release. [CA-T25, CA-T29]
- [ ] Fan-in, fan-out, instability and main-sequence distance are reported for changed components. [CA-T33, CA-T34]
- [ ] A framework adoption records its dependents and how they are contained. [CA-T59]

## More entries in this area

- `CA-T10` — Store changes as transactions with periodic snapshots: when the history of changes matters and full replay would get slow, append each change and read state from the latest snapshot; see [data-systems](data-systems.md) and [domain-modeling](domain-modeling.md).
- `CA-T25` — Publish release notes with each reusable component: when a component is shared with other teams, version it and say which dependents each change affects; see [project-and-team](project-and-team.md).
- `CA-T29` — Depend on pinned released versions: when another team releases mid-work, stay on your pinned release and adopt the new one on your own schedule.
- `CA-T41` — Use one entry point to wire components: when several components must start in order and find each other.
- `CA-T43` — Give each screen its own view model: when a record's structure closely resembles a screen, still pass a view model.
- `CA-T52` — Design each boundary for its own cost: when a system spans several servers, document each boundary kind and its upkeep.
- `CA-T54` — Keep policy free of device I/O: when a core transformation reads from or writes to a device.
- `CA-T73` — Reach OS services only through an abstraction layer: embedded or real-time code that needs threads, timers or messaging.
- `CA-T74` — Hide hardware behind a hardware abstraction layer: embedded code that needs storage, indicators or sensors.
- `CA-T79` — Name domain types in the ubiquitous language: naming interfaces and classes inside the domain package, except gateway interfaces.
- `CC-T13` — Keep framework and hardware calls in a thin layer: when code must touch a screen, socket or hard-to-test framework.
- `CC-T52` — Define your own interface for a missing dependency: when hardware or a service is not finished yet.
- `DDD-T60` — Keep microservices deep and their interfaces small: when reviewing a service that mostly forwards calls.
- `DDD-T71` — Keep one entity's rules in one module: when work on one shared entity is split across teams or stored procedures.
- Testing business rules without delivery mechanisms (CA-P5, CA-T63, CA-T69, CA-T70, CA-T71) is covered in [testing](testing.md).
