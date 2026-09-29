# GitHub, ADO, MCP and Aperture boundary research execution contract

**Goal:** Produce bounded evidence for local GitHub/MCP behavior and public documented capabilities/authority boundaries of separately identified GitHub, ADO and Tailscale/Aperture systems.
**Architecture:** Read local sources without invoking integrations. Look up official public documentation only. Separate observed local facts from documentation statements and never treat transport access as workflow authority.
**Status:** Research planning only. No product implementation readiness or interface selection.
**Scope:** Only this change's `design.md` and `tasks.md` may be changed by this work. No credentials, external APIs, private access, endpoint probes, writes, spend, or Brown resources.

## Research result (2026-09-27)

- [x] Inspected only listed local source anchors and direct behavior. Exact source spans and per-operation authority/side-effect/failure/current-limit records are in `design.md` → Local behavior records.
- [x] Read official public GitHub PR/auth documentation (API version 2026-03-10), Microsoft Learn Azure DevOps Git Pull Requests (API 7.1), and official Tailscale Aperture overview/how-it-works/reference and Tailscale transport documentation. Evidence rows include canonical URLs, headings, observed date and scope limits.
- [x] Added complete evidence-schema rows, explicit unknown/blocked claims, provisional child adapter records with all required fields, and scenario/PRD clause coverage in `design.md`.
- [x] Bounded the unknowns: GitHub API-wide retry/rate/idempotency detail; exact ADO deployment/authority/auth and operational semantics; Aperture runtime/version/connector/workflow authority; named external source of truth; and product policy for remote-only repositories.
- [x] No provider APIs, credentials, private access, endpoint probes, Brown resources, writes, install/configuration, or commits. Firecrawl 1.23.3 was present and authenticated, but its inspected help did not expose a DNS/every-redirect validation guarantee; no Firecrawl URL fetch was made. Official public-document lookup used the built-in web research interface.

| Check | Result |
|---|---|
| Evidence-checker self-tests | Not applicable: no evidence-checker/self-test script was identified in this change contract or required local anchors; no checker was invented or run. |
| `python3 openspec/changes/prd-execution-map/validate.py` | Exit 0: PASS, 36 child changes, all 19 PRD references, 10 CI barriers, acyclic dependencies, existing anchors and scenario mappings. Planning validation only. |
| `git diff --check` | Exit 0. |
| Commit / provider acceptance | None; not authorized and not claimed. |

## R1. Recover authority and inspect local implementation
1. Read `../../../docs/fork-prd.md`, `../prd-execution-map/design.md`, `specs/integration-github-ado-research/spec.md`, and this change's `design.md`. List applicable ZF-19/ZF-07 clauses, C01-C04, and Unknown prerequisite scenario in the final coverage table. Existing read-only anchors are `crates/engine/src/source_control.rs`, `crates/mcp/src/tools.rs`, `crates/mcp/src/jsonrpc.rs`, `docs/mcp.md`, and `docs/fork-prd.md`; no other source paths are in scope.
2. From repository root run these read-only commands:
```bash
graft ask "GitHub source control operations local status MCP tools authority" --source
graft ask "ADO Tailscale Aperture official API authority boundary research" --source
rg -n "GitHubCli|pub fn|async fn|tool|scope|profile|source_control|repo" crates/engine/src/source_control.rs crates/mcp/src/tools.rs crates/mcp/src/jsonrpc.rs docs/mcp.md docs/fork-prd.md
```
Expected: record relevant exact source symbols/spans. `rg` exit 1 means no matching text under that pattern, not proof a capability is absent. Read only relevant source ranges and do not display secrets/configuration values.
3. In `local_behavior` rows record `operation`, `input`, `source_span`, `authority_check`, `side_effect`, `failure_result`, `current_limit`, and cite only source/docs. Explicitly distinguish current GitHub read/status and MCP behavior from desired behavior. Do not call MCP/provider tools.

## R2. Public documentation lookup
For GitHub, ADO, Tailscale, and Aperture as applicable, look up official public docs. Search results may locate docs but are not evidence until the publisher's page is opened and cited. Ask each doc the exact questions: What canonical product/API name and publisher own it? Which API/version is documented? What auth scopes and read/write operations does it specify? What status, pagination, rate limits, retry/idempotency and error behavior are documented? Which system is authoritative for issue/workflow/review state? Does official guidance describe a remote-only repository without local materialization? What data crosses network boundaries? Is Aperture a product/workflow or only a transport/access layer in the cited material? Capture canonical URL, page title, exact heading/section, doc version/update date if shown, retrieval UTC date, short excerpt, and each unanswered question as `unknown`. Do not infer parity.

## Required implementation acceptance after refinement
- MCP tool available but action outside profile/workflow scope: unavailable for that action.
- External issue says Done while local output unverified: no acceptance transition.
- Remote repository cannot be materialized locally: report capability limitation, not require local storage as product policy.
- ADO/Brown endpoint discovered: no access attempt solely because Brown profile exists.
- Unknown prerequisite: block with reason; no silent success/reroute.

## R3. Evidence and decisions
1. Use design.md's full evidence schema for every claim. Allowed states: `verified`, `contradicted`, `unknown`, `blocked`. Allowed evidence kinds: `official_doc`, `local_source`, `local_observation`. Do not use `local_observation` in this task because it authorizes no provider invocation.
2. For C01-C04 and unknown prerequisite, create rows with `scenario_id`, `state`, `evidence_refs`, `reason`, `remaining_question`. Preserve these exact required acceptance sentences:
   - MCP tool available but action outside profile/workflow scope: unavailable for that action.
   - External issue says Done while local output unverified: no acceptance transition.
   - Remote repository cannot be materialized locally: report capability limitation, not require local storage as product policy.
   - ADO/Brown endpoint discovered: no access attempt solely because Brown profile exists.
   Do not convert external Done to local acceptance. If remote-only is unsupported or undocumented, report the limitation/unknown, not a product policy requiring checkout. An ADO/Brown endpoint mention is not permission to access it.
3. For each genuinely evidenced follow-up, create design.md's child-adapter record with every field present. Use `unknown` where evidence is absent, and `write_operations=not authorized`. `candidate` is only a proposal for a separate review, not a selected interface or claim of universal implementability. Reject/block per design.md criteria.

## R4. Review and checks
1. Trace each applicable clause/scenario to evidence. Verify every external claim cites official public documentation and every implementation claim cites exact current local source. Label docs as documented, not live observed. Confirm no API calls, private access, credentials, endpoint probes, external writes, Brown resources, or commits occurred.
2. Run `python3 openspec/changes/prd-execution-map/validate.py` and `git diff --check` from repository root. Expected: both exit 0. These validate plans/whitespace only, not integration behavior. Record command and exit code in the task result; do not claim provider acceptance.

## CI phase after every implementation iteration

Research itself has no implementation iterations. If a separately approved implementation follows, run its exact refined tests and required CI, then record command, result, evidence class, and remaining blocks. This required heading does not authorize implementation.

## Completion boundary
Complete means documented evidence or explicit `unknown`/`blocked` for each bounded question, scenario coverage, and planning checks pass. No interfaces are selected. The result does not claim all future adapters are implementable.

## Rollback
Only the two canonical files listed in scope may change. This research has no external side effects to roll back.
