# Tidy First? — techniques

### TF-T01: Tidy the blocking structure first

Tidy the structure that blocks the planned change before changing behavior.

- **Why:** A blocking structure makes the change hard, so tidying first eases it.
- **When:** The code must change and its structure makes that change hard (TF-P4).
- **Not when:** Tidying would not ease the planned change, so change first (TF-T03).
- **Check:** A structural commit touching the blocking code precedes the behavior commit that depends on it.
- **Source:** ch. Preface p. 15, ch. 21 p. 77

### TF-T02: Choose only the tidyings the problem needs

Pick only the few tidyings that fit the current problem.

- **Why:** One problem needs few tidyings, so mastering them all is unnecessary.
- **When:** You face messy code and cannot tell which tidyings to apply.
- **Check:** The commit message names the tidyings used, and the diff holds only those kinds.
- **Source:** ch. Preface p. 16, ch. Introduction p. 24

### TF-T03: Tidy after a change that must ship first

Make the behavior change first, then tidy the same area right after it.

- **Why:** Shipping value sooner outweighs optional tidying, and waiting can make tidying costlier.
- **When:** The code is workable, the change ships value now, and tidying first would not lower total cost (TF-P4).
- **Not when:** Messy code blocks the change (TF-T01), or tidying would take far longer than the change.
- **Check:** A tidying commit follows the behavior commit in the same file, with a comparable diff size.
- **Source:** ch. Preface p. 16, ch. 21 p. 77, ch. 24 p. 90

### TF-T04: Add the smallest design that starts feedback

Add only the smallest design that starts the feedback loop for a hard-to-add feature class.

- **Why:** Design pays off once a feature class resists change, so start small.
- **When:** A class of features has become hard to add in one area.
- **Not when:** Choosing the moment needs judgment, since the book gives no fixed rule.
- **Check:** The first design change is small and followed by a feature change in that area.
- **Source:** ch. Preface p. 18

### TF-T05: Keep each design step small enough to undo

Make each design step small and safe, so no step gets skipped.

- **Why:** Small design steps keep each mistake cheap to undo.
- **When:** You make any design change, or you are tempted to skip design as too costly.
- **Check:** Each design diff covers one small step, named in its commit message.
- **Source:** ch. Introduction p. 23, ch. 11 p. 47

### TF-T06: Replace a wrapping condition with a guard clause

Replace a condition that wraps all remaining routine code with an early return.

- **Why:** Removing the wrapping condition removes one level of nesting.
- **When:** A condition nests all of the remaining code in a routine.
- **Not when:** The condition covers only part of the routine, or guards would pile up and hurt readability.
- **Check:** The early return precedes the remaining logic, leaving no nesting and few guards.
- **Source:** ch. 1 p. 27

### TF-T07: Delete code that never runs

Delete code confirmed never to execute, and rely on version control to recover it.

- **Why:** Version control keeps deleted code, so the tree does not need it.
- **When:** Code is confirmed never called, not just suspected (TF-T33), and you might want it later.
- **Not when:** The old code no longer works or is used differently, so rewrite it instead.
- **Check:** The deletion removes only code that never runs, and no commented-out code remains.
- **Source:** ch. 2 p. 29

### TF-T33: Log suspected dead code before deleting it

Add usage logging to suspected dead code, and delete it once the log shows no use.

- **Why:** Reflection can hide callers that a reader cannot see.
- **When:** Code may be unused, but reflection can hide its callers.
- **Check:** The PR shows usage logging, or a period with no recorded calls, before the deletion.
- **Source:** ch. 2 p. 29

### TF-T08: Pick one form for a repeated idiom

Choose one form for a repeated idiom, converting one kind of variant per tidying.

- **Why:** Changing one kind of variation per tidying keeps each diff small and checkable.
- **When:** The same logic appears in several styles, or variants coexist.
- **Check:** The idiom appears in one form, and each tidying changes one kind of variation.
- **Source:** ch. 3 p. 32

