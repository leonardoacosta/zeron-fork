# Manual bounded investigation workflow execution contract

**Goal:** Explicitly launch one configured investigation for an assignment after profile/preflight/resource/selection gates.
**Architecture:** Existing Rust engine/proto/RPC/profile storage and native clients are the starting point. Freeze interfaces from observed source; no speculative provider API or generic framework.
**Tech stack:** Rust/Tokio/Serde/SQLite; GPUI/Swift/Worker TypeScript only if the approved surface requires them.
**Status:** executable discovery/refinement steps; product implementation NOT READY.
**Dependencies:** `safe-resume-reconciliation`, `verification-acceptance-gates`, `run-resource-ledger`, `work-profile-boundary`. Only exact prerequisite promotion admits implementation.

## D1. Recover authority and source (one bounded read per listed anchor)
**Files:** design.md and tasks.md in this change; read-only source anchors in design.md.
- [ ] Read PRD clauses ZF-03, ZF-05, ZF-06, ZF-08 and every C-scenario in `specs/manual-investigation-runner/spec.md`; state excluded sibling behavior in design.md.
- [ ] From repository root, verify listed anchors exist:
```bash
python3 - <<'PY'
from pathlib import Path
paths = ['crates/engine/src/sessions.rs', 'crates/engine/src/rpc.rs', 'crates/proto/src/assignment.rs', 'crates/sync/src/store.rs', 'crates/engine/tests/restart_resume.rs']
for name in paths:
    p = Path(name)
    assert p.is_file(), name
    print(name, len(p.read_text().splitlines()), "lines")
PY
```
Expected: one line per anchor, exit0. Missing path means re-discover with graft and correct this contract; do not create a dummy file. Read `graft/INDEX.md` then matching cards. Use `graft ask "Manual bounded investigation workflow" --source` only if the CLI is already available; graph files are sufficient.
- [ ] In design.md, cite exact symbols/current line spans for the input, authority, persistence and side-effect paths. For each C-scenario record whether current behavior is observed, contradicted or not yet tested. Do not equate missing grep hit with absence proof.

## A. Exact additive DocsStore admission patch
**Modify:** `crates/sync/src/store.rs` only for this slice: typed admission DTO/errors, one appended migration, atomic claim/outbox methods and6 inline tests. No Loro append, Harness::run or automatic dispatch. This is storage admission, not the full investigation runner.

Inspected source SHA256: `108896194bbe67ca2e6e63e42463d42d650731e3fec55896d7859906c5437442`. If source differs, refresh exact anchors and rerun tests; do not overwrite concurrent changes or apply a stale patch blindly.

