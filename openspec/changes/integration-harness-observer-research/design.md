# Jcode, Herdr and observer capability research: design boundary

## Read first
`../../../docs/fork-prd.md`, `../prd-execution-map/design.md`, this proposal/spec, and the prerequisite changes `ci-promotion-gates`. Baseline `1427da6`; all source lines must be refreshed after prerequisite changes. Paths below are existing anchors, not permission to edit every file.

## Existing surfaces and file responsibilities
- `crates/harness/src/lib.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/engine/src/registry.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/engine/src/sessions.rs`: existing source/test/config anchor; inspect its graph card before source.
- `docs/research/harness.md`: existing source/test/config anchor; inspect its graph card before source.
- `docs/fork-prd.md`: existing source/test/config anchor; inspect its graph card before source.

## Integration contract to freeze before implementation
- Input: explicit actor/work-profile, operation identity, relevant immutable version bindings and requested scope; validate at owning engine boundary, not merely UI.
- Output: typed observed result with version/owner, unsupported/denied/uncertain states distinguished; no fake success.
- Side effects: enumerate each process/file/database/network effect in refinement, including retries and failure between persistence and acknowledgment.
- Ownership: reuse current Rust engine + typed RPC + profile SQLite where appropriate; registry LWW is not authoritative revision history. Reuse existing mechanisms before adding new module/dependency.
- Interface freeze: discovery must record exact existing symbols and proposed DTO/state transitions, error payloads, capability identifier, migration/version compatibility and callers/tests. No names in this paragraph create a runtime API.

## Required behavior
Produce versioned evidence for Jcode environment-local swarm integration and Herdr attachment, and separately SystemOne observer, Jev, Laya and empryo identity/capabilities. Identify native IDs, start/stop proof, status, configuration, usage and isolation contracts. Unknown products/APIs remain unknown and cannot become executable adapters. Keep SystemOne distinct from engineering harness.

## Misinterpretations to reject in review
- Do not conflate names or assume empryo spelling identifies a known product.
- No synthetic API response labelled live.
- Do not create a generic adapter framework before verified concrete need.

## Failure and compatibility scenarios
- C01: A tool is installed but no stop proof/API exists: capability remains blocked.
- C02: Documentation and observed version disagree: record mismatch and do not guess request shape.
- C03: Jcode preferred but unavailable: ordinary configured engineer stays unchanged.

## Rollout / rollback
Research changes only canonical design/spec/tasks. No installing/upgrading providers, changing defaults, credentials or spend without separate scoped authority.

## Acceptance boundary
Pinned official source/API references plus read-only local version/capability probes when authorized; output exact adapter contracts or explicit blocked decisions.
Structural inspection and provider doubles may support but cannot replace this boundary. External/native prerequisites unavailable means blocked, not complete. User has authorized local homelab/Mac work previously; that does not authorize unrelated Brown/cloud/provider mutations or spend.

## Implementation readiness
This is a bounded behavior contract, not code-complete implementation instructions. A `feature` refinement must replace discovery tasks with exact 2–5 minute test/red/minimal-code/green/commit steps, complete code blocks and actual symbol names, then pass review. Newly created paths must be explicitly listed there. If provider/UI/product judgment remains genuinely unresolved, retain blocked status and ask that one question rather than choose silently.
