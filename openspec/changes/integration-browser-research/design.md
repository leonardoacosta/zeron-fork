# Browser provider isolation research: design boundary

## Read first
`../../../docs/fork-prd.md`, `../prd-execution-map/design.md`, this proposal/spec, and prerequisite `ci-promotion-gates`. Baseline `1427da6`; refresh citations against the current checkout. Listed paths are read-only anchors.

## Existing surfaces and responsibilities
- `crates/ui/src/browser/mod.rs`: current browser actions and UI boundaries.
- `crates/ui/src/browser/model.rs`: browser state/data model.
- `crates/ui/src/browser/macos.rs`: native browser process and lifecycle behavior.
- `scripts/run-macos-browser-fixture.sh`: existing local fixture launch contract; inspect only, do not run without explicit local fixture authorization.
- `docs/fork-prd.md`: approved isolation and scope requirements.

All listed paths are pre-existing read-only anchors for this research. They are not proposed product edits.
Existing anchors remain exactly: `crates/ui/src/browser/mod.rs`, `crates/ui/src/browser/model.rs`, `crates/ui/src/browser/macos.rs`, `scripts/run-macos-browser-fixture.sh`, `docs/fork-prd.md`.

## Bounded questions
For the built-in browser and each candidate independently, consult official public docs and ask: What exact product/version/platform is documented? Does its documented storage context isolate cookies, cache, local storage and downloads per requested work profile/session? How is signed-in scope explicitly granted and revoked? What native session/process ID associates actions with that scope? What documented action proves startup, status and completed stop/cancellation? Does close return before child work ends? What evidence can be captured and redacted? Where does page data travel, including cloud upload/telemetry? What credentials are stored and where? Cite exact page/section/version. Unknown means no inference.

## Evidence states and child adapter schema
Each evidence row contains: `claim_id`, `subject`, `claim`, `state` (`verified`, `contradicted`, `unknown`, `blocked`), `evidence_kind` (`official_doc`, `local_source`, `local_observation`), `source_or_command`, `version_or_commit`, `observed_at_utc`, `result_or_excerpt`, `scope`, `limitations`, `reviewer`. Public documentation establishes documented claims only. A local harmless fixture observation, if separately authorized, is not proof of provider-wide behavior.

Each possible follow-up record contains: `adapter_id` (provisional label, not API), `system_identity`, `supported_versions`, `capability`, `owner_boundary`, `inputs_and_scope`, `outputs_and_states`, `native_id`, `start_proof`, `stop_proof`, `status_proof`, `configuration_source`, `auth_boundary`, `data_boundary`, `isolation_boundary`, `read_only_operations`, `write_operations` (`not authorized` absent separate approval), `failure_and_retry_behavior`, `compatibility`, `evidence_refs`, `rejection_reasons`, `decision_state` (`candidate`, `blocked`, `rejected`, `needs_review`). This is research output, not a runtime interface.

## Rejection criteria
A candidate is rejected or blocked if profile/session storage isolation is undocumented or unproven; screenshot support is the only evidence; session identity cannot be tied to actions; close returns without action-stop proof; credentials or private data may be uploaded without a fully documented and approved boundary; product/version is unpinned; meaningful evidence cannot be redacted; or testing requires modifying a user profile, private page, credentials, provider install/configuration, external probe, or spend. Do not choose based only on an available skill name.

## Failure scenarios
- C01: screenshots without isolated storage do not meet isolation.
- C02: close returns before action-stop proof: cancellation remains `unknown`/`blocked`.
- C03: cloud upload required: disclose boundary; no private page use.
- Unknown prerequisite: block with reason rather than claiming success.

## Scope and acceptance boundary
Public official documentation and read-only local source inspection only. No browser session, user profile, private page, credentials, external provider API, network probe, installation, configuration change, or cloud upload. A future harmless local fixture probe requires explicit scope/authorization and must not be represented as public API proof. Research does not select a provider, claim a runtime interface, or claim all future adapters are implementable.

