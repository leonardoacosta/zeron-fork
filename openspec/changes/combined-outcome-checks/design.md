# Parent outcome verification over delivered versions: design boundary

## Read first
`../../../docs/fork-prd.md`, `../prd-execution-map/design.md`, this proposal/spec, and the prerequisite changes `multi-repository-breakdown`, `git-delivery-actions`, `release-deploy-publish-actions`. Baseline `1427da6`; all source lines must be refreshed after prerequisite changes. Paths below are existing anchors, not permission to edit every file.

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
Parent workflow evaluates combined checks across exact required child output and delivered versions before objective completion. Finished children are insufficient. Partial delivery visible; failed child blocks dependents only. Configured human/autonomous outcome gates apply. Superseded child outputs cannot silently count.

## Misinterpretations to reject in review
- No completion percentage as proof of combined correctness.
- No replacing failed child output with previous version silently.
- No universal simultaneous release gate.

## Failure and compatibility scenarios
- C01: All child tasks done but integration endpoint fails: parent outcome remains unconfirmed.
- C02: One child delivered old accepted revision while another expects new API: combined check fails with exact mismatch.
- C03: Optional independent child failure does not automatically stop unrelated required work; requiredness is explicit.
- C04: Partial deployment survives restart and remains visible with reconciliation options.

## Rollout / rollback
Persist combined-check input set and observations immutably; rollback withdraws unsupported completion claims but preserves delivery facts.

## Acceptance boundary
Real two-repository local consumer/provider compatibility check including stale delivered version and partial failure.
Structural inspection and provider doubles may support but cannot replace this boundary. External/native prerequisites unavailable means blocked, not complete. User has authorized local homelab/Mac work previously; that does not authorize unrelated Brown/cloud/provider mutations or spend.

## Implementation readiness
This is a bounded behavior contract, not code-complete implementation instructions. A `feature` refinement must replace discovery tasks with exact 2–5 minute test/red/minimal-code/green/commit steps, complete code blocks and actual symbol names, then pass review. Newly created paths must be explicitly listed there. If provider/UI/product judgment remains genuinely unresolved, retain blocked status and ask that one question rather than choose silently.
