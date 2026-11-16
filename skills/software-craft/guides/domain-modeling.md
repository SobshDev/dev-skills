# Domain modeling (domain-driven design)

This guide covers how to model a business in code: classifying subdomains, sharing one language with domain experts, drawing bounded contexts and their integrations, and building entities, value objects, aggregates, events, event-sourced stores, read models, sagas and the outbox. The single most important idea is to match design effort to business value and rule complexity: model core subdomains carefully, keep everything else simple, and adopt an advanced pattern only when a stated requirement needs it.

**Read this when:** naming classes for a business area, adding or changing a business rule, deciding what belongs inside an aggregate, integrating with another team's service or model, publishing domain events, choosing between a transaction script, active record, domain model or event sourcing, adding a read model, coordinating a process that spans several aggregates, or reviewing a diff that touches any of these.

**Entry IDs** such as `WELC-T12` point to `../books/<book>/techniques.md` (T) or `principles.md` (P);
the prefix table is in [SKILL.md](../SKILL.md).

## Contents

- [Rules: subdomains and language](#rules-subdomains-and-language)
- [Rules: bounded contexts and integration](#rules-bounded-contexts-and-integration)
- [Rules: entities, value objects and aggregates](#rules-entities-value-objects-and-aggregates)
- [Rules: choosing the business-logic pattern](#rules-choosing-the-business-logic-pattern)
- [Rules: event sourcing](#rules-event-sourcing)
- [Rules: CQRS and projections](#rules-cqrs-and-projections)
- [Rules: events, outbox and long-running processes](#rules-events-outbox-and-long-running-processes)
- [Playbooks](#playbooks)
- [Where the books disagree](#where-the-books-disagree)
- [Review checklist](#review-checklist)
- [More entries in this area](#more-entries-in-this-area)

Neighbouring topics live elsewhere. Layering, ports and adapters, service layers and service boundaries are in [architecture](architecture.md). Testing domain models is in [testing](testing.md). Moving legacy code toward aggregates or behind a strangler facade is in [legacy-code](legacy-code.md). Change logs, change data capture and derived stores are in [data-systems](data-systems.md). The State pattern for entities whose behavior depends on their state is in [design-patterns](design-patterns.md).

## Core rules

The rules are grouped by sub-topic, from strategic design down to messaging.

## Rules: subdomains and language

### 1. Classify each subdomain before designing it

Describe the business as the service it offers clients, then split it into subdomains and label each one core, supporting or generic. Core subdomains give the business its competitive edge, so they earn the most design effort, while the others earn less. A useful test is whether anyone would pay for the part on its own, and a painful legacy area that no product could replace is probably core. [DDD-P1, DDD-T01, DDD-T07, DDD-T08]

- **Do:** In an organization you do not know well, start from departments as a first draft, then refine by client service. Draw each subdomain around use cases that share actors and closely related data. Record each subdomain's type and the business reason in the design notes. Set aside areas that software does not touch.
- **Not when:** The business has not yet described its strategy, so get that description before classifying. Stop splitting generic and supporting areas once a finer split would change no design decision, but keep distilling core subdomains.
- **Check:** Design notes name the client-facing service, list the subdomains behind it, and give each one a type and a reason.

### 2. Recheck subdomain types when the business changes

A subdomain's type is not permanent. A core area can become generic when a product appears or the strategy shifts, and an old label then misleads later design choices. [DDD-T02, DDD-T59]

- **Do:** Revisit types when strategy, competitors or products change, or when a product replaces custom code. Check subdomain, context and aggregate boundaries during periodic architecture reviews and after many features ship.
- **Check:** Each subdomain has a review date, each type change has a dated reason, and review notes record a boundary check for each growing component.

### 3. Build core in-house, buy generic, keep supporting cheap

Spend effort in proportion to business value. Core logic is the company's advantage, so build it in-house with the strongest engineers and guarded tests, and keep generic or supporting code out of it. Generic problems are already solved, and maintained products receive security patches. Supporting logic changes rarely and adds little value, so elaborate design there does not pay. [DDD-T03, DDD-T04, DDD-T05, DDD-T06]

- **Do:** Extract generic and supporting parts out of core modules. Staff core subdomains with experienced engineers and protect their frequent changes with automated tests. Use a maintained library or product for generic needs such as authentication, and keep it updated. Build supporting subdomains with framework scaffolding and simple scripts or records, and only in-house when no ready product exists.
- **Not when:** Supporting and generic subdomains can be outsourced or used to onboard new people, so in-house ownership applies to core only. Skip the ready-made product when integrating it costs more than building the feature. If a supporting subdomain seems to need advanced modeling, first check whether that complexity is accidental or whether the area hides a competitive edge.
- **Check:** Core modules hold no generic or supporting functions and have a named in-house owner. Dependency manifests pin maintained versions with regular upgrades. Supporting modules have no extra abstraction layers.

### 4. Name code with the domain experts' terms

Developers and domain experts must share one vocabulary, because misunderstandings between them reach production. Use the terms in classes, methods, tests and tickets, in supporting and generic areas too, and in daily conversation, not only in documents. [DDD-P2, DDD-T09, PP-T26, CA-T79]

- **Do:** Take names for aggregates, value objects, commands, events and tests from the glossary. Name domain types with business terms rather than technical suffixes such as Repository.
- **Not when:** The gateway interfaces that use cases depend on may carry technical names (CA-T79).
- **Check:** Class and test names match the glossary terms in the context's requirements. Business rules in documentation name the domain expert they came from.

### 5. Give each term one meaning and keep the glossary current

A word with two meanings produces wrong rules. Split an overloaded term such as "policy" into explicit concepts instead of prefixing it differently in each area. Keep a shared glossary, because it speeds onboarding and keeps the language aligned with the model as it evolves. [DDD-T10, DDD-T11]

- **Do:** Split a class that carries two unrelated concepts. Treat one concept that gets a different name prefix in several areas as a sign of a missing context boundary. Update the glossary in the same commit that renames or redefines a domain term.
- **Check:** No class carries two unrelated concepts, and a commit that changes a term's meaning also changes the glossary file.

## Rules: bounded contexts and integration

### 6. Draw each bounded context around one consistent model

A bounded context is the scope in which every term has one meaning and one model. Size it by the model's language, business needs and consistency requirements, not by a target number of services, and avoid a single model that tries to serve every department. [DDD-P3, DDD-T53, DDD-T63]

- **Do:** Split a context where its terms conflict. Start core contexts wide while their logic is unclear, including the subdomains they interact with most, and narrow them once the logic stabilizes. Once a modeling workshop's timeline of commands, events and policies is complete, group them into aggregates, then group aggregates linked by events into candidate contexts.
- **Not when:** Wide starting boundaries are advice for core contexts. Generic and supporting contexts are more formulaic and less volatile. Do not force a one-to-one mapping from subdomains to contexts when one problem needs different models.
- **Check:** Each context defines its terms once, and references to another context's terms pass through an explicit mapping. No context maps one-to-one to a single aggregate. Recurring changes that cross two contexts signal a wrong boundary.

### 7. Name an integration pattern for every context pair

Every touchpoint between contexts needs a documented contract and a named integration pattern. Choose the pattern from how closely the two teams collaborate, because each pattern trades coordination effort against coupling. Record all of it on one versioned context map, which also exposes organizational problems such as one team causing most separate-ways links. [DDD-P4, DDD-T43, DDD-T45]

- **Do:** Coordinate ad hoc when the teams communicate often. Otherwise pick from conformist or translation, published language, shared kernel and separate ways (rules 8 to 10). Keep the map under version control from the project's start, and let each team maintain its own entries.
- **Not when:** Teams that are geographically distributed and find synchronizing difficult should not rely on close ad hoc coordination.
- **Check:** A versioned context map lists each integration, its pattern, both sides and the owning team, and each touchpoint has a documented contract.

### 8. Translate foreign models at the boundary, or conform

Keep upstream concepts out of your domain by mapping upstream types into your own types inside one translation layer. The consumer's model then stays simple even when the upstream model is messy or changes often. [DDD-T40]

- **Do:** Put all mapping of upstream types in one module, and have domain modules use only your context's types.
- **Not when:** The supplier's model already suits the consumer, so conforming to it is simpler.
- **Check:** Domain modules import no upstream types, and the translation module is the only place that does.

### 9. Publish a consumer-oriented language for public interfaces

When many or external consumers depend on a context, expose a published language that is separate from the internal model, and translate internal events before publishing them. Consumers depend on the contract, so internal changes should not ripple out to them. Old and new versions must read each other's data, because they run side by side during upgrades, and old requests must keep working, because clients you do not control may not upgrade. [DDD-T41, DDIA-P5]

- **Do:** Give API names and payloads their own shapes and a schema per version. Test old readers against new data and new readers against old data.
- **Not when:** The pattern does not hold once a changed internal model can no longer be translated into the published language.
- **Check:** API names and payloads differ from internal domain classes, each version has its own schema, and compatibility tests decode old fixtures with new code and the reverse.

### 10. Share a kernel or go separate ways only on cost

Share a small kernel of contracts and transfer types only when duplicating the model would cost more than coordinating it, because a shared kernel couples the contexts strongly. When collaboration costs more than duplication, two contexts may each implement the same non-core feature. Core logic is never duplicated, even when collaboration fails. [DDD-T42, DDD-T44, DDD-P4]

- **Do:** Keep a shared kernel minimal and run every consumer's tests against it in CI. Choose separate ways when communication problems make collaboration expensive or the models differ too much to conform or translate cheaply.
- **Not when:** Skip a shared kernel when either team finds its coupling unacceptable. Separate ways does not apply to functionality in a core subdomain.
- **Check:** The shared module holds only contracts, and CI runs every consumer's tests. Any feature implemented twice is non-core and has no shared dependency.

## Rules: entities, value objects and aggregates

### 11. Put business rules and invariants inside domain objects

Give domain entities methods that perform business actions and enforce the rules, rather than plain fields that callers set. Rules kept in the objects stay enforced for every caller and cannot drift apart. Central business concepts that would exist without software are the natural candidates. [DDD-T12, CA-T55]

- **Do:** Expose operations such as "calculate interest" or "escalate" and keep invariant fields private.
- **Not when:** Simple CRUD logic can stay in transaction scripts or active records, as rule 20 explains [DDD-P6, DDD-T06].
- **Check:** Domain classes expose business-action methods, and callers cannot assign their invariant fields.

### 12. Replace primitives that carry rules with value objects

Represent names, money, identifiers, phone numbers and similar concepts with named domain types, because a bare string or number cannot carry their rules. Put parsing and validation inside the value object's construction so that no caller can skip it and every place that accepts the concept enforces the same rule. [DDD-T13, DDD-T14, FPS-T26]

- **Do:** Accept named domain types in domain method parameters and properties. Build values from unchecked input through one constructor or factory function that rejects invalid input. In a functional codebase, that function returns an Either, and the raw constructor is not called directly.
- **Not when:** A supporting subdomain with simple logic can keep primitives (DDD-T06). See the tension on primitives below for when a plain value is enough for now.
- **Check:** Validation for a concept lives in one value class and callers do not repeat it. Domain signatures use domain types rather than plain strings or numbers.

### 13. Make value objects immutable and compare them by value

A value object has no identity. Make it read-only, return a new instance from every operation, and define equality over all of its fields, with a hash code that agrees. An immutable value cannot change under another holder, so sharing it is safe, and field equality matches how the business compares values. [DDD-T15, REF-T84, TDD-T27, TDD-T28, TDD-T29, FPS-P2]

- **Do:** Assign fields only in the constructor and add no setters or identity field. Compare every field in equals, and override the hash code together with equals.
- **Not when:** If callers deliberately update one shared object in place, it is a reference object, not a value object (REF-T84). If allocating new values proves slow with realistic data, measure before optimizing. Copying a large state on every call is costly, and efficient persistent structures help there (TDD-T27, FPS-P2). TDD defers the hash code until the class is used as a map key or set member (TDD-T29). See the tension below.
- **Check:** Value classes have no setters or identity field, and equality and hash code use every field.

```java
final class Money {
  private final long cents; private final Currency currency;
  Money(long cents, Currency currency) {
    if (currency == null) throw new IllegalArgumentException("currency");
    this.cents = cents; this.currency = currency;
  }
  Money plus(Money o) { requireSame(o); return new Money(cents + o.cents, currency); }
  @Override public boolean equals(Object x) {
    return x instanceof Money m && m.cents == cents && m.currency.equals(currency);
  }
  @Override public int hashCode() { return Objects.hash(cents, currency); }
}
```

### 14. Keep entity identifiers unchanged

Give each entity a unique identifier and do not reassign it during its lifecycle. Identity is what distinguishes two entities with equal attributes, so changing it breaks that link. [DDD-T16]

- **Do:** Make identifier properties read-only and remove any update path that assigns a new identifier.
- **Not when:** The book mentions rare exceptions but does not describe them.
- **Check:** Identifier properties have no setter, and no update path writes a new identifier.

### 15. Change an aggregate only through its root's named commands

An aggregate is the consistency boundary, and only its own methods change its state. Expose one root entity as the aggregate's public interface, create child entities only inside it, and express each state change as a named business action or command object. A single entry point lets the root check every change, and named commands keep changes behind validation and show the business intent. [DDD-P5, DDD-T17, DDD-T18]

- **Do:** Have application services load the aggregate, call one command, and save. Do not return child entities from accessors.
- **Check:** The aggregate's public members are business actions, no external setters exist, and callers reach children only through root methods.

### 16. Keep only invariant-bearing data inside an aggregate

Hold only the fields that the aggregate's commands need to enforce its invariants, and reference everything else by identifier. Smaller aggregates make each strongly consistent transaction cheaper and simpler. The deciding test is whether the logic would give wrong results under eventual consistency: if so, that data belongs in the same aggregate. [DDD-T21, DDD-T22, DDD-P5]

- **Do:** For each candidate field, ask whether a command's decision depends on it being current. Keep it inside if so, and replace it with an identifier if not. Write down a risk assessment for every place where you relax consistency for scale.
- **Not when:** Where corrupted data would be a business showstopper, relaxing consistency is not an option.
- **Check:** Each aggregate enforces an invariant, data that feeds its decisions sits inside it, and other aggregates appear only as identifiers.

### 17. Commit one aggregate per transaction, with a version check

Save a single aggregate instance in each transaction, so the consistency boundary stays clear for every save. When an operation seems to need two aggregates in one transaction, revisit the boundaries rather than widening the transaction. Store a version on each aggregate and reject an update whose expected version no longer matches, so a second writer cannot silently overwrite changes it never read. Versions or logical counters, not wall-clock timestamps, decide the order of concurrent writes. [DDD-T20, DDD-T19, DDD-P5, DDIA-P4]

- **Do:** Include the version read earlier in every update and fail with a conflict error when it is stale. Use a saga (rule 32) for a process that really spans several aggregates.
- **Not when:** Do not use a saga to split operations that need strong consistency. Those belong in one aggregate (rule 16). Last-write-wins by timestamp fits only where losing concurrent writes is acceptable (DDIA-P4).
- **Check:** Each command handler, repository save or transaction writes a single aggregate's data, and a stale update fails with a conflict.

### 18. Put calculations that span aggregates in stateless domain services

When a calculation needs data from several aggregates or sources, such as a policy and a shift schedule, put it in a stateless domain service. The service hosts rules that span sources without loading any one aggregate with extra data. [DDD-T23]

- **Do:** Place the service in the domain layer, keep no mutable state in it, and have it save at most one aggregate per transaction.
- **Check:** Domain service classes keep no mutable fields, live in the domain layer, and save at most one aggregate.

### 19. Compute dependent fields from their sources in one place

A field whose value is a function of other fields should be computed inside one method and never assigned on its own, because separate assignments let it fall out of step with its sources. Where possible, replace a stored derived value with a query that computes it, so it cannot go stale. [DDD-T24, REF-T30, REF-T31]

- **Do:** Assign each dependent field only inside the method that computes it from its source fields, or derive it on read.
- **Not when:** When the source data is immutable, the derived result can be immutable and stored too (REF-T31).
- **Check:** Dependent fields are assigned only inside the computing method, and no other code writes them.

## Rules: choosing the business-logic pattern

### 20. Choose the business-logic pattern per subdomain, by its needs

Match the pattern to the subdomain, not to a favorite. Ask in order: does money or audit need full history, how complex are the rules, and does the vocabulary describe processes? Money and audit needs point to event sourcing, complex invariants to a domain model, and simple CRUD work to a transaction script or active record. Advanced patterns add cost, so each must justify itself with a stated requirement, and you should understand why a tool fits before using it. [DDD-P6, DDD-T54, DDD-T56, DDD-P8]

- **Do:** Record the answers and the chosen pattern per subdomain in the design notes, along with any heuristic you set aside. Keep working active records for simple logic. Move a script or active-record module to a richer pattern when its invariant checks keep growing.
- **Not when:** Advanced patterns still fit subdomains with real complexity, so judge each case by its reasoning rather than avoiding them by reflex. Event sourcing adds significant cost, so adopt it only where history, audit, deep behavior analysis or very complex event-publishing logic requires it.
- **Check:** Advanced patterns wrap only logic with real rules, simple modules have no extra layers, and design notes tie each domain model, event-sourced store or CQRS setup to a specific requirement.

## Rules: event sourcing

### 21. Event-source an aggregate only where history matters

Store an aggregate as a sequence of events only when the business needs full history, audits, money tracking, deep behavior analysis, or logic that has outgrown state-based patterns. Event sourcing needs training and ongoing effort, so it pays off only in those cases. [DDD-T26, DDD-P6]

- **Do:** Budget team training before adoption and state the requirement that justifies it.
- **Check:** Aggregate storage appends event rows, and the project plan includes training.

### 22. Rebuild state by replay and append with an expected version

Load an event-sourced aggregate by applying its stored events in order, run the command, and append the new events against the version you loaded. The event store allows only reads and appends, because the stored events are the history and editing them destroys the record. When an append finds a newer version, inspect the newer events before rejecting the command. [DDD-T27, DDD-T28]

- **Do:** Expose only fetch and append on the store. Loop over stored events in the constructor or loader.
- **Not when:** An exceptional case such as a data migration may need a controlled change to stored events.
- **Check:** The store offers fetch and append only, loads replay events in order, and stale appends are checked against newer events.

```python
def handle(store, agg_id, command):
    events = store.fetch(agg_id)
    agg = Account.replay(events)           # apply each stored event in order
    new_events = agg.execute(command)      # decide, do not mutate the store
    store.append(agg_id, new_events, expected_version=len(events))
```

### 23. Version event schemas instead of rewriting history

When an event's shape must change after events of that type are stored, add a new schema version beside the old one. Rewriting stored events would corrupt the history the design depends on. Readers must handle both versions. [DDD-T33, DDIA-P5]

- **Do:** Add a version to each event type and keep handling code for old versions.
- **Not when:** A controlled event-store migration, as allowed in rule 22, may change stored events.
- **Check:** Stored event records are never updated, and new versions appear beside old ones.

### 24. Add snapshots only after measuring slow replay

Introduce snapshot caching only when a benchmark at realistic event counts shows that replay is slow. Snapshots add complexity, and replay is often fast enough, so measure before tuning [DDD-T30, REF-T87].

- **Do:** Benchmark replay at realistic counts first. If you add snapshots, load the snapshot and its version, then query only the newer events.
- **Not when:** Aggregates stay far below the event counts at which replay becomes noticeably slow.
- **Check:** Benchmark results exist, and the load path reads the snapshot version and then newer events.

### 25. Make personal data in events erasable through per-aggregate keys

Stored events cannot be edited, so encrypt sensitive event fields with a key per aggregate, and delete the key when the data must become unreadable, for example under GDPR. [DDD-T31]

- **Do:** Hold keys in a separate store indexed by aggregate ID, and encrypt only the sensitive fields.
- **Check:** Sensitive fields are stored encrypted, with keys in a separate per-aggregate store.

### 26. Use persisted domain events as the audit trail

When an audit trail must reflect operations that change the database, derive it from the persisted events. Separately written log lines or audit rows can diverge from the change, and trigger-based history misses the reason. [DDD-T32]

- **Check:** No code inserts audit rows by hand, and the audit trail comes from persisted events.

## Rules: CQRS and projections

### 27. Separate the command model from read models

When the same data must be shown or stored in several shapes, use one command model for state changes and separate read models for queries, each shaped for its own use, and fill read models only from the write path. Each model can then fit its job, and read models can be rebuilt at will. In an event-sourced system, build several projections from the same stream and answer state queries from a projection, not from the event store, so new questions need no change to the producers. Keep the command model as the authoritative record and treat every read model as derived data. [DDD-T37, DDD-T29, DDIA-P1]

- **Do:** Name the source and the rebuild command for each read model. Make each projection's apply method ignore unrelated events.
- **Not when:** A duplicated copy is acceptable only when a process updates every copy (DDIA-P1).
- **Check:** Only the command path saves to the command model, read models receive writes only from projection code, and each projection keeps its own state.

### 28. Project with checkpoints, synchronously first

Update a read model from the changes after a stored checkpoint, and rebuild it by resetting the checkpoint to zero. A monotonic checkpoint lets a projection resume without skipping or repeating changes. Build a synchronous projection first and add an asynchronous one only on top of it, because the synchronous version is simpler and asynchronous projections bring disorder. [DDD-T38, DDD-T39]

- **Do:** Set a checkpoint column on every insert and update, order the projection query by it, and save the last value processed.
- **Check:** The projection query orders by the checkpoint column and stores its last value, and a synchronous projector exists before any message-bus projector.

## Rules: events, outbox and long-running processes

### 29. Name domain events in the past tense

A domain event records something that already happened in the business, so name it in the past tense. A command-style name reads as an instruction to act, which is a different thing. [DDD-T25]

- **Check:** Event class names end in past-tense verbs, such as TicketEscalated rather than EscalateTicket.

### 30. Save events in an outbox in the aggregate's transaction

When a state change must reach other components, write the new events to an outbox in the same transaction as the aggregate, and publish them from a relay afterwards. A crash between saving and publishing would otherwise lose events or announce a change that never committed. The relay marks or deletes each outbox row only after it has published that event successfully. An outbox with its own schema also lets internal schemas change while downstream consumers stay stable, and feeding other systems from one ordered change log avoids fragile multi-system writes. [DDD-P7, DDD-T46, DDD-T47, DDIA-T50, DDIA-P8]

- **Do:** Keep publish calls out of aggregate methods. Insert outbox rows in the same transaction as the domain write, and have the relay update the published flag only after a successful publish.
- **Not when:** Published events cannot be cancelled, so reverse them with compensating commands. Skip a separately shaped outbox when maintaining its transformation and extra writes costs too much (DDIA-T50). Distributed transactions remain an option only in environments that accept their cost (DDIA-P8).
- **Check:** One transaction writes the aggregate record and its unpublished event records, no publish call sits inside an aggregate, and the relay marks rows only after a successful publish.

```sql
BEGIN;
UPDATE orders SET status = 'PAID', version = 8 WHERE id = :id AND version = 7;
INSERT INTO outbox (event_id, type, payload, published) VALUES (:eid, 'OrderPaid', :json, false);
COMMIT;
-- relay, later: publish row, then UPDATE outbox SET published = true WHERE event_id = :eid;
```

### 31. Make subscribers tolerate duplicates and disorder

A relay that fails to mark an event will publish it again, so duplicate messages are normal. Design every subscriber to skip or safely reapply events it has already processed and to accept messages out of order. Where a caller may retry an update after an unclear failure, send the target value rather than an increment, because a retried increment double-counts. [DDD-T48, DDD-T67, DDIA-P3]

- **Do:** Store processed event IDs or sequence numbers and check them before applying. Write updates that set an explicit value.
- **Not when:** Idempotence through operation IDs assumes replays in original order, a deterministic handler and one writer per key. Operations that are not naturally idempotent need extra metadata and fencing during failover (DDIA-P3).
- **Check:** Handlers record and check processed IDs or sequence numbers, and update statements set values instead of adding to stored ones.

### 32. Coordinate multi-aggregate processes with compensating sagas

Model a business process that spans several transactions as a saga, and pair each state-changing step with a compensating command, because a finished step cannot be undone directly. Store the events the saga receives and the commands it issues, so it can compensate after failures. Treat its participants as eventually consistent and do not assume atomic reads across them. [DDD-T49, DDD-T50, DDD-P5, DDD-P7]

- **Do:** Write the compensating command next to each step in the saga code. Append a command-issued event whenever the saga sends a command.
- **Not when:** If the next step depends on earlier results, use a process manager (rule 33). Do not use a saga to split operations that need strong consistency.
- **Check:** Each state-changing saga step has a paired compensating command, saga state changes append command-issued events, and no read assumes atomicity across components.

### 33. Use a process manager when the process branches

When the next step depends on earlier outcomes, such as choosing between alternative routes, implement the process as a process manager. Create it explicitly with its own identifier and persist its state, because it must remember choices and progress that a plain saga would lose. [DDD-T51]

- **Do:** Give the process class an identifier, persist its state, and branch on stored outcomes.
- **Check:** The process class has an identifier, persists its state and branches on earlier outcomes.

### 34. Send notifications, then query the producer for details

When notification data is sensitive, or the consumer must see the latest write, send a short notification with identifiers and let the consumer query the producer for details. Notifications can be stale or arrive before the write is visible, so the producer is the reliable source. When several consumers receive a notification but only one may process it, lock the record before processing. [DDD-T52, DDD-T72]

- **Do:** Have the handler authorize and call the producer's detail endpoint before using the data. Take a lock on the record before processing a single-consumer notification.
- **Check:** Handlers fetch details from the producer before acting, and single-consumer handlers lock the record first.

## Playbooks

### When you start modeling a new business area
1. Describe the client-facing service, take the departments as a first draft of subdomains, and refine by client service [DDD-P1, DDD-T07].
2. Draw each subdomain around use cases that share actors and data, and stop splitting generic and supporting parts once finer cuts change no decision [DDD-T08, DDD-P1].
3. Label each subdomain core, supporting or generic with a business reason, and decide build, buy or keep simple for each [DDD-T01, DDD-T03, DDD-T05, DDD-T06].
4. Start the glossary with the domain experts' terms, and split any term with two meanings [DDD-T09, DDD-T10, DDD-T11].
5. Once a modeling workshop's timeline of commands, events and policies is complete, group them into aggregates, and aggregates linked by events into candidate contexts, starting core contexts wide [DDD-T63, DDD-T53].
6. Choose the business-logic pattern for each subdomain by the ordered questions, and record the answers [DDD-T54, DDD-T56].
7. Draw the context map with a pattern and owner for each integration [DDD-T45, DDD-T43].

### When you add or change a business rule in a domain model
1. Name the rule with glossary terms, and update the glossary in the same commit if a term's meaning changes [DDD-T09, DDD-T11].
2. Find the aggregate whose invariant the rule protects. If the rule needs data that must be current at decision time, that data belongs in the aggregate [DDD-T22, DDD-T21].
3. If the rule spans several aggregates or sources, put it in a stateless domain service instead [DDD-T23].
4. Expose the change as a named command on the root, and replace any primitive the rule validates with a value object [DDD-T18, DDD-T13, DDD-T14].
5. Test it with unit tests that construct the aggregate and value objects directly; see [testing](testing.md) [DDD-T55].

### When your context needs another context's data or behavior
1. Look up the relationship on the context map, or choose a pattern from how closely the teams collaborate [DDD-T45, DDD-T43].
2. If the upstream model suits you, conform. Otherwise map its types inside one translation module [DDD-T40].
3. If you are the upstream serving many consumers, publish a separate, versioned language [DDD-T41, DDIA-P5].
4. Share a kernel only if duplication costs more than coordination and both teams accept the coupling [DDD-T42].
5. If collaboration costs more than duplication and the feature is not core, implement it separately [DDD-T44, DDD-P4].

### When a state change must notify other components
1. Name the event in the past tense [DDD-T25].
2. Write the event to the outbox in the aggregate's transaction, and publish nothing from inside the aggregate [DDD-T46, DDD-P7].
3. Have the relay mark each row published only after the publish succeeds [DDD-T47].
4. When external or numerous consumers depend on the events, translate internal events into the published language before they leave the context [DDD-T41, DDIA-T50].
5. Make every subscriber skip duplicates, accept disorder and set target values [DDD-T48, DDD-T67].
6. If the data is sensitive or must be fresh, send identifiers only and let the consumer query the producer. Lock the record if only one consumer may act [DDD-T52, DDD-T72].

### When a business process spans several aggregates
1. Test whether the operation would give wrong results under eventual consistency. If it would, redraw the aggregate boundary rather than coordinate [DDD-T22, DDD-P5].
2. If no step depends on the results of earlier ones, write a saga and give each state-changing step a compensating command [DDD-T49].
3. If later steps depend on earlier results, write a process manager with its own identifier and persisted state [DDD-T51].
4. Persist the events the process receives and the commands it issues, and do not assume atomic reads across participants [DDD-T50].
5. Make each step's handler idempotent, because messages may arrive twice or out of order [DDD-T48, DDIA-P3].

### When you adopt event sourcing for an aggregate
1. Confirm a stated need for history, audit, money tracking or very complex event logic, and budget training [DDD-T26, DDD-T56].
2. Restrict the store to fetch and append, and append with the expected version [DDD-T28].
3. Load by replaying events in order, then execute the command and append the new events [DDD-T27].
4. Serve queries from projections rather than the event store [DDD-T29].
5. Encrypt personal fields with per-aggregate keys, and plan schema versions for future changes [DDD-T31, DDD-T33].
6. Use the event stream as the audit trail [DDD-T32].
7. Add snapshots only after a benchmark at realistic counts shows slow replay [DDD-T30].

### When you add a read model
1. Confirm that the same data must be shown in several shapes, then keep the command model as the only write target [DDD-T37, DDIA-P1].
2. Build a synchronous projection first [DDD-T39].
3. Drive it from a checkpoint column set on every insert and update, and save the last value [DDD-T38].
4. Add an asynchronous projector only on top of the working synchronous one, and make it tolerate disorder [DDD-T39, DDD-T48].

## Where the books disagree

### When does a concept deserve a value object instead of a primitive?
- **Learning DDD:** Represent money, names, identifiers and similar concepts with value objects that validate themselves, except in simple supporting subdomains [DDD-T13, DDD-T14, DDD-T06].
- **TDD:** Use a plain value such as a string for a new concept until it needs behavior of its own, and add classes only when a failing test needs them [TDD-T19, TDD-T18, TDD-P9].
- **Decide:** Use a value object once the concept has rules of its own, such as validation, which is DDD-T13's reason and meets TDD-T19's own *Not when*, or once several places accept the same input, which is DDD-T14's *When*. Keep a plain value while the concept is needed only for identity and no rule touches it, which is TDD-T19's *When*. In a simple supporting subdomain, primitives are acceptable either way [DDD-T13, DDD-T14, TDD-T19, DDD-T06].

### Should equal logic in two contexts be shared or duplicated?
- **Refactoring and Pragmatic Programmer:** Keep each piece of knowledge in one place, because copies drift and a missed copy becomes a defect [REF-P4, PP-P3].
- **Learning DDD:** Give each context its own model and meaning for a term, share a kernel only when duplication costs more than coordination, and let non-core features be duplicated when collaboration costs more [DDD-T10, DDD-T42, DDD-T44].
- **Decide:** Never duplicate core logic [DDD-P4, DDD-T44]. Within one context, unify real duplicates at the third similar case, or sooner when a bug or feature exposes them, and let code that never changes keep its copies [REF-P4]. Across contexts, first check whether identical-looking code encodes different rules that change separately, as both PP-P3 and REF-P4 warn. If it does, it is not duplication. If it is truly one rule in a non-core area, compare the cost of coordinating a shared kernel against the cost of a second implementation, and choose separate ways only when collaboration is the more expensive one [PP-P3, DDD-T42, DDD-T44].

### Should the business-logic pattern be chosen up front or grown from tests?
- **TDD and Design Patterns:** Add classes, interfaces and patterns only when a failing test or a real variation demands them [TDD-P9, GOF-P4].
- **Learning DDD:** Choose transaction script, active record, domain model or event sourcing per subdomain from the business's needs before building it, and start core contexts wide [DDD-T54, DDD-T53].
- **Decide:** Treat the per-subdomain pattern choice and the context boundaries as system-shaping decisions, which TDD-P9's own *Limits* allows to be reasoned through before code. Answer the DDD-T54 questions and record them, but adopt an advanced pattern only for a stated requirement [DDD-T56, GOF-P4]. Inside the chosen pattern, add each class or parameter only when a failing test or current behavior requires it [TDD-T18]. When a simpler module's invariant checks keep growing, move it to a richer pattern then [DDD-T54].

### Must a value object define its hash code from the start?
- **Learning DDD and Refactoring:** A value object's equality and hash code both use every field [DDD-T15, REF-T84].
- **TDD:** Override the hash code with equals once the class serves as a map key or set member, and defer it until then [TDD-T29].
- **Decide:** Implement the hash code with equals once the value object serves as a map key or set member, which is TDD-T29's *When* and falls under DDD-T15's "stored in a collection". Before that, DDD-T15 and REF-T84 still check a hash code over every field, while TDD-T29 allows deferring it. The entries give no further condition, so follow the codebase's existing convention for value classes [DDD-T15, REF-T84, TDD-T29].

## Review checklist

- [ ] New and renamed classes, methods, events and tests use glossary terms, and the glossary changed in the same commit as any redefined term [DDD-T09, DDD-T11].
- [ ] No class mixes two unrelated concepts under one name, and no name prefix is repeated across areas to tell meanings apart [DDD-T10].
- [ ] Core modules contain no generic or supporting code, and supporting modules add no extra abstraction layers [DDD-T03, DDD-T06].
- [ ] Each advanced pattern in the diff (domain model, event sourcing, CQRS) is tied to a stated requirement in design notes [DDD-T56, DDD-T54].
- [ ] Domain modules import no upstream context's types, and mapping happens in one translation module [DDD-T40].
- [ ] Public APIs for external or numerous consumers use payloads that differ from internal domain classes, with a per-version schema [DDD-T41].
- [ ] Any new cross-context integration appears on the versioned context map with its pattern and owner [DDD-T45, DDD-P4].
- [ ] No core rule is implemented in two contexts [DDD-P4, DDD-T44].
- [ ] Domain classes expose business actions, invariant fields have no external setters, and children are reached only through the root [DDD-T12, DDD-T17, DDD-T18].
- [ ] Concepts with rules are value objects that validate in construction, with no setters, with equality over every field, and with a matching hash code at least once they serve as map keys or set members [DDD-T13, DDD-T14, DDD-T15, TDD-T29].
- [ ] Identifier properties have no setter [DDD-T16].
- [ ] Each command handler or transaction saves exactly one aggregate and passes the version it read [DDD-T20, DDD-T19].
- [ ] Other aggregates are referenced by identifier, and data feeding a decision lives in the deciding aggregate [DDD-T21, DDD-T22].
- [ ] Dependent fields are assigned only in the method that computes them [DDD-T24].
- [ ] Event names are past tense [DDD-T25].
- [ ] No publish call sits in an aggregate, the outbox insert shares the domain write's transaction, and the relay marks rows only after a successful publish [DDD-P7, DDD-T46, DDD-T47].
- [ ] Subscribers record and check processed IDs and accept disorder, and retried updates set target values rather than increments [DDD-T48, DDD-T67].
- [ ] Every state-changing saga step has a compensating command, and branching processes are process managers with identifiers [DDD-T49, DDD-T51].
- [ ] The event store exposes fetch and append only, and no migration rewrites stored events outside a controlled change [DDD-T28, DDD-T33].
- [ ] Personal data in events is encrypted with per-aggregate keys, and audit history comes from events, not hand-written rows [DDD-T31, DDD-T32].
- [ ] Snapshots in the diff come with benchmark results [DDD-T30].
- [ ] Read models are written only by projection code, driven by a checkpoint, and a synchronous projector exists before any asynchronous one [DDD-T37, DDD-T38, DDD-T39].

## More entries in this area

- `DDD-T64` — Record analytics as append-only facts: when building an analytical model, append fact rows for business activities and never update or delete them.
- `DDD-T65` — Validate records against a schema on ingestion: when a data lake accepts records several analytical models may use, validate them against a declared schema and quality checks first.
- `DDD-T66` — Publish analytical outputs with schemas and SLAs: when other teams consume an analytical output from a context, serve it through a defined port with a versioned schema and a monitored SLA, fed from outputs rather than operational tables.
- `DDD-T55` — Unit-test domain models through aggregates: most domain-model tests construct aggregates and value objects directly; see [testing](testing.md).
- `DDD-T57` and `DDD-T58` — Refactoring legacy code toward aggregates and replacing it through a strangler facade; see [legacy-code](legacy-code.md).
- `DDD-T34`, `DDD-T35`, `DDD-T36`, `DDD-T60`, `DDD-T68`, `DDD-T69`, `DDD-T70`, `DDD-T71` — Keeping rules out of UI and storage, service layers, ports, deep services, vertical modules and service data ownership; see [architecture](architecture.md).
- `GOF-T18` — Represent each entity state as its own object: when an entity's behavior depends on a state that changes over time; see [design-patterns](design-patterns.md).
- `DDIA-T52` — Make writes idempotent with stored input offsets: when a consumer writes from a log-based broker into an external database; see [data-systems](data-systems.md).
