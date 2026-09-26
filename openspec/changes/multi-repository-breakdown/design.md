# Bounded parent/child repository objectives: design boundary

## Read first
`../../../docs/fork-prd.md`, `../prd-execution-map/design.md`, this proposal/spec, and the prerequisite changes `accepted-output-dependencies`, `priority-backlog`, `run-resource-ledger`, `workflow-version-selection`. Baseline `1427da6`; all source lines must be refreshed after prerequisite changes. Paths below are existing anchors, not permission to edit every file.

## Existing surfaces and file responsibilities
- `crates/proto/src/assignment.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/sync/src/store.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/engine/src/rpc.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/engine/src/repos.rs`: existing source/test/config anchor; inspect its graph card before source.

## Integration contract to freeze before implementation
- Input: explicit actor/work-profile, operation identity, relevant immutable version bindings and requested scope; validate at owning engine boundary, not merely UI.
- Output: typed observed result with version/owner, unsupported/denied/uncertain states distinguished; no fake success.
- Side effects: enumerate each process/file/database/network effect in refinement, including retries and failure between persistence and acknowledgment.
- Ownership: reuse current Rust engine + typed RPC + profile SQLite where appropriate; registry LWW is not authoritative revision history. Reuse existing mechanisms before adding new module/dependency.
- Interface freeze: discovery must record exact existing symbols and proposed DTO/state transitions, error payloads, capability identifier, migration/version compatibility and callers/tests. No names in this paragraph create a runtime API.

## Required behavior
Parent objective groups linked repository-scoped children with independent workflow, permissions, candidate/evidence and delivery status. Agent breakdown is proposal until its workflow gate authorizes creation. Leo can inspect/edit. Children stay inside parent objective, approved repositories/profile and shared budget. Grouping neither grants cross-profile access nor requires simultaneous deployment.

## Misinterpretations to reject in review
- Do not clone parent permissions as unrestricted child authority.
- Do not merge children into one worktree or one evidence revision.
- Do not require all repositories deploy at once.

## Failure and compatibility scenarios
- C01: Agent proposes an extra unapproved repository: retain proposal but do not create executable child.
- C02: Autonomous breakdown within configured scope can create children without imposing universal human confirmation.
- C03: Concurrent child reservations cannot exceed parent budget.
- C04: Editing breakdown after a child starts preserves prior evidence/effects and revalidates changed dependencies.

## Rollout / rollback
Add parent links without rewriting existing assignments; retain orphan/partial delivery status on rollback and hold new dispatch.

## Acceptance boundary
Two real local repositories with independent children, one dependency and budget/scope-denied child; restart restores editable breakdown.
Structural inspection and provider doubles may support but cannot replace this boundary. External/native prerequisites unavailable means blocked, not complete. User has authorized local homelab/Mac work previously; that does not authorize unrelated Brown/cloud/provider mutations or spend.

## Implementation readiness
This is a bounded behavior contract, not code-complete implementation instructions. A `feature` refinement must replace discovery tasks with exact 2–5 minute test/red/minimal-code/green/commit steps, complete code blocks and actual symbol names, then pass review. Newly created paths must be explicitly listed there. If provider/UI/product judgment remains genuinely unresolved, retain blocked status and ask that one question rather than choose silently.