### TF-T09: Write the interface you wish existed, then delegate

Write the interface you wish existed, then implement it by calling the existing routine.

- **Why:** Designing the call first shapes the interface around its callers.
- **When:** The current call interface is awkward, or a needed helper does not exist yet.
- **Check:** The new interface exists, callers use it, and it only delegates to the old routine.
- **Source:** ch. 4 p. 33

### TF-T10: Reorder code in a move-only commit

Reorder code so each definition precedes its first use, in a commit that only moves lines.

- **Why:** A move-only diff is easy to review, since no logic changes hide among moved lines.
- **When:** A reader must scan ahead to understand earlier code.
- **Not when:** The language requires declarations first, so move only what must precede use.
- **Check:** The diff holds only moved lines, and definitions precede first use where the language allows.
- **Source:** ch. 5 p. 35

### TF-T11: Move coupled elements beside their peers

Move each element beside the peers it is coupled with, one element per commit.

- **Why:** Elements that a change must touch should sit next to each other.
- **When:** A change touches dispersed spots, or a module holds an element coupled to none of its peers.
- **Check:** The elements a change must touch are adjacent, and each commit moves one element.
- **Source:** ch. 6 p. 37, ch. 32 p. 114

### TF-T12: Group elements that change together

Group the elements that always change together into one helper or submodule.

- **Why:** When decoupling is blocked, grouping makes a coupled change touch fewer places.
- **When:** Decoupling is not feasible now, or a module holds functions always changed together.
- **Not when:** Grouping would need a new object, outside the scope of tidying.
- **Check:** The new helper contains only elements edited together, and the grouped elements move into it.
- **Source:** ch. 6 p. 37, ch. 17 p. 64, ch. 32 p. 114

### TF-T34: Initialize variables in data-dependency order

Initialize a variable before any variable whose initializer reads it.

- **Why:** Data dependencies, not position, decide the safe order of initializations.
- **When:** You move an initialization up or down within a routine.
- **Check:** Each initializer reads only values already initialized above it.
- **Source:** ch. 7 p. 40

### TF-T13: Name literals with unclear meaning

Replace a literal with an unclear meaning by one named constant.

- **Why:** A named constant states what a value means.
- **When:** A number or string appears unexplained, or repeats across the code.
- **Not when:** The same value has another meaning elsewhere, so it needs its own constant.
- **Check:** The constant is defined once, and each use of it shares one meaning.
- **Source:** ch. 9 p. 43

### TF-T14: Pass hidden inputs as explicit parameters

Pass every input a routine uses as an explicit parameter, splitting the routine so its top part gathers them.

- **Why:** Explicit parameters show callers exactly what a routine depends on.
- **When:** A routine reads map fields or environment variables deep in the code, or uses data it was not passed.
- **Check:** The signature lists each input, with no environment reads below the entry point.
- **Source:** ch. 10 p. 45

### TF-T15: Chunk a long block with blank lines

Separate each distinct part of a long block with a blank line, and comment a part only when its purpose is not visible.

- **Why:** Chunks let a reader see the distinct steps in a long block.
- **When:** A long block contains distinct parts, and some parts' purposes are not visible in the code.
- **Check:** Each distinct step has a blank line before it, and any added comment states what the code does not show.
- **Source:** ch. 11 p. 47, ch. 17 p. 64

### TF-T16: Set a tidying boundary and stop inside it

Set how far tidying will go, and stop once the requested change can be made.

- **Why:** Growing design work delays the change the user asked for.
- **When:** Design or tidying work keeps delaying the requested behavior change.
- **Check:** The PR or commit message states the tidying scope, and tidying stays inside it.
- **Source:** ch. 11 p. 47, ch. 27 p. 97

### TF-T17: Extract a purposeful block into a helper

Extract a block with one clear purpose and few links into a helper.

