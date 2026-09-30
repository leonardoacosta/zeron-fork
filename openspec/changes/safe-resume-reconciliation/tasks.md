# Recovery with continuing authority and effect reconciliation execution contract

**Goal:** On crash/reconnect reconstruct frozen configuration, authorization, native session identity and effect uncertainty.
**Architecture:** Existing Rust engine/proto/RPC/profile storage and native clients are the starting point. Freeze interfaces from observed source; no speculative provider API or generic framework.
**Tech stack:** Rust/Tokio/Serde/SQLite; GPUI/Swift/Worker TypeScript only if the approved surface requires them.
**Status:** executable discovery/refinement steps; product implementation NOT READY.
**Dependencies:** `confirmed-stop-handoff`, `run-resource-ledger`. Only exact prerequisite promotion admits implementation.

## D1. Recover authority and source (one bounded read per listed anchor)
**Files:** design.md and tasks.md in this change; read-only source anchors in design.md.
- [ ] Read PRD clauses ZF-04, ZF-14 and every C-scenario in `specs/safe-resume-reconciliation/spec.md`; state excluded sibling behavior in design.md.
- [ ] From repository root, verify listed anchors exist:
```bash
python3 - <<'PY'
from pathlib import Path
paths = ['crates/engine/src/run_journal.rs', 'crates/engine/src/sessions.rs', 'crates/engine/src/lib.rs', 'crates/engine/tests/restart_resume.rs', 'crates/engine/tests/session_publication.rs']
for name in paths:
    p = Path(name)
    assert p.is_file(), name
    print(name, len(p.read_text().splitlines()), "lines")
PY
```
Expected: one line per anchor, exit0. Missing path means re-discover with graft and correct this contract; do not create a dummy file. Read `graft/INDEX.md` then matching cards. Use `graft ask "Recovery with continuing authority and effect reconciliation" --source` only if the CLI is already available; graph files are sufficient.
- [ ] In design.md, cite exact symbols/current line spans for the input, authority, persistence and side-effect paths. For each C-scenario record whether current behavior is observed, contradicted or not yet tested. Do not equate missing grep hit with absence proof.

## D2. Freeze one implementable contract
- [ ] Resolve the design's legacy startup admission prerequisite before implementation admission: trace `assemble_with_profile_locked` → `recover_stale`, freeze binding/current-policy/effect-safety admission at the owning boot-recovery boundary before retry accounting and revival scheduling, and specify retained evidence for old journals missing bindings. Freshness, retry budget, prompt deduplication, remembered identity and the `last_request`/`request_from_chat_row`/journal-cwd fallback are not authorization or proof of reconstructed frozen configuration. Hold missing evidence without dispatch, resend or default substitution; record exact persisted representation through the interface-freeze task below rather than inventing an API here.
- [ ] Record explicit compatibility/test disposition for `crates/engine/tests/restart_resume.rs::fresh_crash_auto_resumes_and_notes_the_interruption` (verified span `569-693`): split or revise, never silently delete its regression coverage. Map its existing insufficient-evidence fixture to held recovery with zero harness dispatch/external effects, retained interrupted transcript/journal and no false resuming note. Require a second restart to remain held without a launch/resume-attempt increment or substituted defaults. Map a separate positively bound, currently authorized, reconciled fixture to permitted automatic continuation while retaining interruption-note, no-duplicate-user-message and original-native-identity assertions. Freeze exact resulting test names/assertions before implementation; these proposed cases neither prove acceptance nor replace C02/C04.
- [ ] Record exact DTO fields/enums, state transitions, error classes and owning API boundaries in design.md. For a research-only unit, record actual provider/version observations and explicitly blocked decisions instead of inventing DTOs.
- [ ] Assign each C-scenario one exact native test path/name and its observable assertion. For C04, start with a persisted run bound to a specific native session/account/environment, make that exact session unavailable on restart, and assert the run is Held/Uncertain with a typed unavailability reason, original binding unchanged, zero alternate account/environment selection, zero resume/dispatch calls and zero external effects. Re-read after a second restart and assert it remains held until explicit reconciliation; do not make native unavailability a substitute for permission-revocation coverage. List existing files modified versus new files created, role of each file and shared-file conflicts with other changes.
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
- C01: Crash after dispatch but before receipt: no blind resend of an external mutation.
- C02: Profile permission revoked while owner is down: restart cannot auto-resume old authority.
- C03: Journal has torn final entry: recover known prefix and mark missing effects uncertain.
- C04: Native session unavailable: do not substitute a new account/environment or claim continuation.

## CI phase after every implementation iteration
- [ ] Run exact refined feature tests and core/affected-platform CI from `../prd-execution-map/design.md`. Verify at least one test actually selected; preserve failing evidence. No next iteration/round promotion while required checks fail or are missing.
- [ ] Run real acceptance: Crash-boundary subprocess tests and authorized native restart with revoked-policy negative case; no external side effect replay.
- [ ] Update this tasks.md with exact tested commit/tree, commands, counts, exit codes, evidence class, native environment and remaining blocks. Commit scoped files only, then CI on that integrated commit before downstream promotion.

## Rollback
Keep original journal immutable or backed up; new recovery metadata additive. If reader cannot understand uncertainty state, fail closed and retain data.
