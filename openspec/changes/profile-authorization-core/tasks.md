# Owner policy core execution contract

**Dependencies:** `work-profile-catalog`

## Low-context execution order
Read only the current numbered step and its complete referenced Rust block. Do not implement the entire file in one turn. Before every commit re-read the scoped diff and required check output. The complete code blocks are literal proposed target contents, not permission to skip the test-first sequence.

1. Extract the test module from slice A into the exact target file, add its module declaration, and record the expected missing-definition red.
2. Add slice A definitions above that same test module, not a duplicated test module. Run the exact focused test command/count. If compiler imports differ, stop and correct this contract before proceeding.
3. Run slice A's negative-control mutation in scratch, restore, rerun green and formatting. Do not promote unused production modules alone when required lint fails; keep consumer integration in the same approved change.
4. Extract slice B test module, then its complete implementation. Reuse upstream proto/evaluator types exactly; do not recreate look-alike structs to get compilation green.
5. Run slice B tests and combined A+B tests. Fault/concurrency tests must run, not just compile. Record selected counts and all warnings.
6. Run complete changed-crate and round CI, then independent contract/security review before scoped commit/promotion. Hosted acceptance is separately required where stated.

The unit remains gated if any later integration step is unresolved. A helper passing isolated tests is not the full feature. Never invent new source files or API names beyond those explicitly listed below.

## A. Exact synchronous authorization core proposal
**Create:** `crates/engine/src/work_authorization.rs`. **Modify:** `crates/engine/src/lib.rs` adds private `mod work_authorization;`. Reuse proposed proto profile types; no provider calls or credential values in this module.

