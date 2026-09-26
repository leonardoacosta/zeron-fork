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

## Boot and attachment contract to implement in C

- Engine selection pins one profile for an engine runtime. Hot switching a running runtime is unsupported in the initial slice. This is a bounded implementation ceiling, not a final product decision about multi-window UX.
- Add additive EngineInfo work-profile binding/capability. Requesting a named profile and encountering an old daemon without identity is unsupported, never attach by port alone. Mismatch returns a typed profile-mismatch with no foreign metadata reads.
- Every local/remote RPC resolves against the engine-owned selected binding. Client labels cannot select a store or authorize access. Direct sessions and assignments inherit explicit binding when created; retries never re-home prior records.
- Device identity/harness installation may be shared metadata, not shared resource grants. Repo/account access requires profile-access-enforcement before any named-profile launch. Unsupported resource enforcement is held, not globally allowed for compatibility.
- Boot cannot call stale-session recovery for unbound/unauthorized profile state. Named store roots must be canonical, engine-generated, no symlink escape or caller-supplied relative path.
- Keep existing transport code unchanged until scoped sync contract verified; no silent offline fallback if synced named-profile operation was requested.

## Legacy migration contract to implement in D

No automatic copy/move/rename of an existing account store. Enumerate legacy identity/root read-only and ask for explicit binding/migration intent at the authorized surface. Preserve source bytes and retain a manifest with source identity, target identity, source digest and observed completion. Existing partial target or ambiguous credentials/uploads grants blocks. A crash mid-copy must not publish a ready target or execute recovered sessions. No overwriting target, deleting source or credential copy. This non-destructive policy does not decide future UX or allow providers to read Brown data.

## Acceptance scenarios (canonical)
- C01: Two profiles on one device cannot retrieve each other's assignment, transcript, upload or repository binding through local or remote RPC.
- C02: Rename a profile while a session runs: identity stays stable and the frozen binding does not silently change.
- C03: Open legacy data without an unambiguous work-profile binding: show migration-required state, retain original bytes and prohibit execution.
- C04: Create a fourth profile without changing an enum or granting default access.

Additional hazards: same UUID under different principal; revoked authority during preflight; stale daemon after profile selection; reused mutation ID with different payload; max revision overflow; duplicate display names; corrupt catalog; missing provider enforcement; symlinked store; old mobile decoder; already-running legacy session; lost migration acknowledgment; restart after partial import. Each needs an exact test/API once B-D are refined.

## Rollout / rollback
Types first without advertising support. Feature support remains unavailable until entire binding enforcement passes. New catalog metadata is additive. Back up old store before any explicitly authorized migration. Downgrade reader refuses named-profile store it cannot enforce; never coalesces back into legacy account root. Preserve originals, replay receipts and migration uncertainty.

## Genuine later decisions versus safe defaults
Per-window profile switching UI, whether users may deliberately bind multiple work profiles to one remote account workspace, and exact migration UX require reviewed design. None blocks type/catalog refinement. They do block silently implementing shared sync namespace or hot-switch behavior. The allowed actions/resource policy remains a separate downstream contract, not arbitrary strings interpreted as authorization here.
