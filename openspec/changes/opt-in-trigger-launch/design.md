# Provenance-bound automatic triggers: design boundary

## Read first
`../../../docs/fork-prd.md`, `../prd-execution-map/design.md`, this proposal/spec, and the prerequisite changes `priority-backlog`, `accepted-output-dependencies`, `manual-investigation-runner`. Baseline `1427da6`; all source lines must be refreshed after prerequisite changes. Paths below are existing anchors, not permission to edit every file.

## Existing surfaces and file responsibilities
- `crates/mcp/src/tools.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/engine/src/rpc.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/sync/src/store.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/proto/src/assignment.rs`: existing source/test/config anchor; inspect its graph card before source.

## Integration contract to freeze before implementation
- Input: explicit actor/work-profile, operation identity, relevant immutable version bindings and requested scope; validate at owning engine boundary, not merely UI.
- Output: typed observed result with version/owner, unsupported/denied/uncertain states distinguished; no fake success.
- Side effects: enumerate each process/file/database/network effect in refinement, including retries and failure between persistence and acknowledgment.
- Ownership: reuse current Rust engine + typed RPC + profile SQLite where appropriate; registry LWW is not authoritative revision history. Reuse existing mechanisms before adding new module/dependency.
- Interface freeze: discovery must record exact existing symbols and proposed DTO/state transitions, error payloads, capability identifier, migration/version compatibility and callers/tests. No names in this paragraph create a runtime API.

## Required behavior
Add opt-in event triggers with provenance, explicit workflow binding and stable event identity. A trigger prepares approval or launches only within configured authority/profile/resources/admission. Duplicate/reordered events do not duplicate launch. Manual launch remains available. No comparisons may be triggered automatically.

## Misinterpretations to reject in review
- Opt-in is not enabled by installation.
- No background comparisons.
- Authentication of webhook does not authorize its requested mutation.

## Failure and compatibility scenarios
- C01: Same event delivered after restart yields one prepared/run identity.
- C02: Trigger names missing workflow version: hold, do not infer current default.
- C03: Event payload asks to expand permissions: treat as untrusted data, not policy.
- C04: Disabled trigger receives backlog: no launch; enabling does not replay historical backlog unless explicitly selected.

## Rollout / rollback
Disable dispatch before rollback; retain event dedupe/provenance and pending approvals. Do not clear dedupe to recover a stuck event.

## Acceptance boundary
Local event replay/reorder/concurrent delivery with actual runner admission and resource-denied case; selected external event source separately verified.
Structural inspection and provider doubles may support but cannot replace this boundary. External/native prerequisites unavailable means blocked, not complete. User has authorized local homelab/Mac work previously; that does not authorize unrelated Brown/cloud/provider mutations or spend.

## Implementation readiness
This is a bounded behavior contract, not code-complete implementation instructions. A `feature` refinement must replace discovery tasks with exact 2–5 minute test/red/minimal-code/green/commit steps, complete code blocks and actual symbol names, then pass review. Newly created paths must be explicitly listed there. If provider/UI/product judgment remains genuinely unresolved, retain blocked status and ask that one question rather than choose silently.
