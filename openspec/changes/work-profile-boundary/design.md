# Named work profiles: proposed shared contract

Status: proposed technical contract, not implemented or approved for execution. Complete unit acceptance still requires storage, boot/RPC and migration steps below; a DTO alone does not enforce isolation.

## Existing anchors and observed hazards
- `crates/engine/src/profile.rs`: EngineProfile currently combines transport/account scope with store roots. Named work identity does not exist. Repositories/worktrees/accounts remain device-scoped.
- `crates/engine/src/lib.rs`: Engine::resolve_profile chooses transport/account roots; EngineCore::assemble_with_profile_locked opens store and calls recover_stale before clients interact. Legacy migration-required must prevent recovery/dispatch, not just display a UI warning.
- `crates/proto/src/workspace.rs`: EngineInfo capability negotiation exists, but no work-profile identity. Old clients must not attach to a requested profile merely because IPC responds.
- `crates/sync/src/store.rs`: DocsStore per-root SQLite, assignment revisions/replay. No global connection should bypass active work-profile binding.
- `crates/engine/tests/local_profiles.rs`: transport/account store isolation tests, not named work-profile authorization.
- Additional consumers: `crates/ui/src/state.rs` EngineHandle::bootstrap attaches to daemon before resolving config; `crates/engine/src/agent_accounts.rs` and `repos.rs` own device-wide resources; `crates/engine/src/local_import.rs` and profile legacy-upload grants can widen reads if carried across bindings unchecked.

## Frozen names for dependent plans
All names below are proposed new symbols, not existing API claims. Define them once in new `crates/proto/src/work_profile.rs`, exported through `crates/proto/src/lib.rs`.

1. `WorkProfileId`: opaque canonical lower-case UUID string. Owner generates it. Display name/slug/account is not identity. Validate deserialization, not just constructors. UUID strings are never arbitrary filesystem paths.
2. `WorkProfileRevision`: positive u64 serialized as a JSON integer; reject0 and values above the exact interoperable integer ceiling9,007,199,254,740,991. Increment checked against same ceiling before persistence; no wrap or saturating update.
3. `WorkProfileBinding { profile_id: WorkProfileId, revision: WorkProfileRevision }`: immutable run/session/assignment authority input. Rename updates catalog revision, does not silently rebind an active run. Permission changes cause boundary revalidation in profile-access-enforcement; a past binding is not perpetual authorization.
4. `WorkProfileRecord { binding: WorkProfileBinding, display_name: WorkProfileName }`: catalog metadata. WorkProfileName rejects leading/trailing whitespace and controls, is nonempty, bounded256 UTF-8 bytes. Personal/Priceless/Brown are ordinary explicit records; no hardcoded enum or automatic Brown access. No repository/credential grants in this record.
5. `WorkProfileSelection`: `UnboundLegacy` or `Named(WorkProfileBinding)`. Unbound legacy may be inspected only through a separately reviewed read-only migration surface; it is never execution authority. Do not reinterpret None as Personal or silently attach to a different daemon.

Account/transport principal is separate: keep existing org/user/scope metadata. Named profile storage identity cannot be shared across differing account principals by selecting the same ID. Store locator must bind both principal and work profile. Same-profile cross-device synchronization requires server-validated work-profile namespace before enabling it. Appending profile ID to a room name is NOT authorization; unverified scoped relay support fails closed. Development/private relay tests do not waive that boundary.

## Proposed sequencing within this unit

A. Define and test wire types with complete source in tasks.md. No runtime behavior change or capability advertisement yet.
B. Define owner catalog persistence and compare-and-swap revision semantics; frozen input below. Build real transaction tests before routes.
C. Bind boot/runtime/resources and exact daemon attach checks; do not advertise complete capability before these pass.
D. Explicit legacy classification/read-only migration gate and old-client behavior; only then native cross-profile acceptance.

Do not promote this whole unit after A. If split into child changes, A must expose only a non-executable type contract and downstream runtime work waits for B-D. Keep this tasks.md as canonical checklist until a reviewed split updates every dependency.

## Catalog storage contract to implement in B

Catalog is owner-local, located under device data root but contains no secrets. Use SQLite transaction support already present, not unlocked JSON rewrites. Catalog rows identify immutable profile ID, current revision and display name. Updating requires matching expected revision. Distinct work-profile stores remain independent; catalog is not assignment history. Required mutation identity is scoped to actor/principal plus operation/profile and binds exact payload; retry returns original result without revision duplication. A rejected mutation writes nothing. Atomic catalog update+replay receipt is mandatory.

