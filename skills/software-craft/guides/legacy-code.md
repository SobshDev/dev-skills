# Changing legacy code (code without tests)

This guide covers how to change code that has no tests: pinning what it does today, finding where to observe a change, breaking the dependencies that keep it out of a test harness, adding new behaviour beside it, shrinking monster methods and classes, and replacing old parts gradually instead of rewriting them. The single most important idea is that tests come first: until tests pin the current behaviour, nothing tells you that an edit broke it, so every move before those tests exist must be small, conservative and checked by other means.

**Read this when:** fixing a bug in code with no tests, adding a feature to a long untested method, a class will not build or run in a test harness, a constructor, global, singleton or static call blocks a test, refactoring uncovered code, splitting a huge class, someone proposes a rewrite, or inherited code has no clear purpose.

**Entry IDs** such as `WELC-T12` point to `../books/<book>/techniques.md` (T) or `principles.md` (P);
the prefix table is in [SKILL.md](../SKILL.md).

## Contents
- [Rules: getting the code under test](#rules-getting-the-code-under-test)
- [Rules: breaking dependencies](#rules-breaking-dependencies)
- [Rules: adding new behaviour](#rules-adding-new-behaviour)
- [Rules: monster methods and classes](#rules-monster-methods-and-classes)
- [Rules: replacing instead of rewriting](#rules-replacing-instead-of-rewriting)
- [Playbooks](#playbooks)
- [Where the books disagree](#where-the-books-disagree)
- [Review checklist](#review-checklist)
- [More entries in this area](#more-entries-in-this-area)

## Rules: getting the code under test

### 1. Pin current behaviour with tests before changing it

In untested code nothing reports when an edit breaks existing behaviour, so tests that pin that behaviour come before the edit. Legacy Code, Clean Code, Pragmatic Programmer, Refactoring and TDD all put these tests in place before restructuring, because only then can anyone see whether behaviour survived each step. [WELC-P1, CC-T75, PP-T43, TDD-T45, REF-T01, REF-T03]

- **Do:** Before editing, write automated tests that assert the behaviour your change must keep. When your change makes a new call to an existing method that has no tests, write tests for that method first [WELC-T73]. Before a large change that feels too risky, build the tests and modules that make it safe, then start it [TDD-T22].
- **Not when:** Some dependency breaking must happen before the first test can run (rule 10). Code that will never change again does not repay the cost, simple code may need only a few tests, and stable parts of a system may keep looser tests [WELC-P1, TDD-T22]. Pragmatic Programmer frames its rule around restructuring: a change that alters behaviour or interfaces is a feature change, covered by rules 18 and 19 rather than by this one [PP-T43].
- **Check:** Test commits for an area come before its change commits, or the diff adds automated tests for the code it touches, including legacy methods that a changed call site now uses [WELC-P1, WELC-T73, REF-T01].

### 2. Learn why inherited code exists before changing it

Inherited code often encodes a reason that the code no longer shows. SWE at Google asks you to find that reason and pin the observable behaviour with tests before you alter or remove it. Tidy First adds that behaviour other callers already use needs a compatibility or migration plan before it changes. [SWE-T62, SWE-T04, TF-T37]

- **Do:** Learn why the code was built that way before changing or deleting code whose purpose is unclear [SWE-T62]. Delete code that no caller reaches when you find it, but if its purpose is unclear, learn why it was there first [SWE-T04]. When the change alters behaviour that users or other systems rely on, include compatibility handling or a migration [TF-T37].
- **Not when:** Code that really is unclear or wrong still needs changing, so learning its history is a step before the change, not a reason to skip it [SWE-T62]. Code that still delivers more value than its upkeep stays [SWE-T04].
- **Check:** Changes to inherited code carry tests of its behaviour, and a change that overrides an earlier choice states why the old reason no longer holds [SWE-T62].

### 3. Name the change points and test points before editing

Decide which methods you will change and where a test can observe each change before you edit anything. Effects spread to other code through callers, object state, parameters and statics, so trace those four paths from each changed method out to a system boundary. [WELC-P7, WELC-T32, WELC-T34]

- **Do:** List each method you will change. For each, list its callers, the fields it reads and writes, its parameters and the statics it uses, and follow the callers outward [WELC-T32]. Put the test at the changed method, or at the nearest method whose result shows the effect [WELC-T34].
- **Not when:** If no test point detects every change, make the change set smaller [WELC-P7]. Callers that never reach the changed method need no tracing [WELC-T32]. When the change point is itself the test point, or a more distant point is much easier to set up, test there instead [WELC-T34].
- **Check:** The commit message or PR description names each changed method, the paths its effects travel and the test that observes it [WELC-P7, WELC-T32].

### 4. Cover a cluster of changes through one narrow entry point

Breaking dependencies class by class across a large area is impractical. Look for one narrow place that every planned change passes through, a pinch point, and test the whole cluster there. A characterization test at a public entry point holds behaviour steady while you break the dependencies inside. [WELC-T16, WELC-T33, WELC-T35]

- **Do:** Find a single method through which all planned changes flow, or a pair of methods when no single one exists [WELC-T35]. Write one characterization test (rule 5) that enters through that public point before you start breaking the classes apart [WELC-T33]. Aim the tests at that entry point rather than at each class behind it [WELC-T16].
- **Not when:** With only one planned change, test it at its own method instead (rule 3) [WELC-T35]. A class that already has unit tests entering it directly does not need the higher-level test first [WELC-T33].
- **Check:** The tests at the pinch point fail if any one of the planned changes is applied wrongly [WELC-T35].

### 5. Characterize what the code does, not what it should do

Legacy code usually has no specification to check against, so the first tests record what the code actually does today. Refactoring uses the same tool, a characterization test placed at a seam, so that any change to behaviour shows up. [WELC-T37, REF-T03, WELC-T40, WELC-T41]

- **Do:** Assert what the code does today. A common way is to write the test with a guessed expected value, run it, let it fail, and copy the actual result into the assertion [WELC-T37]. Reach every branch whose lines the planned diff will alter [WELC-T40]. Add minimum, maximum and boundary inputs, plus one input for each type conversion on the path, since silent truncation only shows at certain values [WELC-T41]. See snippet below.
- **Not when:** Branches the change leaves alone do not need tests yet [WELC-T40]. Refactoring warns that output copied from a placeholder run must be confirmed before you rely on it [REF-T03].
- **Check:** Expected values match today's output, tests reach each branch that appears in the diff, and inputs include the extremes and each conversion on the path [WELC-T37, WELC-T40, WELC-T41].

```java
@Test
void lateFeeForThirtyOneDays() {
    // Value copied from the first, deliberately failing run.
    assertEquals(12, fees.lateFee(31));
}

@Test
void lateFeeForNegativeDays() {
    // SUSPICIOUS: a negative day count still charges a fee. Follow-up: BILL-142
    assertEquals(3, fees.lateFee(-1));
}
```

### 6. Prove each pinning test can fail

A test that cannot fail gives false confidence, and a characterization test is only useful if it would catch a changed result. Refactoring and TDD both ask you to break the code on purpose and watch the new test fail. [REF-T02, REF-T03, TDD-P8, TDD-T17, SWE-T54]

- **Do:** After a new characterization test passes, inject a fault in the code it covers and confirm it fails [REF-T02, REF-T03]. When a test you expected to fail passes, find out why before trusting it [TDD-T17]. Use a coverage report to locate untested code, then add tests that assert results [SWE-T54].
- **Not when:** Refactoring exempts judgments that are subjective, where an injected fault cannot reveal false confidence [REF-T02]. Passing unit tests do not establish security or concurrency correctness, and an injected fault that only swaps one constant for another does not change what the program means [TDD-P8]. Coverage alone does not explain an unexpected pass [TDD-T17].
- **Check:** Commit or PR notes record a run where each new test failed after an injected fault [REF-T02, REF-T03].

### 7. Mark suspicious results, and fix them in a separate change

A characterization test sometimes exposes behaviour that looks like a bug. Deployed users may already depend on it, so the test records what happens and flags it rather than silently fixing it. Refactoring agrees from the other side: a structural change keeps a bug you notice, and the fix comes later on its own. [WELC-T38, TDD-T31, REF-P1, REF-T04]

- **Do:** Mark the surprising test as suspicious, give the reason and link a follow-up item [WELC-T38]. Name the test after the surprising rule so later readers see it [TDD-T31]. Fix the bug in its own change, starting from a test that fails because of it [REF-T04], and check who relies on the old behaviour first [TF-T37].
- **Check:** Surprising characterization tests carry a marker such as `// SUSPICIOUS: <reason> <follow-up ID>`, and any fix lands in a separate commit with a test that failed before it [WELC-T38, REF-T04].

### 8. Observe hidden effects with recording fakes and sensing variables

Some effects are visible only through a collaborator the class calls, or not at all from outside. A fake that records the calls it receives makes outgoing effects readable, and such tests are real tests. When tangled logic hides whether a branch ran, a temporary flag set in that branch lets tests see it. [WELC-P6, WELC-T07, WELC-T39]

- **Do:** When the collaborator's interface exposes the effect, sense through it. Otherwise replace the collaborator with a fake that implements its interface and records what it is sent, and hold the fake by its concrete type in the test [WELC-P6, WELC-T07]. For tangled logic, add a flag that the branch sets, and write a pair of tests asserting it in both states [WELC-T39].
- **Not when:** Sensing variables are temporary, so remove them when the refactoring is finished [WELC-P6, WELC-T39].
- **Check:** Tests assert on fake records or flags that only the changed code can set, and no sensing flag remains after the refactoring ends [WELC-P6, WELC-T39].

### 9. Keep fakes slim, and use cheap real collaborators when you can

A test fake never runs in production, so it may skip production rules and hold only what tests assert on. A cheap, read-only real collaborator needs no fake at all, and a maintained mock library is less code to own than hand-copied doubles. [WELC-T08, WELC-T22, WELC-T11]

- **Do:** Give each fake only the behaviour and stored values the tests need, and keep it in test sources [WELC-T08]. Pass the real object when it builds quickly and only reads, for example a file [WELC-T22]. Take doubles from a maintained library when a test needs several [WELC-T11]. For how far to go with doubles, see the tension below and [testing](testing.md).
- **Not when:** If production code constructs or calls the fake, use a real implementation or a seam instead [WELC-T08]. A collaborator that writes data or takes long to build is not a candidate for the real-object route [WELC-T22]. Where no mock library exists, hand-write simple recording fakes [WELC-T11].
- **Check:** Fake classes sit in test sources and production code never references them, and real objects in tests are read-only and quick to build [WELC-T08, WELC-T22].

## Rules: breaking dependencies

### 10. Break each dependency at the nearest seam, with the smallest edit

Code that cannot run in a test harness needs its dependencies broken. A seam is a place where behaviour can be changed without editing the callers, and each seam has an enabling point where the substitute is chosen. Without tests, logic changes are the main danger, so the first breaks change only signatures or add interfaces. [WELC-P5, WELC-T05, WELC-T06, WELC-T60]

- **Do:** Find the seam closest to the blocking dependency and its enabling point [WELC-P5]. Limit the first edits to signature changes and new interfaces [WELC-T05]. Copy the original parameter list exactly into any extracted method and its call, except for the signature changes the conservative first break itself makes [WELC-T60, WELC-T05]. Commit the dependency break, then the commit that adds the tests it makes possible [WELC-T06]. Remove the workarounds once tests cover the code [WELC-T05].
- **Not when:** Pervasive dependencies may leave no practical seam [WELC-P5]. Then, if the change is small, put it in a sprouted class instead (rule 18) [WELC-T14]. Refactoring warns that making a seam before any test exists is itself risky, which is why these edits stay minimal and checked (rule 11) [REF-T03].
- **Check:** The first dependency-breaking commit changes signatures or adds interfaces only, it precedes the test commit for the same class, and production call sites stay unchanged [WELC-T05, WELC-T06, WELC-P5].

### 11. Lean on the compiler and a second reader while tests are missing

Before tests exist, Legacy Code relies on the compiler and a second reader to catch mistakes. Mistakes in dependency breaks can go unnoticed, so a second person reads each one before it counts as done. [WELC-T31, WELC-T56, WELC-T59, PP-T54]

- **Do:** Change the declaration, fix each compile error, then search by hand for shadowed and inherited uses the compiler cannot flag [WELC-T31]. After any hand extraction, check that each signature passes every variable the code needs, matches the declared types and hides no base-class name [WELC-T56]. Use the IDE's refactoring commands for renames and signature changes where they exist [REF-T14]. Flag every dependency-breaking edit for a second reader, or pair on it [WELC-T59, PP-T54].
- **Not when:** When builds are slow, searching for uses may be more practical than compiling [WELC-T31]. Without static typing the tool cannot find every match, so check matches by hand [REF-T14].
- **Check:** Changed declarations leave no compile errors at commit, and review records show a second person read each dependency-breaking change [WELC-T31, WELC-T59].

### 12. Pass hidden dependencies in instead of creating them inside

A constructor or method that creates a live resource cannot be tested without that resource. Legacy Code, Clean Code, Pragmatic Programmer, TDD and Tidy First agree on the fix: receive the dependency as a parameter. Tests can then pass a fake without touching global state, and callers can see what the routine depends on. To avoid breaking existing callers, keep the old constructor and let it supply the production default. [WELC-T62, WELC-T63, CC-T12, PP-T27, TDD-T40, TF-T14]

- **Do:** Move the object the constructor creates into a constructor parameter [WELC-T62]. Keep the original constructor and make its body a single call to the new one with the default collaborator [WELC-T63]. If the parameter list would grow too long, move creation into a factory method that a testing subclass overrides [WELC-T76]. See the snippet below.
- **Not when:** A constructor that builds many objects makes the parameter list long, so prefer the factory method there [WELC-T62]. In languages without direct constructor chaining, move the shared body into an initialize method that both constructors call [WELC-T63]. In C++, a constructor calls only the base version of a virtual factory method, so the override route does not work [WELC-T76].
- **Check:** The constructor accepts the dependency instead of creating it, the old constructor only forwards to the new one, and no global or singleton holds a resource that tests must replace [WELC-T62, WELC-T63, TDD-T40].

```java
public InvoiceSender(Config config) {
    this(config, new SmtpMailClient(config));  // old signature, production default
}

InvoiceSender(Config config, MailClient mail) { // new seam: tests pass a fake
    this.config = config;
    this.mail = mail;
}
```

### 13. Add an interface where a test must substitute a collaborator

When a parameter's type is hard to create or fake, extract an interface from its class and make the method depend on that. Growing the interface from compile errors keeps it to the methods the code really calls. For a sealed or final library class, mirror only the members you use in your own interface and write a wrapper that delegates to the library. [WELC-T61, WELC-T66, WELC-T30, CC-T51, PP-T12]

- **Do:** Extract an interface from the parameter's class and change the method to take it [WELC-T61]. Start from an empty interface, switch the users to it, and add one method per compile error [WELC-T66]. For a library class tests cannot fake, write the interface and a delegating wrapper, so only the wrapper names the library [WELC-T30, CC-T51, PP-T12]. When another team owns the API, ask them for a maintained fake first [SWE-T13].
- **Not when:** Skip the interface when the parameter type is low-level or tied to one implementation technology [WELC-T61]. Grow the interface from errors only when the design does not need one that covers every public method [WELC-T66]. Do not skin and wrap a library that already offers interfaces, and split a large API by responsibility instead of mirroring it [WELC-T30]. If the owning team declines to supply a fake, wrap their API in one class and fake the wrapper [SWE-T13].
- **Check:** The changed method's parameter is an interface type that tests fake, the interface declares only methods the code calls, and only the wrapper references the library [WELC-T61, WELC-T66, WELC-T30].

### 14. Override only the problem method in a test subclass

When one method opens a connection or calls a resource tests must avoid, subclass the class in the test and override just that method. The rest of the class then runs as production code. When the troublesome calls are inline, first extract them into methods, then override those. [WELC-T23, WELC-T29, WELC-T69]

- **Do:** Override only the method that reaches the dependency, and record or suppress the call there [WELC-T23]. Extract inline collaborator calls into their own methods and override those in the test subclass [WELC-T29]. When environment dependencies run through many methods, make the class abstract, move the environment-bound members into a production subclass, and let a test subclass give them empty bodies [WELC-T69]. See the snippet below.
- **Not when:** Do not override the method that is under test, and return empty results only where tests never check them [WELC-T23]. When an existing method can be overridden directly, nothing needs extracting [WELC-T29]. When only a few calls reach the environment, override those calls instead of splitting the class [WELC-T69].
- **Check:** The test subclass overrides only the methods that reach collaborators or the environment [WELC-T23, WELC-T29, WELC-T69].

```java
class TestableReportJob extends ReportJob {
    final List<String> printed = new ArrayList<>();

    @Override
    void sendToPrinter(String page) {   // the one method that reaches the printer
        printed.add(page);              // record instead of printing
    }
}
// The test runs the real report logic, then asserts on 'printed'.
```

### 15. Route globals, statics and singletons through something tests can replace

Globals, static calls and singletons cannot be swapped by passing a different object, so Legacy Code introduces a small indirection that tests can control while production keeps its behaviour. Which indirection fits depends on how many places use the global and whether its state can be set up from outside. TDD and Pragmatic Programmer state the end goal: shared resources reach code as parameters, not through globals or singletons. [WELC-T09, WELC-T64, WELC-T65, WELC-T70, WELC-T25, WELC-T26, TDD-T40, PP-T27]

- **Do:** Wrap a global function in a member with the same signature that only forwards to it, and override the member in tests [WELC-T09]. Move global variables or arrays into a holder class reached through one instance [WELC-T64]. Replace direct uses of a heavily used global with a protected getter that a test subclass overrides [WELC-T65]. Add an instance method that delegates to a hard static call, and give the class an object tests can replace [WELC-T70]. For a singleton tied to external resources, add a static setter that installs a test instance [WELC-T25]. For a singleton whose public methods can set up any state, add a reset method and call it in setup and teardown [WELC-T26].
- **Not when:** Use the getter only when several methods call the global, and override one extracted call when only one does [WELC-T65]. A static method with nothing hard to depend on needs no delegate [WELC-T70]. Skip the setter when the singleton's public methods already let tests set up all needed state [WELC-T25]. Skip the reset when the state depends on external resources or one replacement serves every test [WELC-T26].
- **Check:** Production wrappers only forward, the class touches the global only through its getter or holder, the static setter is called only from test setup, and setup and teardown both call any reset method [WELC-T09, WELC-T64, WELC-T65, WELC-T25, WELC-T26].

### 16. Separate pure computation from API and environment calls

Useful logic often sits right beside calls to a library or service, which makes it hard to reach from a test. Describe the chunk's core job in a sentence or two, then move the work that does not call the service into code that a test can run with a fake or with no dependency at all. Clean Code applies the same idea to screens, sockets and frameworks, keeping them behind a thin forwarding layer. [WELC-T43, WELC-T42, WELC-T44, CC-T13]

- **Do:** Write down the chunk's core computation, which separates real work from input, output and calls [WELC-T43]. Move the computation into its own function, with a thin wrapper that calls it and then the dependency [WELC-T44]. Move larger blocks of non-service logic into classes that depend on an interface to the service [WELC-T42]. Keep the forwarding layer free of branches and loops [CC-T13]. The [functional-style](functional-style.md) guide covers the pure-core approach in depth.
- **Not when:** Logic that still uses the library's data types cannot be fully freed [WELC-T42]. Dependencies too pervasive for thin wrappers block this move [WELC-T44].
- **Check:** Core logic classes import no service classes, the computation lives in a function that calls no external API, and the wrapper only forwards [WELC-T42, WELC-T44, CC-T13].

### 17. Reach a hard-to-test method with the smallest access change

Sometimes the method you must test is private or lives on an object that is hard to create. Legacy Code allows a temporary widening: make one private method protected and reach it from a test subclass, or make a stateless method static so tests can call it without an instance. TDD agrees that tests should check public behaviour, and tolerates checking private state only until a better design appears. [WELC-T27, WELC-T28, TDD-T13]

- **Do:** Test through public callers first. If that fails, change one private method to protected and test it from a subclass [WELC-T27]. Make a method static when it reads no instance fields and calls no instance methods [WELC-T28]. Note the widened access as needing a better design later [TDD-T13].
- **Not when:** Avoid reflection, and move the logic into its own class once that is affordable [WELC-T27]. Do not make a method static when it reads instance state, a test subclass overrides it, or the language warns about static calls [WELC-T28].
- **Check:** Only the method's access changed, widened access is narrowed later, and a new static method references no instance fields or methods [WELC-T27, WELC-T28].

## Rules: adding new behaviour

### 18. Put new behaviour in new code that the legacy code calls

Adding logic inside a large untested method adds risk to code nobody can test. Writing the new logic as its own method or class, with its own tests, means the legacy method changes by only one call. Clean Code reaches the same conclusion for existing classes in general: a new case belongs in a new single-purpose class, not in a new branch. [WELC-P4, WELC-T12, WELC-T14, WELC-T45, WELC-T53, CC-T45]

- **Do:** If the class builds in a harness, write the new logic as a new method, test it, then add its call to the legacy method [WELC-T12]. If the class is too tangled to instantiate, put the logic in a new class that the legacy class creates and calls [WELC-T14]. For a small addition to a large class, give it a new well-named method instead of inline lines [WELC-T45]. Treat this as the default for long methods you cannot yet test [WELC-T53]. When the class builds in a harness, drive the sprouted method test-first, after getting at least one passing test on the class it joins, or features end up bolted on around untested code [WELC-T18, WELC-T19, TDD-P1]. See the snippet below.
- **Not when:** A class that cannot be built in a harness needs the sprouted class, and a class that can be built needs only a sprouted method [WELC-T12, WELC-T14]. A small addition that is really a distinct sequence of steps calls for the full sprout-method route, tested first, rather than a quick named method [WELC-T45]. Sprouted code does not test the legacy callers, which still need coverage over time [WELC-P4].
- **Check:** New logic lives in a new method or class with its own unit test, and the legacy method gains only a call [WELC-P4, WELC-T12, WELC-T53].

```java
void applyCharges(Order order) {
    order.addAll(loyaltyDiscounts(order)); // the only line added to the legacy method
    // ... untouched legacy body ...
}

// New method, written and tested on its own before the call above was added.
List<Charge> loyaltyDiscounts(Order order) { ... }
```

### 19. Wrap a method when new behaviour must run on every call

When the new behaviour must happen every time the old method runs, and the old method cannot be tested yet, rename the old method and give its name to a wrapper. The wrapper calls the renamed original and adds the new step around it, so the original body stays untouched and does not grow. [WELC-T13]

- **Do:** Rename the existing method, create a method with the old name that calls it, and put the new behaviour before or after that call [WELC-T13].
- **Not when:** Do not wrap when the code is simple, when an extract-method tool would give better names, or when the new behaviour has to interleave with the old steps [WELC-T13].
- **Check:** The original method body is unchanged apart from its new name [WELC-T13].

## Rules: monster methods and classes

### 20. Shrink a monster method with small, tool-checked extractions

A long method is safest to break up with an extraction tool after tests cover its side effects, because the tool checks each step and hand edits escape those checks. Before any tests exist, take only small chunks of two to five lines, which have few parameters and return values to get wrong. Extracting every condition and its body leaves a skeleton of control flow that you can then refactor on its own. [WELC-T54, WELC-T55, WELC-T56, WELC-T58]

- **Do:** Once tests cover the side effects, make every extraction with a safe tool and no hand edits between steps [WELC-T54]. Before tests exist, extract short chunks with clear names and leave large blocks for later [WELC-T55]. Check each hand-made extraction's signature (rule 11) [WELC-T56]. When the control structure itself needs work, extract each condition and its body until the method holds only conditionals and calls [WELC-T58]. The [refactoring](refactoring.md) guide covers extraction mechanics.
- **Not when:** If the tool cannot extract methods, or changes behaviour when it does, edit by hand and check signatures [WELC-T54, WELC-T56].
- **Check:** The commit names the tool used, the diff has no hand edits between extractions, and early extractions are short methods named for one action [WELC-T54, WELC-T55].

### 21. Turn a monster method into a method object when its locals are worth sensing

Moving the body of a long method into its own class, with parameters and locals as fields, turns the former locals into state that tests can check. Refactoring and Clean Code use the same shape to unblock extraction: once the locals are fields, helper steps can be split out without long parameter lists. [WELC-T57, REF-T81, CC-T35]

- **Do:** Create a class whose fields hold the method's parameters and locals, move the body into one run method, and leave a single call in the original [WELC-T57, REF-T81]. Then extract helpers that share state through those fields [CC-T35].
- **Not when:** A sensing variable may be enough, and a small method with no instance data should become static instead [WELC-T57]. Refactoring says plain functions usually suffice, and a local that is reused for several purposes should be split into separate variables first [REF-T81]. Static fields shared by several threads can break the helpers [CC-T35].
- **Check:** The original method only creates the object and calls it, and the new class holds the parameters and locals as fields [WELC-T57, REF-T81].

### 22. Name a large class's main job, then extract hidden classes as you touch them

A large class usually hides several responsibilities. State its primary job in one sentence and list the other duties apart, which shows what belongs elsewhere. Fields that only a few methods use mark a hidden class, and a side group of methods is cheapest to extract when the next change already touches it. [WELC-T49, WELC-T36, WELC-T47, WELC-T48]

- **Do:** Write the class's main purpose in one sentence and list its other duties [WELC-T49]. Move a cluster of methods and the fields only they use into a new class, leaving overriding methods and shadowing fields in place [WELC-T36]. Extract a side group of methods in the same change that modifies one of them [WELC-T47]. When clients use only part of the class, give each client group an interface with its methods and delegate from a new client-facing class [WELC-T48]. Without a refactoring tool and without tests, move each method by copying it to a temporary `MOVING`-prefixed copy, pointing callers at it, then deleting the original and renaming [WELC-T46]. Refactoring's copy, delegate, redirect sequence keeps callers working in the same way [REF-T49].
- **Not when:** One method per class is not the goal, since methods can express responsibilities [WELC-T49]. Do not try to sort every method name into a new class at once [WELC-T47]. Avoid the client interfaces when the clients lack tests, because changing them is risky [WELC-T48]. When tests can be put in place first, extract the class normally instead of using `MOVING` copies [WELC-T46]. The source function may stay as a delegate indefinitely [REF-T49].
- **Check:** The new class holds the fields that only its own methods reference, the extraction lands in a change that modifies one of its methods, and no `MOVING`-prefixed name remains in the final diff [WELC-T36, WELC-T47, WELC-T46].

### 23. Remove duplication in small steps by converging similar methods

When repeated code shows up while you change a legacy system, removing small fragments during that feature work keeps each step safe and reveals larger duplication. Two methods with the same shape become one when you first pull their differing steps into separate methods, so the bodies match. The shared method then moves to a base class, and subclasses keep only their constructor data and one hook, the shape Design Patterns calls a template method. [WELC-T50, WELC-T51, WELC-T52, GOF-T66, TDD-T11]

- **Do:** Remove small duplicated fragments as you change the system, running the tests between steps [WELC-T50]. Pull the steps that differ between two similar methods into their own methods until the bodies differ only in calls, then declare abstract hooks and move the shared method up once it uses only shared data and hooks [WELC-T51, GOF-T66]. Make two near-identical pieces fully identical before merging them [TDD-T11, REF-T78]. Leave each subclass with its constructor and one overridden hook [WELC-T52].
- **Check:** Feature diffs include small de-duplication edits rather than one large rewrite, merged bodies were identical before one copy was removed, and each subclass holds a constructor and one hook [WELC-T50, TDD-T11, WELC-T52].

## Rules: replacing instead of rewriting

### 24. Improve legacy design gradually instead of rewriting it

A legacy system cannot become ideal in one change, and a rewrite does not escape the old problems. Legacy Code accepts imperfect intermediate designs and improves each touched area a little. Learning DDD modernizes legacy code the same way, one component at a time, moving scripts and records toward aggregates in small steps. [WELC-P8, DDD-P8, DDD-T57]

- **Do:** Improve each area you touch a little and leave others alone until they must change [WELC-P8]. Leave an area that will never change, or that would teach you nothing, untidied [TF-T28]. When modernizing toward a domain model, add value objects first, restructure into state-based aggregates next, and leave event sourcing for last [DDD-T57]. Name a strategy, strangler or refactoring, for each component in the modernization plan [DDD-P8].
- **Not when:** Large restructurings suit parts the team has chosen to rewrite, and early in a release with accepted risk a bigger refactoring may fit [WELC-P8]. Move toward aggregates only once a domain model is justified by a stated business need [DDD-T57, DDD-T56]. Advanced patterns still fit subdomains with real complexity, judged by their reasoning [DDD-P8]. Tidy First notes that truly static systems are rare, so code you expect never to change may still need it [TF-T28].
- **Check:** History shows small cleanup commits beside feature work, unrelated areas stay untouched, and value types appear in small commits before aggregates are restructured [WELC-P8, DDD-T57].

### 25. Replace a legacy part step by step behind a facade

When a legacy part must go, build the new requirements in a new component, route requests through a facade that decides per request which side serves it, and move one function at a time. Release It! makes the same point for whole stacks: replacing every component at once multiplies the risk, because nobody knows how the new stack behaves in production. SWE at Google adds that removal starts only once the replacement exists. [DDD-T58, RI-T53, SWE-T28, SWE-P7]

- **Do:** Put a facade in front of the legacy context, send each request to the old or new side, and limit legacy commits to hotfixes [DDD-T58]. Plan several cutover steps, each moving traffic or data to a new component [RI-T53]. Begin removing the old part only after the replacement covers the same or better functionality, and give each migration an owner [SWE-T28, SWE-P7]. Move callers across one at a time until none remain [TF-T25]. Test each substitute through the exact calls its parent makes [RI-T60]. When the switch goes out through a rolling deployment, make code and data changes tolerate old and new versions running at the same time [RI-T46]. The [architecture](architecture.md) and [production-reliability](production-reliability.md) guides cover the deployment side.
- **Not when:** A legacy context that is not planned for retirement does not need a strangler facade [DDD-T58]. Deprecate only systems that are demonstrably obsolete and have a comparable replacement [SWE-P7]. Automated rewrite tools can convert every caller at once instead of one at a time [TF-T25].
- **Check:** The release plan has more than one cutover step, routing code decides per request, the removal follows the release that introduced the replacement, and the facade goes once the legacy context is retired [RI-T53, DDD-T58, SWE-T28]. During migration both contexts may share a database when splitting the data would need distributed transactions [DDD-T58].

## Playbooks

### When you must fix a bug or change behaviour in untested code
1. Find out why the code is built as it is before touching it [SWE-T62].
2. Name the change points, trace their effects through callers, state, parameters and statics, and choose a test point at or near each change [WELC-P7, WELC-T32, WELC-T34].
3. If the class will not run in a harness, follow the next playbook first [WELC-T06].
4. Write characterization tests at the test point that reach every branch your diff will alter, including boundary and conversion inputs [WELC-T37, WELC-T40, WELC-T41].
5. Break the code on purpose and confirm the new tests fail [REF-T02, REF-T03].
6. Write a failing test that shows the bug, then fix it in its own commit [REF-T04]. If the bug is something users may rely on, mark it suspicious and raise a follow-up before changing it [WELC-T38, TF-T37].
7. Keep any structural cleanup in separate commits from the fix, and run the tests after each step [WELC-P3, WELC-P2]. The [change-workflow](change-workflow.md) guide covers commit discipline.

### When a class will not build or run in a test harness
1. Identify what blocks construction or the call: a constructor that creates a live resource, a global, a singleton, a static call, or a sealed library type [WELC-P5].
2. Pick the seam nearest the blocker. For a created resource, parameterize the constructor and keep the old one as an overload, or override a factory method [WELC-T62, WELC-T63, WELC-T76]. For a hard parameter type, extract an interface grown from compile errors [WELC-T61, WELC-T66]. For a global or singleton, use the indirection rule 15 picks [WELC-T09, WELC-T64, WELC-T65, WELC-T25, WELC-T70]. For a library class, skin and wrap it [WELC-T30]. For one troublesome method, override it in a test subclass [WELC-T23].
3. Keep the edit to signature changes and new interfaces, copy parameter lists exactly, and let the compiler find affected call sites [WELC-T05, WELC-T60, WELC-T31].
4. Ask a second reader to check the dependency break, then commit it on its own [WELC-T59, WELC-T06].
5. Write the first passing test against the class in its own commit [WELC-T06, WELC-T19].
6. Once tests cover the code, remove the temporary workarounds [WELC-T05].

### When you must add a feature to a long method you cannot test yet
1. Decide whether the class builds in a harness [WELC-T12, WELC-T14].
2. If it does, write the feature as a new method, drive it with tests, then add one call to it from the legacy method [WELC-T12, WELC-T18].
3. If it does not, write the feature as a new class with its own tests, and have the legacy class create and call it [WELC-T14].
4. If the behaviour must run on every call and does not interleave with the old steps, wrap the method instead [WELC-T13].
5. Plan to cover the legacy callers later, since the sprouted code does not test them [WELC-P4].

### When you break up a monster method
1. Pin its behaviour with a characterization test at the method or a pinch point above it [WELC-T37, WELC-T35].
2. If locals hide its effects, add sensing variables, or move the method into a method object so its locals become fields tests can read [WELC-T39, WELC-T57].
3. Before tests cover the side effects, extract only small chunks of two to five lines and check each hand-made signature [WELC-T55, WELC-T56].
4. Once tests cover the side effects, make every further extraction with a safe tool and no hand edits between steps [WELC-T54].
5. Extract conditions and their bodies until the method holds only control flow, then refactor that skeleton [WELC-T58].
6. Remove the sensing variables when the refactoring ends [WELC-P6].

### When someone proposes rewriting a legacy system
1. Prefer gradual improvement of each area you touch, and keep a rewrite for parts the team has deliberately chosen to replace [WELC-P8].
2. Name a strategy, strangler or refactoring, for each component [DDD-P8].
3. For a component being replaced, build new requirements in a new context behind a routing facade [DDD-T58].
4. Plan the switch as several cutovers, each moving some traffic or data, not one big bang [RI-T53].
5. Start removing the old code only after the replacement matches it, and move callers over until none remain [SWE-T28, TF-T25, SWE-T29].
6. Remove the facade once the legacy context is retired [DDD-T58].

## Where the books disagree

### Tests first, or dependency breaks first?
- **Clean Code, Pragmatic Programmer, TDD, Refactoring:** Write tests that pin behaviour before restructuring untested code [CC-T75, PP-T43, TDD-T45, REF-T01].
- **Legacy Code:** The tests often cannot run until some dependency is broken, so the dependency-breaking commit comes before the test commit [WELC-P1, WELC-T06].
- **Refactoring:** Making a seam before tests exist is itself risky [REF-T03].
- **Decide:** Make only the edits needed for the first test to run before that test exists, and keep them to signature changes and new interfaces with copied parameter lists, checked by the compiler and a second reader [WELC-T05, WELC-T60, WELC-T31, WELC-T59]. Legacy Code also allows extracting small chunks of two to five lines, with checked signatures, before tests exist (rule 20) [WELC-T55, WELC-T56]. Every other restructuring waits until tests pin the behaviour [CC-T75, PP-T43, TDD-T45].

### Should tests sit near the change or behind a public entry point?
- **Legacy Code (near):** Test each change at its own method or the nearest method that shows its effect, so a failure points at the cause [WELC-T34].
- **Legacy Code (entry point):** Cover a group of classes through one public entry point or pinch point before breaking them apart [WELC-T33, WELC-T35, WELC-T16].
- **SWE at Google:** Test through public interfaces, and test a helper used by one or two classes through those classes [SWE-P5, SWE-T08].
- **Decide:** Use a single entry point or pinch point when several changes span several classes, or when the classes do not yet have unit tests of their own [WELC-T35, WELC-T33]. Test at the change point when only one change is planned, unless a distant point is much easier to set up [WELC-T34, WELC-T35]. Keep a narrow helper's tests at its callers, and test general libraries directly [SWE-T08]. SWE at Google allows interaction checks where the call is itself the behaviour, which covers sensing through a collaborator [SWE-P5].

### Should expected values come from today's output or from hand calculation?
- **Legacy Code:** Assert what the code does now, often by copying the value a deliberately failing first run prints [WELC-T37].
- **Clean Code:** Work out expected values by hand, since a test that reuses the code under test cannot catch its errors [CC-T78].
- **Refactoring:** Output copied from a placeholder run must be confirmed before it is trusted [REF-T03].
- **Decide:** When pinning legacy code that has no specification, record today's output, mark anything surprising as suspicious, and confirm each value before relying on it [WELC-T37, WELC-T38, REF-T03]. When testing new behaviour or a calculation you are writing, compute the expected value by hand and do not call the production lookup to produce it [CC-T78].

### Recording fakes and mocks, or real collaborators?
- **Legacy Code:** Replace a collaborator with a recording fake when its calls are the only visible effect, keep fakes slim, and use a maintained mock library when a test needs several doubles [WELC-T07, WELC-T08, WELC-T11]. Use the real collaborator when it is cheap and read-only [WELC-T22].
- **SWE at Google:** Prefer the real implementation whenever it is fast and deterministic, assert on state rather than calls, and do not mock APIs whose owners may change them [SWE-T46, SWE-T10, SWE-T48]. A fake should match the real contract and be tested against it [SWE-T12].
- **Decide:** Use the real object when it is fast, deterministic and writes nothing [WELC-T22, SWE-T46]. Use a recording fake when the effect is visible only through the call, which is the case SWE at Google allows for interaction checks [WELC-T07, SWE-T10, SWE-T11]. For an API another team owns, use the owner's fake or fake your own wrapper rather than mocking it directly [SWE-T13, SWE-T48]. The [testing](testing.md) guide covers doubles in general.

### Sprout around the mess, or restructure before adding the feature?
- **Legacy Code:** Put new behaviour in a sprouted method or class and touch the untested long method by one call only [WELC-T53, WELC-P4].
- **Refactoring, Pragmatic Programmer, Tidy First, POSD:** Restructure the code a feature needs just before adding it, rather than forcing the feature into an unfit structure [REF-T88, PP-T64, TF-T01, POSD-T33].
- **Decide:** While the method cannot be tested, sprout or wrap, because restructuring it without tests is the risk Legacy Code avoids [WELC-T53, WELC-T13]. Once tests cover it, restructure first when the structure blocks the change, in small steps that each pass their tests [REF-T88, PP-T64, TF-T01]. The restructuring sources keep their own limits: skip it when the schedule impact outweighs keeping the old design, or when deadlines or incompatible teams make it impractical, and then use a nearly as clean alternative or a scheduled cleanup, keep it small for a very small feature, and change first when tidying would not ease the change [PP-T64, POSD-T33, REF-T88, TF-T01]. Legacy Code allows a bigger refactoring early in a release with accepted risk [WELC-P8].

### Subclass for testing and variation, or compose?
- **Legacy Code:** Subclassing is a quick tool here: test subclasses override problem methods, a variant overrides one method, and thin subclasses keep one hook [WELC-T23, WELC-T20, WELC-T52].
- **Design Patterns, Refactoring:** Prefer holding collaborators over subclassing for reuse, and switch to delegation when behaviour varies on two axes or the variant changes at run time [GOF-P3, REF-T70].
- **Decide:** Test-only subclasses live in test code and serve to get a class under test, so they do not set the production design [WELC-T23]. For production variants, subclass for a single variation and switch to composition when variations must combine or change at run time [WELC-T20, REF-T70]. Design Patterns accepts inheritance when new components must combine with existing ones, and Refactoring accepts starting with inheritance until it causes problems [GOF-P3, REF-T70].

### Add an interface just so a test can fake a collaborator?
- **Legacy Code:** Extract an interface when a parameter is hard to create in tests, and put interfaces at volatile dependencies [WELC-T61, WELC-T17].
- **Clean Code, TDD:** Add no interface until a current caller needs it, and add one only when a failing test or a real variation calls for it [CC-T77, TDD-P9, CC-P5].
- **Decide:** A failing test that must substitute the dependency is a need TDD accepts, so extract the interface then, grown from the methods the code calls [TDD-P9, WELC-T61, WELC-T66]. Skip it when the parameter type is low-level or tied to one technology, and add none for features not yet planned unless growth is a confirmed business direction or the odds of needing the hook are high [WELC-T61, CC-T77]. The [module-design](module-design.md) guide covers interfaces more broadly.

### Remove duplication now, or wait for more copies?
- **Legacy Code:** Remove small duplicated fragments as you work, since each small removal is safe and reveals larger duplication [WELC-T50].
- **Refactoring:** Unify copies at the third similar case, or sooner when a bug or feature exposes them, after comparing near-duplicates [REF-P4].
- **Pragmatic Programmer:** Identical-looking code may encode different rules that change separately [PP-P3].
- **Decide:** Remove a copy now when the change you are making touches it and the copies encode the same rule, making them identical first [WELC-T50, REF-P4, TDD-T11]. Leave copies that may encode different rules, or code that never changes, as they are [PP-P3, REF-P4]. The [refactoring](refactoring.md) guide covers this trade-off in full.

## Review checklist

- [ ] Tests pinning the touched behaviour exist in the diff, or in earlier commits, before the change commits [WELC-P1, CC-T75, TDD-T45].
- [ ] Each legacy method that a changed call site now uses has tests [WELC-T73].
- [ ] The PR names each changed method, the paths its effects travel and the test that observes it [WELC-P7, WELC-T32].
- [ ] Characterization tests reach every branch whose lines appear in the diff, including boundary and conversion inputs [WELC-T40, WELC-T41].
- [ ] Notes record each new characterization test failing after an injected fault [REF-T02, REF-T03].
- [ ] Surprising behaviour is marked `SUSPICIOUS` with a reason and follow-up, not silently fixed [WELC-T38].
- [ ] The first dependency-breaking commit changes only signatures or adds interfaces, and extracted methods keep the original parameter lists [WELC-T05, WELC-T60].
- [ ] Dependency breaks precede the test commit and were read by a second person [WELC-T06, WELC-T59].
- [ ] Constructors receive dependencies as parameters, and any old constructor only forwards to the new one [WELC-T62, WELC-T63].
- [ ] Production wrappers around globals, statics and library classes only forward [WELC-T09, WELC-T30, WELC-T70].
- [ ] Static setters and singleton resets are called only from test setup and teardown [WELC-T25, WELC-T26].
- [ ] Fakes live in test sources, store only what tests assert, and production never references them [WELC-T08].
- [ ] Test subclasses override only the methods that reach dependencies, not the method under test [WELC-T23, WELC-T29].
- [ ] Widened access is narrowed later, and sensing variables are removed when the refactoring ends [WELC-T27, WELC-T39].
- [ ] New logic lives in a new method or class with its own test, and the legacy method gains only a call [WELC-P4, WELC-T12, WELC-T14].
- [ ] Extractions in a monster method were made by a safe tool with no hand edits between them, or hand signatures were checked [WELC-T54, WELC-T56].
- [ ] Extracted classes appear in a change that also modifies one of their methods [WELC-T47].
- [ ] Core logic classes import no service or library classes [WELC-T42, WELC-T44].
- [ ] Replacement plans have several cutover steps, and removal follows the release that introduced the replacement [RI-T53, SWE-T28].
- [ ] Unrelated legacy areas are untouched by the change [WELC-P8].

## More entries in this area

- `WELC-T15` — Build and test each class alone: in compiled projects with long builds, arrange each class so its test target compiles without unrelated modules, keeping edit-to-test loops under about ten seconds. Interpreted languages usually give fast feedback already.
- `WELC-T17` — Put interfaces at volatile dependencies: when a class depends on a concrete class whose implementation changes often, depend on an interface so edits there do not force recompiles.
- `WELC-T20` — Add a variant by subclassing: override only the method that differs when a class needs one variant and a quick test matters, but not when variations must combine or several subclasses need the method (see the inheritance tension).
- `WELC-T21` — Make parent methods abstract instead of overriding: when several subclasses each need their own version of a method, declare it abstract in the parent, though a few concrete overrides that keep substitutability and call the parent are acceptable.
- `WELC-T10` — Substitute preprocessor definitions in C: replace a C or C++ dependency with test-only macros or headers when nothing else can override the call, and not when heavy preprocessing makes production code hard to maintain.
- `WELC-T24` — Stub a heavy method in tests: in a linked, compiled language, link an empty body for a construction-time method only into the test program, only for the worst first dependencies and not when other test files need the original.
- `WELC-T67` — Replace free functions with an interface: when the same free functions are called from many methods and classes, declare one virtual method per function and pass the implementation in, but parameterize the single method when all calls sit in one place.
- `WELC-T68` — Replace a C function with a function pointer: in procedural code where object or link seams are impractical, call through a pointer assigned at startup, unless the team considers function pointers too unsafe.
- `WELC-T71` — Use a lazy getter for constructor-created objects: in C++, when a constructor-created object is used by many methods, read it through a getter tests can override, and free fakes as production frees objects, but override one call instead when only one method uses it.
