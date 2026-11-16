# Learning Domain-Driven Design — techniques

### DDD-T01: Classify subdomains by competitive advantage
Label each subdomain core, supporting or generic, asking whether someone would pay for it on its own.

- **Why:** Core parts earn the business its advantage, and a painful legacy part no product replaces is likely core.
- **When:** Planning how much design effort each part of the business domain needs.
- **Not when:** The business has not yet described its strategy, so classify it first.
- **Check:** Design notes record each subdomain's type and business reason.
- **Source:** ch. 1, 13 p. 30

### DDD-T02: Recheck subdomain types as business changes
Revisit each subdomain's type when strategy, competitors or products change.

- **Why:** A core subdomain can become generic, so an old label can mislead later design choices.
- **When:** A product replaces custom code, or the business value of an area shifts.
- **Check:** Each subdomain has a review date, and each type change has a dated reason beside it.
- **Source:** ch. 1, 11, Appendix A p. 32

### DDD-T03: Keep core subdomains in-house and distilled
Build core subdomains in-house, and extract their generic and supporting parts into separate subdomains.

- **Why:** Core logic is the company's advantage, and mixed-in generic code hides it.
- **When:** Deciding who builds a differentiating subdomain, or reviewing its module contents.
- **Not when:** Supporting and generic subdomains can be outsourced or used for onboarding.
- **Check:** Core modules hold no generic or supporting functions, and design notes name an in-house owner.
- **Source:** ch. 1, 11 p. 36

### DDD-T04: Staff core subdomains with senior engineers
Assign the most experienced engineers to core subdomains, and apply the most advanced practices there.

- **Why:** Core requirements keep changing, so they need the strongest skills and guarded testing.
- **When:** Staffing a core subdomain whose requirements change often.
- **Check:** Core modules have automated tests that guard their frequent changes.
- **Source:** ch. 1 p. 36

### DDD-T05: Adopt proven solutions for generic subdomains
Use a maintained library or product for generic capabilities such as authentication, and keep it updated.

- **Why:** Generic problems are solved, and their solutions receive security patches over time.
- **When:** A subdomain is a solved problem and integrating a ready solution is manageable.
- **Not when:** Integrating the ready solution costs more than building the feature.
- **Check:** Dependency manifests pin maintained versions, and upgrades appear regularly.
- **Source:** ch. 1 p. 32

### DDD-T06: Keep supporting subdomains simple and cheap
Keep supporting subdomains simple, build them in-house only without a ready product, and invest less effort.

- **Why:** Supporting logic changes rarely and adds little business value, so elaborate design does not pay.
- **When:** A subdomain has simple data entry, ETL or CRUD logic without competitive value.
- **Not when:** Advanced modeling needs a check for accidental complexity or a hidden edge first.
- **Check:** Supporting modules use framework scaffolding and simple scripts or records, not extra abstraction layers.
- **Source:** ch. 1, Closing Words, Appendix A p. 33

### DDD-T07: Start subdomain analysis from departments
Use departments and organizational units as a first draft of subdomains, then refine them by client service (DDD-P1).

- **Why:** Departments already group related business work, which gives a quick starting map.
- **When:** Starting subdomain analysis in an organization you do not know well.
- **Check:** The subdomain list starts from department responsibilities and then splits them finer.
- **Source:** ch. 1, 13 p. 37

### DDD-T08: Bound subdomains by coherent use cases
Draw a subdomain's boundary around use cases that share actors and closely related data.

- **Why:** A finer split would pull apart use cases that work on shared data.
- **When:** Deciding when to stop splitting a subdomain into finer subdomains.
- **Check:** Use cases in one module involve the same actors and operate on related data.
- **Source:** ch. 1, 11 p. 38

### DDD-T09: Use domain terms in code names
Name classes, methods, tests and tickets with the terms domain experts use.

- **Why:** Shared terms keep requirements, tests and code aligned with the business.
- **When:** Creating or renaming aggregates, value objects, commands, events or test names.
- **Check:** Class and test names match the glossary terms used in the context's requirements.
- **Source:** ch. 2, 6, 13 p. 48

### DDD-T10: Give each term one meaning
Give each business term one meaning in its scope, and split overloaded terms into explicit concepts rather than prefixed names.

