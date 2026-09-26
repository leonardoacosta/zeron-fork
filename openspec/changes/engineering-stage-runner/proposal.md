# Approved proposal implementation and verification stages

Status: proposed; discovery/refinement contract only. Implementation gate CLOSED.

**PRD:** ZF-05, ZF-14, ZF-15
**Round:** 6
**Hard prerequisites:** `manual-investigation-runner`, `verification-acceptance-gates`, `run-resource-ledger`

## Scope
Extend the bounded investigation runner to Understand, Investigate, Propose, Implement and Verify transitions under a pinned workflow. A proposal must pass its configured gate before any implementation dispatch. Bind exact approved scope, engineer, repository, baseline and resource policy; ordinary implementation uses that engineer once. Produce a new revision-bound candidate from observed working-tree changes, then run independent configured verification. Deliver and Confirm outcome invoke their separately gated contracts, not implicit inline side effects.

## Non-scope
No unrelated subsystem rewrite, global defaults change, unauthorized external mutation or silent capability fallback. This change does not implement sibling change responsibilities. See design.md for exact boundary and approval gate.

## Outcome
Real harmless local repository: accepted proposal to one engineer implementation, exact candidate capture, failing then passing independent check, no unauthorized delivery.

## Promotion
Follow `../prd-execution-map/design.md` CI protocol. This change and its round cannot promote on stale/partial/missing checks. Approval of the PRD is not blanket implementation or delivery authorization.
