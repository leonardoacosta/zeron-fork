# Git push and change-request create/merge actions: design boundary

## Read first
`../../../docs/fork-prd.md`, `../prd-execution-map/design.md`, this proposal/spec, and the prerequisite changes `delivery-effect-ledger`, `integration-github-ado-research`. Baseline `1427da6`; all source lines must be refreshed after prerequisite changes. Paths below are existing anchors, not permission to edit every file.

## Existing surfaces and file responsibilities
- `crates/engine/src/source_control.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/engine/src/change_requests.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/engine/src/repos.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/engine/src/rpc.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/engine/tests/github_cli_login_shell.rs`: existing source/test/config anchor; inspect its graph card before source.

## Integration contract to freeze before implementation
- Input: explicit actor/work-profile, operation identity, relevant immutable version bindings and requested scope; validate at owning engine boundary, not merely UI.
- Output: typed observed result with version/owner, unsupported/denied/uncertain states distinguished; no fake success.
- Side effects: enumerate each process/file/database/network effect in refinement, including retries and failure between persistence and acknowledgment.
- Ownership: reuse current Rust engine + typed RPC + profile SQLite where appropriate; registry LWW is not authoritative revision history. Reuse existing mechanisms before adding new module/dependency.
- Interface freeze: discovery must record exact existing symbols and proposed DTO/state transitions, error payloads, capability identifier, migration/version compatibility and callers/tests. No names in this paragraph create a runtime API.

## Required behavior
Implement push, create change request and merge as independently authorized actions using verified provider methods. Freeze remote/ref/repository/account/candidate; observe exact delivered commit. Support required GitHub/ADO providers only when their research and native acceptance are complete; unsupported remains explicit. Respect protected branches and external review authority.

## Misinterpretations to reject in review
- No universal push-on-accept.
- GitHub support does not imply ADO parity.
- No force push or deleting user branches as rollback.

## Failure and compatibility scenarios
- C01: Remote URL changes between proposal and push: block and reauthorize.
- C02: PR creation times out after successful creation: discover matching external identity, do not create duplicate.
- C03: Merge observes newer head than accepted candidate: reject stale candidate.
- C04: Branch protection rejects merge: surface provider decision; never bypass or force push.

## Rollout / rollback
Disable action dispatch, preserve external links/effect ledger. Rollback cannot undo a pushed/merged effect by pretending it never occurred.

## Acceptance boundary
Local bare-remote push first; actual authorized sandbox GitHub/ADO create/merge with exact head verification and provider failure paths.
Structural inspection and provider doubles may support but cannot replace this boundary. External/native prerequisites unavailable means blocked, not complete. User has authorized local homelab/Mac work previously; that does not authorize unrelated Brown/cloud/provider mutations or spend.

## Implementation readiness
This is a bounded behavior contract, not code-complete implementation instructions. A `feature` refinement must replace discovery tasks with exact 2–5 minute test/red/minimal-code/green/commit steps, complete code blocks and actual symbol names, then pass review. Newly created paths must be explicitly listed there. If provider/UI/product judgment remains genuinely unresolved, retain blocked status and ask that one question rather than choose silently.
