# Capability preflight and frozen run configuration: design boundary

## Read first
`../../../docs/fork-prd.md`, `../prd-execution-map/design.md`, this proposal/spec, and the prerequisite changes `work-profile-boundary`. Baseline `1427da6`; all source lines must be refreshed after prerequisite changes. Paths below are existing anchors, not permission to edit every file.

## Existing surfaces and file responsibilities
- `crates/engine/src/registry.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/harness/src/lib.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/proto/src/agent.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/engine/src/sessions.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/harness/src/codex/mod.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/harness/src/claude/mod.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/harness/src/acp/mod.rs`: existing source/test/config anchor; inspect its graph card before source.

## Integration contract to freeze before implementation
- Input: explicit actor/work-profile, operation identity, relevant immutable version bindings and requested scope; validate at owning engine boundary, not merely UI.
- Output: typed observed result with version/owner, unsupported/denied/uncertain states distinguished; no fake success.
- Side effects: enumerate each process/file/database/network effect in refinement, including retries and failure between persistence and acknowledgment.
- Ownership: reuse current Rust engine + typed RPC + profile SQLite where appropriate; registry LWW is not authoritative revision history. Reuse existing mechanisms before adding new module/dependency.
- Interface freeze: discovery must record exact existing symbols and proposed DTO/state transitions, error payloads, capability identifier, migration/version compatibility and callers/tests. No names in this paragraph create a runtime API.

## Required behavior
Produce comparable per-harness capability results with supported/unsupported/unknown distinctions and observed version. Freeze requested harness/model/account reference/environment/sandbox/resource configuration for a run. Inspect actual adapter behavior, especially Codex sandbox overrides and Claude/ACP auto-approval, before claiming enforcement. Unsupported requested isolation blocks dispatch. Configuration changes require explicit new run binding.

## Misinterpretations to reject in review
- Jcode preference is not an already integrated SDK.
- A mock descriptor proves serialization, not provider behavior.
- Ordinary engineering uses the configured engineer once, not an implicit comparison.

## Failure and compatibility scenarios
- C01: A harness advertises cancellation but cannot prove descendant stopping: report that capability as unverified, not supported.
- C02: Requested sandbox differs from actual process arguments: preflight fails and no agent starts.
- C03: Missing model/account/executable cannot silently route to another engineer.
- C04: A model or adapter version changes between preflight and launch: invalidate/recheck binding.

## Rollout / rollback
Preserve existing direct-session records; gate only capabilities whose policy requires proof. Retain prior configuration/version evidence and reject unsupported downgrade.

## Acceptance boundary
Adapter argument/protocol tests plus one authorized native harness preflight; token-spending execution requires separate bounded budget.
Structural inspection and provider doubles may support but cannot replace this boundary. External/native prerequisites unavailable means blocked, not complete. User has authorized local homelab/Mac work previously; that does not authorize unrelated Brown/cloud/provider mutations or spend.

## Implementation readiness
This is a bounded behavior contract, not code-complete implementation instructions. A `feature` refinement must replace discovery tasks with exact 2–5 minute test/red/minimal-code/green/commit steps, complete code blocks and actual symbol names, then pass review. Newly created paths must be explicitly listed there. If provider/UI/product judgment remains genuinely unresolved, retain blocked status and ask that one question rather than choose silently.