- [ ] Extract the `assignment_execution_tests` module from this patch into the real file first and run `cargo test --locked -p zeron-sync --lib assignment_execution_tests`. Expect missing API compile-red initially; record it as preparatory, not behavioral proof.
- [ ] Apply the remaining exact added types/migration/methods from the patch. Do not add the test module twice. The migration is appended to existing MIGRATIONS; do not replace schema_migrations or create a second database containing copied assignments.
```diff
--- a/crates/sync/src/store.rs
+++ b/crates/sync/src/store.rs
@@ -26,6 +26,40 @@
     Invalid,
 }

+#[derive(Debug, Clone, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
+pub struct AssignmentExecutionRequest {
+    pub assignment_id: String,
+    pub owner: String,
+    pub profile: String,
+    pub expected_revision: u64,
+    pub operation_key: String,
+    pub workflow_id: String,
+    pub workflow_revision: u64,
+    pub stage_id: String,
+    pub chat_id: String,
+    pub command_payload: String,
+}
+
+#[derive(Debug, Clone, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
+pub struct AssignmentExecution {
+    pub execution_id: String,
+    pub command_id: String,
+    pub assignment_revision: u64,
+    pub state: String,
+}
+
+#[derive(Debug, Clone, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
+pub struct AssignmentExecutionOutboxItem {
+    pub execution_id: String,
+    pub command_id: String,
+    pub chat_id: String,
+    pub payload: String,
+}
+
+#[derive(Debug, Clone, Copy, PartialEq, Eq)]
+pub enum AssignmentExecutionError { Missing, Stale, Conflict, ActiveStage, Invalid, Sqlite }
+
+
 /// Synchronous command/doc callbacks still need commit-before-send semantics.
 /// Relinquish a multithread runtime's core BEFORE either SQLite or its mutex
 /// can block; moving only the snapshot writer leaves these contenders fatal.
@@ -85,6 +119,27 @@
     "CREATE TABLE assignments (id TEXT PRIMARY KEY, owner TEXT NOT NULL, profile TEXT NOT NULL, revision INTEGER NOT NULL, payload TEXT NOT NULL) STRICT;
      CREATE TABLE assignment_history (assignment_id TEXT NOT NULL, revision INTEGER NOT NULL, payload TEXT NOT NULL, committed_at INTEGER NOT NULL, PRIMARY KEY(assignment_id,revision)) STRICT;
      CREATE TABLE assignment_mutations (assignment_id TEXT NOT NULL, owner TEXT NOT NULL, profile TEXT NOT NULL, mutation_id TEXT NOT NULL, payload TEXT NOT NULL, result TEXT NOT NULL, PRIMARY KEY(assignment_id,owner,profile,mutation_id)) STRICT;",
+    // v8 — assignment stage execution claims and SQLite-local command projection outbox.
+    "CREATE TABLE assignment_executions (
+        execution_id TEXT PRIMARY KEY, command_id TEXT NOT NULL UNIQUE,
+        owner TEXT NOT NULL, profile TEXT NOT NULL, assignment_id TEXT NOT NULL,
+        assignment_revision INTEGER NOT NULL CHECK(assignment_revision > 0),
+        operation_key TEXT NOT NULL, request_payload TEXT NOT NULL,
+        workflow_id TEXT NOT NULL, workflow_revision INTEGER NOT NULL CHECK(workflow_revision > 0),
+        stage_id TEXT NOT NULL, chat_id TEXT NOT NULL, command_payload TEXT NOT NULL,
+        state TEXT NOT NULL CHECK(state IN ('admitted','queued','starting','running','finished','blocked','uncertain')),
+        created_at INTEGER NOT NULL, updated_at INTEGER NOT NULL,
+        UNIQUE(owner,profile,assignment_id,operation_key),
+        FOREIGN KEY(assignment_id) REFERENCES assignments(id)
+     ) STRICT;
+     CREATE UNIQUE INDEX assignment_executions_active_stage
+       ON assignment_executions(owner,profile,assignment_id,workflow_id,workflow_revision,stage_id)
+       WHERE state IN ('admitted','queued','starting','running','blocked','uncertain');
+     CREATE TABLE assignment_execution_outbox (
+        execution_id TEXT PRIMARY KEY REFERENCES assignment_executions(execution_id),
+        command_id TEXT NOT NULL UNIQUE, chat_id TEXT NOT NULL, payload TEXT NOT NULL,
+        state TEXT NOT NULL CHECK(state IN ('pending','delivered')), created_at INTEGER NOT NULL
+     ) STRICT;",
 ];

 /// SQLite-backed store under a data directory (`{data_dir}/docs.sqlite3`).
@@ -116,6 +171,114 @@
         })
     }

+    /// Claim an assignment execution and SQLite-local projection outbox in one transaction.
+    /// It does not commit a SessionDoc/Loro command or launch a process. The outbox command_id
+    /// is stable; projection must be made idempotent at the Loro boundary separately.
+    pub fn claim_assignment_execution(
+        &self,
+        request: &AssignmentExecutionRequest,
+    ) -> Result<AssignmentExecution, AssignmentExecutionError> {
+        store_blocking(|| {
+            for value in [
+                request.assignment_id.as_str(), request.owner.as_str(), request.profile.as_str(),
+                request.operation_key.as_str(), request.workflow_id.as_str(), request.stage_id.as_str(),
+                request.chat_id.as_str(), request.command_payload.as_str(),
+            ] {
+                if value.trim().is_empty() { return Err(AssignmentExecutionError::Invalid); }
+            }
+            if request.expected_revision == 0 || request.workflow_revision == 0 {
+                return Err(AssignmentExecutionError::Invalid);
+            }
+            let mut conn = self.conn();
+            let tx = conn.transaction_with_behavior(rusqlite::TransactionBehavior::Immediate)
+                .map_err(|_| AssignmentExecutionError::Sqlite)?;
+            let request_payload = serde_json::to_string(request)
+                .map_err(|_| AssignmentExecutionError::Invalid)?;
+            if let Some((saved, execution_id, command_id, revision, state)) = tx.query_row(
+                "SELECT request_payload,execution_id,command_id,assignment_revision,state
+                 FROM assignment_executions WHERE owner=?1 AND profile=?2 AND assignment_id=?3 AND operation_key=?4",
+                params![request.owner, request.profile, request.assignment_id, request.operation_key],
+                |r| Ok((r.get::<_,String>(0)?,r.get::<_,String>(1)?,r.get::<_,String>(2)?,r.get::<_,i64>(3)?,r.get::<_,String>(4)?)),
+            ).optional().map_err(|_| AssignmentExecutionError::Sqlite)? {
+                if saved != request_payload { return Err(AssignmentExecutionError::Conflict); }
+                let assignment_revision = u64::try_from(revision).map_err(|_| AssignmentExecutionError::Sqlite)?;
+                tx.commit().map_err(|_| AssignmentExecutionError::Sqlite)?;
+                return Ok(AssignmentExecution { execution_id, command_id, assignment_revision, state });
+            }
+            // assignments.id is the existing global PK. Resolve owner/profile in the same tx.
+            let current: Option<(String,String,i64)> = tx.query_row(
+                "SELECT owner,profile,revision FROM assignments WHERE id=?1",
+                [&request.assignment_id], |r| Ok((r.get(0)?,r.get(1)?,r.get(2)?)),
+            ).optional().map_err(|_| AssignmentExecutionError::Sqlite)?;
+            let Some((owner,profile,revision)) = current else { return Err(AssignmentExecutionError::Missing); };
+            if owner != request.owner || profile != request.profile { return Err(AssignmentExecutionError::Missing); }
+            if revision != i64::try_from(request.expected_revision).map_err(|_| AssignmentExecutionError::Invalid)? {
+                return Err(AssignmentExecutionError::Stale);
+            }
+            let execution_id = uuid::Uuid::new_v4().to_string();
+            let command_id = uuid::Uuid::new_v4().to_string();
+            let now = now_ms();
+            let insert = tx.execute(
+                "INSERT INTO assignment_executions(execution_id,command_id,owner,profile,assignment_id,assignment_revision,operation_key,request_payload,workflow_id,workflow_revision,stage_id,chat_id,command_payload,state,created_at,updated_at)
+                 VALUES (?1,?2,?3,?4,?5,?6,?7,?8,?9,?10,?11,?12,?13,'admitted',?14,?14)",
+                params![execution_id,command_id,request.owner,request.profile,request.assignment_id,revision,request.operation_key,request_payload,request.workflow_id,request.workflow_revision,request.stage_id,request.chat_id,request.command_payload,now],
+            );
+            if let Err(error) = insert {
+                let active_stage_unique = matches!(error,
+                    rusqlite::Error::SqliteFailure(ref code, _)
+                    if code.extended_code == rusqlite::ffi::SQLITE_CONSTRAINT_UNIQUE);
+                if active_stage_unique {
+                    let active: bool = tx.query_row(
+                        "SELECT EXISTS(SELECT 1 FROM assignment_executions
+                         WHERE owner=?1 AND profile=?2 AND assignment_id=?3 AND workflow_id=?4
+                         AND workflow_revision=?5 AND stage_id=?6
+                         AND state IN ('admitted','queued','starting','running','blocked','uncertain'))",
+                        params![request.owner,request.profile,request.assignment_id,request.workflow_id,request.workflow_revision,request.stage_id],
+                        |r| r.get(0),
+                    ).map_err(|_| AssignmentExecutionError::Sqlite)?;
+                    if active { return Err(AssignmentExecutionError::ActiveStage); }
+                }
+                return Err(AssignmentExecutionError::Sqlite);
+            }
+            tx.execute(
+                "INSERT INTO assignment_execution_outbox(execution_id,command_id,chat_id,payload,state,created_at)
+                 VALUES (?1,?2,?3,?4,'pending',?5)",
+                params![execution_id,command_id,request.chat_id,request.command_payload,now],
+            ).map_err(|_| AssignmentExecutionError::Sqlite)?;
+            tx.commit().map_err(|_| AssignmentExecutionError::Sqlite)?;
+            Ok(AssignmentExecution { execution_id, command_id, assignment_revision: request.expected_revision, state: "admitted".into() })
+        })
+    }
+
+    /// Pending SQLite projection items. A projector appends to Loro with stable command_id;
+    /// only after that separate write can it mark the row delivered.
+    pub fn pending_assignment_execution_outbox(&self, limit: usize) -> Result<Vec<AssignmentExecutionOutboxItem>, StoreError> {
+        store_blocking(|| {
+            let conn = self.conn();
+            let mut stmt = conn.prepare("SELECT execution_id,command_id,chat_id,payload FROM assignment_execution_outbox WHERE state='pending' ORDER BY created_at,execution_id LIMIT ?1")?;
+            Ok(stmt.query_map([limit.min(100) as i64], |r| Ok(AssignmentExecutionOutboxItem {
+                execution_id: r.get(0)?, command_id: r.get(1)?, chat_id: r.get(2)?, payload: r.get(3)?,
+            }))?.collect::<Result<Vec<_>,_>>()?)
+        })
+    }
+
+    pub fn mark_assignment_execution_queued(&self, execution_id: &str, command_id: &str) -> Result<(), AssignmentExecutionError> {
+        store_blocking(|| {
+            let mut conn = self.conn();
+            let tx = conn.transaction().map_err(|_| AssignmentExecutionError::Sqlite)?;
+            let state: Option<String> = tx.query_row(
+                "SELECT state FROM assignment_executions WHERE execution_id=?1 AND command_id=?2",
+                params![execution_id,command_id], |r| r.get(0),
+            ).optional().map_err(|_| AssignmentExecutionError::Sqlite)?;
+            let Some(state) = state else { return Err(AssignmentExecutionError::Missing); };
+            if state != "admitted" && state != "queued" { return Err(AssignmentExecutionError::Invalid); }
+            tx.execute("UPDATE assignment_execution_outbox SET state='delivered' WHERE execution_id=?1 AND command_id=?2",params![execution_id,command_id]).map_err(|_|AssignmentExecutionError::Sqlite)?;
+            tx.execute("UPDATE assignment_executions SET state='queued',updated_at=?1 WHERE execution_id=?2",params![now_ms(),execution_id]).map_err(|_|AssignmentExecutionError::Sqlite)?;
+            tx.commit().map_err(|_| AssignmentExecutionError::Sqlite)?;
+            Ok(())
+        })
+    }
+
     pub fn assignment_mutation_result(
         &self,
         id: &str,
@@ -1229,3 +1392,122 @@
         );
     }
 }
+
+#[cfg(test)]
+mod assignment_execution_tests {
+    use super::*;
+
+    fn request() -> AssignmentExecutionRequest {
+        AssignmentExecutionRequest {
+            assignment_id: "assignment-a".into(),
+            owner: "device-a".into(),
+            profile: "profile-a".into(),
+            expected_revision: 3,
+            operation_key: "investigation-once".into(),
+            workflow_id: "manual-investigation-v1".into(),
+            workflow_revision: 1,
+            stage_id: "Investigate".into(),
+            chat_id: "chat-a".into(),
+            command_payload: r#"{"kind":"run","prompt":"inspect fixture"}"#.into(),
+        }
+    }
+
+    fn store() -> (tempfile::TempDir, DocsStore) {
+        let dir = tempfile::tempdir().unwrap();
+        let store = DocsStore::open(dir.path()).unwrap();
+        let initial = r#"{"id":"assignment-a","ownerDeviceId":"device-a","profileId":"profile-a","revision":1,"objective":"inspect local fixture"}"#;
+        store.create_assignment("assignment-a", "device-a", "profile-a", initial, "create-a").unwrap();
+        for (expected, mutation) in [(1_u64,"edit-1"),(2_u64,"edit-2")] {
+            let value: serde_json::Value = serde_json::from_str(initial).unwrap();
+            store.save_assignment(&value, expected, mutation, initial, "device-a", "profile-a").unwrap();
+        }
+        assert_eq!(serde_json::from_str::<serde_json::Value>(&store.load_assignment("assignment-a","device-a","profile-a").unwrap().unwrap()).unwrap()["revision"],3);
+        (dir, store)
+    }
+
+    #[test]
+    fn claim_replays_same_payload_and_rejects_operation_key_conflict() {
+        let (_dir, store) = store();
+        let first = store.claim_assignment_execution(&request()).unwrap();
+        let replay = store.claim_assignment_execution(&request()).unwrap();
+        assert_eq!(first, replay);
+        assert_eq!(store.pending_assignment_execution_outbox(10).unwrap().len(), 1);
+        let mut changed = request();
+        changed.command_payload = "different prompt".into();
+        assert_eq!(store.claim_assignment_execution(&changed), Err(AssignmentExecutionError::Conflict));
+        assert_eq!(store.pending_assignment_execution_outbox(10).unwrap().len(), 1);
+        drop(store);
+        let reopened = DocsStore::open(_dir.path()).unwrap();
+        assert_eq!(reopened.claim_assignment_execution(&request()).unwrap(), first);
+        assert_eq!(reopened.pending_assignment_execution_outbox(10).unwrap().len(), 1);
+    }
+
+    #[test]
+    fn stale_revision_and_foreign_owner_profile_deny_before_outbox() {
+        let (_dir, store) = store();
+        let mut stale = request(); stale.expected_revision = 2;
+        assert_eq!(store.claim_assignment_execution(&stale), Err(AssignmentExecutionError::Stale));
+        let mut foreign_owner = request(); foreign_owner.owner = "other-device".into();
+        assert_eq!(store.claim_assignment_execution(&foreign_owner), Err(AssignmentExecutionError::Missing));
+        let mut foreign_profile = request(); foreign_profile.profile = "other-profile".into();
+        assert_eq!(store.claim_assignment_execution(&foreign_profile), Err(AssignmentExecutionError::Missing));
+        assert!(store.pending_assignment_execution_outbox(10).unwrap().is_empty());
+    }
+
+    #[test]
+    fn execution_and_outbox_roll_back_together_on_late_sql_failure() {
+        let (_dir, store) = store();
+        store.conn().execute_batch("CREATE TRIGGER fail_assignment_execution_outbox BEFORE INSERT ON assignment_execution_outbox BEGIN SELECT RAISE(FAIL,'injected'); END;").unwrap();
+        assert_eq!(store.claim_assignment_execution(&request()), Err(AssignmentExecutionError::Sqlite));
+        assert!(store.pending_assignment_execution_outbox(10).unwrap().is_empty());
+        let execution_count: i64 = store.conn().query_row("SELECT count(*) FROM assignment_executions", [], |row| row.get(0)).unwrap();
+        assert_eq!(execution_count, 0, "failed outbox insertion must roll back the execution row");
+        store.conn().execute_batch("DROP TRIGGER fail_assignment_execution_outbox;").unwrap();
+        assert!(store.claim_assignment_execution(&request()).is_ok(), "failed claim left no operation-key row");
+    }
+
+    #[test]
+    fn duplicate_active_stage_rejected_with_specific_error() {
+        let (_dir, store) = store();
+        store.claim_assignment_execution(&request()).unwrap();
+        let mut another_key = request(); another_key.operation_key = "second-attempt".into();
+        assert_eq!(store.claim_assignment_execution(&another_key), Err(AssignmentExecutionError::ActiveStage));
+    }
+
+    #[test]
+    fn concurrent_same_key_claim_replays_same_ids_after_reopen() {
+        let (dir, store) = store();
+        let first = store.claim_assignment_execution(&request()).unwrap();
+        drop(store);
+        let path = dir.path().to_path_buf();
+        let barrier = std::sync::Arc::new(std::sync::Barrier::new(3));
+        let mut workers = Vec::new();
+        for _ in 0..2 {
+            let path = path.clone();
+            let barrier = barrier.clone();
+            workers.push(std::thread::spawn(move || {
+                let store = DocsStore::open(path).unwrap();
+                barrier.wait();
+                store.claim_assignment_execution(&request()).unwrap()
+            }));
+        }
+        barrier.wait();
+        for worker in workers {
+            assert_eq!(worker.join().unwrap(), first);
+        }
+        let reopened = DocsStore::open(dir.path()).unwrap();
+        assert_eq!(reopened.pending_assignment_execution_outbox(10).unwrap().len(), 1);
+    }
+
+    #[test]
+    fn queued_projection_has_stable_ids_across_pending_reads() {
+        let (_dir, store) = store();
+        let claim = store.claim_assignment_execution(&request()).unwrap();
+        let first = store.pending_assignment_execution_outbox(10).unwrap().remove(0);
+        let second = store.pending_assignment_execution_outbox(10).unwrap().remove(0);
+        assert_eq!(first, second);
+        assert_eq!(first.command_id, claim.command_id);
+        store.mark_assignment_execution_queued(&claim.execution_id, &claim.command_id).unwrap();
+        assert!(store.pending_assignment_execution_outbox(10).unwrap().is_empty());
+    }
+}
```
- [ ] Run `cargo test --locked -p zeron-sync --lib assignment_execution_tests`; require6 selected tests and6 passes. Run full `cargo test --locked -p zeron-sync --lib` and existing assignment storage regression afterward. Run `cargo clippy --workspace --all-targets --all-features -- -D warnings` only after scoped formatting and actual project build prerequisites are available.
- [ ] Behavioral negative control in isolated source copy: remove the late outbox insert from the transaction or commit execution before it, then require rollback test failure. Restore exact patch before any commit. Concurrent same-key claim must return identical execution/command IDs after reopen.
- [ ] Do not expose `AssignmentExecutionRequest` as an authority-bearing client DTO: owner/profile are owning engine resolved values. Before external RPC admission add explicit size/canonical typed validation and required workflow/preflight/resource binding from prerequisite contracts. Current store request fields are internal inputs, not permission labels.
- [ ] Stable command ID is not yet safe projection. In `crates/doc/src/schema.rs`, `SessionDoc::queue_command` unconditionally pushes a new Loro map, while `read_commands` deserializes and skips malformed rows. Add a distinct idempotent method (do not change ordinary append semantics) for outbox projection: scan raw `commands` list maps for exact string `id` before append; same ID plus semantically identical serialized `SessionCommandEntry` returns success without commit, same ID with different valid fields returns `DocError::Schema` conflict, and malformed entries are ignored unless their raw `id` exactly collides, in which case fail closed. Exact expected entry/status must be fixed by the caller contract; repeated delivery after status updates must not rewrite status or payload. Keep Loro operation synchronous and commit only on first append. Add inline regression tests for new ID appends once; identical replay leaves command count/export bytes/version unchanged; conflicting ID rejects without mutation; malformed unrelated row doesn't block projection; malformed colliding row rejects; and pending-to-applied then replay preserves applied status. Test reopen/import replay and same-instance replay.
  - Required command: `cargo test --locked -p zeron-doc --lib <exact_projection_test_filter>` with nonzero selected tests, plus `cargo test --locked -p zeron-doc --lib`; `cargo clippy --locked -p zeron-doc --all-targets -- -D warnings`. Record exact counts and exit codes. Add source-copy negative controls for removing duplicate detection and allowing conflicting ID; both must fail their named tests. Then bind the DocsStore outbox projector to this helper and test crash-after-Loro-commit/before-SQLite-ack replay using the same IDs.
  - Generation/start/uncertain transitions and actual owner runner wiring remain separate unproven gates; do not claim these from projection tests.
