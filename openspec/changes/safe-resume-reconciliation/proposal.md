# Recovery with continuing authority and effect reconciliation

Status: proposed; discovery/refinement contract only. Implementation gate CLOSED.

**PRD:** ZF-04, ZF-14
**Round:** 4
**Hard prerequisites:** `confirmed-stop-handoff`, `run-resource-ledger`

## Scope
On crash/reconnect reconstruct frozen configuration, authorization, native session identity and effect uncertainty. Resume only a known-safe still-authorized continuation. Unknown external effects hold for Leo with evidence and reconciliation options. Keep interrupted, stopped, failed and outcome-confirmed distinct. Direct-session recovery must obey the same boundary.

## Non-scope
No unrelated subsystem rewrite, global defaults change, unauthorized external mutation or silent capability fallback. This change does not implement sibling change responsibilities. See design.md for exact boundary and approval gate.

## Outcome
Crash-boundary subprocess tests and authorized native restart with revoked-policy negative case; no external side effect replay.

## Promotion
Follow `../prd-execution-map/design.md` CI protocol. This change and its round cannot promote on stale/partial/missing checks. Approval of the PRD is not blanket implementation or delivery authorization.