- **Why:** One word with two meanings produces wrong rules, so separate names prevent mixing them.
- **When:** A word such as policy covers unrelated concepts, or one concept gets prefixed names in several areas.
- **Check:** No class carries two unrelated concepts, and a repeated name prefix signals a missing boundary.
- **Source:** ch. 2, 3, Appendix A p. 52

### DDD-T11: Keep the glossary current and shared
Keep a shared glossary and update it in the same commit as any change to a term's meaning.

- **Why:** New members onboard faster, and the language stays aligned with the model as it evolves.
- **When:** A term changes meaning, or new people join the project.
- **Check:** A commit that renames or redefines a domain term also changes the glossary file.
- **Source:** ch. 2 p. 55

### DDD-T12: Model behavior and invariants in domain objects
Give domain entities behavior methods that enforce business rules, not only data fields.

- **Why:** Rules kept in the objects stay enforced for every caller, so they cannot drift apart.
- **When:** Designing a domain entity that must enforce business rules and invariants.
- **Check:** Domain classes expose business-action methods, and callers cannot assign their invariant fields.
- **Source:** ch. 2, 6 p. 54

### DDD-T13: Use value objects instead of primitives
Represent names, money and identifiers with named domain types, not raw strings or numbers.

- **Why:** Money and identifiers need their own rules, which a bare number or string cannot carry.
- **When:** A concept is held as a string, integer or dictionary, such as a price or a phone number.
- **Not when:** A supporting subdomain has simple logic, so DDD-T06 applies.
- **Check:** Domain method parameters and properties use named domain types, not plain strings or numbers.
- **Source:** ch. 6 p. 104

### DDD-T14: Validate inputs inside value object construction
Put parsing and validation of a concept inside its value object, so callers cannot skip it.

- **Why:** One validation point means every place that accepts the concept enforces the same rule.
- **When:** Several places accept the same kind of input, such as email addresses.
- **Check:** Validation for a concept lives in one value class, and callers do not repeat it.
- **Source:** ch. 6 p. 106

### DDD-T15: Make value objects immutable with value equality
Make value objects read-only and identity-free, return new instances for changes, and compare them by their fields.

- **Why:** Immutable values cannot change under a caller, and field equality matches how the business compares them.
- **When:** A value is compared, stored in a collection or changed by an operation.
- **Check:** Value classes have no setters or identity field, and their equality and hash code use every field.
- **Source:** ch. 6 p. 104

### DDD-T16: Keep entity identifiers unchanged
Give each entity a unique identifier and never reassign it during its lifecycle.

- **Why:** Identity tells two entities with equal attributes apart, so a changed ID breaks that link.
- **When:** Designing an entity's identifier or writing code that could reassign it.
- **Not when:** Rare exceptions exist, which the book does not detail.
- **Check:** Identifier properties have no setter, and no update path assigns a new identifier.
- **Source:** ch. 6 p. 109

### DDD-T17: Make the aggregate root the entry point
Expose one root entity as the public interface of an aggregate, and create child entities only inside it.

- **Why:** A single entry point lets the root check every change to its internal hierarchy.
- **When:** Adding an entity type to a model, or defining an aggregate's public members.
- **Check:** Callers reach child entities only through root methods, and no accessor returns a child.
- **Source:** ch. 6, 11 p. 110

### DDD-T18: Change aggregates through named commands
Expose each state change of an aggregate as a named business action or command object.

- **Why:** Named commands keep every change behind validation and make the business intent visible.
- **When:** Defining the public interface of an aggregate or writing an application service method.
- **Check:** Aggregate public members are business actions, and services call one command before saving.
- **Source:** ch. 6 p. 111

### DDD-T19: Detect conflicting saves with version numbers
Store a version on each aggregate and reject an update whose expected version no longer matches.

- **Why:** Versions stop a second writer from silently overwriting changes it never read.
- **When:** Two processes may update the same aggregate concurrently.
- **Check:** Updates include the version read earlier, and a stale update fails with a conflict error.
- **Source:** ch. 5, 6 p. 94

### DDD-T20: Commit one aggregate per transaction
Save changes to a single aggregate instance in each transaction, and revisit boundaries when an operation seems to need two.

- **Why:** One aggregate per transaction keeps the consistency boundary clear for every save.
- **When:** An operation would change several aggregates in one transaction.
- **Check:** Each repository save or transaction writes to a single aggregate's data.
- **Source:** ch. 6, 13 p. 113

