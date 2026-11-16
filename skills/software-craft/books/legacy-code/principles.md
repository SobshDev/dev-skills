# Working Effectively with Legacy Code — Michael Feathers (1st edition, 2004)

## Summary
Feathers defines legacy code as code without tests, whatever its quality. His core argument is that such code can still be changed safely once tests pin its existing behaviour. The method is to get the code under test with seams, fakes and small dependency breaks, then change it in small verified steps. Each step is checked by tests before the next begins, so the code stays verified. New behaviour goes into new code where possible, and design improves gradually, because a legacy system cannot be made ideal in one change. The method applies when a team must change code that lacks tests.

## Principles

### WELC-P1: Cover untested code before changing it
Nothing reports when existing behaviour breaks in untested code, so tests that pin it come before the edit. They cost time now, and that time is repaid when the code changes again.

- **Apply:** Before editing untested code, write tests that pin the behaviour the change must keep.
- **Limits:** Some dependency breaking must come first. Code that never changes again does not repay the test cost, and simple code may need few tests.
- **Check:** Test commits for an area come before its change commits, or the diff adds tests for the code it touches.
- **See:** WELC-T06, WELC-T18, WELC-T37
- **Source:** ch. 2, 6, 11

### WELC-P2: Change code in small verified steps
Small verified steps keep each mistake easy to find, since large untested changes carry serious risk.

- **Apply:** Make each refactoring a small step, and run the tests before taking the next.
- **Limits:** Small steps do not replace tests that must exist before they begin.
- **Check:** Refactoring commits are small, and each one is followed by a passing test run.
- **See:** WELC-T01, WELC-T15
- **Source:** ch. 1, 7, 12, 23

### WELC-P3: Keep refactoring and behaviour changes apart
Refactoring must leave functional behaviour unchanged, so a diff that mixes the two cannot be checked by existing tests.

- **Apply:** Commit structural and behaviour changes separately, labelling each edit.
- **Limits:** Structural changes may still alter performance, so they need their own checks.
- **Check:** Commits separate refactoring from behaviour changes.
- **See:** WELC-T01, WELC-T50
- **Source:** ch. 1, 8, 23

### WELC-P4: Add new behaviour in new code
New logic inside a large untested method adds risk to code nobody can test. Sprouting and wrapping put it in reachable code, so the legacy method changes by only a call.

- **Apply:** Put new logic in a new method or class, and let legacy code call it.
- **Limits:** Sprouted or wrapped code does not test legacy callers, which still need coverage over time.
- **Check:** New logic lives in new methods or classes, and the legacy method gains only a call.
- **See:** WELC-T12, WELC-T13, WELC-T14, WELC-T45
- **Source:** ch. 6, 19, 20

### WELC-P5: Break dependencies at seams safely
Code that cannot run in a test harness needs its dependencies broken. Feathers breaks each dependency at a seam, where behaviour changes without editing callers, with the smallest change.

- **Apply:** Find the seam nearest the blocked dependency and its enabling point, then change as little code as possible.
- **Limits:** Pervasive dependencies may leave no practical seam.
- **Check:** The test build substitutes the dependency at a named seam, leaving production call sites unchanged.
- **See:** WELC-T05, WELC-T06, WELC-T17, WELC-T61
- **Source:** ch. 4, 7

### WELC-P6: Observe effects with fakes and sensing points
Some effects are visible only through a collaborator or from outside the class. Recording fakes and temporary sensing variables let tests observe them without changing production behaviour.

- **Apply:** Sense through the collaborator's interface when it exposes the effect. Otherwise use a recording fake or a flag, then assert on it.
- **Limits:** Sensing variables are temporary and must be removed when the refactoring finishes.
- **Check:** Tests assert on fake records or sensing flags that only the changed code can set.
- **See:** WELC-T07, WELC-T08, WELC-T39
- **Source:** ch. 3, 4, 13, 22, 25

### WELC-P7: Find change points and test points before editing
Name both points before editing, so the tests can detect the change.

- **Apply:** Name the change points and test points before editing any code.
- **Limits:** When no test point detects every change, narrow the change set.
- **Check:** The commit message or PR description names each changed method and the test that observes it.
- **See:** WELC-T16, WELC-T34, WELC-T35, WELC-T40
- **Source:** ch. 2, 11, 12

### WELC-P8: Improve legacy design gradually instead of rewriting it
Feathers accepts imperfect intermediate design, since a legacy system cannot become ideal in one change. Steady small improvements ease change, and a rewrite does not escape old problems.

- **Apply:** Improve each area you touch a little, leaving others alone until they must change.
- **Limits:** Large restructurings suit parts the team has chosen to rewrite. Early in a release, with accepted risk, a bigger refactoring may fit.
- **Check:** Recent history shows small cleanup commits beside feature work, and unrelated areas stay untouched.
- **See:** WELC-T50, WELC-T53
- **Source:** ch. 6, 20, 24
