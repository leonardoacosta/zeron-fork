# Validated profile identity and owner catalog execution contract

**Dependencies:** `ci-promotion-gates`. Only exact prerequisite promotion admits implementation.
**Status:** proposed; no runtime implementation authorization.

## A. Exact wire-contract slice (not full profile acceptance)
**Create:** `crates/proto/src/work_profile.rs`, wire validation only.
**Modify:** `crates/proto/src/lib.rs`, export module/types.
**Test:** inline module shown below. Existing serde/serde_json/uuid dependencies suffice; no Cargo dependency changes.

- [ ] Add the following test module to the new file first. Compile-red is expected because proposed types do not exist; this alone is not behavioral red proof.
```rust
#[cfg(test)]
mod tests {
    use super::*;
    const ID: &str = "e317f12a-17e1-4b0c-a56f-9502b870db9e";
    #[test]
    fn rejects_noncanonical_or_path_ids_on_wire() {
        for value in ["../other", "", "00000000-0000-0000-0000-000000000000", "E317F12A-17E1-4B0C-A56F-9502B870DB9E", "e317f12a17e14b0ca56f9502b870db9e"] {
            assert!(serde_json::from_value::<WorkProfileId>(serde_json::json!(value)).is_err());
        }
        assert_eq!(serde_json::from_value::<WorkProfileId>(serde_json::json!(ID)).unwrap().as_str(), ID);
    }
    #[test]
    fn rejects_revision_zero_overflow_and_fraction() {
        for value in [serde_json::json!(0), serde_json::json!(MAX_WORK_PROFILE_REVISION + 1), serde_json::json!(-1), serde_json::json!(1.5), serde_json::json!("1")] {
            assert!(serde_json::from_value::<WorkProfileRevision>(value).is_err());
        }
        assert!(WorkProfileRevision::try_from(MAX_WORK_PROFILE_REVISION).unwrap().checked_next().is_err());
        assert_eq!(WorkProfileRevision::try_from(1).unwrap().checked_next().unwrap().get(), 2);
    }
    #[test]
    fn names_are_metadata_not_fixed_profile_enum() {
        for value in ["Personal", "Priceless", "Brown", "Fourth profile", "研究"] {
            assert_eq!(WorkProfileName::try_from(value.to_owned()).unwrap().as_str(), value);
        }
        for value in ["".to_owned(), "  ".into(), " leading".into(), "trailing ".into(), "a\nb".into(), "界".repeat(86)] {
            assert!(WorkProfileName::try_from(value).is_err());
        }
    }
    #[test]
    fn binding_wire_and_rename_keep_original_identity() {
        let binding = WorkProfileBinding { profile_id: WorkProfileId::try_from(ID.to_owned()).unwrap(), revision: WorkProfileRevision::try_from(1).unwrap() };
        let original = WorkProfileRecord { binding: binding.clone(), display_name: WorkProfileName::try_from("Personal".to_owned()).unwrap() };
        let renamed = WorkProfileRecord { binding: WorkProfileBinding { revision: binding.revision.checked_next().unwrap(), ..binding.clone() }, display_name: WorkProfileName::try_from("Renamed".to_owned()).unwrap() };
        assert_eq!(original.binding.profile_id, renamed.binding.profile_id);
        assert_eq!(original.binding.revision.get(), 1);
        let wire = serde_json::to_value(WorkProfileSelection::Named(binding)).unwrap();
        assert_eq!(wire, serde_json::json!({"state":"named","binding":{"profileId":ID,"revision":1}}));
        assert!(serde_json::from_value::<WorkProfileSelection>(serde_json::json!({"state":"named"})).is_err());
        assert!(serde_json::from_value::<WorkProfileBinding>(serde_json::json!({"profileId":ID,"revision":1,"allowAll":true})).is_err());
    }
}
```
- [ ] Add `pub mod work_profile;` beside existing module declarations and `pub use work_profile::*;` beside reexports in `crates/proto/src/lib.rs`. Exact added lines:
```rust
pub mod work_profile;
pub use work_profile::*;
```
- [ ] Run `cargo test --locked -p zeron-proto --lib work_profile::tests`; expect missing-type compilation failure, not zero selected tests.
- [ ] Insert this complete implementation above the tests. Do not advertise a capability or alter runtime/store paths in this slice.
```rust
use serde::{Deserialize, Serialize};

pub const MAX_WORK_PROFILE_REVISION: u64 = 9_007_199_254_740_991;

#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
#[serde(try_from = "String", into = "String")]
pub struct WorkProfileId(String);

impl TryFrom<String> for WorkProfileId {
    type Error = String;
    fn try_from(value: String) -> Result<Self, Self::Error> {
        let id = uuid::Uuid::parse_str(&value).map_err(|_| "invalid work profile ID".to_owned())?;
        if id.is_nil() || id.hyphenated().to_string() != value {
            return Err("work profile ID must be a non-nil canonical UUID".into());
        }
        Ok(Self(value))
    }
}
impl From<WorkProfileId> for String {
    fn from(value: WorkProfileId) -> Self { value.0 }
}
impl WorkProfileId {
    pub fn as_str(&self) -> &str { &self.0 }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(try_from = "u64", into = "u64")]
pub struct WorkProfileRevision(u64);
impl TryFrom<u64> for WorkProfileRevision {
    type Error = String;
    fn try_from(value: u64) -> Result<Self, Self::Error> {
        if !(1..=MAX_WORK_PROFILE_REVISION).contains(&value) {
            return Err("work profile revision is outside interoperable range".into());
        }
        Ok(Self(value))
    }
}
impl From<WorkProfileRevision> for u64 {
    fn from(value: WorkProfileRevision) -> Self { value.0 }
}
impl WorkProfileRevision {
    pub fn get(self) -> u64 { self.0 }
    pub fn checked_next(self) -> Result<Self, String> { Self::try_from(self.0 + 1) }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct WorkProfileBinding {
    pub profile_id: WorkProfileId,
    pub revision: WorkProfileRevision,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(try_from = "String", into = "String")]
pub struct WorkProfileName(String);
impl TryFrom<String> for WorkProfileName {
    type Error = String;
    fn try_from(value: String) -> Result<Self, Self::Error> {
        if value.is_empty() || value.len() > 256 || value.trim() != value || value.chars().any(char::is_control) {
            return Err("invalid work profile display name".into());
        }
        Ok(Self(value))
    }
}
impl From<WorkProfileName> for String {
    fn from(value: WorkProfileName) -> Self { value.0 }
}
impl WorkProfileName {
    pub fn as_str(&self) -> &str { &self.0 }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct WorkProfileRecord {
    pub binding: WorkProfileBinding,
    pub display_name: WorkProfileName,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(tag = "state", content = "binding", rename_all = "camelCase", deny_unknown_fields)]
pub enum WorkProfileSelection {
    UnboundLegacy,
    Named(WorkProfileBinding),
}

```
- [ ] Run `cargo test --locked -p zeron-proto --lib work_profile::tests`; require four selected tests and four passes. Run complete `cargo test --locked -p zeron-proto` for compatibility.
- [ ] Establish behavioral negative control in an isolated scratch copy, never committed source: remove the canonical-ID equality check and confirm `rejects_noncanonical_or_path_ids_on_wire` fails. Restore exact implementation and require green. This verifies assertion sensitivity, not runtime profile isolation.
- [ ] Format only these files with `rustfmt --edition 2024 --config skip_children=true crates/proto/src/work_profile.rs crates/proto/src/lib.rs`, run required iteration CI, then scoped commit:
```bash
git add crates/proto/src/work_profile.rs crates/proto/src/lib.rs
git commit -m "feat(proto): define validated work profile bindings"
```

