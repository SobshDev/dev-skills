# Learning Domain-Driven Design — Vlad Khononov (1st edition, 2021)

## Summary
Domain-driven design ties software design to the business problem it solves. The book starts with strategy: it separates core subdomains from supporting and generic ones, and draws bounded contexts around coherent models. Tactical patterns then follow the complexity of each area's logic. Shared language and explicit integration contracts keep models honest as systems grow.

## Principles

### DDD-P1: Start from the business and its subdomains
The book starts with the business strategy and the client service, then splits the domain into subdomains.

- **Apply:** Describe the business as a client service, then split it into subdomains, setting aside areas that software does not touch.
- **Limits:** Stop splitting generic and supporting areas once finer parts change no design decision. Distill core subdomains as far as possible.
- **Check:** Design notes name the client-facing service and list the subdomains behind it.
- **See:** DDD-T01, DDD-T02, DDD-T03
- **Source:** ch. 1

### DDD-P2: Speak one language with the business
The book calls the ubiquitous language the cornerstone of the approach. Developers' misunderstandings reach production, so developers and domain experts must share its terms.

- **Apply:** Name classes, methods, tests and tickets with the glossary terms, in supporting and generic areas too, and use the terms in daily conversation, not only in documents.
- **Check:** Business rules in documentation name a domain expert as their source, and identifiers match the glossary.
- **See:** DDD-T09, DDD-T10, DDD-T11
- **Source:** ch. 1, 2, Appendix A

### DDD-P3: Draw bounded contexts around one model
A bounded context gives each term one meaning and one model. The book sizes contexts by business needs and consistency requirements, not by a fixed target.

- **Apply:** Split a context where its terms conflict, and avoid one model for every department.
- **Limits:** Start core contexts wide while the logic is unclear, and narrow them once it stabilizes. Avoid a one-to-one subdomain mapping where problems need different models.
- **Check:** Each context defines its terms once, and references to another context's terms go through an explicit mapping.
- **See:** DDD-T10, DDD-T53, DDD-T59
- **Source:** ch. 3, 11

### DDD-P4: Integrate through explicit contracts
Every touchpoint needs a documented contract, and the integrations belong on a context map.

- **Apply:** Name the integration pattern for each context pair on the context map.
- **Limits:** Never duplicate core logic, even when collaboration fails.
- **Check:** The context map lists each integration with its pattern, and each touchpoint has a documented contract.
- **See:** DDD-T40, DDD-T42, DDD-T43, DDD-T44, DDD-T45
- **Source:** ch. 4

### DDD-P5: Keep strong consistency inside one aggregate
An aggregate is the consistency boundary, and only its own methods change its state. Data that must stay strongly consistent belongs inside it.

- **Apply:** Change one aggregate per transaction, and keep only the data its invariants need inside it.
- **Limits:** Use a saga for multi-aggregate processes, but never to split operations that need strong consistency.
- **Check:** Each command handler saves a single aggregate, and aggregate fields have no external setters.
- **See:** DDD-T18, DDD-T20, DDD-T21, DDD-T22, DDD-T49
- **Source:** ch. 6, 9

### DDD-P6: Let logic complexity choose the pattern
The book matches the business-logic pattern to the complexity of the rules. Simple CRUD work can use transaction scripts or active records. Complex invariants need a domain model, and subdomains that track money or audit need event sourcing.

- **Apply:** Choose transaction script, active record, domain model or event sourcing per subdomain, and keep working active records for simple logic.
- **Limits:** Event sourcing adds significant cost, so adopt it only where history, audit, deep behavior analysis, or very complex event-publishing logic requires it.
- **Check:** Advanced patterns wrap only logic with real rules, and simple modules avoid extra layers.
- **See:** DDD-T54, DDD-T55, DDD-T56
- **Source:** ch. 5, 7, 10, 11

### DDD-P7: Publish events only after reliable storage
When a change must reach other components, the book uses the outbox pattern. The state change and its events are saved in one transaction, and a relay publishes them afterwards.

- **Apply:** Write events to an outbox in the same transaction as the aggregate, then publish them from the relay.
- **Limits:** Events cannot be cancelled, so reversals use compensating commands.
- **Check:** No publish call sits inside an aggregate method, and the outbox write shares the aggregate's transaction.
- **See:** DDD-T46, DDD-T47, DDD-T48, DDD-T49
- **Source:** ch. 5, 9, 15

### DDD-P8: Start simple and evolve in small steps
The book introduces DDD concepts gradually, and it asks for the reasoning behind each tool before use. Legacy systems change through gradual replacement.

- **Apply:** Understand why each DDD tool fits before applying it, and modernize legacy code one component at a time.
- **Limits:** Advanced patterns still fit subdomains with real complexity, so judge each one by its reasoning, not by reflex.
- **Check:** The modernization plan names a strategy, strangler or refactoring, for each component.
- **See:** DDD-T56, DDD-T57, DDD-T58
- **Source:** ch. 13, Closing Words
