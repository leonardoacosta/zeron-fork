# Configured verification and acceptance transitions execution contract

**Goal:** Keep agent-finished, verified, accepted, delivered and outcome-confirmed separate.
**Architecture:** Existing Rust engine/proto/RPC/profile storage and native clients are the starting point. Freeze interfaces from observed source; no speculative provider API or generic framework.
**Tech stack:** Rust/Tokio/Serde/SQLite; GPUI/Swift/Worker TypeScript only if the approved surface requires them.
**Status:** executable discovery/refinement steps; product implementation NOT READY.
**Dependencies:** `workflow-version-selection`, `revision-evidence-bindings`, `profile-access-enforcement`. Only exact prerequisite promotion admits implementation.

## D1. Recover authority and source (one bounded read per listed anchor)
**Files:** design.md and tasks.md in this change; read-only source anchors in design.md.
- [ ] Read PRD clauses ZF-05, ZF-14, ZF-11 and every C-scenario in `specs/verification-acceptance-gates/spec.md`; state excluded sibling behavior in design.md.
- [ ] From repository root, verify listed anchors exist:
```bash
python3 - <<'PY'
from pathlib import Path
paths = ['crates/engine/src/rpc.rs', 'crates/proto/src/assignment.rs', 'crates/sync/src/store.rs', 'crates/engine/src/run_journal.rs']
for name in paths:
    p = Path(name)
    assert p.is_file(), name
    print(name, len(p.read_text().splitlines()), "lines")
PY
```
Expected: one line per anchor, exit0. Missing path means re-discover with graft and correct this contract; do not create a dummy file. Read `graft/INDEX.md` then matching cards. Use `graft ask "Configured verification and acceptance transitions" --source` only if the CLI is already available; graph files are sufficient.
- [ ] In design.md, cite exact symbols/current line spans for the input, authority, persistence and side-effect paths. For each C-scenario record whether current behavior is observed, contradicted or not yet tested. Do not equate missing grep hit with absence proof.

## A. Exact verification predicate proposal
**Proposed create:** `crates/engine/src/output_verification.rs`; **modify:** `crates/engine/src/lib.rs` private module declaration. This proposed core evaluates an owner-selected evidence set. It does not record acceptance, run checks, prove artifact truth, or authorize delivery. The content digest binds the full immutable output context described by revision-evidence-bindings, not merely a commit string.

- [ ] Add test module then definitions below. Run `cargo test --locked -p zeron-engine --lib output_verification::tests`; require4 tests. Prove behavioral red in scratch by removing binding equality and requiring the stale-evidence test to fail. Restore before commit.
```rust
use std::collections::BTreeSet;
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct OutputBinding {
    pub output_id: String,
    pub revision: u64,
    pub content_digest: String,
}
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum EvidenceClass {
    Structural,
    Synthetic,
    RealWorkflow,
}
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum CheckOutcome {
    Passed,
    Failed,
    Blocked,
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct CheckEvidence {
    pub check_id: String,
    pub binding: OutputBinding,
    pub class: EvidenceClass,
    pub outcome: CheckOutcome,
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct CheckRequirement {
    pub check_id: String,
    pub class: EvidenceClass,
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Hold {
    EmptyRequirements,
    DuplicateRequirement,
    InvalidBinding,
    Missing(String),
    Stale(String),
    Contradictory(String),
    WrongClass(String),
    NotPassed(String),
}
// Pure verification evaluation, not acceptance or delivery authorization.
// Only owner-recorded evidence may enter this evaluator; clients cannot assert Passed.
pub fn verification_ready(
    binding: &OutputBinding,
    required: &[CheckRequirement],
    evidence: &[CheckEvidence],
) -> Result<(), Hold> {
    if binding.output_id.is_empty()
        || binding.revision == 0
        || binding.content_digest.len() != 64
        || !binding
            .content_digest
            .bytes()
            .all(|b| b.is_ascii_digit() || (b'a'..=b'f').contains(&b))
    {
        return Err(Hold::InvalidBinding);
    }
    if required.is_empty() {
        return Err(Hold::EmptyRequirements);
    }
    let mut ids = BTreeSet::new();
    for req in required {
        if req.check_id.is_empty() || !ids.insert(&req.check_id) {
            return Err(Hold::DuplicateRequirement);
        }
        let rows: Vec<_> = evidence
            .iter()
            .filter(|e| e.check_id == req.check_id)
            .collect();
        if rows.is_empty() {
            return Err(Hold::Missing(req.check_id.clone()));
        }
        // Preserve historical rows separately. Caller must select exact evidence set;
        // a mixture of bindings cannot pass by optimistic filtering.
        if rows.iter().any(|e| e.binding != *binding) {
            return Err(Hold::Stale(req.check_id.clone()));
        }
        if rows
            .windows(2)
            .any(|r| r[0].outcome != r[1].outcome || r[0].class != r[1].class)
        {
            return Err(Hold::Contradictory(req.check_id.clone()));
        }
        if rows[0].class != req.class {
            return Err(Hold::WrongClass(req.check_id.clone()));
        }
        if rows[0].outcome != CheckOutcome::Passed {
            return Err(Hold::NotPassed(req.check_id.clone()));
        }
    }
    Ok(())
}
#[cfg(test)]
mod tests {
    use super::*;
    fn binding() -> OutputBinding {
        OutputBinding {
            output_id: "o".into(),
            revision: 1,
            content_digest: "a".repeat(64),
        }
    }
    fn req() -> CheckRequirement {
        CheckRequirement {
            check_id: "acceptance".into(),
            class: EvidenceClass::RealWorkflow,
        }
    }
    fn row() -> CheckEvidence {
        CheckEvidence {
            check_id: "acceptance".into(),
            binding: binding(),
            class: EvidenceClass::RealWorkflow,
            outcome: CheckOutcome::Passed,
        }
    }
    #[test]
    fn exact_pass_does_not_imply_acceptance_or_delivery() {
        assert_eq!(verification_ready(&binding(), &[req()], &[row()]), Ok(()));
    }
    #[test]
    fn empty_missing_and_duplicate_requirements_hold() {
        assert_eq!(
            verification_ready(&binding(), &[], &[]),
            Err(Hold::EmptyRequirements)
        );
        assert!(matches!(
            verification_ready(&binding(), &[req()], &[]),
            Err(Hold::Missing(_))
        ));
        assert_eq!(
            verification_ready(&binding(), &[req(), req()], &[row()]),
            Err(Hold::DuplicateRequirement)
        );
    }
    #[test]
    fn new_dirty_tree_or_revision_stales_old_evidence() {
        for changed in [
            OutputBinding {
                revision: 2,
                ..binding()
            },
            OutputBinding {
                content_digest: "b".repeat(64),
                ..binding()
            },
        ] {
            assert!(matches!(
                verification_ready(&changed, &[req()], &[row()]),
                Err(Hold::Stale(_))
            ));
        }
    }
    #[test]
    fn synthetic_and_contradictory_cannot_promote() {
        let synthetic = CheckEvidence {
            class: EvidenceClass::Synthetic,
            ..row()
        };
        assert!(matches!(
            verification_ready(&binding(), &[req()], &[synthetic]),
            Err(Hold::WrongClass(_))
        ));
        let failed = CheckEvidence {
            outcome: CheckOutcome::Failed,
            ..row()
        };
        assert!(matches!(
            verification_ready(&binding(), &[req()], &[row(), failed]),
            Err(Hold::Contradictory(_))
        ));
        let blocked = CheckEvidence {
            outcome: CheckOutcome::Blocked,
            ..row()
        };
        assert!(matches!(
            verification_ready(&binding(), &[req()], &[blocked]),
            Err(Hold::NotPassed(_))
        ));
    }
}
```
- [ ] Persisted acceptance must additionally verify workflow gate mode, current authority, external reviewer decisions, exact output identity and required evidence. Do not accept a client-written Passed entry as owner observation. This function returning Ok is necessary verification readiness, not sufficient acceptance.
- [ ] Superseded failed evidence is retained historically. A new explicitly bound check attempt/evidence-set may replace it for evaluation only with recorded provenance; never silently filter out a current contradictory row to obtain green.
- [ ] Full immutable evidence schema, typed artifact references, review authority and atomic acceptance persistence must be implemented in remaining tasks before full-unit promotion. Do not expose this helper alone as an Accept RPC.

