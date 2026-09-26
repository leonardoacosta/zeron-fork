# Release, deploy and publish adapters: design boundary

## Read first
`../../../docs/fork-prd.md`, `../prd-execution-map/design.md`, this proposal/spec, and the prerequisite changes `delivery-effect-ledger`, `integration-github-ado-research`. Baseline `1427da6`; all source lines must be refreshed after prerequisite changes. Paths below are existing anchors, not permission to edit every file.

## Existing surfaces and file responsibilities
- `scripts/package-linux.sh`: existing source/test/config anchor; inspect its graph card before source.
- `scripts/package-macos.sh`: existing source/test/config anchor; inspect its graph card before source.
- `scripts/package-windows.ps1`: existing source/test/config anchor; inspect its graph card before source.
- `.github/workflows/release.yml`: existing source/test/config anchor; inspect its graph card before source.
- `apps/zeron/src/daemon.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/engine/src/project_actions.rs`: existing source/test/config anchor; inspect its graph card before source.

## Integration contract to freeze before implementation
- Input: explicit actor/work-profile, operation identity, relevant immutable version bindings and requested scope; validate at owning engine boundary, not merely UI.
- Output: typed observed result with version/owner, unsupported/denied/uncertain states distinguished; no fake success.
- Side effects: enumerate each process/file/database/network effect in refinement, including retries and failure between persistence and acknowledgment.
- Ownership: reuse current Rust engine + typed RPC + profile SQLite where appropriate; registry LWW is not authoritative revision history. Reuse existing mechanisms before adding new module/dependency.
- Interface freeze: discovery must record exact existing symbols and proposed DTO/state transitions, error payloads, capability identifier, migration/version compatibility and callers/tests. No names in this paragraph create a runtime API.

## Required behavior
Implement individually callable release/deploy/publish against explicitly selected destinations and verified contracts. Preserve build artifact identity, target environment, authorization and post-delivery observation. Local installation is a valid deploy target; hosted replacement is never inferred. Full release-candidate management beyond these actions remains outside approved scope.

## Misinterpretations to reject in review
- Do not trigger existing release workflow just to validate a plan.
- Deploy success is not confirmed user outcome.
- Do not invent an entire release train/lifecycle.

## Failure and compatibility scenarios
- C01: Artifact built from revision A cannot be presented as delivery of B.
- C02: Install fails after staging: retain previous executable/data and report rollback result.
- C03: Publish returns success but target serves old content: delivered may be observed but outcome-confirmed fails.
- C04: Unsupported signing/provider credentials: blocked acceptance, no disabling security or password resets.

## Rollout / rollback
Per-target rollback recipe required before dispatch; back up user data and executable, never destructive blanket cleanup. External irreversible effects require explicit reconciliation.

## Acceptance boundary
Harmless local install with service recovery and rollback, then separately authorized external destinations only when selected.
Structural inspection and provider doubles may support but cannot replace this boundary. External/native prerequisites unavailable means blocked, not complete. User has authorized local homelab/Mac work previously; that does not authorize unrelated Brown/cloud/provider mutations or spend.

## Implementation readiness
This is a bounded behavior contract, not code-complete implementation instructions. A `feature` refinement must replace discovery tasks with exact 2–5 minute test/red/minimal-code/green/commit steps, complete code blocks and actual symbol names, then pass review. Newly created paths must be explicitly listed there. If provider/UI/product judgment remains genuinely unresolved, retain blocked status and ask that one question rather than choose silently.
