# Parent outcome verification over delivered versions

Status: proposed; discovery/refinement contract only. Implementation gate CLOSED.

**PRD:** ZF-13, ZF-12, ZF-14
**Round:** 9
**Hard prerequisites:** `multi-repository-breakdown`, `git-delivery-actions`, `release-deploy-publish-actions`

## Scope
Parent workflow evaluates combined checks across exact required child output and delivered versions before objective completion. Finished children are insufficient. Partial delivery visible; failed child blocks dependents only. Configured human/autonomous outcome gates apply. Superseded child outputs cannot silently count.

## Non-scope
No unrelated subsystem rewrite, global defaults change, unauthorized external mutation or silent capability fallback. This change does not implement sibling change responsibilities. See design.md for exact boundary and approval gate.

## Outcome
Real two-repository local consumer/provider compatibility check including stale delivered version and partial failure.

## Promotion
Follow `../prd-execution-map/design.md` CI protocol. This change and its round cannot promote on stale/partial/missing checks. Approval of the PRD is not blanket implementation or delivery authorization.
