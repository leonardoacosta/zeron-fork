# Explicit non-destructive work-profile migration

## Existing anchors
- `crates/engine/src/profile.rs`
- `crates/engine/src/lib.rs`
- `crates/proto/src/workspace.rs`
- `crates/sync/src/store.rs`
- `crates/engine/tests/local_profiles.rs`

## Contract
Migrate only explicitly selected legacy source to a new named-profile target with verified identity, non-destructive staged copy, content manifest and atomic publication. Preserve original data; no credentials copied. Interrupted or ambiguous migration remains non-executable. Imported runs require safe resume authorization, never automatic journal replay.

See `../work-profile-boundary/design.md` for shared identity and runtime distinction. This unit has separate promotion; full ZF02 acceptance needs runtime plus access enforcement.

## Misinterpretations
- Existing LocalImporter account import is not named-profile migration.
- A completed copy does not authorize recovered runs.
- No live credential copy or auto-selection by profile label.

## C04 acceptance: copied journals never auto-resume
A successfully published target containing copied run journals is not proof of continuing authority. Acceptance must seed a pending source journal, migrate/publish the target, restart it, and observe the run remains held with zero harness invocations or journal replay; preserve its original account/environment binding. Only a separate current safe-resume authorization may allow continuation. This assertion is distinct from atomic target publication and crash reconciliation.
Keep source immutable; retain staging and incomplete marker for diagnosis. Never delete original or overwrite target. Revert capability without erasing migration receipts.
