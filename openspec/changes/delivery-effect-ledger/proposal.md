# Independent delivery authorization and effect reconciliation

Status: proposed; discovery/refinement contract only. Implementation gate CLOSED.

**PRD:** ZF-07, ZF-04, ZF-14
**Round:** 6
**Hard prerequisites:** `verification-acceptance-gates`, `safe-resume-reconciliation`

## Scope
Define independently callable push/create-PR/merge/release/deploy/publish intents, each bound to exact candidate, destination, account reference and workflow action policy. Persist planned/dispatched/observed/uncertain/reconciled outcome states. An ambiguous effect is queried/reconciled before another dispatch; dedupe keys are not exactly-once claims. This unit defines the contract, not every provider adapter.

## Non-scope
No unrelated subsystem rewrite, global defaults change, unauthorized external mutation or silent capability fallback. This change does not implement sibling change responsibilities. See design.md for exact boundary and approval gate.

## Outcome
Controlled local external-effect fixture with crash boundaries, plus each adapter's separate authorized real destination gate.

## Promotion
Follow `../prd-execution-map/design.md` CI protocol. This change and its round cannot promote on stale/partial/missing checks. Approval of the PRD is not blanket implementation or delivery authorization.
