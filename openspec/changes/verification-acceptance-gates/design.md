# Configured verification and acceptance transitions: design boundary

## Read first
`../../../docs/fork-prd.md`, `../prd-execution-map/design.md`, this proposal/spec, and the prerequisite changes `workflow-version-selection`, `revision-evidence-bindings`, `profile-access-enforcement`. Baseline `1427da6`; all source lines must be refreshed after prerequisite changes. Paths below are existing anchors, not permission to edit every file.

## Existing surfaces and file responsibilities
- `crates/engine/src/rpc.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/proto/src/assignment.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/sync/src/store.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/engine/src/run_journal.rs`: existing source/test/config anchor; inspect its graph card before source.

## Integration contract to freeze before implementation
- Input: explicit actor/work-profile, operation identity, relevant immutable version bindings and requested scope; validate at owning engine boundary, not merely UI.
- Output: typed observed result with version/owner, unsupported/denied/uncertain states distinguished; no fake success.
- Side effects: enumerate each process/file/database/network effect in refinement, including retries and failure between persistence and acknowledgment.
- Ownership: reuse current Rust engine + typed RPC + profile SQLite where appropriate; registry LWW is not authoritative revision history. Reuse existing mechanisms before adding new module/dependency.
- Interface freeze: discovery must record exact existing symbols and proposed DTO/state transitions, error payloads, capability identifier, migration/version compatibility and callers/tests. No names in this paragraph create a runtime API.

## Required behavior
Keep agent-finished, verified, accepted, delivered and outcome-confirmed separate. Evaluate configured checks against exact bound output versions. Human or autonomous acceptance is allowed only as workflow policy specifies. Preserve external reviewer/OpenSpec/planning authority; in-product status cannot overwrite it. Missing/stale/contradictory evidence holds dependent transitions.

## Misinterpretations to reject in review
- CI success alone is not every product acceptance condition.
- Acceptance grants no blanket delivery permission.
- Do not combine booleans that permit impossible state combinations.

## Failure and compatibility scenarios
- C01: Agent reports success while required check fails: verified/accepted stay false.
- C02: Autonomous gate with all required checks and valid policy accepts without inventing a universal manual approval.
- C03: Human approval for output A cannot apply to changed output B.
- C04: External reviewer rejects a required review while internal tests pass: gate remains held.

## Rollout / rollback
Persist decision and inputs atomically, append revisions instead of rewriting past approvals. Rollback holds unsupported decisions.

## Acceptance boundary
C04 real acceptance must use the owner RPC with required internal checks passing and an external reviewer rejection. Persist the held decision, restart at the decision commit boundary, then re-read the same output/evidence binding and assert it remains held with the external rejection intact and no accepted/delivery/effect record. The owner-RPC transitions for stale/revoked/external rejection must be checked against this durable state. Structural inspection and provider doubles may support but cannot replace this boundary. External/native prerequisites unavailable means blocked, not complete. User has authorized local homelab/Mac work previously; that does not authorize unrelated Brown/cloud/provider mutations or spend.

## Implementation readiness
This is a bounded behavior contract, not code-complete implementation instructions. A `feature` refinement must replace discovery tasks with exact 2–5 minute test/red/minimal-code/green/commit steps, complete code blocks and actual symbol names, then pass review. Newly created paths must be explicitly listed there. If provider/UI/product judgment remains genuinely unresolved, retain blocked status and ask that one question rather than choose silently.

## Exact proposed predicate boundary
Tasks contain compiled4-test pure verification evaluator: empty requirements, duplicate checks, wrong evidence class, stale revision/dirty digest, blocked/failed and contradictory observations hold. This does not execute any check or establish trust in incoming records. Only owner-recorded results and a reviewed immutable evidence-set binding may reach it. Actual acceptance requires workflow-selected human/autonomous decision and external authority checks in one persisted transition; delivery remains independently gated.