### DDD-T21: Keep aggregates to the data their invariants need
Hold only the fields that the aggregate's commands need for invariants, and reference the rest by identifier.

- **Why:** Smaller aggregates lower the cost and the complexity of each strongly consistent transaction.
- **When:** Deciding which related data should become part of an aggregate.
- **Check:** Each aggregate enforces an invariant, and other data appears only as identifiers.
- **Source:** ch. 6, 11, 13, Appendix A p. 116

### DDD-T22: Keep strongly consistent data inside one aggregate
Test whether logic would give wrong results under eventual consistency, and if so, keep that data in the same aggregate.

- **Why:** Objects that must change together need one transaction, which only one aggregate guarantees.
- **When:** Deciding whether a piece of data belongs inside an aggregate, or whether to relax consistency for scale.
- **Not when:** Corrupted data would be a business showstopper, so relaxing consistency is not an option.
- **Check:** Data feeding aggregate decisions sits in that aggregate, and each relaxed choice has a risk assessment.
- **Source:** ch. 5, 6, 13 p. 98

### DDD-T23: Put multi-source calculations in domain services
Place logic spanning several aggregates or sources in a stateless domain service that saves at most one aggregate per transaction.

- **Why:** A stateless service hosts rules that span sources without giving any one aggregate extra data.
- **When:** A calculation needs data from several sources, such as a policy and a shift schedule.
- **Check:** Domain service classes keep no mutable state, sit in the domain layer, and save at most one aggregate.
- **Source:** ch. 6 p. 118

### DDD-T24: Derive dependent fields in one method
Compute each field that depends on other fields inside one method, and never assign it independently.

- **Why:** Separate assignments let dependent values fall out of step with their sources.
- **When:** A class has fields whose values are functions of other fields.
- **Check:** Dependent fields are assigned only inside a method that computes them from source fields.
- **Source:** ch. 6 p. 121

### DDD-T25: Name domain events in the past tense
Name each domain event in the past tense.

- **Why:** A past-tense name records a business event that already happened, not a command to act.
- **When:** Other components must react to a change inside an aggregate.
- **Check:** Event class names end in past-tense verbs, not command-style names such as escalate.
- **Source:** ch. 6 p. 117

### DDD-T26: Use event sourcing only where history matters
Store an aggregate as events only when the business needs full history, audit, or very complex logic that publishes events.

- **Why:** Event sourcing needs training and ongoing effort, so it pays off only for history or very complex logic.
- **When:** The business needs audits, money tracking or deep behavior analysis, or logic outgrows state-based patterns.
- **Check:** Aggregate storage appends event rows, and the project plan budgets training before adoption.
- **Source:** ch. 7, Appendix A p. 138

### DDD-T27: Rebuild aggregate state by replaying events
Load an event-sourced aggregate by applying its stored events in order, then run the command and commit new events.

- **Why:** Every state change is recorded as an event, so replaying stored events rebuilds the aggregate's state.
- **When:** Loading an event-sourced aggregate before executing a command on it.
- **Check:** The constructor loops over stored events, and the operation appends against the original version.
- **Source:** ch. 7 p. 134

### DDD-T28: Append events only and pass the expected version
Allow only appends and reads on the event store, and on a stale expected version inspect the newer events before rejecting.

- **Why:** Stored events are the history, so editing them destroys the record the design depends on.
- **When:** Designing the event store interface, or appending events that other writers may also update.
- **Not when:** An exceptional case such as data migration needs a controlled change.
- **Check:** The store exposes fetch and append only, and stale appends are checked against newer events.
- **Source:** ch. 7 p. 133

### DDD-T29: Build several projections from one event stream
Create separate projections from the same events, each shaped for one need, and answer state queries from a projection rather than the event store.

- **Why:** One stream can answer new questions later without changing the producers.
- **When:** A feature needs a view of an aggregate that its current state does not provide.
- **Check:** Projection apply methods ignore unrelated events, and each projection keeps its own state.
- **Source:** ch. 7, 8 p. 130

### DDD-T30: Add snapshots only after measured slowness
Introduce snapshot caching only when a benchmark at realistic event counts shows that replay is slow.

- **Why:** Snapshots add complexity, and replay is often fast enough at realistic event counts.
- **When:** Rebuilding an aggregate from its events becomes slow at realistic event counts.
- **Not when:** Aggregates stay far below the event counts where replay is noticeably slow.
- **Check:** Benchmark results exist, and the load path reads the snapshot version and queries newer events.
- **Source:** ch. 7 p. 139

