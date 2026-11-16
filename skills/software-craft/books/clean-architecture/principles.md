# Clean Architecture — Robert C. Martin (1st edition, 2017)

## Summary

The book argues that architecture exists to keep a system cheap to change over its whole life, because a system that resists change eventually becomes useless. It keeps business rules independent of user interfaces, databases and frameworks, and it arranges source dependencies so they point toward stable, high-level policy. Boundaries are drawn where parts change for different reasons, and decisions stay open while they are still unknown. The same ideas apply from classes up to deployable components and services, and design is judged by the effort each change takes.

## Principles

### CA-P1: Point source dependencies toward stable policy

Source dependencies should point toward stable, high-level policy and abstractions, never toward volatile details. A change in a detail must not force a change in the policy it serves. Here a component is stable when many other components depend on it, and volatile when it changes often, such as presentation or reports.

- **Apply:** Make each new import point toward an interface or a more stable component.
- **Limits:** Stable platform classes, such as strings, may stay concrete.
- **Check:** No stable or high-level module imports a volatile or low-level module.
- **See:** CA-T08, CA-T13, CA-T53
- **Source:** ch. 11, 19, 22, 34

### CA-P2: Keep business rules free of delivery details

Business rules should not reference user interfaces, databases, web code or frameworks. These are details that plug into the rules, which keeps the rules reusable.

- **Apply:** Keep rule modules free of imports from UI, database, web and framework packages.
- **Limits:** The database-as-detail idea concerns the storage technology, not the data model itself.
- **Check:** Business-rule modules import no UI, database or framework packages.
- **See:** CA-T47, CA-T48, CA-T56, CA-T60
- **Source:** ch. 5, 20, 22, 30, 31

### CA-P3: Group code by reasons and rates of change

Group code that changes for the same reason at the same time, and separate code that changes for different reasons. The same test drives component boundaries and single responsibilities.

- **Apply:** Before placing a class, ask which stakeholder or cause would make it change, inside its feature package (CA-T76).
- **Check:** Each component's classes share one reason for change and one rate of change.
- **See:** CA-T11, CA-T12, CA-T26
- **Source:** ch. 7, 13, 17, 33

### CA-P4: Defer decisions the design does not need yet

Keep choices about frameworks, databases and views open until the use cases and constraints settle them. The book holds that a good architecture leaves as many of these decisions open as it can.

- **Apply:** Put each infrastructure choice behind a boundary, and choose at the latest responsible moment, once the core no longer depends on it.
- **Check:** Database and framework choices are confined to one module that the core does not reference.
- **See:** CA-T45, CA-T46, CA-T58
- **Source:** ch. 15, 16, 17, 21

### CA-P5: Test business rules without delivery mechanisms

Business rules should be testable without a GUI, database, web server or device running, so each part can be tested on its own.

- **Apply:** Build rule tests from the use case with stub gateways instead of live infrastructure.
- **Check:** The rule test suite runs with no server, database, GUI or device process started.
- **See:** CA-T63, CA-T64, CA-T70
- **Source:** ch. 4, 21, 23, 29

### CA-P6: Pass plain data across boundaries

Data that crosses a boundary should be simple structures, not entities, database rows or framework objects. Each side then stays free of the other side's formats.

- **Apply:** Define a plain request or response structure for each boundary crossing.
- **Check:** Boundary parameters are plain structs, transfer objects or maps, never entity or row types.
- **See:** CA-T43, CA-T57, CA-T60
- **Source:** ch. 20, 22, 30

### CA-P7: Judge architecture by how easily it changes

Judge architecture by the effort needed to change, build, deploy and maintain the system over its life. A system that cannot change becomes useless, so changeability outranks rigid present behavior.

- **Apply:** Include the estimated cost of likely future changes in each design review.
- **Check:** Review notes estimate the cost of likely future changes, not only current features.
- **See:** CA-T05
- **Source:** ch. 2, 15, 16, 29
