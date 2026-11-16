# software-craft

**An agent skill that gives a coding agent the engineering judgment of 14 classic software books.**

Coding agents write code that works. They are less reliable at what the books teach: making
small steps you can verify, keeping a refactor out of a behavior change, adding a timeout
before a retry, leaving out an interface nobody needs, and pinning untested code with tests
before touching it. `software-craft` turns those books into rules an agent can follow while it
works. Each rule says what to do, when not to do it, and how to check it in a diff.

```text
/plugin marketplace add SobshDev/dev-skills
/plugin install software-craft@dev-skills
```

---

## Contents

- [What the agent gets](#what-the-agent-gets)
- [Install](#install)
- [How it works](#how-it-works)
- [The books](#the-books)
- [The guides](#the-guides)
- [When the books disagree](#when-the-books-disagree)
- [How it was built](#how-it-was-built)
- [Evaluation](#evaluation)
- [Limits](#limits)
- [License](#license)

## What the agent gets

- **16 core rules** that most of the books agree on, such as *change code in small steps and
  verify each one*, *keep structure changes and behavior changes apart*, and *assume every
  remote call can fail, hang or repeat*.
- **8 workflows** for the situations agents meet most: adding a feature, fixing a bug,
  changing untested code, refactoring, designing a module or API, designing a system,
  touching production paths (integrations, deploys, migrations), and reviewing a change.
- **Decision rules where the books disagree**: function length, comments, exceptions versus
  returned errors, when to add an interface, when to remove duplication, fakes versus mocks,
  how much cleanup belongs in a change, and small versus deep classes.
- **17 topic guides**, each merged across all 14 books, with step-by-step playbooks and a
  review checklist you can run against a diff.
- **1,028 source entries** (103 principles and 925 techniques). Each one gives the book's
  chapter and page, so every rule can be checked against the book.

The skill triggers on its own whenever the agent writes or changes non-trivial code, fixes a
bug, refactors, writes tests, reviews a pull request, designs a module, schema or service,
or changes production behavior. You don't need to mention it.

## Install

### Claude Code (plugin)

```text
/plugin marketplace add SobshDev/dev-skills
/plugin install software-craft@dev-skills
```

### Any agent that reads `SKILL.md` (Claude Code, Cursor, Codex, and others)

```bash
npx skills add SobshDev/dev-skills
```

### Manually

Copy the skill folder into your personal skills folder:

```bash
git clone https://github.com/SobshDev/dev-skills.git
cp -r dev-skills/skills/software-craft ~/.claude/skills/
```

To share it with a team, put it in the repository instead, at
`<your-repo>/.claude/skills/software-craft`.

## How it works

The skill holds about 210,000 words in total. The agent never loads all of it. It reads in
three layers and goes deeper only when the task calls for it.

| Layer | Size | When the agent reads it |
|---|---|---|
| [`SKILL.md`](skills/software-craft/SKILL.md) | ~5k words | Every time the skill triggers: core rules, workflows, tie-breakers, the guide router, and a checklist to run before finishing |
| [`guides/`](skills/software-craft/guides/) | 17 files, 5–8.5k words each | The one to three guides that match the task |
| [`books/<book>/`](skills/software-craft/books/) | 14 × `principles.md` + `techniques.md` | When the agent needs the full detail of one entry |

Every rule ends with the IDs of the entries it comes from, such as `[POSD-T35, CC-T33]`. The
prefix names the book, `P` marks a principle and `T` a technique. The agent uses these IDs to
look things up. It is told to keep them out of replies, commits and comments, and to explain
its reasons in plain words.

A rule in a guide looks like this:

```markdown
### 1. Get trusted tests in place before you change code

<the rule and the reason the books give> [WELC-P1, WELC-T37, CC-T75, REF-T01, PP-T43]

- **Do:** <concrete actions>
- **Not when:** <every caveat from every merged entry>
- **Check:** <what you can see in the code, tests or diff>
```

## The books

| Prefix | Book | Author(s) | Edition | Principles | Techniques |
|---|---|---|---|---:|---:|
| TF | *Tidy First?* | Kent Beck | 2023 | 7 | 37 |
| CC | *Clean Code* | Robert C. Martin | 2nd ed., 2025 | 6 | 77 |
| GOF | *Design Patterns* | Gamma, Helm, Johnson & Vlissides | 1994 | 6 | 75 |
| POSD | *A Philosophy of Software Design* | John Ousterhout | 2nd ed., 2021 | 7 | 57 |
| REF | *Refactoring* | Martin Fowler | 2nd ed., 2018 | 5 | 75 |
| WELC | *Working Effectively with Legacy Code* | Michael Feathers | 2004 | 8 | 73 |
| TDD | *Test-Driven Development: By Example* | Kent Beck | 2002 | 9 | 50 |
| PP | *The Pragmatic Programmer* | David Thomas & Andrew Hunt | 20th anniv. ed., 2019 | 9 | 74 |
| CA | *Clean Architecture* | Robert C. Martin | 2017 | 7 | 72 |
| DDD | *Learning Domain-Driven Design* | Vlad Khononov | 2021 | 8 | 70 |
| FPS | *Functional Programming in Scala* | Paul Chiusano & Rúnar Bjarnason | 2014 | 7 | 65 |
| RI | *Release It!* | Michael T. Nygard | 2nd ed., 2018 | 8 | 75 |
| DDIA | *Designing Data-Intensive Applications* | Martin Kleppmann & Chris Riccomini | 2nd ed., 2026 | 8 | 61 |
| SWE | *Software Engineering at Google* | Titus Winters, Tom Manshreck & Hyrum Wright | 2020 | 8 | 64 |
| | | | **Total** | **103** | **925** |

## The guides

| Guide | Read when the agent is… |
|---|---|
| [change-workflow](skills/software-craft/guides/change-workflow.md) | starting a change, splitting commits and PRs, deciding when to clean up |
| [testing](skills/software-craft/guides/testing.md) | writing tests first, choosing fakes or mocks, fixing slow or flaky tests |
| [legacy-code](skills/software-craft/guides/legacy-code.md) | changing code without tests, breaking dependencies to get a class into a test |
| [refactoring](skills/software-craft/guides/refactoring.md) | renaming, extracting, moving, inlining, replacing conditionals, deleting dead code |
| [readable-code](skills/software-craft/guides/readable-code.md) | naming, splitting functions, writing or deleting comments |
| [errors-and-contracts](skills/software-craft/guides/errors-and-contracts.md) | validating input, throwing or returning errors, cleaning up resources |
| [module-design](skills/software-craft/guides/module-design.md) | designing a class, module or API, judging coupling and depth |
| [design-patterns](skills/software-craft/guides/design-patterns.md) | about to add a factory, wrapper, strategy, observer or hierarchy |
| [architecture](skills/software-craft/guides/architecture.md) | crossing a layer, adopting a framework, splitting services |
| [domain-modeling](skills/software-craft/guides/domain-modeling.md) | modeling business rules, aggregates, domain events, bounded contexts |
| [functional-style](skills/software-craft/guides/functional-style.md) | pushing effects to the edges, using `Option`/`Either`, writing folds and combinators |
| [data-systems](skills/software-craft/guides/data-systems.md) | choosing a store, changing a schema, transactions, replication, streams |
| [production-reliability](skills/software-craft/guides/production-reliability.md) | adding remote calls, timeouts, retries, pools, health checks, rollouts |
| [security](skills/software-craft/guides/security.md) | building queries or commands from input, handling secrets, storing personal data |
| [performance-and-concurrency](skills/software-craft/guides/performance-and-concurrency.md) | optimizing, adding threads, locks, queues or pools |
| [debugging](skills/software-craft/guides/debugging.md) | reproducing a bug, bisecting a regression, handling an incident |
| [project-and-team](skills/software-craft/guides/project-and-team.md) | unclear requirements, dependencies, deprecations, docs, ownership |

## When the books disagree

The books don't always agree, and a skill that hides this gives worse advice. When they
pull in different directions, the skill states each position, then a **Decide** rule built
from the conditions the books give themselves. Here is the one on function length, from `SKILL.md`:

> **How long should a function be?**
> - **Clean Code:** keep functions near a dozen lines with at most two indentation levels,
>   though some functions read better undivided.
> - **Philosophy of Software Design:** split a method only when callers become simpler and
>   each part reads on its own, never for length alone.
> - **Refactoring and Tidy First:** inline helpers that are no clearer than their bodies,
>   and re-extract along better lines.
> - **Decide:** extract a block when its new name is more abstract than the code it hides.
>   Do not extract helpers that merely restate one statement, or that must be read together
>   to make sense.

## How it was built

1. **Extraction.** Each book was read chapter by chapter. Every principle and technique was
   paraphrased into the same shape (*Do / Why / When / Not when / Check*), with its source
   chapter and page.
2. **Verification.** Every candidate was checked against the original text by a separate
   pass, then each book's layers were cold-read for gaps, and the largest books got
   extra omission reviews.
3. **Synthesis.** For each of the 17 topics, one writer merged the entries of all 14 books.
   Agreements became one rule citing every book. Disagreements became decision rules.
   Ordered situations became playbooks.
4. **Fidelity review.** A fresh reviewer checked every cited sentence of `SKILL.md` and of
   each guide against the entries it cites. It looked for claims the entries don't make,
   wrong citations, dropped caveats, misstated disagreements and outside knowledge. Each
   guide got 12–27 fixes and `SKILL.md` got 35.
5. **Automated checks.** A checker confirms that every cited ID exists, that each of the
   1,028 entries is cited by at least one guide, and that every link resolves. It also
   confirms that no run of eight words is copied from any book.

The skill contains **no quotations** from the books. Everything is paraphrased.

## Evaluation

The repository includes four eval cases in
[`skills/software-craft/evals/`](skills/software-craft/evals/). Each one has a real task
and input files:

| Case | What it tests |
|---|---|
| `retry-flaky-payment-provider` | bounded retries, timeouts, idempotency keys, tests for the failure paths |
| `legacy-pricing-tier-change` | characterization tests before changing untested pricing code |
| `review-orders-pr` | a PR with planted problems (SQL injection, missing timeout, unbounded cache, mixed refactor) |
| `zero-downtime-column-rename` | expand/contract migration that both app versions survive |

First round, with and without the skill on the same model:

| | With skill | Without skill |
|---|---:|---:|
| Assertions passed | 20 / 20 | 19 / 20 |
| Mean time per task | 152 s | 87 s |
| Mean tokens per task | 89k | 57k |

To be honest about this result: a strong model already handles these tasks well, and most
of the assertions didn't tell the two runs apart. The differences showed up in the
details. With the skill, the agent:

- kept the column drop out of the migrations that run before rollout;
- calculated the worst-case retry wait correctly;
- committed the refactor separately from the rate change;
- checked that its new tests fail on deliberately broken code;
- warned that re-rendered old invoices would show new prices.

The run without the skill did better on one review (it caught a VAT and shipping
arithmetic issue) and on batching a backfill. Harder assertions are the next step.

Run the evals yourself with:

```bash
claude plugin eval . --eval-dir skills/software-craft/evals
```

## Limits

- The skill knows only what these 14 books say. It is silent on topics they don't cover,
  such as user-interface design or specific frameworks.
- The rules are strong defaults, not laws. Several books present their strictest rules as
  defaults to weigh against context, and the skill tells the agent to give its reason when
  it departs from one.
- The FP in Scala entries use Scala terms. The ideas carry over to any language with
  first-class functions.
- Loading the skill costs time and tokens: in the evals above, about a minute and 30k
  tokens per task.

## License

The skill text and code are released under the [MIT License](LICENSE).

The books belong to their authors and publishers. This project is not affiliated with or
endorsed by any of them. The skill paraphrases their ideas and cites chapter and page so you
can go to the source, and it does not replace reading them.