### DDD-T31: Encrypt personal event data for erasure
Encrypt sensitive event fields with a per-aggregate key, and delete the key to make the data unreadable.

- **Why:** Stored events cannot be edited, so deleting the key is how personal data becomes erasable.
- **When:** Personal data inside events must be erasable, for example under GDPR.
- **Check:** Sensitive fields are stored encrypted, with keys held in a separate store per aggregate ID.
- **Source:** ch. 7 p. 140

### DDD-T32: Keep audit history in persisted events
Use persisted domain events as the audit log, not text logs or manually written audit rows.

- **Why:** Separately written records can diverge from the change, and trigger history misses the reason.
- **When:** An audit trail must reflect operations that also change the database.
- **Check:** No audit row is inserted by hand, and the audit trail comes from persisted events.
- **Source:** ch. 7, 13 p. 140

### DDD-T33: Version event schemas instead of rewriting history
Handle a changed event shape through schema versions, and never rewrite stored events to fit a new schema.

- **Why:** Rewriting stored events would corrupt the history the design depends on.
- **When:** An event's fields must change after events of that type were already stored.
- **Not when:** A controlled event-store migration, which DDD-T28 allows.
- **Check:** Stored event records are never updated, and new versions appear beside old ones.
- **Source:** ch. 7 p. 138

### DDD-T34: Keep business rules out of UI and storage
Keep business rules out of controllers, views and database scripts.

- **Why:** Each concern gets its own boundary, so business rules have one home.
- **When:** Business rules start appearing in controllers, views or storage scripts.
- **Check:** Controllers, views and database scripts contain no business rule conditions.
- **Source:** ch. 8 p. 143

### DDD-T35: Move transaction orchestration into a service layer
Move transaction handling into one in-process service layer that every entry point calls.

- **Why:** Controllers that coordinate transactions repeat the same orchestration for every interface.
- **When:** A controller coordinates transactions and domain calls, or two interfaces expose one operation.
- **Not when:** The business logic is already a transaction script, which can serve as the service layer.
- **Check:** Controller and message handler code only translate input and output, while service methods own the transaction.
- **Source:** ch. 8 p. 144

### DDD-T36: Define ports for infrastructure needs
Define interfaces in business logic for each infrastructure need, and implement them in the outer layer.

- **Why:** Dependencies then point inward, keeping business logic free of frameworks and infrastructure.
- **When:** Business logic needs messaging, storage or an external service.
- **Check:** Domain and application code import only port interfaces, and one composition root wires adapters.
- **Source:** ch. 8 p. 153

### DDD-T37: Separate the command model from read models
Use one command model for state changes and separate read models for queries, and fill each read model from the write path.

- **Why:** Each model can then be shaped for its job, and read models can be rebuilt at will.
- **When:** The same data must be shown or stored in several shapes for different uses.
- **Check:** Only the command path saves to the command model, and read models receive writes only from projection code.
- **Source:** ch. 5, 8 p. 92

### DDD-T38: Project read models with checkpoints
Update a read model from changes after a stored checkpoint, and rebuild it by resetting the checkpoint to zero.

- **Why:** A monotonic checkpoint lets a projection resume without skipping or repeating changes.
- **When:** Read models must follow changes in the command model's database.
- **Check:** The projection query orders by a checkpoint column set on every insert and update, and it saves the last value.
- **Source:** ch. 8 p. 157

### DDD-T39: Build synchronous projection before asynchronous
Implement a synchronous projection first, and add an asynchronous one only on top of it.

- **Why:** The synchronous version is simpler, and asynchronous projections bring disorder.
- **When:** Choosing how a new CQRS system updates its read models.
- **Check:** A synchronous projector exists before any message-bus projector is added.
- **Source:** ch. 8 p. 158

### DDD-T40: Translate foreign models at the context boundary
Map upstream types into your own context's types inside one translation layer, so foreign types never reach the domain.

- **Why:** Foreign concepts stay outside the domain, so the consumer's model stays simple.
- **When:** The downstream cannot conform, or the upstream model is messy or changes often.
- **Not when:** The supplier's model suits the consumer, so conforming is simpler.
- **Check:** Upstream types are mapped inside one translation module, and domain modules do not import them.
- **Source:** ch. 4, 9, 13 p. 79

