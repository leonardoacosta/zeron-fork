# Desktop assignment and intervention surface execution contract

**Goal:** Add explicit create/promote/read/history/launch controls alongside direct sessions.
**Architecture:** Existing Rust engine/proto/RPC/profile storage and native clients are the starting point. Freeze interfaces from observed source; no speculative provider API or generic framework.
**Tech stack:** Rust/Tokio/Serde/SQLite; GPUI/Swift/Worker TypeScript only if the approved surface requires them.
**Status:** executable discovery/refinement steps; product implementation NOT READY.
**Dependencies:** `manual-investigation-runner`. Read-only research can proceed without using unimplemented prerequisite APIs; implementation waits for all prerequisite CI promotion records.

## D1. Recover authority and source (one bounded read per listed anchor)
**Files:** design.md and tasks.md in this change; read-only source anchors in design.md.
- [ ] Read PRD clauses ZF-01, ZF-02, ZF-03, ZF-04, ZF-05, ZF-06, ZF-14, ZF-18 and every C-scenario in `specs/assignment-desktop-surface/spec.md`; state excluded sibling behavior in design.md.
- [ ] From repository root, verify listed anchors exist:
```bash
python3 - <<'PY'
from pathlib import Path
paths = ['crates/ui/src/state.rs', 'crates/ui/src/shell.rs', 'crates/ui/src/settings.rs', 'crates/ui/src/notify.rs', 'crates/proto/src/assignment.rs']
for name in paths:
    p = Path(name)
    assert p.is_file(), name
    print(name, len(p.read_text().splitlines()), "lines")
PY
```
Expected: one line per anchor, exit0. Missing path means re-discover with graft and correct this contract; do not create a dummy file. Read `graft/INDEX.md` then matching cards. Use `graft ask "Desktop assignment and intervention surface" --source` only if the CLI is already available; graph files are sufficient.
- [ ] In design.md, cite exact symbols/current line spans for the input, authority, persistence and side-effect paths. For each C-scenario record whether current behavior is observed, contradicted or not yet tested. Do not equate missing grep hit with absence proof.

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
- C01: Open ordinary conversation: no forced assignment administration.
- C02: Promote requires explicit action and preserves transcript.
- C03: Disconnected owner or old capability: show unavailable/unsupported, never local duplicate.
- C04: Screen-reader/keyboard user can inspect workflow reason and stop uncertainty without relying on color.

## CI phase after every implementation iteration
- [ ] Run exact refined feature tests and core/affected-platform CI from `../prd-execution-map/design.md`. Verify at least one test actually selected; preserve failing evidence. No next iteration/round promotion while required checks fail or are missing.
- [ ] Run real acceptance: Native GPUI workflow with actual owner/client, keyboard/focus/accessibility checks and zero implicit assignments.
- [ ] Update this tasks.md with exact tested commit/tree, commands, counts, exit codes, evidence class, native environment and remaining blocks. Commit scoped files only, then CI on that integrated commit before downstream promotion.

## Rollback
Feature-gate presentation, keep stored records intact; remove UI entry points without deleting assignments. Preserve old client capability behavior.
