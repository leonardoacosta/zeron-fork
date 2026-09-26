# Confirmed stopping and explicit human handoff execution contract

**Goal:** Define pause-requested, stopping, stopped-confirmed, human-owned, handback-requested and resumable states with guarded transitions.
**Architecture:** Existing Rust engine/proto/RPC/profile storage and native clients are the starting point. Freeze interfaces from observed source; no speculative provider API or generic framework.
**Tech stack:** Rust/Tokio/Serde/SQLite; GPUI/Swift/Worker TypeScript only if the approved surface requires them.
**Status:** executable discovery/refinement steps; product implementation NOT READY.
**Dependencies:** `profile-access-enforcement`, `harness-preflight-binding`. Only exact prerequisite promotion admits implementation.

## D1. Recover authority and source (one bounded read per listed anchor)
**Files:** design.md and tasks.md in this change; read-only source anchors in design.md.
- [ ] Read PRD clauses ZF-04, ZF-15, ZF-10 and every C-scenario in `specs/confirmed-stop-handoff/spec.md`; state excluded sibling behavior in design.md.
- [ ] From repository root, verify listed anchors exist:
```bash
python3 - <<'PY'
from pathlib import Path
paths = ['crates/engine/src/sessions.rs', 'crates/harness/src/lib.rs', 'crates/engine/src/terminals.rs', 'crates/engine/src/rpc.rs', 'crates/engine/tests/turn_quiesce.rs', 'crates/engine/tests/self_continued_quiesce.rs']
for name in paths:
    p = Path(name)
    assert p.is_file(), name
    print(name, len(p.read_text().splitlines()), "lines")
PY
```
Expected: one line per anchor, exit0. Missing path means re-discover with graft and correct this contract; do not create a dummy file. Read `graft/INDEX.md` then matching cards. Use `graft ask "Confirmed stopping and explicit human handoff" --source` only if the CLI is already available; graph files are sufficient.
- [ ] In design.md, cite exact symbols/current line spans for the input, authority, persistence and side-effect paths. For each C-scenario record whether current behavior is observed, contradicted or not yet tested. Do not equate missing grep hit with absence proof.

## A. Exact pure transition proposal and tests
**Proposed create:** `crates/engine/src/assignment_lifecycle.rs`. **Proposed modify:** `crates/engine/src/lib.rs` adds private `mod assignment_lifecycle;`. This core is not a stopped-process implementation and cannot be exposed as a public claim-producing RPC.

