# Preserve direct sessions and two-device baseline: design boundary

## Read first
`../../../docs/fork-prd.md`, `../prd-execution-map/design.md`, this proposal/spec, and the prerequisite changes `ci-promotion-gates`, `assignment-record`. Baseline `1427da6`; all source lines must be refreshed after prerequisite changes. Paths below are existing anchors, not permission to edit every file.

## Existing surfaces and file responsibilities
- `crates/engine/tests/device_routing.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/engine/tests/local_profiles.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/engine/tests/restart_resume.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/rpc/src/lib.rs`: existing source/test/config anchor; inspect its graph card before source.
- `apps/zeron/src/daemon.rs`: existing source/test/config anchor; inspect its graph card before source.
- `openspec/changes/assignment-record/tasks.md`: existing source/test/config anchor; inspect its graph card before source.

## Integration contract to freeze before implementation
- Input: explicit actor/work-profile, operation identity, relevant immutable version bindings and requested scope; validate at owning engine boundary, not merely UI.
- Output: typed observed result with version/owner, unsupported/denied/uncertain states distinguished; no fake success.
- Side effects: enumerate each process/file/database/network effect in refinement, including retries and failure between persistence and acknowledgment.
- Ownership: reuse current Rust engine + typed RPC + profile SQLite where appropriate; registry LWW is not authoritative revision history. Reuse existing mechanisms before adding new module/dependency.
- Interface freeze: discovery must record exact existing symbols and proposed DTO/state transitions, error payloads, capability identifier, migration/version compatibility and callers/tests. No names in this paragraph create a runtime API.

## Required behavior
Codify current successful assignment persistence and ordinary-session behavior as regression gates. Preserve explicit null RPC successes, unsupported owner rejection, no local substitutes and no implicit delegation. Keep local private deployment distinct from hosted authentication acceptance. Verify exact installed artifacts rather than version string alone.

## Misinterpretations to reject in review
- Do not reimplement existing assignment-record.
- Do not count private relay tests as WorkOS proof.
- A version string shared by upstream/fork does not identify binary bytes.

## Failure and compatibility scenarios
- C01: Owner restarts after acknowledged assignment: native second-device read/history match and owner unchanged.
- C02: Old owner lacks capability: assignment rejected explicitly, ordinary session unaffected.
- C03: Successful null response completes RPC rather than hanging.
- C04: Direct session opens without an assignment or hidden workflow launch.

## Rollout / rollback
Use isolated data and preserve installed original app; service tests stop only owned fixtures. Do not reboot user machines without interruption authorization.

## Acceptance boundary
Existing native suites plus installed Mac/homelab test evidence reconciled to commit/binary identity; lifecycle caveats explicit.
Structural inspection and provider doubles may support but cannot replace this boundary. External/native prerequisites unavailable means blocked, not complete. User has authorized local homelab/Mac work previously; that does not authorize unrelated Brown/cloud/provider mutations or spend.

## Implementation readiness
This is a bounded behavior contract, not code-complete implementation instructions. A `feature` refinement must replace discovery tasks with exact 2–5 minute test/red/minimal-code/green/commit steps, complete code blocks and actual symbol names, then pass review. Newly created paths must be explicitly listed there. If provider/UI/product judgment remains genuinely unresolved, retain blocked status and ask that one question rather than choose silently.
