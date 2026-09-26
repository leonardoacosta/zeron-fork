# Browser provider isolation research

Status: proposed; discovery/refinement contract only. Implementation gate CLOSED.

**PRD:** ZF-17, ZF-19
**Round:** 1
**Hard prerequisites:** `ci-promotion-gates`

## Scope
Compare existing embedded browser capability and candidate automation providers against required profile/session isolation, explicit signed-in scope, stopping and redacted evidence. Record API/version and credential handling, select only after reviewed decision. Browser choice is a genuine open decision, not a reason to reopen approved isolation rules.

## Non-scope
No unrelated subsystem rewrite, global defaults change, unauthorized external mutation or silent capability fallback. This change does not implement sibling change responsibilities. See design.md for exact boundary and approval gate.

## Outcome
Harmless local page/isolation probe where possible; unresolved provider decision explicitly blocks scoped-browser-capability implementation.

## Promotion
Follow `../prd-execution-map/design.md` CI protocol. This change and its round cannot promote on stale/partial/missing checks. Approval of the PRD is not blanket implementation or delivery authorization.
