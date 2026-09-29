# Jcode, Herdr and observer capability research execution contract

**Goal:** Produce bounded, versioned research records for the subjects listed in design.md without implementing or selecting interfaces.
**Architecture:** Inspect local source read-only, then consult official public documentation for separately pinned product identities. Keep source facts, documentation claims, and any separately authorized local observations distinct.
**Status:** Research planning only. No product implementation readiness claim.
**Scope:** For this research, record evidence in this change's canonical `design.md` and modify only this change's `design.md` and `tasks.md`. Do not install, upgrade, configure, authenticate, call provider APIs, probe private endpoints, or spend funds.

## R1. Recover authority and source
1. Read `../../../docs/fork-prd.md`, `../prd-execution-map/design.md`, `specs/integration-harness-observer-research/spec.md`, and this change's `design.md`. Extract applicable ZF-15, ZF-09, ZF-19 clauses, C01-C03, and Unknown prerequisite scenario. Record exclusions and unresolved questions in the decision table in design.md.
2. Treat `crates/harness/src/lib.rs`, `crates/engine/src/registry.rs`, `crates/engine/src/sessions.rs`, `docs/research/harness.md`, and `docs/fork-prd.md` as existing read-only anchors. No other source paths are in scope.
3. From repository root, inspect graph context and exact local anchors using only read operations:
```bash
graft ask "harness capability launch lifecycle observer registry sessions" --source
graft ask "Jcode Herdr SystemOne observer Jev Laya empryo research" --source
rg -n "trait Harness|enum HarnessId|struct Harness|fn .*launch|fn .*stop|observer|registry|session" crates/harness/src/lib.rs crates/engine/src/registry.rs crates/engine/src/sessions.rs docs/research/harness.md docs/fork-prd.md
```
Expected: graft returns relevant source spans or explicitly no useful indexed match; `rg` prints matches or exit 1 for no matches. Exit 1 is not evidence of absence. Follow a relevant source span by reading only that range. Do not dump environment variables, process arguments containing secrets, or local configuration values.
4. Query official public docs for each subject individually with the exact design.md questions. Search results are discovery only. Open the official publisher/project documentation page, capture canonical URL, title, section, published/version date if shown, retrieval UTC date, and verbatim short supporting excerpt. No undocumented facts may be inferred. An unresolved identity stays `unknown`; do not silently normalize empryo spelling.
5. Fill one evidence row per claim using the exact schema in design.md. Set `evidence_kind=local_source` for repository facts and `official_doc` for public docs. Reserve `local_observation` for an explicitly authorized, non-network, read-only local command observation; none is authorized merely by this plan. Set `state=blocked` when authorization or a required source is missing, and `unknown` when evidence search is bounded but inconclusive.

## Required implementation acceptance after refinement
- A tool is installed but no stop proof/API exists: capability remains blocked.
- Documentation and observed version disagree: record mismatch and do not guess request shape.
- Jcode preferred but unavailable: ordinary configured engineer stays unchanged.
- Unknown prerequisite: affected work is `blocked` with reason, not reported successful or rerouted.

## R2. Make bounded evidence and rejection decisions
1. Complete separate subject rows for Jcode local swarm, Herdr, SystemOne observer, Jev, Laya, and empryo. For each capture identity/version, native ID, documented start/status/stop proof, configuration, usage, auth/data boundary, isolation, and unknowns. Do not collapse identities.
2. Run through C01-C03 and the unknown-prerequisite case. For each record `scenario_id`, `state` (`verified`, `contradicted`, `unknown`, `blocked`), `evidence_refs`, `reason`, and `remaining_question`. Preserve these exact required acceptance sentences:
   - A tool is installed but no stop proof/API exists: capability remains blocked.
   - Documentation and observed version disagree: record mismatch and do not guess request shape.
   - Jcode preferred but unavailable: ordinary configured engineer stays unchanged.
   C01 cannot be accepted without stop proof. C02 must preserve the mismatch and must not invent a request shape. C03 must state whether the configured engineer remains unchanged when Jcode is unavailable.
3. Create a child adapter decision record only when enough evidence exists. Use all fields in design.md; put `unknown` in unsupported fields. `decision_state=candidate` means only eligible for a separately reviewed follow-up, not selected or implementable. Otherwise use `blocked`, `rejected`, or `needs_review`. Never produce fake provider responses.
4. Reject/block any candidate meeting design.md rejection criteria. No API calls, private access, credentials, process-control actions, profile/config changes, installation, upgrades, or external probes are part of this task.

## R3. Review and validation
1. Check every applicable PRD/spec clause and scenario against a row; verify all docs claims cite official public pages and source claims cite current exact paths/spans. Keep docs separate from live observations. Check all evidence rows include every required field and allowed state/kind, and each child record includes every required field.
2. Persist completed evidence, scenario rows, and child adapter records in the Evidence register section of this canonical `design.md`; do not leave the only research result in a temporary JSON file.
3. Run the planned standard-library checker below from repository root against a temporary JSON export of the Evidence register. It validates record shape, not factual truth. Keep the canonical design.md register authoritative.
4. Run `python3 openspec/changes/prd-execution-map/validate.py` and `git diff --check`. Expected: validator exit 0; whitespace check exit 0. These do not validate provider functionality.

