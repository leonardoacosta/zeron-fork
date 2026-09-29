# Agent integrations exploration

Date: 2026-09-29. Status: exploration only, not implementation approval.
Baseline: `136e812`. The working tree was clean when inspected, despite the earlier session snapshot listing modifications.

## Intent and outcome

Remove Devin, Grok, and Antigravity from supported providers, make Jcode a first-class ACP agent, provide a global/project skill viewer, integrate MCP, and expose gateway/model metrics. Four parallel investigations covered these five areas. No application code was changed or runtime integration claimed.

ACP connects a client application to a coding agent. MCP connects an agent to tools and data. A provider catalog, an account quota display, and a durable per-model usage ledger are separate concerns.

## Internal prior art and constraints

- `openspec/README.md:3-17` requires refinement and review before named implementation. Existing roadmap approval is not blanket execution approval.
- `openspec/changes/integration-provider-adapters/proposal.md:3-19` is a discovery contract with a closed implementation gate. It requires concrete adapter contracts and engine authorization for MCP exposure.
- Active changes include harness research, profile access enforcement, preflight binding, resource accounting, and provider adapters. No `openspec/changes/archive` directory was present. This exploration must not silently authorize those changes or replace their task ledger.
- Retrieved memory says global Jcode customizations belong under `~/.jcode`, not this repository. This is a preference, not evidence of Jcode's actual skill discovery paths. This document is repository planning, not a global customization.

## Current state and proposed boundaries

### 1. Remove providers without corrupting history

`crates/proto/src/agent.rs:5-28` serializes `HarnessId` using kebab-case strings and includes Devin, Grok, and Antigravity. Removing variants outright risks decoding older persisted or synchronized records. Jcode is absent from this enum, and an indexed search for `jcode` returned no hits.

Recommended boundary: stop advertising, installing, authenticating, and launching the three providers while retaining explicit legacy decoding. Historical chats should remain readable. Attempting to resume a retired provider should explain that it is unavailable, not silently select another agent. Existing credentials should not be deleted as a side effect.

Refinement must enumerate enum consumers, catalogs, account usage/auth paths, platform installation logic, desktop/mobile pickers, docs, and tests before deletion. Removal of a coding harness must not accidentally block similarly named upstream model IDs accessed through another agent.

### 2. Jcode as a first-class ACP harness

Reuse the existing ACP transport rather than creating another agent runner. First-class means a stable harness identity, executable detection, truthful readiness/auth state, catalog and model selection, session creation/resume, streaming, cancellation, permission handling, skill integration, and desktop/mobile visibility. Capabilities must come from a pinned tested Jcode version, not assumptions based on another ACP agent.

Critical source boundary: `crates/harness/src/acp/mod.rs:2986-3026` initializes ACP and supplies the same session parameters to new/load. Current parameters contain an empty `mcpServers` array. Existing resume failure may start a fresh session with an error event, so the Jcode contract must explicitly cover this behavior.

Gap: bundled Jcode documentation searches did not establish the executable arguments, ACP version, authentication mechanism, or supported MCP and usage capabilities. Pin those through actual Jcode documentation and an authorized harmless handshake before promising compatibility. Do not infer that a plausible command name is a verified launch contract.

### 3. Host-scoped global and project skill viewer

Discovery already exists. `crates/harness/src/skills.rs:108-213` defines provider roots, user/global roots, project traversal, and precedence. `crates/engine/src/rpc.rs:2054-2083` exposes `ListSkills`. `docs/harness-skill-completion.md:65-73` documents selected-host discovery and ACP command binding. This is a composer catalog, not a dedicated scoped browser.

Recommended first slice: a read-only viewer using the existing engine discovery path, with selected host, harness, and project shown explicitly. Display scope, provenance, effective versus shadowed status, description, and content availability. Preserve the existing completion behavior. A global view must work without pretending an arbitrary current directory is the project.

Do not infer scope solely from a display path. Decide whether to extend the response with provenance or add an inventory view because the effective catalog may discard shadowed entries. Native advertised skills can lack readable local files. Canonicalize content reads against approved discovered roots, define symlink behavior, bound file size and scan work, and never open a remote-host path on the local machine by mistake. Treat skill Markdown as untrusted content.

Worker-located regression anchors for refinement: `crates/harness/src/skills.rs:699-916` and `crates/engine/tests/rich_composer_delivery.rs:415-474`. Revalidate these before editing.

### 4. MCP integration has two directions

`docs/mcp.md:1-28` documents the existing `zeron mcp` stdio server, which exposes engine operations through localhost IPC and carries originating chat identity. This is outward exposure of Zeron, not evidence that users can attach arbitrary MCP servers to agents.

The inbound gap is concrete: `crates/harness/src/acp/mod.rs:2994` passes `mcpServers: []` to session setup. Recommended scope is a host-local server inventory and approved server handoff to capable ACP agents, beginning with Jcode after its contract is verified. Do not build a second MCP execution runtime in Zeron if the agent already owns connections.

Separate metadata visible to the UI from host-local secrets. Project configuration is untrusted executable input. Discovery must not launch commands, install packages, provision credentials, or contact configured endpoints. Approval must bind to host, project, command/arguments or endpoint, and configuration revision. Reject unsupported transport capabilities explicitly. Define whether changes apply only to new sessions or require reconnecting existing sessions.

Existing Zeron MCP exposure should continue through engine authorization. Project MCP ingestion must not become an authorization bypass. Configuration discovery, health checks, and tool execution are distinct actions with distinct consent requirements.

