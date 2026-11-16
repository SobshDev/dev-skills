# Security and data responsibility

This guide covers code that handles untrusted input, access to protected data, credentials and login, and the personal data a system stores or uses to decide about people. The single most important idea is that an outside value is bound, escaped or checked against an allow-list at the point where it reaches a query, command, page, file path or fetch.

**Read this when:** building a query, shell command, HTML page, file path or outbound fetch from request data, adding or changing an endpoint or admin control, handling a password, key or token, implementing login, deploying a new server or base image, storing personal data in logs, events or derived stores, handling an erasure request, placing data for users in several jurisdictions, training or tuning a model that accepts or rejects people.

**Entry IDs** such as `WELC-T12` point to `../books/<book>/techniques.md` (T) or `principles.md` (P);
the prefix table is in [SKILL.md](../SKILL.md).

## Contents

- [Rules: untrusted input](#rules-untrusted-input)
- [Rules: access and exposed surface](#rules-access-and-exposed-surface)
- [Rules: credentials, login and cryptography](#rules-credentials-login-and-cryptography)
- [Rules: personal data and decisions about people](#rules-personal-data-and-decisions-about-people)
- [Rules: verifying security work](#rules-verifying-security-work)
- [Playbooks](#playbooks)
- [Where the books disagree](#where-the-books-disagree)
- [Review checklist](#review-checklist)
- [More entries in this area](#more-entries-in-this-area)

## Rules: untrusted input

### 1. Bind external values into queries and commands

Pass every outside value to a database query, view or shell command as a bound parameter or a properly escaped value, and do not concatenate it into the command text. Pragmatic Programmer's reason is that concatenated input lets an attacker rewrite the command that actually runs, and Release It! says SQL injection has no excuse today. Pragmatic Programmer applies the rule to user, file and system data, and Release It! to values from users or from stored data, so a value that came out of your own database is not exempt. [PP-T74, RI-T42]

- **Do:** Use the driver's placeholder syntax for every value in SQL. For shell calls, pass arguments as a list to the process API instead of building a command string, so no input is interpolated into shell syntax.
- **Check:** No query or shell call in the diff is built with string concatenation, formatting or interpolation of a variable. Values appear only as bound parameters or escaped values.

```python
# Wrong: the value becomes part of the SQL text.
cur.execute("SELECT * FROM orders WHERE owner = '" + user_id + "'")

# Right: the driver binds the value as data.
cur.execute("SELECT * FROM orders WHERE owner = %s", (user_id,))

# Wrong: the filename is parsed by a shell.
subprocess.run(f"convert {name} out.png", shell=True)
# Right: arguments go straight to the program, no shell parsing.
subprocess.run(["convert", name, "out.png"])
```

### 2. Generate HTML with an auto-escaping template or builder

Produce markup through a template engine or builder API that escapes inserted values by default. Release It! warns against assembling structured output by gluing strings together, and this applies to request data and to stored values alike. [RI-T65]

- **Do:** Insert request and database values into markup only through the template's normal substitution, which escapes them. Treat any raw or unescaped-output helper as a finding that needs a reason.
- **Check:** HTML generation in the diff uses an escaping template or builder, and no variable is concatenated into an HTML string.

### 3. Do not build file paths from request input

Release It! warns against assembling a file path from a filename or parameter that the caller supplies, including the names of uploaded files. [RI-T66]

- **Do:** Keep request parameters and uploaded filenames out of path construction for both reads and writes.
- **Check:** No path in the diff is joined or concatenated from a request parameter or an uploaded filename.

### 4. Fetch only hosts on an allow-list

When the service accepts a URL from an external caller and fetches it, accept only hosts on an explicit allow-list. Release It! notes that the caller controls such a URL, so fetching it arbitrarily makes the service send requests on the caller's behalf. [RI-T58]

- **Do:** Parse the URL, compare its host with a configured allow-list, and refuse anything else before any network call is made.
- **Check:** Fetch code passes a caller-supplied URL to the HTTP client only after an allow-list check of its host.

```python
ALLOWED_HOSTS = {"images.partner.example", "cdn.partner.example"}

def fetch_avatar(raw_url: str) -> bytes:
    host = urllib.parse.urlsplit(raw_url).hostname
    if host not in ALLOWED_HOSTS:
        raise ValueError(f"host not allowed: {host!r}")
    return http.get(raw_url).content
```

### 5. Validate at the boundary, and still bind at use

Check each external value once where it enters the system, and name the invalid value in the error. Pragmatic Programmer and Learning DDD both put that check in one place, at the entry point or inside the value object that represents the concept, so callers cannot skip it. The binding and escaping rules above carry no exception for input that was validated earlier, so do both. [PP-T14, DDD-T14, PP-T74, RI-T42]

- **Do:** Validate types and ranges at the documented entry point or in the value object's constructor. Then bind or escape the value wherever it reaches a query, command or page. Add invalid and boundary inputs to the tests.
- **Not when:** Routine preconditions inside the code flag caller bugs, not bad outside input, so they are not the boundary check (PP-T14).
- **Check:** Each external value has one validation point, and tests feed it invalid and boundary values. [PP-T42]

For how to report and propagate validation failures, see [errors and contracts](errors-and-contracts.md). For value objects that own their validation, see [domain modeling](domain-modeling.md).

## Rules: access and exposed surface

### 6. Authorize every request for a protected resource

Run an authorization check on every request that reads or changes protected data, whatever route the caller took to reach the URL. Release It! asks for the check on each request, not only the first one in a flow, and Pragmatic Programmer asks that data endpoints verify credentials before they act. [RI-T67, PP-T49]

- **Do:** Put the check in each handler for protected objects, or in a layer every such handler passes through, and run it before any read or change.
- **Check:** Each handler for a protected object performs an authorization check on every call, and no handler relies on an earlier page having checked.

### 7. Expose only entry points with a current, documented need

Every endpoint, port and data entry point is a route for attackers, so Pragmatic Programmer keeps only those with a present, written-down need and requires authentication on those that read or change data. DDIA adds that production should offer no open-ended SQL access, because such queries reach data in ways the application never planned for. [PP-T49, DDIA-T03]

- **Do:** Remove or close endpoints and ports nobody currently needs. Point analysts at a warehouse or replica rather than at the operational database.
- **Not when:** Occasional maintenance or troubleshooting queries may still be run by hand against the operational database (DDIA-T03).
- **Check:** Each exposed endpoint or port has a documented need, data endpoints check credentials first, and production exposes no open SQL endpoint.

### 8. Keep hazardous controls out of production

Release It! calls schema changes, delete-and-reseed and whole-cache flushes hazardous in production, so leave them out of the production admin API. Clean Architecture keeps a testing API that skips secured steps out of production builds for the same reason. Pragmatic Programmer allows diagnostics behind a per-user switch but not where end users or unauthorized people could see them. [RI-T41, CA-T71, PP-T63]

- **Do:** Ship admin controls that operators need during incidents, such as a breaker reset (RI-T40), and leave out anything that alters schema, deletes data or flushes a whole cache. Build test-only state shortcuts into test builds only.
- **Not when:** Breaker resets stay allowed in production (RI-T41). A breaker reset control does not apply when the service has no circuit breakers (RI-T40).
- **Check:** The production admin API has no schema, delete or whole-cache flush endpoint, the testing API is absent from production builds, and diagnostic switches are limited to authorized users.

Operational controls in general are covered in [production reliability](production-reliability.md).

### 9. Hold elevated rights for the shortest possible scope

When a task needs root, administrator or another elevated right, request only the rights it needs, use them in a short scope and drop them afterward. Pragmatic Programmer's reason is that rights held for less time leave less room for a bug or an attacker to misuse them. [PP-T50]

- **Do:** Wrap the privileged call in the smallest block that needs it, and drop the right as soon as the block ends.
- **Check:** Privileged calls sit inside short scopes, and the process gives up the rights afterward.

### 10. Send identifiers in notifications, and fetch sensitive data with authorization

When an event or notification concerns sensitive data, send a short message with identifiers and let the consumer query the producer for the details. Learning DDD notes that notifications can be stale or arrive before the write, so the producer is the reliable source, and the consumer's query passes an authorization check. [DDD-T52]

- **Do:** Put identifiers, not sensitive fields, in the notification. Have the handler authorize and call the producer's detail endpoint before it uses the data.
- **Check:** Notification payloads carry identifiers only, and the handler authorizes before calling the detail endpoint.

## Rules: credentials, login and cryptography

### 11. Keep credentials out of source, images and artifacts

Read keys, passwords and license values at runtime from configuration outside the code, and supply them at startup or from an override location outside the release artifact. Pragmatic Programmer's reason is that a key committed to version control stays readable in every clone and in the history. Release It! extends this to container images, build outputs and install directories. [PP-T35, RI-P8]

- **Do:** Load each credential from external configuration when the process starts. Keep everything else needed to build and deploy under version control, except the credentials (PP-T17). Treat hosts and ports that vary by environment the same way (PP-T34).
- **Not when:** Values that never vary between environments, such as protocol limits, can stay in code (PP-T34). That exception does not cover credentials.
- **Check:** Source files, images and build outputs contain no credential or license literals and no production passwords, hostnames or ports. Credentials are read at runtime.

### 12. Replace every default credential before production

Release It! says a default password must not remain on a production server. This covers databases, admin consoles and container base images. [RI-T43]

- **Do:** Have the deployment scripts or configuration set new admin credentials for each installed component.
- **Check:** Deployment config or scripts set new admin credentials, and no component keeps its factory login.

### 13. Send credentials only over TLS

Credentials sent in the clear can be read by anyone who can observe the traffic, so send them only over TLS. This applies to web services you expose and to connections between services that exchange credentials. [RI-T44]

- **Do:** Use https URLs for every client and endpoint that carries credentials.
- **Check:** No credential-bearing client or endpoint in the diff uses a plain http URL.

### 14. Use vetted libraries and providers for cryptography and login

Use established libraries and authentication providers for encryption, hashing, secure tokens, password storage and social sign-in, rather than code you write yourself. Pragmatic Programmer's reason is that such libraries avoid security errors custom code would make. Learning DDD treats authentication as a generic, solved problem whose maintained solutions receive security patches over time. [PP-T70, DDD-T05]

- **Do:** Call a vetted library or provider SDK for every hash, cipher, token and login step, and keep its version maintained.
- **Not when:** An expert with peer review and field trials may write primitives. A provider must suit your users. Learning DDD builds in-house only when integrating the ready solution costs more than building it. See the tension below for how these combine.
- **Check:** Login and crypto code calls a vetted library or provider SDK, with no hand-written hashing, cipher or credential storage.

### 15. Accept long passwords with any characters

Accept passwords of at least 64 characters, including spaces and Unicode, and do not impose composition rules or forced timed changes. Pragmatic Programmer notes that truncating or restricting input blocks the strong passphrases users would otherwise pick. [PP-T48]

- **Do:** Set the maximum length to at least 64 characters, accept any character, and remove rules that require a mix of character classes or a change on a schedule.
- **Check:** Password limits are at least 64 characters, and no code truncates the input or forces a character mix or timed change.

### 16. Throttle failed logins per account instead of locking accounts

Limit how many login attempts can be made against one account by throttling or adding delays. Release It! points out that locking an account after a few failures lets an attacker lock out the legitimate user. [RI-T74]

- **Do:** Count failed attempts per account in the login path, and slow down or delay further attempts as the count grows.
- **Check:** The login path counts failures per account and applies a throttle or delay, and it does not lock the account outright.

### 17. Keep security-relevant dependencies patched

Learning DDD notes that maintained solutions receive security patches over time and asks that they be kept updated, with maintained versions pinned and upgraded regularly. Software Engineering at Google prefers small, regular upgrades, because accumulated change makes each later upgrade larger and riskier. [DDD-T05, SWE-T01, SWE-P1]

- **Do:** Upgrade libraries and runtimes in small, frequent steps, and script any step you repeat.
- **Not when:** An upgrade may be skipped when it costs more than it gives over the code's lifespan (SWE-T01). Short-lived or narrow code may skip heavy practices, but a long-lived fork still needs security fixes. Code that is never upgraded may take any available dependency (SWE-P1).
- **Check:** Dependency manifests pin maintained versions, and dependency update commits are frequent and small.

Upgrade policy in general is covered in [project and team](project-and-team.md).

## Rules: personal data and decisions about people

### 18. Design erasure through every copy of personal data

Plan erasure so that every copy of a person's data can be deleted on request, including copies in logs, event streams and derived datasets. DDIA's reason is that append-only logs and derived stores keep old copies, so deleting only the primary record leaves the request unmet. [DDIA-T61]

- **Do:** List each store that holds the personal data, including logs and derived datasets, and give each one an erasure path. Have events carry identifiers instead of personal fields wherever possible, so fewer records need rewriting.
- **Check:** The erasure path rewrites or removes stored records in logs and derived datasets as well as the primary store, and event schemas hold IDs rather than personal fields.

### 19. Encrypt personal fields in immutable events with a per-aggregate key

Where stored events cannot be edited, encrypt their sensitive fields with a key that belongs to one aggregate, and delete that key to make the data unreadable. Learning DDD offers this as the way to make personal data erasable in an event store, for example under GDPR. [DDD-T31, DDIA-T61]

- **Do:** Store one key per aggregate ID in a key store separate from the events, encrypt the personal fields with it through a vetted library (PP-T70), and implement erasure as deletion of that key.
- **Check:** Sensitive event fields are stored encrypted, and keys live in a separate store indexed by aggregate ID.

```text
# On write: encrypt personal fields with this aggregate's own key.
key   = key_store.get_or_create(aggregate_id)
event = {"type": "CustomerRegistered", "id": aggregate_id,
         "email": crypto_lib.encrypt(key, email)}
event_store.append(aggregate_id, event)

# On erasure: the events stay untouched, but their personal fields can no longer be read.
key_store.delete(aggregate_id)
```

### 20. Append corrections, except when erasing personal data

Record changes, corrections and raw inputs as new appended records instead of editing or deleting originals. DDIA keeps the originals as the evidence needed to recover from bugs and to study change over time. Erasure on request is the stated exception. Learning DDD applies the same append-only rule to analytical fact rows. [DDIA-T60, DDD-T64]

- **Do:** Insert corrections as new records, and route erasure requests through rules 18 and 19 instead.
- **Not when:** Erasure of personal data on request follows DDIA-T61 instead (DDIA-T60).
- **Check:** Outside the erasure path, no update or delete statement touches a logged or stored input.

Append-only storage and event sourcing in general are covered in [data systems](data-systems.md) and [domain modeling](domain-modeling.md).

### 21. Keep residency-bound data in its permitted jurisdiction

Where a residency law applies, store and process each user's data in the jurisdiction that law names, and map each tenant to a permitted region. DDIA's reason is that residency laws bind where personal data may be stored and processed, and it lists legal requirements among the reasons that can force a distributed design. [DDIA-T05, DDIA-P6]

- **Do:** Record the jurisdiction for each user or tenant, and configure storage location or shard placement from it.
- **Not when:** This rule does not apply when the applicable residency law covers only medical or financial data (DDIA-T05).
- **Check:** Storage locations or shard placement are configured per user or tenant jurisdiction.

### 22. State who pays for wrong rejections

When a model or rule accepts or rejects people for jobs, loans, insurance, travel or housing, weigh how a wrong rejection harms the person it excludes. DDIA's reason is that the threshold moves errors onto people, so that harm must be counted beside accuracy. [DDIA-T58]

- **Do:** When choosing a threshold, write down how false accepts and false rejects are weighted and which groups bear the false rejects.
- **Check:** Model risk review names the excluded groups, and the threshold configuration states how the two kinds of error are weighted.

### 23. Inspect training inputs for systematic bias

Before training a model on records about people or on past decisions about them, inspect the inputs for systematic bias. DDIA notes that models learn and amplify the bias in their inputs, and that past decisions used as labels often carry the same bias, so treat them as possibly discriminatory until reviewed. [DDIA-T59]

- **Do:** Write a bias analysis into the dataset documentation, and check features such as postal code and IP address for correlation with protected traits.
- **Check:** Dataset docs include a bias analysis, and feature review records the proxy-variable checks.

## Rules: verifying security work

### 24. Add a regression test for every security defect

Whenever exploratory or security testing finds a defect, add an automated test that exercises it, because that test runs far more often than any manual check. TDD adds that passing unit tests alone do not establish security correctness. [SWE-T57, TDD-P8]

- **Do:** Reproduce the security defect in a test that fails before the fix (PP-T20), then fix it. Keep invalid, boundary and hostile inputs in the suite (PP-T42).
- **Check:** The security fix diff includes a test that exercises the reported failure.

### 25. Raise security problems in review even in untouched code

Software Engineering at Google scopes analyzer warnings to the lines a change touches, but it makes an exception for important existing problems such as security issues. [SWE-T17]

- **Do:** When an analyzer or review turns up an important existing problem, such as a security issue, in code the change does not touch, highlight it even though the diff did not introduce it.
- **Check:** Review notes or the PR description mention any security issue spotted outside the changed lines.

Review practice in general is covered in [change workflow](change-workflow.md), and test design in [testing](testing.md).

## Playbooks

### When you add an endpoint that reads or changes data

1. Write down the current need for the endpoint, and do not add it if nobody needs it now. [PP-T49]
2. Require authentication, and authorize the caller on every request for each protected object it touches. [PP-T49, RI-T67]
3. Validate each input once at the entry point or in its value object. [PP-T14, DDD-T14]
4. Bind every value into queries and shell calls, and render any HTML through an escaping template. [PP-T74, RI-T42, RI-T65]
5. Serve it over TLS if it carries credentials. [RI-T44]
6. Add tests with invalid, boundary and unauthorized requests. [PP-T42, RI-T67]

### When the caller supplies a URL, filename or path

1. If the service will fetch the URL, check its host against an allow-list before any network call. [RI-T58]
2. Keep the supplied filename or parameter out of any file path you build, for reads and writes. [RI-T66]
3. Reject bad values at the boundary with an error that names them. [PP-T14]
4. Add tests with hosts outside the allow-list and with hostile filenames. [PP-T42]

### When you implement login or password handling

1. Choose a vetted authentication provider or library, and confirm it suits your users. [PP-T70, DDD-T05]
2. Accept passwords of at least 64 characters with any characters, and drop composition and expiry rules. [PP-T48]
3. Hash and store credentials only through the vetted library. [PP-T70]
4. Throttle or delay failed attempts per account rather than locking the account. [RI-T74]
5. Serve the login endpoint and every credential exchange over TLS. [RI-T44]
6. Read any provider keys from external configuration at runtime. [PP-T35, RI-P8]

### When you add a credential or deploy a new server or image

1. Put the credential in external configuration or an override location outside the artifact, and read it at runtime. [PP-T35, RI-P8]
2. Keep the rest of the deployment definition in version control, without the credential. [PP-T17]
3. Replace every default password on databases, consoles and base images in the deployment scripts. [RI-T43]
4. Grant the process only the rights it needs, and scope any elevated step tightly. [PP-T50]
5. Close ports and endpoints the deployment does not need, and leave hazardous admin controls out. [PP-T49, RI-T41]
6. Scan the image and build outputs for passwords, hostnames and ports before release. [RI-P8]

### When you introduce a store, log or event that holds personal data

1. Where a residency law applies, decide which jurisdiction each user's or tenant's copy must live in, and configure placement from it. [DDIA-T05]
2. Prefer identifiers to personal fields in events and notifications. [DDIA-T61, DDD-T52]
3. If personal fields must go into immutable events, encrypt them with a per-aggregate key held in a separate store. [DDD-T31]
4. Add the new store, log or derived dataset to the erasure path. [DDIA-T61]
5. Keep other corrections append-only. [DDIA-T60]

### When you handle an erasure request

1. Find every copy, including logs, event streams and derived datasets, not only the primary record. [DDIA-T61]
2. For encrypted event fields, delete the aggregate's key. [DDD-T31]
3. For other append-only or derived stores, rewrite the stored records to remove the personal data. [DDIA-T61]
4. Treat this as the one allowed exception to append-only correction, and keep it on its own code path. [DDIA-T60]

### When a model or threshold decides about people

1. Review the training inputs and any past-decision labels for systematic bias, and record the analysis. [DDIA-T59]
2. Check proxy features such as postal code and IP address for correlation with protected traits. [DDIA-T59]
3. Name the groups a false rejection would exclude, and state how false accepts and false rejects are weighted in the threshold. [DDIA-T58]

### When you fix a security defect

1. Write a test that reproduces the defect and fails before the fix. [SWE-T57, PP-T20]
2. Fix it with the matching rule above, such as binding, escaping, an allow-list or an authorization check. [PP-T74, RI-T42, RI-T65, RI-T58, RI-T66, RI-T67]
3. Report any similar problem you see in code the change does not touch. [SWE-T17]
4. Do not treat a passing suite as proof that the code is secure. [TDD-P8]

## Where the books disagree

### Can append-only history coexist with erasure?

- **DDIA:** Record corrections as new records and do not edit or delete originals, which are the evidence for recovery and history. [DDIA-T60]
- **Learning DDD:** Event stores allow only appends and reads, stored events are not rewritten, and analytical facts are not updated or deleted. [DDD-T28, DDD-T33, DDD-T64]
- **DDIA:** Erasure must reach every copy, which means rewriting stored records in logs and derived datasets. [DDIA-T61]
- **Learning DDD:** Encrypt personal event fields with a per-aggregate key and delete the key, which leaves the events unedited. [DDD-T31]
- **Decide:** Erasure on request is the stated exception to append-only correction (DDIA-T60). In an event store, keep the events unedited by encrypting personal fields per aggregate and deleting the key (DDD-T31). Elsewhere, rewrite the records in each log and derived dataset (DDIA-T61). Keeping personal fields out of events in the first place, by storing IDs, shrinks both jobs (DDIA-T61). Learning DDD allows a controlled change to the event store only for exceptional cases such as data migration (DDD-T28), and it does not name erasure among them, so do not assume an edit is allowed there. [DDIA-T60, DDIA-T61, DDD-T31, DDD-T28]

### Should you build authentication or cryptography yourself?

- **Pragmatic Programmer:** Use established libraries and providers for encryption, hashing, tokens and login. An expert with peer review and field trials may write primitives, and a provider must suit your users. [PP-T70]
- **Learning DDD:** Adopt a maintained product for generic capabilities such as authentication, unless integrating it costs more than building the feature. [DDD-T05]
- **Decide:** Default to a vetted library or provider, which both books recommend. Build authentication yourself only when integrating a ready solution costs more than building it (DDD-T05). Write cryptographic primitives only when an expert writes them with peer review and field trials (PP-T70). If no available provider suits your users, the entries give no further rule, so raise it with the user. [PP-T70, DDD-T05]

### Which operational controls belong in production?

- **Release It!:** Expose a runtime control that resets circuit breakers, so operators can restore an integration once a fault clears. [RI-T40]
- **Release It!:** Leave schema changes, delete-and-reseed and whole-cache flushes out of the production admin API. [RI-T41]
- **Pragmatic Programmer:** Expose only entry points with a current, documented need, and authenticate those that read or change data. Show diagnostics only to selected, authorized users. [PP-T49, PP-T63]
- **Clean Architecture:** Keep the testing API, with its power to skip secured steps, out of production. [CA-T71]
- **Decide:** Include a control when operators have a current, documented need for it and it is not one of the hazardous kinds Release It! names. A breaker reset qualifies when the service has breakers (RI-T40). Schema changes, reseeds, whole-cache flushes and test shortcuts do not. Put every remaining control behind authentication. [PP-T49, RI-T40, RI-T41, CA-T71, PP-T63]

### How do residency limits fit with cross-datacenter redundancy?

- **DDIA:** Give each component whose failure would take the whole system down a replica or failover path, with replicas on separate machines or in separate datacenters. [DDIA-T04]
- **DDIA:** Store and process residency-bound data only in its permitted jurisdiction. [DDIA-T05]
- **Decide:** Residency placement is a legal requirement, and DDIA lists legal requirements among the forces that shape distribution (DDIA-P6). DDIA-T04 is satisfied by separate machines or datacenters, so place replicas of residency-bound data on separate machines or datacenters inside the permitted region. The entries give no rule for a region that cannot host a separate replica, so record that gap and raise it with the user. [DDIA-T04, DDIA-T05, DDIA-P6]

## Review checklist

- [ ] Every query and shell call binds outside values as parameters, with no concatenation or interpolation, including values read from storage. [PP-T74, RI-T42]
- [ ] HTML is produced by an escaping template or builder, with no variables glued into markup. [RI-T65]
- [ ] No file path is built from a request parameter or an uploaded filename. [RI-T66]
- [ ] Any fetch of a caller-supplied URL checks the host against an allow-list first. [RI-T58]
- [ ] Each external value is validated at one entry point, and tests include invalid and boundary inputs. [PP-T14, PP-T42]
- [ ] Every handler for a protected object authorizes the caller on each request. [RI-T67]
- [ ] Each new endpoint or port has a documented need, and data endpoints check credentials before acting. [PP-T49]
- [ ] The production admin API has no schema, reseed or whole-cache flush control, and test-only APIs are absent from production builds. [RI-T41, CA-T71]
- [ ] Privileged calls sit in short scopes, and rights are dropped afterward. [PP-T50]
- [ ] Source, images and build outputs contain no credentials, license keys, or production hostnames and ports. [PP-T35, RI-P8]
- [ ] Deployment scripts replace default passwords on every database, console and base image. [RI-T43]
- [ ] Every credential-bearing client and endpoint uses https. [RI-T44]
- [ ] Hashing, ciphers, tokens and login use a vetted library or provider, not custom code. [PP-T70]
- [ ] Password fields accept at least 64 characters of any kind, with no truncation, composition rule or forced expiry. [PP-T48]
- [ ] Failed logins are throttled or delayed per account, without outright lockout. [RI-T74]
- [ ] Notifications about sensitive data carry identifiers, and consumers authorize before fetching details. [DDD-T52]
- [ ] Every new store, log or derived dataset holding personal data is covered by the erasure path. [DDIA-T61]
- [ ] Personal fields in immutable events are encrypted with a per-aggregate key held in a separate store. [DDD-T31]
- [ ] Outside the erasure path, corrections are inserts, not updates or deletes of stored inputs. [DDIA-T60]
- [ ] Storage or shard placement for residency-bound data follows each user's or tenant's jurisdiction. [DDIA-T05]
- [ ] Models that gate people have a recorded bias analysis of inputs and a threshold that states how both error kinds are weighted. [DDIA-T59, DDIA-T58]
- [ ] Each security fix adds a test that exercises the reported failure. [SWE-T57]

## More entries in this area

- `RI-T40` — Expose a runtime control that resets breakers: the admin control Release It! keeps allowed in production while it removes hazardous ones, when the service has circuit breakers.
- `CA-T71` — Give tests a dedicated testing API: when tests need to skip secured steps, and why that API stays out of production.
- `PP-T63` — Use feature switches for diagnostics and unfinished features: when extra diagnostics must reach only selected, authorized users.
- `DDIA-T03` — Keep analytical queries off operational databases: when someone asks for open SQL access to production data.
- `DDD-T28` — Append events only and pass the expected version: the event-store contract that erasure must work around.
- `DDD-T33` — Version event schemas instead of rewriting history: when an event's shape changes after events of that type were stored.
- `DDD-T64` — Record analytics as append-only facts: when building an analytical model for reports, whose fact rows are never updated or deleted.
- `DDIA-T04` — Remove single points of failure from the architecture: when replicas must also respect residency limits.
- `SWE-T01` — Upgrade dependencies in small regular increments: when scheduling dependency or runtime upgrades for a long-lived project.
