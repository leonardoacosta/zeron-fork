# Jcode, Herdr and observer capability research: design boundary

## Read first
`../../../docs/fork-prd.md`, `../prd-execution-map/design.md`, this proposal/spec, and prerequisite `ci-promotion-gates`. The source baseline is `1427da6`; refresh every code citation against the current checkout. These are read-only anchors, not files to modify.

## Existing surfaces and responsibilities
- `crates/harness/src/lib.rs`: harness identity/capability declarations and launch contract.
- `crates/engine/src/registry.rs`: registry ownership and persistence behavior.
- `crates/engine/src/sessions.rs`: session lifecycle and configuration paths.
- `docs/research/harness.md`: existing harness documentation to compare with source.
- `docs/fork-prd.md`: product authority and exclusions.

All listed paths are pre-existing read-only anchors for this research. They are not proposed product edits.
Existing anchors remain exactly: `crates/harness/src/lib.rs`, `crates/engine/src/registry.rs`, `crates/engine/src/sessions.rs`, `docs/research/harness.md`, `docs/fork-prd.md`.

## Bounded questions
Answer separately for (a) Jcode local swarm, (b) Herdr attachment, and (c) SystemOne observer, Jev, Laya, empryo. Do not infer that similar labels identify the same product. For each identity ask official docs: What is the publisher/project's canonical name and URL? Which supported versions/platforms apply? What documented read-only status, start, stop/cancel, configuration, native identifier, and isolation guarantees exist? What are the documented auth and data boundaries? Which calls are local versus networked? Quote the exact page/section and version. If official material does not answer a question, mark `unknown`.

## Evidence protocol and states
Use the procedures in `tasks.md`. Each claim must have an evidence row with these exact fields: `claim_id`, `subject`, `claim`, `state` (`verified`, `contradicted`, `unknown`, `blocked`), `evidence_kind` (`official_doc`, `local_source`, `local_observation`), `source_or_command`, `version_or_commit`, `observed_at_utc`, `result_or_excerpt`, `scope`, `limitations`, `reviewer`. Documentation is not live observation. A command's exit code/version output is local observation only; it does not prove documented semantics. Never enter credentials or private identifiers in the evidence file.

## Child adapter decision record (research output only)
For each potential follow-up provide: `adapter_id` (provisional label, not API), `system_identity`, `supported_versions`, `capability`, `owner_boundary`, `inputs_and_scope`, `outputs_and_states`, `native_id`, `start_proof`, `stop_proof`, `status_proof`, `configuration_source`, `auth_boundary`, `data_boundary`, `isolation_boundary`, `read_only_operations`, `write_operations` (must say `not authorized` unless separately approved), `failure_and_retry_behavior`, `compatibility`, `evidence_refs`, `rejection_reasons`, `decision_state` (`candidate`, `blocked`, `rejected`, `needs_review`). Unknown fields remain unknown. This schema is a research handoff format, not a runtime interface.

## Rejection criteria
Reject or block executable-adapter recommendations if the product identity or version cannot be pinned; no documented or authorized local stop proof exists; identity/status cannot be tied to the correct process/session; docs and observed version disagree; isolation/authority is inferred rather than evidenced; operation needs credentials, private access, installation, upgrade, network probe, spend, or mutation not explicitly authorized. Jcode unavailable must not silently change the engineer's configured harness. Keep SystemOne distinct from engineering harness.

## Failure scenarios
- C01: installed tool without stop proof/API remains `blocked`.
- C02: docs/observed version mismatch is recorded; do not guess request shape.
- C03: Jcode preferred but unavailable leaves ordinary configured engineer unchanged.
- Unknown prerequisite: affected work is `blocked` with reason, not reported successful or rerouted.

## Scope and acceptance boundary
No external endpoint probes, private access, credentials, installation/upgrades, configuration changes, or provider writes. Exact official public documentation citations and explicitly permitted read-only local observations only. Research may establish a candidate follow-up, but must not claim a chosen interface or that all future adapters are implementable. No generic adapter framework.

## Rollback
Only these canonical design/tasks files may change. No product state changes occur. If the evidence cannot establish a criterion, preserve the `unknown`/`blocked` result rather than broadening scope.

## Refined handoff validation
Extracted exact proposed stdlib checker and ran its6 self-tests successfully in scratch19:19 UTC. This validates shape checks only, not provider claims or API readiness.
