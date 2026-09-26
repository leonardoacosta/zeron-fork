# Profile authorization: exact enforcement map

Status: proposed; existing effect paths inspected, full code task refinement still required. No source implementation in this planning iteration.

## Existing anchors
- `crates/engine/src/rpc.rs`: handle performs device forwarding then local method match; repo/file/account/terminal actions bypass SessionsEngine.
- `crates/engine/src/sessions.rs`: dispatch_inner, steer and drive_run are distinct agent-effect boundaries.
- `crates/engine/src/agent_accounts.rs`: device-global CLI credential stores, list/activate/forget/login operations.
- `crates/engine/src/repos.rs`: raw path read/mutation and worktree processes.
- `crates/engine/src/terminals.rs`: open/write/subscribe/resize/close terminal IDs are process capabilities, not authorization tokens.
- `crates/harness/src/lib.rs`: Harness::run starts execution; preflight alone does not guard actual call.
- `crates/engine/tests/local_profiles.rs`: existing transport-scope tests, must extend with named-profile grants.
- Additional exact callers: `crates/engine/src/doc_host.rs` dispatch_queued/dispatch_with_source_context; `crates/mcp/src/tools.rs` create_chat/deliver/send_message; `crates/engine/src/uploads.rs` read grants. Follow these even if the UI hides an operation.

## Shared identity and decision contract
Consume WorkProfileBinding/WorkProfileSelection from work-profile-boundary. Never redefine profile as display name/account/scope. Runtime principal is authenticated owning engine context, not request JSON.

Proposed new engine-owned `WorkAuthorizer` is a concrete policy evaluator owned by EngineCore, not a plugin framework. `authorize` returns `Result<AuthorizationPermit, WorkAuthorizationError>`, not an allowed bool plus optional contradictory denial. Permit fields are private, cannot be deserialized from a client. A permit names binding, policy revision, operation, resolved resource and effect generation; use it only at the checked boundary. Revalidate immediately before asynchronous effect dispatch. A missing evaluator returns Unavailable, never allow.

Proposed closed operation variants: ReadSession, MutateSession, RunSession, SteerSession, ReadRepository, MutateRepository, OpenTerminal, WriteTerminal, ObserveTerminal, CloseTerminal, ReadUpload, SelectAgentAccount, ManageAgentLogin. Do not authorize by substring matching an RPC name. Operations for future delivery/browser/triggers are added only with their own reviewed contracts.

Proposed resources are typed internal values: SessionId with owner binding; canonical RepositoryRoot plus repo identity; TerminalId with creator binding and process generation; UploadId with profile-owned root; AgentAccountRef with harness/slot/principal identity. Caller path or opaque ID must resolve to an actual resource before policy comparison; do not expose foreign metadata while resolving. Resolution failure and forbidden must not leak foreign contents.

Typed errors: UnboundLegacy, MigrationRequired, ProfileMismatch, StalePolicy, ResourceDenied, ResourceUnresolved, CapabilityUnavailable. Public RPC error mapping needs exact safe payloads before implementation; never serialize credential path/token or another profile's content in reason text.

## Mandatory integration map

| Entry/effect | Required check location | Denial assertion |
|---|---|---|
| Direct/queued/recovery run | sessions dispatch_inner before transcript/status/title effects; drive_run immediately before Harness::run | zero run calls, no Working transition/user-message append/title launch |
| Warm steer | sessions steer before mailbox send and message write | no steer event or input mutation; unrelated run unchanged |
| MCP create-with-prompt/send | owning engine boundary after MCP deliver, not origin metadata | foreign target denied, zero run; unauthorized create must not leave executable row |
| Device forwarding | destination engine after route resolution and before handler read/effect | client-supplied profile cannot select foreign store; no local substitute |
| OPEN_TERMINAL/project action | RPC resolved cwd/profile plus terminal/process creation boundary | no PTY/process for escaped/foreign root |
| WRITE/SUBSCRIBE/RESIZE/CLOSE_TERMINAL | resolve terminal's binding and generation on each operation | other profile cannot observe/control terminal; revocation blocks write |
| Repository/file/worktree | resolved canonical root before read or subprocess | no bytes read or files/git state mutated on denial |
| Upload chunk/read | profile-owned upload root and explicit migration grant | no legacy/shared-root leakage |
| Account list/activate/forget/login | resolve granted account reference before metadata/file mutation | credential bytes unchanged and foreign slots not enumerated |

Raw ProcessRequest/Command helpers are not policy sources. Callers that bypass these checks must be enumerated before completion. Existing auto-recovery and auto-title paths count as execution, not harmless internal work.

## Required tests to author against actual production boundaries

1. Counting Harness registered in real EngineCore: RunSession denial leaves run count0, transcript unchanged and no working status. Repeat via direct RPC, queued doc command and recovery path.
2. Allow preflight, advance policy revision before blocked dispatch barrier releases: drive_run denies with zero Harness::run. Test barrier is deterministic, not timing sleep.
3. Create two profile stores on same device/principal. Foreign chat/upload/account IDs denied over local and actual device route, not merely store helper access.
4. Harmless terminal fixture writes a marker only on received input. Unauthorized open creates no process; revoked write produces no marker; foreign observe/close cannot control owned terminal.
5. Repository symlink points outside approved root; both read and mutation fail before effect. Validate nonexistent target parent canonicalization for create/write separately.
6. Agent account fixture snapshots fake credential files. Denied activation/login completion/forget leaves byte-identical files. No live credential mutation in test.
7. Steer to prior generation after agent replacement is denied. An unrelated isolated run still progresses.
8. Missing or corrupt policy cannot become unrestricted default; an old client without named-profile capability receives explicit unsupported behavior.

## Canonical scenarios
- C01: A trusted remote device supplies a foreign profile/account/repository ID: reject before any read or child process starts.
- C02: A symlink or renamed checkout escapes the approved repository root: reject the resolved target.
- C03: Policy changes after preflight but before dispatch: dispatch rechecks and denies stale authority.
- C04: An unavailable requested account/tool must report unavailable, not fall back to a global default.
- C05: Direct session and assignment invoking the same protected operation receive equivalent authorization decisions.

## Policy storage and revision ceiling
Use work-profile revision semantics, but distinguish display metadata revision from authorization policy revision in exact schema. A rename need not grant/deny resources; policy update always invalidates affected permits. No global cache keyed only by profile ID. Revoked policy cannot be bypassed by old persisted binding. Exact grant schema and native credential isolation capabilities must be authored before implementation, not delegated as unspecified strings.

## Rollback
Disable new named-profile effects if enforcement cannot be loaded. Preserve policy audit history and original credential data. Never remove checks or silently fall back to device-global access to make old tests pass. Existing direct-session UX preserved only within valid authority; compatibility is not a permission override.
