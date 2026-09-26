# CI admission and round promotion: design boundary

## Read first
`../../../docs/fork-prd.md`, `../prd-execution-map/design.md`, this proposal/spec, and the prerequisite changes none. Baseline `1427da6`; all source lines must be refreshed after prerequisite changes. Paths below are existing anchors, not permission to edit every file.

## Existing surfaces and file responsibilities
- `.github/workflows/ui-tests.yml`: existing source/test/config anchor; inspect its graph card before source.
- `.github/workflows/preview-tests.yml`: existing source/test/config anchor; inspect its graph card before source.
- `.github/workflows/windows.yml`: existing source/test/config anchor; inspect its graph card before source.
- `Cargo.toml`: existing source/test/config anchor; inspect its graph card before source.
- `openspec/README.md`: existing source/test/config anchor; inspect its graph card before source.

## Integration contract to freeze before implementation
- Input: explicit actor/work-profile, operation identity, relevant immutable version bindings and requested scope; validate at owning engine boundary, not merely UI.
- Output: typed observed result with version/owner, unsupported/denied/uncertain states distinguished; no fake success.
- Side effects: enumerate each process/file/database/network effect in refinement, including retries and failure between persistence and acknowledgment.
- Ownership: reuse current Rust engine + typed RPC + profile SQLite where appropriate; registry LWW is not authoritative revision history. Reuse existing mechanisms before adding new module/dependency.
- Interface freeze: discovery must record exact existing symbols and proposed DTO/state transitions, error payloads, capability identifier, migration/version compatibility and callers/tests. No names in this paragraph create a runtime API.

## Required behavior
Extend existing CI, not a separate build system. Every change iteration must pass its declared checks; every integrated round must pass the union of affected checks on one exact commit. Persist requirement-to-check results, platform, toolchain, skipped tests and artifact references in the change tasks. A failed, missing, cancelled or stale required check blocks promotion. Newly discovered prerequisite failures become bounded repair changes, not permanent waivers.

## Misinterpretations to reject in review
- Do not call local shell execution a hosted CI run.
- Do not use continue-on-error, lowered lint severity, deleted assertions, blanket ignores or rerun-until-green as fixes.
- The currently observed formatter/clippy baseline is not proven green; repair it in scope before admitting later rounds.

## Failure and compatibility scenarios
- C01: Given two independently green changes with conflicting combined behavior, when integrated CI fails, then neither combined round nor its dependents promote.
- C02: Given CI success for commit A, when source/config/lockfile changes to B, then A evidence cannot promote B.
- C03: Given a filter selects zero tests or an ignored external test never runs, then it is not coverage.
- C04: Given native platform/auth credentials are unavailable, record blocked evidence and hold the affected acceptance, without disabling a job to manufacture green.

## Rollout / rollback
Revert workflow changes without deleting historical artifacts. Never modify deploy/release triggers to run on planning branches. Preserve read-only permissions; no secrets in untrusted pull-request jobs.

## Acceptance boundary
Run documented quality/test commands and demonstrate an intentionally failing disposable branch cannot promote; no real release or hosted mutation is needed.
Structural inspection and provider doubles may support but cannot replace this boundary. External/native prerequisites unavailable means blocked, not complete. User has authorized local homelab/Mac work previously; that does not authorize unrelated Brown/cloud/provider mutations or spend.

## Implementation readiness
This is a bounded behavior contract, not code-complete implementation instructions. A `feature` refinement must replace discovery tasks with exact 2–5 minute test/red/minimal-code/green/commit steps, complete code blocks and actual symbol names, then pass review. Newly created paths must be explicitly listed there. If provider/UI/product judgment remains genuinely unresolved, retain blocked status and ask that one question rather than choose silently.
