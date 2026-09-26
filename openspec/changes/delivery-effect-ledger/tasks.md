# Independent delivery authorization and effect reconciliation execution contract

**Goal:** Define independently callable push/create-PR/merge/release/deploy/publish intents, each bound to exact candidate, destination, account reference and workflow action policy.
**Architecture:** Existing Rust engine/proto/RPC/profile storage and native clients are the starting point. Freeze interfaces from observed source; no speculative provider API or generic framework.
**Tech stack:** Rust/Tokio/Serde/SQLite; GPUI/Swift/Worker TypeScript only if the approved surface requires them.
**Status:** executable discovery/refinement steps; product implementation NOT READY.
**Dependencies:** `verification-acceptance-gates`, `safe-resume-reconciliation`. Read-only research can proceed without using unimplemented prerequisite APIs; implementation waits for all prerequisite CI promotion records.

## D1. Recover authority and source (one bounded read per listed anchor)
**Files:** design.md and tasks.md in this change; read-only source anchors in design.md.
- [ ] Read PRD clauses ZF-07, ZF-04, ZF-14 and every C-scenario in `specs/delivery-effect-ledger/spec.md`; state excluded sibling behavior in design.md.
- [ ] From repository root, verify listed anchors exist:
```bash
python3 - <<'PY'
from pathlib import Path
paths = ['crates/engine/src/source_control.rs', 'crates/engine/src/change_requests.rs', 'crates/engine/src/rpc.rs', 'crates/sync/src/store.rs', 'crates/proto/src/assignment.rs']
for name in paths:
    p = Path(name)
    assert p.is_file(), name
    print(name, len(p.read_text().splitlines()), "lines")
PY
```
Expected: one line per anchor, exit0. Missing path means re-discover with graft and correct this contract; do not create a dummy file. Read `graft/INDEX.md` then matching cards. Use `graft ask "Independent delivery authorization and effect reconciliation" --source` only if the CLI is already available; graph files are sufficient.
- [ ] In design.md, cite exact symbols/current line spans for the input, authority, persistence and side-effect paths. For each C-scenario record whether current behavior is observed, contradicted or not yet tested. Do not equate missing grep hit with absence proof.

## A. Exact effect uncertainty core proposal
**Proposed create:** `crates/engine/src/delivery_state.rs`; **modify:** `crates/engine/src/lib.rs` with private module declaration. Pure core below is not an external-action API or a durable receipt. Binding and observations must come from owner-validated records, never client authority booleans.

