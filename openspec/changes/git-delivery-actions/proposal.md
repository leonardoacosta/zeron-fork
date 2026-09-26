# Git push and change-request create/merge actions

Status: proposed; discovery/refinement contract only. Implementation gate CLOSED.

**PRD:** ZF-07, ZF-19
**Round:** 7
**Hard prerequisites:** `delivery-effect-ledger`, `integration-github-ado-research`

## Scope
Implement push, create change request and merge as independently authorized actions using verified provider methods. Freeze remote/ref/repository/account/candidate; observe exact delivered commit. Support required GitHub/ADO providers only when their research and native acceptance are complete; unsupported remains explicit. Respect protected branches and external review authority.

## Non-scope
No unrelated subsystem rewrite, global defaults change, unauthorized external mutation or silent capability fallback. This change does not implement sibling change responsibilities. See design.md for exact boundary and approval gate.

## Outcome
Local bare-remote push first; actual authorized sandbox GitHub/ADO create/merge with exact head verification and provider failure paths.

## Promotion
Follow `../prd-execution-map/design.md` CI protocol. This change and its round cannot promote on stale/partial/missing checks. Approval of the PRD is not blanket implementation or delivery authorization.
