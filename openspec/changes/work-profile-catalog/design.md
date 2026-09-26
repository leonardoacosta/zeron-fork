# Validated profile identity and owner catalog

## Existing anchors
- `crates/engine/src/profile.rs`
- `crates/engine/src/lib.rs`
- `crates/proto/src/workspace.rs`
- `crates/sync/src/store.rs`
- `crates/engine/tests/local_profiles.rs`

## Contract
Define validated opaque profile identity, display metadata and revision types plus owner-local principal-scoped catalog persistence. Create/rename use atomic per-profile CAS and actor/principal-scoped exact replay receipts. This foundation provides no runtime authority, no daemon attachment, no sync namespace, and no legacy execution permission.

See `../work-profile-boundary/design.md` for shared identity and runtime distinction. This unit has separate promotion; full ZF02 acceptance needs runtime plus access enforcement.

## Misinterpretations
- Do not mark named-profile isolation complete from catalog tests.
- Never duplicate shared wire types downstream.
- Principal and actor are owner context, not untrusted request labels.

## Rollback
Additive unused catalog only; do not advertise runtime capability. Future schema refused before mutation; retain legacy stores unchanged.
