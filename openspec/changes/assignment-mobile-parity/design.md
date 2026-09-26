# Mobile compatible assignment control/read surface: design boundary

## Read first
`../../../docs/fork-prd.md`, `../prd-execution-map/design.md`, this proposal/spec, and the prerequisite changes `assignment-desktop-surface`. Baseline `1427da6`; all source lines must be refreshed after prerequisite changes. Paths below are existing anchors, not permission to edit every file.

## Existing surfaces and file responsibilities
- `apps/ios/Zeron/Sync/DeviceRelayClient.swift`: existing source/test/config anchor; inspect its graph card before source.
- `apps/ios/Zeron/Sync/WorkspaceStore.swift`: existing source/test/config anchor; inspect its graph card before source.
- `apps/ios/Zeron/Views/SessionView.swift`: existing source/test/config anchor; inspect its graph card before source.
- `apps/ios/ZeronTests/DeviceRelayClientTests.swift`: existing source/test/config anchor; inspect its graph card before source.
- `crates/proto/src/assignment.rs`: existing source/test/config anchor; inspect its graph card before source.

## Integration contract to freeze before implementation
- Input: explicit actor/work-profile, operation identity, relevant immutable version bindings and requested scope; validate at owning engine boundary, not merely UI.
- Output: typed observed result with version/owner, unsupported/denied/uncertain states distinguished; no fake success.
- Side effects: enumerate each process/file/database/network effect in refinement, including retries and failure between persistence and acknowledgment.
- Ownership: reuse current Rust engine + typed RPC + profile SQLite where appropriate; registry LWW is not authoritative revision history. Reuse existing mechanisms before adding new module/dependency.
- Interface freeze: discovery must record exact existing symbols and proposed DTO/state transitions, error payloads, capability identifier, migration/version compatibility and callers/tests. No names in this paragraph create a runtime API.

## Required behavior
Add reviewed mobile parity for the accepted desktop assignment contract, with explicit capability negotiation and owner routing. Preserve direct sessions and display profile/workflow/evidence/stop state correctly. Mobile reconnect must not repeat launches or delivery. Define supported controls explicitly in design rather than silently treating unsupported controls as success.

## Misinterpretations to reject in review
- Do not reuse registry LWW as authoritative assignment history.
- Do not claim physical-device acceptance from Swift decoding tests only.

## Failure and compatibility scenarios
- C01: Old owner lacks assignment capability: ordinary session still works, assignment operation reports unsupported.
- C02: Phone loses connection after launch request: reconcile run identity, no duplicate launch.
- C03: Stale phone view submits old revision: conflict and refresh, no overwrite.
- C04: Stop receipt remains stopping until owner confirms cessation.

## Rollout / rollback
Additive decoding and capability flags; retain previous compatible read path. No forced desktop data migration for mobile layout.

## Acceptance boundary
Existing iOS unit CI plus authorized simulator/device-to-owner workflow and disconnected/stale-revision checks.
Structural inspection and provider doubles may support but cannot replace this boundary. External/native prerequisites unavailable means blocked, not complete. User has authorized local homelab/Mac work previously; that does not authorize unrelated Brown/cloud/provider mutations or spend.

## Implementation readiness
This is a bounded behavior contract, not code-complete implementation instructions. A `feature` refinement must replace discovery tasks with exact 2–5 minute test/red/minimal-code/green/commit steps, complete code blocks and actual symbol names, then pass review. Newly created paths must be explicitly listed there. If provider/UI/product judgment remains genuinely unresolved, retain blocked status and ask that one question rather than choose silently.
