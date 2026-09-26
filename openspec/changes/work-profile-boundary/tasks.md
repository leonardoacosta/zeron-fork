# Named work profiles and explicit bindings execution contract

**Goal:** Introduce extensible work-profile identity/configuration separate from Local/Synced/Development transport scope.
**Architecture:** Existing Rust engine/proto/RPC/profile storage and native clients are the starting point. Freeze interfaces from observed source; no speculative provider API or generic framework.
**Tech stack:** Rust/Tokio/Serde/SQLite; GPUI/Swift/Worker TypeScript only if the approved surface requires them.
**Status:** executable discovery/refinement steps; product implementation NOT READY.
**Dependencies:** `work-profile-catalog`, `profile-access-enforcement`. Only exact prerequisite promotion admits implementation.

## D1. Recover authority and source (one bounded read per listed anchor)
**Files:** design.md and tasks.md in this change; read-only source anchors in design.md.
- [ ] Read PRD clauses ZF-02 and every C-scenario in `specs/work-profile-boundary/spec.md`; state excluded sibling behavior in design.md.
- [ ] From repository root, verify listed anchors exist:
```bash
python3 - <<'PY'
from pathlib import Path
paths = ['crates/engine/src/profile.rs', 'crates/engine/src/lib.rs', 'crates/proto/src/workspace.rs', 'crates/sync/src/store.rs', 'crates/engine/tests/local_profiles.rs']
for name in paths:
    p = Path(name)
    assert p.is_file(), name
    print(name, len(p.read_text().splitlines()), "lines")
PY
```
Expected: one line per anchor, exit0. Missing path means re-discover with graft and correct this contract; do not create a dummy file. Read `graft/INDEX.md` then matching cards. Use `graft ask "Named work profiles and explicit bindings" --source` only if the CLI is already available; graph files are sufficient.
- [ ] In design.md, cite exact symbols/current line spans for the input, authority, persistence and side-effect paths. For each C-scenario record whether current behavior is observed, contradicted or not yet tested. Do not equate missing grep hit with absence proof.

## Foundation dependency
Exact wire/catalog implementation moved to `../work-profile-catalog/tasks.md`. Do not duplicate that checklist or mark this runtime unit complete from foundation tests.

## C. Runtime binding, early EngineInfo and daemon attach refusal
**Depends on:** A wire contract, B catalog persistence, and `profile-access-enforcement` after it is split to depend only on the A+B contract child. C does not implement named-profile execution or advertise its capability without that resource-enforcement prerequisite.

**Owned callsites:** `crates/proto/src/workspace.rs` (`EngineInfo`, capability constants); `crates/rpc/src/lib.rs` (only add a method/error code if a real RPC is required); `crates/engine/src/lib.rs` (`EngineConfig`, `Engine::resolve_profile`, `Engine::engine_info`, `EngineCore`, `assemble_runtime_inner`, `assemble_with_profile_locked`); `crates/ui/src/state.rs` (`EngineBootConfig`, `EngineHandle::bootstrap`, `attach_to_daemon`, `query_engine_info`, `DeferredEngineRpc`); `crates/engine/src/rpc.rs` (RPC uses engine-owned context). Existing test homes: `crates/proto/src/workspace.rs` inline tests and `crates/ui/src/state.rs` bootstrap/daemon tests. Add `crates/engine/tests/work_profile_boot.rs` only if a public Engine API can exercise resolution without making internal fields public.