## Rollback
Only these canonical design/tasks files may change. Preserve existing browser behavior and all user profile state.

## Filled source-evidence example
Verified against actual source at stated commit; concurrent unrelated working-tree edits are not runtime evidence.
```json
{
  "claim_id": "local-browser-close",
  "subject": "BrowserSurface",
  "claim": "Source hides surface and drops native handle; process stop and storage isolation not established.",
  "state": "verified",
  "evidence_kind": "local_source",
  "source_or_command": "crates/ui/src/browser/mod.rs:408-435",
  "version_or_commit": "b9623ae80225b924fe00d577d600f65938967bf6",
  "observed_at_utc": "2026-09-26T19:56:18Z",
  "result_or_excerpt": "close sets Presentation::Hidden; self.native = None",
  "scope": "Read-only source declaration, not runtime acceptance",
  "limitations": "No browser process/action termination or profile isolation probe.",
  "reviewer": "coordinator source verification"
}
```

## Bounded discovery stop rule
For each named subject/question inspect the official documentation entry point and one relevant official reference page, plus listed local anchors and their direct callers. Stop once an authoritative source answers that question. If two relevant official pages do not establish the claim, record unknown with exact searched sources, not a guessed interface. Missing/denied required source is blocked. Conflicting authoritative sources require escalation rather than optimistic choice. A later separately scoped research iteration may widen search; this budget is a research stopping rule, not proof of absence. Unknown product identity stays unknown without normalizing spelling. Persist rows in this design, never only disposable scratch.

## Research execution record

Bounded research completion reviewed 2026-09-30 using the 2026-09-27 evidence below and fresh passing planning checks. This closes only the bounded documentation/source inquiry under its explicit unknown/blocked stop rule. Historical dirty-tree source citations are not newly verified current-source evidence. C01 remains blocked, C02/C03 remain unknown, and the CI prerequisite remains blocked. Provider/interface selection and runtime implementation/acceptance remain unapproved.

Research retrieved 2026-09-27 UTC. Official docs below support documented behavior only, not a selected provider or runtime acceptance. No browser fixture, profile, private page, credentials, provider API, endpoint probe, install/config change, cloud upload, or spend was used. The named candidate is Playwright as a documentation subject only; this does not select it.

### Requirement coverage

| Requirement/scenario | Coverage and evidence | Outcome |
|---|---|---|
| ZF-17 | E-LOCAL-1 through E-LOCAL-4; E-APPLE-1; E-PW-1 through E-PW-4 | Existing embedded browser is per-window ephemeral website data by source; its session/profile semantics do not establish the full ZF-17 scope. Playwright documents isolated contexts and storage handling, but several required controls remain unknown. |
| ZF-19 | E-PW-3, E-PW-4; E-LOCAL-2 through E-LOCAL-4 | Completion, explicit scope grant/revoke, redaction, and credential boundary are incomplete or unknown. |
| C01 | E-APPLE-1, E-LOCAL-1, E-PW-1 | Screenshots are not isolation evidence. Existing source shares one non-persistent store across a `BrowserContext`; Playwright documents isolated contexts but download behavior must be separately configured/verified. Scenario remains not satisfied absent complete storage-isolation evidence. |
| C02 | E-PW-2, E-LOCAL-2 | Playwright documents awaited context close closing its pages and browser close force-quitting; it does not establish for an arbitrary child action that close completion means action execution has stopped. Unknown/blocked. |
| C03 | E-PW-3, E-PW-4 | Playwright docs describe local trace/HAR/auth-state artifacts; they do not establish a hosted cloud upload requirement. Data flow for a proposed deployment is unknown. No private page used. Required rule: Provider needs cloud data upload: disclose data boundary before any private page use. |
| Unknown prerequisite | E-PREREQ-1 | `ci-promotion-gates` design says hosted enforcement needs branch protection plus failing disposable PR proof; not established here. Block dependent work with reason, not success. |

### Evidence rows

