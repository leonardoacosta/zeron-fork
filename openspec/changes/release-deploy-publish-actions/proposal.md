# Release, deploy and publish adapters

Status: proposed; discovery/refinement contract only. Implementation gate CLOSED.

**PRD:** ZF-07, ZF-19
**Round:** 7
**Hard prerequisites:** `delivery-effect-ledger`, `integration-github-ado-research`

## Scope
Implement individually callable release/deploy/publish against explicitly selected destinations and verified contracts. Preserve build artifact identity, target environment, authorization and post-delivery observation. Local installation is a valid deploy target; hosted replacement is never inferred. Full release-candidate management beyond these actions remains outside approved scope.

## Non-scope
No unrelated subsystem rewrite, global defaults change, unauthorized external mutation or silent capability fallback. This change does not implement sibling change responsibilities. See design.md for exact boundary and approval gate.

## Outcome
Harmless local install with service recovery and rollback, then separately authorized external destinations only when selected.

## Promotion
Follow `../prd-execution-map/design.md` CI protocol. This change and its round cannot promote on stale/partial/missing checks. Approval of the PRD is not blanket implementation or delivery authorization.