Exact SQL/API patch must be completed before B implementation. This clause is an explicit remaining plan gap, not an instruction for a lesser executor to guess table names or error wire format. Existing assignment replay mechanics are reuse evidence, not permission to copy unchecked SQL.

## C. Boot, EngineInfo, and daemon binding contract

**Observed call chain:** `EngineHandle::bootstrap` in `crates/ui/src/state.rs:279-432` invokes `attach_to_daemon(config.ipc_port)` at the start, before it constructs `EngineConfig` or resolves a profile. `attach_to_daemon` at `state.rs:437-499` calls `query_engine_info` (`state.rs:542-566`) and currently accepts any valid `EngineInfo`. `query_engine_info` synthesizes Synced scope when an old server lacks `EngineInfo`. On embed, bootstrap creates `EngineConfig`, takes `InstanceLock`, then builds auth, captures scope, calls `Engine::resolve_profile`, constructs early `EngineInfo`, serves `DeferredEngineRpc`, and assembles after onboarding. `Engine::resolve_profile` is `crates/engine/src/lib.rs:655-698`; `Engine::engine_info` is `701-712`; `EngineCore::assemble_with_profile_locked` is `209-344`, where `SessionsEngine::recover_stale` runs before assembly returns. `DeferredEngineRpc::handle` at `state.rs:177-218` serves `EngineInfo` before profile assembly and waits other calls.

**Required binding behavior:** add a requested `WorkProfileSelection` to `EngineBootConfig` (`state.rs:93-108`) and carry the resolved `WorkProfileBinding` plus authenticated principal through `EngineConfig`, `Engine`, `EngineCore`, `EngineInfo`, and `EngineRpc`. Resolve it only after acquiring the existing data-dir `InstanceLock`, but before opening any work-profile store, journal, importer, preview, upload root, or session recovery. The engine owns the resolved binding. RPC parameters cannot select or override it. `EngineInfo` reports the binding (or explicit unbound/migration state) and a capability only after the engine has installed all required profile/resource enforcement. Do not put display name or account secrets in the identity response.

`attach_to_daemon` must receive the caller's expected selection/principal context, then validate returned identity before producing a Remote `EngineHandle`. For `Named(binding)`, missing binding/capability, missing identity (`query_engine_info` legacy fallback), principal mismatch, profile-ID mismatch, or revision incompatible with the request is a typed attach refusal; it must not return a handle and must not query chats/devices/transcripts or retry with an implicit default. Preserve the existing “port contains non-engine/wedged listener, embed instead” handling, but distinguish that from a real engine that refuses a requested profile. Do not let that refusal fall through to embedding another profile under the same port/data directory. A legacy client request may attach to a legacy daemon only when both sides explicitly select the same `UnboundLegacy` read-only inspection mode; that mode never reaches executable data RPCs.

Until `profile-access-enforcement` has installed and tested resource grants for repos, worktrees, agent credentials, and uploads, C must hold named-profile execution before `EngineCore::assemble_with_profile_locked`, not merely hide UI buttons. In particular, do not call `SessionsEngine::recover_stale`, `DocHost::set_sessions`, importer construction, or any dispatch path for an unbound/unauthorized store. Existing device-wide roots are not grants. Keep existing sync disabled for named profiles until the remote registry/session namespace is server-authenticated and profile-specific. Hot switch remains unsupported: a different selection requires shutdown/rebootstrap and a fresh daemon identity check.

## D. Legacy inspection and migration gate

**Observed paths:** `EngineProfile::local`, `synced`, and `development` in `crates/engine/src/profile.rs:34-70` currently choose roots from scope/account. `EngineCore::assemble_with_profile_locked` (`lib.rs:209-344`) opens the profile store/journal, performs `recover_stale`, calls `claim_legacy_uploads_root`, and applies `local_import::marker_grants_read_root`. It creates `LocalImporter` for Synced profiles. `LocalImporter::status` and `run` are in `crates/engine/src/local_import.rs:258-392`; the write path imports rows/docs/journals/processed-command ledger and records an account marker. RPC methods `LOCAL_IMPORT_STATUS` and `IMPORT_LOCAL_WORKSPACE` execute these at `crates/engine/src/rpc.rs:2473-2509`. `marker_grants_read_root` at `local_import.rs:474-484` grants the old local uploads root based on org/user marker. These existing local-to-synced behaviors must not automatically bind or grant a newly named profile.

