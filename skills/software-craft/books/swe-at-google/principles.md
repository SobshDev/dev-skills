# Software Engineering at Google — Titus Winters, Tom Manshreck & Hyrum Wright (2020)

## Summary
The book treats software engineering as programming integrated over time. Code must stay changeable as libraries, platforms, teams and requirements move. Its practices favor small, frequent, automated change, tests that run on every change, explicit ownership, and removal of obsolete code. The right amount of process depends on how long code lives and how many people depend on it.

## Principles

### SWE-P1: Plan every choice around code lifespan
Practices should match how long code must live. Long-lived code needs upgrades, owners and documentation.

- **Apply:** Before choosing tests, docs, dependencies or forks, decide whether others or later work will depend on the code, and treat it as long-lived if so.
- **Limits:** Short-lived or narrow code may fork or skip heavy practices, but long-lived forks still need security fixes. Code never upgraded may take any available dependency.
- **Check:** Long-lived code has an owner file, a test suite, and a README stating its support and lifespan.
- **See:** SWE-T01, SWE-T02, SWE-T18
- **Source:** ch. 1, 14, 15, 21

### SWE-P2: Make change small, frequent and automated
Large batches are costly to upgrade, review and debug, while small steps stay cheap to check and undo.

- **Apply:** Split work into small increments, split large changes into shards that each land alone, and use tooling for mechanical edits.
- **Limits:** Some large new features cannot be split well.
- **Check:** Recent commits each address one concern, and mechanical edits come from a script or tool.
- **See:** SWE-T03, SWE-T14, SWE-T21
- **Source:** ch. 1, 22

### SWE-P3: Run checks early and on every change
Defects are cheaper to fix the earlier they are found, and several imperfect checks catch more than one.

- **Apply:** Run relevant tests, analyzers and the formatter before sharing a change, and on each submit. Shorten the delay to test feedback.
- **Limits:** Expensive suites belong after submit or at release, not at every presubmit.
- **Check:** Presubmit runs fast tests, and post-submit or release runs the expensive ones.
- **See:** SWE-T15, SWE-T16, SWE-T26
- **Source:** ch. 1, 11, 23

### SWE-P4: Keep most tests small, hermetic and deterministic
Most tests should be small, fast and free of network, clock or ordering dependence, since larger tests cost more to keep stable.

- **Apply:** Write most tests small, and reserve larger tests for behavior that needs real components.
- **Limits:** Larger tests remain necessary for behavior that small tests cannot reach.
- **Check:** Tests carry size labels, small tests avoid sleeps and real I/O, and each test builds its own state.
- **See:** SWE-T05, SWE-T06, SWE-T09
- **Source:** ch. 11, 12, 14

### SWE-P5: Test observable behavior through public interfaces
Tests should check outcomes through public interfaces, as every observable behavior gets depended on. Treat ordering, timing or log format changes as breaking, even if the signature is unchanged.

- **Apply:** Call code through its public API, assert on results or state, and test every behavior you want to keep.
- **Limits:** Interaction checks remain useful where a call is itself the behavior, such as caching reducing reads. Many tests legitimately combine both kinds of check.
- **Check:** Tests import the public API, and assertions check results or state rather than calls made.
- **See:** SWE-T07, SWE-T10, SWE-T11
- **Source:** ch. 1, 11, 12, 14, 21

### SWE-P6: Integrate on trunk and separate deploy from release
Long-lived branches delay integration and hide conflicts. A runtime switch lets unfinished work land on trunk, separating deploy from release.

- **Apply:** Commit small changes to trunk, guard unfinished features with a flag, and rely on tests, CI and review, not dev branches.
- **Limits:** Small organizations may keep a few branches. Flags do not hide sensitive features, since code can be scraped, and some add too much complexity.
- **Check:** Unfinished features sit behind a flag, and feature branches merge into trunk regularly rather than staying open.
- **See:** SWE-T19, SWE-T20, SWE-T23
- **Source:** ch. 1, 16, 24

### SWE-P7: Migrate and remove obsolete code with owners
Removal needs a replacement and an owner for each migration. Compulsory deprecations need a deadline and enforcement.

- **Apply:** Start removal only after a replacement exists, and have the owner move the callers or keep the old interface working.
- **Limits:** Deprecate only systems that are demonstrably obsolete and have a comparable replacement.
- **Check:** A deprecated symbol has an owner and removal milestone, and compulsory deprecations add a presubmit check blocking new uses (see SWE-T30).
- **See:** SWE-T28, SWE-T29, SWE-T30
- **Source:** ch. 1, 15, 22

### SWE-P8: Decide with evidence and keep decisions reversible
Each decision should state its reasons and costs. Hard-to-undo decisions need more scrutiny than reversible ones.

- **Apply:** Record each decision's reason, make objective data its largest input, prefer reversible options, and revisit on new evidence or a schedule.
- **Limits:** Explaining reasoning costs more than a trivial decision is worth.
- **Check:** Changes that override an existing decision explain why its original reason no longer holds.
- **See:** SWE-T02, SWE-T35
- **Source:** ch. 1, 5, 6
