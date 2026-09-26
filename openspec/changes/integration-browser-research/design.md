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
