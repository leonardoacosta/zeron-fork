# Approved proposal implementation and verification stages: design boundary

## Read first
`../../../docs/fork-prd.md`, `../prd-execution-map/design.md`, this proposal/spec, and the prerequisite changes `manual-investigation-runner`, `verification-acceptance-gates`, `run-resource-ledger`. Baseline `1427da6`; all source lines must be refreshed after prerequisite changes. Paths below are existing anchors, not permission to edit every file.

## Existing surfaces and file responsibilities
- `crates/engine/src/sessions.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/engine/src/rpc.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/proto/src/assignment.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/engine/src/repos.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/sync/src/store.rs`: existing source/test/config anchor; inspect its graph card before source.

## Integration contract to freeze before implementation
- Input: explicit actor/work-profile, operation identity, relevant immutable version bindings and requested scope; validate at owning engine boundary, not merely UI.
- Output: typed observed result with version/owner, unsupported/denied/uncertain states distinguished; no fake success.
- Side effects: enumerate each process/file/database/network effect in refinement, including retries and failure between persistence and acknowledgment.
- Ownership: reuse current Rust engine + typed RPC + profile SQLite where appropriate; registry LWW is not authoritative revision history. Reuse existing mechanisms before adding new module/dependency.
- Interface freeze: discovery must record exact existing symbols and proposed DTO/state transitions, error payloads, capability identifier, migration/version compatibility and callers/tests. No names in this paragraph create a runtime API.

## Required behavior
Extend the bounded investigation runner to Understand, Investigate, Propose, Implement and Verify transitions under a pinned workflow. A proposal must pass its configured gate before any implementation dispatch. Bind exact approved scope, engineer, repository, baseline and resource policy; ordinary implementation uses that engineer once. Produce a new revision-bound candidate from observed working-tree changes, then run independent configured verification. Deliver and Confirm outcome invoke their separately gated contracts, not implicit inline side effects.

## Misinterpretations to reject in review
- Do not equate an investigation executor with the full engineering workflow.
- Do not launch comparison entrants for an ordinary stage.
- Do not conflate stage success, candidate acceptance and delivery authorization.

## Failure and compatibility scenarios
- C01: Investigation suggests code changes before proposal acceptance: no implementation launch.
- C02: Accepted proposal changes repository or allowed actions: implementation refuses stale scope and requests new gate.
- C03: Engineer finishes with uncommitted changes: candidate binds exact dirty tree, not just HEAD.
- C04: Verification fails: preserve candidate/evidence and follow configured retry or hold policy within original budget, no automatic delivery.
- C05: Workflow marks a stage optional: skip only by recorded policy, not agent improvisation.

## Rollout / rollback
Hold active stage execution with confirmed stopping before downgrade; preserve candidate bytes, run bindings and evidence. No reset of user working tree as rollback.

## Acceptance boundary
Real harmless local repository: accepted proposal to one engineer implementation, exact candidate capture, failing then passing independent check, no unauthorized delivery.
Structural inspection and provider doubles may support but cannot replace this boundary. External/native prerequisites unavailable means blocked, not complete. User has authorized local homelab/Mac work previously; that does not authorize unrelated Brown/cloud/provider mutations or spend.

## Implementation readiness
This is a bounded behavior contract, not code-complete implementation instructions. A `feature` refinement must replace discovery tasks with exact 2–5 minute test/red/minimal-code/green/commit steps, complete code blocks and actual symbol names, then pass review. Newly created paths must be explicitly listed there. If provider/UI/product judgment remains genuinely unresolved, retain blocked status and ask that one question rather than choose silently.
