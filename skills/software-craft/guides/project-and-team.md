# Projects, requirements, dependencies and team practice

This guide covers the work around the code: starting a project, turning vague requests into working slices, keeping known problems visible, automating and versioning the project, managing dependencies and deprecations, documenting, and making decisions a team can review. The single most important idea is to let running, end-to-end code and written, reviewable records carry the project, not memory, verbal agreements or modules that are "mostly done".

**Read this when:** creating a new repository or service, picking up a feature request or a vague requirement, deciding whether to prototype, finding a known defect you cannot fix in this change, adding or upgrading a dependency, publishing a shared library, deprecating or removing an old API or system, writing or changing project documentation, choosing between technical options, or setting up owners, CI and scripts.

**Entry IDs** such as `WELC-T12` point to `../books/<book>/techniques.md` (T) or `principles.md` (P);
the prefix table is in [SKILL.md](../SKILL.md).

## Contents
- [Core rules](#core-rules)
- [Rules: requirements and delivery](#rules-requirements-and-delivery)
- [Rules: known problems and broken windows](#rules-known-problems-and-broken-windows)
- [Rules: automation and version control](#rules-automation-and-version-control)
- [Rules: dependencies and shared components](#rules-dependencies-and-shared-components)
- [Rules: deprecation and migration](#rules-deprecation-and-migration)
- [Rules: documentation](#rules-documentation)
- [Rules: decisions and trade-offs](#rules-decisions-and-trade-offs)
- [Rules: ownership and teamwork](#rules-ownership-and-teamwork)
- [Playbooks](#playbooks)
- [Where the books disagree](#where-the-books-disagree)
- [Review checklist](#review-checklist)
- [More entries in this area](#more-entries-in-this-area)

## Core rules

### 1. Decide how long the code must live first

SWE at Google ties every practice to the code's expected lifespan. Before choosing how much testing, documentation, dependency discipline or forking a piece of code gets, decide whether other people or later work will depend on it, and treat it as long-lived if so. Long-lived code needs owners, upgrades and documentation, while short-lived or narrow code can skip the heavier practices. [SWE-P1]

- **Do:** Ask whether anyone else, or any later work, will build on this code. If yes, give it an owners file, a test suite and a README that states its support level and expected lifespan. Use that answer to size the other rules in this guide.
- **Not when:** Short-lived or narrow code may fork or skip heavy practices, but a long-lived fork still needs security fixes. Code that will never be upgraded may take whatever dependency version is available.
- **Check:** Long-lived code has an owners file, a test suite, and a README stating its support and lifespan.

### 2. Make the first commit build, run and verify

Pragmatic Programmer starts a new project with minimal code that is confirmed to build and run before any feature exists, so later features rest on a known-working base. SWE at Google adds that a long-lived project should get an owners file naming a primary and a backup owner, plus continuous integration, when it is created, so responsibility and verification are explicit from the start. [PP-T01, SWE-T18, SWE-P1]

- **Do:** Make the first commit a skeleton with build and run steps that succeed. In the same early commits, add an owners file with two named owners and a CI configuration. For the detailed CI and presubmit setup, see [change-workflow](change-workflow.md).
- **Not when:** The owners-and-CI step is for long-lived repositories, services and libraries (SWE-P1).
- **Check:** The first commit includes build and run steps that succeed, and a new long-lived project's first commit includes an owners file naming two owners and a CI configuration.

## Rules: requirements and delivery

### 3. Check whether the need requires software at all

Pragmatic Programmer notes that the cheapest way to meet a need often involves no new code. Before building a requested feature, look for a non-software option, and if one meets the need, ask the user before building. [PP-T69]

- **Do:** Before implementing, list the alternatives you considered, including non-software ones, and put that list in your reply to the user. Start building slices (rule 6) only once software is confirmed as the answer (PP-T24).
- **Check:** The reply to the user lists the alternatives considered, including non-software ones.

### 4. Ask about the edges of simple-sounding requirements

Pragmatic Programmer treats requirements as discovered, not handed over. Edge cases cost far more to find after the code exists, so a requirement that sounds simple and self-contained deserves questions about its boundaries, and each refined requirement should be written down where the work is tracked. [PP-T53, PP-P9]

- **Do:** Ask the user what should happen at the edges of the requirement, record each question and answer in the ticket, and update the ticket again when a demo reshapes the requirement. Ask stakeholders how they will judge success a month or a year after delivery. Name what you build in the domain's own terms (PP-T26, DDD-P2); see [domain-modeling](domain-modeling.md).
- **Check:** Requirement tickets list edge-case questions with recorded answers, and refined requirements appear in their tickets.

### 5. Build a thin end-to-end path before widening any layer

Pragmatic Programmer connects one feature through every layer early, as a runnable path built to production standard with error checks, structure and documentation. Integration problems and gaps in the target only show up when all the layers meet, so a single path through the interface, logic, data and storage surfaces them early. The book applies this when requirements are vague, or when the algorithms, libraries or environment are unfamiliar. [PP-T02]

- **Do:** Pick one feature and make it run through every layer before adding a second feature or deepening any one layer. Write that path with real error checks and structure, because it is kept, not thrown away. Where a layer does not exist yet, a stub or in-memory data access can stand in (CA-T45); see [architecture](architecture.md).
- **Not when:** A throwaway prototype answers one narrow question better (rule 8).
- **Check:** One feature runs through the interface, logic, data and storage in a single path.

### 6. Deliver small slices, riskiest first, with feedback each time

Pragmatic Programmer builds working functionality in small slices that each cut through every layer, starts with the riskiest one, and reports each slice to the customer before starting the next. Feedback after each slice shows whether the team understands the problem, and the rate of that feedback limits how fast the work should go. [PP-T24, PP-P9, PP-P2]

- **Do:** Order the slices by risk, deliver one, show it, and adjust the next slice to what the feedback taught you. Split a slice that is too large to confirm quickly. For commit and PR sizing inside a slice, see [change-workflow](change-workflow.md).
- **Not when:** Start slicing once PP-T69 has confirmed that software is needed.
- **Check:** Each change delivers something a user can exercise end to end, and each iteration ends with a demo or review.

### 7. Show and measure progress with working use cases

Pragmatic Programmer prefers a running demo to a progress document, because running code draws feedback that signed documents cannot. It reports progress as use cases that work end to end, since modules reported as mostly complete can hide integration work that has not been done. [PP-T23, PP-T25, PP-P9]

- **Do:** When asked for a status update, show a demo script or branch that runs the full path. Report each use case as working end to end or not started, rather than as modules that are mostly complete.
- **Check:** A demo script or branch runs the full path successfully, and progress reports list each use case as working end to end or not started.

### 8. Prototype risky parts in disposable code

When an unproven component, data format or performance concern affects the design, Pragmatic Programmer builds a throwaway prototype that answers one specific question and then builds the chosen design properly. Tidy First applies the same idea to a structure change that is costly to undo, such as extracting a separate service: a spike is cheap to discard, while a permanent split is expensive to reverse. [PP-T03, TF-T35]

- **Do:** Write down the one question the prototype must answer. Keep the prototype outside the production tree or on a spike branch, answer the question, then write the real implementation cleanly instead of promoting the prototype.
- **Not when:** If the question is how the layers fit together rather than one narrow unknown, build the thin end-to-end path of rule 5 instead.
- **Check:** Prototype code sits outside the production tree, a clean implementation replaces it, and a prototype branch or spike exists before a costly-to-undo split lands.

### 9. Build only what current requirements need

Pragmatic Programmer builds only the structure, options and features that current requirements and callers need, because guessed extensions and extra polish add code that serves no stated requirement. Clean Architecture says the same about reuse in a young or ordinary application: shape components for ease of change and leave reuse for later, since early reuse concerns guess at needs that only real change reveals. [PP-T71, CA-T27]

- **Do:** Trace each extension point, option and polish item to a stated requirement or caller, and stop when those are met. For when an abstraction earns its place, see [module-design](module-design.md) and [design-patterns](design-patterns.md).
- **Not when:** Structure that the agreed value still needs is not a guessed future need. Once other projects already draw from a component and depend on its reuse, design for that reuse (CA-T27).
- **Check:** Extension points and later changes trace back to a stated requirement or caller.

## Rules: known problems and broken windows

### 10. Repair broken windows in the code you touch

Pragmatic Programmer asks you to fix bad design or poor code as soon as you notice it, within the change that touches it, and to report other problems together with a next step. Philosophy of Software Design agrees: when a change exposes a design flaw, fix the structure in that change instead of wrapping it, because small fixes made during changes stop complexity from piling up. Clean Code and Legacy Code likewise improve the area each change touches and leave the rest alone until it must change. [PP-P1, POSD-T18, CC-P6, WELC-P8]

- **Do:** Correct known defects in code your change already touches. Put the structural part in its own commit, separate from behavior changes (TF-P1). For problems outside your change, report them with a concrete next step. The mechanics of tidying are in [refactoring](refactoring.md) and [change-workflow](change-workflow.md).
- **Not when:** A deadline blocks the fix, in which case record the cleanup as an owned follow-up (POSD-T18, POSD-T19). A bug-fix diff under pressure stays limited to the defect's own change (PP-T72). Legacy Code allows larger restructurings in parts the team has chosen to rewrite, and a bigger refactoring early in a release when the risk is accepted (WELC-P8). See the tension on fixing now versus later.
- **Check:** Code the change touches has its known defects corrected in that change, and status notes pair other problems with next steps.

### 11. Contain an unfixable defect with a visible stopgap

When there is not enough time to repair a defect properly, Pragmatic Programmer contains the damage now with a stub or message that is plainly marked as temporary. The visible stopgap limits harm while keeping the unfinished work known to everyone. [PP-T05]

- **Do:** Replace the broken behavior with something safe and obviously temporary, such as a not-implemented error or a clearly named TODO, and open a backlog item for the proper fix (rule 12).
- **Not when:** The proper fix is possible now, so make that fix instead.
- **Check:** Stopgap code carries a visible marker, such as a not-implemented message or a named TODO.

### 12. Keep one named, owned backlog item per known problem

Pragmatic Programmer reviews the project regularly for known defects and weak areas and keeps one backlog entry for each, with a name and an owner, so known problems are not forgotten. Philosophy of Software Design treats cleanup as scheduled work with an owner and suggests reserving roughly 10 to 20 percent of development time for it. Tidy First keeps a Fun List of deferred messes to work through when no feature presses on them. [PP-T04, POSD-T19, TF-T29]

- **Do:** When a review, a new team member or your own change turns up a problem you are not fixing now, add a named item with an owner to the tracker or the change description. Plan cleanup time into the sprint or release.
- **Not when:** The Fun List is not for an area a pending change waits on, because that tidying belongs before or after that change (TF-T29, TF-P4).
- **Check:** The backlog holds a named, owned item for each known problem area, and cleanup not done in this change is listed as a follow-up with an owner.

## Rules: automation and version control

### 13. Keep everything needed to build and deploy in version control

Pragmatic Programmer stores source, configuration, docs, scripts and notes in version control, so any capable machine can reproduce a build and every release can be reviewed. Release It! creates new installations from a deployment definition kept in source control. Both exclude credentials, which are supplied at runtime from outside the source and the release artifact. [PP-P7, PP-T17, RI-T34, PP-T35, RI-P8]

- **Do:** Commit build files, pipeline definitions, deployment configuration and installation definitions. Read keys, passwords and environment values at startup from external configuration. For secret handling, see [security](security.md).
- **Check:** Build and deployment configuration files are tracked in the repository, deployment steps live in a versioned file rather than manual runbooks, and source files contain no credential literals.

### 14. Replace written step lists with scripts

Pragmatic Programmer replaces written instructions for builds, releases, tests and setup with a script or pipeline definition, even for steps that seem to run only once, because a script runs the same way every time and a checklist depends on someone following it. Release It! does the same for repeated deployment steps. Clean Code hands style enforcement to an automated formatter, and SWE at Google generates large mechanical edits with tools instead of making them by hand. [PP-T18, PP-P7, RI-T45, CC-T74, SWE-T03]

- **Do:** When a task is described as "run these steps", turn it into a versioned script or pipeline stage and delete the prose steps. Commit formatter settings. For mechanical edits across many files, record the tool input that generates them.
- **Not when:** Learning a syntax-aware tool pays off for a mechanical edit beyond a few hundred edits, or fewer when the maintainers already know the tools. Smaller edits can use text tools (SWE-T03).
- **Check:** Recurring tasks exist as scripts or pipeline definitions, not as written instructions, and formatter settings are committed.

### 15. Store lasting project knowledge as plain text

Pragmatic Programmer keeps requirements, designs, test data and configuration as readable text files, because plain text stays readable as tools change and works with diff and search. [PP-T19]

- **Do:** Write requirements, design notes, decision records and test data as text files in the repository rather than in opaque binary formats.
- **Check:** Requirements, designs and test data are text files, not opaque binary blobs.

## Rules: dependencies and shared components

### 16. Pin each dependency to a named release

Clean Architecture keeps every dependency on a named release of a component and adopts newer releases on its own schedule, because a moving latest version lets another team's work in progress break your build. Learning DDD makes the same check for adopted generic solutions: manifests pin maintained versions. [CA-T29, DDD-T05]

- **Do:** Declare a named release in the manifest. Adopt a new release in a change of its own, when your team chooses.
- **Check:** Dependency declarations pin a release rather than a moving latest version.

```text
# moving target: another team's in-progress work can break this build
payments-client = "latest"

# pinned: adopt 4.3.x on your own schedule, in its own change
payments-client = "4.2.1"
```

### 17. Upgrade dependencies in small, regular increments

SWE at Google upgrades libraries and runtimes in small, regular steps and scripts any upgrade step that repeats. Accumulated change makes each later upgrade larger and riskier, and a codebase that has never been upgraded costs the most to move. Learning DDD expects adopted generic solutions to stay updated so they keep receiving security fixes. [SWE-T01, SWE-P1, DDD-T05]

- **Do:** Schedule upgrades for long-lived code as frequent, small changes, one dependency or a small group at a time. Script any step you have done before. Run the tests that the upgrade can affect; see [testing](testing.md).
- **Not when:** The upgrade costs more than the value it gives over the code's lifespan. Code that will never be upgraded may take any available dependency (SWE-P1).
- **Check:** Dependency update commits are frequent, each one touches a small set of files, and upgrades appear regularly in the history.

### 18. Write down what you assume about code you do not control

Pragmatic Programmer records each assumption your code makes about behavior it does not control, because unwritten assumptions are hard to recheck when the library changes. [PP-T67]

- **Do:** When your code relies on undocumented or edge-case behavior of a library or service, state the assumption in a comment or a test at the call site. Keep the vendor calls themselves behind your own wrapper (PP-T12); see [module-design](module-design.md).
- **Not when:** Undocumented behavior cannot always be avoided, so when you must rely on it, document the assumption carefully.
- **Check:** A comment or test at the call site states the assumed behavior.

### 19. Version and release-note every shared component

When a component is shared with other teams or projects, Clean Architecture gives it a version number and release notes that say what changed and which dependents it affects. Other teams can then choose when to adopt a release instead of absorbing changes without knowing. [CA-T25, CA-T29]

- **Do:** Bump the version and write release notes naming the changes and the affected dependents when you ship the component. Keep old and new readers working across the change where you cannot control the callers (DDIA-P5, RI-T46); see [data-systems](data-systems.md) and [production-reliability](production-reliability.md).
- **Check:** The component has a version number and release notes naming the changes and dependents.

## Rules: deprecation and migration

### 20. Deprecate only with a replacement and an owner

SWE at Google starts removing an old library, service or API only once a replacement offers the same or better functionality, because removal without one strands its users. Every migration needs an owner, and a compulsory deprecation also needs a deadline and enforcement. [SWE-P7, SWE-T28]

- **Do:** Ship the replacement first. Give the deprecated symbol an owner and a removal milestone. Have that owner move the callers or keep the old interface working, and review each migrated use against the replacement.
- **Not when:** Deprecate only systems that are demonstrably obsolete and have a comparable replacement.
- **Check:** The removal change follows a commit or release that introduces the replacement, and the deprecated symbol has an owner and a removal milestone.

### 21. Stop new uses of a deprecated symbol at review

Without a check at review, new code reintroduces the system a migration is trying to remove. SWE at Google flags each new use during review and suggests the replacement, and once a deprecation is compulsory, makes the check block the change. Refactoring keeps a renamed published function as a deprecated forwarder to the new name, so callers you do not control keep working. [SWE-T30, SWE-P7, REF-T18]

- **Do:** Add a presubmit or review check that names the deprecated symbol and points to its replacement. For a published function, keep the old name forwarding to the new one with a deprecation marker, and remove it once no known caller uses it.
- **Not when:** The forwarder is unnecessary when you control every caller and can update them together, and some published interfaces must stay forever (REF-T18).
- **Check:** A presubmit or review check names the deprecated symbol and points to its replacement, and compulsory deprecations block new uses.

```python
import warnings

def fetch_invoice(invoice_id):
    """Deprecated: use load_invoice. Owner: billing team. Removal: release 7.0."""
    warnings.warn("fetch_invoice is deprecated, use load_invoice",
                  DeprecationWarning, stacklevel=2)
    return load_invoice(invoice_id)
```

### 22. Find every caller with tooling before removing

SWE at Google finds code-level dependents of a deprecated system with static analysis and migrates them with tooling that generates reviewable updates, because analysis usually finds every caller and tooling keeps the migration consistent. Static analysis finds code-level dependents only, and the book's check also requires production logging to show no remaining callers before removal. Large generated changes are split into independent shards and applied to trunk, not to everyone's pending work. Once nothing uses the old code, delete it, because unused code still costs upkeep. [SWE-T29, SWE-T03, SWE-T23, SWE-T04]

- **Do:** Search statically for the deprecated symbol and add production logging for its use. Generate the migration with a tool, split it into shards that land alone, and regenerate a rejected shard instead of patching it by hand. Remove the old system only when both the search and the logs show no callers.
- **Not when:** Keep code that still delivers more value than its upkeep costs, and if its purpose is unclear, learn why it exists first (SWE-T04, SWE-T62).
- **Check:** A static search and production logging for the deprecated symbol both find no remaining callers before it is removed, and the deletion diff leaves no references.

## Rules: documentation

### 23. Review documentation changes like code, in the same change

SWE at Google sends documentation changes through code review, updates docs in the same change as the behavior they describe, and files doc errors in the same tracker as code bugs, because review keeps docs accurate the way it keeps code accurate. Learning DDD updates the shared glossary in the same commit as any change to a term's meaning. Philosophy of Software Design keeps one findable document of the project's main conventions, linked from the contributor entry point. [SWE-T33, DDD-T11, POSD-T32]

- **Do:** Edit the README, reference docs, glossary or conventions document in the same pull request as the behavior or convention change. Link doc-error fixes to their tracked issue. For comments and API doc comments inside code, see [readable-code](readable-code.md).
- **Check:** Doc edits appear in code review and link to a tracked issue when fixing a reported error, a commit that redefines a domain term also changes the glossary, and a new convention is written in the one conventions document.

## Rules: decisions and trade-offs

### 24. Count every cost of every option

SWE at Google compares options by every cost they impose: money, people, opportunity, wider effects on society, and lost focus, while allowing for the pull of the status quo. Leaving out hidden costs makes the apparently cheaper option look better than it is. [SWE-T02]

- **Do:** For a build change, a new service, a new dependency or a framework, list the costs of each option, including the option of keeping things as they are. For a framework, include the cost of leaving it later (CA-T59); see [architecture](architecture.md).
- **Check:** A decision record lists the costs of each option, not only the cost of the chosen one.

### 25. Name and quantify each option's trade-offs

SWE at Google names the trade-offs of every option, measures them where possible and explains them to everyone affected, so the choice is visible and can be challenged. Philosophy of Software Design writes down two or more alternatives before committing and says why the chosen one wins. Design Patterns records consequences and rejected alternatives beside each pattern-based structure. Pragmatic Programmer, Clean Architecture and Tidy First judge options mainly by how easily they will change. [SWE-T35, POSD-P5, GOF-P5, PP-T68, CA-P7, TF-P5]

- **Do:** In the design note or PR description, list at least two options, the trade-offs of each with measurements where you have them, the modules a likely future change would touch under each, and why the chosen one wins. For comparing interface options specifically, see [module-design](module-design.md).
- **Not when:** The principles alone may not identify one best design (POSD-P5).
- **Check:** A design document lists the trade-offs of each option, not only the chosen one.

### 26. Record each decision's reason and prefer reversible options

SWE at Google records why each decision was made, makes objective data its largest input, prefers options that can be undone, and revisits decisions on new evidence or on a schedule. Hard-to-undo decisions get more scrutiny than reversible ones. Tidy First turns that into review practice: list each irreversible change, such as sent data or a migration, for slower review, and review reversible changes lightly. [SWE-P8, TF-T31]

- **Do:** Write the reason and the evidence beside the decision, in a text file or the PR. When two options are close, pick the one you can reverse. Mark irreversible parts of a change in the PR description for extra review.
- **Not when:** Explaining the reasoning costs more than a trivial decision is worth.
- **Check:** The PR lists each irreversible change for extra review, and changes that override an existing decision explain why its original reason no longer holds.

### 27. Learn why a past decision was made before overriding it

SWE at Google learns why inherited code was built the way it is before changing it, because that code often encodes a reason no longer visible in it. When you do override an earlier decision, say why its original reason no longer holds. In review, ask the author why before judging an unusual approach wrong. [SWE-T62, SWE-P8, SWE-T36]

- **Do:** Read the decision record, commit history or ask the owner before reversing a past choice. Pin the current behavior with tests first; see [legacy-code](legacy-code.md). State in the PR why the old reason has lapsed.
- **Not when:** Code that is truly unclear or wrong still needs changing (SWE-T62), and an author's approach that is deficient warrants a better alternative (SWE-T36).
- **Check:** Changes to inherited code carry tests of their behavior, and an override states why the old reason no longer holds.

## Rules: ownership and teamwork

### 28. Own the results you accept

Pragmatic Programmer asks you to own the outcomes of work you take on. When you make a mistake, say so plainly and offer ways to recover rather than excuses. [PP-P1]

- **Do:** Report a mistake you made together with the recovery options. When you report a problem you are not fixing, pair it with a next step.
- **Not when:** Decline work whose risks or ethics you cannot accept.
- **Check:** Status notes pair each reported problem with a next step.

### 29. Give every project, defect and migration a named owner

Ownership recurs across SWE at Google and Pragmatic Programmer: a long-lived project has a primary and a backup owner, each known defect has a named owner in the backlog, and each migration has an owner who moves the callers. Named owners make responsibility explicit and stop work from being forgotten. [SWE-T18, PP-T04, SWE-P7]

- **Do:** Check that the project has an owners file, that each backlog problem names an owner, and that each deprecated symbol names an owner and a milestone. Add the missing owner or ask the user who it should be.
- **Not when:** The owners file at project creation is for long-lived repositories, services and libraries (SWE-T18, SWE-P1).
- **Check:** The owners file names two owners, backlog items for known problems are owned, and deprecated symbols have an owner and a removal milestone.

### 30. Ask for a second person on hard problems

On a tricky or unfamiliar problem, Pragmatic Programmer asks for someone to review or pair with, because a second view catches what one developer misses. [PP-T54]

- **Do:** When a problem is hard, new to the team or being solved in isolation, ask the user for a reviewer or pairing partner, and note the session in the PR or commit trailers. Review practice itself is in [change-workflow](change-workflow.md).
- **Check:** Pairing or review sessions appear in PR notes or commit trailers.

### 31. Timebox a task you keep avoiding, then decide

Pragmatic Programmer gives a task you keep putting off a fixed time box, measured in minutes or attempts, then decides whether to keep or discard what was done. The box makes an intimidating task finite. [PP-T55]

- **Do:** State the box before starting, stop when it runs out, and either keep the work in a branch or delete it, saying which.
- **Check:** The branch or files show a keep-or-delete decision after the time box.

## Playbooks

### When you start a new project or service
1. Check whether a non-software option meets the need, list the alternatives you considered, and ask the user before building if one does. [PP-T69]
2. Decide whether others or later work will depend on the code, which sets how much of the rest applies. [SWE-P1]
3. Make the first commit a skeleton that builds and runs, with the build and run steps scripted. [PP-T01, PP-T18]
4. For long-lived code, add an owners file with two named owners, a CI configuration and a README that states support and lifespan. [SWE-T18, SWE-P1]
5. Commit build, pipeline and deployment definitions, and read credentials from external configuration. [PP-T17, RI-T34, PP-T35]
6. Build one feature as a thin end-to-end path through every layer. [PP-T02]
7. Continue in small slices, riskiest first, demoing each one and recording refined requirements in their tickets. [PP-T24, PP-T23, PP-P9]
8. Let the component structure follow the classes you actually write, rather than a plan made before the code. [CA-T32, CA-T27]

### When you pick up a feature request
1. Check whether a non-software option meets the need, and ask the user before building if one does. [PP-T69]
2. Ask about edge cases, and record each question and answer in the ticket. [PP-T53]
3. Scope the work to what current requirements and callers need. [PP-T71]
4. If one unknown part threatens the design, prototype it in disposable code first (next playbook). [PP-T03]
5. Deliver the feature as end-to-end slices, show each one, and adjust the next slice to the feedback. [PP-T24, PP-T23]
6. Report progress as use cases working end to end or not started. [PP-T25]
7. Update docs and glossary in the same change as the behavior. [SWE-T33, DDD-T11]

### When a risky or unknown part affects the design
1. Write down the single question the prototype must answer. [PP-T03]
2. If the task feels daunting, set a time box in minutes or attempts. [PP-T55]
3. Build the prototype outside the production tree or on a spike branch. [PP-T03, TF-T35]
4. If the problem is hard or unfamiliar, ask the user for a pairing partner or reviewer. [PP-T54]
5. Record the answer and the trade-offs of the options it revealed. [SWE-T35, PP-T19]
6. Make the keep-or-delete decision explicit, then build the chosen design cleanly in production code. [PP-T55, PP-T03]

### When you find a known problem you cannot fix in this change
1. If the problem sits in code your change touches and the fix is possible now, fix it, in its own structural commit. [PP-P1, POSD-T18, TF-P1]
2. If you are fixing a bug under pressure, keep the fix diff to the defect's own change. [PP-T72]
3. If the damage needs containing now, add a visible stopgap such as a not-implemented error. [PP-T05]
4. Add a named, owned backlog item, or list the follow-up with an owner in the change description. [PP-T04, POSD-T19]
5. Report the problem to the user with a proposed next step. [PP-P1]

### When you add or upgrade a dependency
1. For a new dependency or framework, list the costs of each option, including staying as you are and the cost of leaving later. [SWE-T02, CA-T59]
2. For a generic capability, prefer a maintained library or product unless integrating it costs more than building the feature. [DDD-T05]
3. Pin the dependency to a named release. [CA-T29]
4. Upgrade in a small change of its own, and script any upgrade step you repeat. [SWE-T01]
5. Recheck the assumptions recorded at call sites against the new release, and add a comment or test for any new one. [PP-T67]
6. Run the tests the upgrade can affect, and keep upgrading regularly for long-lived code. [SWE-T32, SWE-T01, SWE-P1]

### When you deprecate and remove an old API or system
1. Confirm the old system is demonstrably obsolete and that a comparable replacement exists. [SWE-P7]
2. Ship the replacement first, and give the deprecation an owner and a removal milestone. [SWE-T28, SWE-P7]
3. Mark the old symbol deprecated, and keep a forwarder for published functions whose callers you do not control. [REF-T18]
4. Add a review check that flags new uses and points to the replacement, and make it blocking once the deprecation is compulsory. [SWE-T30]
5. Find callers with static analysis and production logging, and migrate them with generated, sharded changes applied to trunk. [SWE-T29, SWE-T03, SWE-T23]
6. If the component is shared, publish a version and release notes naming the change and the affected dependents. [CA-T25]
7. Delete the old code once the search and the logs show no remaining callers. [SWE-T29, SWE-T04]

### When you make or change a technical decision
1. If it overrides an earlier decision, learn why the original was made. [SWE-T62, SWE-P8]
2. Write down at least two options. [POSD-P5]
3. List every cost of each option, allowing for status quo bias. [SWE-T02]
4. Name the trade-offs of each option, with measurements where possible, including the modules a likely change would touch. [SWE-T35, PP-T68]
5. Prefer the reversible option when the options are close, and flag irreversible parts for slower review. [SWE-P8, TF-T31]
6. Record the reason and the evidence in plain text in the repository or PR, and explain it to everyone affected. [SWE-P8, PP-T19, SWE-T35]

## Where the books disagree

### Thin production path or throwaway prototype?
- **Pragmatic Programmer (tracer path):** Build one feature through every layer to production standard and keep it. [PP-T02]
- **Pragmatic Programmer and Tidy First (prototype):** Build disposable code to answer one risky question, or spike a change that is costly to undo, then throw it away. [PP-T03, TF-T35]
- **Decide:** If the uncertainty is how the layers, libraries or environment fit together, or the requirements are vague, build the kept end-to-end path. If one specific component, data format or performance concern is unproven, or the structure change would be costly to undo, prototype it outside the production tree and rebuild it cleanly. [PP-T02, PP-T03, TF-T35]

### Hold dependencies still or keep them moving?
- **Clean Architecture:** Pin each dependency to a named release and adopt new releases on your own schedule, so other teams' work does not break your build. [CA-T29]
- **SWE at Google:** Upgrade in small, regular increments, because deferred upgrades grow larger and riskier. [SWE-T01]
- **Learning DDD:** Pin maintained versions and upgrade regularly. [DDD-T05]
- **Decide:** These combine rather than conflict. Pin a named release, and for long-lived code upgrade in small, regular increments on a schedule your team sets, each in its own change. Skip an upgrade only when it costs more than it returns over the code's lifespan, and code that will never be upgraded may take any available version. [CA-T29, SWE-T01, SWE-P1]

### Fix a known mess now or later?
- **Pragmatic Programmer, Philosophy of Software Design, Clean Code:** Repair bad code as soon as you notice it, in the change that touches it. [PP-P1, POSD-T18, CC-P6]
- **Tidy First:** Tidy only what the next change needs, and choose first, after, later or never by cost. Keep deferred messes on a Fun List. [TF-P3, TF-P4, TF-T29]
- **Pragmatic Programmer (bug fixes):** Keep a bug fix's diff to the defect's own change, with no unrelated edits. [PP-T72]
- **Decide:** If the mess is in code your change touches and the fix is possible now, fix it in a separate structural commit. Tidy First puts that commit before the behavior change when tidying first lowers the total cost or creates options worth the delay, and after it otherwise. If a deadline or an urgent bug fix blocks it, keep the diff minimal, contain any damage with a visible stopgap, and record an owned follow-up. If no pending change touches the area, list it for later or never. The books give no formula for weighing a fix's options against delay, so that call is judgment. [PP-P1, POSD-T18, TF-P4, PP-T72, PP-T05, POSD-T19]

### Should unfinished work be marked in the source?
- **Pragmatic Programmer:** Mark a stopgap visibly, for example with a not-implemented message or a named TODO. [PP-T05]
- **Clean Code:** Keep history out of source: no commented-out code, change logs, or author and ticket tags. [CC-T73]
- **Decide:** Mark live stopgap code so the temporary behavior is visible, and keep the tracking itself (owner, ticket, history) in the backlog and version control rather than as author or ticket tags in source. Pragmatic Programmer does not say what a named TODO's name is, so if the codebase already puts names or ticket IDs in TODOs, follow its convention. [PP-T05, PP-T04, CC-T73]

## Review checklist

- [ ] A new long-lived project's first commits build and run, and include an owners file with two owners and a CI configuration. [PP-T01, SWE-T18]
- [ ] Long-lived code has a README stating its support and lifespan. [SWE-P1]
- [ ] The reply or PR for a new feature lists the alternatives considered, including non-software ones. [PP-T69]
- [ ] The ticket records edge-case questions and their answers. [PP-T53]
- [ ] The change delivers something a user can exercise end to end. [PP-T24, PP-T02]
- [ ] No extension point, option or polish lacks a stated requirement or caller. [PP-T71]
- [ ] Prototype code is outside the production tree and is not promoted into it. [PP-T03]
- [ ] Known defects in touched code are fixed in the change, in a separate structural commit, or listed as an owned follow-up when a deadline blocks the fix. [PP-P1, TF-P1, POSD-T18]
- [ ] Any stopgap carries a visible temporary marker, and an owned backlog item or follow-up exists for it. [PP-T05, PP-T04, POSD-T19]
- [ ] Build, pipeline and deployment definitions are in the repository, and no credential literal is. [PP-T17, RI-T34, PP-T35]
- [ ] No new prose step list replaces something a script could do. [PP-T18, RI-T45]
- [ ] Requirements, designs and test data added are plain text. [PP-T19]
- [ ] Every dependency declaration pins a named release, with no moving latest version. [CA-T29]
- [ ] A dependency upgrade is its own small change. [SWE-T01]
- [ ] Reliance on undocumented library behavior has a comment or test at the call site. [PP-T67]
- [ ] A shared component's release bumps its version and adds release notes naming changes and dependents. [CA-T25]
- [ ] A removal follows the release that introduced its replacement, and a static search and production logs show no callers. [SWE-T28, SWE-T29]
- [ ] A deprecated symbol has an owner, a removal milestone and a review check that points to the replacement. [SWE-P7, SWE-T30]
- [ ] Docs, glossary and conventions changes ship in the same PR as the behavior they describe. [SWE-T33, DDD-T11, POSD-T32]
- [ ] The design note lists the costs and trade-offs of each option, not only the chosen one. [SWE-T02, SWE-T35]
- [ ] Irreversible changes, such as migrations or sent data, are listed in the PR for extra review. [TF-T31]
- [ ] A change that overrides an earlier decision says why the original reason no longer holds. [SWE-P8]
- [ ] Pairing or review on a hard problem is noted in the PR or commit trailers. [PP-T54]

## More entries in this area

- `PP-T26` — Name domain concepts in the domain's words: use glossary terms in types, functions and tests; see [domain-modeling](domain-modeling.md).
- `PP-T35` — Keep credentials in external configuration: applies whenever code needs keys or passwords; see [security](security.md).
- `PP-T12` — Wrap third-party APIs in your own layer: when you adopt a vendor SDK, database or service; see [module-design](module-design.md).
- `PP-T72` — Keep a bug fix's diff small: when fixing under deadline pressure; see [change-workflow](change-workflow.md).
- `SWE-T15` — Run checks at commit time: when setting up the CI a new project needs; see [change-workflow](change-workflow.md).
- `SWE-T32` — Run every test transitively affected by a change: when upgrading a shared library or dependency; see [testing](testing.md).
- `SWE-T34` — Write reference docs as comments beside declarations: when documenting a public API in source; see [readable-code](readable-code.md).
- `SWE-T37` — Record why non-obvious code exists: when a workaround or constant needs its reason kept; see [readable-code](readable-code.md).
- `CC-T72` — Document public API members with doc comments: for code other teams call, not for team-internal code.
- `CA-T45` — Stub or keep data in memory before persistence: lets the first end-to-end path run before storage exists.
- `CA-T59` — Evaluate each framework by its exit cost: when a framework is proposed; see [architecture](architecture.md).
- `DDD-T03`, `DDD-T06` — Keep core subdomains in-house, keep supporting ones simple: when deciding how much effort and who builds each part; see [domain-modeling](domain-modeling.md).
- `RI-T46` — Let old and new versions run together: when a migration rolls out gradually; see [production-reliability](production-reliability.md).
- `DDIA-P5` — Keep data and APIs readable in both directions: when a shared component's change reaches callers you do not control; see [data-systems](data-systems.md).