### DDD-T41: Publish a consumer-oriented language
Expose a consumer-facing published language, separate from the internal model, and translate internal events before publishing them.

- **Why:** Consumers depend on the contract, so internal changes should not ripple outward.
- **When:** Designing a public API for external or numerous consumers.
- **Not when:** The modified internal model cannot be translated into the published language.
- **Check:** API names and payloads differ from internal domain classes, and each version has its own schema.
- **Source:** ch. 4, 9 p. 81

### DDD-T42: Share a kernel only when duplication costs more
Share a small kernel of contracts and transfer types only when duplicating the model costs more than coordinating it.

- **Why:** A shared kernel couples the contexts strongly, so it must stay minimal and tested by every consumer.
- **When:** Two contexts must share a model, and duplicating it costs more than coordinating.
- **Not when:** The coupling a shared kernel creates is unacceptable to either team.
- **Check:** The shared module holds only contracts, and CI runs every consumer's tests.
- **Source:** ch. 4 p. 77

### DDD-T43: Choose the integration pattern by team collaboration
Pick each integration pattern from how closely two teams collaborate, coordinating ad hoc when they communicate often, and record it on the context map.

- **Why:** Patterns trade coordination effort against coupling, and collaboration decides which trade is affordable.
- **When:** Planning an integration between two bounded contexts.
- **Not when:** The teams are geographically distributed and find synchronizing difficult.
- **Check:** The context map names one pattern per relationship, from DDD-T40 to DDD-T44, and marks both sides.
- **Source:** ch. 4 p. 75

### DDD-T44: Separate ways for non-core features
Duplicate non-core functionality when collaboration costs more than duplication, but never duplicate core logic.

- **Why:** Constant integration friction can cost more than a second non-core implementation.
- **When:** Communication problems make collaboration costlier, or models differ too much to conform or translate cheaply.
- **Not when:** The functionality belongs to a core subdomain.
- **Check:** Two contexts implement the same non-core feature with no shared dependency.
- **Source:** ch. 4, 11 p. 82

### DDD-T45: Plot every integration on a context map
Draw one context map from project start, under version control, with each team maintaining its own entries.

- **Why:** A map exposes organizational problems, such as one team causing most separate-ways links.
- **When:** The system has several contexts that integrate, or a context is added or changed.
- **Check:** A versioned context map file lists every integration, its pattern and its owning team.
- **Source:** ch. 4 p. 83

### DDD-T46: Save events in the outbox with the aggregate
Commit the aggregate's state and its new events in one transaction, and publish the events from a relay afterwards.

- **Why:** A crash between save and publish would lose events, so both must commit together.
- **When:** Domain events must reach subscribers reliably after a state change.
- **Check:** One transaction writes the state-based aggregate record and the unpublished event records.
- **Source:** ch. 9 p. 171

### DDD-T47: Mark published outbox events after publishing
Mark or delete each outbox event only after the relay has published it successfully.

- **Why:** Marking after success prevents losing events the relay has not sent.
- **When:** A relay forwards committed events from the outbox to the message bus.
- **Check:** Relay code updates the published flag or deletes the row only after a successful publish call.
- **Source:** ch. 9 p. 171

### DDD-T48: Make subscribers tolerate duplicate messages
Design every subscriber to skip or safely reapply events it has already processed, and to handle disorder.

- **Why:** The relay can publish an event again when it fails to mark it, so duplicates are normal.
- **When:** Subscribers consume messages from an outbox relay or an asynchronous channel.
- **Check:** Handlers store processed event IDs or sequence numbers, check them before applying, and accept out-of-order messages.
- **Source:** ch. 9, 15 p. 173

### DDD-T49: Give saga steps compensating actions
Model a multi-aggregate process as a saga, and pair each state-changing step with a compensating command.

- **Why:** A finished step cannot be undone directly, so a paired command reverses its effect.
- **When:** A business process spans several transactions and a later step may fail.
- **Not when:** The next step depends on earlier results, so DDD-T51 applies.
- **Check:** Each state-changing saga step has a paired compensating command in the saga code.
- **Source:** ch. 9, 15 p. 173

### DDD-T50: Persist saga state as events
Store the events a saga receives and the commands it issues, and treat the saga's components as eventually consistent.

- **Why:** A recorded command history lets the saga compensate after failures, and it avoids assuming atomic reads.
- **When:** A saga must track what it has commanded, or reads depend on several participants at once.
- **Check:** Saga state changes append command-issued events, and reads do not assume atomicity across components.
- **Source:** ch. 9 p. 176

