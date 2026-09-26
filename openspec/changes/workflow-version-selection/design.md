# Versioned workflow definitions and selection: design boundary

## Read first
`../../../docs/fork-prd.md`, `../prd-execution-map/design.md`, this proposal/spec, and the prerequisite changes `revision-evidence-bindings`, `work-profile-boundary`. Baseline `1427da6`; all source lines must be refreshed after prerequisite changes. Paths below are existing anchors, not permission to edit every file.

## Existing surfaces and file responsibilities
- `crates/proto/src/assignment.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/sync/src/store.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/engine/src/rpc.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/engine/src/profile.rs`: existing source/test/config anchor; inspect its graph card before source.

## Integration contract to freeze before implementation
- Input: explicit actor/work-profile, operation identity, relevant immutable version bindings and requested scope; validate at owning engine boundary, not merely UI.
- Output: typed observed result with version/owner, unsupported/denied/uncertain states distinguished; no fake success.
- Side effects: enumerate each process/file/database/network effect in refinement, including retries and failure between persistence and acknowledgment.
- Ownership: reuse current Rust engine + typed RPC + profile SQLite where appropriate; registry LWW is not authoritative revision history. Reuse existing mechanisms before adding new module/dependency.
- Interface freeze: discovery must record exact existing symbols and proposed DTO/state transitions, error payloads, capability identifier, migration/version compatibility and callers/tests. No names in this paragraph create a runtime API.

## Required behavior
Define independently versioned workflows with stages, agent choices, checks, failure policy, gates and autonomy. Ship the PRD starting sequence without forcing investigation-only work to produce code. Select explicit assignment override, else repository default, else profile default; if none exists hold with a clear configuration error. Persist selected version and explanation before launch. Suggestions create optional updates; active definitions never mutate silently.

## Misinterpretations to reject in review
- Do not use the newest workflow version implicitly on resume.
- No single global mutable pipeline for every workflow.
- Triggers later name a version/selection contract rather than reuse interactive guessing.

## Failure and compatibility scenarios
- C01: Repository and profile defaults differ: repository wins and reason is visible.
- C02: Assignment override selects inaccessible workflow: reject rather than bypass profile policy.
- C03: Workflow updated while assignment runs: old version remains bound unless explicitly changed and revalidated.
- C04: An investigation-only workflow ends with findings and no candidate/delivery stage.

## Rollout / rollback
Immutable versions and additive references; old readers fail explicitly on unsupported workflow versions. Roll back default pointers without rewriting active runs.

## Acceptance boundary
Precedence, version pinning, invalid override and restart tests through owner RPC; UI explanation delivered by presentation changes.
Structural inspection and provider doubles may support but cannot replace this boundary. External/native prerequisites unavailable means blocked, not complete. User has authorized local homelab/Mac work previously; that does not authorize unrelated Brown/cloud/provider mutations or spend.

## Implementation readiness
This is a bounded behavior contract, not code-complete implementation instructions. A `feature` refinement must replace discovery tasks with exact 2–5 minute test/red/minimal-code/green/commit steps, complete code blocks and actual symbol names, then pass review. Newly created paths must be explicitly listed there. If provider/UI/product judgment remains genuinely unresolved, retain blocked status and ask that one question rather than choose silently.

## Exact selection core boundary
Tasks now include a compiled3-test pure precedence/no-fallback/frozen-copy implementation. IDs and versions refer to immutable workflow catalog rows, not latest pointers. Trigger resolution must not call the interactive default-selection helper without an explicit trigger workflow binding. Unknown version and unauthorized override are terminal selection errors, not reasons to fall back. Owner-side policy/catalog callbacks must be validated at persistence/dispatch boundaries. Full workflow schema/storage/runner integration remains open; pure function success is not full workflow acceptance.
