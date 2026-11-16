# Debugging and incidents

This guide covers finding and fixing defects in code, and handling production outages: reproducing the failure, localizing its cause, fixing it, guarding against its return, and restoring service when customers are affected. The single most important idea is to act on evidence rather than guesses. Reproduce the failure and record what you actually observe before you change any code, except during a live outage, where restoring service comes before any diagnosis.

**Read this when:** a bug report arrives, a test or build starts failing, code that worked in an earlier release now fails, a program returns a wrong value without crashing, a failure appears only sometimes or only under concurrency, a resource leak is suspected, you have been stuck on a problem for a while, a change you just made breaks tests in a way you did not expect, a production service is down or slow, or you are writing an incident runbook.

**Entry IDs** such as `WELC-T12` point to `../books/<book>/techniques.md` (T) or `principles.md` (P);
the prefix table is in [SKILL.md](../SKILL.md).

## Contents

- [Core rules](#core-rules)
- [Rules: localizing the cause](#rules-localizing-the-cause)
- [Rules: fixing and guarding](#rules-fixing-and-guarding)
- [Rules: production incidents](#rules-production-incidents)
- [Playbooks](#playbooks)
- [Where the books disagree](#where-the-books-disagree)
- [Review checklist](#review-checklist)
- [More entries in this area](#more-entries-in-this-area)

## Core rules

### 1. Reproduce the defect before forming a theory

Get the failure to happen on demand and write down the exact steps and observations before you start guessing at a cause. Pragmatic Programmer asks for recorded evidence before any hypothesis. [PP-P8]

- **Do:** Reproduce the failure, then record the steps, inputs, environment and exact output in notes, the ticket or the PR before your first edit. [PP-P8]
- **Check:** The notes or PR description record the reproduction and the suspected cause before the commit that changes code. [PP-P8]

### 2. Reduce the reproduction to one command

When a bug needs several manual steps to appear, turn those steps into a single test or script. Anyone, including a later bisect run or a reviewer, can then rerun exactly the same check. [PP-T21]

- **Do:** Write a test or a small script that drives the failing path and reports the failure. Keep it in the repository. [PP-T21]
- **Check:** The repository holds a test or script that reproduces the bug in one command. [PP-T21]

### 3. Read the complete error before editing

Read the whole error message and stack trace, and look at the location it names, before you touch any code. The full message usually names the failing place and the cause, which a quick glance and a guess would miss. [PP-T57]

- **Do:** Copy the complete message and the reported file and line into your notes, open that location, and only then plan an edit. [PP-T57]
- **Check:** The notes or commit message quote the complete error and name the location it reports, before the first edit. [PP-T57]

### 4. Suspect your own recent code first

Look at your own recent change and your own call sites before you blame the compiler, the platform or a library. Pragmatic Programmer puts your own code ahead of the platform as a suspect. When you do come to suspect external code, prove the suspicion with a small test against it rather than with argument. [PP-P8, TDD-T30]

- **Do:** Start with the most recent change to the failing path and with how your code calls the dependency. If a library still looks wrong, write a learning test that calls it directly and shows the behavior you rely on. [PP-P8, TDD-T30]
- **Do:** When the fix depends on undocumented or edge-case behavior of code you do not control, state that assumption in a comment or a test at the call site. [PP-T67]
- **Not when:** The external code is trusted and its behavior does not matter to your code, so no learning test is needed. Undocumented behavior cannot always be avoided, so document the assumption carefully instead of pretending it is not there. [TDD-T30, PP-T67]
- **Check:** A claim in the PR that a library or platform is at fault is backed by a learning test, and assumptions about uncontrolled code appear in a comment or test at the call site. [TDD-T30, PP-T67]

### 5. Keep notes on every lead

When an investigation involves many leads, write down where it started, each clue you chase and what each one showed, including the leads you drop. Writing a finding down exposes reasoning that does not hold up. [PP-T59]

- **Do:** Keep a running log in the ticket, the PR or a scratch file: starting point, lead, result, next lead. [PP-T59]
- **Check:** Notes or PR comments list the leads that were checked and the ones abandoned. [PP-T59]

## Rules: localizing the cause

### 6. Bisect the history to find a regression

When code that worked in an earlier release or commit now fails, test a version halfway between the last good one and the current one, and repeat. Each test halves the range, so few checks find the breaking change. The one-command reproduction makes each check quick to rerun. [PP-T22, PP-T21]

- **Do:** Mark the last known good and the first known bad version, then halve the range until one change remains. For a failing batch of unrelated changes, run the tests on each change alone, or binary-search the batch. [PP-T22, SWE-T27]
- **Not when:** The changes in the batch are broad, change behavior, or are likely to interact with one another, so testing them one at a time may not isolate a single culprit. [SWE-T27]
- **Check:** A bisect log, build log or the PR names the commit that introduced the failure. [PP-T22, SWE-T27]

In git, the halving looks like this, with the PP-T21 reproduction run at each step. This illustrates PP-T22:

```sh
git bisect start
git bisect bad HEAD           # current version fails
git bisect good v2.3.0        # last release known to work
./repro.sh                    # run the one-command reproduction
git bisect bad                # or: git bisect good; repeat until one commit remains
git bisect log > bisect.txt   # keep the record for the PR
git bisect reset
```

### 7. Confirm the bad value, then walk up the stack

When the program returns a wrong result without crashing, first confirm in a debugger that the value really is wrong. Then move up the call stack to the frame where it first becomes wrong. Checking the value first saves a long analysis of behavior that turns out to be correct. [PP-T58]

- **Do:** Break where the wrong output is produced, inspect the value, then step up frame by frame until you find the first frame whose result is wrong. [PP-T58]
- **Check:** Investigation notes record the observed value and name the first wrong frame. [PP-T58]

### 8. Use one parseable format for trace output

When a bug depends on timing, concurrency or the order of events, add trace statements that all share one consistent format, with a fixed prefix and labeled fields. A uniform format lets a script follow state over time, which these bugs need. When the events span several tiers, carry one request identifier through every log line and downstream call so a single request can be followed end to end. [PP-T60, RI-T70]

- **Do:** Give every trace line the same prefix and `key=value` fields, and include a correlation identifier when the request crosses process boundaries. [PP-T60, RI-T70]
- **Not when:** The bug does not depend on timing, concurrency or event order. A bad value without a crash is better confirmed in a debugger (rule 7). [PP-T60, PP-T58]
- **Check:** Trace calls in the diff share one format, and log statements and downstream calls carry the same request identifier. [PP-T60, RI-T70]

### 9. Pair resource opens with closes to find leaks

When a leak is suspected, log every open and every close of the resource with a matching identifier, then look for opens that have no close. Unmatched opens reveal leaks that code review tends to miss. [PP-T61]

- **Do:** Wrap the open and close calls so each logs the same identifier, run the failing workload, and list identifiers that were opened and never closed. [PP-T61]
- **Check:** Logging wraps the open and close calls and records a matching identifier. [PP-T61]

For the fix itself, release the resource in one owning place on every path; see [errors and contracts](errors-and-contracts.md). [PP-T38, PP-T39]

```python
log.debug("TRACE res=conn op=open id=%s", conn_id)    # PP-T60 format
...
log.debug("TRACE res=conn op=close id=%s", conn_id)
# afterwards: ids with op=open but no op=close are the leaked ones (PP-T61)
```

### 10. Treat intermittent threaded failures as real defects

A threaded test that fails once in many runs, or passes only on a rerun, is a probable threading defect, not bad luck. Calling it a one-off hides a race that comes back under load. Random timing at interleaving points can expose the rare ordering. [CC-T60, CC-T61]

- **Do:** Investigate the failure as a race. Add a single swappable timing hook at interleaving points that tests set to sleep or yield randomly, and repeat the test many times. [CC-T60, CC-T61]
- **Not when:** Manual sleep or yield calls left in production code slow it down, so bind the hook to a no-op in production builds. [CC-T61]
- **Check:** The diff does not mark an intermittent threaded test as skipped, retried or one-off. [CC-T60]

Concurrency design itself belongs to [performance and concurrency](performance-and-concurrency.md).

### 11. When a change breaks unexpectedly, shrink the step or test the cause

If a change you just made breaks tests in a way the existing tests do not explain, choose by the size of the change. A large step that is slow to diagnose should be undone and redone in smaller steps. A change that is already small calls for a focused test of the cause before you try it again. [TDD-T05, TDD-T47]

- **Do:** Revert a large failing change and redo it in small commits. For a small change, write one test that fails only on the suspected cause, then retry the change against it. [TDD-T05, TDD-T47]
- **Do:** When a test you expected to fail passes instead, find out why before trusting it. Coverage alone does not explain it. [TDD-T17]
- **Do:** When an edit in one part breaks a test in a part that does not call it, look for a hidden dependency and remove it or merge the two parts. [TDD-T49]
- **Check:** The history shows the large change reverted and redone in smaller commits, or a new test that fails only on the specific cause precedes the retry. [TDD-T05, TDD-T47]

### 12. Step away when stuck, then write the problem down

When repeated attempts make no progress, put the problem aside briefly, then write down what has been tried and the next untested idea. Stepping away lets ideas surface, and explaining the problem in writing exposes hidden assumptions. For a tricky or unfamiliar problem, a second person helps too. [PP-T56, PP-T54]

- **Do:** Stop, record the attempts so far and one next hypothesis, and ask the user for a reviewer or pairing partner when the problem is unfamiliar to the team. [PP-T56, PP-T54]
- **Check:** Problem notes record what was tried before the eventual fix, and pairing or review sessions appear in PR notes or commit trailers. [PP-T56, PP-T54]

## Rules: fixing and guarding

### 13. Write a failing test before you fix the bug

Before changing the code, write the smallest test that fails because of the defect, and watch it fail. The failing run proves both that the defect exists and that the test can catch it. After the fix it keeps the defect from returning unnoticed. Pragmatic Programmer, Refactoring and TDD ask for the failing test before the fix, and SWE at Google and Release It! ask for a regression test for each defect found. TDD also asks for a regression test that runs the whole application. [PP-T20, REF-T04, TDD-T42, SWE-T57, RI-T07]

- **Do:** Turn the reproduction or the manual check that exposed the defect into an automated test, a unit test where the project has unit tests, otherwise the one-command script. Run it red, fix the code, run it green, and keep it. Add a test at application level as well. [PP-T20, PP-T62, TDD-T42, PP-T21]
- **Do:** After diagnosing a production failure that the regular tests missed, write a test that drives that exact failing path. [RI-T07]
- **Not when:** PP-T20 assumes the bug is reproducible. If it is not yet, the first job is rule 1 and rule 2. [PP-T20]
- **Check:** The fix commit adds a test that fails without the fix, including one at application level, and the test exercises the reported failure. [PP-T20, TDD-T42, SWE-T57]

How to shape that test is covered in [testing](testing.md). If the code around the bug has no tests at all, pin its current behavior first; see [legacy code](legacy-code.md). Legacy Code notes that some dependency breaking may have to come first, that code which never changes again does not repay the test cost, and that simple code may need few tests. [WELC-P1]

### 14. Fix the root cause, not the symptom

Change the code that produces the wrong behavior, not only the place where it shows. Pragmatic Programmer asks for root-cause fixes. Release It! adds that when one defect keeps crashing servers one after another under load, limits that slow the spread leave the defect in place to start the next chain reaction. [PP-P8, RI-T16]

- **Do:** Trace the failure to the first wrong value or call (rules 6 and 7) and fix it there. After an incident where the same defect kept crashing servers one after another under load, change the code path named in the incident record, not only limit settings. [PP-P8, PP-T58, RI-T16]
- **Not when:** Partitioning does not stop a chain reaction. It only splits one chain into two that run at different rates, so it is no substitute for the code fix. [RI-T16]
- **Check:** The diff changes the code path where the fault originates, as named in the notes or incident record, not only a guard or a limit downstream. [PP-P8, RI-T16]

### 15. Remove calls that only seem to work

Trial and error can leave behind retries, sleeps or extra calls that made the symptom go away. Such calls hide the real cause. Remove each one unless a comment or a test explains why it is needed. [PP-T66]

- **Do:** Before finishing, list every call added during the investigation, and delete each one that has no documented reason or test. In tests, replace fixed sleeps with a bounded poll or an event wait. [PP-T66, SWE-T55]
- **Not when:** A retry is a designed defense with a documented reason, such as a bounded, delayed retry of documented transient errors. That is a justified call, not a workaround; see [production reliability](production-reliability.md). [PP-T66, RI-T23]
- **Check:** Each remaining retry, sleep or extra call in the diff has a documented reason or a test that needs it, and test code has no fixed sleeps. [PP-T66, SWE-T55]

### 16. Keep the bug fix's diff to the defect

A fix should contain the defect's own change and its test, with no hacks, dead code or unrelated edits. Under deadline pressure, sprawling edits leave messes and break behavior nobody meant to touch. Restructuring needed to make the fix possible goes in its own commit. [PP-T72, PP-T44]

- **Do:** Put any preparatory restructuring in a separate commit before the fix, and leave unrelated problems for their own change. [PP-T44, PP-T72]
- **Not when:** The fix truly needs changes in many modules. Then explain in the PR why each module changed. [PP-T72]
- **Check:** The diff adds no workaround, dead code or unrelated edit beyond the fix, or the PR explains why more modules changed. [PP-T72]

Commit sizing in general is covered in [change workflow](change-workflow.md).

## Rules: production incidents

### 17. Restore service before root-cause analysis

During an outage that affects customers, bring the service back first and investigate afterwards. Diagnosis while customers are down lengthens the outage they feel. When a recent change is confirmed as the cause, rolling it back is the quick way back to known behavior. [RI-T03, SWE-T31]

- **Do:** Make restoration the first step of the incident runbook: roll back the culprit if one is confirmed, or turn off a non-essential dependent feature at runtime. Any restart step names its exact unit (rule 21). [RI-T03, SWE-T31, RI-T30, RI-T35]
- **Do:** After any live configuration change, read the setting back or observe the new behavior, so you know the running component applied it. [RI-T31]
- **Not when:** Collecting postmortem data is acceptable during the outage only if it does not make the outage longer. If the rollback does not apply cleanly to mainline, the fix has to go forward, which is riskier. Settings that are read only at startup need a restart before the read-back check means anything. Do not switch a feature off with a pool limit of zero when it must stay available under heavy load, because zero disables it fully and a limit of one keeps it available. [RI-T03, SWE-T31, RI-T31, RI-T30]
- **Check:** The incident runbook lists service restoration as its first step, before log collection or analysis. [RI-T03]

### 18. Script diagnostic capture before the incident

Prepare scripts that capture thread dumps and database state, so responders do not improvise under pressure. Scripted capture that does not prolong the outage still gives the postmortem the evidence it needs. [RI-T04, RI-T03]

- **Do:** Add capture scripts to the service's runbook tooling, and make the runbook run them only where they do not delay restoration. [RI-T04]
- **Not when:** Capture that would lengthen a live outage waits until service is restored. [RI-T04, RI-T03]
- **Check:** Incident scripts collect thread dumps and database state without manual steps. [RI-T04]

Health checks and metrics that make a running system diagnosable without new code are covered in [production reliability](production-reliability.md). [RI-P5]

### 19. Read thread dumps for threads blocked in calls

When a Java application hangs or stops responding, take a thread dump and look for pool threads blocked inside calls. The dump shows which call each thread is stuck in. [RI-T05]

- **Do:** For each blocked pool thread, note the stack frame where it waits. [RI-T05]
- **Not when:** A live outage still needs service restored, so the dump waits unless a capture script takes it without delaying recovery. The entry is written for Java applications. [RI-T05, RI-T04]
- **Check:** The dump notes name each blocked pool thread and its blocking stack frame. [RI-T05]

### 20. Find the first queue that backs up

When a system slows down, look for the first queue along the request path whose depth grows. Queue depth shows where the slowdown begins, so the first backed-up queue locates the failure. Measure the time a request spends waiting in queues as well as processing, since measuring only processing time is a common mistake. [RI-T36, RI-T75]

- **Do:** Walk the request path tier by tier, compare queue depths, and start the investigation at the earliest queue that is growing. [RI-T36]
- **Check:** Monitoring exposes queue depth for each tier of the request path, and latency metrics start when a request reaches the server socket. [RI-T36, RI-T75]

### 21. Name the exact unit a restart affects

Every restart instruction should say whether it restarts a process, an instance or a whole machine. Operators act on the wording, so a vague unit changes what actually gets restarted. [RI-T35]

- **Do:** In runbooks and in requests to responders, name whether the step restarts a process, an instance or a machine. [RI-T35]
- **Check:** Runbook steps name the process, instance or machine they act on. [RI-T35]

Runbooks that operations staff can follow without the developers are part of [production reliability](production-reliability.md). [RI-T01]

## Playbooks

### When you receive a bug report

1. Reproduce the failure and record the exact steps and observations. [PP-P8]
2. If it needs several manual steps, reduce it to one test or script command. [PP-T21]
3. Read the complete error and open the location it names before editing anything. [PP-T57]
4. Start with your own recent changes and call sites. Prove any suspicion of a library with a learning test. [PP-P8, TDD-T30]
5. Write the smallest test that fails because of the defect, and watch it fail. [PP-T20, REF-T04, TDD-T42]
6. Localize the cause with the debugger, traces or bisection (see the playbooks below), keeping notes on each lead. [PP-T58, PP-T60, PP-T22, PP-T59]
7. Fix the root cause in its own small commit, with any preparatory restructuring in a separate commit. [PP-P8, PP-T72, PP-T44]
8. Run the new test green, add an application-level regression test, and keep both. [TDD-T42, SWE-T57]
9. Remove every retry, sleep or extra call from the investigation that has no reason or test. [PP-T66]

### When code that used to work now fails

1. Write the one-command reproduction. [PP-T21]
2. Mark the last good and first bad version, and bisect until one change remains. For a failing batch of independent changes, test each one alone. [PP-T22, SWE-T27]
3. If the culprit is confirmed and the failure is hurting production or the shared build, roll it back first, provided the revert applies cleanly. [SWE-T31]
4. In the culprit version, read the complete error if it crashes, or confirm the bad value in a debugger if it returns a wrong result, and walk up the stack to where it first goes wrong. [PP-T57, PP-T58]
5. Write the failing test, then fix forward on top of the restored state. [PP-T20, SWE-T31]
6. Record the bisect result in the PR. [PP-T22]

### When a program gives a wrong result without crashing

1. Confirm in a debugger that the value is really wrong, before analyzing anything. [PP-T58]
2. Walk up the call stack to the first frame whose result is wrong, and note it. [PP-T58]
3. Write a test that fails at that frame's level. [PP-T20]
4. If the wrong value depends on library behavior, pin that behavior with a learning test, or record it as a named test if it surprised you. [TDD-T30, TDD-T31]
5. Fix the first wrong frame, not the place where the value is finally shown. [PP-P8]

### When a failure is intermittent or depends on timing

1. Treat it as a probable threading or ordering defect, and do not mark the test as skipped or retried. [CC-T60, PP-T73]
2. Add trace statements in one parseable format, with a request identifier if the events cross tiers. [PP-T60, RI-T70]
3. Add a swappable timing hook at interleaving points, randomize it in tests, and rerun until the failure appears. Keep it a no-op in production. [CC-T61]
4. Script over the trace output to find the event order that precedes the failure. [PP-T60]
5. Once the order is known, write a test that forces it, fix the race, and remove any sleeps added along the way. [PP-T20, PP-T66, SWE-T55]

### When you suspect a resource leak

1. Log every open and close of the resource with a matching identifier. [PP-T61]
2. Run the workload long enough to collect unmatched opens. When a spare machine is available, a steady load running for days, with idle periods, exposes slow leaks that short runs do not. [PP-T61, RI-T09]
3. Find the code path behind the unmatched opens, and give the resource one owner that releases it on every path. [PP-T39, PP-T38]
4. Keep a test that checks the release on the failing path. [PP-T20, PP-T62]

### When a change you just made breaks tests unexpectedly

1. Judge the size of the change. If it is a large step that is slow to diagnose, revert it and redo it in smaller steps. [TDD-T05]
2. If the change is already small, write one focused test for the suspected cause and retry against it. [TDD-T47]
3. If the broken test sits in a part your edit does not call, look for a hidden dependency. [TDD-T49]
4. If a test you expected to fail passes, find out why before continuing. [TDD-T17]
5. Run the tests after each small step from here on, so the next failure is close to its cause. [TDD-T14, PP-T07]

### When production is down or degraded

1. Restore service first: roll back a confirmed culprit or turn off a non-essential dependent feature at runtime. Name the exact unit in any restart request. [RI-T03, SWE-T31, RI-T30, RI-T35]
2. Run the scripted diagnostic capture only if it does not lengthen the outage. Otherwise wait until service is back. [RI-T04, RI-T03]
3. Confirm each live configuration change took effect by reading it back or observing the behavior. [RI-T31]
4. Once service is restored, read the thread dumps for blocked pool threads, and find the first queue that backed up. [RI-T05, RI-T36]
5. Trace the failure to the defect in code, and change that code path rather than only limits. [RI-T16, PP-P8]
6. Write a test that drives the diagnosed failing path. [RI-T07]
7. Update the runbook: restoration as the first step, capture scripted, restart units named. [RI-T03, RI-T04, RI-T35]

### When you are stuck

1. Write down where you started, every lead you followed and what each showed. [PP-T59]
2. Step away briefly, then write the next untested idea. [PP-T56]
3. If the problem is unfamiliar to the team, ask the user for a second person to pair or review. [PP-T54]
4. If the investigation has grown into one large unverified change, revert to the last state that worked and take smaller steps. [TDD-T05]

## Where the books disagree

### Restore service first, or gather evidence first?

- **Release It!:** During a customer-facing outage, restore service before diagnosing, because diagnosis lengthens the outage customers feel. [RI-T03]
- **Pragmatic Programmer:** Debugging starts from evidence. Reproduce, record observations, and fix the root cause rather than the symptom. [PP-P8]
- **Release It!:** Evidence still matters for the postmortem, so capture it with prepared scripts, and read thread dumps for blocked threads. [RI-T04, RI-T05]
- **Decide:** While customers are affected by a live outage, restore first and collect only what a script can capture without lengthening the outage. Reading the thread dumps and any deeper analysis wait until service is back. Once service is restored, or when no customer-facing outage is running, follow the evidence-first rules. [RI-T03, RI-T04, RI-T05, PP-P8]

### Roll back, contain with a stopgap, or fix forward?

- **SWE at Google:** When a change is confirmed as the cause, roll it back first to restore known behavior while the fix is worked out. [SWE-T31]
- **Pragmatic Programmer:** When a proper fix must wait, contain the damage with a stub or message that is visibly marked as temporary. Otherwise make the proper fix now. [PP-T05]
- **Release It!:** Limits on spread are not a fix. A defect that keeps crashing nodes must be fixed in code. A non-essential feature can be switched off at runtime during the incident. [RI-T16, RI-T30]
- **Decide:** If a recent change is the confirmed cause and its revert applies cleanly, roll it back. If it does not apply cleanly, fix forward and accept the higher risk. If no rollback is available and a non-essential dependent feature is involved, switch that feature off at runtime. If there is not enough time to repair the defect properly, contain the damage with a visibly marked stopgap. In every case, follow up with a code fix of the defect, unless the proper fix is possible right now, in which case make it instead of the stopgap. When the feature must stay available under heavy load, do not set its pool to zero. A limit of one keeps it available. [SWE-T31, PP-T05, RI-T16, RI-T30]

### Fix a bug you notice while refactoring, or leave it?

- **Pragmatic Programmer:** Repair known defects in code you are changing, within that change. [PP-P1]
- **Refactoring:** A refactoring must keep behavior the same, so leave a noticed bug in place and fix it separately, test first. [REF-P1, REF-T04]
- **TDD:** Park side ideas on a list during a planned task, but a reported defect is handled with its own failing test. [TDD-T26, TDD-T42]
- **Decide:** Both can be satisfied. Do not fix the bug inside a refactoring commit. Finish or pause the refactoring, then fix the bug in a separate behavior commit with its own failing test, in the same pull request when the change touches that code. Pragmatic Programmer's own limit applies: decline the work if its risks are not acceptable. [REF-P1, PP-P1, PP-T44, REF-T04]

### Undo the step, or write a test for the cause?

- **TDD:** Undo a large change that breaks in a way that is slow to diagnose, and redo it in smaller steps. [TDD-T05]
- **TDD:** Write a focused test for the cause of an unexplained failure before retrying the change. [TDD-T47]
- **Decide:** The entries settle it by step size. Undo when the breaking change is a large step. Write the focused test when the change is already small. [TDD-T05, TDD-T47]

### Debugger or trace statements?

- **Pragmatic Programmer:** Confirm the wrong value in a debugger and walk up the stack to where it first goes wrong. [PP-T58]
- **Pragmatic Programmer:** Use trace statements in one parseable format so scripts can follow state over time. [PP-T60]
- **Decide:** Use the debugger when the program returns a bad result without crashing. Use formatted traces when the bug depends on timing, concurrency or event order. When a leak is suspected, use paired open and close logs. The entries give no rule for cases that fit none of these, so use the tools the codebase already supports. [PP-T58, PP-T60, PP-T61]

### Keep a workaround or remove it?

- **Pragmatic Programmer:** Remove retries, sleeps and calls that trial and error added, unless a comment or test justifies them. [PP-T66]
- **Pragmatic Programmer:** When a proper fix must wait, a visibly marked stopgap is acceptable. [PP-T05]
- **Release It!:** A delayed, bounded retry of documented transient errors is a designed defense. [RI-T23]
- **Decide:** Keep a call only if it has a documented reason or test (PP-T66), or it is a stopgap with a visible temporary marker while the proper fix is not yet possible (PP-T05), or it is a designed retry that meets RI-T23's conditions. Remove anything else. A bug-fix diff carries no hacks either way. [PP-T66, PP-T05, RI-T23, PP-T72]

## Review checklist

- [ ] The PR or ticket records how the defect was reproduced, with the full error text and location, before the first code change. [PP-P8, PP-T57]
- [ ] A test or script in the repository reproduces the bug in one command. [PP-T21]
- [ ] The fix adds a test that fails without the fix, plus a test at application level. [PP-T20, TDD-T42, SWE-T57]
- [ ] A production failure the regular tests missed now has a test for its exact path. [RI-T07]
- [ ] For a regression, the PR names the commit that introduced it. [PP-T22, SWE-T27]
- [ ] Any blame on a library or platform is backed by a learning test, and assumptions about uncontrolled code are written at the call site. [TDD-T30, PP-T67]
- [ ] The diff changes the code where the fault originates, not only a downstream guard or a limit setting. [PP-P8, RI-T16]
- [ ] Every retry, sleep or extra call added during debugging has a comment or test that justifies it. Tests have no fixed sleeps. [PP-T66, SWE-T55]
- [ ] The fix diff has no dead code, hacks or unrelated edits, and restructuring sits in its own commit. [PP-T72, PP-T44]
- [ ] Debug trace lines share one format with a fixed prefix and labeled fields. [PP-T60]
- [ ] Leak investigations log opens and closes with matching identifiers. [PP-T61]
- [ ] No intermittent threaded test is marked skipped, retried or one-off. [CC-T60]
- [ ] No failing test is skipped, disabled or deleted to get a green run without an open ticket explaining why. [PP-T73, TDD-T15]
- [ ] The incident runbook puts service restoration first, before log collection or analysis. [RI-T03]
- [ ] Incident scripts capture thread dumps and database state without manual steps. [RI-T04]
- [ ] Every restart step in a runbook names the process, instance or machine. [RI-T35]
- [ ] Monitoring exposes queue depth per tier of the request path. [RI-T36]
- [ ] Live configuration changes in the procedure are followed by a read-back or an observed behavior check. [RI-T31]

## More entries in this area

- `PP-T15` — Assert conditions you believe cannot occur: add assertions so a wrong assumption fails visibly where it occurs, but give expected bad input real error handling instead; see [errors and contracts](errors-and-contracts.md).
- `PP-T16` — Crash early on impossible states: stop at the first impossible state so the original fault is not hidden by later damage.
- `PP-T63` — Use feature switches for diagnostics: turn on extra diagnostics for selected users only, never where end users or unauthorized people could see them.
- `PP-T62` — Turn ad hoc debugging checks into unit tests: keep the manual check that exposed the defect as an automated test.
- `TDD-T31` — Record surprising behavior as a named test: when debugging uncovers an unexpected rule, name a test after it.
- `TDD-T46` — Give each assertion a failure message: in batch runs the message is the only record of the cause, unless the team has tried both ways and found messages add no value.
- `TDD-T14` — Run the tests after every small change: keeps the cause of a red bar next to the change that made it.
- `PP-T73` — Do not skip or delete failing tests: fix a failing test or remove it on purpose, never just to get green.
- `RI-T09` — Run steady longevity load on a spare machine: exposes leaks and slow growth that short tests miss.
- `RI-T25` — Log and expose breaker state changes: gives responders a record of when an integration tripped and recovered.
- `RI-T70` — Put a request identifier in logs and calls: lets a failed request be followed across tiers.
- `RI-T75` — Measure residence time, not only processing time: queue wait is part of the latency users feel.
- `RI-T30` — Disable a feature with a zero pool limit: a runtime way to shed a non-essential dependency during an incident.
- `RI-T31` — Verify a runtime configuration change took effect: read the setting back, after a restart if it is read only at startup.
- `RI-T01` — Confirm operations can run the system alone: runbooks and alerts must work for operators, not only for developers.
- `RI-T64` — Simulate the absence of key people: name a backup for each critical incident role.
- `SWE-T31` — Roll back the culprit before fixing forward: restores known behavior while the fix is worked out.
- `SWE-T27` — Split a failing batch to find the culprit: test each change alone or binary-search the batch.
- `DDIA-T47` — Repair bad batch output by rerunning fixed code: for a buggy batch job, roll back, fix and rerun from retained inputs, which does not repair writes to an operational database.
- `WELC-T32` — Trace callers, state, parameters and statics: map how a changed method's effects spread before editing it; see [legacy code](legacy-code.md).
- `TDD-P8` — Trust a test only after it can fail: a regression test that has never failed proves nothing about the defect.