- [ ] Define the exact JSON representation and absence rule for `EngineInfo.workProfileBinding` and its capability in `crates/proto/src/workspace.rs`. `EngineInfo` currently derives serde camelCase and old fields default; named attach must distinguish absent binding from explicit legacy state. `EngineInfo` identity is observable before assembly through `DeferredEngineRpc`, so name the value `requested_selection` until the engine has resolved it and do not advertise ready/capable before enforcement. Add assertions to `engine_info_uses_camel_case_fields` and `old_engine_info_defaults_to_no_capabilities` for new and legacy wire shapes. No capability until the engine can enforce the full binding.
- [ ] Add `work_profile_selection` to `EngineBootConfig` and the corresponding resolved-only field to `EngineConfig`; do not add a UI-provided principal. Derive principal from captured `Auth` after `initial_workspace_scope`, using the existing `AuthState` org/user identity, then call catalog lookup under the held `InstanceLock`. Keep `Engine::resolve_profile` transport/account selection as a distinct stage; never route `UnboundLegacy` through its Local/Development/Synced defaults. Enumerate all `EngineConfig` literals with `graft callers EngineConfig` before implementing.
- [ ] In `EngineHandle::bootstrap`, build the requested identity expectation before the initial daemon probe. Change `attach_to_daemon(ipc_port)` to accept only expected selection/principal data needed for comparison. A valid response with missing identity or mismatched profile/principal is a hard typed refusal, not `None` (which currently means embed). Preserve `None => embed` for no listener or non-engine listener. In the lock-retry path at `state.rs:318-331`, repeat attach and retain the same expected identity; never fall through to assemble a legacy/default profile after a real daemon mismatch. Ensure no workspace/data RPC is sent until identity match succeeds.
- [ ] Change `query_engine_info` (`state.rs:542-566`) so its legacy `LOCAL_DEVICE` fallback remains usable only for requests explicitly selecting `UnboundLegacy` inspection; it cannot synthesize acceptance for `Named`. Add a typed attach error carrying expected/observed identity without leaking chats, account tokens, or store paths. Do not trust caller-provided display name as identity.
- [ ] In `Engine::resolve_profile` / `assemble_runtime_inner`, resolve and validate the selected `WorkProfileBinding` and derive a canonical engine-owned root from principal+UUID. Reject same UUID under another principal, unknown ID, stale binding policy, and symlink/noncanonical root before `DocsStore::open`. Do not treat catalog membership as repository/agent-account permission. Until profile-access-enforcement passes, return a held/unsupported state before opening normal named store or creating a `SessionsEngine` that can recover/dispatch. Move/gate `recover_stale` in `assemble_with_profile_locked` so an unbound/unauthorized selection cannot call it; do not change existing non-named behavior.
- [ ] Carry the binding in `EngineCore` and `EngineRpc` as immutable engine-owned state. Session/assignment create stores that binding; reads and retries compare persisted binding and never rewrite/re-home old rows. Do not take profile ID/revision from RPC params as a store selector. Keep existing sync path disabled for named binding until server-validated namespace support exists; never fall back to account-only registry rooms.
- [ ] Add these exact UI/bootstrap tests in `crates/ui/src/state.rs` tests, using existing `LegacyIdentityRpc`, `DeferredIdentityRpc`, `free_port`, and public `EngineHandle::bootstrap`: (1) explicit named request + matching EngineInfo attaches Remote; (2) legacy daemon fallback with Named request is refused before any data method; (3) same port server with mismatched profile/principal returns mismatch and does not embed/open a default store; (4) no listener still embeds only when requested selection is resolvable; (5) lock-retry daemon match uses identical requested binding; (6) old daemon without binding works only for explicit `UnboundLegacy` inspect and never becomes Ready for data RPC.
- [ ] Add exact engine assembly tests in `crates/engine/tests/local_profiles.rs` or new `work_profile_boot.rs`: same UUID under different principal resolves to different roots and cannot load each other's row; unknown/stale binding opens no target DB; failed resource prerequisite does not invoke stale recovery, pending-command drain, or importer; named sync requested without server namespace returns unsupported rather than offline/account-only success. Use public `Engine::resolve_profile`/assembly/RPC surfaces; do not mock internal storage results.
- [ ] Keep `C01/C02` acceptance blocked until profile-access-enforcement covers repository binding, uploads, credentials and remote RPC. A passing catalog/EngineInfo test alone must not enable `WORK_PROFILE_BINDING_V1` or any “profile ready” capability.

## Migration boundary
Explicit data copy/import is delegated to `../work-profile-legacy-migration/tasks.md`. This runtime unit only classifies legacy state and holds execution; no migration implementation here.

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
- C01: Two profiles on one device cannot retrieve each other's assignment, transcript, upload or repository binding through local or remote RPC.
- C02: Rename a profile while a session runs: identity stays stable and the frozen binding does not silently change.
- C03: Open legacy data without an unambiguous work-profile binding: show migration-required state, retain original bytes and prohibit execution.
- C04: Create a fourth profile without changing an enum or granting default access.

## CI phase after every implementation iteration
- [ ] Run exact refined feature tests and core/affected-platform CI from `../prd-execution-map/design.md`. Verify at least one test actually selected; preserve failing evidence. No next iteration/round promotion while required checks fail or are missing.
- [ ] Run real acceptance: Real two-profile owner/client reads and restart, plus legacy-store fixture migration and denied cross-profile access.
- [ ] Update this tasks.md with exact tested commit/tree, commands, counts, exit codes, evidence class, native environment and remaining blocks. Commit scoped files only, then CI on that integrated commit before downstream promotion.

## Rollback
Additive migration with a backup and old-store compatibility check. Downgrade must refuse unsupported bindings rather than merge profiles. Retain legacy source data.
