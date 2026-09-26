# Confirmed stopping and explicit human handoff: design boundary

## Read first
`../../../docs/fork-prd.md`, `../prd-execution-map/design.md`, this proposal/spec, and the prerequisite changes `profile-access-enforcement`, `harness-preflight-binding`. Baseline `1427da6`; all source lines must be refreshed after prerequisite changes. Paths below are existing anchors, not permission to edit every file.

## Existing surfaces and file responsibilities
- `crates/engine/src/sessions.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/harness/src/lib.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/engine/src/terminals.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/engine/src/rpc.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/engine/tests/turn_quiesce.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/engine/tests/self_continued_quiesce.rs`: existing source/test/config anchor; inspect its graph card before source.

## Integration contract to freeze before implementation
- Input: explicit actor/work-profile, operation identity, relevant immutable version bindings and requested scope; validate at owning engine boundary, not merely UI.
- Output: typed observed result with version/owner, unsupported/denied/uncertain states distinguished; no fake success.
- Side effects: enumerate each process/file/database/network effect in refinement, including retries and failure between persistence and acknowledgment.
- Ownership: reuse current Rust engine + typed RPC + profile SQLite where appropriate; registry LWW is not authoritative revision history. Reuse existing mechanisms before adding new module/dependency.
- Interface freeze: discovery must record exact existing symbols and proposed DTO/state transitions, error payloads, capability identifier, migration/version compatibility and callers/tests. No names in this paragraph create a runtime API.

## Required behavior
Define pause-requested, stopping, stopped-confirmed, human-owned, handback-requested and resumable states with guarded transitions. Stop receipts are observations, not proof. Track native process/session and descendant/tool activity for supported harnesses. Hand takeover only after stop proof; unknown remote/process status remains held. Human handback is explicit and revalidates authority/configuration.

## Misinterpretations to reject in review
- Do not equate stream closure, UI spinner ending or cancellation token delivery with stopped.
- Do not kill unrelated sessions to simplify cancellation.
- Priority never authorizes interruption.

## Failure and compatibility scenarios
- C01: Cancel RPC acknowledges while a spawned child continues writing: status stays stopping and takeover is refused.
- C02: Network disappears during stop: mark uncertain, block conflicting work, keep unrelated isolated work running.
- C03: Repeated pause/handback commands are idempotent without duplicate launches.
- C04: A stale handback for an older run generation cannot resume the replacement run.

## Rollout / rollback
Persist lifecycle transition before acknowledgment. Downgrade active/uncertain work to hold; no replay of unconfirmed external effects.

## Acceptance boundary
Real harmless subprocess with descendant writes proves last write/exit boundary; native harness-specific stopping requires its own evidence.
Structural inspection and provider doubles may support but cannot replace this boundary. External/native prerequisites unavailable means blocked, not complete. User has authorized local homelab/Mac work previously; that does not authorize unrelated Brown/cloud/provider mutations or spend.

## Implementation readiness
This is a bounded behavior contract, not code-complete implementation instructions. A `feature` refinement must replace discovery tasks with exact 2–5 minute test/red/minimal-code/green/commit steps, complete code blocks and actual symbol names, then pass review. Newly created paths must be explicitly listed there. If provider/UI/product judgment remains genuinely unresolved, retain blocked status and ask that one question rather than choose silently.
