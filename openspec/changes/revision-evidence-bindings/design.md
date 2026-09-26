# Versioned outputs and evidence provenance: design boundary

## Read first
`../../../docs/fork-prd.md`, `../prd-execution-map/design.md`, this proposal/spec, and the prerequisite changes `work-profile-catalog`, `assignment-record`. Baseline `1427da6`; all source lines must be refreshed after prerequisite changes. Paths below are existing anchors, not permission to edit every file.

## Existing surfaces and file responsibilities
- `crates/proto/src/assignment.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/sync/src/store.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/engine/src/rpc.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/engine/src/run_journal.rs`: existing source/test/config anchor; inspect its graph card before source.
- `crates/engine/tests/device_routing.rs`: existing source/test/config anchor; inspect its graph card before source.

## Integration contract to freeze before implementation
- Input: explicit actor/work-profile, operation identity, relevant immutable version bindings and requested scope; validate at owning engine boundary, not merely UI.
- Output: typed observed result with version/owner, unsupported/denied/uncertain states distinguished; no fake success.
- Side effects: enumerate each process/file/database/network effect in refinement, including retries and failure between persistence and acknowledgment.
- Ownership: reuse current Rust engine + typed RPC + profile SQLite where appropriate; registry LWW is not authoritative revision history. Reuse existing mechanisms before adding new module/dependency.
- Interface freeze: discovery must record exact existing symbols and proposed DTO/state transitions, error payloads, capability identifier, migration/version compatibility and callers/tests. No names in this paragraph create a runtime API.

## Required behavior
Introduce immutable output/candidate identities bound to exact assignment revision, source revision and dirty-tree content, frozen input/configuration/authorization/resource bindings, environment and native sessions. Evidence records check command, observations, outcome, limitations, timestamps and redacted artifacts. Separate structural, synthetic and real-workflow evidence. Editing inputs creates a new binding; it does not transfer approval.

## Misinterpretations to reject in review
- A hash identifies bytes; it does not prove a test ran.
- Plane Done, agent completion and reviewer approval are different facts.
- Existing evidence strings are not already a complete provenance schema.

## Failure and compatibility scenarios
- C01: Same Git commit with changed uncommitted content produces a different binding and stale prior evidence.
- C02: A candidate has artifacts but no passed check: show unverified, never accepted.
- C03: An artifact contains a secret or unrelated private content: reject/redact before persistence and alert safely.
- C04: Conflicting or missing evidence blocks dependent advancement rather than choosing the optimistic entry.

## Rollout / rollback
Add typed records alongside legacy strings; legacy remains explicitly unverified. Never backfill fabricated observations. Preserve immutable historical bindings on rollback.

## Acceptance boundary
Real create/edit/restart/read workflow proving stale invalidation and exact evidence retrieval, with synthetic fixtures separately tagged.
Structural inspection and provider doubles may support but cannot replace this boundary. External/native prerequisites unavailable means blocked, not complete. User has authorized local homelab/Mac work previously; that does not authorize unrelated Brown/cloud/provider mutations or spend.

## Implementation readiness
This is a bounded behavior contract, not code-complete implementation instructions. A `feature` refinement must replace discovery tasks with exact 2–5 minute test/red/minimal-code/green/commit steps, complete code blocks and actual symbol names, then pass review. Newly created paths must be explicitly listed there. If provider/UI/product judgment remains genuinely unresolved, retain blocked status and ask that one question rather than choose silently.

## Shared output-binding contract
Proposed OutputBinding is immutable output ID + positive revision + lowercase SHA256 content digest. Digest input must cover source commit AND dirty tracked/untracked content, normalized check inputs, workflow version, WorkProfileBinding, policy/preflight/resource references, environment identity and native session references. A hash is only identity, never correctness proof. Keep artifact storage references separate from digest and check result. Reject secrets before artifact persistence. Exact canonical encoding and collection failure semantics must be defined before runtime implementation; missing/unreadable input cannot be omitted from hash silently. Verification evaluator proposed in verification-acceptance-gates consumes exact selected evidence set with class/outcome, rejects missing/stale/contradictory evidence, and produces no delivery grant. Historical rejected rows remain in history; explicit supersession creates a new evidence set rather than deleting inconvenient failures.