## D2. Freeze one implementable contract
- [ ] Record exact DTO fields/enums, state transitions, error classes and owning API boundaries in design.md. For a research-only unit, record actual provider/version observations and explicitly blocked decisions instead of inventing DTOs.
- [ ] Assign each C-scenario one exact owner-RPC/native test path/name and observable assertion. For C04, configure at least one passing internal check plus a required external-review row; persist an explicit external rejection, assert the gate remains held/unaccepted despite the pass, restart the owner store, and re-read the same output/evidence binding to assert the rejection and held decision remain. Assert no acceptance or delivery/effect record appears. Do not substitute an internal-test failure for external rejection. List existing files modified versus new files created, role of each file and shared-file conflicts with other changes.
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
- C01: Agent reports success while required check fails: verified/accepted stay false.
- C02: Autonomous gate with all required checks and valid policy accepts without inventing a universal manual approval.
- C03: Human approval for output A cannot apply to changed output B.
- C04: External reviewer rejects a required review while internal tests pass: gate remains held.

## CI phase after every implementation iteration
- [ ] Run exact refined feature tests and core/affected-platform CI from `../prd-execution-map/design.md`. Verify at least one test actually selected; preserve failing evidence. No next iteration/round promotion while required checks fail or are missing.
- [ ] Run real acceptance: Owner RPC transitions with stale/revoked/external-rejection cases and restart at decision commit boundary.
- [ ] Update this tasks.md with exact tested commit/tree, commands, counts, exit codes, evidence class, native environment and remaining blocks. Commit scoped files only, then CI on that integrated commit before downstream promotion.

## Rollback
Persist decision and inputs atomically, append revisions instead of rewriting past approvals. Rollback holds unsupported decisions.

## Exact embedded-code validation
On2026-09-26 20:28UTC the Rust block was extracted from this canonical tasks.md, compiled with `rustc --edition=2024 --test`, and its tests passed. This validates the literal proposed pure core, not production integration or whole-unit acceptance. Evidence: overnight run overnight_1790451935422_12840308488589231076 validation/exact-embedded-core-tests.json.

Quality check20:38UTC: exact proposal blocks formatted in isolated scratch crate; combined20 tests and clippy all-targets with warnings denied pass. These are pure-module checks, not engine integration. Private unused modules cannot independently pass production dead-code lint; integrate their real consumer in the same admitted change rather than add blanket allows or export internal authority types merely to silence warnings.