## B. Exact catalog persistence slice
**Create:** `crates/engine/src/work_profile_catalog.rs`. **Modify:** `crates/engine/src/lib.rs` adds private `mod work_profile_catalog;`. Engine already depends on rusqlite/sha2/serde/thiserror, so do not add a sync->proto runtime dependency or duplicate wire types. Catalog database is a separate owner-local file; it is not opened automatically until C integration is approved.

- [ ] Add test module first and module declaration; compile-red for missing definitions is preparatory only. Then add complete source below, which imports slice A's exact proto types.
```rust
use rusqlite::{Connection, OptionalExtension, TransactionBehavior, params};
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use std::path::Path;
use std::sync::{Mutex, MutexGuard, PoisonError};
use thiserror::Error;

use zeron_proto::{MAX_WORK_PROFILE_REVISION, WorkProfileBinding, WorkProfileId, WorkProfileName, WorkProfileRecord, WorkProfileRevision};

macro_rules! token_type {
    ($name:ident, $max:expr) => {
        #[derive(Debug, Clone, PartialEq, Eq, Hash)]
        pub struct $name(String);
        impl TryFrom<String> for $name {
            type Error = String;
            fn try_from(v: String) -> Result<Self, String> {
                if v.is_empty()
                    || v.len() > $max
                    || v.trim() != v
                    || v.chars().any(char::is_control)
                {
                    Err(concat!(stringify!($name), " invalid").into())
                } else {
                    Ok(Self(v))
                }
            }
        }
        impl $name {
            pub fn as_str(&self) -> &str {
                &self.0
            }
        }
    };
}
token_type!(PrincipalId, 256);
token_type!(ActorId, 256);
token_type!(OperationId, 128);

#[derive(Debug, Clone)]
pub struct CatalogPrincipal {
    pub principal_id: PrincipalId,
    pub actor_id: ActorId,
}
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(tag = "kind", rename_all = "camelCase", deny_unknown_fields)]
pub enum ProfileChange {
    Create {
        profile_id: WorkProfileId,
        display_name: WorkProfileName,
    },
    Rename {
        profile_id: WorkProfileId,
        expected_revision: WorkProfileRevision,
        display_name: WorkProfileName,
    },
}
#[derive(Debug, Clone)]
pub struct CatalogMutation {
    pub operation_id: OperationId,
    pub change: ProfileChange,
}
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct MutationResult {
    pub record: WorkProfileRecord,
}

#[derive(Debug, Error)]
pub enum CatalogError {
    #[error(transparent)]
    Sqlite(#[from] rusqlite::Error),
    #[error("catalog mutex poisoned")]
    Poisoned,
    #[error("operation ID reused with different request")]
    OperationIdConflict,
    #[error("profile already exists")]
    AlreadyExists,
    #[error("profile not found")]
    NotFound,
    #[error("profile revision stale: expected {expected}, actual {actual}")]
    Stale { expected: u64, actual: u64 },
    #[error("revision exhausted")]
    RevisionExhausted,
    #[error("catalog schema version {found} is newer than supported {supported}")]
    FutureSchema { found: i64, supported: i64 },
    #[error("invalid stored data: {0}")]
    Corrupt(String),
}

const SCHEMA_VERSION: i64 = 1;
const SCHEMA: &str = r#"
CREATE TABLE work_profiles (
 principal_id TEXT NOT NULL CHECK(length(principal_id) BETWEEN 1 AND 256),
 profile_id TEXT NOT NULL CHECK(length(profile_id)=36 AND profile_id=lower(profile_id) AND substr(profile_id,9,1)='-' AND substr(profile_id,14,1)='-' AND substr(profile_id,19,1)='-' AND substr(profile_id,24,1)='-'),
 display_name TEXT NOT NULL CHECK(length(CAST(display_name AS BLOB)) BETWEEN 1 AND 256),
 revision INTEGER NOT NULL CHECK(revision BETWEEN 1 AND 9007199254740991),
 PRIMARY KEY(principal_id,profile_id)
) STRICT;
CREATE TABLE work_profile_mutations (
 principal_id TEXT NOT NULL,
 actor_id TEXT NOT NULL,
 operation_id TEXT NOT NULL,
 request_hash BLOB NOT NULL CHECK(length(request_hash)=32),
 result_json TEXT NOT NULL,
 PRIMARY KEY(principal_id,actor_id,operation_id)
) STRICT;
"#;

pub struct WorkProfileCatalogStore {
    conn: Mutex<Connection>,
}
impl WorkProfileCatalogStore {
    pub fn open(path: impl AsRef<Path>) -> Result<Self, CatalogError> {
        let mut conn = Connection::open(path)?;
        let version: i64 = conn.pragma_query_value(None, "user_version", |r| r.get(0))?;
        if version > SCHEMA_VERSION {
            return Err(CatalogError::FutureSchema {
                found: version,
                supported: SCHEMA_VERSION,
            });
        }
        if version == 0 {
            let tx = conn.transaction_with_behavior(TransactionBehavior::Immediate)?;
            let locked_version: i64 = tx.pragma_query_value(None, "user_version", |r| r.get(0))?;
            if locked_version > SCHEMA_VERSION {
                return Err(CatalogError::FutureSchema {
                    found: locked_version,
                    supported: SCHEMA_VERSION,
                });
            }
            if locked_version == 0 {
                tx.execute_batch(SCHEMA)?;
                tx.pragma_update(None, "user_version", SCHEMA_VERSION)?;
            }
            tx.commit()?;
        }
        conn.pragma_update(None, "journal_mode", "WAL")?;
        conn.pragma_update(None, "synchronous", "NORMAL")?;
        conn.busy_timeout(std::time::Duration::from_secs(5))?;
        Ok(Self {
            conn: Mutex::new(conn),
        })
    }
    fn conn(&self) -> Result<MutexGuard<'_, Connection>, CatalogError> {
        self.conn
            .lock()
            .map_err(|_: PoisonError<_>| CatalogError::Poisoned)
    }
    pub fn list(
        &self,
        principal: &CatalogPrincipal,
    ) -> Result<Vec<WorkProfileRecord>, CatalogError> {
        let conn = self.conn()?;
        let mut stmt = conn.prepare("SELECT profile_id,display_name,revision FROM work_profiles WHERE principal_id=?1 ORDER BY profile_id")?;
        let rows = stmt.query_map([principal.principal_id.as_str()], |r| {
            Ok((
                r.get::<_, String>(0)?,
                r.get::<_, String>(1)?,
                r.get::<_, i64>(2)?,
            ))
        })?;
        rows.map(|row| {
            let (id, name, revision) = row?;
            record(id, name, revision)
        })
        .collect()
    }
    pub fn mutate(
        &self,
        principal: &CatalogPrincipal,
        mutation: &CatalogMutation,
    ) -> Result<MutationResult, CatalogError> {
        let request = serde_json::to_vec(&mutation.change)
            .map_err(|e| CatalogError::Corrupt(e.to_string()))?;
        let digest: [u8; 32] = Sha256::digest(&request).into();
        let mut conn = self.conn()?;
        let tx = conn.transaction_with_behavior(TransactionBehavior::Immediate)?;
        let prior: Option<(Vec<u8>,String)> = tx.query_row(
            "SELECT request_hash,result_json FROM work_profile_mutations WHERE principal_id=?1 AND actor_id=?2 AND operation_id=?3",
            params![principal.principal_id.as_str(),principal.actor_id.as_str(),mutation.operation_id.as_str()],
            |r| Ok((r.get(0)?,r.get(1)?)),
        ).optional()?;
        if let Some((saved, result)) = prior {
            if saved.as_slice() != digest {
                return Err(CatalogError::OperationIdConflict);
            }
            return serde_json::from_str(&result).map_err(|e| CatalogError::Corrupt(e.to_string()));
        }
        let result_record = match &mutation.change {
            ProfileChange::Create {
                profile_id,
                display_name,
            } => {
                let revision = WorkProfileRevision::try_from(1).map_err(CatalogError::Corrupt)?;
                tx.execute(
                    "INSERT INTO work_profiles VALUES (?1,?2,?3,1)",
                    params![
                        principal.principal_id.as_str(),
                        profile_id.as_str(),
                        display_name.as_str()
                    ],
                )
                .map_err(|e| {
                    if is_unique_violation(&e) {
                        CatalogError::AlreadyExists
                    } else {
                        CatalogError::Sqlite(e)
                    }
                })?;
                WorkProfileRecord {
                    binding: WorkProfileBinding {
                        profile_id: profile_id.clone(),
                        revision,
                    },
                    display_name: display_name.clone(),
                }
            }
            ProfileChange::Rename {
                profile_id,
                expected_revision,
                display_name,
            } => {
                let actual: Option<i64> = tx.query_row("SELECT revision FROM work_profiles WHERE principal_id=?1 AND profile_id=?2",params![principal.principal_id.as_str(),profile_id.as_str()],|r|r.get(0)).optional()?;
                let actual = actual.ok_or(CatalogError::NotFound)? as u64;
                if actual != expected_revision.get() {
                    return Err(CatalogError::Stale {
                        expected: expected_revision.get(),
                        actual,
                    });
                }
                let next = expected_revision
                    .checked_next()
                    .map_err(|_| CatalogError::RevisionExhausted)?;
                let changed = tx.execute("UPDATE work_profiles SET display_name=?3,revision=?4 WHERE principal_id=?1 AND profile_id=?2 AND revision=?5",params![principal.principal_id.as_str(),profile_id.as_str(),display_name.as_str(),next.get() as i64,expected_revision.get() as i64])?;
                if changed != 1 {
                    return Err(CatalogError::Stale {
                        expected: expected_revision.get(),
                        actual,
                    });
                }
                WorkProfileRecord {
                    binding: WorkProfileBinding {
                        profile_id: profile_id.clone(),
                        revision: next,
                    },
                    display_name: display_name.clone(),
                }
            }
        };
        let result = MutationResult {
            record: result_record,
        };
        let json =
            serde_json::to_string(&result).map_err(|e| CatalogError::Corrupt(e.to_string()))?;
        tx.execute(
            "INSERT INTO work_profile_mutations VALUES (?1,?2,?3,?4,?5)",
            params![
                principal.principal_id.as_str(),
                principal.actor_id.as_str(),
                mutation.operation_id.as_str(),
                digest.as_slice(),
                json
            ],
        )?;
        tx.commit()?;
        Ok(result)
    }
}
fn is_unique_violation(e: &rusqlite::Error) -> bool {
    matches!(e, rusqlite::Error::SqliteFailure(x,_) if x.extended_code==rusqlite::ffi::SQLITE_CONSTRAINT_PRIMARYKEY || x.extended_code==rusqlite::ffi::SQLITE_CONSTRAINT_UNIQUE)
}
fn record(id: String, name: String, revision: i64) -> Result<WorkProfileRecord, CatalogError> {
    let profile_id = WorkProfileId::try_from(id).map_err(CatalogError::Corrupt)?;
    let display_name = WorkProfileName::try_from(name).map_err(CatalogError::Corrupt)?;
    let revision = WorkProfileRevision::try_from(revision as u64).map_err(CatalogError::Corrupt)?;
    Ok(WorkProfileRecord {
        binding: WorkProfileBinding {
            profile_id,
            revision,
        },
        display_name,
    })
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::sync::{Arc, Barrier};
    use tempfile::tempdir;
    const ID1: &str = "e317f12a-17e1-4b0c-a56f-9502b870db9e";
    const ID2: &str = "b317f12a-17e1-4b0c-a56f-9502b870db9e";
    fn principal(user: &str, actor: &str) -> CatalogPrincipal {
        CatalogPrincipal {
            principal_id: PrincipalId::try_from(user.to_owned()).unwrap(),
            actor_id: ActorId::try_from(actor.to_owned()).unwrap(),
        }
    }
    fn id(s: &str) -> WorkProfileId {
        WorkProfileId::try_from(s.to_owned()).unwrap()
    }
    fn name(s: &str) -> WorkProfileName {
        WorkProfileName::try_from(s.to_owned()).unwrap()
    }
    fn op(s: &str) -> OperationId {
        OperationId::try_from(s.to_owned()).unwrap()
    }
    fn create(id_s: &str, op_s: &str, label: &str) -> CatalogMutation {
        CatalogMutation {
            operation_id: op(op_s),
            change: ProfileChange::Create {
                profile_id: id(id_s),
                display_name: name(label),
            },
        }
    }
    fn rename(id_s: &str, rev: u64, op_s: &str, label: &str) -> CatalogMutation {
        CatalogMutation {
            operation_id: op(op_s),
            change: ProfileChange::Rename {
                profile_id: id(id_s),
                expected_revision: rev.try_into().unwrap(),
                display_name: name(label),
            },
        }
    }

    #[test]
    fn actor_principal_replay_payload_and_reopen() {
        let d = tempdir().unwrap();
        let db = d.path().join("catalog.db");
        let p = principal("user", "actor");
        let m = create(ID1, "op", "A");
        let result = {
            let s = WorkProfileCatalogStore::open(&db).unwrap();
            let r = s.mutate(&p, &m).unwrap();
            assert_eq!(s.mutate(&p, &m).unwrap(), r);
            assert!(matches!(
                s.mutate(&p, &create(ID1, "op", "Changed")),
                Err(CatalogError::OperationIdConflict)
            ));
            r
        };
        let s = WorkProfileCatalogStore::open(&db).unwrap();
        assert_eq!(s.mutate(&p, &m).unwrap(), result);
        let other_actor = principal("user", "other-actor");
        s.mutate(&other_actor, &create(ID2, "op", "B")).unwrap();
        let other_principal = principal("other-user", "actor");
        s.mutate(&other_principal, &create(ID1, "op", "C")).unwrap();
        assert_eq!(s.list(&p).unwrap().len(), 2);
        assert_eq!(s.list(&other_principal).unwrap().len(), 1);
    }
    #[test]
    fn per_profile_cas_and_stale_does_not_change_row() {
        let d = tempdir().unwrap();
        let s = WorkProfileCatalogStore::open(d.path().join("c.db")).unwrap();
        let p = principal("u", "a");
        s.mutate(&p, &create(ID1, "c1", "A")).unwrap();
        s.mutate(&p, &create(ID2, "c2", "B")).unwrap();
        let r = s.mutate(&p, &rename(ID1, 1, "r1", "A2")).unwrap();
        assert_eq!(r.record.binding.revision.get(), 2);
        assert!(matches!(
            s.mutate(&p, &rename(ID1, 1, "r2", "bad")),
            Err(CatalogError::Stale {
                expected: 1,
                actual: 2
            })
        ));
        assert_eq!(
            s.list(&p)
                .unwrap()
                .iter()
                .find(|x| x.binding.profile_id.as_str() == ID1)
                .unwrap()
                .display_name
                .as_str(),
            "A2"
        );
        assert_eq!(
            s.list(&p)
                .unwrap()
                .iter()
                .find(|x| x.binding.profile_id.as_str() == ID2)
                .unwrap()
                .binding
                .revision
                .get(),
            1
        );
    }
    #[test]
    fn sql_trigger_failure_rolls_back_row_and_receipt_even_after_reopen() {
        let d = tempdir().unwrap();
        let db = d.path().join("c.db");
        let p = principal("u", "a");
        let s = WorkProfileCatalogStore::open(&db).unwrap();
        s.conn().unwrap().execute_batch("CREATE TRIGGER reject_receipt BEFORE INSERT ON work_profile_mutations BEGIN SELECT RAISE(ABORT, 'injected receipt failure'); END;").unwrap();
        assert!(matches!(
            s.mutate(&p, &create(ID1, "fault", "A")),
            Err(CatalogError::Sqlite(_))
        ));
        assert!(s.list(&p).unwrap().is_empty());
        drop(s);
        let reopened = WorkProfileCatalogStore::open(&db).unwrap();
        assert!(reopened.list(&p).unwrap().is_empty());
        reopened
            .conn()
            .unwrap()
            .execute_batch("DROP TRIGGER reject_receipt;")
            .unwrap();
        assert_eq!(
            reopened
                .mutate(&p, &create(ID1, "fault", "A"))
                .unwrap()
                .record
                .binding
                .revision
                .get(),
            1
        );
    }
    #[test]
    fn two_connections_competing_same_revision_exactly_one_wins() {
        let d = tempdir().unwrap();
        let db = d.path().join("c.db");
        let p = principal("u", "a");
        let setup = WorkProfileCatalogStore::open(&db).unwrap();
        setup.mutate(&p, &create(ID1, "create", "A")).unwrap();
        drop(setup);
        let s1 = Arc::new(WorkProfileCatalogStore::open(&db).unwrap());
        let s2 = Arc::new(WorkProfileCatalogStore::open(&db).unwrap());
        let barrier = Arc::new(Barrier::new(3));
        let go = |s: Arc<WorkProfileCatalogStore>,
                  actor: &'static str,
                  label: &'static str,
                  barrier: Arc<Barrier>| {
            std::thread::Builder::new()
                .spawn(move || {
                    let p = principal("u", actor);
                    let m = rename(ID1, 1, actor, label);
                    barrier.wait();
                    s.mutate(&p, &m)
                })
                .unwrap()
        };
        let t1 = go(s1, "a1", "first", barrier.clone());
        let t2 = go(s2, "a2", "second", barrier.clone());
        barrier.wait();
        let r1 = t1.join().unwrap();
        let r2 = t2.join().unwrap();
        assert_eq!(usize::from(r1.is_ok()) + usize::from(r2.is_ok()), 1);
        assert_eq!(
            usize::from(matches!(r1, Err(CatalogError::Stale { .. })))
                + usize::from(matches!(r2, Err(CatalogError::Stale { .. }))),
            1
        );
        let final_store = WorkProfileCatalogStore::open(&db).unwrap();
        assert_eq!(final_store.list(&p).unwrap()[0].binding.revision.get(), 2);
    }
    #[test]
    fn rejects_future_schema_without_modifying_it() {
        let d = tempdir().unwrap();
        let db = d.path().join("future.db");
        let c = Connection::open(&db).unwrap();
        c.pragma_update(None, "user_version", 99).unwrap();
        let before: String = c
            .pragma_query_value(None, "journal_mode", |r| r.get(0))
            .unwrap();
        drop(c);
        let before_bytes = std::fs::read(&db).unwrap();
        assert!(matches!(
            WorkProfileCatalogStore::open(&db),
            Err(CatalogError::FutureSchema {
                found: 99,
                supported: 1
            })
        ));
        assert_eq!(std::fs::read(&db).unwrap(), before_bytes);
        let c = Connection::open(&db).unwrap();
        let mode: String = c
            .pragma_query_value(None, "journal_mode", |r| r.get(0))
            .unwrap();
        assert_eq!(mode, before);
        let version: i64 = c
            .pragma_query_value(None, "user_version", |r| r.get(0))
            .unwrap();
        assert_eq!(version, 99);
        let tables: i64 = c
            .query_row(
                "SELECT count(*) FROM sqlite_master WHERE type='table' AND name='work_profiles'",
                [],
                |r| r.get(0),
            )
            .unwrap();
        assert_eq!(tables, 0);
    }
    #[test]
    fn poison_is_reported_not_silently_recovered() {
        let d = tempdir().unwrap();
        let s = Arc::new(WorkProfileCatalogStore::open(d.path().join("c.db")).unwrap());
        let poisoned = std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| {
            let _guard = s.conn.lock().unwrap();
            std::panic::resume_unwind(Box::new("poison test"));
        }));
        assert!(poisoned.is_err());
        assert!(matches!(
            s.list(&principal("u", "a")),
            Err(CatalogError::Poisoned)
        ));
    }
    #[test]
    fn tokens_reject_surrounding_whitespace() {
        assert!(PrincipalId::try_from(" user".to_owned()).is_err());
        assert!(ActorId::try_from("actor ".to_owned()).is_err());
        assert!(OperationId::try_from(" op".to_owned()).is_err());
        assert!(PrincipalId::try_from("\t".to_owned()).is_err());
        assert_eq!(
            OperationId::try_from("op-1".to_owned()).unwrap().as_str(),
            "op-1"
        );
    }
}
```
- [ ] Run `cargo test --locked -p zeron-engine --lib work_profile_catalog::tests`; require7 catalog tests, including two-connection CAS, actual trigger rollback/reopen, future schema no-mutation, poison denial and scoped replay. Full scratch prototype ran11 tests including4 shared wire tests; production filtered catalog run must select7, not11.
- [ ] Behavioral negative control: in scratch remove expected_revision comparison and prove concurrent/stale tests fail; restore. Do not inject a production fault boolean to make rollback tests pass. SQL trigger is test-only and must be removed/reopen verified within fixture.
- [ ] Format exact owned files and commit only module+declaration after core CI. This catalog does not authorize its caller: CatalogPrincipal must come from owner context. No external RPC takes arbitrary principal/actor from JSON.


## Required scenarios
- C01: Invalid UUID/revision/name rejects during wire decoding before catalog write.
- C02: Same operation identity and payload replays exact result; changed payload conflicts without mutation.
- C03: Two connections rename the same revision: exactly one wins, history of receipts survives reopen.
- C04: Late SQL failure rolls back row and receipt; future schema rejected without modifying database.

## CI phase after every implementation iteration
Run exact feature tests plus required round CI from `../prd-execution-map/design.md`, bind evidence to integrated revision, no missing/failed/stale promotion.

## Rollback
Additive unused catalog only; do not advertise runtime capability. Future schema refused before mutation; retain legacy stores unchanged.
