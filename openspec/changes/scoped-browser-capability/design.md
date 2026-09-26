# Isolated browser sessions and explicit signed-in scope: design boundary

## Read first
`../../../docs/fork-prd.md`, `../prd-execution-map/design.md`, this proposal/spec, and the prerequisite changes `profile-access-enforcement`, `confirmed-stop-handoff`, `revision-evidence-bindings`, `integration-browser-research`. Baseline `1427da6`; all source lines must be refreshed after prerequisite changes. Paths below are existing anchors, not permission to edit every file.

## Existing surfaces and file responsibilities
- `crates/ui/src/browser/mod.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/ui/src/browser/model.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/ui/src/browser/macos.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/engine/src/rpc.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/proto/src/assignment.rs`: existing source/test/config anchor; inspect its graph card before source.

## Integration contract to freeze before implementation
- Input: explicit actor/work-profile, operation identity, relevant immutable version bindings and requested scope; validate at owning engine boundary, not merely UI.
- Output: typed observed result with version/owner, unsupported/denied/uncertain states distinguished; no fake success.
- Side effects: enumerate each process/file/database/network effect in refinement, including retries and failure between persistence and acknowledgment.
- Ownership: reuse current Rust engine + typed RPC + profile SQLite where appropriate; registry LWW is not authoritative revision history. Reuse existing mechanisms before adding new module/dependency.
- Interface freeze: discovery must record exact existing symbols and proposed DTO/state transitions, error payloads, capability identifier, migration/version compatibility and callers/tests. No names in this paragraph create a runtime API.

## Required behavior
Browser sessions isolated by default, bound to work profile plus assignment or direct session. Signed-in session reuse is explicit and scope-limited. Browser authentication grants no mutation authority; actions use workflow/profile gates. Redact secrets and unrelated content from evidence. Do not switch browser/account/provider on failure. Integrate only provider selected by research decision.

## Misinterpretations to reject in review
- Embedded preview WebView is not necessarily isolated automation.
- Do not export all cookies or private screenshots as evidence.
- Never reset a password.

## Failure and compatibility scenarios
- C01: Two profiles navigate same domain: cookie/storage/session state does not cross.
- C02: Signed-in page contains instructions to change account or publish: page data cannot authorize action.
- C03: Requested browser/account unavailable: fail visibly without fallback.
- C04: Pause browser automation while an action is pending: preserve effect uncertainty and require stop proof.

## Rollout / rollback
Close only owned sessions, keep user browser untouched. Revoke scoped handles on rollback, no destructive global profile cleanup.

## Acceptance boundary
Actual chosen provider with two isolated browser profiles and harmless local authenticated fixture; external mutation needs separate scoped authorization.
Structural inspection and provider doubles may support but cannot replace this boundary. External/native prerequisites unavailable means blocked, not complete. User has authorized local homelab/Mac work previously; that does not authorize unrelated Brown/cloud/provider mutations or spend.

## Implementation readiness
This is a bounded behavior contract, not code-complete implementation instructions. A `feature` refinement must replace discovery tasks with exact 2–5 minute test/red/minimal-code/green/commit steps, complete code blocks and actual symbol names, then pass review. Newly created paths must be explicitly listed there. If provider/UI/product judgment remains genuinely unresolved, retain blocked status and ask that one question rather than choose silently.
