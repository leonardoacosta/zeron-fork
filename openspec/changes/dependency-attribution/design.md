# Dependency and asset attribution for fork distribution: design boundary

## Read first
`../../../docs/fork-prd.md`, `../prd-execution-map/design.md`, this proposal/spec, and the prerequisite changes `ci-promotion-gates`. Baseline `1427da6`; all source lines must be refreshed after prerequisite changes. Paths below are existing anchors, not permission to edit every file.

## Existing surfaces and file responsibilities
- `Cargo.toml`: existing source/test/config anchor; inspect its graph card before source.
- `Cargo.lock`: existing source/test/config anchor; inspect its graph card before source.
- `edge/package-lock.json`: existing source/test/config anchor; inspect its graph card before source.
- `scripts/package-linux.sh`: existing source/test/config anchor; inspect its graph card before source.
- `scripts/package-macos.sh`: existing source/test/config anchor; inspect its graph card before source.
- `dist/macos/Info.plist`: existing source/test/config anchor; inspect its graph card before source.
- `docs/fork-prd.md`: existing source/test/config anchor; inspect its graph card before source.

## Integration contract to freeze before implementation
- Input: explicit actor/work-profile, operation identity, relevant immutable version bindings and requested scope; validate at owning engine boundary, not merely UI.
- Output: typed observed result with version/owner, unsupported/denied/uncertain states distinguished; no fake success.
- Side effects: enumerate each process/file/database/network effect in refinement, including retries and failure between persistence and acknowledgment.
- Ownership: reuse current Rust engine + typed RPC + profile SQLite where appropriate; registry LWW is not authoritative revision history. Reuse existing mechanisms before adding new module/dependency.
- Interface freeze: discovery must record exact existing symbols and proposed DTO/state transitions, error payloads, capability identifier, migration/version compatibility and callers/tests. No names in this paragraph create a runtime API.

## Required behavior
Inventory exact selected dependency/asset licenses and required attribution for distributed local builds, including pinned GPUI/component forks, fonts and browser/platform components. Root MIT alone does not settle asset/dependency terms. Record evidence and package required notices without claiming legal review beyond verified facts.

## Misinterpretations to reject in review
- Do not rename upstream licenses or remove notices.
- Do not infer commercial distribution permission from successful compilation.

## Failure and compatibility scenarios
- C01: Pinned dependency revision changes: attribution evidence invalidated for that package.
- C02: Binary package omits required font notice: packaging gate fails.
- C03: License unresolved: affected distribution held, no assumption from repository root license.

## Rollout / rollback
Add notices without altering user data. Rebuild package if notice content corrected; preserve original license texts.

## Acceptance boundary
Inspect actual generated package contents and exact pinned licenses; unresolved terms routed to human review without invented conclusions.
Structural inspection and provider doubles may support but cannot replace this boundary. External/native prerequisites unavailable means blocked, not complete. User has authorized local homelab/Mac work previously; that does not authorize unrelated Brown/cloud/provider mutations or spend.

## Implementation readiness
This is a bounded behavior contract, not code-complete implementation instructions. A `feature` refinement must replace discovery tasks with exact 2–5 minute test/red/minimal-code/green/commit steps, complete code blocks and actual symbol names, then pass review. Newly created paths must be explicitly listed there. If provider/UI/product judgment remains genuinely unresolved, retain blocked status and ask that one question rather than choose silently.
