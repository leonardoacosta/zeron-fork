# Desktop assignment and intervention surface: design boundary

## Read first
`../../../docs/fork-prd.md`, `../prd-execution-map/design.md`, this proposal/spec, and the prerequisite changes `manual-investigation-runner`. Baseline `1427da6`; all source lines must be refreshed after prerequisite changes. Paths below are existing anchors, not permission to edit every file.

## Existing surfaces and file responsibilities
- `crates/ui/src/state.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/ui/src/shell.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/ui/src/settings.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/ui/src/notify.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/proto/src/assignment.rs`: existing source/test/config anchor; inspect its graph card before source.

## Integration contract to freeze before implementation
- Input: explicit actor/work-profile, operation identity, relevant immutable version bindings and requested scope; validate at owning engine boundary, not merely UI.
- Output: typed observed result with version/owner, unsupported/denied/uncertain states distinguished; no fake success.
- Side effects: enumerate each process/file/database/network effect in refinement, including retries and failure between persistence and acknowledgment.
- Ownership: reuse current Rust engine + typed RPC + profile SQLite where appropriate; registry LWW is not authoritative revision history. Reuse existing mechanisms before adding new module/dependency.
- Interface freeze: discovery must record exact existing symbols and proposed DTO/state transitions, error payloads, capability identifier, migration/version compatibility and callers/tests. No names in this paragraph create a runtime API.

## Required behavior
Add explicit create/promote/read/history/launch controls alongside direct sessions. Before launch show profile, selected workflow/version/reason, permissions, resources and unavailable capabilities. Show stopping versus confirmed stop, takeover/handback, evidence class and blocked reasons. UI location must be reviewed using existing navigation conventions before implementation; preserve keyboard and screen-reader operation.

## Misinterpretations to reject in review
- Do not mark all linked agents done as assignment accepted.
- Do not hide uncertainty behind a green completion badge.
- Do not independently invent a sidebar/navigation redesign.

## Failure and compatibility scenarios
- C01: Open ordinary conversation: no forced assignment administration.
- C02: Promote requires explicit action and preserves transcript.
- C03: Disconnected owner or old capability: show unavailable/unsupported, never local duplicate.
- C04: Screen-reader/keyboard user can inspect workflow reason and stop uncertainty without relying on color.

## Rollout / rollback
Feature-gate presentation, keep stored records intact; remove UI entry points without deleting assignments. Preserve old client capability behavior.

## Acceptance boundary
Native GPUI workflow with actual owner/client, keyboard/focus/accessibility checks and zero implicit assignments.
Structural inspection and provider doubles may support but cannot replace this boundary. External/native prerequisites unavailable means blocked, not complete. User has authorized local homelab/Mac work previously; that does not authorize unrelated Brown/cloud/provider mutations or spend.

## Implementation readiness
This is a bounded behavior contract, not code-complete implementation instructions. A `feature` refinement must replace discovery tasks with exact 2–5 minute test/red/minimal-code/green/commit steps, complete code blocks and actual symbol names, then pass review. Newly created paths must be explicitly listed there. If provider/UI/product judgment remains genuinely unresolved, retain blocked status and ask that one question rather than choose silently.
