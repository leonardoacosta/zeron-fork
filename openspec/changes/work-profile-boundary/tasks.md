# Named work profiles and explicit bindings execution contract

**Goal:** Introduce extensible work-profile identity/configuration separate from Local/Synced/Development transport scope.
**Architecture:** Existing Rust engine/proto/RPC/profile storage and native clients are the starting point. Freeze interfaces from observed source; no speculative provider API or generic framework.
**Tech stack:** Rust/Tokio/Serde/SQLite; GPUI/Swift/Worker TypeScript only if the approved surface requires them.
**Status:** executable discovery/refinement steps; product implementation NOT READY.
**Dependencies:** `ci-promotion-gates`. Read-only research can proceed without using unimplemented prerequisite APIs; implementation waits for all prerequisite CI promotion records.

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

## B-D. Remaining whole-unit readiness gate
The exact catalog SQL/API, engine boot binding, daemon profile match and explicit legacy migration are not yet code-complete. The coordinator must finish those within this canonical tasks.md before full-unit delegation. Do not infer them from types or promote the whole change after A. Design.md names required contracts and hazards; downstream runtime implementation cannot consume a falsely completed work-profile-boundary.

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
