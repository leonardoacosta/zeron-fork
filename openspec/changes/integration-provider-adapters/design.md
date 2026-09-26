# Verified provider adapters and authority preservation: design boundary

## Read first
`../../../docs/fork-prd.md`, `../prd-execution-map/design.md`, this proposal/spec, and the prerequisite changes `integration-harness-observer-research`, `integration-github-ado-research`, `profile-access-enforcement`, `harness-preflight-binding`, `confirmed-stop-handoff`. Baseline `1427da6`; all source lines must be refreshed after prerequisite changes. Paths below are existing anchors, not permission to edit every file.

## Existing surfaces and file responsibilities
- `crates/harness/src/lib.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/engine/src/registry.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/mcp/src/tools.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/engine/src/source_control.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/engine/src/rpc.rs`: existing source/test/config anchor; inspect its graph card before source.

## Integration contract to freeze before implementation
- Input: explicit actor/work-profile, operation identity, relevant immutable version bindings and requested scope; validate at owning engine boundary, not merely UI.
- Output: typed observed result with version/owner, unsupported/denied/uncertain states distinguished; no fake success.
- Side effects: enumerate each process/file/database/network effect in refinement, including retries and failure between persistence and acknowledgment.
- Ownership: reuse current Rust engine + typed RPC + profile SQLite where appropriate; registry LWW is not authoritative revision history. Reuse existing mechanisms before adding new module/dependency.
- Interface freeze: discovery must record exact existing symbols and proposed DTO/state transitions, error payloads, capability identifier, migration/version compatibility and callers/tests. No names in this paragraph create a runtime API.

## Required behavior
Instantiate one child adapter change per researched concrete provider and action set before implementation. Each child freezes documented API/version, maps native identity/status/stop/effect semantics, honors profile and external authority, and has real authorized acceptance. This boundary is a fan-out contract, not permission to implement all adapters in one patch. MCP exposure must reuse engine authorization, not bypass it.

## Misinterpretations to reject in review
- One mega-adapter is not a bounded change.
- Do not invent start/stop methods absent research proof.
- Integration availability does not authorize mutations.

## Failure and compatibility scenarios
- C01: Adapter returns unsupported for missing stop/isolation instead of claiming a generic interface makes it safe.
- C02: External planning/review status changes: preserve source provenance and never overwrite from local completion.
- C03: Provider upgrade changes contract: capability evidence invalidated and affected launches held.

## Rollout / rollback
Per-provider disable switch and native state/effect reconciliation before removal. Preserve other adapters and direct sessions.

## Acceptance boundary
One real harmless authorized workflow per selected adapter and failure/unknown capability checks. Unselected providers remain blocked, not marked complete.
Structural inspection and provider doubles may support but cannot replace this boundary. External/native prerequisites unavailable means blocked, not complete. User has authorized local homelab/Mac work previously; that does not authorize unrelated Brown/cloud/provider mutations or spend.

## Implementation readiness
This is a bounded behavior contract, not code-complete implementation instructions. A `feature` refinement must replace discovery tasks with exact 2–5 minute test/red/minimal-code/green/commit steps, complete code blocks and actual symbol names, then pass review. Newly created paths must be explicitly listed there. If provider/UI/product judgment remains genuinely unresolved, retain blocked status and ask that one question rather than choose silently.
