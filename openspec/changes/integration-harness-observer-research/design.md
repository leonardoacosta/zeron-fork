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

## Filled source-evidence example
Verified against actual source at stated commit; concurrent unrelated working-tree edits are not runtime evidence.
```json
{
  "claim_id": "local-harness-controls",
  "subject": "zeron_harness::RunControls",
  "claim": "Shared controls declare a CancellationToken interrupt; provider-specific actual stop is not established.",
  "state": "verified",
  "evidence_kind": "local_source",
  "source_or_command": "crates/harness/src/lib.rs:49-62",
  "version_or_commit": "b9623ae80225b924fe00d577d600f65938967bf6",
  "observed_at_utc": "2026-09-26T19:56:18Z",
  "result_or_excerpt": "pub interrupt: CancellationToken;",
  "scope": "Read-only source declaration, not runtime acceptance",
  "limitations": "No native/provider invocation or descendant-stop proof.",
  "reviewer": "coordinator source verification"
}
```

## Bounded discovery stop rule
For each named subject/question inspect the official documentation entry point and one relevant official reference page, plus listed local anchors and their direct callers. Stop once an authoritative source answers that question. If two relevant official pages do not establish the claim, record unknown with exact searched sources, not a guessed interface. Missing/denied required source is blocked. Conflicting authoritative sources require escalation rather than optimistic choice. A later separately scoped research iteration may widen search; this budget is a research stopping rule, not proof of absence. Unknown product identity stays unknown without normalizing spelling. Persist rows in this design, never only disposable scratch.

## Evidence register

Retrieved 2026-09-27 UTC using Firecrawl CLI 1.23.3. CLI status showed authenticated stored credentials; no key exposed. Each URL was HTTPS, DNS-resolved immediately before fetch, all A/AAAA answers checked globally routable, fetched with direct no-shell argv and `--lockdown`. Search results were discovery only. Redirect-hop validation cannot be independently inspected/constrained by this CLI, so sources remain bounded with that limitation. No provider calls, private access, local probes, credentials, install/configuration changes, process control, or writes. Source evidence below is static only. Current checkout commit was not captured; no baseline commit is represented as current.

### Evidence rows

