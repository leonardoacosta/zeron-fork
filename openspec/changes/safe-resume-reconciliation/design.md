# Recovery with continuing authority and effect reconciliation: design boundary

## Read first
`../../../docs/fork-prd.md`, `../prd-execution-map/design.md`, this proposal/spec, and the prerequisite changes `confirmed-stop-handoff`, `run-resource-ledger`. Baseline `1427da6`; all source lines must be refreshed after prerequisite changes. Paths below are existing anchors, not permission to edit every file.

## Existing surfaces and file responsibilities
- `crates/engine/src/run_journal.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/engine/src/sessions.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/engine/src/lib.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/engine/tests/restart_resume.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/engine/tests/session_publication.rs`: existing source/test/config anchor; inspect its graph card before source.

## Integration contract to freeze before implementation
- Input: explicit actor/work-profile, operation identity, relevant immutable version bindings and requested scope; validate at owning engine boundary, not merely UI.
- Output: typed observed result with version/owner, unsupported/denied/uncertain states distinguished; no fake success.
- Side effects: enumerate each process/file/database/network effect in refinement, including retries and failure between persistence and acknowledgment.
- Ownership: reuse current Rust engine + typed RPC + profile SQLite where appropriate; registry LWW is not authoritative revision history. Reuse existing mechanisms before adding new module/dependency.
- Interface freeze: discovery must record exact existing symbols and proposed DTO/state transitions, error payloads, capability identifier, migration/version compatibility and callers/tests. No names in this paragraph create a runtime API.

## Required behavior
On crash/reconnect reconstruct frozen configuration, authorization, native session identity and effect uncertainty. Resume only a known-safe still-authorized continuation. Unknown external effects hold for Leo with evidence and reconciliation options. Keep interrupted, stopped, failed and outcome-confirmed distinct. Direct-session recovery must obey the same boundary.

## Legacy startup admission prerequisite
Planning decision only; implementation remains NOT READY. Freeze this compatibility disposition before implementation admission, including the boot path rather than only an owner RPC:
- Verified 2026-09-30: `assemble_with_profile_locked` invokes `sessions.recover_stale()` at `crates/engine/src/lib.rs:246-253`. The owning recovery check belongs in `recover_stale` (`crates/engine/src/sessions.rs:687-812`), before the retry counter and revival scheduling at `756-759`. Its current admission at `734` is `fresh && prompt.is_some() && attempts < MAX_AUTO_RESUME`, not the proposed frozen-binding/policy admission.
- Require recovered frozen configuration/authorization/native identity bindings, current policy permission and reconciled effect safety before admitting boot continuation. Freshness, retry count, transcript deduplication and remembered session identity alone are insufficient. Legacy journals missing these facts must hold with evidence and reconciliation options, retain recoverable journal/transcript data, and issue zero harness dispatches or external mutation resends. This is a future requirement, not a claim about all downstream guards today.
- The current revival request chain uses `last_request`, `request_from_chat_row`, then journal cwd with default fields (`crates/engine/src/sessions.rs:763-782`), followed by `dispatch_with_source_context` (`788-800`). None may silently reconstruct authority from missing bindings or substitute current/default configuration. Missing evidence must hold before scheduling or consuming a resume attempt/launch, including after a second restart. Exact persisted admission evidence and transition/error representation remain D2 decisions; this paragraph creates no API or new state name.
- Explicit test disposition: split or revise `fresh_crash_auto_resumes_and_notes_the_interruption` (`crates/engine/tests/restart_resume.rs:569-693`), not delete it casually. Its fresh transcript plus `SessionStarted`/`TextDelta` journal (`569-637`) does not establish the required frozen binding/policy/effect facts, yet it currently expects automatic completion, a resuming note, no duplicate user message and remembered native-session reuse (`640-691`). Under the proposed compatibility rule, that insufficient-evidence fixture must instead hold with zero harness dispatch, preserve the interrupted transcript/journal and avoid falsely announcing a resume. A separate positively bound, still-authorized and reconciled fixture may retain automatic continuation with the existing deduplication, visible interruption and native-identity assertions. The held legacy fixture must remain held after a second restart without consuming a launch/resume attempt or substituting defaults. These are proposed acceptance assertions, not executed tests; retain C02 revocation and C04 native-unavailability coverage separately.

## Misinterpretations to reject in review
- Command deduplication is not exactly-once delivery.
- A stale-session flag is not resume authorization.
- Do not reset evidence/usage on restart.

## Failure and compatibility scenarios
- C01: Crash after dispatch but before receipt: no blind resend of an external mutation.
- C02: Profile permission revoked while owner is down: restart cannot auto-resume old authority.
- C03: Journal has torn final entry: recover known prefix and mark missing effects uncertain.
- C04: Native session unavailable: do not substitute a new account/environment or claim continuation.

## Rollout / rollback
Keep original journal immutable or backed up; new recovery metadata additive. If reader cannot understand uncertainty state, fail closed and retain data.

## Acceptance boundary
C04 additionally needs an authorized native restart with the previously bound session unavailable: verify held/uncertain status, typed unavailability reason, exact account/environment binding retained, no substitute session/account launch or external effect, and same held result after a second restart until explicit reconciliation. Keep that distinct from the revoked-policy restart case. Crash-boundary subprocess tests and authorized native restart with revoked-policy negative case prove no external side effect replay. Structural inspection and provider doubles may support but cannot replace this boundary. External/native prerequisites unavailable means blocked, not complete. User has authorized local homelab/Mac work previously; that does not authorize unrelated Brown/cloud/provider mutations or spend.

## Implementation readiness
This is a bounded behavior contract, not code-complete implementation instructions. A `feature` refinement must replace discovery tasks with exact 2–5 minute test/red/minimal-code/green/commit steps, complete code blocks and actual symbol names, then pass review. Newly created paths must be explicitly listed there. If provider/UI/product judgment remains genuinely unresolved, retain blocked status and ask that one question rather than choose silently.
