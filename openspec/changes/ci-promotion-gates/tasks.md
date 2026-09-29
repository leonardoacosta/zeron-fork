# Exact-commit CI promotion gate plan

**Goal:** Add fail-closed required summaries to the existing UI, Preview, and Windows workflows.
**Scope:** Workflow implementation changes only `.github/workflows/ui-tests.yml`, `.github/workflows/preview-tests.yml`, `.github/workflows/windows.yml`, plus `openspec/changes/ci-promotion-gates/tests/test_promotion_gate.py`. A read-only evidence record from the hosted API check was added alongside as `tests/main-protection-api-evidence.md`; it changes no behavior and no authority. The round-evidence consistency checker below is a separately bounded local helper in this same change, not a workflow or hosted gate. If retained, it additionally creates `openspec/changes/ci-promotion-gates/verify_round.py`; it is untrusted review support only and never changes promotion authority. It was NOT retained. No product code or new workflow.
**Readiness:** implemented locally at commit `1631379` (three workflow summaries plus `tests/test_promotion_gate.py`); red/green, structural test, and actionlint evidence are recorded below. Hosted promotion acceptance remains blocked: the active `Protect main` ruleset has no required status-check contexts and this account has pull-only access to `zeronsh/zeron`. The pre-implementation baseline also failed `rust-quality` on two pre-existing product lints, recorded as bounded repair tasks R1/R2 below. Local structural tests are not hosted enforcement.

## Pre-implementation baseline check
Run the required existing commands before changing workflow files:
```bash
cargo fmt --all -- --check
cargo clippy --workspace --all-targets --all-features -- -D warnings
```
Record exact HEAD/tree and output. If they fail, classify missing system toolchain/dependency versus source defect and create a bounded repair task in this same change before promotion. Never lower lint severity or claim another agent's uncommitted repair is the tested commit. Concurrent quality work may change baseline; re-read current workflow and run checks on the actual integrated revision. This step does not authorize broad formatting unrelated user edits.

### Recorded baseline result (2026-09-29, HEAD 7bcaf6a, clean tree)

- `cargo fmt --all -- --check` -> PASS (exit 0, no output).
- `cargo clippy --workspace --all-targets --all-features -- -D warnings` -> FAIL (exit 101), two pre-existing source lints:
  - `crates/doc/src/commands.rs:39` `clippy::large_enum_variant` on `SessionCommandPayload`.
  - `crates/harness/src/opencode/mod.rs:2310` `clippy::too_many_arguments` on `async fn post_prompt` (10/7).

Classification: source defect in product code, not a missing dependency. Both constructs are byte-identical in `origin/main`, so neither was introduced by this branch. Rust toolchain here is system 1.98.1 stable (clippy 0.1.98); the repo pins `channel = "stable"` and no `rustup` is installed locally, so version-dependent lint drift is possible but unproven.

Consequence: `rust-quality` is a required `ui-promotion` check, so round 0 cannot promote until these two lints are repaired. The repairs edit product code (DTO boxing, signature refactor), which is outside this change's "no product code" boundary, so they are recorded below as bounded repair tasks and were NOT executed here.

#### Bounded repair tasks (not executed; each needs its own approval)

- R1: fix `clippy::large_enum_variant` in `crates/doc/src/commands.rs` by boxing `RunRequest` (or an equivalent indirection), re-running the affected crate tests plus `cargo clippy --workspace --all-targets --all-features -- -D warnings`.
- R2: fix `clippy::too_many_arguments` in `crates/harness/src/opencode/mod.rs::post_prompt` by grouping the 10 parameters, re-running the harness tests plus the workspace clippy gate.

## Existing checks to reuse

- `.github/workflows/ui-tests.yml`: `rust-quality`, `session-sync-regressions`, `ui-tests`, `macos-frame-recovery`, conditional `ios-tests`, `linux-browser`.
- `.github/workflows/preview-tests.yml`: `networking` matrix and `coordinator`.
- `.github/workflows/windows.yml`: `tests`; `native-gui` is manual and out of scope.
- `Cargo.toml` and `openspec/README.md` are read-only anchors.