| claim_id | subject | claim | state | evidence_kind | source_or_command | version_or_commit | observed_at_utc | result_or_excerpt | scope | limitations | reviewer |
|---|---|---|---|---|---|---|---|---|---|---|---|
| jcode-identity | Jcode | Official public repo identifies project as `jcode`. | verified | official_doc | https://github.com/1jehuang/jcode repository heading | latest displayed commit `232e49238b8423779c831399e2b20769eb95b7e1` | 2026-09-27T16:02:30Z | “1jehuang / jcode”; public repository | Project identity | Does not establish local swarm integration or API. | coordinator |
| jcode-swarm-contract | Jcode local swarm | Exact version/platform, start/status/stop, native ID, config, auth/data and isolation contract not established by bounded official-page inspection. | blocked | official_doc | Firecrawl search `Jcode CLI local swarm official docs`; https://github.com/1jehuang/jcode | Page latest commit above; no version contract pinned | 2026-09-27T16:02:30Z | Entry page fetched; no qualifying local-swarm control contract captured. | Proposed environment-local swarm | No local command/version/process probe authorized. Search included nonofficial results, not used as evidence. | coordinator |
| herdr-identity | Herdr | Official docs describe Herdr as a terminal workspace/runtime for coding agents. | verified | official_doc | https://herdr.dev/docs/ “Pick your path”, “Core guides”; https://herdr.dev/docs/agents/ “Agents” | Current public docs, version not shown | 2026-09-27T16:02:51Z; 16:03:00Z | “Each agent stays in a real terminal pane”; pane state tracked and rolled up. | Product identity/concepts | No Jcode compatibility established. | coordinator |
| herdr-controls | Herdr attachment | Docs describe local socket API/CLI operations including `agent.list`, `agent.wait`, `agent.start`, `pane.read`, `server.stop`; detach preserves processes, server restart ends pane processes. | verified | official_doc | https://herdr.dev/docs/socket-api/ “Socket API”, “What you can control”, “Raw methods”; https://herdr.dev/docs/session-state/ “What survives” | Current docs; installed binary/API version unknown | 2026-09-27T16:03:00Z | API can “inspect or control a running session”; method list includes read and mutating operations. | Documented Herdr control surface | No calls executed; no target-scoped stop, native identity binding, auth/data/security or isolation proof for proposed attachment. | coordinator |
| systemone-jev | SystemOne observer / Jev | TypeSafe identifies Jev as its first public System One Model, available in early access; this does not identify it as the requested SystemOne observer. | verified | official_doc | https://typesafe.ai/ FAQ; https://typesafe.ai/blog/introducing-system-one-models-and-jev, “Introducing System One Models & Jev” | Announcement dated 2026-09-15 | 2026-09-27T16:03:09Z | “our first System One Model: Jev”; “available today in early access”; typed decisions/probabilities. | Identity distinction only | API version, controls and security boundary not researched/verified. | coordinator |
| laya-identity | Laya | Official identity/capabilities unknown. | unknown | official_doc | Firecrawl search `Jev Laya empryo software official`; no official Laya page opened | unknown | 2026-09-27T16:02:41Z | Search results were third-party; no authoritative source identified. | Exact supplied name | Bounded search is not proof of absence. | coordinator |
| empryo-identity | empryo | Exact spelling `empryo` remains unknown; no normalization. | unknown | official_doc | Firecrawl search `Jev Laya empryo software official`; no official page for exact name identified | unknown | 2026-09-27T16:02:41Z | No authoritative source established in bounded search. | Exact spelling only | Not evidence of nonexistence. | coordinator |
| zeron-harness-source | Zeron harness | `RunControls` declares a `CancellationToken`; comments describe protocol interrupt and child escalation. | verified | local_source | `crates/harness/src/lib.rs:49-61,77-104` | current checkout; exact commit not captured | 2026-09-27T16:00:45Z | `pub interrupt: CancellationToken;` and `Harness` trait. | Static local declaration | Not provider-specific or runtime stop proof. | coordinator |
| zeron-registry-source | Zeron registry | Registry owns per-device harness enablement persisted in `{data_dir}/harness-prefs.json`. | verified | local_source | `crates/engine/src/registry.rs:1-8,19-40,87-99` | current checkout; exact commit not captured | 2026-09-27T16:00:45Z | “owns the device's harness ENABLEMENT”; persisted preferences. | Static local source | No external observer ownership or integration proof. | coordinator |
| zeron-session-interrupt-source | Zeron session | `SessionsEngine::interrupt` signals cancellation, calls harness token, and waits boundedly for settlement. | verified | local_source | `crates/engine/src/sessions.rs:620-653` | current checkout; exact commit not captured | 2026-09-27T16:03:12Z | `token.cancel()` then polls up to 500 × 10ms. | Static local flow | Does not prove external process identity or stop. | coordinator |

### Scenario records

| scenario_id | state | evidence_refs | reason | remaining_question |
|---|---|---|---|---|
| C01 | blocked | jcode-swarm-contract, herdr-controls, zeron-harness-source, zeron-session-interrupt-source | A tool is installed but no stop proof/API exists: capability remains blocked. Herdr docs list controls, but no authorized target-bound operation or Jcode compatibility proof exists. | Can separately authorized evidence bind a stop result to the exact process/session and pinned version? |
| C02 | blocked | jcode-swarm-contract, herdr-controls | Documentation and observed version disagree: record mismatch and do not guess request shape. Here no local version was observed, so there is no basis to invent a request shape. | Which separately authorized installed version matches the official schema? |
| C03 | unknown | jcode-swarm-contract, zeron-registry-source | Jcode preferred but unavailable leaves ordinary configured engineer unchanged. No live availability check or registry/config change was made, so runtime behavior is not verified. | Does an authorized implementation preserve configured engineer selection when Jcode is unavailable? |
| Unknown prerequisite | blocked | jcode-swarm-contract, herdr-controls, systemone-jev, laya-identity, empryo-identity | Unknown prerequisite: affected work is blocked with reason, not reported successful or rerouted. | Obtain separately authorized evidence for unresolved identity/version/control boundaries. |

