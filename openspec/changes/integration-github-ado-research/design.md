# GitHub, ADO, MCP and Aperture boundary research: design boundary

## Read first
`../../../docs/fork-prd.md`, `../prd-execution-map/design.md`, this proposal/spec, and prerequisite `ci-promotion-gates`. Baseline `1427da6`; refresh all source citations against the current checkout. Listed source anchors are read-only.

## Existing surfaces and responsibilities
- `crates/engine/src/source_control.rs`: existing GitHub/source-control behavior.
- `crates/mcp/src/tools.rs`: exposed tool names, inputs and policy gates.
- `crates/mcp/src/jsonrpc.rs`: transport and dispatch boundary.
- `docs/mcp.md`: documented MCP contract.
- `docs/fork-prd.md`: product authority and exclusions.

All listed paths are pre-existing read-only anchors for this research. They are not proposed product edits.
Existing anchors remain exactly: `crates/engine/src/source_control.rs`, `crates/mcp/src/tools.rs`, `crates/mcp/src/jsonrpc.rs`, `docs/mcp.md`, `docs/fork-prd.md`.

## Bounded questions
For current GitHub behavior, what operations and data are actually present in local source and docs? For MCP, which tools/inputs and local authority checks exist? For GitHub, ADO, Tailscale/Aperture separately, what is the canonical product/publisher, official public API documentation, supported version, documented authentication, read/write scope, status, pagination, rate/failure semantics and authoritative source for planning/review/specification? What does the official doc say about remote repositories without a local checkout? Which behavior is local-only versus external? Cite page, section, date/version. Do not infer GitHub/ADO parity or treat Tailscale transport as workflow authority.

## Evidence and child adapter schemas
Use the common evidence row: `claim_id`, `subject`, `claim`, `state` (`verified`, `contradicted`, `unknown`, `blocked`), `evidence_kind` (`official_doc`, `local_source`, `local_observation`), `source_or_command`, `version_or_commit`, `observed_at_utc`, `result_or_excerpt`, `scope`, `limitations`, `reviewer`. A public document citation is `official_doc`, never live observation. Local source inspection is not proof of provider behavior.

Each possible follow-up gets a research-only record: `adapter_id` (provisional, not API), `system_identity`, `supported_versions`, `capability`, `owner_boundary`, `inputs_and_scope`, `outputs_and_states`, `native_id`, `start_proof`, `stop_proof`, `status_proof`, `configuration_source`, `auth_boundary`, `data_boundary`, `isolation_boundary`, `read_only_operations`, `write_operations`, `failure_and_retry_behavior`, `compatibility`, `evidence_refs`, `rejection_reasons`, `decision_state` (`candidate`, `blocked`, `rejected`, `needs_review`). Unknown values stay unknown. Not a runtime DTO.

## Rejection criteria
Reject/block a follow-up if product/version or official docs cannot be pinned; authority is unclear; access requires credentials, private endpoint, network probe, Brown tenant/profile, install/upgrade, write action, spend, or other unapproved access; only transport connectivity is shown; source-of-truth, remote-only behavior, idempotency or failure semantics are unsubstantiated; local output is not verified. In particular, an external issue marked Done cannot prove local acceptance, and a Brown endpoint is never permission to access it.

## Failure scenarios
- C01: MCP tool outside profile/workflow scope is unavailable for that action.
- C02: external issue says Done but local output is unverified: no acceptance transition.
- C03: remote-only repository unsupported by current implementation: report limitation; do not turn local materialization into a product policy.
- C04: ADO/Brown endpoint discovered: do not access it.
- Unknown prerequisite: block with reason; no silent success/reroute.

## Scope and acceptance boundary
Read-only local source/documentation inspection and public official documentation lookup only. No external API calls or endpoint probes, private access, credentials, or writes. Record API claims as documented, not observed. This research can propose separately scoped work for verified systems; it does not select interfaces or establish all future adapters as implementable.

## Rollback
Only these canonical design/tasks files may change. Preserve external source-of-truth assumptions; this work performs no external side effects.

## Filled source-evidence example
Verified against actual source at stated commit; concurrent unrelated working-tree edits are not runtime evidence.
```json
{
  "claim_id": "local-github-pr-list",
  "subject": "GitHubCli",
  "claim": "Source constructs bounded gh pr list request with checkout cwd; no ADO parity inferred.",
  "state": "verified",
  "evidence_kind": "local_source",
  "source_or_command": "crates/engine/src/source_control.rs:198-230",
  "version_or_commit": "b9623ae80225b924fe00d577d600f65938967bf6",
  "observed_at_utc": "2026-09-26T19:56:18Z",
  "result_or_excerpt": "program gh; args pr list --head --state all --limit --json; GH_PROMPT_DISABLED=1",
  "scope": "Read-only source declaration, not runtime acceptance",
  "limitations": "No gh call, credentials or external authorization behavior observed.",
  "reviewer": "coordinator source verification"
}
```

## Bounded discovery stop rule
For each named subject/question inspect the official documentation entry point and one relevant official reference page, plus listed local anchors and their direct callers. Stop once an authoritative source answers that question. If two relevant official pages do not establish the claim, record unknown with exact searched sources, not a guessed interface. Missing/denied required source is blocked. Conflicting authoritative sources require escalation rather than optimistic choice. A later separately scoped research iteration may widen search; this budget is a research stopping rule, not proof of absence. Unknown product identity stays unknown without normalizing spelling. Persist rows in this design, never only disposable scratch.