- [ ] Add tests first then complete definitions below. `cargo test --locked -p zeron-engine --lib work_authorization::tests` must select10 tests and pass. The test closure counts admission only, not provider effects.
```rust
#![forbid(unsafe_code)]

use std::collections::HashMap;
use std::sync::{Arc, RwLock};
use zeron_proto::{WorkProfileBinding, WorkProfileId, WorkProfileSelection};

#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct Principal {
    pub org_id: String,
    pub user_id: String,
}

#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub enum Operation {
    ReadSession,
    MutateSession,
    RunSession,
    SteerSession,
    ReadRepository,
    MutateRepository,
    OpenTerminal,
    WriteTerminal,
    ObserveTerminal,
    CloseTerminal,
    ReadUpload,
    SelectAgentAccount,
    ManageAgentLogin,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Resource {
    Session {
        id: String,
        binding: WorkProfileBinding,
    },
    Repository {
        canonical_root: String,
        repository_id: String,
    },
    Terminal {
        id: String,
        creator: WorkProfileBinding,
        generation: u64,
    },
    Upload {
        id: String,
        binding: WorkProfileBinding,
        canonical_root: String,
    },
    AgentAccount {
        harness: String,
        slot_ref: String,
        principal: Principal,
    },
}
impl Resource {
    fn binding(&self) -> Option<&WorkProfileBinding> {
        match self {
            Self::Session { binding, .. } | Self::Upload { binding, .. } => Some(binding),
            Self::Terminal { creator, .. } => Some(creator),
            Self::Repository { .. } | Self::AgentAccount { .. } => None,
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Grant {
    pub operation: Operation,
    pub resource: Resource,
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Denial {
    CapabilityUnavailable,
    UnboundLegacy,
    MigrationRequired,
    ProfileMismatch,
    StalePolicy,
    ResourceDenied,
    ResourceUnresolved,
    PolicyUnavailable,
}
/// Engine-owned request. Never deserialize this from RPC JSON.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Request {
    pub selection: WorkProfileSelection,
    pub principal: Principal,
    pub expected_policy_revision: u64,
    pub operation: Operation,
    pub resource: Option<Resource>,
    pub migration_required: bool,
    pub unresolved: bool,
}
#[derive(Debug, Clone)]
struct Policy {
    revision: u64,
    grants: Vec<Grant>,
}
#[derive(Debug, Default)]
struct State {
    policies: HashMap<(Principal, WorkProfileId), Policy>,
}
#[derive(Debug, Clone)]
pub struct WorkAuthorizer {
    state: Arc<RwLock<State>>,
    available: bool,
}
impl Default for WorkAuthorizer {
    fn default() -> Self {
        Self::new()
    }
}

impl WorkAuthorizer {
    pub fn new() -> Self {
        Self {
            state: Arc::new(RwLock::new(State::default())),
            available: true,
        }
    }
    #[cfg(test)]
    fn unavailable() -> Self {
        Self {
            state: Arc::new(RwLock::new(State::default())),
            available: false,
        }
    }

    pub fn replace_policy(
        &self,
        principal: Principal,
        binding: &WorkProfileBinding,
        revision: u64,
        grants: Vec<Grant>,
    ) -> Result<(), Denial> {
        if revision == 0 || revision > zeron_proto::MAX_WORK_PROFILE_REVISION {
            return Err(Denial::StalePolicy);
        }
        let mut state = self.state.write().map_err(|_| Denial::PolicyUnavailable)?;
        let key = (principal, binding.profile_id.clone());
        if let Some(current) = state.policies.get(&key) {
            if revision < current.revision {
                return Err(Denial::StalePolicy);
            }
            if revision == current.revision {
                return if current.grants == grants {
                    Ok(())
                } else {
                    Err(Denial::StalePolicy)
                };
            }
        }
        state.policies.insert(key, Policy { revision, grants });
        Ok(())
    }

    pub fn authorize(&self, request: &Request) -> Result<AuthorizationPermit, Denial> {
        if !self.available {
            return Err(Denial::CapabilityUnavailable);
        }
        let binding = match &request.selection {
            WorkProfileSelection::Named(binding) => binding,
            WorkProfileSelection::UnboundLegacy => return Err(Denial::UnboundLegacy),
        };
        if request.migration_required {
            return Err(Denial::MigrationRequired);
        }
        if request.unresolved {
            return Err(Denial::ResourceUnresolved);
        }
        let resource = request
            .resource
            .as_ref()
            .ok_or(Denial::ResourceUnresolved)?;
        if resource.binding().is_some_and(|rb| rb != binding) {
            return Err(Denial::ProfileMismatch);
        }
        if let Resource::AgentAccount { principal, .. } = resource
            && principal != &request.principal
        {
            return Err(Denial::ProfileMismatch);
        }
        let state = self.state.read().map_err(|_| Denial::PolicyUnavailable)?;
        let key = (request.principal.clone(), binding.profile_id.clone());
        let policy = state.policies.get(&key).ok_or(Denial::StalePolicy)?;
        if policy.revision != request.expected_policy_revision {
            return Err(Denial::StalePolicy);
        }
        let grant = Grant {
            operation: request.operation.clone(),
            resource: resource.clone(),
        };
        if !policy.grants.contains(&grant) {
            return Err(Denial::ResourceDenied);
        }
        Ok(AuthorizationPermit {
            binding: binding.clone(),
            principal: request.principal.clone(),
            policy_revision: policy.revision,
            operation: request.operation.clone(),
            resource: resource.clone(),
            seal: Arc::clone(&self.state),
        })
    }

    /// Validate and admit a synchronous effect while holding a read lock against
    /// policy replacement. The closure must be short, synchronous, and must not
    /// re-enter this authorizer. Async work must use a separate generation/lease protocol.
    pub fn with_authorized_effect<T>(
        &self,
        permit: AuthorizationPermit,
        binding: &WorkProfileBinding,
        operation: &Operation,
        resource: &Resource,
        effect: impl FnOnce() -> T,
    ) -> Result<T, Denial> {
        if !self.available {
            return Err(Denial::CapabilityUnavailable);
        }
        if !Arc::ptr_eq(&permit.seal, &self.state) {
            return Err(Denial::ResourceDenied);
        }
        if (&permit.binding, &permit.operation, &permit.resource) != (binding, operation, resource)
        {
            return Err(Denial::ProfileMismatch);
        }
        let state = self.state.read().map_err(|_| Denial::PolicyUnavailable)?;
        let key = (permit.principal, binding.profile_id.clone());
        let policy = state.policies.get(&key).ok_or(Denial::StalePolicy)?;
        if policy.revision != permit.policy_revision {
            return Err(Denial::StalePolicy);
        }
        if !policy.grants.contains(&Grant {
            operation: operation.clone(),
            resource: resource.clone(),
        }) {
            return Err(Denial::ResourceDenied);
        }
        Ok(effect())
    }
}

/// Private fields; no serde, Clone, or public constructor. Local ephemeral capability.
pub struct AuthorizationPermit {
    binding: WorkProfileBinding,
    principal: Principal,
    policy_revision: u64,
    operation: Operation,
    resource: Resource,
    seal: Arc<RwLock<State>>,
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::sync::{
        atomic::{AtomicBool, Ordering},
        mpsc,
    };
    use std::thread;

    fn fixture() -> (
        WorkAuthorizer,
        Principal,
        WorkProfileBinding,
        Resource,
        Operation,
    ) {
        let auth = WorkAuthorizer::new();
        let principal = Principal {
            org_id: "org-a".into(),
            user_id: "user-a".into(),
        };
        let binding = WorkProfileBinding {
            profile_id: WorkProfileId::try_from("e317f12a-17e1-4b0c-a56f-9502b870db9e".to_owned())
                .unwrap(),
            revision: zeron_proto::WorkProfileRevision::try_from(1).unwrap(),
        };
        let resource = Resource::Session {
            id: "chat-1".into(),
            binding: binding.clone(),
        };
        let operation = Operation::RunSession;
        auth.replace_policy(
            principal.clone(),
            &binding,
            8,
            vec![Grant {
                operation: operation.clone(),
                resource: resource.clone(),
            }],
        )
        .unwrap();
        (auth, principal, binding, resource, operation)
    }
    fn request(
        principal: Principal,
        binding: WorkProfileBinding,
        resource: Option<Resource>,
        operation: Operation,
        revision: u64,
    ) -> Request {
        Request {
            selection: WorkProfileSelection::Named(binding),
            principal,
            expected_policy_revision: revision,
            operation,
            resource,
            migration_required: false,
            unresolved: false,
        }
    }

    #[test]
    fn exact_grant_permit_admits_matching_synchronous_effect() {
        let (auth, p, b, r, op) = fixture();
        let permit = auth
            .authorize(&request(p, b.clone(), Some(r.clone()), op.clone(), 8))
            .unwrap();
        assert_eq!(
            auth.with_authorized_effect(permit, &b, &op, &r, || 41 + 1),
            Ok(42)
        );
    }
    #[test]
    fn permit_binds_operation_resource_and_evaluator() {
        let (auth, p, b, r, op) = fixture();
        let permit = auth
            .authorize(&request(p, b.clone(), Some(r.clone()), op.clone(), 8))
            .unwrap();
        assert_eq!(
            auth.with_authorized_effect(permit, &b, &Operation::MutateSession, &r, || ()),
            Err(Denial::ProfileMismatch)
        );
    }
    #[test]
    fn missing_grant_and_stale_revision_deny() {
        let (auth, p, b, r, _) = fixture();
        assert_eq!(
            auth.authorize(&request(
                p.clone(),
                b.clone(),
                Some(r.clone()),
                Operation::MutateSession,
                8
            ))
            .err(),
            Some(Denial::ResourceDenied)
        );
        assert_eq!(
            auth.authorize(&request(p, b, Some(r), Operation::RunSession, 7))
                .err(),
            Some(Denial::StalePolicy)
        );
    }
    #[test]
    fn unbound_migration_missing_policy_and_unavailable_deny() {
        let (auth, p, b, r, op) = fixture();
        let mut req = request(p.clone(), b.clone(), Some(r.clone()), op.clone(), 8);
        req.selection = WorkProfileSelection::UnboundLegacy;
        assert_eq!(auth.authorize(&req).err(), Some(Denial::UnboundLegacy));
        req.selection = WorkProfileSelection::Named(b.clone());
        req.migration_required = true;
        assert_eq!(auth.authorize(&req).err(), Some(Denial::MigrationRequired));
        req.migration_required = false;
        req.expected_policy_revision = 9;
        assert_eq!(auth.authorize(&req).err(), Some(Denial::StalePolicy));
        assert_eq!(
            WorkAuthorizer::unavailable()
                .authorize(&request(p, b, Some(r), op, 8))
                .err(),
            Some(Denial::CapabilityUnavailable)
        );
    }
    #[test]
    fn unresolved_and_foreign_bound_resources_deny() {
        let (auth, p, b, r, op) = fixture();
        let mut req = request(p, b.clone(), Some(r.clone()), op, 8);
        req.resource = None;
        req.unresolved = true;
        assert_eq!(auth.authorize(&req).err(), Some(Denial::ResourceUnresolved));
        req.resource = Some(Resource::Session {
            id: "foreign".into(),
            binding: WorkProfileBinding {
                revision: zeron_proto::WorkProfileRevision::try_from(2).unwrap(),
                ..b
            },
        });
        req.unresolved = false;
        assert_eq!(auth.authorize(&req).err(), Some(Denial::ProfileMismatch));
    }
    #[test]
    fn different_principal_does_not_inherit_grant() {
        let (auth, p, b, r, op) = fixture();
        let other = Principal {
            org_id: p.org_id,
            user_id: "other".into(),
        };
        assert_eq!(
            auth.authorize(&request(other, b, Some(r), op, 8)).err(),
            Some(Denial::StalePolicy)
        );
    }
    #[test]
    fn revoked_permit_denied_before_effect() {
        let (auth, p, b, r, op) = fixture();
        let permit = auth
            .authorize(&request(
                p.clone(),
                b.clone(),
                Some(r.clone()),
                op.clone(),
                8,
            ))
            .unwrap();
        auth.replace_policy(p, &b, 9, Vec::new()).unwrap();
        let ran = AtomicBool::new(false);
        assert_eq!(
            auth.with_authorized_effect(permit, &b, &op, &r, || ran.store(true, Ordering::SeqCst)),
            Err(Denial::StalePolicy)
        );
        assert!(!ran.load(Ordering::SeqCst));
    }
    #[test]
    fn revocation_cannot_interleave_with_synchronous_admission() {
        let (auth, p, b, r, op) = fixture();
        let permit = auth
            .authorize(&request(
                p.clone(),
                b.clone(),
                Some(r.clone()),
                op.clone(),
                8,
            ))
            .unwrap();
        let (effect_entered_tx, effect_entered_rx) = mpsc::channel();
        let (release_tx, release_rx) = mpsc::channel();
        let worker_auth = auth.clone();
        let wb = b.clone();
        let wr = r.clone();
        let wo = op.clone();
        let worker = thread::spawn(move || {
            worker_auth
                .with_authorized_effect(permit, &wb, &wo, &wr, || {
                    effect_entered_tx.send(()).unwrap();
                    release_rx.recv().unwrap();
                    "effect"
                })
                .unwrap()
        });
        effect_entered_rx.recv().unwrap(); // Read lock is held inside the effect closure.
        let (attempt_tx, attempt_rx) = mpsc::channel();
        let (done_tx, done_rx) = mpsc::channel();
        let revoke_auth = auth.clone();
        let revoker = thread::spawn(move || {
            attempt_tx.send(()).unwrap();
            revoke_auth.replace_policy(p, &b, 9, Vec::new()).unwrap();
            done_tx.send(()).unwrap();
        });
        attempt_rx.recv().unwrap();
        assert!(
            done_rx.try_recv().is_err(),
            "revocation cannot complete while effect admission lock is held"
        );
        release_tx.send(()).unwrap();
        assert_eq!(worker.join().unwrap(), "effect");
        done_rx.recv().unwrap();
        revoker.join().unwrap();
    }
    #[test]
    fn poisoned_policy_lock_denies_instead_of_panicking() {
        let (auth, p, b, r, op) = fixture();
        let state = Arc::clone(&auth.state);
        let _ = thread::spawn(move || {
            let _guard = state.write().unwrap();
            panic!("poison test")
        })
        .join();
        assert_eq!(
            auth.authorize(&request(
                p.clone(),
                b.clone(),
                Some(r.clone()),
                op.clone(),
                8
            ))
            .err(),
            Some(Denial::PolicyUnavailable)
        );
        assert_eq!(
            auth.replace_policy(p, &b, 9, Vec::new()),
            Err(Denial::PolicyUnavailable)
        );
    }

    #[test]
    fn same_revision_publication_is_idempotent_only_for_identical_grants() {
        let (authorizer, principal, binding, resource, operation) = fixture();
        let grant = Grant { operation, resource };
        assert_eq!(authorizer.replace_policy(principal.clone(), &binding, 8, vec![grant]), Ok(()));
        assert_eq!(authorizer.replace_policy(principal, &binding, 8, Vec::new()), Err(Denial::StalePolicy));
    }
}
```
- [ ] Behavioral negative control in scratch: remove policy revision comparison in `with_authorized_effect`; revoked-permit test must fail with closure wrongly invoked. Restore. Lock poison must return PolicyUnavailable, not panic or recover unsafe policy.
- [ ] Keep policy replacement and effect admission serialized. The closure must be short/synchronous and non-reentrant; never await while holding the lock. Async work needs generation-scoped cancellation/recheck at each effect boundary, not a promise that one admission check authorizes all future work.
- [ ] This is an in-memory proposed evaluator only. Before full runtime use, define durable policy/CAS, validated principal/resource constructors, actual canonical path resolution, credential containment, safe RPC error mapping and every integration site in design.md. Public fields are internal construction conveniences, never deserialize Request/Grant from an untrusted RPC as authority. No named-profile execution capability before those gates pass.