### DDD-T51: Use a process manager for branching processes
Implement a business process with state-dependent branches as a process manager, created explicitly with its own identifier.

- **Why:** A process manager stores the choices and progress that a plain saga would lose.
- **When:** The next step depends on earlier results, such as choosing alternative routes.
- **Check:** The process class has an identifier, persists its state and branches on earlier outcomes.
- **Source:** ch. 9 p. 177

### DDD-T52: Notify, then query for sensitive or fresh data
Send a short notification with identifiers, then have the consumer query the producer for sensitive, stale or latest data.

- **Why:** Notifications can be stale or race ahead of the write, so the producer is the reliable source.
- **When:** Notification data is sensitive, or the consumer must read the latest write.
- **Check:** The handler authorizes and calls the producer's detail endpoint before using the data.
- **Source:** ch. 15 p. 262

### DDD-T53: Size a bounded context by its model
Set a context's boundary from one consistent ubiquitous language, starting core contexts wide and including the subdomains they interact with most.

- **Why:** A model's language is the natural limit of a context, not an assumed service count.
- **When:** Deciding how wide a bounded context boundary should be.
- **Not when:** The context covers generic or supporting subdomains, which are more formulaic and less volatile.
- **Check:** Recurring cross-context changes signal a wrong boundary, and no context maps one-to-one to an aggregate.
- **Source:** ch. 10, Appendix A p. 186

### DDD-T54: Choose the logic pattern by subdomain questions
Choose each subdomain's pattern by asking in order: does money or audit need history, how complex are the rules, and does the vocabulary describe processes?

- **Why:** Money and audit needs decide event sourcing first, and rule complexity decides the rest.
- **When:** Selecting transaction script, active record, domain model or event sourcing for a subdomain.
- **Check:** Design notes record the answers, and script or record modules with growing invariant checks move to a richer pattern.
- **Source:** ch. 8, 10, Appendix A p. 160

### DDD-T55: Unit-test domain models through aggregates
Test a domain model mostly with unit tests that construct aggregates and value objects directly.

- **Why:** The testing pyramid puts most tests on domain rules, which unit tests check without infrastructure.
- **When:** Writing tests for code built with a domain model pattern.
- **Check:** Most tests construct aggregates or value objects directly, without database or framework setup.
- **Source:** ch. 10 p. 191

### DDD-T56: Use advanced patterns only when required
Treat design heuristics as guides, and adopt the domain model, event sourcing or CQRS only for a stated business need.

- **Why:** Advanced patterns add cost and complexity, so each must justify itself with a stated requirement.
- **When:** Choosing between simple designs and advanced patterns, or applying one favorite pattern everywhere.
- **Check:** Design notes justify each advanced pattern with a specific requirement and record heuristics set aside.
- **Source:** ch. 10 p. 185

### DDD-T57: Refactor legacy toward aggregates in small steps
Move legacy scripts and records into state-based aggregates, adding value objects first and event sourcing last.

- **Why:** Small steps keep the system working, and each step gives the next one a stable base.
- **When:** Modernizing legacy code toward aggregates, once DDD-T56 justifies a domain model.
- **Check:** Immutable value types appear in small commits before aggregates are restructured.
- **Source:** ch. 13 p. 230

### DDD-T58: Replace legacy through a strangler facade
Build new requirements in a new context, route requests through a facade, and remove the facade once the legacy context is retired.

- **Why:** The facade lets old and new code coexist, so each function moves without a full rewrite.
- **When:** A legacy context is replaced step by step during a migration.
- **Not when:** The legacy context is not planned for retirement.
- **Check:** Routing code decides per request, legacy commits are hotfixes only, and both contexts may share a database during migration when splitting data needs distributed transactions.
- **Source:** ch. 13 p. 234

### DDD-T59: Recheck boundaries as growth adds complexity
Review subdomain, context and aggregate boundaries during periodic architecture reviews and after many features ship.

- **Why:** Boundaries drawn for an early system stop fitting once features widen components.
- **When:** A periodic architecture review runs, or a component's functionality keeps expanding.
- **Check:** Review notes record a boundary check for each growing component, and feature PRs include a design note.
- **Source:** ch. 11 p. 206