```yaml
- claim_id: E-LOCAL-1
  subject: Embedded browser (current checkout)
  claim: BrowserContext is allocated at first navigation and native browser storage is non-persistent; it is shared by NativePages created with that BrowserData. Source calls this a window/profile ephemeral website data context. No mapping from requested work-profile/session to a unique store is present in these spans.
  state: verified
  evidence_kind: local_source
  source_or_command: crates/ui/src/browser/mod.rs:70-75,317-350; crates/ui/src/browser/macos.rs:26-52,291-308
  version_or_commit: current working tree (dirty; commit not asserted)
  observed_at_utc: 2026-09-27
  result_or_excerpt: `BrowserContext` owns native `BrowserData`; `configuration` lazily creates `nonPersistentDataStore`, and `NativePage::new` receives that data and uses `with_incognito(true)`.
  scope: Read-only source inspection only
  limitations: Does not prove platform runtime semantics or per-work-profile isolation. Cache, localStorage and download isolation in this app are not proven by source inspection alone.
  reviewer: research execution
- claim_id: E-LOCAL-2
  subject: BrowserSurface close
  claim: close hides presentation, cancels favicon task and drops native page handle; this does not prove child navigation/action stopped or process exit.
  state: verified
  evidence_kind: local_source
  source_or_command: crates/ui/src/browser/mod.rs:408-435 (close starts at 415; exact body continues in current file)
  version_or_commit: current working tree (dirty; commit not asserted)
  observed_at_utc: 2026-09-27
  result_or_excerpt: close is documented as explicit close despite async callback retaining entity; source drops native handle after hiding it.
  scope: Static local code only
  limitations: No runtime observation, native process/session identifier, or stop acknowledgement.
  reviewer: research execution
- claim_id: E-LOCAL-3
  subject: Browser state and navigation
  claim: PageState tracks URL/title/loading/back-forward/error; address validation permits HTTP/HTTPS and rejects embedded user/password, while localhost is allowed. No provider session ID, signed-in scope grant/revoke, evidence redaction or credential store is represented in this model span.
  state: verified
  evidence_kind: local_source
  source_or_command: crates/ui/src/browser/model.rs:4-12,28-69,99-106
  version_or_commit: current working tree (dirty; commit not asserted)
  observed_at_utc: 2026-09-27
  result_or_excerpt: PageState has navigation state only; normalization checks scheme and embedded credentials.
  scope: Static local code only
  limitations: Absence in these exact model spans is not a claim about all other code; no runtime behavior inferred.
  reviewer: research execution
- claim_id: E-LOCAL-4
  subject: Browser fixture launcher
  claim: The listed fixture script copies a supplied binary into a temporary app bundle, invokes it, then removes the bundle. It is not run and does not itself prove lifecycle, isolation or stop behavior.
  state: verified
  evidence_kind: local_source
  source_or_command: scripts/run-macos-browser-fixture.sh:1-14
  version_or_commit: current working tree (dirty; commit not asserted)
  observed_at_utc: 2026-09-27
  result_or_excerpt: `trap` removes temporary bundle; fixture binary is executed with forwarded args.
  scope: Static launcher inspection only
  limitations: Fixture not authorized/run; runtime behavior unknown.
  reviewer: research execution
- claim_id: E-APPLE-1
  subject: WebKit website data stores (platform documentation)
  claim: WebKit says profiles require separate website data stores; non-persistent stores do not persist to disk, and multiple persistent stores are available on macOS 14/iOS 17. It does not specifically establish this app's cookies/cache/localStorage/download guarantees.
  state: verified
  evidence_kind: official_doc
  source_or_command: https://webkit.org/blog/14423/building-profiles-with-new-webkit-api/; sections “Building Profiles with new WebKit API”, “Create a profile”, “What’s next?”
  version_or_commit: Article dated 2023-08-30; WebKit platform API discussion
  observed_at_utc: 2026-09-27
  result_or_excerpt: “An essential requirement ... separate containers for website data”; non-persistent stores “do not store data to disk”.
  scope: Official WebKit publisher documentation
  limitations: Does not evidence Zeron runtime behavior; per-session download isolation, stop, redaction, network/telemetry and credentials not established.
  reviewer: research execution
- claim_id: E-PW-1
  subject: Playwright BrowserContext isolation
  claim: Playwright says contexts are independent sessions and non-persistent contexts do not write browsing data to disk; browser.newContext does not share cookies/cache with other contexts. Docs also define context storage state cookies and localStorage. Download isolation/per-profile mapping is not established by reviewed pages.
  state: verified
  evidence_kind: official_doc
  source_or_command: https://playwright.dev/docs/browser-contexts (Introduction; What is Test Isolation?); https://playwright.dev/docs/api/class-browsercontext (BrowserContext; storageState); https://playwright.dev/docs/api/class-browser (newContext; options)
  version_or_commit: Current versioned docs page did not state a pinned release in retrieved content
  observed_at_utc: 2026-09-27
  result_or_excerpt: “completely isolated”; newContext “won't share cookies/cache”; storageState documents cookies and localStorage.
  scope: Official Playwright publisher documentation
  limitations: Docs do not by themselves establish download isolation, signed-in authority policy, app integration or redaction.
  reviewer: research execution
- claim_id: E-PW-2
  subject: Playwright context and browser close
  claim: BrowserContext.close closes its pages and returns a Promise; Browser.close on launched browser closes browser and pages and is described as similar to force-quitting. Docs do not promise arbitrary child tool action completion when close returns.
  state: verified
  evidence_kind: official_doc
  source_or_command: https://playwright.dev/docs/api/class-browsercontext (close); https://playwright.dev/docs/api/class-browser (close)
  version_or_commit: Current versioned docs page did not state a pinned release in retrieved content
  observed_at_utc: 2026-09-27
  result_or_excerpt: Context close “All the pages ... will be closed”; browser close described as “force-quitting”.
  scope: Official Playwright publisher documentation
  limitations: Does not prove an adapter has observed stop or that an external/child action has terminated.
  reviewer: research execution
- claim_id: E-PW-3
  subject: Playwright trace evidence
  claim: Playwright tracing can capture browser operations/network activity and optional screenshots/DOM snapshots, writing traces to a local file. Docs do not document redaction guarantees.
  state: verified
  evidence_kind: official_doc
  source_or_command: https://playwright.dev/docs/api/class-tracing (overview; start; stop)
  version_or_commit: Current versioned docs page did not state a pinned release in retrieved content
  observed_at_utc: 2026-09-27
  result_or_excerpt: Tracing “captures browser operations and network activity”; stop exports trace to a file.
  scope: Official Playwright publisher documentation
  limitations: Captured network/DOM data may be sensitive; no redaction guarantee or cloud-flow statement found in reviewed docs.
  reviewer: research execution
- claim_id: E-PW-4
  subject: Playwright authentication and artifacts
  claim: Playwright recommends storing authentication state on filesystem and warns it may contain impersonation-capable sensitive cookies/headers; trace/HAR artifacts are filesystem outputs. Docs do not specify an external service upload in this mode.
  state: verified
  evidence_kind: official_doc
  source_or_command: https://playwright.dev/docs/auth (Core concepts); https://playwright.dev/docs/api/class-tracing (stop/startHar)
  version_or_commit: Current versioned docs page did not state a pinned release in retrieved content
  observed_at_utc: 2026-09-27
  result_or_excerpt: Auth state may contain “sensitive cookies and headers”; tracing/HAR methods write to filesystem paths.
  scope: Official Playwright publisher documentation
  limitations: No secret manager/credential-at-rest guarantee, explicit work scope grant/revoke, hosted deployment data flow, telemetry behavior, or cloud requirement established.
  reviewer: research execution
- claim_id: E-PREREQ-1
  subject: ci-promotion-gates prerequisite
  claim: Hosted enforcement requires configured branch protection and failing disposable PR proof; this is not established by this research task.
  state: blocked
  evidence_kind: local_source
  source_or_command: openspec/changes/ci-promotion-gates/design.md:13-15,26-27
  version_or_commit: Current working tree
  observed_at_utc: 2026-09-27
  result_or_excerpt: Design states hosted enforcement is blocked absent admin-configured branch protection and failing disposable PR proof.
  scope: Planning prerequisite status only
  limitations: No hosted settings or PR workflow was accessed.
  reviewer: research execution
```

