# Exact-version output dependencies execution contract

**Goal:** Bind dependency edges to accepted stage-output versions, not just whole assignment completion.
**Architecture:** Existing Rust engine/proto/RPC/profile storage and native clients are the starting point. Freeze interfaces from observed source; no speculative provider API or generic framework.
**Tech stack:** Rust/Tokio/Serde/SQLite; GPUI/Swift/Worker TypeScript only if the approved surface requires them.
**Status:** executable discovery/refinement steps; product implementation NOT READY.
**Dependencies:** `verification-acceptance-gates`, `conflict-admission-observer`. Only exact prerequisite promotion admits implementation.

## D1. Recover authority and source (one bounded read per listed anchor)
**Files:** design.md and tasks.md in this change; read-only source anchors in design.md.
- [ ] Read PRD clauses ZF-11, ZF-14 and every C-scenario in `specs/accepted-output-dependencies/spec.md`; state excluded sibling behavior in design.md.
- [ ] From repository root, verify listed anchors exist:
```bash
python3 - <<'PY'
from pathlib import Path
paths = ['crates/proto/src/assignment.rs', 'crates/sync/src/store.rs', 'crates/engine/src/rpc.rs']
for name in paths:
    p = Path(name)
    assert p.is_file(), name
    print(name, len(p.read_text().splitlines()), "lines")
PY
```
Expected: one line per anchor, exit0. Missing path means re-discover with graft and correct this contract; do not create a dummy file. Read `graft/INDEX.md` then matching cards. Use `graft ask "Exact-version output dependencies" --source` only if the CLI is already available; graph files are sufficient.
- [ ] In design.md, cite exact symbols/current line spans for the input, authority, persistence and side-effect paths. For each C-scenario record whether current behavior is observed, contradicted or not yet tested. Do not equate missing grep hit with absence proof.

## A. Proposed graph invariant core
**Proposed file:** `crates/engine/src/output_dependencies.rs`, private engine module. Exact pure algorithm below is a testable invariant model, not the persisted or authorized graph. Owner must validate same-profile identity and accepted evidence before constructing graph inputs. The accepted map contains only current valid accepted outputs; revoked outputs absent. Do not use mutable latest pointers to silently alter pinned edges.

- [ ] Add tests first, then definitions below; `cargo test --locked -p zeron-engine --lib output_dependencies::tests` must select2 tests and pass. Negative control: remove cycle detection and require cycle test failure in scratch.
```rust
use std::collections::{BTreeMap,BTreeSet};
#[derive(Debug,Clone,PartialEq,Eq)]pub struct OutputRef{pub assignment:String,pub output:String,pub revision:u64}
#[derive(Debug,Clone,PartialEq,Eq)]pub struct Edge{pub downstream:String,pub required:OutputRef}
#[derive(Debug,Clone,PartialEq,Eq)]pub enum Error{InvalidReference,Cycle,DuplicateEdge,Unaccepted,ChangedOutput}
#[derive(Debug,Default)]pub struct Dependencies{edges:Vec<Edge>}
impl Dependencies{
 pub fn add(&mut self,edge:Edge)->Result<(),Error>{
  if edge.downstream.is_empty()||edge.required.assignment.is_empty()||edge.required.output.is_empty()||edge.required.revision==0{return Err(Error::InvalidReference)}
  if self.edges.contains(&edge){return Err(Error::DuplicateEdge)}
  // Edges point downstream -> upstream. Adding d -> u cycles if u already reaches d.
  let mut pending=vec![edge.required.assignment.as_str()];let mut seen=BTreeSet::new();
  while let Some(node)=pending.pop(){if node==edge.downstream{return Err(Error::Cycle)}if seen.insert(node){pending.extend(self.edges.iter().filter(|e|e.downstream==node).map(|e|e.required.assignment.as_str()));}}
  self.edges.push(edge);Ok(())
 }
 pub fn ready(&self,downstream:&str,accepted:&BTreeMap<(String,String),u64>)->Result<(),Error>{
  for edge in self.edges.iter().filter(|e|e.downstream==downstream){
   match accepted.get(&(edge.required.assignment.clone(),edge.required.output.clone())){
    None=>return Err(Error::Unaccepted),Some(version)if *version!=edge.required.revision=>return Err(Error::ChangedOutput),_=>{}
   }
  }Ok(())
 }
 pub fn len(&self)->usize{self.edges.len()}
}
#[cfg(test)]mod tests{
 use super::*;
 fn e(d:&str,u:&str,r:u64)->Edge{Edge{downstream:d.into(),required:OutputRef{assignment:u.into(),output:"findings".into(),revision:r}}}
 #[test]fn cycles_and_duplicate_insert_are_atomic(){let mut g=Dependencies::default();g.add(e("b","a",1)).unwrap();g.add(e("c","b",1)).unwrap();assert_eq!(g.add(e("a","c",1)),Err(Error::Cycle));assert_eq!(g.add(e("a","a",1)),Err(Error::Cycle));assert_eq!(g.add(e("b","a",1)),Err(Error::DuplicateEdge));assert_eq!(g.len(),2);}
 #[test]fn accepted_stage_not_whole_assignment_and_no_latest_substitution(){let mut g=Dependencies::default();g.add(e("b","a",1)).unwrap();let mut accepted=BTreeMap::new();assert_eq!(g.ready("b",&accepted),Err(Error::Unaccepted));accepted.insert(("a".into(),"findings".into()),1);assert_eq!(g.ready("b",&accepted),Ok(()));accepted.insert(("a".into(),"findings".into()),2);assert_eq!(g.ready("b",&accepted),Err(Error::ChangedOutput));assert_eq!(g.ready("unrelated",&accepted),Ok(()));}
}
```
- [ ] Before runtime use, replace plain IDs with shared validated identifiers, bind edges to profile/principal and persist edge insertion plus revision atomically. Concurrent cycle admission must serialize the whole relevant graph transaction; separate in-memory checks are insufficient.
- [ ] Restrict one required version per downstream/upstream-output pair or return a typed contradictory-dependency error. The pure model detects exact duplicates only; incompatible version edges must not reach persisted graph. Full SQL/RPC and invalidation tasks below remain required before promotion.

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
- C01: Investigation output accepted while parent assignment not done: authorized dependent stage may start.
- C02: Upstream new revision cannot silently substitute into already-bound downstream run.
- C03: Cycle or self-edge rejected atomically, no partial graph change.
- C04: Accepted evidence later contradicted: affected downstream waits/reconciles, independent branch continues.

## CI phase after every implementation iteration
- [ ] Run exact refined feature tests and core/affected-platform CI from `../prd-execution-map/design.md`. Verify at least one test actually selected; preserve failing evidence. No next iteration/round promotion while required checks fail or are missing.
- [ ] Run real acceptance: Graph transaction/restart tests and real two-stage workflow proving exact-version binding and invalidation.
- [ ] Update this tasks.md with exact tested commit/tree, commands, counts, exit codes, evidence class, native environment and remaining blocks. Commit scoped files only, then CI on that integrated commit before downstream promotion.

## Rollback
Keep immutable edge/output revisions and append invalidations. Downgrade blocks unknown graph semantics, not deleting edges.
