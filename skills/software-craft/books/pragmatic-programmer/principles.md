# The Pragmatic Programmer — David Thomas & Andrew Hunt (20th Anniversary edition, 2019)

## Summary
The book argues for deliberate craftsmanship. Developers own outcomes, keep knowledge in one trusted place, and design for change. Work proceeds in small steps checked by fast feedback, and repetitive work is automated. The advice covers code, design, team process and delivery, and each practice should be judged by its context.

## Principles

### PP-P1: Own outcomes and repair broken windows

Own the results you accept. When you make a mistake, admit it plainly and offer ways to recover rather than excuses. Repair bad design or poor code as soon as you notice it, within the change that touches it.

- **Apply:** Fix known defects in code you are changing, and report other problems with a next step.
- **Limits:** Decline work whose risks or ethics you cannot accept.
- **Check:** Code the change touches has its known defects corrected in that change, and status notes pair other problems with next steps.
- **See:** PP-T04, PP-T05, PP-T72
- **Source:** ch. 1, 7, 9

### PP-P2: Keep feedback short so mistakes stay small

Work in small steps, and check the feedback from each one before taking the next. The rate of feedback limits how fast you should work, so a change too large to confirm quickly should be split.

- **Apply:** Split large changes into increments, each confirmed by a test, demo or review.
- **Check:** Pull requests are small, and each has a test or demo that confirms it.
- **See:** PP-T06, PP-T07
- **Source:** ch. 4, 8

### PP-P3: Keep each piece of knowledge in one place

Each fact needs one trusted, authoritative representation. Repeats in code, docs, schemas or config drift apart, so one rule should need one edit.

- **Apply:** Consolidate duplicated knowledge when you find it, and generate or link repeated facts from their source.
- **Limits:** Identical-looking code may encode different rules that change separately.
- **Check:** Changing one business rule edits exactly one location.
- **See:** PP-T08, PP-T09
- **Source:** ch. 2, 7

### PP-P4: Decouple modules so changes stay local

Keep each component coupled to as few others as possible. Unrelated parts forced to change together make every change wide, and indirect dependencies count as coupling too.

- **Apply:** Add a dependency only when a module truly needs it, and count indirect dependents when judging impact.
- **Check:** A change inside one module's internals touches no other module's files, and new imports point to only a few modules.
- **See:** PP-T10, PP-T11
- **Source:** ch. 2, 5

### PP-P5: Hide volatile dependencies behind your own code

Wrap databases, SDKs, services and file systems in an interface you control, so a vendor change stays inside one module. Prefer decisions you can reverse later, so the code stays adaptable.

- **Apply:** Keep external calls in a dedicated adapter that domain code uses.
- **Check:** SDK and HTTP calls appear only inside wrapper modules.
- **See:** PP-T12, PP-T13
- **Source:** ch. 2, 5

### PP-P6: Check assumptions and let failures be loud

Assume you will err, so check your own assumptions as well as external input. Treat every error as meaningful, check operations that can fail, and treat a broken contract as a bug rather than a normal path.

- **Apply:** Validate external input at entry, and test each assumption, asserting conditions you are sure cannot occur (PP-T15).
- **Check:** Entry points validate types and ranges, and error paths never fail silently.
- **See:** PP-T14, PP-T15, PP-T16
- **Source:** ch. 4, 7

### PP-P7: Automate repeatable work and version everything

Keep source, config without credentials, docs, scripts and notes in version control (PP-T35). Build, test and deploy run from scripts, so any capable machine can reproduce them.

- **Apply:** Replace manual steps and written instructions with versioned scripts or pipelines.
- **Check:** The repository holds build, test and deploy definitions as scripts or pipeline files.
- **See:** PP-T17, PP-T18
- **Source:** ch. 3, 9

### PP-P8: Debug with evidence before changing code

Reproduce each defect and record exact observations before forming a hypothesis. Suspect your own recent change and your own call sites before the platform, and fix root causes rather than symptoms.

- **Apply:** Reproduce the defect, and record the exact steps and observations before editing.
- **Check:** Notes record the reproduction and the suspected cause before the edit.
- **See:** PP-T20, PP-T21, PP-T22, PP-T58
- **Source:** ch. 3, 7

### PP-P9: Validate requirements with working demos

Requirements are discovered, so show users working code early and let their feedback reshape them. Ask stakeholders how they will judge success a month or a year after delivery.

- **Apply:** Demonstrate a runnable slice to users early, and record each refined requirement in its ticket.
- **Check:** Each iteration ends with a demo or review.
- **See:** PP-T23, PP-T24, PP-T25
- **Source:** ch. 8, 9
