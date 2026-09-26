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
"""Check exact summary structure and execute the workflow's actual gate command.
Supported subset intentionally matches generated summary blocks; actionlint checks YAML.
"""
import json
import os
from pathlib import Path
import re
import subprocess
import unittest

CASES = {
    'ui-tests.yml': ('ui-promotion', ['rust-quality', 'session-sync-regressions', 'ui-tests', 'macos-frame-recovery', 'ios-tests', 'linux-browser']),
    'preview-tests.yml': ('preview-promotion', ['networking', 'coordinator']),
    'windows.yml': ('windows-promotion', ['tests']),
}

def summary(text, name):
    match = re.search(r'^  ' + re.escape(name) + r':\n(.*?)(?=^  [\w-]+:|\Z)', text, re.M | re.S)
    if not match:
        raise ValueError('missing executable summary: ' + name)
    return match.group(1)

def inspect(text, name, required):
    block = summary(text, name)
    if '    if: always()\n' not in block:
        raise ValueError('summary must run after failure')
    trigger = re.search(r'^  pull_request:\s*\n(.*?)(?=^  [\w-]+:|^permissions:|\Z)', text, re.M | re.S)
    if not trigger or re.search(r'^    (paths|paths-ignore|branches|branches-ignore):', trigger.group(1), re.M):
        raise ValueError('PR trigger is absent or filtered')
    needs = re.search(r'^    needs:([^\n]*)\n((?:      - [^\n]+\n)*)', block, re.M)
    if not needs:
        raise ValueError('missing needs')
    actual = re.findall(r'[\w-]+', needs.group(1)) or re.findall(r'^      - ([\w-]+)$', needs.group(2), re.M)
    if set(actual) != set(required) or len(actual) != len(required):
        raise ValueError('needs differs from required jobs')
    if '        shell: bash\n' not in block:
        raise ValueError('explicit bash required')
    if '          RESULTS: ${{ toJSON(needs) }}\n' not in block:
        raise ValueError('results not bound to native needs')
    configured = re.search(r'^          REQUIRED: (.+)$', block, re.M)
    if not configured or configured.group(1).split(',') != required:
        raise ValueError('required list mismatch')
    if 'continue-on-error' in block:
        raise ValueError('fail-open step')
    command = re.search(r'^        run: \|\n          (python3 -c .+)\n?$', block.rstrip() + '\n', re.M)
    if not command:
        raise ValueError('unsupported summary command shape')
    return command.group(1)

class PromotionGateTests(unittest.TestCase):
    def test_exact_summary_and_actual_predicate(self):
        for filename, (name, required) in CASES.items():
            with self.subTest(workflow=filename):
                text = (Path('.github/workflows') / filename).read_text()
                command = inspect(text, name, required)
                if filename == 'ui-tests.yml':
                    ios = summary(text, 'ios-tests')
                    self.assertNotRegex(ios, r'^    if:', 'iOS must not be skipped')
                good = {job: {'result': 'success'} for job in required}
                controls = [(good, 0), ({}, 1)]
                for job in required:
                    missing = dict(good); del missing[job]
                    controls.append((missing, 1))
                    for state in ['failure', 'cancelled', 'skipped', 'timed_out', None]:
                        controls.append(({**good, job: {'result': state}}, 1))
                for results, expected in controls:
                    env = dict(os.environ, RESULTS=json.dumps(results), REQUIRED=','.join(required))
                    result = subprocess.run(['bash', '-c', command], env=env, capture_output=True, text=True, timeout=5)
                    self.assertEqual(result.returncode, expected, (filename, results, result.stderr))
                # Structural mutants must fail before a command can be accepted.
                mutants = [text.replace('  '+name+':', '  removed-summary:', 1),
                           text.replace('  '+name+':\n    if: always()', '  '+name+':\n    if: success()', 1),
                           text.replace('          RESULTS: ${{ toJSON(needs) }}', '          RESULTS: "{}"', 1)]
                for mutant in mutants:
                    with self.assertRaises(ValueError):
                        inspect(mutant, name, required)

if __name__ == '__main__':
    unittest.main()
```

The test parses the deliberately narrow summary shape and executes the actual workflow command for every required job under success, missing, skipped, failed, cancelled and unknown outcomes. Structural mutations target the summary itself. Installed actionlint validates complete YAML separately. Neither check establishes hosted enforcement.

## Red/green and hosted verification

```bash
python3 openspec/changes/ci-promotion-gates/tests/test_promotion_gate.py
# Before workflow edits: expected red due to absent summary jobs.
python3 openspec/changes/ci-promotion-gates/tests/test_promotion_gate.py
# After workflow edits: expected one parameterized test passing all three workflows and their negative controls.
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

## Exact workflow validation
After applying the edits, run `actionlint -shellcheck= -pyflakes= .github/workflows/ui-tests.yml .github/workflows/preview-tests.yml .github/workflows/windows.yml` with an already installed actionlint. Expected exit0; absent validator is a named tooling prerequisite, not permission to claim syntax passed. Require up-to-date branch/merge checks so an old base cannot reuse earlier integrated-tree evidence.
