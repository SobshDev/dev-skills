# Readable code: names, functions, comments, layout

This guide covers what a reader needs from code at the level of a single file: names, function size and abstraction level, signatures and results, conditionals, comments and interface documentation, and layout. The central idea is that code is read far more often than it is written, so each name, split and comment should spare the next reader work, and a reader's confusion counts as a defect even when the author finds the code clear.

**Read this when:** naming a variable, function, type or module, writing or splitting a function, adding a parameter or a return value, writing a conditional, adding or deleting a comment, documenting a public method, setting up a formatter or a project convention, reviewing a diff for clarity.

**Entry IDs** such as `WELC-T12` point to `../books/<book>/techniques.md` (T) or `principles.md` (P);
the prefix table is in [SKILL.md](../SKILL.md).

## Contents

- [Core rules](#core-rules)
- [Rules: names](#rules-names)
- [Rules: functions and control flow](#rules-functions-and-control-flow)
- [Rules: parameters and results](#rules-parameters-and-results)
- [Rules: comments and interface documentation](#rules-comments-and-interface-documentation)
- [Rules: layout and conventions](#rules-layout-and-conventions)
- [Playbooks](#playbooks)
- [Where the books disagree](#where-the-books-disagree)
- [Review checklist](#review-checklist)
- [More entries in this area](#more-entries-in-this-area)

## Core rules

### 1. Treat a reader's confusion as a defect to fix

Clean Code puts readability first because code is read far more often than it is written, and POSD defines complexity partly as how hard readers find the code. POSD adds that complexity is easier to see from the reader's side than the writer's, so the author's sense that code is obvious understates the problem. [CC-P1, POSD-P1, POSD-T02]

- **Do:** When a reviewer or teammate says a passage is hard to follow, change the code (a name, a split, a comment) rather than only explaining it in the review thread.
- **Not when:** Fewer lines are not automatically simpler, so do not compress code to look tidy when a longer version is easier to read. [POSD-P1]
- **Check:** Each review remark about clarity is answered by a change in the diff, not only by a reply.

### 2. Make the code state its intent, and keep structure edits separate

Names, small units and structure should together show what code does and why, so a reader does not have to reconstruct intent from the steps. Tidy First treats structure changes, which keep computed results the same, as belonging in their own commits apart from behavior changes. [CC-P1, TF-P7, REF-P3, TF-P1]

- **Do:** Name each element for its purpose, and extract a named function where a comment would otherwise have to explain a block. Put readability edits in a structure-only commit, and see [change-workflow](change-workflow.md) and [refactoring](refactoring.md) for the mechanics.
- **Not when:** A reason the code cannot carry still belongs in a comment (rule 24). [CC-P1]
- **Check:** New comments explain a reason rather than a step a clearer name could show, and readability edits do not share a commit with behavior changes.

## Rules: names

### 3. Name for a reader who has not seen the implementation

Choose names that tell a reader without your context what the element is for, even if that makes them long. A purpose-revealing name lets callers trust the name and skip the body, and a generic name such as `data` or `info` tells them nothing about why the element exists. Refactoring adds that a name which resists being chosen is a hint that the design is unclear. [CC-T18, PP-T51, REF-P3, REF-T19]

- **Do:** Read each new name on its own, without its body, and ask whether it says what the element is for. Name a parameter for the role it plays for any value of its type, not after the value one caller happens to pass, and check that a reader's guess from the name alone would be right. [POSD-T27]
- **Not when:** A function called very frequently may need a short, memorable name instead (rule 7). [CC-T18]
- **Check:** No new identifier is a generic word such as `data`, `tmp` or `info`, and each parameter name fits every existing call site.

### 4. Use the domain's vocabulary, one word per concept

Take names for types, functions and tests from the application domain, and keep one glossary of them. When the same business concept appears under two names, readers have to wonder whether they are two things, so pick one term and use it in every module. Learning DDD makes the same demand for the language shared with the business, and applies it to supporting and generic areas too. [PP-T26, CC-T22, DDD-P2]

- **Do:** Look up the project glossary or requirements before naming a domain element, and reuse the existing term for a concept already named elsewhere. For bounded contexts and the shared language, see [domain-modeling](domain-modeling.md).
- **Check:** Identifiers and test names use glossary terms, and the diff does not introduce a second name for a value that already has one.

### 5. Give each identifier exactly one meaning

Do not reuse a name, or a variable, for a second purpose. One identifier that holds two concepts forces the reader to work out which meaning applies at each line. [POSD-T25, REF-T35]

- **Do:** Introduce a separate variable for each separate purpose, and declare variables created to name a value as read-only so later reuse becomes a visible error. [REF-T26]
- **Not when:** A collecting variable that accumulates a running total is one purpose and is not split. [REF-T35]
- **Check:** No identifier in a scope holds values for unrelated concepts, and each split variable is assigned in one place.

### 6. Put units and counted items into names or types

A generic name for a number hides its unit or what it counts, and callers guess wrong. POSD wants the name to state the unit or the counted items, and Pragmatic Programmer goes further for values that are easy to misread, such as a percentage or a money amount, by giving them a dedicated type so the compiler stops one being passed for another. [POSD-T26, PP-T52]

- **Do:** Name time values with their unit and counters with what they count. For a parameter that carries a percentage, an amount or a bounded range, define a type instead of passing a bare number.
- **Check:** Time names carry a unit, count names say what is counted, and unit-bearing parameters use defined types.

### 7. Scale name length with visibility

Clean Code gives widely visible names short forms, because they appear at many call sites and short names read cleanly there, and gives narrow, private helpers longer and more specific names, because they appear at few sites where the extra words state purpose. [CC-T20, CC-T18]

- **Do:** Keep a public, widely used name short. Give a private helper called from one place a descriptive name. Length does not excuse imprecision: state units and counted items whatever the length (rule 6). [POSD-T26]
- **Not when:** A function called once can keep a long name. Teams that prefer short names explained by comments keep that convention. [CC-T20]
- **Check:** Public names stay short, and single-call private helpers have descriptive names.

### 8. Name functions as actions and modules as nouns

Name each function as a verb for a domain action and each module or class as a domain noun, so calls read as sentences in the domain's vocabulary. [CC-T21]

- **Do:** Start function names with the action they perform, and name classes and modules after the domain thing they represent.
- **Not when:** A team that names getters after the value they return keeps its convention. [CC-T21]
- **Check:** Class and module names are nouns, and function names are verbs that match domain actions.

### 9. Leave type encodings out of names

Do not prefix names with their type, with an `I` for interfaces, or with member markers such as `m_`. Compilers and editors already track types, and a prefix becomes false the day the type changes. [CC-T23]

- **Do:** Name variables, fields and interfaces for what they mean, and let the type system carry the type.
- **Not when:** A language with very short identifier limits may still need encodings. [CC-T23]
- **Check:** In a language with a rich type system, the diff adds no type prefix, `I` prefix or `m_` marker.

### 10. Replace unexplained literals with named constants

A bare status number, a fixed array position or an unexplained value forces each reader to decode it. Clean Code and Tidy First both replace such literals with a named constant, defined once, so the meaning shows at every use. [CC-T24, TF-T13, TF-P7]

- **Do:** Define one constant per meaning and use it at every site that shares that meaning. Then delete any comment the constant's name has made redundant. [TF-P7]
- **Not when:** The same value means something else elsewhere, so it needs its own constant. On a critical path, a helper call may cost unacceptable time. [TF-T13, CC-T24]
- **Check:** The diff adds no bare status code, index or unexplained number, and each constant's uses share one meaning.

### 11. Rename as soon as you understand the code better

A name that no longer matches its body misleads every later reader. Once you have worked out what a function, variable or field really does, or a name has confused you, rename it. Refactoring stresses persistent fields most, because their names reach the most code. [REF-T20, REF-P3]

- **Do:** Use the editor's automated rename so every reference changes in one step, then run the tests. Rename one identifier per step. [REF-T14, TF-T18, REF-T15]
- **Not when:** A function that other teams or customers call needs the old name kept as a deprecated forwarder until callers move, and callers you do not control cannot be updated in the same change. See [refactoring](refactoring.md). Without static typing, check the tool's matches by hand. A very large rename sweep ships as its own change, quickly. [REF-T18, REF-T17, REF-T14, TF-T18]
- **Check:** Each changed function name matches its body, and the rename commit contains no hand-edited call sites and no other change.

## Rules: functions and control flow

### 12. Keep each function to one idea at one level of abstraction

A function should express one concept at one level, so a reader takes it in at once and can follow detail downward into named helpers. Clean Code sets a default of about a dozen lines and at most two indentation levels, and keeps orchestration apart from detail. POSD splits a method only when the split makes the system simpler and each piece reads on its own, never because of length alone (see the first tension below). [CC-P2, CC-T32, POSD-T35]

- **Do:** When a function passes about a dozen lines or reaches a third level of indentation, look for distinct steps at different levels and move the lower-level steps into named helpers (rule 13). Keep the coordinating function as a list of named steps.
- **Not when:** Some functions read better undivided, and switch statements or formatting code run longer. What counts as one meaningful level is a judgment call, and some teams allow two. A long method with independent blocks and a simple signature can stay whole. [CC-T32, CC-P2, POSD-T35]
- **Check:** Each function in the diff holds steps at one level and calls named helpers for detail, or its length is justified by one of the exceptions above.

### 13. Extract a block only when its name says more than its code

A helper earns its place when its name is more abstract than the code it hides, so the reader learns what the block is for without reading how it works. A helper that restates one statement adds a jump and hides nothing. Tidy First adds that good candidates have one clear purpose and read few values from the rest of the routine, and Refactoring will extract even a single call when the new name is clearer than the call. [CC-T33, TF-T17, REF-T19, REF-T22]

- **Do:** Extract a block that a comment used to introduce, a loop with its body, or a large switch branch into a function named for its purpose. Pass in exactly the values the block reads. [REF-T22, REF-T23, TF-T17]
- **Not when:** A forwarder that only moves code elsewhere is not worth extracting, except a vendor adapter. Do not split a method whose halves would have to be read together. [CC-T33, POSD-T35]
- **Check:** Each extracted helper is named for its purpose, does more than forward one call, and can be understood without opening its caller.

### 14. Inline fragments and forwarders that obscure the logic

The reverse move matters as much. Small pieces that interact through long argument lists or shared mutable data can be harder to follow than one routine, and a method whose body only passes its arguments on teaches nothing. Inline such pieces, then re-extract along better lines if needed. [TF-T19, REF-T44, POSD-T04, REF-T41]

- **Do:** Inline helpers whose bodies are as clear as their names, and pass-through methods that forward the same arguments. Then look again for real boundaries.
- **Not when:** Each small piece is still clear on its own. An external interface must stay unchanged, so the forwarding wrapper is right. Do not inline a method that is overridden, recursive, has several returns or reads hidden fields. A small fix that needs only moving statements to callers does not need the inline-and-re-extract cycle. [TF-T19, POSD-T04, REF-T42, REF-T41]
- **Check:** The diff leaves no single-call wrapper whose body is no clearer than its name, and no pure forwarding method unless it preserves an external interface.

### 15. Name conditions and expressions instead of explaining them

A condition or sub-expression that needs a comment should become a variable or a predicate function named for what it means. The control statement then reads as one sentence about the domain, and the name stays accurate as code changes where a comment drifts. [CC-T31, CC-T19, REF-T24, TF-T24]

- **Do:** Move a multi-step `if` condition or loop body into a function such as `shouldDeleteRecord(r)`, or into an explaining variable. Before moving an expression into a variable, confirm it changes no state, since moving it would change when it runs. [CC-T31, TF-T24, REF-T25]
- **Not when:** A comment recording why a surprising choice was made stays, because no name carries that reason. [CC-T19]
- **Check:** Complex conditions in the diff are named predicate calls or explaining variables, and no explaining variable's initializer has a side effect.

### 16. Return early for unusual cases

When one leg of a conditional is an unusual case or a pre-check, return from it at the top instead of nesting the normal path inside an `else`. Tidy First notes that this removes a level of nesting, and Refactoring that it keeps unusual cases from cluttering the normal path. [REF-T65, TF-T06]

- **Do:** Write the guard as the negation of the old nesting condition, return immediately, and drop any result variable that only existed to reach a single exit.
- **Not when:** Both legs are normal paths, or a single exit point is clearer. The condition covers only part of the routine. Guards would pile up and hurt readability. [REF-T65, TF-T06]
- **Check:** Unusual cases return at the top without an outer negation, and the remaining logic has no wrapping condition.

```python
def ship(order):
    if order is None:              # unusual case: leave at once
        return Rejected("no order")
    if not order.is_paid():
        return Rejected("unpaid")
    address = order.shipping_address()
    return carrier.book(address, order.parcels())
```

### 17. Keep try and catch bodies to one call

A try block that mixes normal steps with handling makes both harder to read. Move a multi-statement try or catch body into its own named function, so the outer function shows the steps and the failure handling side by side. For when to throw and what to catch, see [errors-and-contracts](errors-and-contracts.md). [CC-T30]

- **Do:** Leave one call in the `try` and one call in each `catch`, each naming what it does.
- **Check:** No try or catch block in the diff holds more than one statement.

## Rules: parameters and results

### 18. Keep parameter lists short, and group values that travel together

Each extra argument makes a call harder to read and to get right. Clean Code prefers zero or one parameter and caps the list at three. When several values always travel together, group them into one object, so the signature shrinks and the group gets a visible name. POSD adds defaults, so the common call passes nothing a rare case needs. [CC-T26, CC-T25, POSD-T09]

- **Do:** Before adding a fourth parameter, check whether the values belong together and pass them as one named object. Give parameters defaults that the common use needs.
- **Not when:** A function that genuinely needs several inputs keeps them, in an obvious order. A value the module can derive itself should not become a parameter at all. [CC-T26, POSD-T09]
- **Check:** No signature in the diff takes more than three parameters or gains one without a reason, and values passed together at every call site are grouped.

### 19. Make every input visible in the signature

A routine that reads environment variables, map fields or globals deep inside its body hides what it depends on. Tidy First and Pragmatic Programmer both pass every input as an explicit parameter, so callers and tests can see and supply them. [TF-T14, PP-T27]

- **Do:** Split the routine so its top part gathers the inputs and passes them down, and give configuration, state and services as parameters rather than through singletons. When this pushes a list past three, apply rule 18 (see the second tension).
- **Check:** The signature lists each input, nothing below the entry point reads the environment, and new code takes its dependencies as parameters.

### 20. Replace a flag argument with named functions

When a boolean, enum or string literal selects between behaviors, replace it with one explicitly named function per behavior, so each behavior stays separate. [REF-T83]

- **Do:** Create a named function for each value the flag selects, and change each literal call site to call it.
- **Not when:** The argument is computed at runtime rather than written as a literal at the call site. [REF-T83]
- **Check:** No signature in the diff takes a flag that call sites pass as a literal.

### 21. Return results, and give multi-value results a named type

Return a result instead of writing it into an argument, so callers read the outcome directly instead of tracking side effects. When a method must return several related values, define a named type for them, because a generic pair or tuple makes readers guess which value is which. [CC-T27, POSD-T28]

- **Do:** Return the value, or a small named structure whose fields say what each value means.
- **Not when:** A language without objects or multiple returns may need output arguments. Values that are stored state callers change separately belong in separate objects (POSD-T29). [CC-T27, POSD-T28]
- **Check:** No function writes a result into a parameter that callers read, and no return type is a generic container read through generic getters.

### 22. Separate commands from queries

A method should either change state or answer a question, not both. Callers can then ask freely without causing a side effect, and queries and modifiers can be tested apart. Refactoring treats this as a strong default for any value-returning function. [CC-T28, REF-T28, REF-T29]

- **Do:** Move the calculation into a query that writes nothing, and leave the state change in a modifier that returns nothing callers depend on.
- **Not when:** An atomic query-and-change such as a stack pop may stay combined. Caching a query's result is acceptable. [CC-T28, REF-T28]
- **Check:** No value-returning function in the diff writes, sends or changes state apart from caching.

```python
# Before: asking for the price also changes it.
def apply_discount(self, rate):
    self.price = self.price * (1 - rate)
    return self.price

# After: the query changes nothing, the command returns nothing.
def discounted_price(self, rate):
    return self.price * (1 - rate)

def apply_discount(self, rate):
    self.price = self.discounted_price(rate)
```

## Rules: comments and interface documentation

### 23. Prefer a better name to a comment that explains what

When a comment explains what a block, condition or sub-expression does, a name can usually carry that meaning instead, and a name stays correct as code changes while a comment drifts. Clean Code, Tidy First and Refactoring all treat such a comment as a signal to rename or extract. [CC-T19, CC-P1, TF-P7, REF-T22]

- **Do:** Turn the comment into an explaining variable, a named constant or an extracted function (rules 10, 13, 15), then delete the comment.
- **Not when:** The comment holds a reason the code cannot express (rule 24). [CC-T19, CC-P1]
- **Check:** No comment in the diff introduces a block that could be a named call or a condition that could be a named predicate.

### 24. Comment what the code cannot say: reasons, rationale, conditions

Code cannot show why a choice was made or when a method may be called. POSD wants comments to supply that missing knowledge, written while the author still has it. SWE at Google asks for a comment on each non-obvious branch, workaround or constant, and Tidy First records understanding that took effort to gain. Pragmatic Programmer adds assumptions about routines you do not control. [POSD-P6, POSD-T16, SWE-T37, TF-T20, PP-T67]

- **Do:** Next to the relevant code, write why the surprising form is correct, what the caller must guarantee, and which outside behavior the code relies on.
- **Check:** Non-obvious branches, workarounds and constants carry a comment giving their reason, and each new comment states something the code does not show.

### 25. Document the behavior callers depend on in the interface

A signature cannot express ordering, side effects, constraints, units or what null means, so callers either read the body or guess. POSD documents each public method's behavior, ordering, side effects and constraints, and each variable's units, bound inclusivity and null meaning. Clean Code requires doc comments on public APIs used by other teams, and SWE at Google keeps that reference text beside each declaration so generated docs come from the same source. [POSD-T15, POSD-T17, CC-T72, SWE-T34]

- **Do:** On each public method, state what it does, call-order rules, side effects and units. On fields and parameters, state units, whether bounds are inclusive, and what null means. For an event handler, say what triggers it and which thread calls it. For a class whose methods must be called in a set order, add a short usage example to the class comment. [POSD-T56, POSD-T57]
- **Not when:** A usage example that would only repeat the method comments of a simple class is not needed. How far documentation goes beyond public APIs is disputed (see the third tension). [POSD-T57, CC-T72]
- **Check:** Each new public member has a doc comment covering purpose, inputs, result, ordering and side effects, handler comments name the trigger and calling thread, and generated reference pages read from those comments.

### 26. Write the interface comment before the body

Write a new class's interface comment and its key public signatures before the method bodies. Writing the comments first exposes design problems while changing the design is still cheap. For contracts, preconditions and what a routine does not promise, see [errors-and-contracts](errors-and-contracts.md). [POSD-T21, PP-T36]

- **Do:** Draft the class comment and signatures first, stub the bodies, and let the interface be reviewed before the implementation lands.
- **Check:** A new class arrives with its signatures and interface comments, which describe behavior and not implementation detail. [POSD-P6]

### 27. Delete comments that only restate the code

A comment that says no more than the code beside it still costs reading time, and tidyings and renames often leave nearby comments redundant. Delete them in the same diff. [CC-T80, TF-T22]

- **Do:** After each rename, extraction or constant, reread the comments nearby and remove those the new names have made redundant.
- **Not when:** A comment introduces an algorithm's overall idea. A public API doc comment stays. A comment that returns the reader's attention to a context after a long block of code stays. Delete only comments that are fully redundant. [CC-T80, TF-T22]
- **Check:** No comment in the diff paraphrases the line it precedes.

### 28. Keep each comment true, and change it with its code

A wrong comment misleads more than a missing one. Keep each comment beside the declaration it describes, and when logic changes, update or remove the comments that describe it in the same change. SWE at Google applies the same discipline to documents, reviewing doc edits like code. [CC-T71, SWE-T37, SWE-T33]

- **Do:** For every changed line, search for comments that describe it, including ones further up the file, and fix or delete their claims.
- **Check:** Comments on changed lines, or that describe them, are updated or removed in the same diff.

### 29. Keep history out of the source

Commented-out code, change logs inside files, and author or ticket tags duplicate what version control already keeps, and commented-out code goes stale and confuses readers. Delete them before committing. [CC-T73, REF-T57, TF-T07]

- **Do:** Delete disabled code rather than commenting it out, and move change history into commit messages. Before deleting code as unreachable, search for its callers and confirm it never runs, rather than only suspecting it. [REF-T57, TF-T07]
- **Not when:** Commented-out code used only during local debugging and never committed is fine. When readers cannot see history and must know code existed, a one-line comment may name the deleted code. [CC-T73, REF-T57]
- **Check:** The committed change has no commented-out code, journal comments, or name and ticket tags.

### 30. Summarize the phases of a long method

When a method stays long because its blocks belong together, a short comment at the start of each phase lets a reader skip the detail and find the part they need. Put each summary at the narrowest block it describes. [POSD-T23]

- **Do:** Start each phase with a one-line statement of its intent, and keep inline comments to intent or reason, not a description of the next line.
- **Not when:** A short method that does one thing is already described by its interface comment. If a phase could be extracted under a name more abstract than its code, extracting it may be the better move (see the third tension). [POSD-T23, CC-T33]
- **Check:** Each phase of a long method starts with a summary, and no inline comment narrates the following statement.

### 31. Mark coupling where it cannot be removed

When a change in one place must be matched in another, and no single module can own the decision, say so at the code. Tidy First names the coupled location and the specific change that would propagate. POSD records the decision at the shared declaration and adds a pointer comment at each dependent site. [TF-T21, POSD-T24]

- **Do:** At the shared declaration, list every place that must change with it, and at each dependent site, point back to that list.
- **Not when:** One module can own the decision, so move it there instead (see [module-design](module-design.md)). A separate design-notes file can serve, though such notes drift. [POSD-T24]
- **Check:** The shared declaration lists each dependent site, and each dependent site has a pointer naming the change that must propagate.

## Rules: layout and conventions

### 32. Let one formatter enforce one team style

People's formatting habits differ, and a codebase read as one style is easier to scan. Agree on one simple style and let an automated formatter apply it, and run it as a check before a change is reviewed or lands. [CC-T74, SWE-T15]

- **Do:** Commit the formatter settings, run the formatter on changed files, and add it to the project's pre-commit or presubmit checks.
- **Not when:** Slow or unstable checks belong after submit rather than in the commit-time gate. [SWE-T15]
- **Check:** Formatter settings are committed, and changed files pass the formatter unchanged.

### 33. Follow the conventions of similar existing code

Readers predict behavior from familiar patterns, so new code should copy the structure, ordering and naming of its siblings. When the same idiom appears in several styles, converge on one form. Write the main conventions in one findable document linked from the contributor entry point. [POSD-T31, TF-T08, POSD-T32]

- **Do:** Before creating a file, open a sibling file and match its ordering, naming and layout. Convert variants of an idiom one kind of variation per tidying.
- **Not when:** A better convention is justified, and then every use is upgraded and the old one removed completely, rather than leaving two conventions side by side. [POSD-T31]
- **Check:** A new file matches its siblings' ordering, naming and layout, and any new or changed convention is written in the one conventions document.

### 34. Order code so it reads from top to bottom

Readers should not have to jump back and forth to follow a file. Clean Code places helpers below their caller, in the order the caller first uses them. Tidy First moves each definition before its first use, in a commit that only moves lines. The two orders are opposite (see the fourth tension). [CC-T34, TF-T10]

- **Do:** Pick the order the file and its siblings already use, and reorder in a move-only commit so no logic change hides among moved lines.
- **Not when:** The language requires declarations first, so move only what must precede use. Ordering cannot fix code whose pieces are entangled. [TF-T10, CC-T34]
- **Check:** Where the language leaves order free, helpers follow one consistent order in the file, and reorder commits contain only moved lines.

### 35. Separate the steps of a long block with blank lines

A blank line before each distinct step of a long block lets the reader see the steps. [TF-T15]

- **Do:** Insert a blank line between distinct steps, and comment a step only when its purpose is not visible in the code.
- **Check:** Each distinct step in a long block has a blank line before it, and any added comment states what the code does not show.

## Playbooks

### When you write a new function or class

1. Draft the interface comment and public signatures first, with stubbed bodies, and revise the interface if writing the comment exposes a design problem. [POSD-T21, POSD-T15]
2. Name the class with a domain noun and each method with a domain verb, using glossary terms and one word per concept. [CC-T21, PP-T26, CC-T22]
3. Name parameters for their role, put units into names or types, and keep each name to one meaning. [POSD-T27, POSD-T26, PP-T52, POSD-T25]
4. Keep each signature to three parameters or fewer, with every input explicit and values that travel together grouped. [CC-T26, TF-T14, CC-T25]
5. Decide for each method whether it is a query or a command, and return results rather than writing them into arguments. [CC-T28, CC-T27, POSD-T28]
6. Write the bodies at one level of abstraction, with unusual cases returning early. [CC-P2, REF-T65]
7. Document units, bounds and null meaning on fields and parameters, the trigger and thread for handlers, and a usage example if calls must follow a set order. [POSD-T17, POSD-T56, POSD-T57]
8. Run the formatter and compare the file's layout with its siblings. [CC-T74, POSD-T31]

### When a function has become hard to read

1. Separate its distinct steps with blank lines to see its shape. [TF-T15]
2. Replace unexplained literals with named constants and complex conditions with explaining variables or predicates. [TF-T13, CC-T24, TF-T24, CC-T31]
3. Turn wrapping conditions for unusual cases into guard clauses. [REF-T65, TF-T06]
4. If small helpers interact through long argument lists or shared state, inline them first. [TF-T19, REF-T44]
5. Extract each step whose name would be more abstract than its code, passing in the values it reads, and stop when the remaining pieces would have to be read together. [CC-T33, TF-T17, POSD-T35]
6. If the method stays long because its blocks belong together, add a summary comment at the start of each phase. [POSD-T23]
7. Order the helpers to match the file's convention, delete comments the new names made redundant, and commit these edits apart from any behavior change. [CC-T34, TF-T10, TF-T22, TF-P1]

### When you change code that has comments nearby

1. Find every comment that describes the lines you change, and update or remove each claim the new code no longer supports. [CC-T71, SWE-T37]
2. If a comment explains what a block does, replace it with a name and delete it. [CC-T19, REF-T22]
3. If a comment repeats the adjacent code, delete it, unless it introduces an algorithm's idea, is a public doc comment, or brings the reader back to a context after a long block. [CC-T80, TF-T22]
4. If a comment records why the code is shaped this way, keep it and make sure the reason still holds. [CC-T19, SWE-T37]
5. If you had to work hard to understand the code, record what you learned in a comment the code cannot replace. [TF-T20, POSD-T16]
6. Remove commented-out code and journal or author tags before committing. [CC-T73, REF-T57]

### When you add or change a public API

1. Write the doc comment beside the declaration, in the place the documentation generator reads. [SWE-T34, CC-T72]
2. State behavior, call-order rules, side effects, units, bound inclusivity and null meaning. [POSD-T15, POSD-T17]
3. Add a usage example to the class comment if callers must call methods in a particular sequence. [POSD-T57]
4. For event handlers, state the trigger and the calling thread. [POSD-T56]
5. When renaming a published function, keep a deprecated forwarder until callers have moved. [REF-T18]

### When a signature keeps growing

1. List the inputs the routine reads, including hidden ones from the environment or globals, and make each an explicit parameter. [TF-T14, PP-T27]
2. Group values that always travel together into one named object. [CC-T25]
3. Give defaults to parameters most callers do not need, and drop any the module can derive itself. [POSD-T09]
4. Replace literal flag arguments with one named function per behavior. [REF-T83]
5. If the routine is a large function whose extraction is blocked by shared locals, first split any variable that serves several purposes, then consider a method object whose fields hold the remaining state. Plain functions usually suffice, and fields must not be static state shared across threads. [CC-T35, REF-T81, REF-T35]
6. For system-wide settings that many components need, see the context object in [module-design](module-design.md). [POSD-T44]

### When you introduce or change a project convention

1. Check how similar code already does it, and follow that unless the new convention is clearly better. [POSD-T31]
2. If you adopt a new convention, convert every existing use and remove the old form, one kind of variation per tidying. [POSD-T31, TF-T08]
3. Write the convention into the single conventions document and link it from the contributor entry point. [POSD-T32]
4. If the convention is about formatting, encode it in the formatter settings and run the formatter in pre-commit checks. [CC-T74, SWE-T15]

## Where the books disagree

### How long should a function be, and when should you split it?

- **Clean Code:** Keep functions near a dozen lines with at most two indentation levels, and split until each body holds one level of named steps. [CC-T32, CC-P2]
- **POSD:** Do not split just because a method is long. Split only when the system becomes simpler and each piece reads alone, and keep long methods with independent blocks and a simple signature whole. [POSD-T35]
- **Refactoring:** Extract even a single call when the new name states the purpose more clearly than the call. [REF-T19]
- **Tidy First and Refactoring on the reverse move:** Inline pieces that interact or are no clearer than their names. [TF-T19, REF-T44]
- **Decide:** Treat Clean Code's dozen lines as a prompt to look, not a limit. Extract a block when it has one purpose, reads few values from the rest of the routine, and its name is more abstract than its code [TF-T17, CC-T33]. Do not extract when the halves would have to be read together or the helper would only restate a statement [POSD-T35, CC-T33]. Keep a long function whole when its blocks are independent and its signature is simple, or when it is a switch or formatting code [POSD-T35, CC-T32]. Inline helpers that interact through long argument lists or shared mutable data, unless each piece is still clear on its own [TF-T19].

### Explicit parameters, or few parameters?

- **Tidy First and Pragmatic Programmer:** Pass every input a routine uses as an explicit parameter, rather than reading globals or the environment inside it. [TF-T14, PP-T27]
- **Clean Code:** Keep each function to three parameters or fewer, and share working state between extracted helpers through fields when extraction is blocked. [CC-T26, CC-T35]
- **POSD:** Passing system-wide settings through every method adds parameters that intermediate layers only forward, so put them in a context object. [POSD-T44]
- **Decide:** Make hidden inputs explicit, because explicit parameters show callers what the routine depends on [TF-T14, PP-T27]. If that pushes a list past three, group the values that travel together into one object [CC-T25]. Use fields shared by helpers only when extraction is blocked by several changing locals, and not for static state shared across threads [CC-T35]. Use a context object only for system-wide settings that many components need, keeping its values immutable [POSD-T44]. A function that genuinely needs several inputs keeps them in an obvious order [CC-T26].

### How much should you comment?

- **Clean Code:** A comment explaining unclear code marks intent the code failed to express, so prefer names and extraction, delete comments that restate code, and require doc comments for public APIs. Within one team, clear names and signatures often suffice. [CC-P1, CC-T19, CC-T80, CC-T72]
- **POSD:** Give every class and method an interface comment and every class variable a declaration comment, and add summary comments at the start of each phase of a long method. [POSD-T22, POSD-T23]
- **Both agree:** Comments carrying reasons, rationale and call conditions belong, comments repeating code do not, and public APIs need doc comments. [CC-P1, CC-T80, CC-T72, POSD-P6, POSD-T16, POSD-T15, SWE-T37]
- **Decide:** On public APIs and code other teams call, write doc comments [CC-T72, POSD-T15]. Skip comments on trivial getters and setters whose declaration says everything [POSD-T22]. For internal classes and methods used within one team, the entries give no deciding condition: follow the codebase's existing convention, and where there is none, at least document anything callers cannot see from the signature, such as units, ordering or null meaning [POSD-T17, POSD-T15]. Inside a long method, extract a phase when a helper name would be more abstract than its code, and use a phase summary comment when the method is better kept whole [CC-T33, POSD-T35, POSD-T23].

### Should helpers come before or after their callers?

- **Clean Code:** Put helpers below the caller, in the order the caller first calls them, so the reader steps down through the file. [CC-T34]
- **Tidy First:** Reorder so each definition precedes its first use, so the reader does not have to scan ahead. [TF-T10]
- **Decide:** Both defer to languages that require declarations first [CC-T34, TF-T10]. Beyond that, the entries give no deciding condition, so follow the order the file and its sibling files already use [POSD-T31], and make any reordering a move-only commit [TF-T10].

## Review checklist

- [ ] No new identifier is a generic word such as `data` or `info`, and each reads correctly without its body. [CC-T18, PP-T51]
- [ ] New names use glossary terms, and no concept gains a second name. [PP-T26, CC-T22]
- [ ] No identifier holds two unrelated meanings in one scope. [POSD-T25]
- [ ] Time and count names state their unit or counted items, and percentages or amounts use defined types. [POSD-T26, PP-T52]
- [ ] Parameter names fit every call site, not only the current one. [POSD-T27]
- [ ] No type prefix, `I` prefix or member marker is added in a rich-type language. [CC-T23]
- [ ] No bare status code, index or unexplained number is added. [CC-T24, TF-T13]
- [ ] Renamed functions match their bodies, and renames are tool-made, single-identifier commits. [REF-T20, REF-T14, REF-T15]
- [ ] Functions past about a dozen lines or three indentation levels either hold one level of named steps or fit a stated exception. [CC-T32, CC-P2, POSD-T35]
- [ ] Each extracted helper is more abstract than its code and readable without its caller, and no new method only forwards its arguments. [CC-T33, POSD-T35, POSD-T04]
- [ ] Complex conditions are named predicates or explaining variables without side effects. [CC-T31, TF-T24, REF-T25]
- [ ] Unusual cases return at the top instead of wrapping the main path. [REF-T65, TF-T06]
- [ ] No try or catch body holds more than one statement. [CC-T30]
- [ ] No signature takes more than three parameters unless the function genuinely needs those inputs, no signature takes a literal flag argument, and no routine reads the environment below its entry point. [CC-T26, REF-T83, TF-T14]
- [ ] No function writes its result into an argument, and multi-value results use a named type. [CC-T27, POSD-T28]
- [ ] No value-returning function changes state, apart from caching or an atomic pop. [CC-T28, REF-T28]
- [ ] Comments on changed lines are updated or removed, and no comment paraphrases its next line. [CC-T71, CC-T80, TF-T22]
- [ ] Non-obvious branches, workarounds and constants carry a reason comment. [SWE-T37, POSD-T16]
- [ ] New public members have doc comments beside the declaration covering behavior, ordering, side effects, units and null meaning. [CC-T72, SWE-T34, POSD-T15, POSD-T17]
- [ ] Event handlers name their trigger and calling thread, and order-sensitive classes show a usage example. [POSD-T56, POSD-T57]
- [ ] Coupled sites that no single module owns point to one shared note. [TF-T21, POSD-T24]
- [ ] No commented-out code, change log or author or ticket tag is committed. [CC-T73, REF-T57]
- [ ] Changed files pass the committed formatter unchanged. [CC-T74]
- [ ] New files match their siblings' ordering, naming and layout, and new conventions are in the conventions document. [POSD-T31, POSD-T32]
- [ ] Readability edits sit in structure-only commits, apart from behavior changes. [TF-P1, TF-T10]

## More entries in this area

- `POSD-T30` — Let the normal path handle empty states: when an edge case would add an `if` that the main path could absorb, except on a hot path with several rare conditions.
- `POSD-T29` — Keep two related values in separate objects: when callers read and change two combined values separately.
- `REF-T36` — Pass read-only locals in, return the change: the signature to give a freshly extracted function. When two or more locals change, split them first.
- `REF-T32` — Split a loop that builds two unrelated results: when one loop fills two accumulators, unless profiling shows the single pass is a real bottleneck.
- `REF-T33` — Replace loops with filter and map pipelines: when a loop only filters or maps, has no side effects or early exit, and the language has first-class functions.
- `REF-T66` — Combine checks that lead to the same result: when adjacent conditions return the same value and are not truly independent checks.
- `TF-T34` — Initialize variables in data-dependency order: when moving initializations while reordering a routine.
