# Independent delivery authorization and effect reconciliation: design boundary

## Read first
`../../../docs/fork-prd.md`, `../prd-execution-map/design.md`, this proposal/spec, and the prerequisite changes `verification-acceptance-gates`, `safe-resume-reconciliation`. Baseline `1427da6`; all source lines must be refreshed after prerequisite changes. Paths below are existing anchors, not permission to edit every file.

## Existing surfaces and file responsibilities
- `crates/engine/src/source_control.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/engine/src/change_requests.rs`: existing source/test/config anchor; inspect its graph card before source.
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
Define independently callable push/create-PR/merge/release/deploy/publish intents, each bound to exact candidate, destination, account reference and workflow action policy. Persist planned/dispatched/observed/uncertain/reconciled outcome states. An ambiguous effect is queried/reconciled before another dispatch; dedupe keys are not exactly-once claims. This unit defines the contract, not every provider adapter.

## Misinterpretations to reject in review
- Do not treat PR status polling as delivery orchestration.
- Do not embed provider tokens in ledger or evidence.
- Deploy is not always cloud hosting; preserve explicit destination semantics.

## Failure and compatibility scenarios
- C01: Accepted candidate without deploy permission cannot deploy.
- C02: Autonomous action policy may authorize one action without universal per-action dialog.
- C03: Crash after provider mutation before acknowledgment: uncertain record, query existing effect before retry.
- C04: Destination/account changes after approval: new authorization binding required.

## Rollout / rollback
Append-only effect records retained across downgrade. Disable new dispatch if reconciliation unsupported; never delete uncertainty to unblock work.

## Acceptance boundary
Controlled local external-effect fixture with crash boundaries, plus each adapter's separate authorized real destination gate.
Structural inspection and provider doubles may support but cannot replace this boundary. External/native prerequisites unavailable means blocked, not complete. User has authorized local homelab/Mac work previously; that does not authorize unrelated Brown/cloud/provider mutations or spend.

## Implementation readiness
This is a bounded behavior contract, not code-complete implementation instructions. A `feature` refinement must replace discovery tasks with exact 2–5 minute test/red/minimal-code/green/commit steps, complete code blocks and actual symbol names, then pass review. Newly created paths must be explicitly listed there. If provider/UI/product judgment remains genuinely unresolved, retain blocked status and ask that one question rather than choose silently.