## B. Durable policy snapshot and revocation integration
**Create:** `crates/engine/src/work_policy_store.rs`. **Modify:** `crates/engine/src/lib.rs` adds module declaration. Reuse existing engine rusqlite/sha2/serde/thiserror dependencies and slice A `work_authorization` types. No raw credential values or provider network calls.

- [ ] Add the complete test module below first, then the preceding implementation. The policy snapshot must return grants AND policy revision from the same SQLite row read; a separate revision query is forbidden because it can pair old grants with new authority.
```rust
use crate::work_authorization::{Grant, Operation, Principal, Resource};
use zeron_proto::{WorkProfileBinding, WorkProfileRevision};
use rusqlite::{Connection, OptionalExtension, TransactionBehavior, params};
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use std::path::{Component, Path};
use std::sync::{Mutex, MutexGuard, PoisonError};
use thiserror::Error;

const VERSION: i64 = 1;
#[derive(Debug, Error)]
pub enum PolicyStoreError {
    #[error(transparent)]
    Sqlite(#[from] rusqlite::Error),
    #[error("poisoned policy store mutex")]
    Poisoned,
    #[error("policy revision conflict: expected {expected}, actual {actual:?}")]
    Cas { expected: u64, actual: Option<u64> },
    #[error("operation replay payload conflict")]
    ReplayConflict,
    #[error("unknown future policy schema version {0}")]
    FutureSchema(i64),
    #[error("invalid persisted policy: {0}")]
    Corrupt(String),
    #[error("revision out of range")]
    Revision,
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct PolicySnapshot {
    pub binding: WorkProfileBinding,
    pub policy_revision: WorkProfileRevision,
    pub grants: Vec<Grant>,
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct PolicyReplacement {
    pub principal: Principal,
    pub actor_id: String,
    pub operation_id: String,
    pub expected_revision: Option<WorkProfileRevision>,
    pub new_revision: WorkProfileRevision,
    pub binding: WorkProfileBinding,
    pub grants: Vec<Grant>,
}
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(tag = "kind", rename_all = "camelCase", deny_unknown_fields)]
enum OperationRow {
    ReadSession,
    MutateSession,
    RunSession,
    SteerSession,
    ReadRepository,
    MutateRepository,
    OpenTerminal,
    WriteTerminal,
    ObserveTerminal,
    CloseTerminal,
    ReadUpload,
    SelectAgentAccount,
    ManageAgentLogin,
}
impl From<&Operation> for OperationRow {
    fn from(x: &Operation) -> Self {
        match x {
            Operation::ReadSession => Self::ReadSession,
            Operation::MutateSession => Self::MutateSession,
            Operation::RunSession => Self::RunSession,
            Operation::SteerSession => Self::SteerSession,
            Operation::ReadRepository => Self::ReadRepository,
            Operation::MutateRepository => Self::MutateRepository,
            Operation::OpenTerminal => Self::OpenTerminal,
            Operation::WriteTerminal => Self::WriteTerminal,
            Operation::ObserveTerminal => Self::ObserveTerminal,
            Operation::CloseTerminal => Self::CloseTerminal,
            Operation::ReadUpload => Self::ReadUpload,
            Operation::SelectAgentAccount => Self::SelectAgentAccount,
            Operation::ManageAgentLogin => Self::ManageAgentLogin,
        }
    }
}
impl TryFrom<OperationRow> for Operation {
    type Error = PolicyStoreError;
    fn try_from(x: OperationRow) -> Result<Self, Self::Error> {
        Ok(match x {
            OperationRow::ReadSession => Self::ReadSession,
            OperationRow::MutateSession => Self::MutateSession,
            OperationRow::RunSession => Self::RunSession,
            OperationRow::SteerSession => Self::SteerSession,
            OperationRow::ReadRepository => Self::ReadRepository,
            OperationRow::MutateRepository => Self::MutateRepository,
            OperationRow::OpenTerminal => Self::OpenTerminal,
            OperationRow::WriteTerminal => Self::WriteTerminal,
            OperationRow::ObserveTerminal => Self::ObserveTerminal,
            OperationRow::CloseTerminal => Self::CloseTerminal,
            OperationRow::ReadUpload => Self::ReadUpload,
            OperationRow::SelectAgentAccount => Self::SelectAgentAccount,
            OperationRow::ManageAgentLogin => Self::ManageAgentLogin,
        })
    }
}
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(tag = "kind", rename_all = "camelCase", deny_unknown_fields)]
enum ResourceRow {
    Session {
        id: String,
        binding: WorkProfileBinding,
    },
    Repository {
        canonical_root: String,
        repository_id: String,
    },
    Terminal {
        id: String,
        creator: WorkProfileBinding,
        generation: u64,
    },
    Upload {
        id: String,
        binding: WorkProfileBinding,
        canonical_root: String,
    },
    AgentAccount {
        harness: String,
        slot_ref: String,
        principal_org: String,
        principal_user: String,
    },
}
impl From<&Resource> for ResourceRow {
    fn from(r: &Resource) -> Self {
        match r {
            Resource::Session { id, binding } => Self::Session {
                id: id.clone(),
                binding: binding.clone(),
            },
            Resource::Repository {
                canonical_root,
                repository_id,
            } => Self::Repository {
                canonical_root: canonical_root.clone(),
                repository_id: repository_id.clone(),
            },
            Resource::Terminal {
                id,
                creator,
                generation,
            } => Self::Terminal {
                id: id.clone(),
                creator: creator.clone(),
                generation: *generation,
            },
            Resource::Upload {
                id,
                binding,
                canonical_root,
            } => Self::Upload {
                id: id.clone(),
                binding: binding.clone(),
                canonical_root: canonical_root.clone(),
            },
            Resource::AgentAccount {
                harness,
                slot_ref,
                principal,
            } => Self::AgentAccount {
                harness: harness.clone(),
                slot_ref: slot_ref.clone(),
                principal_org: principal.org_id.clone(),
                principal_user: principal.user_id.clone(),
            },
        }
    }
}
impl TryFrom<ResourceRow> for Resource {
    type Error = PolicyStoreError;
    fn try_from(r: ResourceRow) -> Result<Self, Self::Error> {
        let resource = match r {
            ResourceRow::Session { id, binding } => Self::Session { id, binding },
            ResourceRow::Repository {
                canonical_root,
                repository_id,
            } => Self::Repository {
                canonical_root,
                repository_id,
            },
            ResourceRow::Terminal {
                id,
                creator,
                generation,
            } => Self::Terminal {
                id,
                creator,
                generation,
            },
            ResourceRow::Upload {
                id,
                binding,
                canonical_root,
            } => Self::Upload {
                id,
                binding,
                canonical_root,
            },
            ResourceRow::AgentAccount {
                harness,
                slot_ref,
                principal_org,
                principal_user,
            } => Self::AgentAccount {
                harness,
                slot_ref,
                principal: Principal {
                    org_id: principal_org,
                    user_id: principal_user,
                },
            },
        };
        validate_resource(&resource)?;
        Ok(resource)
    }
}
#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
struct PersistedGrant {
    operation: OperationRow,
    resource: ResourceRow,
}
impl TryFrom<&Grant> for PersistedGrant {
    type Error = PolicyStoreError;
    fn try_from(g: &Grant) -> Result<Self, Self::Error> {
        Ok(Self {
            operation: OperationRow::from(&g.operation),
            resource: ResourceRow::from(&g.resource),
        })
    }
}
impl TryFrom<PersistedGrant> for Grant {
    type Error = PolicyStoreError;
    fn try_from(g: PersistedGrant) -> Result<Self, Self::Error> {
        Ok(Self {
            operation: g.operation.try_into()?,
            resource: g.resource.try_into()?,
        })
    }
}
#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
struct GrantDocument {
    version: u32,
    grants: Vec<PersistedGrant>,
}
const SCHEMA: &str = r#"
CREATE TABLE policies(principal_org TEXT NOT NULL, principal_user TEXT NOT NULL, profile_id TEXT NOT NULL, profile_revision INTEGER NOT NULL CHECK(profile_revision BETWEEN 1 AND 9007199254740991), policy_revision INTEGER NOT NULL CHECK(policy_revision BETWEEN 1 AND 9007199254740991), grants_json TEXT NOT NULL, PRIMARY KEY(principal_org,principal_user,profile_id)) STRICT;
CREATE TABLE policy_mutations(principal_org TEXT NOT NULL,principal_user TEXT NOT NULL,actor_id TEXT NOT NULL,operation_id TEXT NOT NULL,request_hash BLOB NOT NULL CHECK(length(request_hash)=32),result_revision INTEGER NOT NULL CHECK(result_revision BETWEEN 1 AND 9007199254740991),PRIMARY KEY(principal_org,principal_user,actor_id,operation_id)) STRICT;
"#;
pub struct DurablePolicyStore {
    conn: Mutex<Connection>,
}

/// Private owner for the active evaluator and durable source of truth. The
/// coordinator gate is held across persistence, snapshot reload, publication,
/// admission, and the synchronous effect closure. This only serializes one
/// process; it does not stop already-started asynchronous work.
pub struct PolicyCoordinator {
    gate: Mutex<CoordinatorState>,
}
struct CoordinatorState {
    store: DurablePolicyStore,
    authorizer: crate::work_authorization::WorkAuthorizer,
    unavailable: bool,
    #[cfg(test)]
    fail_next_publication: bool,
}
impl PolicyCoordinator {
    pub fn open(path: impl AsRef<Path>) -> Result<Self, PolicyStoreError> {
        let store = DurablePolicyStore::open(path)?;
        Ok(Self {
            gate: Mutex::new(CoordinatorState {
                store,
                authorizer: crate::work_authorization::WorkAuthorizer::new(),
                unavailable: false,
                #[cfg(test)]
                fail_next_publication: false,
            }),
        })
    }
    fn state(&self) -> Result<MutexGuard<'_, CoordinatorState>, PolicyStoreError> {
        self.gate
            .lock()
            .map_err(|_: PoisonError<_>| PolicyStoreError::Poisoned)
    }
    fn publish_latest(
        state: &mut CoordinatorState,
        principal: &Principal,
        binding: &WorkProfileBinding,
    ) -> Result<(), PolicyStoreError> {
        let snapshot = state.store.load(principal, binding)?;
        let Some(snapshot) = snapshot else {
            state.unavailable = true;
            return Err(PolicyStoreError::Corrupt(
                "committed policy snapshot disappeared".into(),
            ));
        };
        #[cfg(test)]
        if std::mem::take(&mut state.fail_next_publication) {
            state.unavailable = true;
            return Err(PolicyStoreError::Corrupt(
                "injected evaluator publication failure".into(),
            ));
        }
        if state
            .authorizer
            .replace_policy(
                principal.clone(),
                binding,
                snapshot.policy_revision.get(),
                snapshot.grants,
            )
            .is_err()
        {
            state.unavailable = true;
            return Err(PolicyStoreError::Corrupt(
                "policy publication failed after durable commit".into(),
            ));
        }
        state.unavailable = false;
        Ok(())
    }
    pub fn replace(
        &self,
        replacement: &PolicyReplacement,
    ) -> Result<WorkProfileRevision, PolicyStoreError> {
        let mut state = self.state()?;
        if state.unavailable {
            return Err(PolicyStoreError::Corrupt(
                "coordinator requires recovery".into(),
            ));
        }
        // Replay also reloads the latest row. Never publish the historical
        // receipt's revision/grants over a later committed policy.
        let result = state.store.replace(replacement)?;
        if let Err(error) =
            Self::publish_latest(&mut state, &replacement.principal, &replacement.binding)
        {
            state.unavailable = true;
            return Err(error);
        }
        Ok(result)
    }
    pub fn recover(
        &self,
        principal: &Principal,
        binding: &WorkProfileBinding,
    ) -> Result<(), PolicyStoreError> {
        let mut state = self.state()?;
        state.unavailable = true;
        Self::publish_latest(&mut state, principal, binding)
    }
    #[cfg(test)]
    fn fail_next_publication(&self) {
        self.gate.lock().unwrap().fail_next_publication = true;
    }
    pub fn with_admitted_effect<T>(
        &self,
        request: &crate::work_authorization::Request,
        effect: impl FnOnce() -> T,
    ) -> Result<T, crate::work_authorization::Denial> {
        let state = self
            .gate
            .lock()
            .map_err(|_| crate::work_authorization::Denial::PolicyUnavailable)?;
        if state.unavailable {
            return Err(crate::work_authorization::Denial::PolicyUnavailable);
        }
        let permit = state.authorizer.authorize(request)?;
        let binding = match &request.selection {
            zeron_proto::WorkProfileSelection::Named(binding) => binding,
            zeron_proto::WorkProfileSelection::UnboundLegacy => {
                return Err(crate::work_authorization::Denial::UnboundLegacy);
            }
        };
        let resource = request
            .resource
            .as_ref()
            .ok_or(crate::work_authorization::Denial::ResourceUnresolved)?;
        state.authorizer.with_authorized_effect(
            permit,
            binding,
            &request.operation,
            resource,
            effect,
        )
    }
}
impl DurablePolicyStore {
    pub fn open(path: impl AsRef<Path>) -> Result<Self, PolicyStoreError> {
        let mut c = Connection::open(path)?;
        let v: i64 = c.pragma_query_value(None, "user_version", |r| r.get(0))?;
        if v > VERSION {
            return Err(PolicyStoreError::FutureSchema(v));
        }
        if v == 0 {
            let tx = c.transaction_with_behavior(TransactionBehavior::Immediate)?;
            let locked: i64 = tx.pragma_query_value(None, "user_version", |r| r.get(0))?;
            if locked > VERSION {
                return Err(PolicyStoreError::FutureSchema(locked));
            }
            if locked == 0 {
                tx.execute_batch(SCHEMA)?;
                tx.pragma_update(None, "user_version", VERSION)?
            }
            tx.commit()?
        }
        c.pragma_update(None, "journal_mode", "WAL")?;
        c.pragma_update(None, "synchronous", "NORMAL")?;
        c.busy_timeout(std::time::Duration::from_secs(5))?;
        Ok(Self {
            conn: Mutex::new(c),
        })
    }
    fn conn(&self) -> Result<MutexGuard<'_, Connection>, PolicyStoreError> {
        self.conn
            .lock()
            .map_err(|_: PoisonError<_>| PolicyStoreError::Poisoned)
    }
    pub fn load(
        &self,
        p: &Principal,
        b: &WorkProfileBinding,
    ) -> Result<Option<PolicySnapshot>, PolicyStoreError> {
        validate_principal(p)?;
        let c = self.conn()?;
        let row: Option<(i64, i64, String)> = c.query_row(
            "SELECT profile_revision,policy_revision,grants_json FROM policies WHERE principal_org=?1 AND principal_user=?2 AND profile_id=?3",
            params![p.org_id, p.user_id, b.profile_id.as_str()],
            |r| Ok((r.get(0)?, r.get(1)?, r.get(2)?)),
        ).optional()?;
        row.map(|(profile_revision, policy_revision, json)| {
            if profile_revision as u64 != b.revision.get() {
                return Err(PolicyStoreError::Corrupt(
                    "profile binding revision mismatch".into(),
                ));
            }
            let policy_revision = WorkProfileRevision::try_from(policy_revision as u64)
                .map_err(|_| PolicyStoreError::Corrupt("policy revision".into()))?;
            let doc: GrantDocument = serde_json::from_str(&json)
                .map_err(|e| PolicyStoreError::Corrupt(e.to_string()))?;
            if doc.version != 1 {
                return Err(PolicyStoreError::Corrupt("grant document version".into()));
            }
            let grants = doc
                .grants
                .into_iter()
                .map(Grant::try_from)
                .collect::<Result<Vec<_>, _>>()?;
            validate_grants(p, b, &grants)?;
            Ok(PolicySnapshot {
                binding: b.clone(),
                policy_revision,
                grants,
            })
        })
        .transpose()
    }
    pub fn replace(&self, x: &PolicyReplacement) -> Result<WorkProfileRevision, PolicyStoreError> {
        validate_principal(&x.principal)?;
        if !valid_token(&x.actor_id, 256) || !valid_token(&x.operation_id, 128) {
            return Err(PolicyStoreError::Corrupt(
                "invalid mutation identity".into(),
            ));
        }
        if x.new_revision.get() > zeron_proto::MAX_WORK_PROFILE_REVISION {
            return Err(PolicyStoreError::Revision);
        }
        validate_grants(&x.principal, &x.binding, &x.grants)?;
        let doc = GrantDocument {
            version: 1,
            grants: x
                .grants
                .iter()
                .map(PersistedGrant::try_from)
                .collect::<Result<_, _>>()?,
        };
        let json =
            serde_json::to_string(&doc).map_err(|e| PolicyStoreError::Corrupt(e.to_string()))?;
        let mut c = self.conn()?;
        let tx = c.transaction_with_behavior(TransactionBehavior::Immediate)?;
        let request = serde_json::to_vec(&(
            x.binding.clone(),
            x.expected_revision,
            x.new_revision,
            json.clone(),
        ))
        .map_err(|e| PolicyStoreError::Corrupt(e.to_string()))?;
        let digest: [u8; 32] = Sha256::digest(&request).into();
        let prior:Option<(Vec<u8>,i64)>=tx.query_row("SELECT request_hash,result_revision FROM policy_mutations WHERE principal_org=?1 AND principal_user=?2 AND actor_id=?3 AND operation_id=?4",params![x.principal.org_id,x.principal.user_id,x.actor_id,x.operation_id],|r|Ok((r.get(0)?,r.get(1)?))).optional()?;
        if let Some((saved, revision)) = prior {
            if saved.as_slice() != digest {
                return Err(PolicyStoreError::ReplayConflict);
            }
            return WorkProfileRevision::try_from(revision as u64)
                .map_err(|_| PolicyStoreError::Corrupt("receipt revision".into()));
        }
        let current:Option<(i64,i64)>=tx.query_row("SELECT profile_revision,policy_revision FROM policies WHERE principal_org=?1 AND principal_user=?2 AND profile_id=?3",params![x.principal.org_id,x.principal.user_id,x.binding.profile_id.as_str()],|r|Ok((r.get(0)?,r.get(1)?))).optional()?;
        match (current, x.expected_revision) {
            (None, None) => {}
            (Some((profile_rev, policy_rev)), Some(expected))
                if profile_rev as u64 == x.binding.revision.get()
                    && policy_rev as u64 == expected.get() => {}
            (row, expected) => {
                return Err(PolicyStoreError::Cas {
                    expected: expected.map(WorkProfileRevision::get).unwrap_or(0),
                    actual: row.map(|(_, v)| v as u64),
                });
            }
        }
        if let Some(expected) = x.expected_revision {
            let next = expected
                .checked_next()
                .map_err(|_| PolicyStoreError::Revision)?;
            if next != x.new_revision {
                return Err(PolicyStoreError::Revision);
            }
        } else if x.new_revision.get() != 1 {
            return Err(PolicyStoreError::Revision);
        }
        match x.expected_revision {
            None => {
                tx.execute(
                    "INSERT INTO policies VALUES (?1,?2,?3,?4,?5,?6)",
                    params![
                        x.principal.org_id,
                        x.principal.user_id,
                        x.binding.profile_id.as_str(),
                        x.binding.revision.get() as i64,
                        x.new_revision.get() as i64,
                        json
                    ],
                )?;
            }
            Some(expected) => {
                let n=tx.execute("UPDATE policies SET profile_revision=?4,policy_revision=?5,grants_json=?6 WHERE principal_org=?1 AND principal_user=?2 AND profile_id=?3 AND profile_revision=?7 AND policy_revision=?8",params![x.principal.org_id,x.principal.user_id,x.binding.profile_id.as_str(),x.binding.revision.get() as i64,x.new_revision.get() as i64,json,x.binding.revision.get() as i64,expected.get() as i64])?;
                if n != 1 {
                    return Err(PolicyStoreError::Cas {
                        expected: expected.get(),
                        actual: None,
                    });
                }
            }
        }
        tx.execute(
            "INSERT INTO policy_mutations VALUES (?1,?2,?3,?4,?5,?6)",
            params![
                x.principal.org_id,
                x.principal.user_id,
                x.actor_id,
                x.operation_id,
                digest.as_slice(),
                x.new_revision.get() as i64
            ],
        )?;
        tx.commit()?;
        Ok(x.new_revision)
    }
    #[cfg(test)]
    fn poison_for_test(&self) {
        let _ = std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| {
            let _g = self.conn.lock().unwrap();
            std::panic::resume_unwind(Box::new("poison"))
        }));
    }
}

fn resource_binding(r: &Resource) -> Option<&WorkProfileBinding> {
    match r {
        Resource::Session { binding, .. } | Resource::Upload { binding, .. } => Some(binding),
        Resource::Terminal { creator, .. } => Some(creator),
        Resource::Repository { .. } | Resource::AgentAccount { .. } => None,
    }
}

fn valid_token(value: &str, max_bytes: usize) -> bool {
    !value.is_empty()
        && value.len() <= max_bytes
        && value.trim() == value
        && !value.chars().any(char::is_control)
}

fn valid_canonical_root(value: &str) -> bool {
    let path = Path::new(value);
    path.is_absolute()
        && path
            .components()
            .all(|component| !matches!(component, Component::ParentDir | Component::CurDir))
        && path.to_str() == Some(value)
}

fn validate_resource(resource: &Resource) -> Result<(), PolicyStoreError> {
    let invalid = match resource {
        Resource::Session { id, binding } => !valid_token(id, 256) || binding.revision.get() == 0,
        Resource::Repository {
            canonical_root,
            repository_id,
        } => !valid_canonical_root(canonical_root) || !valid_token(repository_id, 256),
        Resource::Terminal {
            id,
            creator,
            generation,
        } => !valid_token(id, 256) || creator.revision.get() == 0 || *generation == 0,
        Resource::Upload {
            id,
            binding,
            canonical_root,
        } => {
            !valid_token(id, 256)
                || binding.revision.get() == 0
                || !valid_canonical_root(canonical_root)
        }
        Resource::AgentAccount {
            harness,
            slot_ref,
            principal,
        } => {
            !valid_token(harness, 64)
                || !valid_token(slot_ref, 256)
                || !valid_token(&principal.org_id, 256)
                || !valid_token(&principal.user_id, 256)
        }
    };
    if invalid {
        return Err(PolicyStoreError::Corrupt("invalid resource fields".into()));
    }
    Ok(())
}

fn validate_grants(
    principal: &Principal,
    binding: &WorkProfileBinding,
    grants: &[Grant],
) -> Result<(), PolicyStoreError> {
    validate_principal(principal)?;
    if binding.revision.get() == 0 {
        return Err(PolicyStoreError::Corrupt("invalid profile revision".into()));
    }
    for grant in grants {
        validate_resource(&grant.resource)?;
        let compatible = matches!(
            (&grant.operation, &grant.resource),
            (
                Operation::ReadSession
                    | Operation::MutateSession
                    | Operation::RunSession
                    | Operation::SteerSession,
                Resource::Session { .. }
            ) | (
                Operation::ReadRepository | Operation::MutateRepository,
                Resource::Repository { .. }
            ) | (Operation::OpenTerminal, Resource::Terminal { .. })
                | (Operation::WriteTerminal, Resource::Terminal { .. })
                | (Operation::ObserveTerminal, Resource::Terminal { .. })
                | (Operation::CloseTerminal, Resource::Terminal { .. })
                | (Operation::ReadUpload, Resource::Upload { .. })
                | (
                    Operation::SelectAgentAccount | Operation::ManageAgentLogin,
                    Resource::AgentAccount { .. }
                )
        );
        if !compatible {
            return Err(PolicyStoreError::Corrupt(
                "operation is incompatible with resource kind".into(),
            ));
        }
        if resource_binding(&grant.resource)
            .is_some_and(|resource_binding| resource_binding != binding)
        {
            return Err(PolicyStoreError::Corrupt(
                "grant binding differs from policy key".into(),
            ));
        }
        if let Resource::AgentAccount {
            principal: resource_principal,
            ..
        } = &grant.resource
            && resource_principal != principal
        {
            return Err(PolicyStoreError::Corrupt(
                "agent account principal differs from policy owner".into(),
            ));
        }
    }
    Ok(())
}

fn validate_principal(principal: &Principal) -> Result<(), PolicyStoreError> {
    if !valid_token(&principal.org_id, 256) || !valid_token(&principal.user_id, 256) {
        return Err(PolicyStoreError::Corrupt("invalid principal".into()));
    }
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    use tempfile::tempdir;
    fn p() -> Principal {
        Principal {
            org_id: "org".into(),
            user_id: "user".into(),
        }
    }
    fn b() -> WorkProfileBinding {
        WorkProfileBinding {
            profile_id: zeron_proto::WorkProfileId::try_from(
                "e317f12a-17e1-4b0c-a56f-9502b870db9e".to_owned(),
            )
            .unwrap(),
            revision: WorkProfileRevision::try_from(1).unwrap(),
        }
    }
    fn grant() -> Grant {
        Grant {
            operation: Operation::RunSession,
            resource: Resource::Session {
                id: "session-1".into(),
                binding: b(),
            },
        }
    }
    fn replacement(expected: Option<u64>, new: u64, op: &str) -> PolicyReplacement {
        PolicyReplacement {
            principal: p(),
            actor_id: "device".into(),
            operation_id: op.into(),
            expected_revision: expected.map(|v| WorkProfileRevision::try_from(v).unwrap()),
            new_revision: WorkProfileRevision::try_from(new).unwrap(),
            binding: b(),
            grants: vec![grant()],
        }
    }
    #[test]
    fn replace_cas_reopen_revokes_prior_policy() {
        let d = tempdir().unwrap();
        let db = d.path().join("policy.db");
        let s = DurablePolicyStore::open(&db).unwrap();
        assert_eq!(s.replace(&replacement(None, 1, "create")).unwrap().get(), 1);
        assert_eq!(
            s.load(&p(), &b()).unwrap().unwrap().policy_revision.get(),
            1
        );
        drop(s);
        let s = DurablePolicyStore::open(&db).unwrap();
        assert_eq!(s.load(&p(), &b()).unwrap().unwrap().grants, vec![grant()]);
        assert_eq!(
            s.replace(&replacement(Some(1), 2, "revoke")).unwrap().get(),
            2
        );
        assert_eq!(s.load(&p(), &b()).unwrap().unwrap().grants, vec![grant()]);
        assert!(matches!(
            s.replace(&replacement(Some(1), 2, "stale")),
            Err(PolicyStoreError::Cas {
                expected: 1,
                actual: Some(2)
            })
        ));
    }
    #[test]
    fn replay_is_scoped_and_changed_payload_conflicts() {
        let d = tempdir().unwrap();
        let s = DurablePolicyStore::open(d.path().join("p.db")).unwrap();
        let x = replacement(None, 1, "op");
        assert_eq!(s.replace(&x).unwrap().get(), 1);
        assert_eq!(s.replace(&x).unwrap().get(), 1);
        let mut changed = x.clone();
        changed.grants.clear();
        assert!(matches!(
            s.replace(&changed),
            Err(PolicyStoreError::ReplayConflict)
        ));
        let mut other = replacement(Some(1), 2, "op");
        other.actor_id = "device-2".into();
        assert_eq!(s.replace(&other).unwrap().get(), 2);
    }
    #[test]
    fn unknown_schema_rejected_without_pragma_mutation() {
        let d = tempdir().unwrap();
        let db = d.path().join("future.db");
        let c = Connection::open(&db).unwrap();
        c.pragma_update(None, "user_version", 50).unwrap();
        let mode: String = c
            .pragma_query_value(None, "journal_mode", |r| r.get(0))
            .unwrap();
        drop(c);
        let bytes = std::fs::read(&db).unwrap();
        assert!(matches!(
            DurablePolicyStore::open(&db),
            Err(PolicyStoreError::FutureSchema(50))
        ));
        assert_eq!(std::fs::read(&db).unwrap(), bytes);
        let c = Connection::open(&db).unwrap();
        assert_eq!(
            c.pragma_query_value::<String, _>(None, "journal_mode", |r| r.get(0))
                .unwrap(),
            mode
        );
    }
    #[test]
    fn sql_trigger_fault_rolls_back_policy_and_receipt_then_retries() {
        let d = tempdir().unwrap();
        let db = d.path().join("fault.db");
        let s = DurablePolicyStore::open(&db).unwrap();
        s.conn().unwrap().execute_batch("CREATE TRIGGER reject_mutation BEFORE INSERT ON policy_mutations BEGIN SELECT RAISE(ABORT,'fault'); END;").unwrap();
        let x = replacement(None, 1, "op");
        assert!(matches!(s.replace(&x), Err(PolicyStoreError::Sqlite(_))));
        assert_eq!(s.load(&p(), &b()).unwrap(), None);
        drop(s);
        let s = DurablePolicyStore::open(&db).unwrap();
        assert_eq!(s.load(&p(), &b()).unwrap(), None);
        s.conn()
            .unwrap()
            .execute_batch("DROP TRIGGER reject_mutation;")
            .unwrap();
        assert_eq!(s.replace(&x).unwrap().get(), 1);
    }
    #[test]
    fn poisoned_store_lock_denies() {
        let d = tempdir().unwrap();
        let s = DurablePolicyStore::open(d.path().join("poison.db")).unwrap();
        s.poison_for_test();
        assert!(matches!(
            s.load(&p(), &b()),
            Err(PolicyStoreError::Poisoned)
        ));
    }
    #[test]
    fn unknown_persisted_operation_rejects_entire_policy() {
        let d = tempdir().unwrap();
        let db = d.path().join("corrupt.db");
        let s = DurablePolicyStore::open(&db).unwrap();
        s.replace(&replacement(None, 1, "create")).unwrap();
        s.conn().unwrap().execute("UPDATE policies SET grants_json=?1",[r#"{"version":1,"grants":[{"operation":{"kind":"GrantAll"},"resource":{"kind":"session","id":"session-1","binding":{"profileId":"e317f12a-17e1-4b0c-a56f-9502b870db9e","revision":1}}}]}"#]).unwrap();
        assert!(matches!(
            s.load(&p(), &b()),
            Err(PolicyStoreError::Corrupt(_))
        ));
    }

    #[test]
    fn concurrent_two_connection_cas_has_one_winner() {
        use std::sync::{Arc, Barrier};
        let d = tempdir().unwrap();
        let db = d.path().join("concurrent.db");
        let setup = DurablePolicyStore::open(&db).unwrap();
        setup.replace(&replacement(None, 1, "init")).unwrap();
        drop(setup);
        let first = Arc::new(DurablePolicyStore::open(&db).unwrap());
        let second = Arc::new(DurablePolicyStore::open(&db).unwrap());
        let barrier = Arc::new(Barrier::new(3));
        let spawn =
            |store: Arc<DurablePolicyStore>, operation_id: &'static str, barrier: Arc<Barrier>| {
                std::thread::Builder::new()
                    .spawn(move || {
                        let change = replacement(Some(1), 2, operation_id);
                        barrier.wait();
                        store.replace(&change)
                    })
                    .unwrap()
            };
        let one = spawn(first, "op-one", barrier.clone());
        let two = spawn(second, "op-two", barrier.clone());
        barrier.wait();
        let results = [one.join().unwrap(), two.join().unwrap()];
        assert_eq!(results.iter().filter(|result| result.is_ok()).count(), 1);
        assert_eq!(
            results
                .iter()
                .filter(|result| matches!(result, Err(PolicyStoreError::Cas { .. })))
                .count(),
            1
        );
        let reopened = DurablePolicyStore::open(&db).unwrap();
        assert_eq!(
            reopened
                .load(&p(), &b())
                .unwrap()
                .unwrap()
                .policy_revision
                .get(),
            2
        );
    }

    #[test]
    fn rejects_corrupt_tokens_bindings_and_paths_on_load() {
        let d = tempdir().unwrap();
        let db = d.path().join("bad-values.db");
        let store = DurablePolicyStore::open(&db).unwrap();
        store.replace(&replacement(None, 1, "create")).unwrap();
        let bad_binding = r#"{"version":1,"grants":[{"operation":{"kind":"runSession"},"resource":{"kind":"session","id":"s1","binding":{"profileId":"e317f12a-17e1-4b0c-a56f-9502b870db9e","revision":2}}}]}"#;
        store
            .conn()
            .unwrap()
            .execute("UPDATE policies SET grants_json=?1", [bad_binding])
            .unwrap();
        assert!(matches!(
            store.load(&p(), &b()),
            Err(PolicyStoreError::Corrupt(_))
        ));
        let bad_path = r#"{"version":1,"grants":[{"operation":{"kind":"readRepository"},"resource":{"kind":"repository","canonicalRoot":"/repo/../secret","repositoryId":"repo-1"}}]}"#;
        store
            .conn()
            .unwrap()
            .execute("UPDATE policies SET grants_json=?1", [bad_path])
            .unwrap();
        assert!(matches!(
            store.load(&p(), &b()),
            Err(PolicyStoreError::Corrupt(_))
        ));
        let bad_agent = r#"{"version":1,"grants":[{"operation":{"kind":"selectAgentAccount"},"resource":{"kind":"agentAccount","harness":"codex","slotRef":"slot1","principalOrg":"other","principalUser":"user"}}]}"#;
        store
            .conn()
            .unwrap()
            .execute("UPDATE policies SET grants_json=?1", [bad_agent])
            .unwrap();
        assert!(matches!(
            store.load(&p(), &b()),
            Err(PolicyStoreError::Corrupt(_))
        ));
    }

    #[test]
    fn durable_load_authorize_effect_then_revoke_and_reload_denies_old_permit() {
        use crate::work_authorization::{Denial, Request, WorkAuthorizer};
        use std::sync::atomic::{AtomicBool, Ordering};

        let d = tempdir().unwrap();
        let db = d.path().join("auth-flow.db");
        let principal = p();
        let binding = b();
        let operation = Operation::RunSession;
        let resource = grant().resource;
        let store = DurablePolicyStore::open(&db).unwrap();
        store.replace(&replacement(None, 1, "create")).unwrap();

        let snapshot = store.load(&principal, &binding).unwrap().unwrap();
        assert_eq!(snapshot.policy_revision.get(), 1);
        let authorizer = WorkAuthorizer::new();
        authorizer
            .replace_policy(
                principal.clone(),
                &binding,
                snapshot.policy_revision.get(),
                snapshot.grants,
            )
            .unwrap();
        let request = Request {
            selection: zeron_proto::WorkProfileSelection::Named(binding.clone()),
            principal: principal.clone(),
            expected_policy_revision: 1,
            operation: operation.clone(),
            resource: Some(resource.clone()),
            migration_required: false,
            unresolved: false,
        };
        let permit = authorizer.authorize(&request).unwrap();
        let permit_to_revoke = authorizer.authorize(&request).unwrap();
        let ran = AtomicBool::new(false);
        authorizer
            .with_authorized_effect(permit, &binding, &operation, &resource, || {
                ran.store(true, Ordering::SeqCst);
            })
            .unwrap();
        assert!(ran.load(Ordering::SeqCst));

        let mut revoked_change = replacement(Some(1), 2, "revoke");
        revoked_change.grants.clear();
        store.replace(&revoked_change).unwrap();
        let revoked = store.load(&principal, &binding).unwrap().unwrap();
        assert_eq!(revoked.policy_revision.get(), 2);
        authorizer
            .replace_policy(
                principal.clone(),
                &binding,
                revoked.policy_revision.get(),
                revoked.grants,
            )
            .unwrap();
        let stale_request = Request {
            expected_policy_revision: 1,
            ..request
        };
        assert_eq!(
            authorizer.authorize(&stale_request).err(),
            Some(Denial::StalePolicy)
        );

        let ran_after_revoke = AtomicBool::new(false);
        let stale_permit = authorizer.authorize(&stale_request).err().expect("stale request denied");
        assert_eq!(stale_permit, Denial::StalePolicy);
        assert_eq!(
            authorizer.with_authorized_effect(
                permit_to_revoke,
                &binding,
                &operation,
                &resource,
                || ran_after_revoke.store(true, Ordering::SeqCst),
            ),
            Err(Denial::StalePolicy)
        );
        assert!(!ran_after_revoke.load(Ordering::SeqCst));
    }

    #[test]
    fn rejects_operation_resource_kind_mismatch_on_write_and_load() {
        let d = tempdir().unwrap();
        let db = d.path().join("kind-mismatch.db");
        let store = DurablePolicyStore::open(&db).unwrap();
        let mut invalid = replacement(None, 1, "bad-kind");
        invalid.grants[0].operation = Operation::ReadRepository;
        assert!(matches!(
            store.replace(&invalid),
            Err(PolicyStoreError::Corrupt(_))
        ));
        store.replace(&replacement(None, 1, "valid")).unwrap();
        let invalid_persisted = r#"{"version":1,"grants":[{"operation":{"kind":"runSession"},"resource":{"kind":"agentAccount","harness":"codex","slotRef":"slot1","principalOrg":"org","principalUser":"user"}}]}"#;
        store
            .conn()
            .unwrap()
            .execute("UPDATE policies SET grants_json=?1", [invalid_persisted])
            .unwrap();
        assert!(matches!(
            store.load(&p(), &b()),
            Err(PolicyStoreError::Corrupt(_))
        ));
    }

    #[test]
    fn coordinator_serializes_admission_with_durable_revoke() {
        use crate::work_authorization::{Denial, Request};
        use std::sync::atomic::{AtomicBool, Ordering};
        use std::sync::{Arc, Barrier};

        let d = tempdir().unwrap();
        let coordinator =
            Arc::new(PolicyCoordinator::open(d.path().join("coordinator.db")).unwrap());
        let mut create = replacement(None, 1, "create");
        coordinator.replace(&create).unwrap();
        let request = Request {
            selection: zeron_proto::WorkProfileSelection::Named(b()),
            principal: p(),
            expected_policy_revision: 1,
            operation: Operation::RunSession,
            resource: Some(grant().resource),
            migration_required: false,
            unresolved: false,
        };
        let barrier = Arc::new(Barrier::new(3));
        let admission_barrier = barrier.clone();
        let admission_coordinator = coordinator.clone();
        let admission_request = request.clone();
        let effect_count = Arc::new(AtomicBool::new(false));
        let effect_count_worker = effect_count.clone();
        let admission = std::thread::Builder::new()
            .spawn(move || {
                admission_barrier.wait();
                admission_coordinator.with_admitted_effect(&admission_request, || {
                    effect_count_worker.store(true, Ordering::SeqCst);
                })
            })
            .unwrap();

        let revoke_coordinator = coordinator.clone();
        let revoke_barrier = barrier.clone();
        let revoker = std::thread::Builder::new()
            .spawn(move || {
                revoke_barrier.wait();
                create.grants.clear();
                create.expected_revision = Some(WorkProfileRevision::try_from(1).unwrap());
                create.new_revision = WorkProfileRevision::try_from(2).unwrap();
                create.operation_id = "revoke".into();
                revoke_coordinator.replace(&create)
            })
            .unwrap();
        barrier.wait();
        let admitted = admission.join().unwrap();
        let revoked = revoker.join().unwrap();
        assert!(revoked.is_ok());
        assert!(
            admitted.is_ok()
                || matches!(admitted, Err(Denial::ResourceDenied | Denial::StalePolicy))
        );
        if admitted.is_err() {
            assert!(!effect_count.load(Ordering::SeqCst));
        }
        let effects_before_final_check = effect_count.load(Ordering::SeqCst);
        let after = coordinator.with_admitted_effect(&request, || {
            effect_count.store(true, Ordering::SeqCst);
        });
        assert!(matches!(
            after,
            Err(Denial::ResourceDenied | Denial::StalePolicy)
        ));
        assert_eq!(
            effect_count.load(Ordering::SeqCst),
            effects_before_final_check
        );
    }

    #[test]
    fn replay_of_old_receipt_publishes_latest_durable_snapshot() {
        use crate::work_authorization::{Denial, Request};
        use std::sync::atomic::{AtomicBool, Ordering};
        let d = tempdir().unwrap();
        let coordinator = PolicyCoordinator::open(d.path().join("replay.db")).unwrap();
        let create = replacement(None, 1, "create");
        coordinator.replace(&create).unwrap();
        let mut revoke = replacement(Some(1), 2, "revoke");
        revoke.grants.clear();
        coordinator.replace(&revoke).unwrap();
        assert_eq!(coordinator.replace(&create).unwrap().get(), 1); // exact replay receipt
        let request = Request {
            selection: zeron_proto::WorkProfileSelection::Named(b()),
            principal: p(),
            expected_policy_revision: 2,
            operation: Operation::RunSession,
            resource: Some(grant().resource),
            migration_required: false,
            unresolved: false,
        };
        let ran = AtomicBool::new(false);
        assert_eq!(
            coordinator.with_admitted_effect(&request, || ran.store(true, Ordering::SeqCst)),
            Err(Denial::ResourceDenied)
        );
        assert!(!ran.load(Ordering::SeqCst));
    }

    #[test]
    fn durable_commit_publish_failure_fails_closed_then_recovers_latest_row() {
        use crate::work_authorization::{Denial, Request};
        use std::sync::atomic::{AtomicBool, Ordering};
        let d = tempdir().unwrap();
        let coordinator = PolicyCoordinator::open(d.path().join("publish-failure.db")).unwrap();
        let create = replacement(None, 1, "create");
        coordinator.replace(&create).unwrap();
        let request = Request {
            selection: zeron_proto::WorkProfileSelection::Named(b()),
            principal: p(),
            expected_policy_revision: 1,
            operation: Operation::RunSession,
            resource: Some(grant().resource),
            migration_required: false,
            unresolved: false,
        };
        let first_effect = AtomicBool::new(false);
        coordinator
            .with_admitted_effect(&request, || first_effect.store(true, Ordering::SeqCst))
            .unwrap();
        assert!(first_effect.load(Ordering::SeqCst));

        let mut revoke = replacement(Some(1), 2, "revoke");
        revoke.grants.clear();
        coordinator.fail_next_publication();
        assert!(matches!(
            coordinator.replace(&revoke),
            Err(PolicyStoreError::Corrupt(_))
        ));
        let ran = AtomicBool::new(false);
        assert_eq!(
            coordinator.with_admitted_effect(&request, || ran.store(true, Ordering::SeqCst)),
            Err(Denial::PolicyUnavailable),
        );
        // Durable revocation committed despite publication failure. The old
        // allow stays unavailable until recovery reloads the latest row.
        coordinator.recover(&p(), &b()).unwrap();
        assert!(matches!(
            coordinator.with_admitted_effect(&request, || ran.store(true, Ordering::SeqCst)),
            Err(Denial::ResourceDenied | Denial::StalePolicy)
        ));
        assert!(!ran.load(Ordering::SeqCst));
    }
}

```
- [ ] Run `cargo test --locked -p zeron-engine --lib work_policy_store::tests`, require13 tests. Run `work_authorization::tests` separately, require10. Current combined inventory is4 wire +7 catalog +10 evaluator +13 durable-policy/coordinator =34 tests. These counts must be confirmed by actual filtered listings, not inferred from a previous run.
- [ ] Run `cargo clippy --workspace --all-targets --all-features -- -D warnings` after actual consumer integration. Do not suppress unused private module warnings to ship an unconsumed store. The core module visibility/API must match its reviewed consumer boundary, never expose a mutation RPC that accepts caller-supplied principal as authority.
- [ ] Wire store snapshot loading to evaluator initialization: call `load` with owner-derived principal/binding, reject None/corrupt/error, then `replace_policy(principal, binding, snapshot.policy_revision.get(), snapshot.grants)`. A policy mutation is not acknowledged until durable commit AND active evaluator update have reached a safe serialized state. If evaluator publication fails after commit, hold new effects and reload; never continue serving old grants under a successful mutation response.
- [ ] This slice's integration test proves durable load→authorize→synchronous effect→revoke→reload→old-permit denial. It does not prove multi-process cache invalidation or async effect stopping. Only one owner process may mutate a live profile policy; the later runtime activation must enforce that instance lock and dispatch-generation protocol before exposure.
- [ ] In scratch, remove the operation/resource-kind check and require corruption test failure; restore. Remove CAS predicate and require stale/concurrent tests fail. Preserve late-trigger rollback and future-schema no-mutation assertions. Commit scoped module/tests only after actual core CI.