### Scenario outcomes

```yaml
- scenario_id: C01
  state: blocked
  evidence_refs: [E-LOCAL-1, E-APPLE-1, E-PW-1]
  reason: Screenshots do not establish storage isolation. Playwright documents context separation, but reviewed docs do not settle download isolation or requested work-profile mapping; existing source uses a window-level BrowserData and no runtime probe was authorized.
  remaining_question: Can a reviewed integration guarantee cookies, cache, localStorage and downloads isolated per authorized work session?
- scenario_id: C02
  state: unknown
  evidence_refs: [E-LOCAL-2, E-PW-2]
  reason: Close/hide/drop and documented context close are not proof that a child tool action has stopped.
  remaining_question: What observable action/process/session-specific completion signal proves all child work has terminated?
- scenario_id: C03
  state: unknown
  evidence_refs: [E-PW-3, E-PW-4]
  reason: Reviewed docs describe local artifacts but do not establish a proposed deployment's cloud/network/telemetry boundary. No private page used.
  remaining_question: Would selected deployment upload page content, credentials, traces or telemetry, and under what controls?
- scenario_id: unknown-prerequisite
  state: blocked
  evidence_refs: [E-PREREQ-1]
  reason: Hosted prerequisite evidence is absent; do not report readiness or success.
  remaining_question: Obtain the separately authorized hosted prerequisite proof before dependent promotion.
```

