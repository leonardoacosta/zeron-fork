# CI admission and exact-commit promotion gate

## Boundary
A bounded hosted gate reuses existing workflows. It adds no product API or generic state engine. Local structural validation cannot enforce hosted branch protection.

## Existing surfaces and file responsibilities
- `.github/workflows/ui-tests.yml`: UI/platform checks (`rust-quality`, `session-sync-regressions`, `ui-tests`, `macos-frame-recovery`, conditional `ios-tests`, `linux-browser`).
- `.github/workflows/preview-tests.yml`: preview checks (`networking` matrix, `coordinator`).
- `.github/workflows/windows.yml`: Windows `tests`; manual-only `native-gui` is not required.
- `Cargo.toml`: workspace and locked Rust test configuration anchor; no product-code edit.
- `openspec/README.md`: OpenSpec conventions anchor; no edit.
- Optional only if explicitly retained at named approval: `openspec/changes/ci-promotion-gates/verify_round.py`, an untrusted local consistency helper. It is not part of hosted workflow enforcement and cannot authorize promotion.

Use distinct `ui-promotion`, `preview-promotion`, and `windows-promotion` summary jobs in their existing workflows, with `if: always()`, `needs` for every required job, and a check that every `needs.*.result == success`. Remove `paths:` only from each `pull_request` trigger so branch protection always sees its summary, including docs-only PRs. Keep push filters and existing test jobs. This checks the integrated PR merge revision within the same workflow run and avoids polling/API integrations. Make `ios-tests` unconditional so a skipped required job cannot silently pass. Require Preview's matrix job as a whole, meaning each matrix leg must succeed. Never include manual-only `native-gui`.

The target branch must require each workflow's summary context, distinguished by workflow name if needed. A base/head update must invalidate old checks through normal GitHub PR check semantics. Verify this on hosted GitHub before declaring enforcement complete. Without admin-configured branch protection and a failing disposable PR proof, hosted enforcement is blocked.

## Single code authority
The complete YAML and test source live only in tasks.md. Do not copy an earlier design snippet or a predicate that iterates only present jobs: an empty/missing needs object must fail. The exact tasks require all named jobs, bash explicitly, and a native dependency result of success. The design defines semantics, not duplicate executable code.

## Scenarios
- C01: Given two independently green changes with conflicting combined behavior, when integrated CI fails, then neither combined round nor its dependents promote.
- C02: Given CI success for commit A, when source/config/lockfile changes to B, then A evidence cannot promote B.
- C03: Given a filter selects zero tests or an ignored external test never runs, then it is not coverage.
- C04: Given native platform/auth credentials are unavailable, record blocked evidence and hold the affected acceptance, without disabling a job to manufacture green.

## Acceptance boundary
The canonical scope covers the three workflow summaries and `tests/test_promotion_gate.py`. The round-evidence checker is optional local review tooling and only in scope if explicitly retained at named implementation approval; it is never a merge/deploy authority source. If deferred, no helper file or self-test is required. A local helper self-test cannot prove hosted enforcement.

Use the complete corrected YAML blocks in tasks.md as code authority. Summary steps explicitly use bash, including the Windows workflow whose defaults otherwise use pwsh. Require branches to be up to date before merge or use a separately designed merge-queue gate; an old base merge result cannot promote a new integrated tree.

## Refined handoff validation
Exact three YAML summary predicates extracted from tasks.md passed15 positive/empty/skipped/failed/cancelled controls. Proposed stdlib test ran red against unchanged workflow copies and green (8 tests) after appending the proposed summaries in scratch only. This is synthetic proposal validation, not hosted CI or branch protection. No workflow file was modified.

## Current handoff validation21:12UTC
Supersedes historical8-test substring checks: actual summary commands executed against full scratch workflow copies; installed actionlint passed. Exact structural extraction rejects missing needs, PR path filters and conditional iOS after multiline assertion correction. Round consistency checker12 tests passes but is explicitly untrusted and only eligible_for_review. Required hosted ruleset proof remains an external acceptance task, not a reason to invent local success.

## Implementation status (2026-09-29)
Implemented locally at commit `1631379`: the three summary jobs exist with `if: always()` and exact `needs`, `paths:` is gone from each `pull_request` trigger, and `ios-tests` is unconditional. Evidence and the open blockers are in tasks.md. The "no workflow file was modified" line above describes the earlier synthetic validation round, not the current state. `verify_round.py` was not retained, so its round-consistency self-test did not run against the final revision. Hosted enforcement remains blocked: the active `Protect main` ruleset requires no status contexts, and this account has pull-only access to `zeronsh/zeron`. `rust-quality` is a fork-local check (`1427da6`, absent from `origin/main`), and it currently fails on 125 workspace clippy errors, so `ui-promotion` cannot go green until that lint debt is settled; the wired gates block nothing until an administrator requires the contexts.
