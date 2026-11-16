# Making a change: steps, commits, pull requests, integration

This guide covers how to sequence any code change, from the first edit to a merged and released commit: step size, when to tidy, how to cut commits and pull requests, and how to integrate, release and roll back. The most important idea, shared by every book that covers it, is to move in small steps that each end in a verified, committed state, and to keep structure changes apart from behaviour changes.

**Read this when:** starting a feature or bug fix in existing code, deciding whether to clean up before or after a change, splitting work into commits or pull requests, a test or the build breaks after an edit, a branch has lived longer than a day, preparing a diff for review, accepting generated code, rolling back or releasing a change.

**Entry IDs** such as `WELC-T12` point to `../books/<book>/techniques.md` (T) or `principles.md` (P);
the prefix table is in [SKILL.md](../SKILL.md).

## Contents
- [Core rules](#core-rules)
- [Rules: small verified steps](#rules-small-verified-steps)
- [Rules: structure versus behaviour](#rules-structure-versus-behaviour)
- [Rules: when to tidy](#rules-when-to-tidy)
- [Rules: commits and pull requests](#rules-commits-and-pull-requests)
- [Rules: integration, release and rollback](#rules-integration-release-and-rollback)
- [Playbooks](#playbooks)
- [Where the books disagree](#where-the-books-disagree)
- [Review checklist](#review-checklist)
- [More entries in this area](#more-entries-in-this-area)

## Core rules

The rules fall into five groups: how big each step is, how structure and behaviour stay apart, when to tidy, how commits and pull requests are shaped, and how work reaches trunk and production. How to write the tests themselves is in [testing](testing.md), and how to restructure code safely is in [refactoring](refactoring.md).

## Rules: small verified steps

### 1. Take the smallest step you can verify

Break every change into steps small enough that a failure points at the last few lines you touched, and confirm each step before starting the next. Tidy First, Refactoring, TDD, Legacy Code, Pragmatic Programmer and SWE at Google all give the same reason: a small step keeps each mistake cheap to find and cheap to undo. Pragmatic Programmer adds that the rate of feedback should limit how fast you work. [TF-P2, TF-T05, REF-P1, REF-T09, TDD-P2, WELC-P2, PP-P2, PP-T06, SWE-P2]

- **Do:** Make one move, check it, then make the next. When you follow a named refactoring, follow its written steps in order. Split anything you cannot confirm quickly into increments that a test, a demo or a review can each confirm.
- **Not when:** Routine work along a path that is already clear can take larger steps [TDD-P2]. Small steps do not replace the tests that must exist before you begin, so cover untested code first, as the [legacy code](legacy-code.md) guide describes [WELC-P2]. Some large new features cannot be split well [SWE-P2].
- **Check:** Each commit in the sequence is small enough to verify on its own, and each is followed by a passing test run.

### 2. Run the tests after every small change

Run the suite after each small edit, about once a minute while coding, so a red bar stays next to the edit that caused it. Refactoring wants that suite fast and runnable with one command. [TDD-T14, REF-P2, PP-T07, WELC-T01]

- **Do:** Run the tests after each refactoring step and after each behaviour step, not only before committing.
- **Not when:** Code with no tests gives the run nothing to report, so get it under test first [WELC-T01]. TDD notes that under very high stress the habit can still break down [TDD-T14].
- **Check:** Commit history or CI records show a passing run after each small step, and one documented command runs the full suite.

### 3. Revert a broken step instead of patching over it

When a step you expected to be safe breaks a test, return to the last passing state and redo the work in smaller steps. A known passing state costs less than debugging several unverified edits, and reverting keeps the last working state instead of patching over the failures. [REF-T10, CC-T04, TDD-T05]

- **Do:** Undo only the step that broke the test and keep the edits before it [CC-T04]. Retry the same change in smaller pieces [REF-T10].
- **Not when:** If the breaking change is already small and the failure is unexplained, write a focused test for its cause instead, then retry the change against that test [TDD-T05, TDD-T47]. The [debugging](debugging.md) guide covers that investigation.
- **Check:** The working tree returns to the last passing state before the retry, and failing cleanup edits are reverted rather than patched over.

### 4. Get to green first, then clean up as its own step

Making code work and making it right are separate jobs. Reach a passing state with the quickest code that works, then restructure while every test stays green, before starting the next test. Cleanup is cheapest at that moment, because the code is still small and the new test guards it. [TDD-P3, TDD-T06, CC-P3, CC-T01, CC-T03, PP-T65]

- **Do:** Commit the passing state, then commit each cleanup step separately, running the tests after each one.
- **Not when:** If the clean implementation is obvious and takes no longer to type, write it directly [TDD-T06]. A deadline may justify a quick fix that bends the structure, but that fix still needs a later cleanup pass [CC-P3].
- **Check:** Each refactoring commit follows a commit in which all tests pass, and cleanup commits leave existing test assertions unchanged [CC-T01].

### 5. Settle design questions by running the code

When you have spent minutes reasoning about whether two designs behave the same, make the change and run the tests instead, because the run answers the question more cheaply. On a hard problem whose path is unclear, move in small concrete steps that each return runnable feedback. [TDD-T20, TDD-T21]

- **Not when:** Without tests, reasoning is the only option [TDD-T20].
- **Check:** Work on a hard change shows runnable experiments and test runs rather than long stretches of untested code, and notes or commits record the run that settled the question.

### 6. Keep a work list and park side ideas on it

Write the planned tests and open design questions on a visible list, and mark each one started or finished. When a new idea appears mid-task, add it to the list and return to the current step. Acting on the tangent would mix unrelated work into the change and blur which edit caused a failure. [TDD-T25, TDD-T26]

- **Do:** Put messes you notice but will not tidy now on a list of deferred tidyings, which Tidy First calls the Fun List [TF-T29].
- **Not when:** A tangent that is a breakthrough the current work depends on may be followed now [TDD-T26]. A reported defect is not a side idea, and it gets its own failing test, as the [testing](testing.md) guide describes [TDD-T42].
- **Check:** The new item appears on the list, and the current diff contains no unrelated fix.

### 7. Build the safety net before a risky change

Before a change that seems too risky to attempt, first build the tests and modules that make it safe, so the large change can proceed without losing track of what it broke. Before a structural change that is costly to undo, such as extracting a separate service, prove it in a prototype or spike, because a spike is cheap to discard and a permanent split is not. [TDD-T22, TF-T35]

- **Do:** Write tests covering the code the change will modify before the change starts [TDD-T22, TDD-T45]. For untested code, follow the [legacy code](legacy-code.md) guide.
- **Not when:** Stable parts of the system may keep looser tests [TDD-T22].
- **Check:** Tests covering the code under change exist before the change begins, and a prototype branch or spike exists before a costly split lands.

## Rules: structure versus behaviour

### 8. Keep structure changes and behaviour changes in separate commits

A structural change keeps every computed result the same, and a behaviour change alters results. Tidy First, Refactoring, TDD, Pragmatic Programmer and Legacy Code all keep the two in separate commits. A mixed diff cannot be checked by the existing tests, it hides which edit broke which test, and it is harder to review on its own terms. [TF-P1, REF-P1, REF-T12, TDD-T07, PP-T44, WELC-P3]

- **Do:** Work in one mode at a time and label each commit as structure or behaviour. Reorder code in commits that only move lines [TF-T10]. If you spot a bug while restructuring, leave it in place and fix it later in its own behaviour commit [REF-P1].
- **Not when:** Structural changes can still change performance, so they need their own performance checks [WELC-P3]. If no test covers the behaviour, a change to it cannot be checked as a refactoring, so add tests first [TDD-T07].
- **Check:** Structure-only commits change no computed result, add no feature, and leave existing test files unchanged except where a signature changed [REF-T82, SWE-T60].

```text
c1  tidy: move parseRate next to its only caller       (structure)
c2  tidy: extract RateTable from Billing               (structure)
c3  feat: apply regional rates, with tests             (behaviour)
c4  tidy: inline the now-trivial Billing.lookup        (structure)
```

The sequence above tidies first where the structure blocked the feature, then tidies after it, and no commit mixes the two kinds of change [TF-T01, TF-T03, TF-P1].

### 9. Give tidyings their own pull request where the workflow allows

Tidy First puts tidyings in a pull request of their own, and opens a new one each time the work switches back to behaviour, so structure stays visibly distinct from behaviour at review. Clean Code prefers cleanup inside the feature's pull request, so see [the tension below](#do-tidyings-go-in-their-own-pull-request). [TF-T23, CC-P6]

- **Not when:** If the project has no pull-request workflow, separate commits do the same job [TF-T23].
- **Check:** A tidying pull request contains no change to program behaviour.

### 10. Untangle mixed work instead of trusting the green bar

If about an hour of mixed tidying and behaviour edits has turned into a tangle, decide deliberately among three options: split it into separate changes, discard it and restart with tidying first, or ship it as it is. Restarting with tidying first may reveal more value than the tangle held. [TF-T27]

- **Do:** Choose one option explicitly. If you restart, make the tidying commits first.
- **Check:** The work ends in one of the three options, a restart puts tidyings first, and passing tests alone are never the reason for keeping tangled work.

## Rules: when to tidy

### 11. Tidy first when the structure blocks the change

When the current structure makes the planned change hard, restructure the affected code before changing behaviour. A feature forced into a structure that does not fit leaves the code harder to change, and each patch in a messy area invites more patches. When a small change needs a large effort, the design is spreading costs the change does not itself cause. [TF-T01, TF-P4, REF-T88, PP-T64, POSD-T33, CA-T05]

- **Do:** Land the structural commits first, in small steps that each pass their tests, then the behaviour commit that depends on them [PP-T64]. When a fix or feature conflicts with the current structure, restructure the affected code instead of adding special cases beside the conflict [POSD-T33]. Plan effort by the size of the change itself, and treat a mismatch as a design problem [CA-T05].
- **Not when:** Skip tidying that would not ease the planned change [TF-T01]. A very small feature does not justify a large restructuring, although small preparatory changes still belong [REF-T88]. Keep the old design when the schedule impact outweighs its cost [PP-T64]. If deadlines or incompatible teams make the refactoring impractical, use a nearly as clean alternative or schedule the cleanup [POSD-T33]. Full independence from the shape of the existing system is impractical, so aim for a practical degree of it [CA-T05].
- **Check:** A structural commit touching the blocking code lands before the behaviour commit that needs it, and the diff restructures the code instead of adding special cases beside it.

### 12. Tidy after when the change must ship first

When the code is workable, the change delivers value now, and tidying first would not lower the total cost, make the behaviour change first and tidy the same area right after it. Shipping value sooner outweighs optional tidying, and waiting can make the tidying cost more. [TF-T03, TF-P4]

- **Not when:** Messy code that blocks the change calls for tidying first (rule 11). Tidying that would take far longer than the change itself is not worth doing now [TF-T03].
- **Check:** A tidying commit in the same file follows the behaviour commit, with a comparable diff size.

### 13. Fix flaws you uncover, or record them with an owner

When a change exposes a design flaw or a mess in the code it touches, fix the structure in the same change rather than wrapping it. Small fixes made during changes stop complexity from piling up, and every later change in that area would otherwise pay for the mess again. [CC-P6, CC-T02, POSD-P7, POSD-T18, POSD-T19]

- **Do:** Clean the code you touch as small cleanup commits that follow passing tests [CC-P6]. Make one small design improvement in each area a change touches [POSD-P7]. Treat cleanup as scheduled work with an owner, and POSD suggests reserving about 10 to 20 percent of development time for it [POSD-T19].
- **Not when:** Leave code that no current change touches alone for now [CC-T02]. If a deadline blocks the fix, record the cleanup as a follow-up, which still needs a later pass [POSD-T18, CC-T02]. Initial sketches of a planned design still help when a project starts [CC-P6].
- **Check:** Cleanup touches only code the change also touches, the diff holds at most one unrelated cleanup [POSD-P7], and cleanup left undone is listed as a follow-up with an owner [POSD-T19].

### 14. Tidy only what the next change needs, inside a set boundary

Each tidying should serve a pending change, a current confusion or a listed deferred mess, not an open batch or a speculative benefit. Choose only the few tidyings the problem needs, decide in advance how far the tidying will go, and stop once the requested change can be made. Growing design work delays the behaviour the user asked for. [TF-P3, TF-T02, TF-T16, TF-T26]

- **Do:** Name in each commit message the tidyings used and what they serve. Keep each tidying stretch to about an hour before the behaviour change [TF-T26].
- **Not when:** Very messy code can justify a longer stretch of tidying, though only briefly [TF-T26]. When no behaviour change waits on the code, rule 15 decides between later and never [TF-P3].
- **Check:** The pull request or commit messages state the tidying scope and what each tidying serves, the diff holds only those tidyings, and the behaviour change follows within about an hour.

### 15. Leave static code alone, and tidy code you must understand

Leave an area untidied when it will never need a behaviour change or when tidying it would teach nothing, because such tidying costs effort and never pays back. Do tidy code you are reading to understand it when tidying would make it clearer or expose structure the mess hides. [TF-T28, TF-T30, TF-P4]

- **Do:** For an area that will change later but has no pending change now, work from the Fun List in spare time [TF-T29].
- **Not when:** An area is only safe to skip if it really will not change, and Tidy First notes that later changes are rare only for truly static systems [TF-T28]. A pending change in the area makes this a first-or-after choice instead [TF-T29].
- **Check:** Tidying commits in an area with no pending change cite a Fun List item or a learning purpose, contain no behaviour change, and the pull request says what became clear.

### 16. Start new design with the smallest step that gives feedback

When one class of features has become hard to add in an area, add only the smallest design change that starts the feedback loop, then follow it with a feature change. Keep each design step small and safe enough to undo, so that no design step gets skipped as too costly. [TF-T04, TF-T05]

- **Not when:** Choosing when to start needs judgment, since Tidy First gives no fixed rule for the moment [TF-T04].
- **Check:** The first design change is small, its commit message names it, and a feature change in the same area follows it.

## Rules: commits and pull requests

### 17. Commit every passing step and keep every commit green

Commit each step once its tests pass, so that every commit builds, runs and marks a safe point to stop or return to. Before code goes into a shared branch, every test must pass, because a red check-in breaks the work of everyone who integrates with it. [REF-T11, TDD-T15, TDD-P2]

- **Not when:** A solo session may end on a deliberately failing test until it resumes, but a shared check-in may not [TDD-T15].
- **Check:** The log holds one building, passing commit per step, and each commit on a shared branch passes the full suite.

### 18. Keep each change to one concern and about 200 lines

Limit each hand-written change to one issue and its tests, about 200 changed lines or fewer, and keep it atomic so it can be rolled back without undoing unrelated work. Small pull requests are easier to review, and each one should carry a test or demo that confirms it. [SWE-T14, SWE-P2, PP-P2, PP-T06]

- **Not when:** Tool-generated changes follow rule 20 instead [SWE-T14]. A large feature that cannot be split well goes behind a flag, or onto a branch if flags would add too much complexity [SWE-T14, SWE-P6].
- **Check:** The diff addresses one stated problem, and every file change serves that problem.

### 19. Keep a bug fix to the defect's own change

Change only what the defect requires, with no hacks, dead code or unrelated edits. Under deadline pressure, extra workarounds and sprawling edits leave messes and break unrelated behaviour. Any restructuring the fix needs goes in separate commits (rule 8). [PP-T72, REF-P1]

- **Do:** Start with a test that fails because of the defect, as the [testing](testing.md) and [debugging](debugging.md) guides describe [PP-T20].
- **Check:** The diff adds no workaround, dead code or unrelated edit beyond the fix, or the pull request explains why more modules changed.

### 20. Generate mechanical edits with a tool, and shard them

When a repeated edit touches hundreds of files, generate it with a tool rather than by hand, using syntax-aware transforms for big edits and text tools for small ones. Split the output into independent shards that each land alone. Generate a broad rename or restructuring against trunk, so it does not chase every developer's unsubmitted work. [SWE-T03, SWE-T23, SWE-P2]

- **Do:** Record the tool input. Regenerate a rejected shard instead of patching it by hand. For renames and extractions inside a codebase, use the automated refactoring tool, as the [refactoring](refactoring.md) guide describes [TF-T18].
- **Not when:** The threshold falls below hundreds of files when the maintainers know the tools well [SWE-T03]. A very large automated sweep ships alone and quickly [TF-T18].
- **Check:** The change comes from a recorded tool input, is generated against trunk, and carries no hand edits inside generated shards.

### 21. Move callers over one at a time, and keep old callers working

Before changing behaviour that users or other systems already rely on, check backward compatibility and plan the migration, because production stability depends on that behaviour. Add the new form beside the old one, convert callers one at a time, and remove the old form only when no caller uses it. During a rolling deployment, old and new versions run at the same time, so code, data and APIs must work for both, in both directions. [TF-T37, TF-T25, REF-T17, RI-T46, DDIA-P5]

- **Do:** Keep the old and new forms working together while callers move [REF-T17]. Compatibility of stored data and APIs is in [data systems](data-systems.md), and rolling deployments are in [production reliability](production-reliability.md).
- **Not when:** When automated rewrite tools can convert every caller at once, use them instead [TF-T25]. Callers you control can be updated together, while published functions keep a deprecated forwarder, and some interfaces must stay forever [REF-T18]. Clients outside your control may never upgrade, so their old requests must keep working [DDIA-P5].
- **Check:** The change includes compatibility handling or a migration for existing callers, and the number of callers of the old form falls with each commit until it reaches zero.

### 22. Read the whole diff before committing and before review

Scan every change in a commit before committing it, and read the full change again before requesting review. Leftover debugging code, unfinished placeholders and stale documentation survive unless someone checks the whole change. [SWE-T63, POSD-T54, CC-T73]

- **Do:** Confirm the documentation reflects each change [POSD-T54]. Remove commented-out code and history comments before committing [CC-T73].
- **Check:** The diff contains no leftover debugging code, no unfinished placeholder, no unresolved TODO it introduced, and no commented-out code.

### 23. Accept generated code only once you can judge it

Responsibility for LLM-generated code stays with the person who accepts it, so accept a generated change only after you can evaluate it yourself. [CC-T76]

- **Do:** Evaluate the generated change yourself, and cover the cases you examined with tests.
- **Check:** Generated changes arrive with tests covering the cases the reviewer examined.

### 24. Match review effort to how hard a change is to undo

Flag irreversible changes, such as data sent to another system or a migration, for slower review, and review reversible changes lightly. Review effort should follow the cost of reversing the change, and hard-to-undo decisions deserve more scrutiny than reversible ones. [TF-T31, SWE-P8]

- **Do:** List each irreversible edit in the pull request description, and prototype costly structural splits first (rule 7) [TF-T35].
- **Check:** The pull request lists every irreversible change for extra review.

### 25. Ask why before calling an approach wrong

When you review a change whose approach differs from what you would have written, ask the author for the reason first, and suggest an alternative only when it is a real improvement. The author may have a reason the diff alone does not show. Broader review practice is in [project and team](project-and-team.md). [SWE-T36]

- **Not when:** An approach that is actually deficient warrants proposing the better alternative [SWE-T36].
- **Check:** Review comments on an unusual approach ask a question before proposing a replacement.

## Rules: integration, release and rollback

### 26. Integrate with trunk at least daily

Merge your work into the mainline within hours, or at most a day, and keep branches short-lived. Long-lived branches delay integration, hide conflicts, and make restructuring collide with other people's work, while small merges stay trivial. TDD aims to integrate working code every fifteen to thirty minutes. [REF-T13, CC-T70, SWE-P6, TDD-P7]

- **Do:** Pull the mainline into your branch and push your result back at least once a day [REF-T13].
- **Not when:** A project whose documented policy allows longer-lived branches follows that policy [REF-T13]. Small organizations may keep a few branches [SWE-P6].
- **Check:** No feature branch has gone more than a day without merging into trunk, and pushes arrive several times a day.

### 27. Land unfinished work behind a flag

Commit unfinished features to trunk behind a runtime switch, so deploying code is separate from releasing a feature. Keep flag values in dynamic configuration, because turning a flag off is faster and safer than rolling back a release. [SWE-P6, SWE-T19, PP-T63]

- **Not when:** A flag does not hide a sensitive feature, since shipped code can be scraped, and some flags add too much complexity [SWE-P6]. Static settings that never change stay in version control with the code [SWE-T19]. Do not switch on diagnostics where end users or unauthorized people could see them [PP-T63].
- **Check:** Unfinished features sit behind a flag, and changing a flag value needs no code deployment.

### 28. Run the project's checks before sharing and on every push

Run the project's listed checks, such as tests, analyzers and the formatter, before a change goes to review or lands, and let continuous integration run the full build and tests on every push. Defects cost less the earlier they are found, several imperfect checks catch more than one, and a problem then surfaces on the change that caused it. [SWE-P3, SWE-T15, CC-T68, SWE-T16, SWE-T17]

- **Do:** Make analyzer categories that are reliable enough block the commit [SWE-T16]. Configure review-time analyzers to report mainly on the lines the change touches [SWE-T17].
- **Not when:** Expensive, slow or unstable suites run after submit or at release rather than at every presubmit [SWE-P3, SWE-T15], as discussed in [the tension below](#which-checks-must-pass-before-a-change-lands). Do not turn on a blocking check while violations of it remain, and clean them up first [SWE-T16]. Important existing issues, such as security problems, are worth reporting even in untouched code [SWE-T17].
- **Check:** Commit hooks or presubmit jobs run the listed checks, the contributing document names them, CI triggers on every push, and blocking categories fail the build.

### 29. Measure the feedback loop and shorten it

Record how long building, testing and deploying take after a small edit, and shorten whichever step is slow. Long loops push developers into bigger and riskier batches. [CC-T66, TDD-P7, CC-P4]

- **Do:** Keep build and test after a small edit within a minute or two [CC-T66, CC-P4], and the full suite under about ten minutes [TDD-P7].
- **Check:** Build and test timings are recorded per change.

### 30. Fix a broken build before any other work

When the continuous build or the acceptance suite fails after a push, repair it before making any other change. A red main line blocks everyone's integration. [CC-T67, TDD-T15]

- **Do:** Either fix the failure or revert the change that caused it (rule 32) [SWE-T31].
- **Check:** The fix or revert lands before any further feature commit on the branch.

### 31. Do not disable a failing test to get green

Fix a failing test rather than skipping, ignoring or deleting it to make the build pass. A disabled test stops guarding its behaviour and hides the defect its failure was reporting. [CC-T69, TDD-T15, PP-T73]

- **Not when:** Clean Code allows disabling a slow or broken test when a message states why, but not an intermittent threaded test, which it treats as a probable threading defect [CC-T69, CC-T60]. Pragmatic Programmer allows removing a test on purpose and asks for an open ticket on any skipped test [PP-T73]. See [the tension below](#may-a-failing-test-be-disabled).
- **Check:** The diff adds no skip, ignore or disable marker without a stated reason and an open ticket, and no commented-out test.

### 32. Roll back the culprit before fixing forward

Once a change is confirmed as the cause of a production or test failure, revert it first to restore known behaviour, and work out the real fix afterwards. When a batch of changes fails and the cause is unclear, rerun the tests on each change alone or binary-search the batch to find the culprit. Atomic, single-concern changes (rule 18) let a revert remove the culprit without undoing unrelated work. [SWE-T31, SWE-T27, PP-T22, SWE-T14]

- **Not when:** If the revert does not apply cleanly to the mainline, fix forward, accepting that this is riskier [SWE-T31]. Isolating changes one at a time does not work when they are broad, change behaviour, or are likely to interact [SWE-T27].
- **Check:** The revert applies cleanly to the current mainline, and the build log names the change that failed in isolation.

### 33. Release small batches built only from validated commits

Ship small batches on a short, regular cadence, since smaller batches tend to have fewer defects and are faster to diagnose. Cut each release candidate from the latest change that passed the continuous build, because releasing unverified head can ship code no test ever ran against. [SWE-T21, SWE-T22, RI-P7]

- **Do:** Retest a cherry-picked fix before it ships [SWE-T22]. For staged rollouts, canaries and schema ordering, follow [production reliability](production-reliability.md) [SWE-T20, RI-P7].
- **Not when:** Client apps whose users dislike frequent updates and pay data costs for each one may release less often [SWE-T21]. An emergency push may cut from true head and run a minimal test set [SWE-T22].
- **Check:** The release pipeline records the commit that passed the build, and release records show short intervals between small releases.

## Playbooks

### When you add a feature to existing code
1. Read the area and write the planned tests on a list, adding side ideas to it as they appear. [TDD-T25, TDD-T26]
2. Check that tests cover the code you will change, and add them first where they are missing. [TDD-T22, TDD-T45]
3. Decide the tidying timing: first if the structure blocks the feature, after if the code is workable and the feature should ship now, and skip any tidying the feature does not need. [TF-P4, TF-T01, TF-T03, REF-T88, TF-P3]
4. If tidying first, set its boundary, make structure-only commits that each pass the tests, and stop within about an hour. Open them as their own pull request if the workflow allows. [TF-T16, TF-T26, TF-T23, REF-T11]
5. Make the behaviour change in small steps, with tests that exercise it, running the tests after each step and committing each green state. [TDD-P2, TDD-T14, REF-T11, SWE-T56]
6. Once green, clean the new code in separate commits, limited to code the change touched. [TDD-P3, PP-T65, CC-P6]
7. If callers already depend on the behaviour, add compatibility handling and move callers one at a time. [TF-T37, TF-T25]
8. Read the whole diff, push, let CI run, and merge into trunk the same day, with unfinished parts behind a flag. [SWE-T63, CC-T68, REF-T13, SWE-P6]

### When a step, a test or the build breaks
1. If a local step broke a test, revert that step to the last passing state and retry it in smaller pieces. [REF-T10, CC-T04]
2. If the step was already small and the failure is unexplained, write a focused test for the cause before retrying. [TDD-T05, TDD-T47]
3. If the shared build is red, stop other work until it is green again. [CC-T67]
4. If a batch failed, test each change alone or bisect the range to find the culprit, unless the changes are broad, change behaviour or are likely to interact. [SWE-T27, PP-T22]
5. Once the culprit is confirmed, revert it if the revert applies cleanly, then fix forward, starting with a test that fails because of the defect. [SWE-T31, PP-T20]
6. Do not skip or disable the failing test to restore green. [CC-T69, TDD-T15, PP-T73]

### When you fix a bug
1. Reproduce the defect with a test that fails without the fix, as [debugging](debugging.md) describes. [PP-T20]
2. If the structure blocks a clean fix, restructure first in separate, behaviour-free commits. [TF-T01, POSD-T33, REF-T12]
3. Make the fix commit change only what the defect requires. [PP-T72]
4. Put other problems you notice on the list instead of fixing them in this change. [TDD-T26, REF-P1]
5. If a deadline prevents the proper fix, ship the narrow fix and record the cleanup as a follow-up with an owner. [POSD-T18, POSD-T19]
6. Read the whole diff, then push and let CI run. [SWE-T63, CC-T68]

### When a change is too large for one pull request
1. Split it into increments of about 200 lines, each confirmed by a test or demo. [PP-P2, SWE-T14]
2. Land the preparatory structural changes first, as their own pull requests where possible. [TF-T01, TF-T23]
3. Generate the mechanical parts with a tool and split them into independent shards. [SWE-T03, SWE-T23]
4. Add new interfaces beside the old ones and move callers across one at a time. [TF-T25, REF-T17]
5. Merge into trunk at least daily, with the unfinished feature behind a flag. [REF-T13, SWE-P6]
6. Prototype any split that is costly to undo, and flag irreversible steps for slower review. [TF-T35, TF-T31]
7. If the feature truly cannot be split well, put it behind a flag, or on a branch if flags would add too much complexity. [SWE-T14, SWE-P2]

### When you prepare a change for review
1. Run the project's listed checks locally before sending the change. [SWE-T15, SWE-P3]
2. Confirm that each commit builds and passes and that no commit mixes structure with behaviour. [REF-T11, REF-T12]
3. Read the whole diff for debugging code, placeholders, introduced TODOs, commented-out code and stale docs. [SWE-T63, POSD-T54, CC-T73]
4. If any part was generated, evaluate it yourself and add tests for the cases you examined. [CC-T76]
5. In the description, state the tidying scope and what each tidying serves, and list irreversible changes and compatibility handling. [TF-T16, TF-P3, TF-T31, TF-T37]

### When you release a change
1. Cut the release candidate from the latest commit that passed the continuous build. [SWE-T22]
2. Release a small batch on the regular cadence. [SWE-T21, RI-P7]
3. Expose it to a growing share of users and advance only while guardrail metrics show no harm, as [production reliability](production-reliability.md) describes. [SWE-T20]
4. If a flagged feature misbehaves, turn its flag off through dynamic configuration. [SWE-T19]
5. If a change is confirmed as the cause of a failure, revert it first and fix forward afterwards. [SWE-T31]

## Where the books disagree

### Should you tidy before the change, after it, or not at all?
- **Tidy First:** Choose among first, after, later and never. Lean toward first within limits, tidy after when the change ships value now and tidying first neither lowers cost nor creates worthwhile options, and leave alone areas that will never change. [TF-P4, TF-T01, TF-T03, TF-T28]
- **Refactoring and Pragmatic Programmer:** Restructure the code a feature touches just before adding the feature, when it almost fits but needs structural change. A very small feature does not justify a large restructuring, and the old design stays when the schedule impact outweighs its cost. [REF-T88, PP-T64]
- **Clean Code:** Clean each mess you create or find in the code a change touches, in the same pull request. Code no current change touches is left alone for now, and a deadline may defer the cleanup to a later pass. [CC-P6, CC-T02]
- **POSD:** Make one small design improvement in each area a change touches, and restructure when the change conflicts with the design. [POSD-P7, POSD-T33]
- **Decide:** If the structure blocks the change, tidy first, which Tidy First, Refactoring, Pragmatic Programmer and POSD all support [TF-T01, REF-T88, PP-T64, POSD-T33]. If the code is workable and the change should ship now, tidy right after it, and keeping that tidying in the same pull request also meets Clean Code's same-change cleanup [TF-T03, CC-P6]. If no current change touches the code, leave it or put it on the Fun List [CC-T02, TF-T28, TF-T29]. Under a deadline, defer the cleanup and record it with an owner [CC-P3, POSD-T18, POSD-T19]. Tidy First admits that weighing options against delay is a judgment call with no formula [TF-P4].

### Do tidyings go in their own pull request?
- **Tidy First:** Put tidyings in their own pull request, and open a new one at each switch back to behaviour. [TF-T23]
- **Clean Code:** Clean the code you touch in the same pull request as the feature, as small cleanup commits. [CC-P6]
- **Refactoring, Pragmatic Programmer, Legacy Code:** These ask only for separate commits. [REF-T12, PP-T44, WELC-P3]
- **Decide:** All of them require separate commits, so do that in every case [TF-P1, REF-T12]. The only deciding condition the entries give is that a project without a pull-request workflow uses separate commits [TF-T23]. Beyond that they give none, so follow the codebase's existing convention for grouping tidyings into pull requests.

### How long may work stay off trunk?
- **TDD:** Integrate working code every fifteen to thirty minutes. [TDD-P7]
- **Clean Code:** Merge within hours or a day. [CC-T70]
- **Refactoring:** Integrate at least once a day, unless the project's documented policy allows longer-lived branches. [REF-T13]
- **SWE at Google:** Commit to trunk and guard unfinished work with flags. Small organizations may keep a few branches, and a large feature that cannot be split may branch when flags add too much complexity. [SWE-P6, SWE-T14]
- **Decide:** Treat one day as the upper limit, which Refactoring and Clean Code state and TDD's shorter interval also meets, and integrate sooner whenever a step is complete and the suite is green [REF-T13, CC-T70, TDD-P7]. Exceed a day only where the project's documented policy allows longer branches, or where an unsplittable feature would need an overly complex flag [REF-T13, SWE-P6, SWE-T14].

### Which checks must pass before a change lands?
- **Clean Code and TDD:** Run the full build and tests on every push, and have every test pass before code enters a shared branch. [CC-T68, TDD-T15]
- **SWE at Google:** Gate presubmit on fast, reliable tests only, and run slow, flaky or costly suites after submit or at release. [SWE-P3, SWE-T24, SWE-T26]
- **Decide:** Keep the full suite fast enough to gate every push, and shorten it when it is not [TDD-P7, CC-T66]. When some tests are too slow, flaky or costly to gate each change, move them to post-submit or release jobs without dropping any quality check [SWE-T24, SWE-T26]. Keep a test in the gate when a broken change must be caught before it reaches the shared codebase [SWE-T26]. The [testing](testing.md) guide covers suite structure.

### May a failing test be disabled?
- **TDD:** Every test passes at a shared check-in, and a failing test is never disabled to get there. [TDD-T15]
- **Clean Code:** Never disable a test to go green, but a slow or broken test may be disabled with a message saying why, except an intermittent threaded test. [CC-T69, CC-T60]
- **Pragmatic Programmer:** Fix a failing test or remove it on purpose, never skip or delete it just to get green, and keep no skipped test without an open ticket. [PP-T73]
- **Decide:** Making the build pass is never a valid reason in any of the three [TDD-T15, CC-T69, PP-T73]. If a slow or broken test must be set aside while its fix is deferred, disable it only with a stated reason and an open ticket [CC-T69, PP-T73]. Do not do this for an intermittent failure in threaded code, which is investigated as a defect [CC-T60].

### Should a bug fix also clean the code it touches?
- **Pragmatic Programmer:** Keep the bug fix to the defect's own change, with no unrelated edits, especially under deadline pressure. [PP-T72]
- **Clean Code and POSD:** Clean the code each change touches, and fix flaws the change exposes instead of wrapping them. [CC-P6, CC-T02, POSD-P7, POSD-T18]
- **Decide:** Keep the fix commit itself limited to the defect [PP-T72, REF-P1]. Cleanup of the touched code, if any, goes in separate commits, stays inside code the fix touched, and holds at most one unrelated improvement [CC-P6, POSD-P7]. Under deadline pressure, ship the narrow fix and record the cleanup as an owned follow-up [POSD-T18, POSD-T19, CC-T02].

## Review checklist

- [ ] Each commit is small enough to verify alone and builds with a passing test run. [TF-P2, REF-T11, WELC-P2]
- [ ] No commit mixes structural edits with behaviour changes, and move-only commits contain only moved lines. [TF-P1, REF-T12, PP-T44, TF-T10]
- [ ] Structure-only commits leave existing test files unchanged except where a signature changed. [REF-T82, SWE-T60]
- [ ] Structural commits that the feature needed land before the behaviour commit. [TF-T01, REF-T88, PP-T64]
- [ ] Each tidying names what it serves, and the tidying stays within its stated scope. [TF-P3, TF-T16, TF-T02]
- [ ] Cleanup touches only code the change touches, with at most one unrelated improvement. [CC-P6, POSD-P7]
- [ ] Cleanup left undone appears as a follow-up with an owner. [POSD-T19, POSD-T18]
- [ ] A hand-written diff addresses one concern in about 200 changed lines, or a feature that cannot be split well sits behind a flag or on a branch. [SWE-T14]
- [ ] A bug-fix diff contains no workaround, dead code or unrelated edit. [PP-T72]
- [ ] Mechanical edits come from a recorded tool input generated against trunk. [SWE-T03, SWE-T23]
- [ ] Changes to behaviour in use include compatibility handling, and callers of the old form decrease toward zero. [TF-T37, TF-T25]
- [ ] The diff has no leftover debugging code, unfinished placeholders, introduced TODOs or commented-out code. [SWE-T63, POSD-T54, CC-T73]
- [ ] Generated code comes with tests for the cases the reviewer examined. [CC-T76]
- [ ] Irreversible changes, such as migrations or data sent elsewhere, are listed for slower review. [TF-T31]
- [ ] The branch has merged into trunk within the last day, or the project's policy allows longer. [REF-T13, CC-T70]
- [ ] Unfinished features are behind a flag held in dynamic configuration. [SWE-P6, SWE-T19]
- [ ] Presubmit runs the project's listed checks, and CI runs the build and tests on every push. [SWE-T15, CC-T68]
- [ ] No skip, ignore or disable marker is added without a stated reason and an open ticket. [CC-T69, PP-T73]
- [ ] A red build is fixed or reverted before any further feature commit. [CC-T67, SWE-T31]
- [ ] Release candidates are cut from a commit that passed the continuous build. [SWE-T22]
- [ ] Review comments on an unusual approach ask the author why before proposing a replacement. [SWE-T36]

## More entries in this area

- `TF-T18` — Use automated refactoring for renames and extractions: when one rename or extraction must update many call sites.
- `REF-T18` — Keep a forwarder for renamed published functions: when other teams or customers call the function you rename.
- `SWE-T20` — Roll out changes to growing user percentages: when a risky change reaches a large user base.
- `SWE-T24` — Keep presubmit limited to fast reliable tests: when choosing which suites gate each change.
- `SWE-T26` — Run costly tests after submission and at release: when a test is too slow or flaky for presubmit.
- `SWE-T56` — Block changes that add behavior without tests: when reviewing a change that alters logic or public behaviour.
- `PP-T05` — Contain defects with a visible stopgap: when the proper fix must wait and damage needs containing now.
- `PP-T22` — Bisect releases to find a regression: when code that worked earlier now fails across commits.
- `RI-T46` — Let old and new versions run together: when a rolling deployment serves both versions at once.
- `RI-T47` — Roll out the application before its data migration: when old instances cannot read migrated data.
