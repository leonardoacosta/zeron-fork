# Existing foundation behavior and evidence boundary

## Read first

`../../../docs/fork-prd.md`, `../prd-execution-map/design.md`, this proposal/spec, and the prerequisite changes `ci-promotion-gates`, `assignment-record`. Baseline `1427da6`; source references are current paths and line numbers may move. These files are anchors, not authorization to edit those surfaces.

## Existing surfaces and file responsibilities

- `crates/engine/tests/device_routing.rs`: existing source/test/config anchor. `assignment_routing_rejects_old_owner_without_writing_locally` proves explicit unsupported-owner rejection and no local substitute with a fake relay.
- `crates/engine/tests/local_profiles.rs`: existing source/test/config anchor. `local_and_synced_profiles_remain_isolated_across_restarts` verifies local/synced profile isolation and persistence across engine reopen.
- `crates/engine/tests/restart_resume.rs`: existing source/test/config anchor. `restart_roundtrip_restores_chats_transcript_and_resume` verifies chat/transcript restoration and resumed harness identity after engine restart.
- `crates/rpc/src/lib.rs`: existing source/test/config anchor. `tests::null_unary_response_completes_call` verifies a successful null RPC response.
- `apps/zeron/src/daemon.rs`: existing source/test/config anchor. `restart` targets the managed daemon service. Native acceptance uses only the separately isolated owner systemd unit, never the original app.
- `openspec/changes/assignment-record/tasks.md`: existing source/test/config anchor. This change consumes existing assignment-record behavior and must not reimplement it.

## Existing code and automated evidence

- RPC null results: `crates/rpc/src/lib.rs`, `tests::null_unary_response_completes_call`. A one-second timeout must finish successfully with JSON null. Existing automated evidence.
- Assignment promotion and no harness execution: `crates/engine/src/rpc.rs`, `EngineRpc::create_assignment` / promotion dispatch and `rpc::tests::assignment_create_and_promote_empty_session_over_rpc`. It promotes an existing empty session, checks revision/readback/replay and invalid input, and asserts the counting harness was never run. Existing automated evidence. This is not proof of a direct-session UI journey.
- Assignment owner routing: `crates/engine/tests/device_routing.rs`, `assignment_routing_rejects_old_owner_without_writing_locally`. A legacy owner without the capability is rejected with `assignment records unsupported`, and local assignment GET remains null. Existing test uses a fake relay/owner. It does not establish hosted authentication or that ordinary sessions remain available during every failure.
- Assignment atomicity/history: `crates/sync/src/store.rs`, `store::tests::assignment_mutations_commit_current_history_and_replay_together` and `store::publication_failure_tests::failed_assignment_mutation_write_rolls_back_create_and_update_atomically`. Store transactions keep current record, history and mutation replay together. Injected SQLite write failure verifies create/update rollback across reopen. Existing isolated automated evidence, not a running service rollback.
- Session continuation: `crates/engine/tests/restart_resume.rs`, `restart_roundtrip_restores_chats_transcript_and_resume`. This is engine restart/resume evidence, not the native installed direct-session opening flow.

Relevant existing RPC methods include `CreateAssignment`, `PromoteAssignment`, `GetAssignment`, `ListAssignmentHistory`, and `UpdateAssignment`; persisted authority is owner/profile scoped in `DocsStore`. Existing wire record fields are defined in `crates/proto/src/assignment.rs`. No reference proposes a new DTO.

## Required behavior and scenario status

Codify current successful assignment persistence and ordinary-session behavior as regression gates. Preserve explicit null RPC successes, unsupported owner rejection, no local substitutes and no implicit delegation. Keep local private deployment distinct from hosted authentication acceptance. Verify exact installed artifacts rather than version string alone.

| Scenario | Existing evidence | Evidence still needed |
|---|---|---|
| C01: Owner restarts after acknowledged assignment: native second-device read/history match and owner unchanged. | Existing runtime logs record routed assignment reads/history and recovery after service crashes. Store tests cover isolated persistence. | A separately recorded new owner-service restart run with before/after second-device reads/history and binary identity. |
| C02: Old owner lacks capability: assignment rejected explicitly, ordinary session unaffected. | Fake-relay routing test verifies explicit unsupported error and no local substitute. | Existing test does not prove ordinary session availability in the same native environment. |
| C03: Successful null response completes RPC rather than hanging. | Null unary RPC test checks a one-second timeout and null value. | No additional native proof is required for the primitive. |
| C04: Direct session opens without an assignment or hidden workflow launch. | No exact existing native UI test identified. Assignment promotion and session resume are adjacent evidence only. | Native direct-session observation on isolated Mac test app without assignment selection/creation. |

## Failure and compatibility scenarios

- C01: Owner restarts after acknowledged assignment: native second-device read/history match and owner unchanged.
- C02: Old owner lacks capability: assignment rejected explicitly, ordinary session unaffected.
- C03: Successful null response completes RPC rather than hanging.
- C04: Direct session opens without an assignment or hidden workflow launch.

A transactional assignment write must not leave a created/updated row or history row after the mutation journal write fails. The existing fault-injection test reopens the store to verify durable state. A failed transaction is not permission to reroute locally, switch owners, or erase data. Owner/profile mismatch and unsupported owner capability are explicit errors.

## Native evidence boundary

Existing runtime evidence is described at `/home/nyaptor/.local/share/zeron-fork-services/README.md` with `acceptance-before.log` and `acceptance-after-crash.log`. It records prior persistent-service recovery and is not a new run. `check.mjs` establishes actual WebSocket method names (`EngineInfo`, `CreateAssignment`, `GetAssignment`, `ListAssignmentHistory`) but contains fixture-specific IDs. Use `tasks.md`'s configurable native RPC recipe for new observations. Only the isolated test owner systemd unit may be restarted with explicit run approval. Preserve the original Zeron app/profile. No public hosting/WorkOS conclusion follows from private relay evidence. A version string alone does not identify binary bytes.

Structural inspection, unit tests and provider doubles help explain behavior but cannot replace C01/C04 native evidence. If an endpoint or direct-session route is unavailable, record it blocked rather than claim acceptance or invent a new UI/API.

## Rollout and rollback

Use isolated data and preserve the installed original app. Service tests must operate only on owned fixtures. Do not reboot user machines. Unexpected native state means stop and preserve logs; cleanup or data deletion requires separate authorization.

## Implementation readiness

This is a bounded behavior contract for already built foundation features, not permission to implement new product behavior. Existing automated tests and existing runtime logs are distinct from new native acceptance. No new DTOs or provider APIs are required or authorized.

## Refined handoff validation
Exact first shell block extracted from tasks.md selected exactly1 test for each of five fully-qualified filters and all five executions passed on19:20 UTC. Native recipe code has not been newly executed in this refinement. Existing prior native evidence remains separate.
