# Refactoring moves

This guide covers the concrete restructuring moves and the mechanics that keep each one safe: renames, extract and inline, moving functions and fields, splitting loops and variables, merging duplicates, replacing conditionals, special cases, inheritance versus delegation, dead code and mutable data. The single most important idea is that every move has a safe order of steps, and in most of them the old shape keeps working until every caller has moved to the new one.

**Read this when:** renaming a function, field or published API, extracting or inlining a function, moving a function or field to another module, splitting a loop or a reused variable, merging duplicated code, replacing a type switch or a null check, turning a subclass into a delegate, deleting code you believe is unused, or tightening who may change shared data.

**Entry IDs** such as `WELC-T12` point to `../books/<book>/techniques.md` (T) or `principles.md` (P);
the prefix table is in [SKILL.md](../SKILL.md).

Session discipline (small steps, a test run after each, separate structure commits, revert on red) is in [change-workflow](change-workflow.md) [REF-P1, REF-T09, REF-T10], and building the safety net is in [testing](testing.md) and [legacy-code](legacy-code.md).

## Contents

- [Rules: tools, renames and signatures](#rules-tools-renames-and-signatures)
- [Rules: extract and inline](#rules-extract-and-inline)
- [Rules: variables, loops and queries](#rules-variables-loops-and-queries)
- [Rules: moving code between modules](#rules-moving-code-between-modules)
- [Rules: duplication](#rules-duplication)
- [Rules: conditionals and special cases](#rules-conditionals-and-special-cases)
- [Rules: inheritance and delegation](#rules-inheritance-and-delegation)
- [Rules: dead code and mutable data](#rules-dead-code-and-mutable-data)
- [Playbooks](#playbooks)
- [Where the books disagree](#where-the-books-disagree)
- [Review checklist](#review-checklist)
- [More entries in this area](#more-entries-in-this-area)

## Rules: tools, renames and signatures

### 1. Let a refactoring tool make renames and extractions

Use an automated refactoring command for renames, signature changes and helper extractions instead of hand edits, then run the tests. A tool finds every reference that manual replace misses, and changes a name and all its callers in one step. [REF-T14, TF-T18] An edit reaching hundreds of files belongs to a generated, sharded change, described in [change-workflow](change-workflow.md). [SWE-T03]

- **Do:** Run the tool's command, update comments that mention the old name, and run the suite.
- **Not when:** Without static typing, check the tool's matches by hand, although mature tools handle reflective calls well. When the sweep is huge, ship that change on its own and quickly. [REF-T14, TF-T18]
- **Check:** The rename or extraction is one commit with no hand-edited call sites, related comments are updated, and a test run follows it. [REF-T14, TF-T18]

### 2. Rename one identifier per step

Rename one identifier at a time, apart from any parameter change, so a failing test points at one rename. [REF-T15] When a field is referenced from many functions or modules, first put accessors in front of it, so the rename happens behind them rather than at every reference. [REF-T16] Choosing the new name is covered in [readable-code](readable-code.md). [REF-P3, REF-T20]

- **Do:** Commit the accessors first, then the rename, then any parameter change, each with a passing test run.
- **Not when:** Skip the accessor step when outside code needs a forwarder instead (rule 3), or when the record has limited scope. [REF-T16]
- **Check:** Each rename commit changes exactly one identifier and no parameters, and the accessor commit precedes the rename commit. [REF-T15, REF-T16]

### 3. Keep the old name working until every caller moves

Let old and new names coexist, adding the new field before removing the old one and reading the new one first, and move callers one at a time so the code works between steps. [REF-T17, TF-T25] When the current interface is awkward, write the one you wish existed and implement it by calling the existing routine, so callers shape it. [TF-T09] For a function other teams or customers call, keep the old declaration as a deprecated forwarder, and remove it once no known caller uses it. [REF-T18] Coordinating removal across owners is covered in [project-and-team](project-and-team.md). [SWE-P7]

- **Not when:** Callers you control can be updated together, and some interfaces must stay forever. [REF-T18] Automated rewrite tools can convert every caller at once. [TF-T25]
- **Check:** The new field exists in a commit before the old one is removed, the old name carries a deprecation marker, the new interface only delegates while callers move, and callers of the old name decrease to zero. [REF-T17, REF-T18, TF-T09, TF-T25]

```python
def total_due(invoice):            # new name holds the real body
    return sum(line.amount for line in invoice.lines)

def calc(invoice):                 # old published name, kept for outside callers
    """Deprecated: call total_due instead."""
    return total_due(invoice)
```

### 4. Replace a flag argument with named functions

When a boolean, enum or string argument selects between behaviors, give each behavior its own named function, which keeps the behaviors apart. [REF-T83]

- **Not when:** The argument is computed at runtime rather than written as a literal at the call sites. [REF-T83]
- **Check:** The flag parameter is gone from the signature, and call sites call the named functions. [REF-T83]

## Rules: extract and inline

### 5. Extract an effortful block into a function named for its purpose

Move a fragment that takes effort to read into a function named for what it does, so readers stop re-deriving its purpose. This covers a block a comment introduces, a loop with its body, a large switch branch, and a hard-to-read condition with its branches. [REF-T22, REF-T23, REF-T24, CC-T31] The best candidates have one clear purpose and read few values from the rest of the routine. [TF-T17]

- **Do:** Name the helper for its intent rather than its steps.
- **Not when:** A helper that only restates one statement, or only forwards one call, adds reading cost and hides nothing, so leave that code in place, except a forwarder that serves as a vendor adapter. [CC-T33, CC-T51] The trade-off is set out in [Extract or inline a small function?](#extract-or-inline-a-small-function).
- **Check:** Blocks that comments used to introduce now appear as named calls, complex conditions are named predicate calls, and each helper's parameters are exactly the values the block reads. [REF-T22, REF-T24, TF-T17]

### 6. Slide related statements together before extracting them

Move related statements toward each other one step at a time, so they can later move as one block, and reorder side-effect-free statements freely. [REF-T40] Order initializations by data dependency, so each initializer reads only values set above it. [TF-T34]

- **Not when:** Do not slide a statement past one that assigns data the fragment uses, or past code whose side effects you cannot tell. [REF-T40]
- **Check:** The fragment is contiguous before extraction, a move that broke a test was undone, and each initializer reads only values initialized above it. [REF-T40, TF-T34]

### 7. Give an extracted function read-only inputs and one output

Pass in the surrounding locals that extracted code only reads, and return the one variable it changes, which keeps its effects visible. [REF-T36] Before extracting an expression into a variable, confirm it has no side effects, because moving it changes when and how often it runs. [REF-T25] Declare each variable an extraction or split creates as read-only, so a later reassignment is a visible error. [REF-T26]

- **Do:** List the locals the block reads and writes before extracting.
- **Not when:** Two or more locals change inside the block, so simplify them first by splitting variables and replacing temporaries with queries (rules 13 and 14). [REF-T36, REF-T35, REF-T27]
- **Check:** The new function takes read-only values as parameters and returns its changed value, and each new variable's initializer contains no assignments or state-changing calls. [REF-T36, REF-T25, REF-T26]

```javascript
// The block read `account` and changed one local, so the local becomes the return value.
function reportBalance(account) {
  const unpaid = sumUnpaid(account);   // read-only result
  printSummary(account, unpaid);
}
function sumUnpaid(account) {
  let total = 0;
  for (const bill of account.bills) if (!bill.paid) total += bill.amount;
  return total;
}
```

### 8. Hold tangled state in an object only after simplifying the locals

When locals and arguments still tangle a function after splitting and replacing what you can, move it into a command class with one method, named after the function, holding its arguments and locals as fields. Helpers can then split out without passing the same values around. [REF-T81, CC-T35]

- **Not when:** Plain functions usually suffice, and changing locals should be split first (REF-T35, REF-T27). [REF-T81] Static fields shared by several threads can break the helpers. [CC-T35]
- **Check:** The original function only creates the command and calls it, the class is named after the function, and helpers share state through instance fields rather than static ones or extra parameters. [REF-T81, CC-T35]

### 9. Inline functions and forwarders that add nothing

Inline a function whose body reads as clearly as its name, a class that only wraps one function, and chains of functions that only forward to the next. Needless indirection makes calls hard to trace and adds an interface that teaches nothing. [REF-T44, REF-T45, POSD-T04]

- **Not when:** Overridden forwarders stay (rule 10). A delegate left behind by a move (rule 16) or a deprecated forwarder for outside callers (rule 3) may stay. [REF-T45] An external interface that must stay unchanged justifies a forwarding wrapper. [POSD-T04] See [Keep or remove a forwarding layer?](#keep-or-remove-a-forwarding-layer).
- **Check:** The diff deletes single-call wrappers no clearer than their names, and call chains hold no function whose only logic is forwarding, apart from the exceptions above. [REF-T44, REF-T45, POSD-T04]

### 10. Do not inline overridden, recursive or multi-exit methods

Do not inline a method that a subclass overrides, that calls itself, that has several returns, or that reads fields the call site cannot reach. Inlining an overridden or self-calling method changes which code runs. [REF-T42]

- **Check:** An inlined method had none of these properties, and a method with any of them was left as a call. [REF-T42]

### 11. Inline a badly split group, then extract along better lines

When a group of functions mixes purposes, inline them into one routine and extract along better boundaries. Wrong boundaries are hard to fix while the pieces stay separate, and interacting small pieces can be harder to follow than one routine. [REF-T41, TF-T19]

- **Do:** Inline pieces that interact through long argument lists, repeats, poor names or shared mutable data, then tidy and re-extract.
- **Not when:** A small change needs only moving statements into callers (rule 17). [REF-T41] Pieces that are each still clear alone stay as helpers. [TF-T19]
- **Check:** The fragmented helpers are inlined, and each new function serves one purpose that its name states. [REF-T41, TF-T19]

## Rules: variables, loops and queries

### 12. Split a loop that builds two unrelated results

Split a loop that accumulates two different values into one loop per result, so each updates only its own accumulator and can be tested alone. [REF-T32] In a language with first-class functions, a loop that only filters or maps can then become a pipeline, one behavior at a time, which states what happens to each item without an accumulator. [REF-T33]

- **Do:** Duplicate the loop, delete one accumulator from each copy, remove side effects that would now run twice, and keep a pipeline's source collection in its own variable.
- **Not when:** Profiling shows the loop is a real bottleneck, and side-effect-free work duplicated in both loops may stay. [REF-T32] Loop bodies with side effects or early exits stay as loops. [REF-T33] Performance work is covered in [performance-and-concurrency](performance-and-concurrency.md). [REF-T87]
- **Check:** Each resulting loop updates only its own accumulator, no side effect runs twice, and loops that only filter or map are pipelines. [REF-T32, REF-T33]

### 13. Split a variable that holds several purposes

Give each separate purpose of a reused variable its own variable, splitting in stages, because readers otherwise have to track which value it holds at each point. [REF-T35, POSD-T25] Declare each new variable read-only. [REF-T26]

- **Not when:** A collecting variable that accumulates a running total is not split. [REF-T35]
- **Check:** Each resulting variable is assigned in one place within the function and uses a read-only declaration. [REF-T35, REF-T26]

### 14. Compute derived values instead of storing them

Replace a computable temporary with a query function read wherever the temporary was, so no stale copy exists. [REF-T27] For a stored variable that can be recalculated, list every assignment, add a query, assert the two match, then switch readers to the query. [REF-T30] Compute a total from its source records on read, after splitting out any non-zero initial value, so adding a record updates one place. [REF-T31]

- **Not when:** Snapshot variables, which must keep an earlier value, stay variables, and a query at the top level that would need many parameters stays a temporary. [REF-T27] When the source data is immutable, the total can be immutable too, so it need not be derived on every read. [REF-T31]
- **Check:** The temporary or stored variable is gone, no code reads or assigns it, and a test adds a record and asserts the computed total. [REF-T27, REF-T30, REF-T31]

### 15. Split a function that both computes and changes state

Move the pure calculation into a query and leave the state change in a separate modifier, so each stays predictable and can be tested apart. [REF-T29, CC-T28] The general rule that value-returning functions avoid side effects is in [readable-code](readable-code.md). [REF-T28]

- **Not when:** An atomic query-and-change, such as a stack pop, may stay together. [CC-T28] Caching a query's result is acceptable. [REF-T28]
- **Check:** The query contains no writes, and the modifier returns nothing callers depend on. [REF-T29]

## Rules: moving code between modules

### 16. Move a function to its data, keeping the old home working

Move a function into the module holding most of the data it uses, after checking that it neither overrides nor is overridden, because data and its behavior usually change together. [REF-T48] Copy it to the new home, make the original delegate, and redirect callers one at a time, so the original works until every caller arrives. [REF-T49] Before moving a field, route all its reads and writes through accessors, so they are replaceable during the move. [REF-T51]

- **Not when:** Behavior that varies independently of its data may fit Strategy or Visitor instead, as covered in [design-patterns](design-patterns.md). [REF-T48] The source function may stay indefinitely as a delegate. [REF-T49] If the class itself routinely needs the accessors for its own use, that signals the class is too big, and a bare record makes the move trickier. [REF-T51]
- **Check:** The moved function called more members of the other object than of its own, nothing overrides it, the field is reached only through getters and setters, and tests pass against the new home. [REF-T48, REF-T49, REF-T51]

### 17. Move statements across the call boundary to fit their callers

When every call to a function is followed by the same statements, slide them beside the call and move them into the function, extracting one call site first if there are several callers. [REF-T54] When shared behavior must differ in some calls, move the varying statements out into those callers, so the shared function holds only what every caller needs. [REF-T55]

- **Not when:** The repeated statements do not fit the called function's purpose. [REF-T54]
- **Check:** Callers no longer repeat the moved statements, the shared function is identical for every caller, and varying code sits in the callers. [REF-T54, REF-T55]

### 18. Remove a middle man that mostly forwards

When most methods of a class only delegate to another class, let clients call the object that does the work, and remove the delegating accessor once nothing uses it. Forwarding then adds coupling without hiding anything. [REF-T46] Deciding how much to hide behind an interface is covered in [module-design](module-design.md).

- **Not when:** Some delegation is good encapsulation, so keep forwarders that hide a dependency on purpose. [REF-T46]
- **Check:** Callers reach the working object directly, and no middle-man behavior remains. [REF-T46]

## Rules: duplication

### 19. Unify copies that encode one piece of knowledge

Keep each rule or calculation in one place, because duplicated code makes every change happen several times and a missed copy becomes a defect. [REF-P4, PP-P3] TDD reads repeated logic or data as a missing concept, so remove the copy and name the concept that owns it. [TDD-P5] Merge copies that change together for the same reasons, and factor a long repeated snippet into one method with a short signature. [CC-T36, POSD-T34] Timing is in [When should copies be merged?](#when-should-copies-be-merged).

- **Do:** Search for other copies before finishing, compare near-duplicates line by line, then extract one shared version and point every site at it.
- **Not when:** Near-duplicates may differ for real reasons, and code that never changes may keep its copies. [REF-P4] Identical-looking code may encode different rules that change separately. [PP-P3] Copies that serve different actors, or a repeat of two or three stable lines, stay apart. [CC-T36] Very short snippets gain little, and snippets that would need many arguments lose value. [POSD-T34] A quick copy may wait until the work is shared. [TDD-P5]
- **Check:** No two functions in the changed area implement the same rule, the repeated snippet is written once, and its helper has a short signature. [REF-P4, POSD-T34]

### 20. Make near-copies identical before merging them

Make two similar methods or loops identical in small steps, and merge them only when every line matches, because an early merge hides a real difference a later test would expose. [TDD-T11] Align look-alike subclass methods by matching names and parameter order, and pull up the members they use first. [REF-T78] When a function nearly does what a new feature needs but has fixed values, add a parameter for each differing literal and pass it at every caller, instead of copying it. [REF-T39]

- **Not when:** Ordinary duplicates wait for a third similar case before you parameterize them. [REF-T39, REF-P4]
- **Check:** The two versions are identical in the diff before one is removed, methods in the same role share one name and signature, and no copied function differs from its original only in literals. [TDD-T11, REF-T78, REF-T39]

### 21. Replace copies and hand-written equivalents with calls

After an extraction passes its tests, replace each identical or equivalent copy with a call to it, since copies drift apart and one fix would miss the others. [REF-T38] Replace hand-written code that does what an existing function or library call does with a call to that function. [REF-T56]

- **Not when:** Near-copies that differ only in literals belong to rule 20. [REF-T38] Keep the hand-written code when the function's name reads poorly at the call site, or when the similarity is coincidental. [REF-T56]
- **Check:** No copy of the extracted logic remains, each hand-written block became one call, and the tests pass. [REF-T38, REF-T56]

### 22. Keep one traversal and pass in the varying work

When several features walk the same nested structure in the same way, keep the traversal in one place and pass the varying work in as a function, so the loops change in one place only. [CC-T37]

- **Not when:** Languages without lambdas need a strategy, command or template method instead, as described in [design-patterns](design-patterns.md). [CC-T37]
- **Check:** No identical nested loops remain across classes with only the body changed. [CC-T37]

### 23. Pick one form for a repeated idiom

When the same logic appears in several styles, choose one form and convert the variants, one kind of variation per tidying, so each diff stays small and checkable. [TF-T08]

- **Do:** Convert one kind of variant per tidying, and leave the other kinds for later tidyings.
- **Check:** The idiom appears in one form, and each tidying commit changes one kind of variation. [TF-T08]

## Rules: conditionals and special cases

### 24. Flatten wrapping conditions and combine checks with one result

Replace a condition that wraps all the remaining code of a routine with an early return, which removes a level of nesting. [TF-T06, REF-T65] When several checks lead to the same result, first move any assignment or state-changing call out of the conditions, then join the checks into one condition that states the rule once. [REF-T66]

- **Not when:** The condition covers only part of the routine, or guards would pile up and hurt readability. [TF-T06] Both legs are normal cases, or a single exit point is clearer. [REF-T65] Truly independent checks are not merged. [REF-T66]
- **Check:** Early returns precede the remaining logic with few guards, and adjacent checks with identical results became one condition with no assignments in it. [TF-T06, REF-T66]

### 25. Replace a repeated type switch with polymorphism

When several functions switch on one type code and behavior differs by type, replace the switch with overriding subclasses and client type checks with a superclass method, so each type's behavior lives in one place and a new type adds one class. [REF-T58, CC-T38] Keep a plain type code unless behavior varies by type. [REF-T69] Keep an unavoidable switch in one factory behind an interface, so the rest of the system depends on the interface, not on type codes. [CC-T39] Whether to replace it at all is in [Polymorphism or a switch?](#polymorphism-or-a-switch).

- **Do:** Create a subclass per type and a factory that selects it before removing any branch. [REF-T59] Override each leg in its subclass, and keep the common calculation and the default case in the base. [REF-T60] Where every subclass must provide a method, make the base version throw an error that names the missing responsibility, so a forgotten override fails at once. [REF-T63]
- **Not when:** Only one function uses the type field, no behavior varies by type, or the type changes during an object's life, which calls for a delegate (rule 27). [REF-T58, REF-T69] The switch covers few cases unlikely to grow, or behavior changes more often than the types do. [CC-T38, CC-T39] With indirect inheritance, the selection logic may stay in the constructor. [REF-T59] If the superclass should be abstract, declare the method abstract. [REF-T60] In a static language, declare an abstract member instead of a throwing one, and a shared default belongs in the base rather than in a throwing stub. [REF-T63]
- **Check:** Adding one type touches only the factory, no client tests for a concrete subclass, each subclass overrides its own leg, the base holds the common rule, and base methods that must be overridden throw an error naming the responsibility or are abstract. [REF-T58, REF-T59, REF-T60, REF-T63, CC-T38, CC-T39]

### 26. Replace repeated marker checks with a special-case object

When many clients test for the same special value before doing the same thing, return a special-case object instead, make it immutable, and give it methods for the common responses, so clients stop repeating the check. [REF-T67] When input arrives as plain records and no class holds the special case, add a transform that swaps sentinel values for special-case objects, and move clients across one at a time. [REF-T68] Wider guidance on absence and empty states is in [errors-and-contracts](errors-and-contracts.md).

- **Do:** Keep the old marker check in a client while both forms can still reach it, and have nested properties return special cases rather than null.
- **Not when:** A client that needs a different response keeps its explicit check. [REF-T67]
- **Check:** No client compares the marker, nested properties return special cases rather than null, and transformed records contain no sentinel strings. [REF-T67, REF-T68]

```python
class MissingAuthor:
    """Returned when a post has no author record. Holds no mutable state."""
    display_name = "Anonymous"
    def is_missing(self): return True
    def avatar_url(self): return DEFAULT_AVATAR

def author_of(post):
    return post.author if post.author is not None else MissingAuthor()

# Before: each client wrote `if post.author is None: ... else: ...`
# After:  clients call author_of(post).display_name directly.
```

## Rules: inheritance and delegation

### 27. Switch a subclass to a delegate when inheritance stops fitting

Replace a subclass with a delegate when behavior must vary on two axes, when the variant changes at runtime, or when subclasses depend on parent internals, because inheritance varies an object along only one axis. [REF-T70] Replace a subclass that inherits parent methods it does not support with a delegate, so it stops carrying an interface that makes no sense for its role. [REF-T71] Design Patterns states the general preference for holding collaborators over subclassing, discussed in [design-patterns](design-patterns.md). [GOF-P3]

- **Do:** Confirm that one trigger applies before converting: a second axis, a runtime switch, a dependency on parent internals, or a refused interface whose confusion is real.
- **Not when:** Starting with inheritance is fine until it causes problems. [REF-T70] Subclassing for reuse that confuses no one can stay. [REF-T71] Inheritance still helps when new components must combine with existing ones, and heavy composition hurts understanding. [GOF-P3]
- **Check:** The code swaps a live object's variant or has a second independent axis of variation, or the former subclass no longer inherits methods it would refuse. [REF-T70, REF-T71]

### 28. Convert inheritance to delegation one member at a time

When replacing a superclass with a delegate, write a forwarder for each superclass member the subclass uses, and remove the inheritance link last, so the link stays valid until every member is forwarded. [REF-T72] When turning a subclass into a delegate, move one method at a time to the delegate, testing after each, and dispatch to the delegate when it is present. [REF-T74]

- **Do:** Test each group of forwarders before the next, test a getter and setter pair only once both are forwarded, and delete the subclass when it is empty.
- **Not when:** A delegate override that calls super must not recurse into itself, so extract the base calculation first. [REF-T74]
- **Check:** Each commit moves one method or one tested group of forwarders, and no emptied subclass remains. [REF-T72, REF-T74]

### 29. Pull shared parts up after aligning them, and collapse what no longer differs

When classes duplicate data and behavior and inheritance unifies them more simply than delegation, pull the shared fields up through a new superclass constructor first, then move matching accessors and methods one at a time. Shared data is the stable core, so methods follow it safely. [REF-T80] Align near-duplicate methods before pulling them up (rule 20). [REF-T78] When a subclass and its parent no longer differ enough to justify two classes, merge them, since a hierarchy without a real difference only adds indirection. [REF-T75]

- **Not when:** Delegation fits the shared behavior better, though the classification of the domain can hint at inheritance. [REF-T80] When neither name fits the merged class well, pick one arbitrarily. [REF-T75]
- **Check:** The superclass constructor stores the shared fields, subclasses drop the matching accessors, a merged-away class has no members left, and the survivor's name fits all members. [REF-T80, REF-T75]

## Rules: dead code and mutable data

### 30. Delete dead code once you have confirmed it is unused

Delete code that can no longer be reached, or that only tests call, instead of commenting it out, and rely on version control to restore it. Commented-out code confuses readers and goes stale, and every unused line still costs upkeep. [REF-T57, TF-T07, SWE-T04, CC-T73] Search for callers first, and when reflection could hide callers, add usage logging and delete only after the log shows no use. [TF-T33]

- **Not when:** Readers who cannot see the history need to know the code existed, so leave a one-line comment naming it. [REF-T57] Commented-out code used only during local debugging, and never committed, is fine. [CC-T73] If you would want the code later but it no longer works or would be used differently, plan to rewrite it rather than restore it. [TF-T07] Code that still delivers more value than its upkeep stays, and code whose purpose is unclear needs its reason learned first, as covered in [legacy-code](legacy-code.md). [SWE-T04, SWE-T62]
- **Check:** No commented-out code remains, a search finds no references to the deleted code, and the PR shows logging or a period with no recorded calls when reflection was possible. [REF-T57, TF-T07, TF-T33, SWE-T04]

### 31. Route changes to shared mutable data through one function

Refactoring treats mutable data as a major source of problems, so route updates to shared mutable data through one function and keep changing variables in the narrowest scope, which makes each change visible and controllable. [REF-P5] Returning new values instead of mutating is covered in [functional-style](functional-style.md). [FPS-P2]

- **Not when:** Immutable data needs no accessor wrapper. Mutable data often cannot be removed, and data that one small function uses may stay local. [REF-P5]
- **Check:** Direct writes to shared fields moved into accessors or one update function, and changing variables have short scopes. [REF-P5]

### 32. Copy data before changing or exposing it

Copy a collection or record before changing data you did not create, and return copies from getters of mutable data, because a change to shared data reaches every reader. [REF-T86] Note that a copy protects only its top level. [REF-P5] Keeping internal representations out of accessors is covered in [module-design](module-design.md). [POSD-T52]

- **Not when:** Callers that change shared data on purpose break when they receive a copy, so tests must catch them. [REF-T86]
- **Check:** In-place sorts and added fields run on a copy, and getters of mutable data return a clone. [REF-T86]

### 33. Share one catalogue item by reference through a repository

When several objects hold their own copies of one catalogued item, link them to one shared object instead, so an update reaches every holder at once. [REF-T76] Retrieve each shared item by its identifier from a repository that holds one instance per entity. [REF-T77] Value objects, the opposite choice, are covered in [domain-modeling](domain-modeling.md). [REF-T84]

- **Not when:** A per-object component is enough when the data is never shared. [REF-T76] When the shared data never changes, separate copies are reasonable. [REF-T77]
- **Check:** Each object reads one shared object for matching data and stores its own ID, and constructors take the item ID from the input record. [REF-T76, REF-T77]

## Playbooks

### When you rename a widely used or published name
1. If the name is a field used across many modules, put accessors in front of it and commit that alone. [REF-T16]
2. Add the new name and make the old one forward to it, reading the new field first. [REF-T17, REF-T18]
3. If outside teams or customers call the old name, mark the forwarder deprecated. [REF-T18]
4. Use the refactoring tool to change call sites you control, one identifier per commit, with no parameter changes mixed in. [REF-T14, REF-T15, TF-T18]
5. Move remaining callers one at a time until none uses the old name. [TF-T25]
6. Delete the old name once no known caller uses it, or keep it if the interface has to stay. [REF-T18]

### When you break up a long function with tangled locals
1. Slide related statements together, respecting data dependencies. [REF-T40, TF-T34]
2. Split any variable that holds several purposes, and declare the parts read-only. [REF-T35, REF-T26]
3. Replace computable temporaries with queries. [REF-T27]
4. Extract each purposeful block, passing read-only locals in and returning the one changed value. [REF-T22, REF-T36]
5. If two or more changing locals still block extraction, move the function into a command object and extract helpers that share its fields. [REF-T81, CC-T35]
6. Replace any copies of the extracted logic elsewhere with calls. [REF-T38]
7. If the result is a cluster of helpers that must be read together, inline them and re-extract along better lines. [REF-T41, TF-T19]

### When you move a function or field to another module
1. Confirm the function uses more of the other module's data than its own, and that it neither overrides nor is overridden. [REF-T48]
2. For a field, route every read and write through accessors first. [REF-T51]
3. Copy the function to the new home and make the original delegate to it. [REF-T49]
4. Run the tests against the new home, then redirect callers one at a time. [REF-T49]
5. Move statements that every caller repeats into the function, and statements that vary out to the callers. [REF-T54, REF-T55]
6. Inline the old delegate when nothing outside your control calls it, or keep it on purpose. [REF-T45, REF-T49]

### When you replace a type switch with polymorphism
1. Confirm that several functions switch on the type, that behavior differs by type, and that the type is fixed for an object's life. [REF-T58, REF-T69, CC-T38]
2. Create one subclass per type and a factory that selects it, and route callers through the factory. [REF-T59, CC-T39]
3. Override one leg of the switch at a time in its subclass, testing after each. [REF-T60, REF-T09]
4. Keep the common calculation and default in the base, and make required methods abstract or throw an error naming the missing responsibility. [REF-T60, REF-T63]
5. Replace client type checks with a superclass method, and delete the emptied switch. [REF-T58]

### When you replace a subclass with delegation
1. Confirm which trigger applies: two axes, a runtime variant change, dependence on parent internals, or a refused interface. [REF-T70, REF-T71]
2. Create the delegate and give the host a field that holds it. [REF-T70, GOF-P3]
3. For a superclass link, write forwarders for each used member, testing each group, and remove the link last. [REF-T72]
4. For a subclass, move one method at a time to the delegate and dispatch to it when present, extracting the base calculation first where an override calls super. [REF-T74]
5. Delete the subclass once it is empty. [REF-T74]

### When you merge duplicated code
1. Confirm that the copies encode one rule that changes together for the same reason. [CC-T36, PP-P3]
2. Make near-copies identical in small steps, aligning names and parameter order. [TDD-T11, REF-T78]
3. Turn literals that differ into parameters. [REF-T39]
4. Extract the shared version, then replace every copy and every hand-written equivalent with a call. [REF-T38, REF-T56]
5. For subclasses, pull shared fields up first and methods after. [REF-T80]
6. Search once more for copies before finishing. [REF-P4]

## Where the books disagree

### When should copies be merged?
- **Refactoring:** Unify at the third similar case, or sooner when a bug or feature exposes the copies. [REF-P4]
- **TDD:** Remove duplication right after the test passes, though a quick copy may wait until the work is shared. [TDD-P5, TDD-T10, TDD-T32]
- **Clean Code:** Merge only copies that change together for the same actor. [CC-T36]
- **POSD:** Factor long snippets, but not very short ones or ones needing many arguments. [POSD-T34]
- **Pragmatic Programmer:** Keep one representation of each fact, but identical-looking code may encode different rules. [PP-P3]
- **Decide:** First ask whether the copies change together for the same reason or actor. If not, keep them apart. [CC-T36, PP-P3] If they do, merge when a third similar case appears, when a bug or feature exposes the copies, or before sharing copies you made to reach green. [REF-P4, TDD-P5, TDD-T32] Leave copies that are short and stable, that would need many arguments, or that sit in code that never changes. [CC-T36, POSD-T34, REF-P4] Between a third case and right after green, the entries give no further deciding condition, so follow the codebase's existing convention.

### Extract or inline a small function?
- **Refactoring:** Extract an effortful fragment, even a single call when a name helps, and inline a wrapper that says no more than its name. [REF-T22, REF-T19, REF-T44]
- **Clean Code:** Extract only when the helper's name is more abstract than the code it hides. [CC-T33]
- **Tidy First:** Extract a block with one purpose and few links, and inline fragments that interact heavily. [TF-T17, TF-T19]
- **POSD:** Split a method only when callers gain simplicity and each half reads alone. [POSD-T35]
- **Decide:** Extract when the name tells the reader something the block does not show at a glance and the block reads few outside values. [REF-T22, CC-T33, TF-T17] Inline when reading the body teaches no more than reading the name, or when the pieces must be read together. [REF-T44, TF-T19, POSD-T35] Function length as such is debated in [readable-code](readable-code.md).

### Promote tangled locals to fields, or simplify them first?
- **Clean Code:** When a block modifies two or more locals, promote them to fields of one object. [CC-T35]
- **Refactoring:** Simplify changing locals first, and use a command object only when tangling remains. [REF-T36, REF-T81]
- **Decide:** Split multi-purpose variables and replace computable temporaries first. [REF-T35, REF-T27] If two or more changing locals still block extraction, move the function into a command object or promote the locals to instance fields. [REF-T81, CC-T35] Do not use static fields that several threads share. [CC-T35]

### Polymorphism or a switch?
- **Refactoring:** Replace a type-code switch when several functions switch on it and behavior differs, keep a plain code otherwise, and delegate when the type changes at runtime. [REF-T58, REF-T69, REF-T70]
- **Clean Code:** Replace a switch that repeats or that new types keep extending, but keep one with few stable cases or whose behavior changes more often than its types. [CC-T38, CC-T39]
- **Decide:** Replace the switch when the same switch repeats across several functions and behavior differs by type. [REF-T58, CC-T38] Keep it when only one function uses it, no behavior varies, the cases are few and unlikely to grow, or behavior changes more often than types. [REF-T58, REF-T69, CC-T38] A single switch that new types keep extending is a replacement case for Clean Code but not for Refactoring, and the entries give no further deciding condition, so follow the codebase's existing convention. [CC-T38, REF-T58] If the type changes at runtime, use a delegate. [REF-T70] Wherever a switch remains, put it in one factory, unless behavior changes far more often than the types do. [CC-T39, REF-T59]

### Inherit or delegate?
- **Refactoring:** Inheritance is fine until it causes problems, and subclassing for reuse may stay when it confuses no one. Extract a superclass when that unifies classes more simply than delegation. [REF-T70, REF-T71, REF-T80]
- **Design Patterns:** Reuse behavior through a collaborator field, not a subclass made only to reuse code, within the limits listed in rule 27. [GOF-P3]
- **Decide:** In existing code, keep a working hierarchy until one of the delegation triggers appears, then convert it member by member. [REF-T70, REF-T71, REF-T72] The books differ on subclassing only for reuse: Refactoring tolerates it when it causes no confusion, and Design Patterns advises against it. [REF-T71, GOF-P3] The entries give no further deciding condition, so follow the codebase's existing convention and see [design-patterns](design-patterns.md) for new designs.

### Keep or remove a forwarding layer?
- **Refactoring:** Inline pure forwarders and remove middle men, but keep deprecated forwarders for outside callers and delegation that encapsulates well. [REF-T45, REF-T46, REF-T18, REF-T49]
- **POSD:** Remove pass-through methods unless an external interface must stay unchanged. [POSD-T04]
- **Clean Code:** A forwarding helper is not worth extracting, except a vendor adapter. [CC-T33, CC-T51]
- **Decide:** Remove a forwarder when every caller is code you control and the layer hides nothing. [REF-T45, REF-T46, POSD-T04] Keep it when outside callers use the name, when an external interface must not change, when a subclass overrides it, or when it deliberately hides a dependency such as a vendor API. [REF-T18, POSD-T04, REF-T42, CC-T51]

## Review checklist

- [ ] Renames and extractions come from a tool command, one identifier per commit, with no parameter change mixed in. [REF-T14, REF-T15, TF-T18]
- [ ] A renamed published function keeps a deprecated forwarder, and callers of the old name decrease toward zero. [REF-T18, TF-T25]
- [ ] No boolean, enum or string literal argument selects between behaviors at call sites. [REF-T83]
- [ ] Each extracted helper takes read-only values, returns at most one changed value, and new variables are read-only with side-effect-free initializers. [REF-T36, REF-T25, REF-T26]
- [ ] No inlined method was overridden, recursive, multi-return or reading hidden fields. [REF-T42]
- [ ] No pure forwarding function remains unless it is overridden, published, a deliberate delegate or an external interface. [REF-T45, REF-T18, POSD-T04]
- [ ] Each split loop updates only its own accumulator, and no side effect now runs twice. [REF-T32]
- [ ] Each split variable is assigned in one place, and no collecting variable was split. [REF-T35]
- [ ] Stored derived values and totals were replaced by queries, and a test adds a record and checks the total. [REF-T30, REF-T31]
- [ ] A moved function has tests against its new home, and a moved field was encapsulated first. [REF-T49, REF-T51]
- [ ] No two functions in the changed area implement the same rule or differ only in literals, and merged versions were identical before one was removed. [REF-P4, REF-T39, TDD-T11]
- [ ] Adding a type touches only one factory switch, and no client tests for a concrete subclass. [CC-T38, CC-T39, REF-T58]
- [ ] Base methods that every subclass must override are abstract or throw an error naming the missing responsibility. [REF-T63]
- [ ] No client compares a sentinel value that a special-case object now handles. [REF-T67, REF-T68]
- [ ] A subclass-to-delegate change has a trigger visible in the code (a second axis, a runtime variant change, a dependency on parent internals or a refused interface), and each commit moves one method or one group of forwarders. [REF-T70, REF-T72, REF-T74]
- [ ] No commented-out code remains, deleted code has no remaining references, and suspected reflective callers were logged first. [REF-T57, TF-T07, TF-T33, SWE-T04]
- [ ] Writes to shared mutable fields go through one function, and getters of mutable data return copies. [REF-P5, REF-T86]
- [ ] Objects that share a catalogued item store its ID and read one shared instance. [REF-T76, REF-T77]

## More entries in this area

Every entry assigned to this guide is discussed above. These neighbouring entries belong to other guides but often come up during refactoring:

- `REF-T12` — Keep refactoring commits free of behavior changes: how to split commits around these moves, in [change-workflow](change-workflow.md).
- `REF-T82` — Keep existing tests unchanged during refactoring: what may change in tests while you refactor, in [testing](testing.md).
- `REF-T19` — Name functions for intent, even for one call: choosing the name an extraction needs, in [readable-code](readable-code.md).
- `REF-T85` — Remove hooks and abstractions with no current caller: deleting speculative structure rather than dead code, in [module-design](module-design.md).
- `REF-T84` — Make value objects immutable with value equality: the alternative to sharing by reference, in [domain-modeling](domain-modeling.md).
- `REF-T87` — Measure before tuning for speed: when a split loop or query raises a performance worry, in [performance-and-concurrency](performance-and-concurrency.md).
