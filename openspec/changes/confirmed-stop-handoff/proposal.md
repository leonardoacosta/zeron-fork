# Confirmed stopping and explicit human handoff

Status: proposed; discovery/refinement contract only. Implementation gate CLOSED.

**PRD:** ZF-04, ZF-15, ZF-10
**Round:** 3
**Hard prerequisites:** `profile-access-enforcement`, `harness-preflight-binding`

## Scope
Define pause-requested, stopping, stopped-confirmed, human-owned, handback-requested and resumable states with guarded transitions. Stop receipts are observations, not proof. Track native process/session and descendant/tool activity for supported harnesses. Hand takeover only after stop proof; unknown remote/process status remains held. Human handback is explicit and revalidates authority/configuration.

## Non-scope
No unrelated subsystem rewrite, global defaults change, unauthorized external mutation or silent capability fallback. This change does not implement sibling change responsibilities. See design.md for exact boundary and approval gate.

## Outcome
Real harmless subprocess with descendant writes proves last write/exit boundary; native harness-specific stopping requires its own evidence.

## Promotion
Follow `../prd-execution-map/design.md` CI protocol. This change and its round cannot promote on stale/partial/missing checks. Approval of the PRD is not blanket implementation or delivery authorization.
