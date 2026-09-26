# Mobile compatible assignment control/read surface

Status: proposed; discovery/refinement contract only. Implementation gate CLOSED.

**PRD:** ZF-01, ZF-03, ZF-04, ZF-06, ZF-14
**Round:** 7
**Hard prerequisites:** `assignment-desktop-surface`

## Scope
Add reviewed mobile parity for the accepted desktop assignment contract, with explicit capability negotiation and owner routing. Preserve direct sessions and display profile/workflow/evidence/stop state correctly. Mobile reconnect must not repeat launches or delivery. Define supported controls explicitly in design rather than silently treating unsupported controls as success.

## Non-scope
No unrelated subsystem rewrite, global defaults change, unauthorized external mutation or silent capability fallback. This change does not implement sibling change responsibilities. See design.md for exact boundary and approval gate.

## Outcome
Existing iOS unit CI plus authorized simulator/device-to-owner workflow and disconnected/stale-revision checks.

## Promotion
Follow `../prd-execution-map/design.md` CI protocol. This change and its round cannot promote on stale/partial/missing checks. Approval of the PRD is not blanket implementation or delivery authorization.