### Planned stdlib evidence-schema checker and self-tests
The following complete code is for a temporary `check_evidence.py` during research, not a product file. It validates required evidence fields and enumerated values, nonempty rows, and unique claim IDs. Save exactly as shown only in a temporary directory, then run `python3 check_evidence.py evidence.json`; its self-tests run with `python3 check_evidence.py --self-test`.

```python
import json
import sys
import unittest
from pathlib import Path

FIELDS = {
    "claim_id", "subject", "claim", "state", "evidence_kind",
    "source_or_command", "version_or_commit", "observed_at_utc",
    "result_or_excerpt", "scope", "limitations", "reviewer",
}
STATES = {"verified", "contradicted", "unknown", "blocked"}
KINDS = {"official_doc", "local_source", "local_observation"}


def validate(rows):
    errors = []
    if not isinstance(rows, list):
        return ["top-level JSON must be a list"]
    if not rows:
        return ["evidence list must not be empty"]
    seen_claim_ids = set()
    for i, row in enumerate(rows):
        if not isinstance(row, dict):
            errors.append(f"row {i}: must be an object")
            continue
        missing = FIELDS - row.keys()
        extra = row.keys() - FIELDS
        if missing:
            errors.append(f"row {i}: missing {', '.join(sorted(missing))}")
        if extra:
            errors.append(f"row {i}: unexpected {', '.join(sorted(extra))}")
        if row.get("state") not in STATES:
            errors.append(f"row {i}: invalid state")
        if row.get("evidence_kind") not in KINDS:
            errors.append(f"row {i}: invalid evidence_kind")
        claim_id = row.get("claim_id")
        if isinstance(claim_id, str) and claim_id.strip():
            if claim_id in seen_claim_ids:
                errors.append(f"row {i}: duplicate claim_id {claim_id}")
            seen_claim_ids.add(claim_id)
        for key in FIELDS & row.keys():
            if not isinstance(row[key], str) or not row[key].strip():
                errors.append(f"row {i}: {key} must be a non-empty string")
    return errors


class EvidenceSchemaTests(unittest.TestCase):
    def test_complete_row_passes(self):
        row = {key: "value" for key in FIELDS}
        row.update(state="unknown", evidence_kind="official_doc")
        self.assertEqual(validate([row]), [])

    def test_missing_field_fails(self):
        row = {key: "value" for key in FIELDS if key != "reviewer"}
        row.update(state="blocked", evidence_kind="local_source")
        self.assertIn("row 0: missing reviewer", validate([row]))

    def test_invalid_state_fails(self):
        row = {key: "value" for key in FIELDS}
        row.update(state="maybe", evidence_kind="local_observation")
        self.assertIn("row 0: invalid state", validate([row]))

    def test_non_object_fails(self):
        self.assertIn("row 0: must be an object", validate([None]))

    def test_empty_list_fails(self):
        self.assertIn("evidence list must not be empty", validate([]))

    def test_duplicate_claim_id_fails(self):
        row = {key: "value" for key in FIELDS}
        row.update(claim_id="same", state="unknown", evidence_kind="official_doc")
        self.assertIn("row 1: duplicate claim_id same", validate([row, row]))


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--self-test":
        unittest.main(argv=[sys.argv[0]])
    elif len(sys.argv) == 2:
        errors = validate(json.loads(Path(sys.argv[1]).read_text(encoding="utf-8")))
        print("\n".join(errors) if errors else "valid evidence schema")
        raise SystemExit(bool(errors))
    else:
        raise SystemExit("usage: check_evidence.py EVIDENCE.json | --self-test")
```

## CI phase after every implementation iteration

Research itself has no implementation iterations. If a separately approved implementation follows, run its exact refined tests and required CI, then record command, result, evidence class, and remaining blocks. This required heading does not authorize implementation.

## Completion boundary
A complete research pass means schemas are filled with cited evidence or explicit `unknown`/`blocked` outcomes and the planning checks pass. It does not mean a provider was selected, an adapter API was frozen, or all future adapters can be implemented. External/native acceptance unavailable means blocked, not complete.

## Research execution record (2026-09-27)
- [x] Read applicable PRD, execution-map, prerequisite, spec, and listed read-only anchors.
- [x] Bounded public-doc discovery/fetch via Firecrawl CLI 1.23.3; source citations and URL/DNS limitations recorded in the design register.
- [x] Recorded current local source facts separately from docs; no local observations or runtime probes authorized/performed.
- [x] Added separate subject, scenario, and child decision records. Unresolved product identity and integration contracts remain `unknown`/`blocked`; no candidate selected.
- [x] Scratch schema checker self-tests (6/6), canonical evidence export validates, `python3 openspec/changes/prd-execution-map/validate.py` passes, and `git diff --check` passes. These checks certify shape/planning only, not provider functionality.
- Limitation: local checkout commit was not captured; current code spans are static source citations. Jcode swarm/API and Herdr compatibility/security boundaries are unresolved. Exact `Laya` and `empryo` identities remain unknown. C03 remains unverified because no runtime availability check was authorized.

## Rollback
No product/provider state changes are allowed. Discard temporary checker/evidence files after validation unless separately authorized. Only the two canonical files listed in scope may be edited for this change.