- **Why:** A named helper tells the reader what the block is for, not how it works.
- **When:** A block inside a routine has one clear purpose and reads few values from the rest of the routine.
- **Check:** The helper has one purpose, and its parameters are exactly the values the block reads.
- **Source:** ch. 12 p. 49, ch. 17 p. 64

### TF-T18: Use automated refactoring for renames and extractions

Use an automated refactoring tool for renames and helper extractions, not hand edits.

- **Why:** Automation changes a name and all its callers in one step.
- **When:** One change must update many call sites, or hand extraction is error-prone.
- **Not when:** The sweep is huge, so ship that change alone and quickly.
- **Check:** The rename or extraction is one commit with no hand-edited calls.
- **Source:** ch. 12 p. 49, ch. 29 p. 102

### TF-T19: Inline fragments that obscure logic

Inline fragmented helpers into one routine, then tidy from there.

- **Why:** Interacting small pieces can be harder to follow than one routine.
- **When:** Small pieces interact, with long argument lists, repeats, poor names, or shared mutable data.
- **Not when:** Each small piece is still clear alone, so keep them as helpers (TF-T17).
- **Check:** The fragmented helpers are inlined into one routine.
- **Source:** ch. 13 p. 51

### TF-T20: Comment only what the code does not show

Write a comment only to record understanding that the code does not make obvious.

- **Why:** Effort spent understanding code is worth recording where code cannot show it.
- **When:** You grasp code that took effort to understand.
- **Check:** The new comment states something the code does not show.
- **Source:** ch. 14 p. 53

### TF-T21: Name the coupled location and change

At the coupling point, write a comment naming the coupled location and the specific change that would propagate.

- **Why:** Coupling matters only relative to a specific change.
- **When:** You find a coupling defect, or you claim two elements are coupled.
- **Check:** The comment names the coupled location and the change that must propagate.
- **Source:** ch. 14 p. 53, ch. 29 p. 101

### TF-T22: Delete comments that have become redundant

Delete a comment that the code, a tidying, or a new name has made redundant.

- **Why:** Tidyings chain together, so nearby comments can go stale.
- **When:** A comment repeats adjacent code, or a tidying or name makes it redundant.
- **Not when:** The comment returns attention to a context after a long block of code.
- **Check:** Comments made redundant are removed in the same diff, and only fully redundant ones are deleted.
- **Source:** ch. 15 p. 55, ch. 17 p. 64 and p. 65

### TF-T23: Put each tidying in its own pull request

Put tidyings in their own pull request, and open a new one at each switch to behavior work.

- **Why:** Separate pull requests keep structure distinct from behavior.
- **When:** A change mixes structural cleanup with behavior, or a session switches between them.
- **Not when:** The project has no pull-request workflow, so keep tidyings in separate commits (TF-P1).
- **Check:** A tidying PR contains no change to program behavior.
- **Source:** ch. 16 p. 59 and p. 60

### TF-T24: Name a condition with an explaining variable

Name an understood subexpression or guard with an intention-named variable.

- **Why:** A variable named for its intent spares readers from decoding the expression.
- **When:** A guard clause was just added, or a comment explains a line or block.
- **Check:** The variable replaces the expression, and its name carries the intent the comment held.
- **Source:** ch. 17 p. 63 and p. 65

### TF-T25: Convert callers one at a time

Move callers to a new interface one at a time, until none uses the old one.

- **Why:** Each converted caller removes one reason to keep the old code.
- **When:** A new interface exists and the old implementation still has callers.
- **Not when:** Automated rewrite tools can convert every caller at once.
- **Check:** Callers of the old implementation decrease with each commit and reach zero.
- **Source:** ch. 17 p. 63, ch. 21 p. 76

### TF-T26: Keep each tidying stretch to about an hour

Keep each tidying stretch to about an hour before the behavior change.

- **Why:** Tidying is a minutes-to-an-hour activity, and the needed minimum can be lost.
- **When:** Tidying has run a long stretch without a behavior change.
- **Not when:** The code is so messy that longer tidying pays off, though only briefly.
- **Check:** The PR or commit timestamps show the behavior change within about an hour of tidying.
- **Source:** ch. 19 p. 71