Required acceptance rules retained verbatim: “Provider supports screenshots but cannot isolate storage: does not satisfy session isolation.” “Provider close command returns before tool action stops: cancellation remains unverified.” “Provider needs cloud data upload: disclose data boundary before any private page use.”

### Provisional child adapter record

```yaml
adapter_id: playwright-docs-only
system_identity: Playwright browser automation framework; documentation subject only, not selected provider
supported_versions: unknown (reviewed docs did not pin a release)
capability: documented isolated browser contexts; no integration capability established
owner_boundary: unknown; no product adapter owner selected
inputs_and_scope: unknown; explicit signed-in work-scope grant/revoke not established
outputs_and_states: pages, context/browser closure and optional trace/HAR artifacts documented; adapter output contract unknown
native_id: unknown; browser/context objects documented, durable OS process/session identity contract not established
start_proof: unknown for proposed adapter; docs show launch/newContext APIs, not acceptance proof
stop_proof: context/browser close promises documented; child action termination proof unknown
status_proof: unknown
configuration_source: unknown
auth_boundary: filesystem storageState can contain impersonation-capable cookies/headers; secure storage and approval boundary unknown
data_boundary: docs describe local trace/HAR output; cloud upload, network/telemetry and deployment flow unknown
isolation_boundary: contexts documented as independent and not sharing cookies/cache; localStorage documented via storageState; per-session downloads not established
read_only_operations: unknown; no live operations authorized
write_operations: not authorized
failure_and_retry_behavior: unknown
compatibility: browser engines Chromium/Firefox/WebKit are named in docs; compatible app/runtime versions unknown
evidence_refs: [E-PW-1, E-PW-2, E-PW-3, E-PW-4]
rejection_reasons: [version unpinned, work-profile mapping unknown, download isolation unknown, stop of child actions unproven, explicit scope grant/revoke unknown, redaction unknown, deployed data flow unknown]
decision_state: blocked
```

This record is documentation research, not provider selection, API freeze, implementation readiness, or proof all future adapters are implementable.
