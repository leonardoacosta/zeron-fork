# Exact-version output dependencies

Status: proposed; discovery/refinement contract only. Implementation gate CLOSED.

**PRD:** ZF-11, ZF-14
**Round:** 7
**Hard prerequisites:** `verification-acceptance-gates`, `conflict-admission-observer`

## Scope
Bind dependency edges to accepted stage-output versions, not just whole assignment completion. Reject cycles and foreign-profile edges. Allow independent work to overlap. Upstream replacement/revocation triggers downstream reassessment before next dependent action; prior execution effects are preserved and never retroactively called safe.

## Non-scope
No unrelated subsystem rewrite, global defaults change, unauthorized external mutation or silent capability fallback. This change does not implement sibling change responsibilities. See design.md for exact boundary and approval gate.

## Outcome
Graph transaction/restart tests and real two-stage workflow proving exact-version binding and invalidation.

## Promotion
Follow `../prd-execution-map/design.md` CI protocol. This change and its round cannot promote on stale/partial/missing checks. Approval of the PRD is not blanket implementation or delivery authorization.
