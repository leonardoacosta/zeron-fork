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

## Evidence register (2026-09-27 UTC)

All docs below were read as official public documentation on 2026-09-27; they are statements of documented behavior, not live API observations. No provider API, credential, private system, or endpoint was used. Local citations are exact source spans in this checkout; concurrent working-tree state is not runtime evidence.

| claim_id | subject | claim | state / kind | source_or_command; version | observed_at_utc | result_or_excerpt | scope; limitations; reviewer |
|---|---|---|---|---|---|---|
| L-GH-01 | Zeron GitHub source-control | Resolves pull-request summaries via local checkout context; missing host/owner/repo returns UnsupportedRepository. | verified / local_source | `crates/engine/src/source_control.rs:125-157`; checkout revision `$(git rev-parse HEAD)` | 2026-09-27T16:03Z | `resolve_github` inspects checkout then calls provider; source requires host, owner, repository. | Static source only, no command/API called. No remote-only support evidence. Coordinator. |
| L-GH-02 | Zeron GitHub source-control | Runs `gh pr list --head <selector> --state all --limit 20 --json ...` in checkout cwd; bounds time/output and disables prompts. | verified / local_source | `crates/engine/src/source_control.rs:198-221`; checkout revision `$(git rev-parse HEAD)` | 2026-09-27T16:03Z | `program: gh`; args list/head/state/limit/json; checkout cwd; timeout 20s; output limit 1MiB. | Source declaration only; no `gh` invocation, no current auth/runtime behavior observed. Coordinator. |
| L-GH-03 | Zeron GitHub source-control | Error mapping includes unsupported repo, absent CLI, auth, rate-limit, timeout, decode, command failure. | verified / local_source | `crates/engine/src/source_control.rs:63-82,198-239` | 2026-09-27T16:03Z | Typed `ChangeRequestError` variants; process result mapping. | Static declared handling, not evidence these conditions were exercised. Coordinator. |
| L-MCP-01 | Zeron MCP | MCP advertises tools and dispatches `tools/call` only for catalogued tool names; unknown names produce invalid params. | verified / local_source | `crates/mcp/src/jsonrpc.rs:124-179`; `crates/mcp/src/tools.rs:30-40,57-...` | 2026-09-27T16:03Z | `tools/list`, `tools/call`, `tools.has`; no profile/workflow authorization check at this transport dispatch boundary. | Do not conclude no checks exist elsewhere; anchor and direct implementation ownership only. Coordinator. |
| L-MCP-02 | Zeron MCP documented tool surface | MCP proxies tools to local engine; documented tool table includes read and mutating chat operations. | verified / local_source | `docs/mcp.md:3-12,58-74` | 2026-09-27T16:03Z | `create_chat`, `send_message`, `interrupt_chat`, `archive_chat` among catalog. | Documentation statement, not runtime. Profile/workflow action authorization is not established by this document. Coordinator. |
| GH-DOC-01 | GitHub REST API | GitHub's official pull-request REST reference identifies list/get/edit/create/merge; reference URL's API version is `2026-03-10`; list supports `state`, `head`, `per_page` max 100/page; endpoint-specific permissions and statuses documented. | verified / official_doc | `https://docs.github.com/en/rest/pulls/pulls?apiVersion=2026-03-10`, “REST API endpoints for pull requests”, “List pull requests”, “Create a pull request”; API version 2026-03-10 | 2026-09-27T16:01Z | GET `/repos/{owner}/{repo}/pulls`; 200/304/422. Create POST triggers notifications; 201/403/422 and write access conditions. | Docs only. Not equivalent to local `gh` invocation, not proof external state is acceptance. Coordinator. |
| GH-DOC-02 | GitHub REST auth | Official auth page documents token authentication and endpoint-specific permissions/scopes; missing/insufficient auth can return 404/403, invalid credentials 401. | verified / official_doc | `https://docs.github.com/en/rest/authentication/authenticating-to-the-rest-api?apiVersion=2026-03-10`, “About authentication”, “Personal access tokens”; API version 2026-03-10 | 2026-09-27T16:02Z | Fine-grained token permissions are specified by endpoint reference; classic tokens use scopes. | No credentials created or supplied; auth method used by `gh` at runtime unknown. Coordinator. |
| GH-DOC-03 | GitHub pagination/rate/retry | Endpoint page documents paging params. API-wide precise rate/retry policy and idempotency semantics not captured in the two examined pages. | unknown / official_doc | GH-DOC-01 plus `https://docs.github.com/en/rest/authentication/authenticating-to-the-rest-api?apiVersion=2026-03-10`; pages listed above | 2026-09-27T16:02Z | Only endpoint pagination documented in captured evidence. | Must consult dedicated official rate-limit/pagination guidance in a separately bounded follow-up before implementation policy; no inferred retries/idempotency. Coordinator. |
| ADO-DOC-01 | Azure DevOps Services Git Pull Requests REST API | Official Microsoft Learn reference names Git service, API version 7.1, and create/retrieve/modify operations; lists other versions, including Services 7.2 and Server versions. | verified / official_doc | `https://learn.microsoft.com/en-us/rest/api/azure/devops/git/pull-requests?view=azure-devops-rest-7.1`, “Pull Requests”, “Operations”; 7.1 | 2026-09-27T16:02Z | API describes create, get, get by id, get lists, update; update fields include status/title/description/completion and merge options. | Documentation only, not tenant/provider access. This narrow page does not establish auth details, pagination, rate/retry, idempotency, work-item authority, or remote-only behavior. Coordinator. |
| ADO-ID-01 | “ADO” / deployment identity | Product shorthand in change is not enough to identify a specific Azure DevOps organization, deployment (Services vs Server), project, or approved authority. | unknown / official_doc | ADO-DOC-01 identifies product family/API versions only | 2026-09-27T16:02Z | Several Services/Server API versions exist. | No organization/tenant normalization; no Brown endpoint access. Coordinator. |
| TS-AP-01 | Aperture by Tailscale | Official Tailscale documentation identifies Aperture as a centralized AI gateway; routes LLM requests and proxies external MCP/HTTP connectors, not itself an issue/workflow system in the cited pages. | verified / official_doc | `https://tailscale.com/docs/aperture`, “Aperture”; validated 2026-07-24; `https://tailscale.com/docs/aperture/how-aperture-works`, “Outbound integrations”, validated 2026-07-24 | 2026-09-27T16:03Z | Gateway routes model requests; connectors proxy remote MCP/API and inject configured auth. | Does not establish any local deployment, configured connector, workflow authority, API version, or access grant. Coordinator. |
| TS-AP-02 | Aperture data/auth boundary | Official “How Aperture works” describes Tailscale identity, configured connector credentials, and telemetry capture including request/response bodies subject to retention configuration. | verified / official_doc | `https://tailscale.com/docs/aperture/how-aperture-works`, sections “Identity and authentication”, “Telemetry capture”, “Outbound integrations”; validated 2026-07-24 | 2026-09-27T16:03Z | Gateway-mediated connections; telemetry captures request/response content; connector credentials configured centrally. | Product documentation only. Do not infer this profile's actual configuration or data handling. Coordinator. |
| TS-AP-03 | Tailscale/Aperture API/version/workflow | API version, supported workflow/issue operations, retry/idempotency semantics, and external planning/review authority are not established by the cited Aperture overview/reference. | unknown / official_doc | TS-AP-01/02; `https://tailscale.com/docs/aperture/reference?_rsc=qjuky`, “Aperture reference”, validated 2026-06-16 | 2026-09-27T16:03Z | Reference catalog covers configuration, providers, connectors, CLI; no identified project workflow API in examined material. | Search was bounded; no absence claim or Tailscale workflow parity. Coordinator. |
| TS-NET-01 | Tailscale transport | Official Tailscale KB states device traffic is end-to-end encrypted and private keys do not leave devices. | verified / official_doc | `https://tailscale.com/kb/1093/can-tailscale-decrypt-my-traffic`, “Can Tailscale decrypt my traffic?”, validated 2024-06-18 | 2026-09-27T16:03Z | “All traffic is end-to-end encrypted, always.” | Transport security only; grants no workflow authority, endpoint permission, or Brown access. Coordinator. |
| AUTHORITY-01 | External source of truth | Which GitHub/ADO/Aperture deployment is authoritative for planning, review, spec, or acceptance in this product context is not established by the bounded official documentation and permitted source anchors. | unknown / official_doc + local_source | GH-DOC-01, ADO-DOC-01, TS-AP-01/03; `docs/fork-prd.md:52-55,72-75`; execution map `openspec/changes/prd-execution-map/design.md:37` | 2026-09-27T16:03Z | PRD preserves external reviewer/planning/OpenSpec authority and says ZF labels are not runtime IDs; execution map requires provider-specific reviewed child changes. | Requires named authority decision; external Done cannot establish local acceptance. Coordinator. |
| REMOTE-01 | Remote-only repository | Existing resolver requires checkout context and checkout root, but official docs inspected do not answer whether the product should support a repository with no local materialization. | unknown / local_source + official_doc | `crates/engine/src/source_control.rs:48-54,95-107,125-157,198-221`; GH-DOC-01/02 | 2026-09-27T16:03Z | Current code is checkout-based. | Report implementation limitation; do not set local checkout as product policy. Coordinator. |

