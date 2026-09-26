# Explicit isolated engineering comparisons: design boundary

## Read first
`../../../docs/fork-prd.md`, `../prd-execution-map/design.md`, this proposal/spec, and the prerequisite changes `run-resource-ledger`, `verification-acceptance-gates`, `safe-resume-reconciliation`, `integration-harness-observer-research`. Baseline `1427da6`; all source lines must be refreshed after prerequisite changes. Paths below are existing anchors, not permission to edit every file.

## Existing surfaces and file responsibilities
- `crates/engine/src/repos.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/engine/src/sessions.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/proto/src/assignment.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/sync/src/store.rs`: existing source/test/config anchor; inspect its graph card before source.

## Integration contract to freeze before implementation
- Input: explicit actor/work-profile, operation identity, relevant immutable version bindings and requested scope; validate at owning engine boundary, not merely UI.
- Output: typed observed result with version/owner, unsupported/denied/uncertain states distinguished; no fake success.
- Side effects: enumerate each process/file/database/network effect in refinement, including retries and failure between persistence and acknowledgment.
- Ownership: reuse current Rust engine + typed RPC + profile SQLite where appropriate; registry LWW is not authoritative revision history. Reuse existing mechanisms before adding new module/dependency.
- Interface freeze: discovery must record exact existing symbols and proposed DTO/state transitions, error payloads, capability identifier, migration/version compatibility and callers/tests. No names in this paragraph create a runtime API.

## Required behavior
Only user-launched comparisons with task, entrants and budget. Freeze identical baseline/input/configuration bindings and isolate each attempt. Report disclosed configurations, cost unknowns, independent correctness results and infrastructure failures separately. Comparison recommends; Leo alone approves routing/default changes. No automatic delivery or winning-run adoption.

## Misinterpretations to reject in review
- Ordinary run must not secretly execute multiple engineers.
- Never compare on shared writable worktree.
- A provider marketing capability is not tested isolation.

## Failure and compatibility scenarios
- C01: Entrants start from different dirty trees: admission fails before spending.
- C02: One entrant infrastructure fails: do not rank it as engineering incorrectness without evidence.
- C03: Fast candidate fails independent correctness check: cannot win by speed alone.
- C04: Winner selected: defaults unchanged and delivery not triggered.

## Rollout / rollback
Keep isolated attempt directories/evidence until retention authorized. Abort/stop-confirm all attempts before cleanup; preserve external effects and costs.

## Acceptance boundary
Two bounded harmless local entrants on identical baseline, actual isolation tests, independent verifier and no-default-change assertions.
Structural inspection and provider doubles may support but cannot replace this boundary. External/native prerequisites unavailable means blocked, not complete. User has authorized local homelab/Mac work previously; that does not authorize unrelated Brown/cloud/provider mutations or spend.

## Implementation readiness
This is a bounded behavior contract, not code-complete implementation instructions. A `feature` refinement must replace discovery tasks with exact 2–5 minute test/red/minimal-code/green/commit steps, complete code blocks and actual symbol names, then pass review. Newly created paths must be explicitly listed there. If provider/UI/product judgment remains genuinely unresolved, retain blocked status and ask that one question rather than choose silently.
