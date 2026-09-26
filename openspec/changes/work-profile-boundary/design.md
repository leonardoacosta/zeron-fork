# Named work profiles and explicit bindings: design boundary

## Read first
`../../../docs/fork-prd.md`, `../prd-execution-map/design.md`, this proposal/spec, and the prerequisite changes `ci-promotion-gates`. Baseline `1427da6`; all source lines must be refreshed after prerequisite changes. Paths below are existing anchors, not permission to edit every file.

## Existing surfaces and file responsibilities
- `crates/engine/src/profile.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/engine/src/lib.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/proto/src/workspace.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/sync/src/store.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/engine/tests/local_profiles.rs`: existing source/test/config anchor; inspect its graph card before source.

## Integration contract to freeze before implementation
- Input: explicit actor/work-profile, operation identity, relevant immutable version bindings and requested scope; validate at owning engine boundary, not merely UI.
- Output: typed observed result with version/owner, unsupported/denied/uncertain states distinguished; no fake success.
- Side effects: enumerate each process/file/database/network effect in refinement, including retries and failure between persistence and acknowledgment.
- Ownership: reuse current Rust engine + typed RPC + profile SQLite where appropriate; registry LWW is not authoritative revision history. Reuse existing mechanisms before adding new module/dependency.
- Interface freeze: discovery must record exact existing symbols and proposed DTO/state transitions, error payloads, capability identifier, migration/version compatibility and callers/tests. No names in this paragraph create a runtime API.

## Required behavior
Introduce extensible work-profile identity/configuration separate from Local/Synced/Development transport scope. Personal/Priceless/Brown are named work contexts, not hardcoded three-case permissions. Bind direct sessions and assignments to a stable work-profile ID and revision. Existing data must have an explicit migration/binding rule; ambiguous legacy ownership remains read-only/held rather than assigned by guess.

## Misinterpretations to reject in review
- Transport login/account scope is not a work profile.
- A Brown label must not probe Brown systems.
- Do not remap historical assignments to whichever profile is active now.

## Failure and compatibility scenarios
- C01: Two profiles on one device cannot retrieve each other's assignment, transcript, upload or repository binding through local or remote RPC.
- C02: Rename a profile while a session runs: identity stays stable and the frozen binding does not silently change.
- C03: Open legacy data without an unambiguous work-profile binding: show migration-required state, retain original bytes and prohibit execution.
- C04: Create a fourth profile without changing an enum or granting default access.

## Rollout / rollback
Additive migration with a backup and old-store compatibility check. Downgrade must refuse unsupported bindings rather than merge profiles. Retain legacy source data.

## Acceptance boundary
Real two-profile owner/client reads and restart, plus legacy-store fixture migration and denied cross-profile access.
Structural inspection and provider doubles may support but cannot replace this boundary. External/native prerequisites unavailable means blocked, not complete. User has authorized local homelab/Mac work previously; that does not authorize unrelated Brown/cloud/provider mutations or spend.

## Implementation readiness
This is a bounded behavior contract, not code-complete implementation instructions. A `feature` refinement must replace discovery tasks with exact 2–5 minute test/red/minimal-code/green/commit steps, complete code blocks and actual symbol names, then pass review. Newly created paths must be explicitly listed there. If provider/UI/product judgment remains genuinely unresolved, retain blocked status and ask that one question rather than choose silently.
