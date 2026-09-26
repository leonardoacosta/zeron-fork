# CI admission and exact-commit promotion gate

## Boundary
A bounded hosted gate reuses existing workflows. It adds no product API or generic state engine. Local structural validation cannot enforce hosted branch protection.

## Existing surfaces and file responsibilities
- `.github/workflows/ui-tests.yml`: UI/platform checks (`rust-quality`, `session-sync-regressions`, `ui-tests`, `macos-frame-recovery`, conditional `ios-tests`, `linux-browser`).
- `.github/workflows/preview-tests.yml`: preview checks (`networking` matrix, `coordinator`).
- `.github/workflows/windows.yml`: Windows `tests`; manual-only `native-gui` is not required.
- `Cargo.toml`: workspace and locked Rust test configuration anchor; no product-code edit.
- `openspec/README.md`: OpenSpec conventions anchor; no edit.

Use distinct `ui-promotion`, `preview-promotion`, and `windows-promotion` summary jobs in their existing workflows, with `if: always()`, `needs` for every required job, and a check that every `needs.*.result == success`. Remove `paths:` only from each `pull_request` trigger so branch protection always sees its summary, including docs-only PRs. Keep push filters and existing test jobs. This checks the integrated PR merge revision within the same workflow run and avoids polling/API integrations. Make `ios-tests` unconditional so a skipped required job cannot silently pass. Require Preview's matrix job as a whole, meaning each matrix leg must succeed. Never include manual-only `native-gui`.

The target branch must require each workflow's summary context, distinguished by workflow name if needed. A base/head update must invalidate old checks through normal GitHub PR check semantics. Verify this on hosted GitHub before declaring enforcement complete. Without admin-configured branch protection and a failing disposable PR proof, hosted enforcement is blocked.

## Exact proposed snippet

UI job appended under `jobs:`:

```yaml
  ui-promotion:
    if: always()
    needs:
      - rust-quality
      - session-sync-regressions
      - ui-tests
      - macos-frame-recovery
      - ios-tests
      - linux-browser
    runs-on: ubuntu-24.04
    steps:
      - name: Require every CI job
        env:
          RESULTS: ${{ toJSON(needs) }}
        run: |
          python3 -c 'import json,sys; results=json.loads(sys.argv[1]); failed=[name for name,job in results.items() if job["result"] != "success"]; print("non-success jobs:", failed); sys.exit(bool(failed))' "$RESULTS"
```

Preview uses `needs: [networking, coordinator]`; Windows uses `needs: [tests]`. Use `runs-on: ubuntu-latest` for those two. Keep existing `permissions: contents: read`. Remove only `pull_request.paths` in all three workflows.

## Scenarios
- C01: Given two independently green changes with conflicting combined behavior, when integrated CI fails, then neither combined round nor its dependents promote.
- C02: Given CI success for commit A, when source/config/lockfile changes to B, then A evidence cannot promote B.
- C03: Given a filter selects zero tests or an ignored external test never runs, then it is not coverage.
- C04: Given native platform/auth credentials are unavailable, record blocked evidence and hold the affected acceptance, without disabling a job to manufacture green.

## Acceptance boundary
A stdlib source test guards exact structure, but cannot demonstrate hosted merge blocking. Admin branch rules plus a failing disposable PR are separate required evidence. No push/spend/hosted setting change is part of this plan refinement.

Use the complete corrected YAML blocks in tasks.md as code authority. Summary steps explicitly use bash, including the Windows workflow whose defaults otherwise use pwsh. Require branches to be up to date before merge or use a separately designed merge-queue gate; an old base merge result cannot promote a new integrated tree.

## Refined handoff validation
Exact three YAML summary predicates extracted from tasks.md passed15 positive/empty/skipped/failed/cancelled controls. Proposed stdlib test ran red against unchanged workflow copies and green (8 tests) after appending the proposed summaries in scratch only. This is synthetic proposal validation, not hosted CI or branch protection. No workflow file was modified.
