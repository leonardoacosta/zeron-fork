# Browser provider isolation research: design boundary

## Read first
`../../../docs/fork-prd.md`, `../prd-execution-map/design.md`, this proposal/spec, and the prerequisite changes `ci-promotion-gates`. Baseline `1427da6`; all source lines must be refreshed after prerequisite changes. Paths below are existing anchors, not permission to edit every file.

## Existing surfaces and file responsibilities
- `crates/ui/src/browser/mod.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/ui/src/browser/model.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/ui/src/browser/macos.rs`: existing source/test/config anchor; inspect its graph card before source.
- `scripts/run-macos-browser-fixture.sh`: existing source/test/config anchor; inspect its graph card before source.
- `docs/fork-prd.md`: existing source/test/config anchor; inspect its graph card before source.

## Integration contract to freeze before implementation
- Input: explicit actor/work-profile, operation identity, relevant immutable version bindings and requested scope; validate at owning engine boundary, not merely UI.
- Output: typed observed result with version/owner, unsupported/denied/uncertain states distinguished; no fake success.
- Side effects: enumerate each process/file/database/network effect in refinement, including retries and failure between persistence and acknowledgment.
- Ownership: reuse current Rust engine + typed RPC + profile SQLite where appropriate; registry LWW is not authoritative revision history. Reuse existing mechanisms before adding new module/dependency.
- Interface freeze: discovery must record exact existing symbols and proposed DTO/state transitions, error payloads, capability identifier, migration/version compatibility and callers/tests. No names in this paragraph create a runtime API.

## Required behavior
Compare existing embedded browser capability and candidate automation providers against required profile/session isolation, explicit signed-in scope, stopping and redacted evidence. Record API/version and credential handling, select only after reviewed decision. Browser choice is a genuine open decision, not a reason to reopen approved isolation rules.

## Misinterpretations to reject in review
- Do not assume Chrome profile equals work profile.
- Do not pick a provider based only on available skill name.

## Failure and compatibility scenarios
- C01: Provider supports screenshots but cannot isolate storage: does not satisfy session isolation.
- C02: Provider close command returns before tool action stops: cancellation remains unverified.
- C03: Provider needs cloud data upload: disclose data boundary before any private page use.

## Rollout / rollback
No user browser profile mutation during research; disposable fixtures only under authorized scope. Preserve existing browser unchanged.

## Acceptance boundary
Harmless local page/isolation probe where possible; unresolved provider decision explicitly blocks scoped-browser-capability implementation.
Structural inspection and provider doubles may support but cannot replace this boundary. External/native prerequisites unavailable means blocked, not complete. User has authorized local homelab/Mac work previously; that does not authorize unrelated Brown/cloud/provider mutations or spend.

## Implementation readiness
This is a bounded behavior contract, not code-complete implementation instructions. A `feature` refinement must replace discovery tasks with exact 2–5 minute test/red/minimal-code/green/commit steps, complete code blocks and actual symbol names, then pass review. Newly created paths must be explicitly listed there. If provider/UI/product judgment remains genuinely unresolved, retain blocked status and ask that one question rather than choose silently.
