# Execution-time profile and resource authorization execution contract

**Goal:** Validate work-profile policy at every engine entry point that reads protected content or launches tools: direct sessions, assignment operations, MCP, terminal, repository and credential selection.
**Architecture:** Existing Rust engine/proto/RPC/profile storage and native clients are the starting point. Freeze interfaces from observed source; no speculative provider API or generic framework.
**Tech stack:** Rust/Tokio/Serde/SQLite; GPUI/Swift/Worker TypeScript only if the approved surface requires them.
**Status:** executable discovery/refinement steps; product implementation NOT READY.
**Dependencies:** `work-profile-catalog`, `profile-authorization-core`. Only exact prerequisite promotion admits implementation.

## D1. Recover authority and source (one bounded read per listed anchor)
**Files:** design.md and tasks.md in this change; read-only source anchors in design.md.
- [ ] Read PRD clauses ZF-02, ZF-15, ZF-19 and every C-scenario in `specs/profile-access-enforcement/spec.md`; state excluded sibling behavior in design.md.
- [ ] From repository root, verify listed anchors exist:
```bash
python3 - <<'PY'
from pathlib import Path
paths = ['crates/engine/src/rpc.rs', 'crates/engine/src/sessions.rs', 'crates/engine/src/agent_accounts.rs', 'crates/engine/src/repos.rs', 'crates/engine/src/terminals.rs', 'crates/harness/src/lib.rs', 'crates/engine/tests/local_profiles.rs']
for name in paths:
    p = Path(name)
    assert p.is_file(), name
    print(name, len(p.read_text().splitlines()), "lines")
PY
```
Expected: one line per anchor, exit0. Missing path means re-discover with graft and correct this contract; do not create a dummy file. Read `graft/INDEX.md` then matching cards. Use `graft ask "Execution-time profile and resource authorization" --source` only if the CLI is already available; graph files are sufficient.
- [ ] In design.md, cite exact symbols/current line spans for the input, authority, persistence and side-effect paths. For each C-scenario record whether current behavior is observed, contradicted or not yet tested. Do not equate missing grep hit with absence proof.

## Core dependency
Exact synchronous evaluator source moved to `../profile-authorization-core/tasks.md`. This unit integrates it with actual engine effects and provides the internal binding surfaces needed for tests. No dependency on later public daemon activation.

## D2. Freeze one implementable contract
- [ ] Record exact DTO fields/enums, state transitions, error classes and owning API boundaries in design.md. For a research-only unit, record actual provider/version observations and explicitly blocked decisions instead of inventing DTOs.
- [ ] Assign each C-scenario one exact native test path/name and its observable assertion. C04 must include an unavailable selected account/tool with a usable global/default alternative and assert explicit unavailable, zero fallback/credential read/harness call, and unchanged stored selection. List existing files modified versus new files created, role of each file and shared-file conflicts with other changes.
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
- C01: A trusted remote device supplies a foreign profile/account/repository ID: reject before any read or child process starts.
- C02: A symlink or renamed checkout escapes the approved repository root: reject the resolved target.
- C03: Policy changes after preflight but before dispatch: dispatch rechecks and denies stale authority.
- C04: An unavailable requested account/tool must report unavailable, not fall back to a global default.
- C05: Direct session and assignment invoking the same protected operation receive equivalent authorization decisions.

## CI phase after every implementation iteration
- [ ] Run exact refined feature tests and core/affected-platform CI from `../prd-execution-map/design.md`. Verify at least one test actually selected; preserve failing evidence. No next iteration/round promotion while required checks fail or are missing.
- [ ] Run real acceptance: Instrument real engine dispatch boundaries and prove unauthorized paths perform zero protected reads/effects; approved isolated account succeeds.
- [ ] Update this tasks.md with exact tested commit/tree, commands, counts, exit codes, evidence class, native environment and remaining blocks. Commit scoped files only, then CI on that integrated commit before downstream promotion.

## Rollback
Roll back enforcement code only with execution disabled for newly bound profiles. Never turn unknown policy into allow to preserve compatibility.
