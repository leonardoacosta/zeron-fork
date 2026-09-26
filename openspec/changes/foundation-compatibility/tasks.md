# Existing-foundation acceptance tasks

Scope: regression evidence for already implemented behavior only. No product implementation, new DTOs, APIs, tests, service operations, or commit are part of this unit. Do not interpret a missing native run as a request to invent behavior.

## Existing automated acceptance

From the repository root, run this exact shell block. It lists each exact test first, asserts one match (preventing a zero-test pass), and then executes that exact fully qualified test. `--locked` holds dependency resolution fixed.

```bash
set -eu
run_one() {
  package="$1"; test_name="$2"; shift 2
  listing=$(cargo test --locked -p "$package" "$@" "$test_name" -- --list --exact)
  printf '%s\n' "$listing"
  count=$(printf '%s\n' "$listing" | grep -Fxc "$test_name: test" || true)
  test "$count" -eq 1 || { echo "expected one test: $test_name, got $count" >&2; exit 1; }
  cargo test --locked -p "$package" "$@" "$test_name" -- --exact
}
run_one zeron-rpc tests::null_unary_response_completes_call --lib
run_one zeron-engine rpc::tests::assignment_create_and_promote_empty_session_over_rpc --lib
run_one zeron-engine assignment_routing_rejects_old_owner_without_writing_locally --test device_routing
run_one zeron-sync store::tests::assignment_mutations_commit_current_history_and_replay_together --lib
run_one zeron-sync store::publication_failure_tests::failed_assignment_mutation_write_rolls_back_create_and_update_atomically --lib
```

Expected assertions and evidence limits:

- `tests::null_unary_response_completes_call`: a null unary result finishes within one second and remains JSON null. Existing automated evidence.
- `rpc::tests::assignment_create_and_promote_empty_session_over_rpc`: promotes an existing empty session, verifies revision/readback/replay and invalid input, and asserts the counting harness has zero runs. Existing automated no-execution evidence; not a native direct-session UI assertion.
- `assignment_routing_rejects_old_owner_without_writing_locally`: an old owner lacking capability returns the explicit unsupported error and local GET remains null. Fake-relay assignment-routing evidence only; not hosted-authentication evidence and not proof that ordinary sessions stay available in every failure mode.
- `store::tests::assignment_mutations_commit_current_history_and_replay_together`: current record, history, and mutation replay persist consistently across store reopen.
- `store::publication_failure_tests::failed_assignment_mutation_write_rolls_back_create_and_update_atomically`: injected mutation-table failure leaves create/update state and history unchanged across reopen; removing the trigger permits a later write. Isolated SQLite rollback evidence, not a live-service rollback.

## Required scenario sentences

Preserve these exact sentences from the shared roadmap:

- Owner restarts after acknowledged assignment: native second-device read/history match and owner unchanged.
- Old owner lacks capability: assignment rejected explicitly, ordinary session unaffected.
- Successful null response completes RPC rather than hanging.
- Direct session opens without an assignment or hidden workflow launch.

## Native Mac/homelab acceptance (new run, not existing test evidence)

A real persistent-service recovery run already exists in `/home/nyaptor/.local/share/zeron-fork-services/README.md` and its `acceptance-before.log` / `acceptance-after-crash.log`. It records prior routed create/replay/get/history checks and recovery after service processes crashed. Treat that strictly as **existing runtime evidence**, not as a new run for this change. Its `check.mjs` names the actual WebSocket RPC protocol (`EngineInfo`, `CreateAssignment`, `GetAssignment`, `ListAssignmentHistory`) but has fixture-specific owner and assignment IDs. Do not copy those IDs as universal fixtures.

For a new run use the isolated persistent test app/profile and homelab owner. The local Mac `EngineRpc` WebSocket endpoint defaults to `ws://127.0.0.1:28755`. Do not touch the original Zeron application or its data. Set `RPC_URL`, `OWNER_DEVICE_ID`, `ASSIGNMENT_ID`, and `MUTATION_ID` explicitly. Choose a fresh unique assignment ID and mutation ID for each write run. The following complete JavaScript uses the actual RPC method names and wire envelope established by the existing `check.mjs`. `WRITE=1` performs the first routed durable-write check; omitting it only re-reads and verifies an already-created assignment after owner restart.

