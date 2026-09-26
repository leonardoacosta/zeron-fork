# Durable resource budgets and usage

Status: proposed; discovery/refinement contract only. Implementation gate CLOSED.

**PRD:** ZF-15, ZF-12, ZF-16
**Round:** 3
**Hard prerequisites:** `harness-preflight-binding`, `profile-access-enforcement`

## Scope
Persist reservations and observed usage bound to run/profile/resource policy. Unknown price or usage remains unknown. Parent and child runs draw from one authorized shared budget without double counting; reservation/launch is atomic or recoverably reconciled. Budget exhaustion holds new work and invokes safe stopping for active work according to policy. No invented universal numeric budget.

## Non-scope
No unrelated subsystem rewrite, global defaults change, unauthorized external mutation or silent capability fallback. This change does not implement sibling change responsibilities. See design.md for exact boundary and approval gate.

## Outcome
Concurrent reservation/restart integration and provider fixture with duplicated/missing usage; real supported provider observations separately labelled.

## Promotion
Follow `../prd-execution-map/design.md` CI protocol. This change and its round cannot promote on stale/partial/missing checks. Approval of the PRD is not blanket implementation or delivery authorization.
