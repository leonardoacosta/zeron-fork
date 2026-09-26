# Profile-configurable routine briefings: design boundary

## Read first
`../../../docs/fork-prd.md`, `../prd-execution-map/design.md`, this proposal/spec, and the prerequisite changes `exception-attention`, `workflow-version-selection`. Baseline `1427da6`; all source lines must be refreshed after prerequisite changes. Paths below are existing anchors, not permission to edit every file.

## Existing surfaces and file responsibilities
- `crates/ui/src/settings/notifications.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/ui/src/notify.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/sync/src/store.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/engine/src/rpc.rs`: existing source/test/config anchor; inspect its graph card before source.

## Integration contract to freeze before implementation
- Input: explicit actor/work-profile, operation identity, relevant immutable version bindings and requested scope; validate at owning engine boundary, not merely UI.
- Output: typed observed result with version/owner, unsupported/denied/uncertain states distinguished; no fake success.
- Side effects: enumerate each process/file/database/network effect in refinement, including retries and failure between persistence and acknowledgment.
- Ownership: reuse current Rust engine + typed RPC + profile SQLite where appropriate; registry LWW is not authoritative revision history. Reuse existing mechanisms before adding new module/dependency.
- Interface freeze: discovery must record exact existing symbols and proposed DTO/state transitions, error payloads, capability identifier, migration/version compatibility and callers/tests. No names in this paragraph create a runtime API.

## Required behavior
Provide morning/routine briefing schedule and destinations per profile with explicit configuration. Summarize progress, blockers, uncertainty and accepted/delivered/outcome states distinctly. Delivery provider/channel selection must be recorded before adapter implementation. Missed schedule, timezone/DST and duplicate delivery are explicit policies; no guessed universal morning time.

## Misinterpretations to reject in review
- Do not schedule unsolicited messages by default.
- No alert text implies authority to resume.
- Do not leak one profile into another briefing.

## Failure and compatibility scenarios
- C01: Clock crosses DST or device was offline: apply configured missed-run policy once, not duplicate delivery.
- C02: Destination revoked: retain failed-delivery state without sending to a fallback account.
- C03: Briefing reports agent-finished but unverified output as unverified.
- C04: Routine progress stays activity while urgent exception still alerts immediately.

## Rollout / rollback
Disable schedules before rollback, preserve delivery identity/history and user configuration. No replay of past messages without explicit policy.

## Acceptance boundary
Deterministic clock/scheduler tests plus actual authorized local notification destination; external email/chat destination separately authorized.
Structural inspection and provider doubles may support but cannot replace this boundary. External/native prerequisites unavailable means blocked, not complete. User has authorized local homelab/Mac work previously; that does not authorize unrelated Brown/cloud/provider mutations or spend.

## Implementation readiness
This is a bounded behavior contract, not code-complete implementation instructions. A `feature` refinement must replace discovery tasks with exact 2–5 minute test/red/minimal-code/green/commit steps, complete code blocks and actual symbol names, then pass review. Newly created paths must be explicitly listed there. If provider/UI/product judgment remains genuinely unresolved, retain blocked status and ask that one question rather than choose silently.
