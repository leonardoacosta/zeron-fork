# Versioned workflow definitions and selection execution contract

**Goal:** Define independently versioned workflows with stages, agent choices, checks, failure policy, gates and autonomy.
**Architecture:** Existing Rust engine/proto/RPC/profile storage and native clients are the starting point. Freeze interfaces from observed source; no speculative provider API or generic framework.
**Tech stack:** Rust/Tokio/Serde/SQLite; GPUI/Swift/Worker TypeScript only if the approved surface requires them.
**Status:** executable discovery/refinement steps; product implementation NOT READY.
**Dependencies:** `revision-evidence-bindings`, `work-profile-boundary`. Read-only research can proceed without using unimplemented prerequisite APIs; implementation waits for all prerequisite CI promotion records.

## D1. Recover authority and source (one bounded read per listed anchor)
**Files:** design.md and tasks.md in this change; read-only source anchors in design.md.
- [ ] Read PRD clauses ZF-05, ZF-06 and every C-scenario in `specs/workflow-version-selection/spec.md`; state excluded sibling behavior in design.md.
- [ ] From repository root, verify listed anchors exist:
```bash
python3 - <<'PY'
from pathlib import Path
paths = ['crates/proto/src/assignment.rs', 'crates/sync/src/store.rs', 'crates/engine/src/rpc.rs', 'crates/engine/src/profile.rs']
for name in paths:
    p = Path(name)
    assert p.is_file(), name
    print(name, len(p.read_text().splitlines()), "lines")
PY
```
Expected: one line per anchor, exit0. Missing path means re-discover with graft and correct this contract; do not create a dummy file. Read `graft/INDEX.md` then matching cards. Use `graft ask "Versioned workflow definitions and selection" --source` only if the CLI is already available; graph files are sufficient.
- [ ] In design.md, cite exact symbols/current line spans for the input, authority, persistence and side-effect paths. For each C-scenario record whether current behavior is observed, contradicted or not yet tested. Do not equate missing grep hit with absence proof.

## A. Exact selection core proposal
**Create after approval:** `crates/engine/src/workflow_selection.rs`; **modify:** `crates/engine/src/lib.rs` with private module declaration. The `WorkflowVersion` reference is proposed and must become the single shared workflow reference, not independently duplicated by triggers/dependencies. The string ID validation shown here is a minimal in-memory contract; wire validation and immutable-store lookup remain part of D2, not inferred.

- [ ] Add the test module below first and record red; then definitions. Run `cargo test --locked -p zeron-engine --lib workflow_selection::tests`, require3 selected/passing tests. No launch or DB write belongs in this helper.
```rust
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct WorkflowVersion { pub id: String, pub revision: u64 }
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum SelectionReason { AssignmentOverride, RepositoryDefault, ProfileDefault }
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Selection { pub version: WorkflowVersion, pub reason: SelectionReason }
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum SelectionError { MissingConfiguration, InvalidReference, NotAuthorized, UnknownVersion }
// resolve/authorize must read owner-side immutable workflow and current profile policy.
// This pure function performs no launch or store write. No fallback after an explicit error.
pub fn select(
    assignment: Option<&WorkflowVersion>, repository: Option<&WorkflowVersion>, profile: Option<&WorkflowVersion>,
    known: impl Fn(&WorkflowVersion)->bool, authorized: impl Fn(&WorkflowVersion)->bool,
) -> Result<Selection,SelectionError> {
    let (version,reason)=if let Some(v)=assignment {(v,SelectionReason::AssignmentOverride)}
        else if let Some(v)=repository {(v,SelectionReason::RepositoryDefault)}
        else if let Some(v)=profile {(v,SelectionReason::ProfileDefault)}
        else {return Err(SelectionError::MissingConfiguration)};
    if version.id.is_empty() || version.id.len()>128 || version.id.trim()!=version.id || version.revision==0 || version.revision>9_007_199_254_740_991 {
        return Err(SelectionError::InvalidReference);
    }
    if !authorized(version) { return Err(SelectionError::NotAuthorized); }
    if !known(version) { return Err(SelectionError::UnknownVersion); }
    Ok(Selection{version:version.clone(),reason})
}
#[cfg(test)] mod tests {
    use super::*;
    fn v(id:&str,n:u64)->WorkflowVersion {WorkflowVersion{id:id.into(),revision:n}}
    #[test] fn precedence_and_reason() {
        let(a,r,p)=(v("a",1),v("r",2),v("p",3));
        for (override_,repo,expected,reason) in [(Some(&a),Some(&r),&a,SelectionReason::AssignmentOverride),(None,Some(&r),&r,SelectionReason::RepositoryDefault),(None,None,&p,SelectionReason::ProfileDefault)] {
            let s=select(override_,repo,Some(&p), |_|true, |_|true).unwrap();assert_eq!(&s.version,expected);assert_eq!(s.reason,reason);
        }
    }
    #[test] fn explicit_failure_never_falls_back() {
        let(a,p)=(v("bad",1),v("good",1));
        assert_eq!(select(Some(&a),None,Some(&p), |_|true, |x|x.id=="good"),Err(SelectionError::NotAuthorized));
        assert_eq!(select(Some(&a),None,Some(&p), |x|x.id=="good", |_|true),Err(SelectionError::UnknownVersion));
        assert_eq!(select(Some(&v("",1)),None,Some(&p), |_|true, |_|true),Err(SelectionError::InvalidReference));
        assert_eq!(select(None,None,None, |_|true, |_|true),Err(SelectionError::MissingConfiguration));
    }
    #[test] fn selected_version_is_frozen() {
        let mut default=v("main",1);let chosen=select(None,None,Some(&default), |_|true, |_|true).unwrap();default.revision=2;
        assert_eq!(chosen.version.revision,1);assert_eq!(default.revision,2);
    }
}
```
- [ ] Negative control in scratch: swap repository and profile precedence, then require `precedence_and_reason` to fail. Remove authorization check and require `explicit_failure_never_falls_back` to fail. Restore before scoped commit.
- [ ] Review callback ownership: `known` and `authorized` come from owner-side immutable catalog and current profile policy, never client booleans. Evaluate selection, policy and persisted binding atomically or revalidate before launch. This pure test does not prove race safety.
- [ ] Pin the selected version/reason in assignment launch state before acknowledgment. Later default changes do not mutate that copy. Explicit changes create a new validated binding and invalidate dependent evidence; do not update old evidence in place.

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
- C01: Repository and profile defaults differ: repository wins and reason is visible.
- C02: Assignment override selects inaccessible workflow: reject rather than bypass profile policy.
- C03: Workflow updated while assignment runs: old version remains bound unless explicitly changed and revalidated.
- C04: An investigation-only workflow ends with findings and no candidate/delivery stage.

## CI phase after every implementation iteration
- [ ] Run exact refined feature tests and core/affected-platform CI from `../prd-execution-map/design.md`. Verify at least one test actually selected; preserve failing evidence. No next iteration/round promotion while required checks fail or are missing.
- [ ] Run real acceptance: Precedence, version pinning, invalid override and restart tests through owner RPC; UI explanation delivered by presentation changes.
- [ ] Update this tasks.md with exact tested commit/tree, commands, counts, exit codes, evidence class, native environment and remaining blocks. Commit scoped files only, then CI on that integrated commit before downstream promotion.

## Rollback
Immutable versions and additive references; old readers fail explicitly on unsupported workflow versions. Roll back default pointers without rewriting active runs.