## Local behavior records

| operation | input | source_span | authority_check | side_effect | failure_result | current_limit |
|---|---|---|---|---|---|---|
| Inspect checkout | cwd | `crates/engine/src/source_control.rs:95-107,125-142` | Git metadata availability, not profile/workflow permission | Local subprocesses via inspector | `RepositoryUnavailable` and typed errors | Requires local checkout. |
| Resolve GitHub PR summary | `CheckoutSourceContext` with host/owner/repo/branch selectors | `crates/engine/src/source_control.rs:145-157,183-239,281-317` | Repository identity presence; no profile/workflow gate visible here | `gh` process can access provider; this task did not invoke it | Typed `ChangeRequestError` incl auth/rate/timeout/decode/command | GitHub-only implementation; 20 result cap; no ADO parity. |
| MCP list/call | JSON-RPC method/name/arguments | `crates/mcp/src/jsonrpc.rs:124-179`; catalog `crates/mcp/src/tools.rs:57-...` | Method and tool-name existence at dispatcher; profile/workflow enforcement not shown at this layer | Depends on selected engine tool; some are mutating | JSON-RPC invalid params / tool error | This surface is local engine control, not an external provider authority. |

## Child adapter research records

These are provisional research records, not runtime DTOs, selected APIs, or implementation authorization. `write_operations` is explicitly not authorized. `unknown` is retained where docs do not establish behavior.