- [ ] Place the test module at the end of the following block first; run `cargo test --locked -p zeron-engine --lib assignment_lifecycle::tests` and record missing-type red. Then add the preceding definitions exactly. A compile failure alone does not prove behavioral sensitivity; next negative control is required.
```rust
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Phase {
    Running,
    StopRequested,
    StopUncertain,
    StoppedConfirmed,
    HumanOwned,
    HandbackPending,
}
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum StopObservation {
    ReceiptOnly,
    Unknown,
    ScopeQuiescent,
}
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Error {
    StaleGeneration,
    InvalidTransition,
    AuthorityRequired,
    GenerationExhausted,
}
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Lifecycle {
    generation: u64,
    phase: Phase,
}
impl Lifecycle {
    pub fn running(generation: u64) -> Result<Self, Error> {
        if generation == 0 {
            return Err(Error::StaleGeneration);
        }
        Ok(Self {
            generation,
            phase: Phase::Running,
        })
    }
    pub fn phase(&self) -> Phase {
        self.phase
    }
    pub fn generation(&self) -> u64 {
        self.generation
    }
    fn check(&self, generation: u64) -> Result<(), Error> {
        if generation == self.generation {
            Ok(())
        } else {
            Err(Error::StaleGeneration)
        }
    }
    pub fn request_stop(&mut self, generation: u64) -> Result<(), Error> {
        self.check(generation)?;
        match self.phase {
            Phase::Running => self.phase = Phase::StopRequested,
            Phase::StopRequested | Phase::StopUncertain | Phase::StoppedConfirmed => {}
            _ => return Err(Error::InvalidTransition),
        }
        Ok(())
    }
    // Owner-only observation. Never construct ScopeQuiescent from client claims,
    // stream EOF, token delivery, elapsed grace, or lack of recent file writes.
    pub fn observe_stop(
        &mut self,
        generation: u64,
        observation: StopObservation,
    ) -> Result<(), Error> {
        self.check(generation)?;
        if !matches!(self.phase, Phase::StopRequested | Phase::StopUncertain) {
            return Err(Error::InvalidTransition);
        }
        match observation {
            StopObservation::ReceiptOnly => {}
            StopObservation::Unknown => self.phase = Phase::StopUncertain,
            StopObservation::ScopeQuiescent => self.phase = Phase::StoppedConfirmed,
        }
        Ok(())
    }
    pub fn take_over(&mut self, generation: u64) -> Result<(), Error> {
        self.check(generation)?;
        match self.phase {
            Phase::StoppedConfirmed => self.phase = Phase::HumanOwned,
            Phase::HumanOwned => {}
            _ => return Err(Error::InvalidTransition),
        }
        Ok(())
    }
    pub fn request_handback(&mut self, generation: u64) -> Result<(), Error> {
        self.check(generation)?;
        match self.phase {
            Phase::HumanOwned => self.phase = Phase::HandbackPending,
            Phase::HandbackPending => {}
            _ => return Err(Error::InvalidTransition),
        }
        Ok(())
    }
    pub fn resume(&mut self, generation: u64, authority_revalidated: bool) -> Result<u64, Error> {
        self.check(generation)?;
        if self.phase != Phase::HandbackPending {
            return Err(Error::InvalidTransition);
        }
        if !authority_revalidated {
            return Err(Error::AuthorityRequired);
        }
        let next = self
            .generation
            .checked_add(1)
            .ok_or(Error::GenerationExhausted)?;
        self.generation = next;
        self.phase = Phase::Running;
        Ok(next)
    }
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn receipt_and_unknown_never_allow_takeover() {
        let mut x = Lifecycle::running(1).unwrap();
        x.request_stop(1).unwrap();
        x.observe_stop(1, StopObservation::ReceiptOnly).unwrap();
        assert_eq!(x.phase(), Phase::StopRequested);
        assert_eq!(x.take_over(1), Err(Error::InvalidTransition));
        x.observe_stop(1, StopObservation::Unknown).unwrap();
        assert_eq!(x.phase(), Phase::StopUncertain);
        assert_eq!(x.take_over(1), Err(Error::InvalidTransition));
    }
    #[test]
    fn explicit_handback_and_fresh_authority_required() {
        let mut x = Lifecycle::running(7).unwrap();
        x.request_stop(7).unwrap();
        x.request_stop(7).unwrap();
        x.observe_stop(7, StopObservation::ScopeQuiescent).unwrap();
        x.take_over(7).unwrap();
        x.take_over(7).unwrap();
        assert_eq!(x.resume(7, true), Err(Error::InvalidTransition));
        x.request_handback(7).unwrap();
        x.request_handback(7).unwrap();
        assert_eq!(x.resume(7, false), Err(Error::AuthorityRequired));
        assert_eq!(x.phase(), Phase::HandbackPending);
        assert_eq!(x.resume(7, true), Ok(8));
        assert_eq!(x.resume(7, true), Err(Error::StaleGeneration));
        assert_eq!(
            x.observe_stop(7, StopObservation::ScopeQuiescent),
            Err(Error::StaleGeneration)
        );
    }
    #[test]
    fn unrelated_run_unaffected_and_overflow_atomic() {
        let y = Lifecycle::running(2).unwrap();
        let mut x = Lifecycle::running(u64::MAX).unwrap();
        x.request_stop(u64::MAX).unwrap();
        x.observe_stop(u64::MAX, StopObservation::ScopeQuiescent)
            .unwrap();
        x.take_over(u64::MAX).unwrap();
        x.request_handback(u64::MAX).unwrap();
        assert_eq!(x.resume(u64::MAX, true), Err(Error::GenerationExhausted));
        assert_eq!(x.phase(), Phase::HandbackPending);
        assert_eq!(y.phase(), Phase::Running);
    }
}
```
- [ ] Run `cargo test --locked -p zeron-engine --lib assignment_lifecycle::tests`; require three tests pass. In an isolated scratch copy, change ReceiptOnly branch to set StoppedConfirmed: `receipt_and_unknown_never_allow_takeover` must fail. Restore before commit.
- [ ] Do not promote full change after core tests. `ScopeQuiescent` is owner-only evidence from a verified process/action scope observer, never a request field. `authority_revalidated` is an internal predicate result, never a client-provided boolean. At integration replace direct boolean passing with the concrete private AuthorizationPermit from profile-access-enforcement; exact permit handoff must be typed before effectful code is admitted.
- [ ] Persist generation/transition/replay receipt atomically before acknowledgment. The pure struct mutates memory only and must be wrapped by the real store transaction before RPC use. This required integration is not supplied by these tests.

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
- C01: Cancel RPC acknowledges while a spawned child continues writing: status stays stopping and takeover is refused.
- C02: Network disappears during stop: mark uncertain, block conflicting work, keep unrelated isolated work running.
- C03: Repeated pause/handback commands are idempotent without duplicate launches.
- C04: A stale handback for an older run generation cannot resume the replacement run.

## CI phase after every implementation iteration
- [ ] Run exact refined feature tests and core/affected-platform CI from `../prd-execution-map/design.md`. Verify at least one test actually selected; preserve failing evidence. No next iteration/round promotion while required checks fail or are missing.
- [ ] Run real acceptance: Real harmless subprocess with descendant writes proves last write/exit boundary; native harness-specific stopping requires its own evidence.
- [ ] Update this tasks.md with exact tested commit/tree, commands, counts, exit codes, evidence class, native environment and remaining blocks. Commit scoped files only, then CI on that integrated commit before downstream promotion.

## Rollback
Persist lifecycle transition before acknowledgment. Downgrade active/uncertain work to hold; no replay of unconfirmed external effects.

## Exact embedded-code validation
On2026-09-26 20:28UTC the Rust block was extracted from this canonical tasks.md, compiled with `rustc --edition=2024 --test`, and its tests passed. This validates the literal proposed pure core, not production integration or whole-unit acceptance. Evidence: overnight run overnight_1790451935422_12840308488589231076 validation/exact-embedded-core-tests.json.

Quality check20:38UTC: exact proposal blocks formatted in isolated scratch crate; combined20 tests and clippy all-targets with warnings denied pass. These are pure-module checks, not engine integration. Private unused modules cannot independently pass production dead-code lint; integrate their real consumer in the same admitted change rather than add blanket allows or export internal authority types merely to silence warnings.