In each workflow remove `paths:` only from the `pull_request` trigger, so the summary appears for docs-only PRs. Keep push filters and all existing test commands. Add the distinct stable `ui-promotion`, `preview-promotion`, or `windows-promotion` job with `if: always()`, `needs` for every required job, and the complete job below. Require each workflow-specific summary context in branch protection, distinguishing by workflow name if necessary. Each summary runs in the same workflow run as its tests. The PR run tests GitHub's merge revision. `needs.networking.result` represents the matrix as a whole and succeeds only when both matrix legs pass. Make existing conditional `ios-tests` unconditional so skip cannot silently count as success. Do not include Windows `native-gui`.

## Exact trigger edits before adding summaries
For `.github/workflows/ui-tests.yml`, `.github/workflows/preview-tests.yml`, and `.github/workflows/windows.yml`, replace the entire `pull_request` mapping (including only its nested path filters) with this same mapping. Leave the following `push` and `workflow_dispatch` siblings byte-for-byte unchanged:
```yaml
  pull_request:
```
For `.github/workflows/ui-tests.yml` only, remove exactly this existing line from the `ios-tests` job, retaining its `needs: changes` and all steps:
```yaml
    if: needs.changes.outputs.ios == 'true'
```
If the exact job/trigger anchors differ from inspected baseline, stop and refresh the patch. Do not globally delete every `paths` or `if` key. These edits deliberately run all required PR jobs; no docs-only skip can strand a required summary.

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
                    self.assertNotRegex(ios, r'(?m)^    if:', 'iOS must not be skipped')
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
- [x] Run the test red before workflow changes and green after; record commands and results. RED at HEAD 7bcaf6a: `python3 openspec/changes/ci-promotion-gates/tests/test_promotion_gate.py` exited 1, three errors (missing `ui-promotion`, `preview-promotion`, `windows-promotion`). GREEN after the edits: same command exited 0, `Ran 1 test ... OK`.
- [x] Confirm all needed job IDs, matrix behavior, unconditional PR runs, and no degraded test steps. Verified independently: `needs` sets equal the required sets exactly (ui: rust-quality, session-sync-regressions, ui-tests, macos-frame-recovery, ios-tests, linux-browser; preview: networking, coordinator; windows: tests); `ios-tests` runs unconditionally and keeps `needs: changes`; `needs.networking` covers the whole matrix; Windows `native-gui` is never a dependency; no existing test step changed.
- [x] Run actionlint and structural tests for the three workflows; independently note whether the optional `verify_round.py` was retained and, only if retained, run its self-test. `actionlint v1.7.12` exited 0 on all three workflows; `python3 .../test_promotion_gate.py` exited 0. `verify_round.py` was NOT retained, so its self-test was not run.
- [ ] Record hosted branch-rule and failing-PR evidence separately. Without it, hosted enforcement remains BLOCKED. Read-only API evidence (2026-09-29, `gh` as `leonardoacosta`) is in `tests/main-protection-api-evidence.md`: `main` is protected and ruleset `20150191` "Protect main" is active, but its rules are only `deletion`, `non_fast_forward`, `pull_request`, so NO required status-check contexts are configured, and this account has `pull`-only permission (`admin: false, push: false`) on `zeronsh/zeron`, with no writable fork remote. Required-context configuration and a failing-PR observation therefore cannot be produced here.
- [x] Commit only the three workflows, `test_promotion_gate.py`, and (if retained) `verify_round.py` after implementation approval. Do not include unrelated files or hosted configuration. Committed as `1631379` with exactly `.github/workflows/{ui-tests,preview-tests,windows}.yml` and `openspec/changes/ci-promotion-gates/tests/test_promotion_gate.py`; no `verify_round.py`, no hosted configuration, no unrelated file.

## Rollback
Revert the three workflow changes. Do not relax branch protection automatically. A missing required context should block merging until an administrator deliberately revises policy.

## Exact workflow validation
After applying the edits, run `actionlint -shellcheck= -pyflakes= .github/workflows/ui-tests.yml .github/workflows/preview-tests.yml .github/workflows/windows.yml` with an already installed actionlint. Expected exit0; absent validator is a named tooling prerequisite, not permission to claim syntax passed. Require up-to-date branch/merge checks so an old base cannot reuse earlier integrated-tree evidence.

## Round evidence consistency check (never an authority source)
**Proposed create:** `openspec/changes/ci-promotion-gates/verify_round.py`. This belongs to the canonical CI change, not a second task lifecycle. Inputs are a reviewed round manifest and CI-observation record retained as evidence attachments to tasks.md. Success means eligible_for_review only. No signature service, new secret or automatic merge/deploy consumer is introduced.

