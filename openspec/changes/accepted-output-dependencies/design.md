# Exact-version output dependencies: design boundary

## Read first
`../../../docs/fork-prd.md`, `../prd-execution-map/design.md`, this proposal/spec, and the prerequisite changes `verification-acceptance-gates`, `conflict-admission-observer`. Baseline `1427da6`; all source lines must be refreshed after prerequisite changes. Paths below are existing anchors, not permission to edit every file.

## Existing surfaces and file responsibilities
- `crates/proto/src/assignment.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/sync/src/store.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/engine/src/rpc.rs`: existing source/test/config anchor; inspect its graph card before source.

## Integration contract to freeze before implementation
- Input: explicit actor/work-profile, operation identity, relevant immutable version bindings and requested scope; validate at owning engine boundary, not merely UI.
- Output: typed observed result with version/owner, unsupported/denied/uncertain states distinguished; no fake success.
- Side effects: enumerate each process/file/database/network effect in refinement, including retries and failure between persistence and acknowledgment.
- Ownership: reuse current Rust engine + typed RPC + profile SQLite where appropriate; registry LWW is not authoritative revision history. Reuse existing mechanisms before adding new module/dependency.
- Interface freeze: discovery must record exact existing symbols and proposed DTO/state transitions, error payloads, capability identifier, migration/version compatibility and callers/tests. No names in this paragraph create a runtime API.

## Required behavior
Bind dependency edges to accepted stage-output versions, not just whole assignment completion. Reject cycles and foreign-profile edges. Allow independent work to overlap. Upstream replacement/revocation triggers downstream reassessment before next dependent action; prior execution effects are preserved and never retroactively called safe.

## Misinterpretations to reject in review
- Do not bind a mutable latest pointer.
- Do not block every child until whole parent finishes.
- Reassessment is not automatic rollback of external effects.

## Failure and compatibility scenarios
- C01: Investigation output accepted while parent assignment not done: authorized dependent stage may start.
- C02: Upstream new revision cannot silently substitute into already-bound downstream run.
- C03: Cycle or self-edge rejected atomically, no partial graph change.
- C04: Accepted evidence later contradicted: affected downstream waits/reconciles, independent branch continues.

## Rollout / rollback
Keep immutable edge/output revisions and append invalidations. Downgrade blocks unknown graph semantics, not deleting edges.

## Acceptance boundary
Graph transaction/restart tests and real two-stage workflow proving exact-version binding and invalidation.
Structural inspection and provider doubles may support but cannot replace this boundary. External/native prerequisites unavailable means blocked, not complete. User has authorized local homelab/Mac work previously; that does not authorize unrelated Brown/cloud/provider mutations or spend.

## Implementation readiness
This is a bounded behavior contract, not code-complete implementation instructions. A `feature` refinement must replace discovery tasks with exact 2–5 minute test/red/minimal-code/green/commit steps, complete code blocks and actual symbol names, then pass review. Newly created paths must be explicitly listed there. If provider/UI/product judgment remains genuinely unresolved, retain blocked status and ask that one question rather than choose silently.
