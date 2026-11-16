# Clean Code — Robert C. Martin (2nd edition, 2025)

## Summary
Clean Code argues that software is written for the people who will read and change it, and that messy code makes every later change slower and riskier. It gives small disciplines for names, functions, comments, classes, tests, concurrency, and architecture, and offers them as guidelines to weigh against context. Its central claim is that cleanliness protects delivery speed over the long run. Use this layer when you write, change, or review code, especially under deadline pressure or when generated code arrives. The appendix records real disagreements about method length and test-first rules, so treat the strictest forms as defaults with known exceptions.

## Principles

### CC-P1: Write code that states its intent
Names, short units, and structure should show what code does and why. Code is read far more often than written, so readability comes first. A comment explaining unclear code marks intent the code does not express.

- **Apply:** Name each element for its purpose, and extract a named function where a comment would otherwise explain a block.
- **Limits:** Comments holding reasons that code cannot carry still belong.
- **Check:** New comments in a diff explain a reason, not a step that a clearer name could show.
- **See:** CC-T18, CC-T19
- **Source:** ch. 4 § Use Intention-Revealing Names; ch. 5 § Compensating for Failure; ch. 18 § Maximize Expression; ch. 1 § We Read More Than We Write; appendix § Comments

### CC-P2: Keep each unit to one idea and level
A function or module should express one concept at one level of abstraction, so a reader can take it in at once and follow it downward.

- **Apply:** Split a unit until each body holds one level of named steps, not helpers that restate one statement (CC-T33), and keep orchestration apart from detail.
- **Limits:** What counts as meaningful is a judgment call, and some teams allow two levels.
- **Check:** Each function in a diff holds one step at one level and calls named helpers for its detail.
- **See:** CC-T32, CC-T33, CC-T34
- **Source:** ch. 1 § Putting All This Together; ch. 7 § One Level of Abstraction per Function; ch. 10 § Extract Method Refactoring; ch. 11 § The Stepdown Rule: Once Again

### CC-P3: Make it work, then clean in small steps
The book separates making code work from making it right. Cleanup then runs in small steps, each followed by a passing test, so a failure points to the last edit.

- **Apply:** Get the behavior working first, then restructure in small steps and run the tests after each one.
- **Limits:** A deadline may justify a quick fix that bends structure, which still needs later cleanup.
- **Check:** Each cleanup is its own commit, and the commit before it passes the test command.
- **See:** CC-T01, CC-T03, CC-T04
- **Source:** ch. 1 § The Art of Clean Code?; ch. 2 § The Cleaning Process; ch. 9 § Make It Right; ch. 29 § (opening); ch. 29 § Do Your Best

### CC-P4: Keep the test suite fast and trusted
Refactoring is safe only under tests that run quickly and can be trusted. The book treats test speed as a design requirement and a passing suite as evidence, not proof.

- **Apply:** Keep the suite fast enough to rerun after each small change, and refactor only while it passes.
- **Limits:** A passing suite is strong evidence, not a formal proof of correctness.
- **Check:** Build and test time after a small edit stays within a minute or two, and cleanup commits pass without test edits.
- **See:** CC-T11, CC-T66, CC-T68
- **Source:** ch. 9 § Make It Right; ch. 14 § Muzzling the Devil; ch. 15 § Fast; ch. 18 § Design?; ch. 30 § Test-Driven Development et al.

### CC-P5: Point dependencies toward stable policy
A policy module holds the business rules. Those rules change for different reasons than storage, web, and UI details. The book makes every cross-boundary dependency point toward the higher-level side, so detail changes cannot disturb policy.

- **Apply:** Point each cross-boundary dependency toward the policy side, and keep policy modules free of database and framework imports.
- **Limits:** Adding interfaces everywhere adds ones nobody needs. Add one when a second implementation or an inverted dependency needs it.
- **Check:** Policy modules import no database, UI, or framework packages.
- **See:** CC-T48, CC-T51, CC-T53
- **Source:** ch. 3 § A More Significant Example; ch. 9 § Considering the Design and Architecture; ch. 19 § A Thought Experiment; ch. 19 § Stable Abstractions; ch. 25 § Conclusion; ch. 27 § The Dependency Rule

### CC-P6: Clean as part of every change
The book treats design as continuous, not a phase at the project's start. Each change alters the design, so it should leave the code slightly cleaner.

- **Apply:** Clean the code you touch in the same pull request, as small cleanup commits that follow passing tests (CC-P3).
- **Limits:** Initial sketches of the planned design still help when a project starts.
- **Check:** The pull request's cleanup touches only code that the feature change also touches.
- **See:** CC-T02, CC-T03
- **Source:** ch. 1 § The Boy Scout Rule; ch. 21 § Continuous Design; Part IV § The Oath
