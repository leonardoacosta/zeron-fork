# Browser provider isolation research execution contract

**Goal:** Compare current embedded-browser source with bounded public documentation claims about candidate provider isolation, scope, stopping and evidence behavior.
**Architecture:** Inspect local source read-only, then evaluate each identified product only from official public documentation. Do not launch browsers or invoke provider APIs.
**Status:** Bounded documentation/source research complete, reviewed 2026-09-30 against evidence recorded 2026-09-27. No provider/interface selection, runtime acceptance, implementation readiness, or prerequisite promotion claim.
**Scope:** Only this change's `design.md` and `tasks.md` may be edited. No user profile mutation, private pages, credentials, API calls, network probes, installs/configuration changes, cloud uploads, or spend.

## R1. Recover authority and inspect local source
1. Read `../../../docs/fork-prd.md`, `../prd-execution-map/design.md`, `specs/integration-browser-research/spec.md`, and this change's `design.md`. List ZF-17/ZF-19 requirements, C01-C03, and Unknown prerequisite scenario in the final coverage table. Existing read-only anchors are `crates/ui/src/browser/mod.rs`, `crates/ui/src/browser/model.rs`, `crates/ui/src/browser/macos.rs`, `scripts/run-macos-browser-fixture.sh`, and `docs/fork-prd.md`; no other source paths are in scope.
2. From repository root run read-only commands:
```bash
graft ask "embedded browser model macOS lifecycle isolation" --source
graft ask "browser fixture process start stop cancellation evidence" --source
rg -n "struct .*Browser|enum .*Browser|start|stop|close|cancel|profile|session|cookie|storage|download" crates/ui/src/browser/mod.rs crates/ui/src/browser/model.rs crates/ui/src/browser/macos.rs scripts/run-macos-browser-fixture.sh docs/fork-prd.md
```
Expected: cite exact relevant symbols/spans. `rg` exit 1 means no pattern match, not evidence that a capability is absent. Read only relevant source spans. Do not run the fixture script.
3. Record local behavior as `local_source` claims only: relevant action/state, owning function, process/session identity if visible in code, storage/config source if visible, close/cancellation behavior visible in code, and what remains unproven. Source code cannot prove actual provider behavior.

## R2. Official public documentation review
1. Identify candidates only from already available public product documentation; do not install tools or select based on a skill name. For each candidate and the embedded-browser platform documentation, open official publisher docs and answer design.md's exact bounded questions: canonical name/version/platform; isolation of cookies/cache/local storage/downloads; explicit scope grant/revoke; native session/process ID; start/status/completed-stop proof; close versus child-action completion; evidence redaction; network/cloud/telemetry data flow; credential storage.
2. Capture canonical URL, page title, exact section, doc version/update date if shown, retrieval UTC date and short excerpt. Search result snippets are not evidence. If docs are absent or ambiguous, write `unknown`, not a guessed API behavior.

## Required implementation acceptance after refinement
- Provider supports screenshots but cannot isolate storage: does not satisfy session isolation.
- Provider close command returns before tool action stops: cancellation remains unverified.
- Provider needs cloud data upload: disclose data boundary before any private page use.
- Unknown prerequisite: block with reason rather than claiming success.

## R3. Record decisions and scenario outcomes
1. Create evidence rows using every design.md evidence field and allowed state/kind. `official_doc` means documented only. `local_observation` is not authorized by this task and must not be used.
2. For C01-C03 and unknown prerequisite, record `scenario_id`, `state`, `evidence_refs`, `reason`, `remaining_question`. Preserve these exact required acceptance sentences:
   - Provider supports screenshots but cannot isolate storage: does not satisfy session isolation.
   - Provider close command returns before tool action stops: cancellation remains unverified.
   - Provider needs cloud data upload: disclose data boundary before any private page use.
   C01 fails if storage isolation is not evidenced even when screenshots work. C02 remains unknown/blocked without proof actions stopped. C03 must identify any documented cloud boundary and must not use private pages.
3. Any child adapter candidate must include every field from design.md. Use unknown where facts are absent and `write_operations=not authorized`. `candidate` allows only separate review; it does not select a provider, freeze an API, or prove all future adapters implementable. Reject/block against design.md criteria.

## R4. Review and planning validation
1. Trace every applicable clause/scenario to evidence. Verify official-doc claims link to publisher pages, local-source claims cite exact current source ranges, and docs are never mislabeled live observation. Verify no prohibited browser launch, profile/private-page access, credentials, provider calls, external probes, installs/config changes or data uploads occurred.
2. Run `python3 openspec/changes/prd-execution-map/validate.py` and `git diff --check` from repository root. Expected: both exit 0. These checks validate planning/whitespace only. Record commands and exit codes; do not claim browser acceptance.

## CI phase after every implementation iteration

Research itself has no implementation iterations. If a separately approved implementation follows, run its exact refined tests and required CI, then record command, result, evidence class, and remaining blocks. This required heading does not authorize implementation.

## Completion boundary
Complete means every bounded question and scenario has cited evidence or explicit `unknown`/`blocked`, and planning checks pass. Provider choice and runtime interface remain unselected. No claim that all future adapters are implementable.

## Rollback
Only the two canonical files listed in scope may change. No browser/provider state changes occur.

## Research execution status (2026-09-27)

- R1: inspected `fork-prd.md`, execution-map design, spec, this design, prerequisite design, and only listed local source anchors. Local facts and exact spans are classified `local_source` in design.md. Graft queries returned no graph; source paths were then inspected directly. No fixture was run.
- R2: official docs reviewed: WebKit profile/data-store article (2023-08-30); Playwright isolation, BrowserContext, Browser, authentication and tracing pages (retrieved 2026-09-27; pages did not state a pinned release in fetched content). URLs, sections, excerpts and limits are in design.md. Playwright is documentation subject only, not a selection.
- R3: evidence rows, C01-C03 and unknown-prerequisite records, and complete provisional child adapter schema are in design.md. C01 blocked; C02 unknown; C03 unknown; prerequisite blocked. `write_operations=not authorized` retained.
- R4: no browser/profile/private-page/provider/API/network-probe/install/config/cloud operation was performed. Evidence/scenario records reviewed 2026-09-30; fresh planning validation and whitespace checks passed (exit 0). Historical source rows retain their stated dirty-tree provenance and are not reclassified as current-source or runtime observations.

Required acceptance sentences retained exactly in design.md:
“Provider supports screenshots but cannot isolate storage: does not satisfy session isolation.”
“Provider close command returns before tool action stops: cancellation remains unverified.”
“Provider needs cloud data upload: disclose data boundary before any private page use.”

Validation (rerun 2026-09-30): `python3 openspec/changes/prd-execution-map/validate.py` — exit 0 (`PASS: 36 child changes, all 19 PRD references, 10 CI barriers, acyclic dependencies, existing anchors and scenario mappings`; planning validation only). `git diff --check` — exit 0.
