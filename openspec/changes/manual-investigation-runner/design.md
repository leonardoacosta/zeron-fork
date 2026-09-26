# Manual bounded investigation workflow: design boundary

## Read first
`../../../docs/fork-prd.md`, `../prd-execution-map/design.md`, this proposal/spec, and the prerequisite changes `safe-resume-reconciliation`, `verification-acceptance-gates`, `run-resource-ledger`. Baseline `1427da6`; all source lines must be refreshed after prerequisite changes. Paths below are existing anchors, not permission to edit every file.

## Existing surfaces and file responsibilities
- `crates/engine/src/sessions.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/engine/src/rpc.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/proto/src/assignment.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/sync/src/store.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/engine/tests/restart_resume.rs`: existing source/test/config anchor; inspect its graph card before source.

## Integration contract to freeze before implementation
- Input: explicit actor/work-profile, operation identity, relevant immutable version bindings and requested scope; validate at owning engine boundary, not merely UI.
- Output: typed observed result with version/owner, unsupported/denied/uncertain states distinguished; no fake success.
- Side effects: enumerate each process/file/database/network effect in refinement, including retries and failure between persistence and acknowledgment.
- Ownership: reuse current Rust engine + typed RPC + profile SQLite where appropriate; registry LWW is not authoritative revision history. Reuse existing mechanisms before adding new module/dependency.
- Interface freeze: discovery must record exact existing symbols and proposed DTO/state transitions, error payloads, capability identifier, migration/version compatibility and callers/tests. No names in this paragraph create a runtime API.

## Required behavior
Explicitly launch one configured investigation for an assignment after profile/preflight/resource/selection gates. Bind native session IDs and observations; findings can be the terminal output. Preserve objective and permissions through replacement, with stop proof for affected old execution. Keep direct sessions runnable without implicit assignments. No coding/delivery authorization inferred from investigation.

## Misinterpretations to reject in review
- Do not build a generic autonomous executor before safety prerequisites pass.
- Investigate does not mean implement.
- Store creation/promotion must still perform zero harness launches.

## Failure and compatibility scenarios
- C01: Double-click/retried launch yields one run identity and one resource reservation.
- C02: Replacement adds linked session while preserving findings/history and allowed actions.
- C03: Investigation ends with checked findings and unresolved questions, without requiring code changes.
- C04: Direct session opens normally without automatic assignment creation.

## Rollout / rollback
Existing assignments remain records until explicit launch. Pause/hold active runs before downgrade; preserve run IDs and findings.

## Acceptance boundary
First real end-to-end investigation on harmless local repository: launch, stop, replace, restart, accepted findings; bounded authorized harness budget.
Structural inspection and provider doubles may support but cannot replace this boundary. External/native prerequisites unavailable means blocked, not complete. User has authorized local homelab/Mac work previously; that does not authorize unrelated Brown/cloud/provider mutations or spend.

## Implementation readiness
This is a bounded behavior contract, not code-complete implementation instructions. A `feature` refinement must replace discovery tasks with exact 2–5 minute test/red/minimal-code/green/commit steps, complete code blocks and actual symbol names, then pass review. Newly created paths must be explicitly listed there. If provider/UI/product judgment remains genuinely unresolved, retain blocked status and ask that one question rather than choose silently.