### GitHub REST follow-up
```yaml
adapter_id: github-rest-research-candidate
system_identity: GitHub REST API, GitHub Inc.; official docs name REST API endpoints for pull requests
supported_versions: documented endpoint version 2026-03-10; product deployment/enterprise host unknown
capability: documented PR list/get/create/edit/merge endpoints; not chosen for Zeron
owner_boundary: GitHub owns provider PR state; Zeron owns local output verification and acceptance
inputs_and_scope: documented owner/repo/pull number/head/state/page parameters; actual scope unknown
outputs_and_states: documented PR resource/state and endpoint HTTP statuses; local acceptance states unknown
native_id: PR number and API resource id documented
start_proof: unknown
stop_proof: unknown
status_proof: provider PR state only; cannot prove local output acceptance
configuration_source: unknown
auth_boundary: token with endpoint-specific permissions; local gh auth mechanism runtime unknown
data_boundary: API request/response fields per docs; actual deployment boundary unknown
isolation_boundary: unknown
read_only_operations: documented list/get
write_operations: not authorized
failure_and_retry_behavior: endpoint statuses documented; API-wide retry/idempotency behavior unknown
compatibility: no parity with ADO or local gh behavior established
evidence_refs: [GH-DOC-01, GH-DOC-02, GH-DOC-03, L-GH-01, L-GH-02]
rejection_reasons: no authority/deployment decision; no validated complete rate/failure contract; no runtime verification
decision_state: needs_review
```

### Azure DevOps follow-up
```yaml
adapter_id: azure-devops-git-pr-research-blocked
system_identity: Azure DevOps Services Git Pull Requests REST API (Microsoft Learn); specific org/deployment unknown
supported_versions: 7.1 page inspected; docs list 7.2, 7.0 and Server versions; target unknown
capability: reference documents Git PR create/retrieve/modify
owner_boundary: provider owns PR state; Zeron acceptance authority remains separate
inputs_and_scope: project/repository/PR filter scope unknown for intended use
outputs_and_states: pull-request result; detailed status authority unknown
native_id: pull request identifier implied by operations; exact chosen identity field unknown
start_proof: unknown
stop_proof: unknown
status_proof: provider PR status only; local acceptance unknown
configuration_source: unknown
auth_boundary: unknown; no credentials inspected or used
data_boundary: unknown for intended deployment
isolation_boundary: unknown; no tenant/profile access
read_only_operations: get/list documented
write_operations: not authorized
failure_and_retry_behavior: unknown from inspected page
compatibility: no GitHub parity inferred; Azure DevOps Services vs Server deployment unresolved
evidence_refs: [ADO-DOC-01, ADO-ID-01, AUTHORITY-01]
rejection_reasons: target deployment and authority unclear; auth, rate, pagination, retry/idempotency and failure semantics unresearched
decision_state: blocked
```