## Required scenarios
- C01: Missing or unavailable policy, unbound legacy and foreign binding deny without invoking effect closure.
- C02: Permit bound to another evaluator, operation or resource cannot be consumed.
- C03: Revocation before synchronous admission rejects stale permit and executes zero effects.
- C04: Concurrent synchronous admission and policy replacement have a defined serialized order; poison denies.

## CI phase after every implementation iteration
Run exact core tests and integrated round CI with commit-bound evidence.

## Rollback
Roll back enforcement code only with execution disabled for newly bound profiles. Never turn unknown policy into allow to preserve compatibility.

## Combined literal handoff validation20:47UTC
Extracted wire/catalog/evaluator/durable-store blocks into matching proto+engine crate/module topology. Initial integration caught wrong crate-root type path, Debug-dependent unwrap_err and collapsible-if lint; corrected canonical blocks. Final30 tests (4 wire,7 catalog,9 evaluator,10 durable policy) and workspace/all-target clippy-Dwarnings pass in scratch. This is cross-contract source compatibility evidence, not real EngineCore routing/provider enforcement. No host services or runtime code changed.

## C. Atomic durable-to-live publication consumer
The complete B source now includes PolicyCoordinator. Engine runtime must own only this coordinator, not separate public store/evaluator handles. All policy replacement/recovery and synchronous effect admission pass its private mutex. Durable commit is followed by latest-row reload and publication before unlock/acknowledgment. Replay returns original receipt but republishes latest durable policy, never old grants. Publication failure closes admission until explicit latest-state recovery succeeds. Coordinator tests cover concurrent revoke/admission, old receipt replay, and a committed revoke whose publication fails while old grants existed. Equal-revision evaluator publication is idempotent only for identical grants. This is one-owner-process synchronization; external database writers or async effect continuation remain unsupported without the later runtime generation/instance-lock protocol. Do not claim this closes full EngineCore resource enforcement.

