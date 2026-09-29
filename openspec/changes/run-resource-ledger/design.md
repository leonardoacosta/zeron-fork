# Durable resource budgets and usage: design boundary

## Read first
`../../../docs/fork-prd.md`, `../prd-execution-map/design.md`, this proposal/spec, and the prerequisite changes `harness-preflight-binding`, `profile-access-enforcement`. Baseline `1427da6`; all source lines must be refreshed after prerequisite changes. Paths below are existing anchors, not permission to edit every file.

## Existing surfaces and file responsibilities
- `crates/engine/src/sessions.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/engine/src/run_journal.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/engine/src/agent_accounts/usage.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/proto/src/agent.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/sync/src/store.rs`: existing source/test/config anchor; inspect its graph card before source.

## Integration contract to freeze before implementation
- Input: explicit actor/work-profile, operation identity, relevant immutable version bindings and requested scope; validate at owning engine boundary, not merely UI.
- Output: typed observed result with version/owner, unsupported/denied/uncertain states distinguished; no fake success.
- Side effects: enumerate each process/file/database/network effect in refinement, including retries and failure between persistence and acknowledgment.
- Ownership: reuse current Rust engine + typed RPC + profile SQLite where appropriate; registry LWW is not authoritative revision history. Reuse existing mechanisms before adding new module/dependency.
- Interface freeze: discovery must record exact existing symbols and proposed DTO/state transitions, error payloads, capability identifier, migration/version compatibility and callers/tests. No names in this paragraph create a runtime API.

## Required behavior
Persist reservations and observed usage bound to run/profile/resource policy. Unknown price or usage remains unknown. Parent and child runs draw from one authorized shared budget without double counting; reservation/launch is atomic or recoverably reconciled. Budget exhaustion holds new work and invokes safe stopping for active work according to policy. No invented universal numeric budget.

## Misinterpretations to reject in review
- Estimated cost is not settled cost.
- A task retry must not reset the budget.
- No resource guarantee without a capability that enforces it.

## Failure and compatibility scenarios
- C01: Two concurrent runs race for the final reservation: at most one starts.
- C02: Owner restarts with a reserved-but-unconfirmed run: reconcile rather than spend reservation twice or refund blindly.
- C03: Provider omits cost: show unknown and enforce policy for unknown cost, never display zero.
- C04: Child usage rolls up once despite repeated provider events.

## Rollout / rollback
Append-only ledger migration; reconcile outstanding reservations before rollback. Do not discard charges or return allocations until effects are known.

## Acceptance boundary
Concurrent reservation/restart integration and provider fixture with duplicated/missing usage; real supported provider observations separately labelled. The provider fixture must also exercise C03 with a selected provider response that omits cost while a bounded unknown-cost policy applies. Assert the displayed/returned value is `unknown` (never numeric zero), the configured unknown-cost policy is enforced before another launch, and no guessed provider cost or successful budget settlement is recorded. Keep fixture evidence synthetic; real provider semantics remain separately evidenced or blocked.
Structural inspection and provider doubles may support but cannot replace this boundary. External/native prerequisites unavailable means blocked, not complete. User has authorized local homelab/Mac work previously; that does not authorize unrelated Brown/cloud/provider mutations or spend.

## Implementation readiness
This is a bounded behavior contract, not code-complete implementation instructions. A `feature` refinement must replace discovery tasks with exact 2–5 minute test/red/minimal-code/green/commit steps, complete code blocks and actual symbol names, then pass review. Newly created paths must be explicitly listed there. If provider/UI/product judgment remains genuinely unresolved, retain blocked status and ask that one question rather than choose silently.