This checker is optional review tooling, separate from the three required workflow summaries and `test_promotion_gate.py`. During named implementation approval, explicitly retain or defer it. If deferred, skip this entire section and do not create its file; workflow summary implementation/acceptance remains independently scoped. If retained, include its file in the approved file list and use the steps below only after the workflow work. It cannot satisfy or replace hosted branch-rule/failing-PR acceptance.

- [ ] N/A (helper not retained): Create exact code below and run `python3 openspec/changes/ci-promotion-gates/verify_round.py --self-test`; require12 tests. Every failed required test blocks; evidence cannot change a manifest's test unit into research. Ignored tests must be predeclared non-required with separate coverage references; no waiver of required behavior.
```python
#!/usr/bin/env python3
"""Untrusted consistency checker for an integrated-round evidence manifest.

This tool only checks internal consistency of supplied JSON and emits
"eligible_for_review". It cannot establish that run IDs, job conclusions, test
counts, URLs, or artifact digests are true. A reviewer must independently verify
provenance against native CI records before using this output.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

SHA_RE = re.compile(r"^[0-9a-f]{40}$")
DIGEST_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
SCHEMA_VERSION = 1


class EvidenceError(ValueError):
    pass


def _fail(message: str) -> None:
    raise EvidenceError(message)


def verify(manifest: dict[str, Any], record: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(record, dict):
        _fail("evidence must be an object")

    if manifest.get("schema_version") != SCHEMA_VERSION:
        _fail("unsupported manifest schema")
    target_sha = manifest.get("integrated_sha")
    if not isinstance(target_sha, str) or not SHA_RE.fullmatch(target_sha):
        _fail("manifest integrated_sha must be a full lowercase commit SHA")
    if record.get("schema_version") != SCHEMA_VERSION:
        _fail("unsupported evidence schema")
    if record.get("integrated_sha") != target_sha:
        _fail("evidence commit is stale or does not match integrated SHA")
    if not isinstance(record.get("run_id"), str) or not record["run_id"].strip():
        _fail("missing CI run_id")
    provenance = record.get("producer_provenance")
    if not isinstance(provenance, str) or not provenance.strip():
        _fail("missing reviewer-verifiable producer provenance")
    if not isinstance(record.get("run_url"), str) or not record["run_url"].strip():
        _fail("missing native CI run URL")

    unit_specs = manifest.get("required_units")
    jobs = manifest.get("required_jobs")
    if not isinstance(unit_specs, list) or not unit_specs or not isinstance(jobs, list) or not jobs:
        _fail("manifest required_units and required_jobs must be non-empty lists")
    unit_ids = []
    for spec in unit_specs:
        if not isinstance(spec, dict) or not isinstance(spec.get("id"), str) or not spec["id"].strip():
            _fail("each required unit needs an id")
        if spec.get("check_kind") not in ("test", "research"):
            _fail(f"unit check_kind must be test or research: {spec.get('id')}")
        if not _unique_nonempty_strings(spec.get("allowed_ignored_test_ids", [])) and spec.get("allowed_ignored_test_ids", []) != []:
            _fail(f"invalid allowed ignored-test inventory: {spec.get('id')}")
        if "allowed_failed_test_ids" in spec:
            _fail(f"failed tests can never be waived: {spec.get('id')}")
        ignored_allowance = spec.get("allowed_ignored_test_ids", [])
        if not _unique_nonempty_strings(ignored_allowance) and ignored_allowance != []:
            _fail(f"invalid allowed ignored-test inventory: {spec.get('id')}")
        if ignored_allowance and not _unique_nonempty_strings(spec.get("ignored_coverage_refs")):
            _fail(f"ignored tests require separate coverage evidence: {spec.get('id')}")
        unit_ids.append(spec["id"])
    if len(set(unit_ids)) != len(unit_ids) or not _unique_nonempty_strings(jobs):
        _fail("manifest unit/job IDs must be unique non-empty strings")

    _verify_units(record.get("units"), unit_specs, target_sha)
    _verify_rows(record.get("jobs"), jobs, target_sha, "job")

    return {
        "decision": "eligible_for_review",
        "integrated_sha": target_sha,
        "run_id": record["run_id"],
        "unit_count": len(unit_specs),
        "job_count": len(jobs),
        "limitation": "untrusted consistency check only; reviewer must verify native CI provenance; not promotion",
    }


def _unique_nonempty_strings(value: Any) -> bool:
    return (isinstance(value, list) and bool(value)
            and all(isinstance(item, str) and item.strip() for item in value)
            and len(set(value)) == len(value))


def _index_rows(rows: Any, required: list[str], sha: str, kind: str) -> dict[str, dict[str, Any]]:
    if not isinstance(rows, list):
        _fail(f"missing {kind} evidence rows")
    by_id: dict[str, dict[str, Any]] = {}
    for row in rows:
        if not isinstance(row, dict):
            _fail(f"malformed {kind} evidence row")
        item_id = row.get("id")
        if not isinstance(item_id, str) or item_id in by_id:
            _fail(f"missing or duplicate {kind} id")
        by_id[item_id] = row
    for item_id in required:
        row = by_id.get(item_id)
        if row is None:
            _fail(f"missing required {kind}: {item_id}")
        allowed_statuses = {"success"} if kind != "unit" else {"success", "blocked"}
        if row.get("status") not in allowed_statuses:
            _fail(f"{kind} did not succeed: {item_id}")
        if row.get("tested_sha") != sha:
            _fail(f"stale {kind} evidence: {item_id}")
        if not isinstance(row.get("evidence_ref"), str) or not row["evidence_ref"].strip():
            _fail(f"missing evidence reference: {item_id}")
        if not isinstance(row.get("artifact_digest"), str) or not DIGEST_RE.fullmatch(row["artifact_digest"]):
            _fail(f"missing/invalid artifact digest: {item_id}")
    return by_id


def _count(row: dict[str, Any], field: str, item_id: str) -> int:
    value = row.get(field)
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        _fail(f"missing or invalid {field}: {item_id}")
    return value


def _verify_units(rows: Any, required: list[dict[str, Any]], sha: str) -> None:
    by_id = _index_rows(rows, [spec["id"] for spec in required], sha, "unit")
    for spec in required:
        item_id = spec["id"]
        row = by_id[item_id]
        kind = spec["check_kind"]
        if row.get("check_kind") != kind:
            _fail(f"evidence check_kind differs from manifest: {item_id}")
        if kind == "test":
            selected = _count(row, "selected_tests", item_id)
            passed = _count(row, "passed_tests", item_id)
            ignored = _count(row, "ignored_tests", item_id)
            failed = _count(row, "failed_tests", item_id)
            if failed != 0:
                _fail(f"failed tests always block promotion: {item_id}")
            if selected == 0 or passed != selected:
                _fail(f"zero, partial, or missing selected/passed test counts: {item_id}")
            _require_allowed_count_ids(row, "ignored_test_ids", ignored, spec.get("allowed_ignored_test_ids", []), item_id)
            if ignored and not _unique_nonempty_strings(spec.get("ignored_coverage_refs")):
                _fail(f"ignored tests lack manifest-listed separate coverage evidence: {item_id}")
        else:
            observations = row.get("observations_count")
            if not isinstance(observations, int) or isinstance(observations, bool) or observations <= 0:
                _fail(f"research unit requires at least one observation: {item_id}")
            if row.get("status") == "blocked":
                _fail(f"research unit is blocked: {item_id}")
            if row.get("check_kind") != "research":
                _fail(f"evidence check_kind differs from manifest: {item_id}")
            refs = row.get("observation_refs")
            if not isinstance(refs, list) or len(refs) != observations or not all(isinstance(x, str) and x.strip() for x in refs):
                _fail(f"research observation references missing or count mismatch: {item_id}")


def _require_allowed_count_ids(row: dict[str, Any], field: str, count: int, allowed: list[str], item_id: str) -> None:
    ids = row.get(field, [])
    if not isinstance(ids, list) or len(ids) != count or any(not isinstance(x, str) or not x.strip() for x in ids):
        _fail(f"{field} must enumerate each counted test: {item_id}")
    if len(set(ids)) != len(ids) or not set(ids).issubset(set(allowed)):
        _fail(f"unapproved {field}: {item_id}")
    if count and not allowed:
        _fail(f"nonzero {field} requires explicit non-required inventory: {item_id}")


def _verify_rows(rows: Any, required: list[str], sha: str, kind: str) -> None:
    _index_rows(rows, required, sha, kind)


def load_json(path: str) -> dict[str, Any]:
    try:
        value = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise EvidenceError(f"cannot read JSON input: {path}") from exc
    if not isinstance(value, dict):
        _fail(f"JSON input must be an object: {path}")
    return value


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("usage: verify_round.py MANIFEST.json EVIDENCE.json", file=sys.stderr)
        return 2
    try:
        result = verify(load_json(argv[1]), load_json(argv[2]))
    except EvidenceError as exc:
        print(f"BLOCKED: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0


def _self_test() -> None:
    import copy
    import unittest

    sha = "a" * 40
    manifest = {"schema_version": 1, "integrated_sha": sha,
                "required_units": [
                    {"id": "alpha", "check_kind": "test"},
                    {"id": "beta", "check_kind": "research"},
                ], "required_jobs": ["ui", "windows"]}

    def artifact(label: str) -> str:
        return "sha256:" + hashlib.sha256(label.encode()).hexdigest()

    def fresh_record() -> dict[str, Any]:
        return {
            "schema_version": 1, "producer_provenance": "reviewer must match native CI run/job records",
            "run_id": "run-123", "run_url": "https://ci.invalid/runs/run-123",
            "integrated_sha": sha,
            "units": [
                {"id": "alpha", "check_kind": "test", "status": "success", "tested_sha": sha,
                 "selected_tests": 3, "passed_tests": 3, "ignored_tests": 0, "failed_tests": 0,
                 "ignored_test_ids": [], "failed_test_ids": [],
                 "evidence_ref": "https://ci.invalid/run-123/alpha",
                 "artifact_digest": artifact("alpha")},
                {"id": "beta", "check_kind": "research", "status": "success", "tested_sha": sha,
                 "observations_count": 2,
                 "observation_refs": ["docs://official/source-a", "repo://source-span"],
                 "evidence_ref": "https://ci.invalid/run-123/beta",
                 "artifact_digest": artifact("beta")},
            ],
            "jobs": [
                {"id": job, "status": "success", "tested_sha": sha,
                 "evidence_ref": f"https://ci.invalid/run-123/{job}",
                 "artifact_digest": artifact(job)}
                for job in ["ui", "windows"]
            ],
        }


    class Tests(unittest.TestCase):
        def test_consistent_exact_sha_is_only_eligible_for_review(self):
            got = verify(manifest, fresh_record())
            self.assertEqual(got["decision"], "eligible_for_review")
            self.assertEqual((got["unit_count"], got["job_count"]), (2, 2))

        def test_missing_provenance_or_run_url_denies(self):
            for field in ("producer_provenance", "run_url"):
                record = fresh_record(); record[field] = ""
                with self.assertRaises(EvidenceError):
                    verify(manifest, record)

        def test_self_reported_success_is_not_authenticated(self):
            record = fresh_record()
            result = verify(manifest, record)
            self.assertEqual(result["decision"], "eligible_for_review")
            self.assertIn("untrusted consistency check only", result["limitation"])
            # Review, not this function, must establish the claimed provenance.

        def test_stale_round_sha_denies(self):
            record = fresh_record()
            record["integrated_sha"] = "b" * 40
            for rows in (record["units"], record["jobs"]):
                for row in rows:
                    row["tested_sha"] = "b" * 40
            with self.assertRaisesRegex(EvidenceError, "does not match"):
                verify(manifest, record)

        def test_missing_unit_or_job_denies(self):
            for field, target in (("units", "unit"), ("jobs", "job")):
                record = fresh_record()
                record[field].pop()
                with self.assertRaisesRegex(EvidenceError, f"missing required {target}"):
                    verify(manifest, record)

        def test_skipped_cancelled_and_failed_rows_deny(self):
            for state in ("skipped", "cancelled", "failure", "timed_out"):
                record = fresh_record()
                record["jobs"][0]["status"] = state
                with self.assertRaisesRegex(EvidenceError, "did not succeed"):
                    verify(manifest, record)

        def test_zero_missing_or_partial_tests_deny(self):
            mutations = (("selected_tests", 0), ("selected_tests", None), ("passed_tests", 2))
            for field, value in mutations:
                record = fresh_record(); record["units"][0][field] = value
                with self.assertRaises(EvidenceError): verify(manifest, record)

        def test_failed_tests_never_waive_and_check_kind_cannot_downgrade(self):
            record=fresh_record(); record["units"][0]["failed_tests"]=1; record["units"][0]["failed_test_ids"]=["test_x"]
            with self.assertRaisesRegex(EvidenceError, "failed tests always block"):
                verify(manifest, record)
            record=fresh_record(); record["units"][0]["check_kind"]="research"
            record["units"][0].update(observations_count=1, observation_refs=["repo://fake"])
            with self.assertRaisesRegex(EvidenceError, "check_kind differs"):
                verify(manifest, record)
            record=fresh_record(); record["units"][1]["check_kind"]="test"
            record["units"][1].update(selected_tests=1, passed_tests=1, ignored_tests=0, failed_tests=0)
            with self.assertRaisesRegex(EvidenceError, "check_kind differs"):
                verify(manifest, record)

        def test_ignored_tests_require_manifest_allowance_and_separate_coverage(self):
            record=fresh_record(); record["units"][0]["ignored_tests"]=1; record["units"][0]["ignored_test_ids"]=["test_non_required"]
            with self.assertRaisesRegex(EvidenceError, "unapproved"):
                verify(manifest, record)
            no_coverage={**manifest, "required_units":[{**manifest["required_units"][0],
                "allowed_ignored_test_ids":["test_non_required"]}, manifest["required_units"][1]]}
            with self.assertRaisesRegex(EvidenceError, "separate coverage"):
                verify(no_coverage, record)
            allowed={**manifest, "required_units":[{**manifest["required_units"][0],
                "allowed_ignored_test_ids":["test_non_required"],
                "ignored_coverage_refs":["unit_suite.coverage:cases-1-2"]}, manifest["required_units"][1]]}
            self.assertEqual(verify(allowed, record)["decision"], "eligible_for_review")
            no_failed_waiver={**manifest, "required_units":[{**manifest["required_units"][0], "allowed_failed_test_ids":["test_x"]}, manifest["required_units"][1]]}
            with self.assertRaisesRegex(EvidenceError, "never be waived"):
                verify(no_failed_waiver, fresh_record())

        def test_research_requires_observation_and_blocked_denies(self):
            for row in ({"status":"blocked","observations_count":0,"observation_refs":[]},
                        {"status":"success","observations_count":0,"observation_refs":[]},
                        {"status":"success","observations_count":2,"observation_refs":["one"]}):
                record=fresh_record(); record["units"][1].update(row)
                with self.assertRaises(EvidenceError): verify(manifest,record)

        def test_missing_refs_bad_digests_and_duplicate_ids_deny(self):
            for mutate, message in (
                (lambda r: r["units"][0].update(evidence_ref=""), "reference"),
                (lambda r: r["jobs"][0].update(artifact_digest="sha256:bad"), "digest"),
                (lambda r: r["jobs"].append(copy.deepcopy(r["jobs"][0])), "duplicate"),
            ):
                record = fresh_record(); mutate(record)
                with self.assertRaisesRegex(EvidenceError, message):
                    verify(manifest, record)

        def test_missing_expected_job_list_or_provenance_denies(self):
            bad_manifest = {**manifest, "required_jobs": []}
            with self.assertRaisesRegex(EvidenceError, "required"):
                verify(bad_manifest, fresh_record())
            record = fresh_record(); record["producer_provenance"] = ""
            with self.assertRaisesRegex(EvidenceError, "provenance"):
                verify(manifest, record)

    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Tests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        raise SystemExit(1)


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--self-test":
        _self_test()
    else:
        raise SystemExit(main(sys.argv))
```
- [x] Do not invoke, create or commit `verify_round.py` unless its bounded-helper scope is retained in the approved implementation. This is local review support, not hosted enforcement or promotion authorization. Not retained: `verify_round.py` was neither created nor committed.
- [ ] Populate record only from observed CI run/job and artifact outputs. Independent reviewer opens native run URLs, verifies tested merge/head/base revision, required jobs, real selected counts and evidence artifacts. Self-reported JSON can be forged; this checker intentionally cannot prove provenance and must never be sole promotion input.
- [ ] Run `python3 openspec/changes/ci-promotion-gates/verify_round.py MANIFEST.json EVIDENCE.json`. Nonzero blocks review. Zero does not authorize merge, execution or delivery; current required hosted checks and independent product acceptance still gate promotion.
- [ ] A research unit may finish a bounded research deliverable with explicit unknown findings, but no dependent implementation may promote while its required capability remains unknown/blocked. Do not use research success as provider support.