### Tailscale/Aperture follow-up
```yaml
adapter_id: tailscale-aperture-gateway-research-blocked
system_identity: Aperture by Tailscale, documented centralized AI gateway with MCP/HTTP connectors
supported_versions: docs validated 2026-07-24; exact runtime/API version unknown
capability: gateway/connectors for LLM, MCP, HTTP traffic; no planning/review workflow capability established
owner_boundary: Tailscale/Aperture transport/gateway; upstream service owns its workflow state
inputs_and_scope: connector requests; exact local connector and grants unknown
outputs_and_states: proxied upstream result; workflow states unknown
native_id: unknown
start_proof: unknown
stop_proof: unknown
status_proof: gateway/connector response only; no workflow authority proven
configuration_source: product docs describe centralized config; local source/config not allowed/inspected
auth_boundary: Tailscale identity and centrally configured connector credentials described; actual grant unknown
data_boundary: docs describe request/response telemetry and retention config; actual deployment unknown
isolation_boundary: no actual tailnet or profile access established
read_only_operations: unknown for any named issue/review system
write_operations: not authorized
failure_and_retry_behavior: unknown for workflow operations
compatibility: transport/connectivity does not imply workflow authority or GitHub/ADO parity
evidence_refs: [TS-AP-01, TS-AP-02, TS-AP-03, TS-NET-01]
rejection_reasons: no concrete upstream product/connector or workflow authority; no operation contract
decision_state: blocked
```

## Scenario coverage

| scenario_id | state | evidence_refs | reason | remaining_question |
|---|---|---|---|---|
| C01 | verified | L-MCP-01, L-MCP-02 | MCP tool available but action outside profile/workflow scope: unavailable for that action. Dispatcher checks tool existence; profile/workflow gate is not established in permitted anchors. Do not claim enforced behavior absent evidence. | Where is authoritative profile/workflow gate implemented and how does it deny this action? |
| C02 | verified | AUTHORITY-01, L-GH-02 | External issue says Done while local output unverified: no acceptance transition. External status cannot substitute for local output verification. | Exact future acceptance gate belongs to separately scoped change. |
| C03 | verified | REMOTE-01, L-GH-01 | Remote repository cannot be materialized locally: report capability limitation, not require local storage as product policy. Current code requires checkout context; product policy remains unknown. | Should remote-only support be a separate capability? |
| C04 | blocked | ADO-ID-01, ADO-DOC-01 | ADO/Brown endpoint discovered: no access attempt solely because Brown profile exists. No endpoint accessed; specific deployment/authority unknown. | None for this task; future access requires separate explicit authorization. |
| Unknown prerequisite | blocked | AUTHORITY-01, ADO-ID-01, TS-AP-03 | Unknown prerequisite or acceptance result blocks with reason, not silent success/reroute. | Name prerequisite and its acceptance evidence before implementation. |

## PRD clause coverage

| clause | evidence | research disposition |
|---|---|---|
| ZF-19 | GH-DOC-01/02/03, ADO-DOC-01, TS-AP-01/02/03, L-GH-01/02 | GitHub behavior and product identities bounded; ADO/Aperture operation/authority gaps explicit. No interface selected. |
| ZF-07 | `docs/fork-prd.md:72-75`; AUTHORITY-01 | Delivery actions individually callable under workflow/stage authority; research grants no delivery authorization. External Done does not prove acceptance. |
| ZF-02 | `docs/fork-prd.md:52-55`; C04 | Brown support grants no Brown-system access; no profile/account substitution or access occurred. |
| External reviewer/planning/OpenSpec authority | `docs/fork-prd.md:52-55`; `openspec/changes/prd-execution-map/design.md:37`; AUTHORITY-01 | Preserve authority; exact provider owner for this context remains unknown. |

## Bounded-search omissions and access boundary

Official pages inspected: GitHub PR endpoint and auth reference; Microsoft Learn Azure DevOps Git PR reference; Tailscale Aperture overview, how-it-works, reference, and Tailscale traffic encryption FAQ. Search surfaced official GitHub rate/pagination pages and ADO auth/rate/version pages but they were not opened; those details remain unknown. No official docs established a specific ADO organization, Aperture connector deployment, or remote-only product policy. No provider API calls, credentials, private access, endpoint probes, Brown resources, writes, installations/configuration, or commits occurred. Firecrawl CLI was available/authenticated, but its help did not establish controls to validate DNS and every redirect hop; it was not used for URL fetches. Public official-doc search/fetch used the built-in public web research interface, not provider APIs.

## Bounded discovery stop rule
For each named subject/question inspect the official documentation entry point and one relevant official reference page, plus listed local anchors and their direct callers. Stop once an authoritative source answers that question. If two relevant official pages do not establish the claim, record unknown with exact searched sources, not a guessed interface. Missing/denied required source is blocked. Conflicting authoritative sources require escalation rather than optimistic choice. A later separately scoped research iteration may widen search; this budget is a research stopping rule, not proof of absence. Unknown product identity stays unknown without normalizing spelling. Persist rows in this design, never only disposable scratch.
