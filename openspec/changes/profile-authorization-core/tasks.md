# Owner policy core execution contract

**Dependencies:** `work-profile-catalog`

## A. Exact synchronous authorization core proposal
**Create:** `crates/engine/src/work_authorization.rs`. **Modify:** `crates/engine/src/lib.rs` adds private `mod work_authorization;`. Reuse proposed proto profile types; no provider calls or credential values in this module.

- [ ] Add tests first then complete definitions below. `cargo test --locked -p zeron-engine --lib work_authorization::tests` must select9 tests and pass. The test closure counts admission only, not provider effects.
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
    pub fn unavailable() -> Self {
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
        if state
            .policies
            .get(&key)
            .is_some_and(|p| revision <= p.revision)
        {
            return Err(Denial::StalePolicy);
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
        if let Resource::AgentAccount { principal, .. } = resource {
            if principal != &request.principal {
                return Err(Denial::ProfileMismatch);
            }
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
}
```
- [ ] Behavioral negative control in scratch: remove policy revision comparison in `with_authorized_effect`; revoked-permit test must fail with closure wrongly invoked. Restore. Lock poison must return PolicyUnavailable, not panic or recover unsafe policy.
- [ ] Keep policy replacement and effect admission serialized. The closure must be short/synchronous and non-reentrant; never await while holding the lock. Async work needs generation-scoped cancellation/recheck at each effect boundary, not a promise that one admission check authorizes all future work.
- [ ] This is an in-memory proposed evaluator only. Before full runtime use, define durable policy/CAS, validated principal/resource constructors, actual canonical path resolution, credential containment, safe RPC error mapping and every integration site in design.md. Public fields are internal construction conveniences, never deserialize Request/Grant from an untrusted RPC as authority. No named-profile execution capability before those gates pass.


## Durable policy slice still required
Exact policy schema/CAS/load/restart source and tests must be authored before whole-unit promotion. This is a concrete open planning item, not permission for an executor to invent a grant store.

## Required scenarios
- C01: Missing or unavailable policy, unbound legacy and foreign binding deny without invoking effect closure.
- C02: Permit bound to another evaluator, operation or resource cannot be consumed.
- C03: Revocation before synchronous admission rejects stale permit and executes zero effects.
- C04: Concurrent synchronous admission and policy replacement have a defined serialized order; poison denies.

## CI phase after every implementation iteration
Run exact core tests and integrated round CI with commit-bound evidence.

## Rollback
Roll back enforcement code only with execution disabled for newly bound profiles. Never turn unknown policy into allow to preserve compatibility.
