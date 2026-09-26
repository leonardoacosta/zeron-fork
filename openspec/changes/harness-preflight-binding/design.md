# Harness preflight: proposed execution boundary

Status: exact observed hazards and proposed interface, not implemented. Full runtime handoff still requires adapter-specific patches/tests below. No availability flag is enforcement proof.

## Existing anchors
- `crates/engine/src/registry.rs`: HarnessDescriptor has installed/enabled/steering/model metadata, no verified sandbox/stop/resource contract.
- `crates/harness/src/lib.rs`: Harness::run consumes RunRequest/RunControls; interrupt token does not itself prove stopped.
- `crates/proto/src/agent.rs`: RunRequest contains optional harness/model, sandbox, auto_approve, cwd, resume, attachments/worktree. Old host may ignore worktree and use main cwd. This fallback must be denied when isolation required.
- `crates/engine/src/sessions.rs`: dispatch/dispatch_with and persisted session runtime configuration are launch enforcement points; metadata-only registry checks are insufficient.
- `crates/harness/src/codex/mod.rs`: normal run overwrites requested sandbox with DangerFullAccess at ordinary-run startup; approval_policy is always never. These are confirmed source facts at8d5189f, not only historical Recon findings.
- `crates/harness/src/claude/mod.rs`: CLI permission flags depend on auto_approve, but handle_control_request allows every non-AskUserQuestion tool. Flags alone cannot establish denied tool enforcement.
- `crates/harness/src/acp/mod.rs`: handle_server_request chooses preferred allow option; handle_server_request_live routes ordinary permission calls there. An adapter label or false auto_approve is not a deny boundary.

## Proposed shared interface
Use existing HarnessId, SandboxLevel, RunRequest. Do not add a second harness enum or conflate SystemOne with engineering harnesses. New proposed types in `crates/proto/src/harness_preflight.rs`:

- `CapabilityVerdict`: tagged `Supported { evidence_id: String }`, `Unsupported { reason: String }`, `Unknown { reason: String }`. Empty reason/evidence invalid. Evidence ID is reference to observed capability test, not provider marketing.
- `HarnessObservation`: exact executable canonical path and content identity, provider version string, platform, adapter source revision, observation timestamp. Store no token/environment values. Resolve identity on owning host; remote caller cannot assert it as fact.
- `PreflightRequest`: selected WorkProfileBinding, explicit HarnessId/model ID/account reference/environment reference, SandboxLevel, permission-policy reference, requested resource policy and required capability names. Model/account/environment unset is invalid for delegated execution; direct-session UX may resolve explicit configured defaults before creating this request, then display actual resolved values.
- `PreflightResult`: immutable request binding, observation and capability verdicts. Any required capability not Supported makes launch inadmissible. Optional unknown cost remains unknown and invokes resource policy, never zero.
- `LaunchBinding`: reference to persisted preflight result plus immutable selected run configuration; produced by owner only after authorization. A preflight result is not an authority token from an untrusted client.

Wire fields and persisted schema must be shared with profile-access-enforcement/run-resource-ledger/revision-evidence-bindings. Those contracts consume the same WorkProfileBinding defined by work-profile-boundary, not independent string profile labels. Requested sandbox and observed provider configuration are both recorded; mismatch is a failure, never normalized into a claimed pass.

## Safe initial adapter coverage matrix

| Existing adapter path | Current observed behavior | Required initial preflight disposition |
|---|---|---|
| Codex ordinary run | Overwrites sandbox with DangerFullAccess | Restricted requested sandbox unsupported until actual wire behavior repaired and verified |
| Claude tool control | Non-question tools auto-allowed | Enforced per-tool restriction unknown/unsupported until control handler is policy-bound |
| ACP tool permission | Preferred allow option chosen | Same restriction unavailable until request handler consumes enforced policy |
| Any old host | May ignore additive isolation fields | Required isolation rejects old capability, never falls back to ordinary cwd |
| Any provider | CancellationToken exposed | Stop-confirmed remains unknown until confirmed-stop-handoff provider evidence |

This matrix is not a permanent disable-all implementation. Each capability can become supported only through a narrowly tested concrete adapter change. Keep ordinary explicit full-access behavior only when its selected profile/action policy authorizes it; never globally downgrade requested safety to retain compatibility.

## Exact adapter observations to test next

1. Codex: existing `crates/harness/tests/codex.rs` and `tests/fixtures/fake-codex.sh` observe thread/start and turn/start. Add cases that request ReadOnly and WorkspaceWrite with auto_approve false and assert wire sandbox values are preserved; add false-auto-approve permission requests that cannot receive blanket allow. Existing wire-params scenario currently expects dangerFullAccess, so blindly changing production code without updating intent-specific cases would create misleading tests. Title-only ReadOnly remains separately tested.
2. Claude: use actual `ControlRequestFrame` parsing and existing control handler tests. An ordinary denied tool must yield documented deny response and zero effect; AskUserQuestion remains a user input operation, not a permission grant. Obtain exact deny wire schema from existing `wire.rs` or pinned official protocol before patching; do not invent fields.
3. ACP: test provider options with allow_once/allow_always/reject choices, no reject option, foreign sessionId and dropped input channel. Default unavailable policy responds cancelled, not preferred allow. Never interpret user question options as tool authorization.
4. Engine: mutation of provider executable/version/config after preflight invalidates launch. Validate before subprocess construction and after any async policy wait. Denied/unknown preflight must show zero Harness::run calls, no worktree creation, no credential export and no remote dispatch.
5. Native provider: a harmless file-write outside authorized sandbox must actually be prevented before capability becomes Supported. Protocol fixture tests are synthetic evidence, not OS sandbox proof.

## Canonical scenarios
- C01: A harness advertises cancellation but cannot prove descendant stopping: report that capability as unverified, not supported.
- C02: Requested sandbox differs from actual process arguments: preflight fails and no agent starts.
- C03: Missing model/account/executable cannot silently route to another engineer.
- C04: A model or adapter version changes between preflight and launch: invalidate/recheck binding.

## Rollback and promotion
Retain old observations and capability evidence with their adapter versions. Reverting an enforcement repair invalidates Supported verdicts for that capability and blocks affected new launches. Do not alter active authorized runs without confirmed stop. Run provider tests and engine no-launch negative tests before promotion; actual provider isolation/stopping requires separately authorized native evidence. Jcode/Herdr provider contracts remain research-dependent, never inferred from current adapter collection.
