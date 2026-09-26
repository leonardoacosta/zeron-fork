# Dependency and asset attribution for fork distribution execution contract

**Goal:** Inventory exact selected dependency/asset licenses and required attribution for distributed local builds, including pinned GPUI/component forks, fonts and browser/platform components.
**Architecture:** Existing Rust engine/proto/RPC/profile storage and native clients are the starting point. Freeze interfaces from observed source; no speculative provider API or generic framework.
**Tech stack:** Rust/Tokio/Serde/SQLite; GPUI/Swift/Worker TypeScript only if the approved surface requires them.
**Status:** executable discovery/refinement steps; product implementation NOT READY.
**Dependencies:** `ci-promotion-gates`. Only exact prerequisite promotion admits implementation.

## D1. Recover authority and source (one bounded read per listed anchor)
**Files:** design.md and tasks.md in this change; read-only source anchors in design.md.
- [ ] Read PRD clauses ZF-01, ZF-19 and every C-scenario in `specs/dependency-attribution/spec.md`; state excluded sibling behavior in design.md.
- [ ] From repository root, verify listed anchors exist:
```bash
python3 - <<'PY'
from pathlib import Path
paths = ['Cargo.toml', 'Cargo.lock', 'edge/package-lock.json', 'scripts/package-linux.sh', 'scripts/package-macos.sh', 'dist/macos/Info.plist', 'docs/fork-prd.md']
for name in paths:
    p = Path(name)
    assert p.is_file(), name
    print(name, len(p.read_text().splitlines()), "lines")
PY
```
Expected: one line per anchor, exit0. Missing path means re-discover with graft and correct this contract; do not create a dummy file. Read `graft/INDEX.md` then matching cards. Use `graft ask "Dependency and asset attribution for fork distribution" --source` only if the CLI is already available; graph files are sufficient.
- [ ] In design.md, cite exact symbols/current line spans for the input, authority, persistence and side-effect paths. For each C-scenario record whether current behavior is observed, contradicted or not yet tested. Do not equate missing grep hit with absence proof.

## D2. Execute exact inventory, no guessed licenses
**Files changed:** only `design.md` and this `tasks.md` until the inventory establishes an exact packaging change. **Read:** pinned lockfiles and actual dependency license files. No dependency upgrade or installation authorized by this step.

- [ ] Run this read-only locked-component inventory from repository root. Python3.11+ is required for stdlib tomllib. It prints actual pinned identities and missing license metadata; it does not interpret legal compatibility.
```bash
python3 - <<'PYCODE'
import json, tomllib
from pathlib import Path
cargo = tomllib.loads(Path('Cargo.lock').read_text())['package']
npm = json.loads(Path('edge/package-lock.json').read_text())['packages']
for package in cargo:
    print(json.dumps({'ecosystem':'cargo','name':package['name'],'version':package['version'],'source':package.get('source','workspace'),'license_status':'unresolved-until-source-read'}))
for path, package in npm.items():
    if path:
        print(json.dumps({'ecosystem':'npm','path':path,'version':package.get('version'),'license':package.get('license'),'dev':package.get('dev',False)}))
for path in sorted(Path('crates/ui/assets/fonts/licenses').iterdir()):
    assert path.is_file(), path
    print(json.dumps({'ecosystem':'asset','path':str(path),'bytes':path.stat().st_size}))
PYCODE
```
Expected: nonempty pinned Cargo/npm inventory and both font notice files. Do not copy all transitive build/dev dependencies into a statement that they are shipped; classify linked/shipped/tool-only using actual artifact/build metadata.

- [ ] Run `cargo metadata --locked --offline --format-version 1` and inspect package license/license_file/manifest_path for exact locked sources. If offline cache is absent, record missing source, not inferred MIT; authorized public retrieval can be a separate read-only step. Resolve each selected artifact's native libraries, pinned git dependencies and assets in design.md using columns below.

| Exact package/asset + version/hash | Shipped role | License source path/URL + revision | Required notice text/path | Actual artifact member | Evidence class | Disposition |
|---|---|---|---|---|---|---|

Allowed disposition values: `verified-notice-present`, `missing-notice`, `unresolved-terms`, `not-shipped-with-evidence`. Empty rows are not evidence. Root license, registry metadata and a successful build are insufficient by themselves. Read actual source license text; retain it unchanged.

## D3. Verify notice enforcement with actual artifacts
- [ ] Set `PACKAGE_ROOT` to an extracted **existing** Linux package or Mac app `Contents/Resources`. Do not run release/deploy workflows to get an artifact. The existing packaging scripts put notices under `licenses/fonts`. If an artifact is unavailable, this step blocks distribution acceptance rather than fabricating one.
- [ ] Run this exact check against that real artifact:
```bash
python3 - <<'PYCODE'
import os
from pathlib import Path
root = Path(os.environ['PACKAGE_ROOT'])
source = Path('crates/ui/assets/fonts/licenses')
for path in source.iterdir():
    if path.is_file():
        actual = root / 'licenses/fonts' / path.name
        assert actual.is_file(), f'missing packaged notice: {actual}'
        assert actual.read_bytes() == path.read_bytes(), f'changed notice: {actual}'
print('PASS: packaged font notices match source bytes; other inventory rows still require their own evidence')
PYCODE
```
Expected exit0 only when every current font notice is actually present and byte-identical. This assertion deliberately does not claim complete dependency licensing.
- [ ] Prove failure behavior without modifying the artifact: copy just its `licenses` directory into a new directory under `$JCODE_SCRATCH_DIR`, delete one copied font notice, set PACKAGE_ROOT to that copy and rerun the same block. Expected nonzero with `missing packaged notice`. Restore PACKAGE_ROOT to the real artifact and require green. This is a synthetic negative control, not product acceptance.
- [ ] In design.md map C01 to exact lockfile/artifact hash drift, C02 to missing-notice negative control, C03 to an unresolved inventory row that blocks promotion. No legal conclusion may be guessed by an agent. List exactly which sources remain unavailable.

## D4. Admit only a concretely demonstrated packaging repair
- [ ] If all required notices are present, make no packaging code change. Commit only verified inventory/results in this change after review.
- [ ] If missing, record the exact existing notice source and target artifact member, then author the literal copy/install command and a runnable failing artifact test in this tasks.md before implementing. Never synthesize a license. Unknown legal terms remain blocked for human judgment; do not solve by removing attribution or disabling the check.
- [ ] Validate planning artifacts and record command results:
```bash
python3 openspec/changes/prd-execution-map/validate.py
git diff --check
```
Expected exit0. Review actual package contents against all selected inventory rows before any distribution claim; record tested artifact identity and source commit in this tasks.md.

## Required implementation acceptance after refinement
- C01: Pinned dependency revision changes: attribution evidence invalidated for that package.
- C02: Binary package omits required font notice: packaging gate fails.
- C03: License unresolved: affected distribution held, no assumption from repository root license.

## CI phase after every implementation iteration
- [ ] Run exact refined feature tests and core/affected-platform CI from `../prd-execution-map/design.md`. Verify at least one test actually selected; preserve failing evidence. No next iteration/round promotion while required checks fail or are missing.
- [ ] Run real acceptance: Inspect actual generated package contents and exact pinned licenses; unresolved terms routed to human review without invented conclusions.
- [ ] Update this tasks.md with exact tested commit/tree, commands, counts, exit codes, evidence class, native environment and remaining blocks. Commit scoped files only, then CI on that integrated commit before downstream promotion.

## Rollback
Add notices without altering user data. Rebuild package if notice content corrected; preserve original license texts.