- [ ] Add tests first then complete definitions; `cargo test --locked -p zeron-engine --lib delivery_state::tests` must select4 tests and pass. Remove uncertainty rejection in a scratch negative control and require crash test failure. Restore before commit.
```rust
#[derive(Debug,Clone,Copy,PartialEq,Eq)]pub enum Action{Push,CreatePr,Merge,Release,Deploy,Publish}
#[derive(Debug,Clone,PartialEq,Eq)]pub struct Binding{pub candidate_digest:String,pub destination:String,pub account_ref:String,pub action:Action,pub policy_revision:u64}
#[derive(Debug,Clone,Copy,PartialEq,Eq)]pub enum Phase{Planned,Dispatched,Uncertain,ObservedSuccess,ObservedFailure,ReconciledAbsent}
#[derive(Debug,Clone,Copy,PartialEq,Eq)]pub enum Observation{Succeeded,Failed,Unknown,AbsentVerified}
#[derive(Debug,Clone,Copy,PartialEq,Eq)]pub enum Error{InvalidBinding,AuthorityRequired,BindingChanged,ReconciliationRequired,InvalidTransition,AttemptExhausted}
#[derive(Debug,Clone,PartialEq,Eq)]pub struct Delivery{binding:Binding,phase:Phase,attempt:u64}
impl Delivery{
 pub fn plan(binding:Binding)->Result<Self,Error>{if binding.candidate_digest.len()!=64||!binding.candidate_digest.bytes().all(|x|x.is_ascii_digit()||(b'a'..=b'f').contains(&x))||binding.destination.trim().is_empty()||binding.account_ref.trim().is_empty()||binding.policy_revision==0{return Err(Error::InvalidBinding)}Ok(Self{binding,phase:Phase::Planned,attempt:0})}
 pub fn phase(&self)->Phase{self.phase}
 // owner-only checked authority, not client boolean. Persist before issuing effect.
 pub fn dispatch(&mut self,current:&Binding,authorized:bool)->Result<u64,Error>{if &self.binding!=current{return Err(Error::BindingChanged)}if !authorized{return Err(Error::AuthorityRequired)}match self.phase{Phase::Uncertain|Phase::Dispatched=>return Err(Error::ReconciliationRequired),Phase::Planned|Phase::ReconciledAbsent=>{},_=>return Err(Error::InvalidTransition)}let next=self.attempt.checked_add(1).ok_or(Error::AttemptExhausted)?;self.attempt=next;self.phase=Phase::Dispatched;Ok(next)}
 pub fn observe(&mut self,attempt:u64,observation:Observation)->Result<(),Error>{if attempt!=self.attempt||!matches!(self.phase,Phase::Dispatched|Phase::Uncertain){return Err(Error::InvalidTransition)}self.phase=match observation{Observation::Succeeded=>Phase::ObservedSuccess,Observation::Failed=>Phase::ObservedFailure,Observation::Unknown=>Phase::Uncertain,Observation::AbsentVerified=>Phase::ReconciledAbsent};Ok(())}
 pub fn recover(&mut self){if self.phase==Phase::Dispatched{self.phase=Phase::Uncertain}}
}
#[cfg(test)]mod tests{
 use super::*;fn b()->Binding{Binding{candidate_digest:"a".repeat(64),destination:"local:test".into(),account_ref:"account-a".into(),action:Action::Deploy,policy_revision:1}}
 #[test]fn accepted_candidate_is_not_action_authority(){let mut d=Delivery::plan(b()).unwrap();assert_eq!(d.dispatch(&b(),false),Err(Error::AuthorityRequired));assert_eq!(d.phase(),Phase::Planned);assert_eq!(d.dispatch(&b(),true),Ok(1));}
 #[test]fn crash_never_blindly_replays(){let mut d=Delivery::plan(b()).unwrap();d.dispatch(&b(),true).unwrap();d.recover();assert_eq!(d.dispatch(&b(),true),Err(Error::ReconciliationRequired));d.observe(1,Observation::Unknown).unwrap();assert_eq!(d.dispatch(&b(),true),Err(Error::ReconciliationRequired));d.observe(1,Observation::AbsentVerified).unwrap();assert_eq!(d.dispatch(&b(),false),Err(Error::AuthorityRequired));assert_eq!(d.dispatch(&b(),true),Ok(2));assert_eq!(d.observe(1,Observation::Succeeded),Err(Error::InvalidTransition));}
 #[test]fn changed_destination_account_candidate_and_policy_need_new_binding(){for changed in [Binding{destination:"other".into(),..b()},Binding{account_ref:"other".into(),..b()},Binding{candidate_digest:"b".repeat(64),..b()},Binding{policy_revision:2,..b()}]{let mut d=Delivery::plan(b()).unwrap();assert_eq!(d.dispatch(&changed,true),Err(Error::BindingChanged));}}
 #[test]fn observed_success_not_redispatched(){let mut d=Delivery::plan(b()).unwrap();d.dispatch(&b(),true).unwrap();d.observe(1,Observation::Succeeded).unwrap();assert_eq!(d.dispatch(&b(),true),Err(Error::InvalidTransition));}
}
```
- [ ] Persist transition to Dispatched and attempt identity atomically before invoking any provider. Crash before/after effect but before observation always recovers Uncertain. The in-memory `recover` method is not durable recovery until real storage integration is supplied.
- [ ] `AbsentVerified` requires authoritative provider reconciliation that excludes pending/eventually consistent duplicate effects. A404/list miss alone is insufficient. Unsupported reconciliation remains Uncertain and holds for human decision. A failed HTTP response can still have effects; classify Unknown unless absence is proved.
- [ ] Explicit new action binding is required after account/destination/candidate/policy change. Do not mutate an uncertain binding to retry elsewhere. Success is observed delivery only, not combined outcome confirmation.
- [ ] Async effect authorization consumes concrete private permit and generation at dispatch; the boolean in this pure model is an internal test seam, not wire input. Full permission/provider/persistence patches remain mandatory before runtime promotion.

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
- C01: Accepted candidate without deploy permission cannot deploy.
- C02: Autonomous action policy may authorize one action without universal per-action dialog.
- C03: Crash after provider mutation before acknowledgment: uncertain record, query existing effect before retry.
- C04: Destination/account changes after approval: new authorization binding required.

## CI phase after every implementation iteration
- [ ] Run exact refined feature tests and core/affected-platform CI from `../prd-execution-map/design.md`. Verify at least one test actually selected; preserve failing evidence. No next iteration/round promotion while required checks fail or are missing.
- [ ] Run real acceptance: Controlled local external-effect fixture with crash boundaries, plus each adapter's separate authorized real destination gate.
- [ ] Update this tasks.md with exact tested commit/tree, commands, counts, exit codes, evidence class, native environment and remaining blocks. Commit scoped files only, then CI on that integrated commit before downstream promotion.

## Rollback
Append-only effect records retained across downgrade. Disable new dispatch if reconciliation unsupported; never delete uncertainty to unblock work.
