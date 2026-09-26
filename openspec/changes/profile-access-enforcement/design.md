# Execution-time profile and resource authorization: design boundary

## Read first
`../../../docs/fork-prd.md`, `../prd-execution-map/design.md`, this proposal/spec, and the prerequisite changes `work-profile-boundary`. Baseline `1427da6`; all source lines must be refreshed after prerequisite changes. Paths below are existing anchors, not permission to edit every file.

## Existing surfaces and file responsibilities
- `crates/engine/src/rpc.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/engine/src/sessions.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/engine/src/agent_accounts.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/engine/src/repos.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/engine/src/terminals.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/harness/src/lib.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/engine/tests/local_profiles.rs`: existing source/test/config anchor; inspect its graph card before source.

## Integration contract to freeze before implementation
- Input: explicit actor/work-profile, operation identity, relevant immutable version bindings and requested scope; validate at owning engine boundary, not merely UI.
- Output: typed observed result with version/owner, unsupported/denied/uncertain states distinguished; no fake success.
- Side effects: enumerate each process/file/database/network effect in refinement, including retries and failure between persistence and acknowledgment.
- Ownership: reuse current Rust engine + typed RPC + profile SQLite where appropriate; registry LWW is not authoritative revision history. Reuse existing mechanisms before adding new module/dependency.
- Interface freeze: discovery must record exact existing symbols and proposed DTO/state transitions, error payloads, capability identifier, migration/version compatibility and callers/tests. No names in this paragraph create a runtime API.

## Required behavior
Validate work-profile policy at every engine entry point that reads protected content or launches tools: direct sessions, assignment operations, MCP, terminal, repository and credential selection. Bind allowed repositories, account references, tools, environments and action scope explicitly. Revalidate at launch and external-effect boundaries; policy revocation blocks new effects and enters the configured stop/hold path. Never serialize secret values into authority snapshots.

## Misinterpretations to reject in review
- Connectivity, parent assignment and browser login grant no authority.
- Do not enforce only in UI or only when creating a record.
- Do not snapshot raw credentials or copy all host environment variables into children.

## Failure and compatibility scenarios
- C01: A trusted remote device supplies a foreign profile/account/repository ID: reject before any read or child process starts.
- C02: A symlink or renamed checkout escapes the approved repository root: reject the resolved target.
- C03: Policy changes after preflight but before dispatch: dispatch rechecks and denies stale authority.
- C04: An unavailable requested account/tool must report unavailable, not fall back to a global default.
- C05: Direct session and assignment invoking the same protected operation receive equivalent authorization decisions.

## Rollout / rollback
Roll back enforcement code only with execution disabled for newly bound profiles. Never turn unknown policy into allow to preserve compatibility.

## Acceptance boundary
Instrument real engine dispatch boundaries and prove unauthorized paths perform zero protected reads/effects; approved isolated account succeeds.
Structural inspection and provider doubles may support but cannot replace this boundary. External/native prerequisites unavailable means blocked, not complete. User has authorized local homelab/Mac work previously; that does not authorize unrelated Brown/cloud/provider mutations or spend.

## Implementation readiness
This is a bounded behavior contract, not code-complete implementation instructions. A `feature` refinement must replace discovery tasks with exact 2–5 minute test/red/minimal-code/green/commit steps, complete code blocks and actual symbol names, then pass review. Newly created paths must be explicitly listed there. If provider/UI/product judgment remains genuinely unresolved, retain blocked status and ask that one question rather than choose silently.