### 5. Gateway/model metrics need a data contract first

Verified evidence:

- `crates/harness/src/claude/catalog.rs:199-221` uses `gateway/model` in a settings test. This is not proof of an integrated gateway service.
- `crates/doc/src/schema.rs:46-62` stores optional assistant-turn `duration_ms`, absent for live streams and older documents. It is wall-clock turn duration, not necessarily upstream model latency.
- `crates/harness/src/acp/mod.rs:2438-2454` normalizes optional token usage and defaults an absent counterpart to zero. This loses missing-versus-zero information relevant to metrics.
- Worker investigation identified account quota/cache fields in `crates/engine/src/agent_accounts.rs:480-507,581-599`. Quota windows are not billable request totals.

Recommended interpretation pending confirmation: metrics for model calls made through configured agent/gateway routes, not deployment of a new gateway. A truthful first display can show completed-turn counts and observed duration with coverage. Model grouping requires an immutable model/provider snapshot at the measured turn, not today's chat selection. Token and cost totals require durable usage provenance first.

Do not label wall-clock duration as provider latency, infer cost from quota, count missing data as zero, or conflate selected and actually routed models. Before collecting new metrics, specify request/attempt IDs, retry and continuation accounting, cancellation/failure semantics, reported versus estimated usage, effective model identity, retention, and redaction. Never collect prompt/tool bodies merely to produce aggregate metrics.

## External evidence

Context7 was consulted for explicitly required ACP and MCP:

- `/agentclientprotocol/agent-client-protocol`: schema/documentation confirms `session/new` carries `cwd` and `mcpServers`. Results also mixed protocol v2 and transport proposals, so this supports the architectural pattern, not compatibility with the repository's current negotiated version. Reference: https://github.com/agentclientprotocol/agent-client-protocol/blob/main/schema/v2/schema.json
- `/modelcontextprotocol/modelcontextprotocol`: security guidance explicitly identifies malicious local-server startup commands. Authorization guidance rejects token passthrough. Reference: https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/docs/2026-07-28/tutorials/security/security_best_practices.mdx

No external credentials, installations, server launches, or writes were performed. Version-pinned Jcode ACP evidence remains missing.

## Adversarial findings and alternatives

| Decision | Rejected shortcut | Recommendation and trade-off |
| --- | --- | --- |
| Provider removal | Delete serialized variants immediately | Retire execution while preserving legacy reads. Leaves a small compatibility surface. |
| Jcode integration | Copy another ACP provider's capabilities | Reuse transport, verify capabilities independently. Requires a real versioned acceptance probe. |
| Skill viewer | Duplicate filesystem discovery in UI | Extend engine inventory/provenance. May require a response-contract change. |
| MCP ownership | Build a second general-purpose tool runtime | Let the ACP agent own connections. Makes support dependent on truthful agent capabilities. |
| Metrics | Derive spend/latency from quota and turn duration | Persist missing provenance first. Initial dashboard has fewer but defensible metrics. |

Additional risks: retired IDs arriving from older clients, host switches during skill loading, stale async results crossing project boundaries, symlink escapes, remote/offline hosts, oversized Markdown, terminal-only authentication, ACP resume incompatibility, secrets in synchronized state, project command execution without approval, retry double counting, and stale model catalogs. UI acceptance must include keyboard access, scope labels that do not rely on color, loading/empty/error states, and accessible content navigation.

## Decisions and user-only actions

Nonblocking recommended defaults: read-only skill viewing, backward-readable provider retirement, ACP reuse, agent-owned MCP connections, and no invented metrics.

Resolve during feature refinement:

1. Does “gateway” name a specific service such as an existing local gateway, or mean any configured model route? Its identity determines required APIs and credentials.
2. Does MCP mean attaching external servers to Jcode, exposing Zeron to external agents, or both? Recommended new work is the former while preserving existing exposure.
3. Confirm initial platform coverage and whether legacy retired-provider chats must remain resumable. Recommended behavior is readable but not resumable.
4. Pin the supported Jcode build, install/auth path, ACP behavior, and which capabilities it actually exports.

Only the user or an authorized operator should approve credentials, paid requests, remote endpoints, or execution of project-supplied MCP commands. No password reset, credential cleanup, publication, deployment, or spend is authorized by this exploration.

## Recommended next step and verification concerns

Route to feature authoring as bounded contracts: provider retirement compatibility, Jcode ACP integration, scoped skill inventory/viewer, ACP MCP configuration/handoff, and model telemetry/metrics. Share protocol/provenance contracts where necessary but avoid one all-or-nothing rewrite. Keep existing OpenSpec prerequisite and approval gates explicit.

Verification must include legacy serialization fixtures and old-client inputs, fake ACP lifecycle/cancel/auth tests, one real harmless Jcode new/resume workflow, selected-host skill scope/collision/symlink tests, new/load MCP configuration equivalence with consent and secret-redaction checks, and replay-safe metrics aggregation with absent usage and retries. Rust implementation must run README formatting/Clippy gates and focused crate tests. Desktop and mobile UI checks need their actual supported runners.

Exploration validation: current source spans and repository documentation were inspected and workers' main claims were checked against current source. `git diff --check` passed, and a local script verified 16 referenced paths and document trailing whitespace. Concurrent changes appeared in `crates/engine/src/doc_host.rs` and `crates/harness/tests/fixtures/fake-claude.sh` during investigation and were left untouched. No application source changes, runtime tests, or GitHub Actions results are claimed.