**Fail-closed opening:** classify roots before normal assembly. A known explicitly named profile may open normally. A legacy root lacking an unambiguous persisted binding enters `UnboundLegacy` inspection only: no `DocsStore`/journal is opened for normal RPC/session execution; no stale recovery, command draining, importer, preview, repo/account access, upload fallback, edge join, or sync runs. The inspection API returns identity and a typed migration-required state only. `None`, invalid/corrupt marker/catalog, partial target, multiple plausible legacy owners, or missing profile grant never resolves to a default named profile. Preserve source files byte-for-byte. Do not invoke `EngineProfile::claim_legacy_uploads_root` or `marker_grants_read_root` for a named target unless a separate explicit grant is validated against both source and target profile IDs and principal.

The existing `LocalImporter` is not the named-profile migration implementation. Keep its current transport behavior unchanged for current Local→Synced accounts, but prevent its `IMPORT_LOCAL_WORKSPACE` and `LOCAL_IMPORT_STATUS` methods from being repurposed for named-profile binding. A later migration surface must identify source and target bindings, stage to a new empty engine-generated target, copy without deleting or overwriting, verify content/digest, atomically publish a completion manifest only after all required stores/attachments/ledgers are validated, and remain non-executable after any failed or interrupted stage. Never copy credentials. Never execute recovered journals copied from an unbound source until a separately authorized resume policy exists.

**Required migration states/errors:** `UnboundLegacy` is inspection-only; `MigrationRequired { source_ref, reason }` is a boot/attach outcome, not a usable engine profile. Distinguish `LegacyAmbiguous`, `LegacyMarkerCorrupt`, `MigrationTargetExists`, `MigrationSourceChanged`, `MigrationIncomplete`, and `MigrationVerificationFailed`. The concrete wire payload and persistent migration manifest are a separate design decision and must be frozen before D implementation. This plan intentionally does not invent the source digest algorithm or whether the manifest belongs in catalog DB vs target store.

## Legacy migration contract to implement in D

No automatic copy/move/rename of an existing account store. Enumerate legacy identity/root read-only and ask for explicit binding/migration intent at the authorized surface. Preserve source bytes and retain a manifest with source identity, target identity, source digest and observed completion. Existing partial target or ambiguous credentials/uploads grants blocks. A crash mid-copy must not publish a ready target or execute recovered sessions. No overwriting target, deleting source or credential copy. This non-destructive policy does not decide future UX or allow providers to read Brown data.

## Acceptance scenarios (canonical)
- C01: Two profiles on one device cannot retrieve each other's assignment, transcript, upload or repository binding through local or remote RPC.
- C02: Rename a profile while a session runs: identity stays stable and the frozen binding does not silently change.
- C03: Open legacy data without an unambiguous work-profile binding: show migration-required state, retain original bytes and prohibit execution.
- C04: Create a fourth profile without changing an enum or granting default access.

Additional hazards: same UUID under different principal; revoked authority during preflight; stale daemon after profile selection; reused mutation ID with different payload; max revision overflow; duplicate display names; corrupt catalog; missing provider enforcement; symlinked store; old mobile decoder; already-running legacy session; lost migration acknowledgment; restart after partial import. Each needs an exact test/API once B-D are refined.

## Recommended proposal boundary

Split C-D from A-B before implementation. A (wire types) and B (catalog persistence) are independently testable and do not grant execution authority. C is a runtime/IPC security boundary spanning engine config, auth/principal capture, early EngineInfo, daemon attachment, RPC, session recovery, and resource-enforcement dependency. D is a separate data migration protocol spanning importer, uploads grants, journals, crash recovery, and old-client compatibility. Recommend two child changes: `work-profile-runtime-binding` depends on A+B and `profile-access-enforcement`; `work-profile-legacy-migration` depends on runtime binding plus an approved source/target/digest manifest contract. Keep this parent design as the shared contract, not a promise that C/D are one bounded coding task.

## Rollout / rollback
Types first without advertising support. Feature support remains unavailable until entire binding enforcement passes. New catalog metadata is additive. Back up old store before any explicitly authorized migration. Downgrade reader refuses named-profile store it cannot enforce; never coalesces back into legacy account root. Preserve originals, replay receipts and migration uncertainty.

## Genuine later decisions versus safe defaults
Per-window profile switching UI, whether users may deliberately bind multiple work profiles to one remote account workspace, and exact migration UX require reviewed design. None blocks type/catalog refinement. They do block silently implementing shared sync namespace or hot-switch behavior. The allowed actions/resource policy remains a separate downstream contract, not arbitrary strings interpreted as authorization here.