```js
// Save as $JCODE_SCRATCH_DIR/foundation-rpc-check.mjs.
import assert from 'node:assert/strict';
const url = process.env.RPC_URL ?? 'ws://127.0.0.1:28755';
const owner = process.env.OWNER_DEVICE_ID;
const id = process.env.ASSIGNMENT_ID;
const mutationId = process.env.MUTATION_ID;
assert.ok(owner && id && mutationId, 'set OWNER_DEVICE_ID, ASSIGNMENT_ID, MUTATION_ID');
const ws = new WebSocket(url);
await new Promise((resolve, reject) => {
  const timer = setTimeout(() => { ws.close(); reject(Error('connect timeout')); }, 12_000);
  ws.onopen = () => { clearTimeout(timer); resolve(); };
  ws.onerror = (error) => { clearTimeout(timer); reject(error); };
});
let seq = 0;
const pending = new Map();
ws.onmessage = ({ data }) => {
  const reply = JSON.parse(data);
  const waiter = pending.get(reply.id);
  if (!waiter) return;
  clearTimeout(waiter.timer);
  pending.delete(reply.id);
  reply.err ? waiter.reject(Error(reply.err)) : waiter.resolve(reply.ok);
};
function call(method, params = {}) {
  return new Promise((resolve, reject) => {
    const requestId = ++seq;
    const timer = setTimeout(() => reject(Error(`${method} timeout`)), 12_000);
    pending.set(requestId, { resolve, reject, timer });
    ws.send(JSON.stringify({ id: requestId, method, params }));
  });
}
try {
  const info = await call('EngineInfo');
  assert.ok(info.capabilities.includes('assignment-record-v1'));
  assert.notEqual(info.deviceId, owner, 'Mac caller must differ from assignment owner');
  if (process.env.WRITE === '1') {
    const request = { id, objective: 'foundation compatibility acceptance', allowedActions: [], mutationId, targetDeviceId: owner };
    const created = await call('CreateAssignment', request);
    assert.equal(created.ownerDeviceId, owner);
    assert.deepEqual(await call('CreateAssignment', request), created, 'same mutation replays idempotently');
    await assert.rejects(call('CreateAssignment', { ...request, objective: 'conflicting payload' }));
  }
  const record = await call('GetAssignment', { id, targetDeviceId: owner });
  assert.equal(record?.id, id);
  assert.equal(record.ownerDeviceId, owner);
  assert.equal(record.revision, 1);
  assert.equal(record.objective, 'foundation compatibility acceptance');
  const history = await call('ListAssignmentHistory', { id, targetDeviceId: owner });
  assert.deepEqual(history, [record]);
  assert.equal(await call('GetAssignment', { id }), null, 'no local substitute');
  console.log('ROUTED_ASSIGNMENT_PASS', JSON.stringify({ caller: info.deviceId, record, history, write: process.env.WRITE === '1' }));
} finally {
  ws.close();
}
```

1. Before any service action, record UTC time, source commit/tree, Mac test-app executable SHA-256, isolated profile path, caller/owner device IDs, RPC URL, selected assignment/mutation IDs, and `systemctl --user status zeron-fork-owner`. Confirm its unit/process belongs to the isolated test owner described in `/home/nyaptor/.local/share/zeron-fork-services/README.md`. If identity does not match, stop.
2. Run initial acceptance from the Mac using `WRITE=1 node $JCODE_SCRATCH_DIR/foundation-rpc-check.mjs` with the four IDs/endpoints configured. Save output and exit code as the pre-restart acknowledgement and second-device read/history baseline. This only creates a test assignment in the isolated owner profile.
3. Restart only that isolated owner, not the Mac app, relay, tunnel, or original application: `systemctl --user restart zeron-fork-owner`. Capture unit status before and after. This owner restart is authorized only within a separately approved test run.
4. Run `node $JCODE_SCRATCH_DIR/foundation-rpc-check.mjs` with the same IDs, without `WRITE=1`. Pass C01 only when the second-device record/history match the acknowledged baseline and owner/profile remain unchanged. Save output and exit code as a **new native run**.
5. For C04, open an ordinary direct session in the isolated Mac test app without creating/selecting an assignment. Record its session ID and confirm no assignment/workflow was created or launched. Do not invoke the original app or send a prompt to an unapproved live provider. If no existing UI route can establish this safely, record C04 as blocked, not passed. RPC assignment checks alone do not prove direct-session UI behavior.
6. Record exact commands/actions, timestamps, process/service identities, artifact hashes, RPC outcomes, test counts and exit codes. Redact tokens and user content. Keep new evidence separate from Cargo results and existing runtime logs.

This tests private local deployment only, not WorkOS or public hosting. A shared version string is not binary identity. The recipe itself does not operate a service; the separately approved test run performs the explicitly listed isolated owner restart.

## CI heading required by planning validator

## CI phase after every implementation iteration

This unit authorizes no product implementation iteration. The block below validates planning structure and whitespace only. It does not establish feature behavior. Future implementation work must run the tests above and gather separate native evidence, recording selected test counts, source tree, installed binary hashes, environment, and remaining blocks.

```bash
python3 openspec/changes/prd-execution-map/validate.py
git diff --check
```

## Rollback

Automated rollback testing uses isolated temporary SQLite stores and injected triggers. For native acceptance, preserve the original application and data. Only the isolated owner unit may be restarted, and only in the separately approved run. If state is unexpected, stop and preserve logs; do not delete assignment data, reset profiles, modify the original application, or reboot user machines.
