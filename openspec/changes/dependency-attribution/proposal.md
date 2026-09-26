# Dependency and asset attribution for fork distribution

Status: proposed; discovery/refinement contract only. Implementation gate CLOSED.

**PRD:** ZF-01, ZF-19
**Round:** 0
**Hard prerequisites:** `ci-promotion-gates`

## Scope
Inventory exact selected dependency/asset licenses and required attribution for distributed local builds, including pinned GPUI/component forks, fonts and browser/platform components. Root MIT alone does not settle asset/dependency terms. Record evidence and package required notices without claiming legal review beyond verified facts.

## Non-scope
No unrelated subsystem rewrite, global defaults change, unauthorized external mutation or silent capability fallback. This change does not implement sibling change responsibilities. See design.md for exact boundary and approval gate.

## Outcome
Inspect actual generated package contents and exact pinned licenses; unresolved terms routed to human review without invented conclusions.

## Promotion
Follow `../prd-execution-map/design.md` CI protocol. This change and its round cannot promote on stale/partial/missing checks. Approval of the PRD is not blanket implementation or delivery authorization.