## Publication consumer validation21:05UTC
Literal canonical evaluator+store/coordinator blocks extracted into proto/engine topology pass30 engine tests plus4 wire tests and clippy all-targets with warnings denied. Includes old receipt replay against latest revoke, serialized admission/revocation, publication failure after durable mutation and fail-closed recovery. Earlier30-total count is superseded by34 total. Still no actual async EngineCore/provider enforcement claim.

## Exact owner-facing library exports (required for bounded core CI)
Keep implementation modules private. Add exactly these declarations/reexports to `crates/engine/src/lib.rs`, once each:
```rust
mod work_authorization;
mod work_policy_store;
pub use work_authorization::{Denial, Grant, Operation, Principal, Request, Resource};
pub use work_policy_store::{PolicyCoordinator, PolicyReplacement, PolicyStoreError};
```
Do not publicly reexport WorkAuthorizer, AuthorizationPermit, DurablePolicyStore or their raw handles. They stay behind PolicyCoordinator. `unavailable` is a test-only evaluator constructor, not unused production API. Public Rust input types are NOT remote capabilities: do not add Serde decoding or expose them directly as authorized RPC parameters. The owning engine must construct principal/binding/resolved resources under the runtime enforcement contract. Library callers can express a request but cannot fabricate a permit or bypass the coordinator's current grant/revision checks.

These exact exports with private modules, existing canonical implementations and test-only unavailable constructor passed34 tests plus all-target clippy-Dwarnings in the extracted proto/engine topology21:29UTC. No duplicate facade enums, wrappers or blanket lint suppression are required. This closes bounded core compilation/visibility, not remote identity resolution or async effect containment.
