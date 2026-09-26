# Bounded parent/child repository objectives

Status: proposed; discovery/refinement contract only. Implementation gate CLOSED.

**PRD:** ZF-12, ZF-02, ZF-15
**Round:** 8
**Hard prerequisites:** `accepted-output-dependencies`, `priority-backlog`, `run-resource-ledger`, `workflow-version-selection`

## Scope
Parent objective groups linked repository-scoped children with independent workflow, permissions, candidate/evidence and delivery status. Agent breakdown is proposal until its workflow gate authorizes creation. Leo can inspect/edit. Children stay inside parent objective, approved repositories/profile and shared budget. Grouping neither grants cross-profile access nor requires simultaneous deployment.

## Non-scope
No unrelated subsystem rewrite, global defaults change, unauthorized external mutation or silent capability fallback. This change does not implement sibling change responsibilities. See design.md for exact boundary and approval gate.

## Outcome
Two real local repositories with independent children, one dependency and budget/scope-denied child; restart restores editable breakdown.

## Promotion
Follow `../prd-execution-map/design.md` CI protocol. This change and its round cannot promote on stale/partial/missing checks. Approval of the PRD is not blanket implementation or delivery authorization.