### Child adapter decision records

No candidate selected. `write_operations` are not authorized. Unknown fields remain unknown.

| adapter_id | system_identity | supported_versions | capability | owner_boundary | inputs_and_scope | outputs_and_states | native_id | start_proof | stop_proof | status_proof | configuration_source | auth_boundary | data_boundary | isolation_boundary | read_only_operations | write_operations | failure_and_retry_behavior | compatibility | evidence_refs | rejection_reasons | decision_state |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| jcode-local-swarm-research | Jcode project `1jehuang/jcode`; integration unknown | unknown | Environment-local specialist swarm | Jcode runtime vs Zeron owner boundary unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown | not authorized | unknown | unknown | jcode-identity,jcode-swarm-contract | No pinned integration version, API, native ID, stop/status or isolation proof; no local probe authorized. | blocked |
| herdr-attachment-research | Herdr terminal runtime/local socket API documented | unknown | Possible pane/session observation or attachment | Herdr owns server/panes; Zeron authority boundary unknown | unknown | Agent/pane states documented; exact contract unknown | Pane IDs such as `w1:p1` documented, no target binding proof | `agent.start` documented, not executed | `server.stop` documented, not target-scoped proof | State methods documented, not observed | Herdr docs/local config; exact values unknown | Local socket boundary documented; security/auth details unknown | Pane history may contain secrets/tokens per session-state docs | unknown | No calls performed | not authorized | unknown | Installed schema/version unknown | No version pin, compatibility, target-scoped stop, identity/auth/data/isolation proof. | blocked |
| systemone-observer-research | Observer identity unknown; not equated with TypeSafe model | unknown | ZF-09 proposal/conflict observation | Observer grants no authority; ownership unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown | not authorized | unknown | unknown | systemone-jev | Jev source identifies a model, not this observer/API. | blocked |
| jev-research | TypeSafe Jev; first public System One Model, early access | API version unknown; early access announcement 2026-09-15 | Typed probabilistic decisions at description level | Provider/model vs observer authority unknown | unknown | Typed decisions/probabilities described; no response contract pinned | unknown | unknown | unknown | unknown | Official docs linked but not inspected | unknown | unknown | unknown | unknown | not authorized | unknown | API docs/version unresolved | systemone-jev | No adapter controls, native ID, boundaries, isolation or observer equivalence. | blocked |
| laya-research | Exact name `Laya`; identity unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown | not authorized | unknown | unknown | laya-identity | No official identity established. | blocked |
| empryo-research | Exact name `empryo`; identity unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown | not authorized | unknown | unknown | empryo-identity | Exact spelling retained; no official identity established. | blocked |

### Authority and unresolved decisions

| item | disposition | evidence / issue |
|---|---|---|
| ZF-15 | Jcode preference is not readiness. No silent substitution or isolation downgrade. | `docs/fork-prd.md:104-106`; jcode-swarm-contract, herdr-controls. |
| ZF-09 | Keep SystemOne observer distinct from engineering harness and Jev model; observer grants no authority. | `docs/fork-prd.md:80-82`; systemone-jev. Observer identity unknown. |
| ZF-19 | Exact APIs, versions and capabilities require evidence. | `docs/fork-prd.md:120-123`; citations above. |
| `ci-promotion-gates` | Hard prerequisite remains unresolved for promotion; no hosted/CI acceptance claim. | `openspec/changes/ci-promotion-gates/design.md:26-35`. |
| Exclusions | No credentials, private access, installation, config changes, provider API calls, process control, spend or writes. | No such actions performed. |
| Unresolved | Jcode swarm contract; Herdr-Jcode compatibility/security and target stop proof; observer identity; Jev API boundary; Laya and exact `empryo` identity; version mismatch; isolation. | Remain blocked/unknown; require separate authorization and bounded research. |
