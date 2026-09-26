# Conflict admission for assignments and direct sessions: design boundary

## Read first
`../../../docs/fork-prd.md`, `../prd-execution-map/design.md`, this proposal/spec, and the prerequisite changes `manual-investigation-runner`, `revision-evidence-bindings`. Baseline `1427da6`; all source lines must be refreshed after prerequisite changes. Paths below are existing anchors, not permission to edit every file.

## Existing surfaces and file responsibilities
- `crates/engine/src/sessions.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/engine/src/rpc.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/engine/src/repos.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/proto/src/assignment.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/sync/src/store.rs`: existing source/test/config anchor; inspect its graph card before source.

## Integration contract to freeze before implementation
- Input: explicit actor/work-profile, operation identity, relevant immutable version bindings and requested scope; validate at owning engine boundary, not merely UI.
- Output: typed observed result with version/owner, unsupported/denied/uncertain states distinguished; no fake success.
- Side effects: enumerate each process/file/database/network effect in refinement, including retries and failure between persistence and acknowledgment.
- Ownership: reuse current Rust engine + typed RPC + profile SQLite where appropriate; registry LWW is not authoritative revision history. Reuse existing mechanisms before adding new module/dependency.
- Interface freeze: discovery must record exact existing symbols and proposed DTO/state transitions, error payloads, capability identifier, migration/version compatibility and callers/tests. No names in this paragraph create a runtime API.

## Required behavior
At proposal admission inspect overlapping changes, incompatible assumptions, shared resources and unmet dependencies. Include direct sessions without converting them into assignments. Represent limited outside-Zeron visibility. Different files can conflict; independent work proceeds. Recheck scope changes and shared-action boundaries. Uncertain conflicts require another reviewer; unresolved uncertainty holds affected work and alerts. System One is observer, not execution authority; unverified adapter can only return unknown.

## Misinterpretations to reject in review
- No filename-only lock as complete conflict analysis.
- No observer grant of permissions or priority changes.
- Do not fabricate SystemOne API or replace engineering harness with it.

## Failure and compatibility scenarios
- C01: Disjoint files share one database migration invariant: identify conflict or uncertainty, not automatic independence.
- C02: Two proposals race admission: no overlapping exclusive lease granted twice.
- C03: One uncertain conflict holds only affected work, not all queues.
- C04: Reviewer unavailable or external work invisible: expose unknown and hold affected scope.

## Rollout / rollback
Admission records/leases durable; downgrade stops new overlapping launches, preserves already-running ownership and uncertainty.

## Acceptance boundary
Concurrent direct-session plus assignment admission with resource conflicts, unknown observer and changed-scope checks; provider-specific SystemOne evidence separately required.
Structural inspection and provider doubles may support but cannot replace this boundary. External/native prerequisites unavailable means blocked, not complete. User has authorized local homelab/Mac work previously; that does not authorize unrelated Brown/cloud/provider mutations or spend.

## Implementation readiness
This is a bounded behavior contract, not code-complete implementation instructions. A `feature` refinement must replace discovery tasks with exact 2–5 minute test/red/minimal-code/green/commit steps, complete code blocks and actual symbol names, then pass review. Newly created paths must be explicitly listed there. If provider/UI/product judgment remains genuinely unresolved, retain blocked status and ask that one question rather than choose silently.
