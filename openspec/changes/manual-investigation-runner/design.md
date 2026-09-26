# Manual investigation execution: durable admission before dispatch

Status: source-grounded integration contract; exact admission/outbox implementation being refined. Existing record APIs must continue performing zero launches.

## Existing anchors
- `crates/engine/src/sessions.rs`: dispatch_inner mints volatile run_id, starts Working/title/drive_run; native session identity is separate and may span turns.
- `crates/engine/src/rpc.rs`: owner forwarding/capability checks and assignment CRUD. New launch action must be explicit and separately gated.
- `crates/proto/src/assignment.rs`: record/revision/review DTOs, no execution identity.
- `crates/sync/src/store.rs`: assignments/replay and processed_commands, but no transaction spanning assignment launch and Loro queue.
- `crates/engine/tests/restart_resume.rs`: native-session recovery assertions, not durable assignment-stage identity.
- Required additional boundary: `crates/engine/src/doc_host.rs` queue_command_with_transfers generates a new ID, appends Loro then spawns delivery; drain_commands claims SQLite processed ID before effect. `crates/doc/src/schema.rs` queue_command blindly appends and commits, no same-ID payload conflict guard.

## Distinct identities that must never be collapsed
1. Assignment ID/revision: persistent objective snapshot.
2. Execution ID: new immutable owner-minted identity for one explicit stage launch intent, stable across request replay.
3. Command ID: stable preallocated projection ID for that execution's durable outbox entry, not regenerated on pump retry.
4. Execution generation/attempt: durable monotonic start attempt, bound before spawn. Late prior-generation events ignored/rejected.
5. Existing SessionsEngine run_id: volatile process-generation guard; associate it with durable execution generation, never claim it survives restart.
6. Native harness session_id: provider resume reference, can span turns, not a stage identity.
7. Journal sequence: per-chat observation order, not a globally unique execution identity.

## Required admission transaction
Owning engine validates current work-profile authority, pinned workflow/stage, preflight capability/configuration, repository and budget. Then one SQLite transaction checks expected assignment revision and scoped mutation identity, allocates execution+command IDs once, records frozen request binding and creates an outbox row. Same identity+payload returns original IDs; changed payload conflicts. No native launch or Loro append inside that transaction. Resource reservation must be the same transaction or a recoverable explicitly bound prior reservation; do not invent cross-database atomicity.

Outbox pump projects an immutable entry using stable command ID. Existing queue append must gain an owner-internal idempotent path: exact immutable payload/issuer/time/frontier/expiry match is a no-op even if status has progressed; changed content under same ID rejects. Never reset Applied/Rejected back to Pending. Because current read_commands skips malformed entries, projection must inspect raw matching IDs and fail closed on malformed duplicate identity rather than silently append. Serialize owner projection per chat. Multi-writer Loro merge is not a transaction lock and requires explicit duplicate detection after merge.

After append but before marking outbox delivered, crash replay uses identical command ID and payload. Do not claim this alone proves exactly-once agent effects. Consumed-before-spawn crash remains uncertain. Persist execution generation/start intent before dispatch, associate actual volatile run/native session/journal sequence as observations arrive, and reject stale-generation terminal events.

## Restart semantics
Queued outbox may redeliver exact command. Starting without trustworthy native start receipt holds Uncertain and never blindly respawns. Running requires safe-resume reconciliation and continuing authority. Finished observation is not verification/acceptance; findings are bound to exact output revision and configured checks. Preserve reservation and effect uncertainty across restart. Default recovery of unrelated direct sessions must not accidentally replay assignment starts through legacy path.

## Bounded first vertical slice
One explicitly launched Investigate stage on one isolated local repository, configured engineer once, durable admission/outbox, stable command projection, one real SessionsEngine dispatch generation, counting harmless mock Harness emitting SessionStarted/Text/Done, durable findings reference. No autonomous stage progression, implementation, delivery, UI redesign or external mutation. This slice is a regression fixture, not real native provider acceptance; final unit still requires authorized harmless native investigation with stop/replacement/restart.

## Acceptance cases and negative controls
- C01: Double-click/retried launch yields one run identity and one resource reservation.
- C02: Replacement adds linked session while preserving findings/history and allowed actions.
- C03: Investigation ends with checked findings and unresolved questions, without requiring code changes.
- C04: Direct session opens normally without automatic assignment creation.

Additional exact tests: failure inserting outbox rolls back execution claim; two callers race same revision/key; crash after projection before delivered marker; malformed/changed same-ID command; status already Applied; duplicate Loro merge; crash after starting before native receipt; late old-generation Done; revoked policy before dispatch; reservation uncertain; invalid workflow version; assignment CRUD still zero Harness::run. No successful zero-test filters.

## Rollback / promotion
Hold/confirm stop for active affected execution before downgrade. Preserve durable intent, outbox, generations, native IDs, findings and costs. Never delete processed ledger to retry. Only after real integrated CI and all prerequisite safety gates can explicit launch capability be advertised. Until conflict observer exists, acceptance uses isolated single-run scope with affected-resource holds, not unrestricted concurrency.
