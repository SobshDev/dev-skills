# Tidy First? — Kent Beck (1st edition, 2023)

## Summary

Tidy First? argues that small structural edits, called tidyings, keep code cheap to change. A tidying rearranges code without changing what it computes, and the book keeps tidyings apart from behavior changes. It applies when current structure makes a needed change costly. Whether to tidy before or after a change is an economic decision, based on total cost and on the value the change delivers now. Beck treats these timing choices as judgment, not proof. Design earns its place by keeping later change cheap, so tidying should serve only the next change.

## Principles

### TF-P1: Keep structure and behavior changes apart

Structure changes keep computed results the same, while behavior changes alter them. The book keeps them in separate commits and uses ease of reversal as the test.

- **Apply:** Put each structure-only edit in its own commit, free of behavior changes.
- **Check:** A structure-only commit contains no change to computed results.
- **See:** TF-T10, TF-T23
- **Source:** ch. Preface, 8, 23

### TF-P2: Make each change in small, safe steps

A failed tidying costs more when it is large, so the book splits work into small, safe steps. When an analysis goes wrong, return to the last correct version and take smaller steps.

- **Apply:** Split large changes into steps you can verify and revert alone, and keep each tidying and deletion tiny (TF-T05 sizes design steps).
- **Check:** Each commit in the sequence is small enough to verify on its own.
- **See:** TF-T05, TF-T25
- **Source:** ch. Preface, 2, 7, 17, 21

### TF-P3: Tidy only what the next change needs

Tidying serves a change, so each tidying should trace to a pending change or a current confusion. Do not add tidyings merely because a batch is open or a speculative benefit seems possible.

- **Apply:** Before each tidying, name the pending change, confusion or Fun List item it serves.
- **Limits:** When no behavior change waits on the code, TF-P4 decides between later and never.
- **Check:** The commit message names the pending change, confusion or Fun List item each tidying serves.
- **See:** TF-T16, TF-T28, TF-T29
- **Source:** ch. 17, 18, 21, 33

### TF-P4: Choose first, after, later or never

Beck leans toward tidying first, within limits. A change that ships value now can come first when tidying first would neither lower total cost nor create options worth the delay.

- **Apply:** Use later or never when no pending change waits. Use after when the change ships value and tidying first neither lowers cost nor creates worthwhile options. Otherwise use first.
- **Limits:** The book gives no formula for weighing options against delay, so that comparison is a judgment call, and tidying must not become a goal.
- **Check:** The commit message names each tidying's timing and change, and commit order matches that timing.
- **See:** TF-T01, TF-T03, TF-T28, TF-T29
- **Source:** ch. 21, 25, 27

### TF-P5: Judge design by the cost of future change

Beck treats the cost of software as roughly the cost of changing it. Design is judged by the future behaviors it makes possible, and an uncertain option is worth keeping open.

- **Apply:** Name the future behaviors a design change enables, and spend the least effort that secures each option.
- **Check:** The commit message or PR description names the future behaviors the design change enables.
- **See:** TF-T04
- **Source:** ch. 24, 26, 30

### TF-P6: Reduce coupling that makes the planned change costly

Coupling is costly when a change to one element forces edits to others. Reducing coupling lowers cost, but each separation adds its own cost.

- **Apply:** Decouple only when removing a coupling costs less than keeping it.
- **Limits:** Skip decoupling when the team lacks the skill, time or capacity. The book admits decoupling may add coupling elsewhere, a belief it cannot prove.
- **Check:** The commit message names the cross-module dependency removed and any new dependency the change adds.
- **See:** TF-T11, TF-T32
- **Source:** ch. 6, 29, 30, 31

### TF-P7: Let names and constants state intent

Code that states its intent needs fewer comments. Beck names intermediate results and replaces unexplained literals with named constants, then tidies until comments carry only what code cannot say.

- **Apply:** Name each subexpression and literal whose meaning a reader cannot get from the surrounding code, then delete comments the names make redundant.
- **Check:** Each remaining comment adds information beyond the code it sits beside.
- **See:** TF-T13, TF-T20, TF-T22, TF-T24
- **Source:** ch. 8, 14, 17
