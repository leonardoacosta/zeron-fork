# Priority, blockers and non-preemptive urgent work execution contract

**Goal:** Queue conflicted proposals with blocker type/reason and explicit priority.
**Architecture:** Existing Rust engine/proto/RPC/profile storage and native clients are the starting point. Freeze interfaces from observed source; no speculative provider API or generic framework.
**Tech stack:** Rust/Tokio/Serde/SQLite; GPUI/Swift/Worker TypeScript only if the approved surface requires them.
**Status:** executable discovery/refinement steps; product implementation NOT READY.
**Dependencies:** `conflict-admission-observer`, `confirmed-stop-handoff`. Only exact prerequisite promotion admits implementation.

## D1. Recover authority and source (one bounded read per listed anchor)
**Files:** design.md and tasks.md in this change; read-only source anchors in design.md.
- [ ] Read PRD clauses ZF-10, ZF-09 and every C-scenario in `specs/priority-backlog/spec.md`; state excluded sibling behavior in design.md.
- [ ] From repository root, verify listed anchors exist:
```bash
python3 - <<'PY'
from pathlib import Path
paths = ['crates/engine/src/rpc.rs', 'crates/engine/src/sessions.rs', 'crates/sync/src/store.rs', 'crates/proto/src/assignment.rs']
for name in paths:
    p = Path(name)
    assert p.is_file(), name
    print(name, len(p.read_text().splitlines()), "lines")
PY
```
Expected: one line per anchor, exit0. Missing path means re-discover with graft and correct this contract; do not create a dummy file. Read `graft/INDEX.md` then matching cards. Use `graft ask "Priority, blockers and non-preemptive urgent work" --source` only if the CLI is already available; graph files are sufficient.
- [ ] In design.md, cite exact symbols/current line spans for the input, authority, persistence and side-effect paths. For each C-scenario record whether current behavior is observed, contradicted or not yet tested. Do not equate missing grep hit with absence proof.

## A. Exact eligible-order core proposal
**Proposed create:** `crates/engine/src/assignment_queue.rs`; private module in `crates/engine/src/lib.rs`. The algorithm returns candidates, not launch permits. Numeric priority is an explicit stored input, not an approved UI scale/default. Admission sequence comes from one durable owner transaction, not wall-clock timestamps.

- [ ] Add tests then definitions below; `cargo test --locked -p zeron-engine --lib assignment_queue::tests` must select4 tests and pass. Negative control: include blocked items or sort priority ascending in scratch and require corresponding tests fail. Restore.
```rust
#[derive(Debug,Clone,PartialEq,Eq)]pub enum Blocker{Conflict{reason:String},Dependency{reason:String},UncertainStop{run:String},Authority{reason:String}}
#[derive(Debug,Clone,PartialEq,Eq)]pub struct Entry{pub id:String,pub priority:i32,pub admission_sequence:u64,pub blockers:Vec<Blocker>}
#[derive(Debug,PartialEq,Eq)]pub enum Error{InvalidEntry,DuplicateId,DuplicateSequence}
// Owner transaction assigns immutable admission sequence; clocks are not queue order.
// This computes candidates only, never authorizes or dispatches a run.
pub fn eligible_order(entries:&[Entry])->Result<Vec<&Entry>,Error>{
 let mut ids=std::collections::BTreeSet::new();let mut seq=std::collections::BTreeSet::new();
 for e in entries{if e.id.is_empty()||e.admission_sequence==0{return Err(Error::InvalidEntry)}if !ids.insert(&e.id){return Err(Error::DuplicateId)}if !seq.insert(e.admission_sequence){return Err(Error::DuplicateSequence)}}
 let mut ready:Vec<_>=entries.iter().filter(|e|e.blockers.is_empty()).collect();
 ready.sort_by(|a,b|b.priority.cmp(&a.priority).then(a.admission_sequence.cmp(&b.admission_sequence)));Ok(ready)
}
#[cfg(test)]mod tests{
 use super::*;fn e(id:&str,p:i32,n:u64)->Entry{Entry{id:id.into(),priority:p,admission_sequence:n,blockers:vec![]}}
 #[test]fn blocked_high_priority_does_not_block_independent(){let mut urgent=e("urgent",i32::MAX,1);urgent.blockers.push(Blocker::Conflict{reason:"shared checkout".into()});let normal=e("normal",0,2);let items=[urgent,normal];assert_eq!(eligible_order(&items).unwrap().iter().map(|x|x.id.as_str()).collect::<Vec<_>>(),vec!["normal"]);}
 #[test]fn priority_then_durable_oldest_not_input_order(){let items=[e("new",3,4),e("old",3,1),e("low",-1,2),e("high",4,3)];assert_eq!(eligible_order(&items).unwrap().iter().map(|x|x.id.as_str()).collect::<Vec<_>>(),vec!["high","old","new","low"]);}
 #[test]fn urgency_cannot_remove_stop_or_dependency_blocker(){let mut x=e("x",i32::MAX,1);x.blockers=vec![Blocker::UncertainStop{run:"r".into()},Blocker::Dependency{reason:"unaccepted".into()}];assert!(eligible_order(&[x]).unwrap().is_empty());}
 #[test]fn corrupt_order_is_not_silently_tiebroken(){assert_eq!(eligible_order(&[e("x",0,1),e("x",1,2)]),Err(Error::DuplicateId));assert_eq!(eligible_order(&[e("x",0,1),e("y",0,1)]),Err(Error::DuplicateSequence));}
}
```
- [ ] Exact SQL transaction must combine eligibility recheck, current policy, conflict/dependency state, lease reservation and dispatch identity before launch. Two callers cannot both dispatch the first candidate. Pure ordering tests do not establish C04 concurrency/restart acceptance.
- [ ] Priority changes require explicit authorized actor and audit record. Observer recommendation never mutates Entry.priority. Human-requested interruption is a separate stop-confirmed flow; do not clear UncertainStop because priority is urgent.

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
- C01: Old blocked high-priority item does not stall lower-priority unrelated eligible work.
- C02: Equal-priority eligible items retain oldest-first order across restart.
- C03: Urgent conflict cannot launch on mere cancellation acknowledgment.
- C04: Priority update racing admission produces one auditable order, not duplicate dispatch.

## CI phase after every implementation iteration
- [ ] Run exact refined feature tests and core/affected-platform CI from `../prd-execution-map/design.md`. Verify at least one test actually selected; preserve failing evidence. No next iteration/round promotion while required checks fail or are missing.
- [ ] Run real acceptance: Concurrent queue/restart integration and actual-stop boundary with direct sessions included.
- [ ] Update this tasks.md with exact tested commit/tree, commands, counts, exit codes, evidence class, native environment and remaining blocks. Commit scoped files only, then CI on that integrated commit before downstream promotion.

## Rollback
Persist queue identity/order/blockers; freeze dispatch on downgrade and rebuild indices without losing original admission timestamps.
