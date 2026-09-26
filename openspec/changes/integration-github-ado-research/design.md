# GitHub, ADO, MCP and Aperture boundary research: design boundary

## Read first
`../../../docs/fork-prd.md`, `../prd-execution-map/design.md`, this proposal/spec, and the prerequisite changes `ci-promotion-gates`. Baseline `1427da6`; all source lines must be refreshed after prerequisite changes. Paths below are existing anchors, not permission to edit every file.

## Existing surfaces and file responsibilities
- `crates/engine/src/source_control.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/mcp/src/tools.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/mcp/src/jsonrpc.rs`: existing source/test/config anchor; inspect its graph card before source.
- `docs/mcp.md`: existing source/test/config anchor; inspect its graph card before source.
- `docs/fork-prd.md`: existing source/test/config anchor; inspect its graph card before source.

## Integration contract to freeze before implementation
- Input: explicit actor/work-profile, operation identity, relevant immutable version bindings and requested scope; validate at owning engine boundary, not merely UI.
- Output: typed observed result with version/owner, unsupported/denied/uncertain states distinguished; no fake success.
- Side effects: enumerate each process/file/database/network effect in refinement, including retries and failure between persistence and acknowledgment.
- Ownership: reuse current Rust engine + typed RPC + profile SQLite where appropriate; registry LWW is not authoritative revision history. Reuse existing mechanisms before adding new module/dependency.
- Interface freeze: discovery must record exact existing symbols and proposed DTO/state transitions, error payloads, capability identifier, migration/version compatibility and callers/tests. No names in this paragraph create a runtime API.

## Required behavior
Map current GitHub read/status and MCP behavior; verify exact ADO and Tailscale Aperture identities, versions, APIs and authority boundaries. Record external planning/review/specification systems as authoritative. Determine remote-only repository support separately from local storage convenience. Produce independently scoped adapter follow-ups per verified system, never a blanket integration permission.

## Misinterpretations to reject in review
- Do not treat Tailscale transport or Aperture access as workflow authority.
- Do not fabricate ADO/GitHub parity.
- Never dump credentials while probing versions.

## Failure and compatibility scenarios
- C01: MCP tool available but action outside profile/workflow scope: unavailable for that action.
- C02: External issue says Done while local output unverified: no acceptance transition.
- C03: Remote repository cannot be materialized locally: report capability limitation, not require local storage as product policy.
- C04: ADO/Brown endpoint discovered: no access attempt solely because Brown profile exists.

## Rollout / rollback
Research only, read-only probes scoped to approved systems. Adapter rollback must preserve external source of truth and reconcile effects.

## Acceptance boundary
Exact provider/version capability matrix and authoritative-source mapping; write probes await named sandbox authorization.
Structural inspection and provider doubles may support but cannot replace this boundary. External/native prerequisites unavailable means blocked, not complete. User has authorized local homelab/Mac work previously; that does not authorize unrelated Brown/cloud/provider mutations or spend.

## Implementation readiness
This is a bounded behavior contract, not code-complete implementation instructions. A `feature` refinement must replace discovery tasks with exact 2–5 minute test/red/minimal-code/green/commit steps, complete code blocks and actual symbol names, then pass review. Newly created paths must be explicitly listed there. If provider/UI/product judgment remains genuinely unresolved, retain blocked status and ask that one question rather than choose silently.