- [ ] Commit this slice only after named implementation approval and its CI phase, scoped to store.rs. Never clear processed_commands or retry uncertain starts to make a test pass.

Validation already performed during planning: exact patch dry-run against stated source; copied actual DocsStore using real zeron-doc/proto dependencies,6 added tests and lint pass without stubs/blanket suppression. This is source-copy validation, not full project integration or real provider acceptance.

## D2. Freeze one implementable contract
- [ ] Record exact DTO fields/enums, state transitions, error classes and owning API boundaries in design.md. For a research-only unit, record actual provider/version observations and explicitly blocked decisions instead of inventing DTOs.
- [ ] Assign each C-scenario one exact native test path/name and its observable assertion. List existing files modified versus new files created, role of each file and shared-file conflicts with other changes.
- [ ] Enumerate crash points, concurrent callers, stale revisions, unauthorized caller, unavailable owner/provider and compatibility with older readers. Explain rollback using this design's explicit rule.
- [ ] Replace D-only tasks with atomic failing-test/run-red/minimal-code/run-green/commit steps using actual complete code and exact commands. Do not write a second plan file or mark implementation-ready while this step is incomplete.

## D3. Review and admission
- [ ] Self-review every PRD clause/C-scenario, all prohibited interpretations, type names across steps, reverse dependencies and rollback. An independent reviewer must challenge authority boundaries and whether the tests can pass without the intended behavior.
- [ ] Get the named change's written approval/readiness decision recorded in proposal.md. A changed public contract returns to review; do not treat a prior broad deployment mandate as approval for new product architecture.
- [ ] Run the planning validator from repository root:
```bash
python3 openspec/changes/prd-execution-map/validate.py
git diff --check
```
Expected: complete coverage/acyclic dependency/path checks pass, exit0; whitespace check exit0. This validates planning artifacts, not product functionality.

## Required implementation acceptance after refinement
- C01: Double-click/retried launch yields one run identity and one resource reservation.
- C02: Replacement adds linked session while preserving findings/history and allowed actions.
- C03: Investigation ends with checked findings and unresolved questions, without requiring code changes.
- C04: Direct session opens normally without automatic assignment creation.

## CI phase after every implementation iteration
- [ ] Run exact refined feature tests and core/affected-platform CI from `../prd-execution-map/design.md`. Verify at least one test actually selected; preserve failing evidence. No next iteration/round promotion while required checks fail or are missing.
- [ ] Run real acceptance: First real end-to-end investigation on harmless local repository: launch, stop, replace, restart, accepted findings; bounded authorized harness budget.
- [ ] Update this tasks.md with exact tested commit/tree, commands, counts, exit codes, evidence class, native environment and remaining blocks. Commit scoped files only, then CI on that integrated commit before downstream promotion.

## Rollback
Existing assignments remain records until explicit launch. Pause/hold active runs before downgrade; preserve run IDs and findings.
