# Priority, blockers and non-preemptive urgent work: design boundary

## Read first
`../../../docs/fork-prd.md`, `../prd-execution-map/design.md`, this proposal/spec, and the prerequisite changes `conflict-admission-observer`, `confirmed-stop-handoff`. Baseline `1427da6`; all source lines must be refreshed after prerequisite changes. Paths below are existing anchors, not permission to edit every file.

## Existing surfaces and file responsibilities
- `crates/engine/src/rpc.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/engine/src/sessions.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/sync/src/store.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/proto/src/assignment.rs`: existing source/test/config anchor; inspect its graph card before source.

## Integration contract to freeze before implementation
- Input: explicit actor/work-profile, operation identity, relevant immutable version bindings and requested scope; validate at owning engine boundary, not merely UI.
- Output: typed observed result with version/owner, unsupported/denied/uncertain states distinguished; no fake success.
- Side effects: enumerate each process/file/database/network effect in refinement, including retries and failure between persistence and acknowledgment.
- Ownership: reuse current Rust engine + typed RPC + profile SQLite where appropriate; registry LWW is not authoritative revision history. Reuse existing mechanisms before adding new module/dependency.
- Interface freeze: discovery must record exact existing symbols and proposed DTO/state transitions, error payloads, capability identifier, migration/version compatibility and callers/tests. No names in this paragraph create a runtime API.

## Required behavior
Queue conflicted proposals with blocker type/reason and explicit priority. Among eligible work sort priority then oldest admission; Leo override recorded. Observer recommendations never silently change priority. Reassess on blocker resolution. Urgent conflicting work waits unless Leo explicitly requests interruption and actual stop is confirmed. Dependency-wait and conflict-wait are different states.

## Misinterpretations to reject in review
- No automatic preemption because number is high.
- No global serialization of independent work.
- No changing priority based on model enthusiasm.

## Failure and compatibility scenarios
- C01: Old blocked high-priority item does not stall lower-priority unrelated eligible work.
- C02: Equal-priority eligible items retain oldest-first order across restart.
- C03: Urgent conflict cannot launch on mere cancellation acknowledgment.
- C04: Priority update racing admission produces one auditable order, not duplicate dispatch.

## Rollout / rollback
Persist queue identity/order/blockers; freeze dispatch on downgrade and rebuild indices without losing original admission timestamps.

## Acceptance boundary
Concurrent queue/restart integration and actual-stop boundary with direct sessions included.
Structural inspection and provider doubles may support but cannot replace this boundary. External/native prerequisites unavailable means blocked, not complete. User has authorized local homelab/Mac work previously; that does not authorize unrelated Brown/cloud/provider mutations or spend.

## Implementation readiness
This is a bounded behavior contract, not code-complete implementation instructions. A `feature` refinement must replace discovery tasks with exact 2–5 minute test/red/minimal-code/green/commit steps, complete code blocks and actual symbol names, then pass review. Newly created paths must be explicitly listed there. If provider/UI/product judgment remains genuinely unresolved, retain blocked status and ask that one question rather than choose silently.