### DDD-T60: Keep microservices deep and their interfaces small
Give each service a small public interface that hides complex logic, and stop splitting once services turn shallow.

- **Why:** A shallow service adds integration cost without hiding complexity.
- **When:** Deciding how much functionality a service hides, or reviewing a service that mostly forwards calls.
- **Check:** The public interface lists few operations, and no boundary needs data from most other services.
- **Source:** ch. 14, Appendix A p. 244

### DDD-T63: Group workshop events into aggregates and contexts
Group commands, events and policies into aggregates, then group aggregates linked by events into candidate contexts.

- **Why:** Linked commands and events show which data must stay consistent and which parts belong together.
- **When:** The workshop timeline is complete and boundaries are needed.
- **Check:** Each automatic reaction is a policy that dispatches its command, and aggregates linked by events form one candidate context, as DDD-T53 describes.
- **Source:** ch. 12 p. 217

### DDD-T64: Record analytics as append-only facts
Record business activities as append-only fact rows, and never update or delete them.

- **Why:** Appended facts keep history intact, so a changed measurement becomes a new record.
- **When:** Building an analytical model for reports, or a measurement's state changes over time.
- **Check:** No update or delete targets fact tables, and facts model business activities rather than entities.
- **Source:** ch. 16 p. 276

### DDD-T65: Validate records against a schema on ingestion
Validate records against a declared schema and quality checks before storing them in the data lake.

- **Why:** Unvalidated ingestion fills the lake with records that later analyses cannot trust.
- **When:** Data lake ingestion accepts records that several analytical models may need.
- **Check:** The ingestion job validates records against a declared schema before storing them.
- **Source:** ch. 16 p. 284

### DDD-T66: Publish analytical outputs with schemas and SLAs
Serve each analytical output through a defined port with a versioned schema, and feed analytics from outputs, not operational tables.

- **Why:** Consumers depend on an output only when its shape and availability are stated and watched.
- **When:** Other teams consume an analytical output from a bounded context.
- **Check:** Each output has a versioned schema file, and monitoring tracks an SLA for it.
- **Source:** ch. 16 p. 282

### DDD-T67: Make retried updates set target values
Send the target value in each update, not an increment, so a retry leaves the result unchanged.

- **Why:** A retried increment changes the stored value again, so each repeat double-counts.
- **When:** A caller may retry an update after an unclear failure.
- **Check:** Update statements set an explicit value rather than adding to the stored value.
- **Source:** ch. 5 p. 94

### DDD-T68: Split monolithic contexts into vertical modules
Divide a monolithic bounded context into one module per business subdomain, with explicit interfaces between them.

- **Why:** Horizontal layers spread one subdomain's rules across the whole context, which tangles the codebase.
- **When:** A bounded context spans several subdomains and risks becoming a tangled codebase.
- **Check:** Each subdomain has its own module, and other modules reach it through its interface.
- **Source:** ch. 8 p. 160

### DDD-T69: Weigh distributed complexity before splitting a monolith
Weigh the integration calls and distributed complexity that each new service adds before splitting a monolith.

- **Why:** Distributed services bring integration work that a single codebase never carries.
- **When:** Deciding to split a monolithic codebase into services.
- **Check:** The split proposal lists the new integration calls each service adds.
- **Source:** ch. 14 p. 243

### DDD-T70: Keep each service's database encapsulated
Keep each service's database private, and let other services reach its data only through the service's public interface.

- **Why:** Services reading its tables bypass the interface, so its storage cannot change freely.
- **When:** Designing data access between services.
- **Not when:** A strangler migration, where DDD-T58 allows a temporary shared database.
- **Check:** No other service connects to the service's database or tables.
- **Source:** ch. 14 p. 245

### DDD-T71: Keep one entity's rules in one module
Keep the business rules for one entity inside one bounded context, implemented once in one module.

- **Why:** Rules spread across services, procedures or teams drift apart.
- **When:** Splitting work on one shared entity across teams or stored procedures.
- **Check:** Each rule for one entity is implemented once, in one module.
- **Source:** Appendix A p. 304

### DDD-T72: Lock before processing a single-consumer notification
When only one consumer may process a notification, lock the record before processing it.

- **Why:** Locking the record lets one consumer take the notification while the others leave it alone.
- **When:** Several consumers receive a notification, but only one should process it.
- **Check:** The consumer takes a lock on the record before processing the notification.
- **Source:** ch. 15 p. 263
