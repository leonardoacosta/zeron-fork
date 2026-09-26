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
Crash-boundary subprocess tests and authorized native restart with revoked-policy negative case; no external side effect replay.
Structural inspection and provider doubles may support but cannot replace this boundary. External/native prerequisites unavailable means blocked, not complete. User has authorized local homelab/Mac work previously; that does not authorize unrelated Brown/cloud/provider mutations or spend.

## Implementation readiness
This is a bounded behavior contract, not code-complete implementation instructions. A `feature` refinement must replace discovery tasks with exact 2–5 minute test/red/minimal-code/green/commit steps, complete code blocks and actual symbol names, then pass review. Newly created paths must be explicitly listed there. If provider/UI/product judgment remains genuinely unresolved, retain blocked status and ask that one question rather than choose silently.
