# Exact-commit CI promotion gate plan

**Goal:** Add fail-closed required summaries to the existing UI, Preview, and Windows workflows.
**Scope:** Implementation would change only `.github/workflows/ui-tests.yml`, `.github/workflows/preview-tests.yml`, `.github/workflows/windows.yml`, plus `openspec/changes/ci-promotion-gates/tests/test_promotion_gate.py`. No product code or new workflow. No workflow implementation occurred in this planning task.
**Readiness:** exact implementation proposal, pending named approval; hosted promotion acceptance remains blocked until configured and observed. The snippets and stdlib predicate are executable, but hosted branch-rule setup and a disposable failing-PR proof remain outstanding. An administrator must require all three summary contexts and verify failure blocks merge. Local structural tests are not hosted enforcement.

## Existing checks to reuse

- `.github/workflows/ui-tests.yml`: `rust-quality`, `session-sync-regressions`, `ui-tests`, `macos-frame-recovery`, conditional `ios-tests`, `linux-browser`.
- `.github/workflows/preview-tests.yml`: `networking` matrix and `coordinator`.
- `.github/workflows/windows.yml`: `tests`; `native-gui` is manual and out of scope.
- `Cargo.toml` and `openspec/README.md` are read-only anchors.

In each workflow remove `paths:` only from the `pull_request` trigger, so the summary appears for docs-only PRs. Keep push filters and all existing test commands. Add the distinct stable `ui-promotion`, `preview-promotion`, or `windows-promotion` job with `if: always()`, `needs` for every required job, and the complete job below. Require each workflow-specific summary context in branch protection, distinguishing by workflow name if necessary. Each summary runs in the same workflow run as its tests. The PR run tests GitHub's merge revision. `needs.networking.result` represents the matrix as a whole and succeeds only when both matrix legs pass. Make existing conditional `ios-tests` unconditional so skip cannot silently count as success. Do not include Windows `native-gui`.

## Exact summary jobs

UI, appended under `jobs:`:

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
      - name: Require every UI check
        env:
          RESULTS: ${{ toJSON(needs) }}
          REQUIRED: rust-quality,session-sync-regressions,ui-tests,macos-frame-recovery,ios-tests,linux-browser
        shell: bash
        run: |
          python3 -c 'import json,os,sys; results=json.loads(os.environ["RESULTS"]); required=os.environ["REQUIRED"].split(","); failed=[name for name in required if name not in results or results[name].get("result") != "success"]; print("missing or non-success required jobs:", failed); sys.exit(bool(failed))'
```

Preview, appended under `jobs:`:

```yaml
  preview-promotion:
    if: always()
    needs: [networking, coordinator]
    runs-on: ubuntu-latest
    steps:
      - name: Require every Preview check
        env:
          RESULTS: ${{ toJSON(needs) }}
          REQUIRED: networking,coordinator
        shell: bash
        run: |
          python3 -c 'import json,os,sys; results=json.loads(os.environ["RESULTS"]); required=os.environ["REQUIRED"].split(","); failed=[name for name in required if name not in results or results[name].get("result") != "success"]; print("missing or non-success required jobs:", failed); sys.exit(bool(failed))'
```

Windows, appended under `jobs:`:

```yaml
  windows-promotion:
    if: always()
    needs: [tests]
    runs-on: ubuntu-latest
    steps:
      - name: Require Windows check
        env:
          RESULTS: ${{ toJSON(needs) }}
          REQUIRED: tests
        shell: bash
        run: |
          python3 -c 'import json,os,sys; results=json.loads(os.environ["RESULTS"]); required=os.environ["REQUIRED"].split(","); failed=[name for name in required if name not in results or results[name].get("result") != "success"]; print("missing or non-success required jobs:", failed); sys.exit(bool(failed))'
```

The predicate fails missing jobs and every result other than `success`, including skipped, cancelled, or failed. It needs only GitHub Actions `needs` and hosted-runner Python. Do not add `continue-on-error`.

## Test-first implementation

Create `openspec/changes/ci-promotion-gates/tests/test_promotion_gate.py` and run before workflow edits:

```bash
python3 openspec/changes/ci-promotion-gates/tests/test_promotion_gate.py
```

Expected red: the summary job structure is absent. Exact stdlib test source:

```python
import unittest
from pathlib import Path


