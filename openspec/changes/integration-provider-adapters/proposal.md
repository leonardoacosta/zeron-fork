# Verified provider adapters and authority preservation

Status: proposed; discovery/refinement contract only. Implementation gate CLOSED.

**PRD:** ZF-19, ZF-15
**Round:** 5
**Hard prerequisites:** `integration-harness-observer-research`, `integration-github-ado-research`, `profile-access-enforcement`, `harness-preflight-binding`, `confirmed-stop-handoff`

## Scope
Instantiate one child adapter change per researched concrete provider and action set before implementation. Each child freezes documented API/version, maps native identity/status/stop/effect semantics, honors profile and external authority, and has real authorized acceptance. This boundary is a fan-out contract, not permission to implement all adapters in one patch. MCP exposure must reuse engine authorization, not bypass it.

## Non-scope
No unrelated subsystem rewrite, global defaults change, unauthorized external mutation or silent capability fallback. This change does not implement sibling change responsibilities. See design.md for exact boundary and approval gate.

## Outcome
One real harmless authorized workflow per selected adapter and failure/unknown capability checks. Unselected providers remain blocked, not marked complete.

## Promotion
Follow `../prd-execution-map/design.md` CI protocol. This change and its round cannot promote on stale/partial/missing checks. Approval of the PRD is not blanket implementation or delivery authorization.
