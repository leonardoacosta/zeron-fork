# Verified provider adapters and authority preservation execution contract

**Goal:** Instantiate one child adapter change per researched concrete provider and action set before implementation.
**Architecture:** Existing Rust engine/proto/RPC/profile storage and native clients are the starting point. Freeze interfaces from observed source; no speculative provider API or generic framework.
**Tech stack:** Rust/Tokio/Serde/SQLite; GPUI/Swift/Worker TypeScript only if the approved surface requires them.
**Status:** executable discovery/refinement steps; product implementation NOT READY.
**Dependencies:** `integration-harness-observer-research`, `integration-github-ado-research`, `profile-access-enforcement`, `harness-preflight-binding`, `confirmed-stop-handoff`. Only exact prerequisite promotion admits implementation.

## D1. Recover authority and source (one bounded read per listed anchor)
**Files:** design.md and tasks.md in this change; read-only source anchors in design.md.
- [ ] Read PRD clauses ZF-19, ZF-15 and every C-scenario in `specs/integration-provider-adapters/spec.md`; state excluded sibling behavior in design.md.
- [ ] From repository root, verify listed anchors exist:
```bash
python3 - <<'PY'
from pathlib import Path
paths = ['crates/harness/src/lib.rs', 'crates/engine/src/registry.rs', 'crates/mcp/src/tools.rs', 'crates/engine/src/source_control.rs', 'crates/engine/src/rpc.rs']
for name in paths:
    p = Path(name)
    assert p.is_file(), name
    print(name, len(p.read_text().splitlines()), "lines")
PY
```
Expected: one line per anchor, exit0. Missing path means re-discover with graft and correct this contract; do not create a dummy file. Read `graft/INDEX.md` then matching cards. Use `graft ask "Verified provider adapters and authority preservation" --source` only if the CLI is already available; graph files are sufficient.
- [ ] In design.md, cite exact symbols/current line spans for the input, authority, persistence and side-effect paths. For each C-scenario record whether current behavior is observed, contradicted or not yet tested. Do not equate missing grep hit with absence proof.

## D2. Execute bounded adapter fan-out, not a generic implementation
This unit produces provider-specific change contracts. It cannot implement an unknown provider from a generic trait. Its output is an updated canonical dependency graph and one bounded child proposal per selected verified action set.

- [ ] Read the completed research evidence rows in `integration-harness-observer-research/design.md` and `integration-github-ado-research/design.md`. For every selected subject record exact publisher identity, version, canonical API source, allowed read/write actions, authentication reference, native ID/status/stop semantics, isolation capability, usage limitations and external authority owner. Do not copy a `verified local_source` row as provider runtime proof.
- [ ] Reject child admission when identity/API/version is unknown, required stop/isolation unsupported, or scope/account authorization absent. Record a blocked row with one exact missing prerequisite in this tasks.md. Continue independently verified subjects rather than marking all providers ready.
- [ ] For each admitted subject choose slug `adapter-<verified-provider>-<bounded-action-set>`. Before creating files, search existing changes for the same provider/action to avoid duplicates. A single child may not cover unrelated engineering harness + observer + browser services.
- [ ] Create the four canonical artifacts under that slug. Proposal must list exact selected actions and non-actions; spec must include unauthorized principal, unavailable provider, stale version, lost receipt and partial-effect scenarios; design must cite actual API/version and existing engine authorizer/preflight/stop/effect boundaries; tasks must contain complete request/response fixture bytes from verified public contract, exact tests, minimal implementation source and native acceptance commands. No guessed SDK method names or example tokens.
- [ ] Extend `prd-execution-map/units.json` with that child and exact hard prerequisites. Add the child as dependency of every consumer that requires its capability. Preserve blocked/unselected subjects as blocked, not fake successful children. Run the plan validator and explicitly inspect semantic acceptance dependencies, not just acyclic metadata.
- [ ] Cold executor must run the child's fixture/contract tests without inventing a field. Independently review mutation scope and native evidence. Only then request named child implementation approval. This fan-out unit's completion does not imply any provider adapter is implemented.

### Required child evidence record (in the child design.md, not a second ledger)
| Field | Required value source |
|---|---|
| provider_identity / version | exact official source or authorized installed version observation |
| actions / non_actions | approved bounded scope, no implied blanket permissions |
| native_identity / stop_proof | verified protocol and observed capability, unknown explicitly held |
| work_profile / account_reference | owning engine policy context, no credentials |
| input_output_contract | complete DTO/wire samples with public-source citation and redaction |
| reconciliation | known method to resolve uncertain effect or explicit hold behavior |
| unit_tests / native_acceptance | exact paths/commands/assertions and required authorized environment |
| downstream_consumers | exact unit slugs waiting on this capability |

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
- C01: Adapter returns unsupported for missing stop/isolation instead of claiming a generic interface makes it safe.
- C02: External planning/review status changes: preserve source provenance and never overwrite from local completion.
- C03: Provider upgrade changes contract: capability evidence invalidated and affected launches held.

## CI phase after every implementation iteration
- [ ] Run exact refined feature tests and core/affected-platform CI from `../prd-execution-map/design.md`. Verify at least one test actually selected; preserve failing evidence. No next iteration/round promotion while required checks fail or are missing.
- [ ] Run real acceptance: One real harmless authorized workflow per selected adapter and failure/unknown capability checks. Unselected providers remain blocked, not marked complete.
- [ ] Update this tasks.md with exact tested commit/tree, commands, counts, exit codes, evidence class, native environment and remaining blocks. Commit scoped files only, then CI on that integrated commit before downstream promotion.

## Rollback
Per-provider disable switch and native state/effect reconciliation before removal. Preserve other adapters and direct sessions.