def failed_required(results, required):
    return [name for name in required
            if name not in results or results[name].get("result") != "success"]


class PromotionGateTests(unittest.TestCase):
    def test_all_required_jobs_success(self):
        required = ["tests", "networking"]
        self.assertEqual(failed_required({name: {"result": "success"} for name in required}, required), [])

    def test_missing_job_fails(self):
        self.assertEqual(failed_required({"tests": {"result": "success"}}, ["tests", "networking"]), ["networking"])

    def test_empty_results_fails(self):
        self.assertEqual(failed_required({}, ["tests", "networking"]), ["tests", "networking"])

    def test_skipped_job_fails(self):
        self.assertEqual(failed_required({"tests": {"result": "skipped"}}, ["tests"]), ["tests"])

    def test_failed_job_fails(self):
        self.assertEqual(failed_required({"tests": {"result": "failure"}}, ["tests"]), ["tests"])

    def test_cancelled_job_fails(self):
        self.assertEqual(failed_required({"tests": {"result": "cancelled"}}, ["tests"]), ["tests"])

    def test_missing_result_fails(self):
        self.assertEqual(failed_required({"tests": {}}, ["tests"]), ["tests"])

    def test_workflow_summaries_cover_required_jobs(self):
        cases = {
            ".github/workflows/ui-tests.yml": ["rust-quality", "session-sync-regressions", "ui-tests", "macos-frame-recovery", "ios-tests", "linux-browser"],
            ".github/workflows/preview-tests.yml": ["networking", "coordinator"],
            ".github/workflows/windows.yml": ["tests"],
        }
        for path, required in cases.items():
            with self.subTest(path=path):
                text = Path(path).read_text(encoding="utf-8")
                summary = {".github/workflows/ui-tests.yml": "ui-promotion", ".github/workflows/preview-tests.yml": "preview-promotion", ".github/workflows/windows.yml": "windows-promotion"}[path]
                self.assertIn(summary + ":", text)
                self.assertIn("if: always()", text)
                for job in required:
                    self.assertIn(job, text)
                self.assertIn('!= "success"', text)
                self.assertNotIn("continue-on-error", text)


if __name__ == "__main__":
    unittest.main()
```

The seven predicate tests exercise success, empty/missing, skipped, failed, cancelled, and missing-result cases. The workflow test checks expected summary fragments only and is not hosted-enforcement evidence.

## Red/green and hosted verification

```bash
python3 openspec/changes/ci-promotion-gates/tests/test_promotion_gate.py
# Before workflow edits: expected red due to absent summary jobs.
python3 openspec/changes/ci-promotion-gates/tests/test_promotion_gate.py
# After workflow edits: expected eight passing tests.
git diff --check
```

After workflow edits, validate YAML with an already-installed validator if available. Inspect that each `needs` references real job IDs, UI iOS runs unconditionally, Preview matrix job remains intact, and each `pull_request` trigger has no `paths:` filter. Do not add dependencies for validation.

Hosted acceptance is separate: an administrator requires the three `ui-promotion`, `preview-promotion`, and `windows-promotion` contexts on the target branch, verifies they appear on a docs-only PR, then observes a required-job failure make its summary red and block merge. Record workflow contexts and PR head/base SHAs. Until this evidence exists, report hosted promotion blocked. No hosted settings changes, push, or spend during this refinement.

## Scenarios
- C01: Given two independently green changes with conflicting combined behavior, when integrated CI fails, then neither combined round nor its dependents promote.
- C02: Given CI success for commit A, when source/config/lockfile changes to B, then A evidence cannot promote B.
- C03: Given a filter selects zero tests or an ignored external test never runs, then it is not coverage.
- C04: Given native platform/auth credentials are unavailable, record blocked evidence and hold the affected acceptance, without disabling a job to manufacture green.

## CI phase after every implementation iteration
- [ ] Run the test red before workflow changes and green after; record commands and results.
- [ ] Confirm all needed job IDs, matrix behavior, unconditional PR runs, and no degraded test steps.
- [ ] Validate workflow YAML if an installed parser exists; run `git diff --check`.
- [ ] Record hosted branch-rule and failing-PR evidence separately. Without it, hosted enforcement remains blocked.
- [ ] Commit only the three workflows and test file after implementation approval.

## Rollback
Revert the three workflow changes. Do not relax branch protection automatically. A missing required context should block merging until an administrator deliberately revises policy.