### TF-T27: Untangle mixed tidying and behavior edits

Untangle mixed tidying and behavior edits by splitting them, restarting with tidying first, or shipping as is.

- **Why:** Restarting with tidying first may reveal more value than the tangle.
- **When:** An hour of mixed tidying and behavior work has made a tangle.
- **Check:** The work ends in one listed option, a restart puts tidyings first, and passing tests alone never justify tangled work.
- **Source:** ch. 20 p. 73

### TF-T28: Leave static or unhelpful areas untidied

Leave an area untidied when it will never change or tidying would teach nothing.

- **Why:** Tidying that never pays off costs effort for nothing.
- **When:** An area will never need a behavior change, or tidying it would teach nothing (TF-P4).
- **Not when:** Code may still need changes later, which the book says is rare for truly static systems.
- **Check:** Tidying commits in an area with no pending change cite a Fun List item (TF-T29) or a learning purpose (TF-T30).
- **Source:** ch. 21 p. 75 and p. 78

### TF-T29: Keep a Fun List of deferred messes

Keep a list of messes to tidy later, and work from it in spare time.

- **Why:** A deferred mess can be tidied once no feature presses for it.
- **When:** No pending change waits on the area, the area will change later, and spare time or low energy is available (TF-P4).
- **Not when:** A pending change waits on the area (TF-P4 chooses first or after), and a never-changing area is TF-T28's case.
- **Check:** Each later tidying commit traces to a listed item and makes no feature change.
- **Source:** ch. 21 p. 76

### TF-T30: Tidy code you must read to understand it

Tidy code you are reading now when tidying would make it clearer or reveal hidden structure.

- **Why:** Tidying can expose useful structure that messy code hides.
- **When:** You read code to understand it, or sense useful structure hidden in it (TF-P4 sets the timing).
- **Check:** The tidying commit has no behavior change, and the PR says what became clear.
- **Source:** ch. 21 p. 77, ch. 27 p. 98

### TF-T31: Flag irreversible changes for slower review

Flag irreversible changes for slower review, and review reversible ones lightly.

- **Why:** Review effort should match how hard a change is to reverse.
- **When:** A batch mixes reversible and irreversible edits.
- **Check:** The PR lists each irreversible change, such as sent data or a migration, for extra review, and reversible changes get light review.
- **Source:** ch. 28 p. 99 and p. 100

### TF-T35: Prototype structure changes that are costly to undo

Prototype a structure change that is costly to undo before the permanent split lands.

- **Why:** A spike costs little to discard, but a permanent split is expensive to undo.
- **When:** The change is costly to undo, such as extracting a separate service.
- **Check:** A prototype branch or spike exists before the permanent split lands.
- **Source:** ch. 28 p. 100

### TF-T36: Find couplings from commit co-change history

Find coupled elements by checking which files change together in commit history, not only by reading code.

- **Why:** Commit history records what changed together, which static reading cannot reveal.
- **When:** Source references do not show which elements change together.
- **Check:** The coupling note cites commit co-change history.
- **Source:** ch. 29 p. 101

### TF-T37: Check compatibility before changing behavior in use

Check backward compatibility and migration before changing behavior that callers already use.

- **Why:** Production stability depends on behavior that users already rely on.
- **When:** Changing software that users or other systems already depend on.
- **Check:** The change includes compatibility handling or migration for existing callers.
- **Source:** ch. 30 p. 106

### TF-T32: Stop decoupling at diminishing returns

Stop decoupling once added indirection outweighs the coupling removed, adding interfaces only where changes are expected.

- **Why:** Each separation adds its own cost, so decoupling stops paying at some point.
- **When:** Decoupling is reaching diminishing returns, or you are choosing how many interfaces to add.
- **Check:** The decoupling diff adds only the interfaces the PR names for a specific planned change.
- **Source:** ch. 31 p. 110
