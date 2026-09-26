# Provenance-bound automatic triggers

Status: proposed; discovery/refinement contract only. Implementation gate CLOSED.

**PRD:** ZF-08, ZF-06, ZF-09, ZF-10
**Round:** 8
**Hard prerequisites:** `priority-backlog`, `accepted-output-dependencies`, `manual-investigation-runner`

## Scope
Add opt-in event triggers with provenance, explicit workflow binding and stable event identity. A trigger prepares approval or launches only within configured authority/profile/resources/admission. Duplicate/reordered events do not duplicate launch. Manual launch remains available. No comparisons may be triggered automatically.

## Non-scope
No unrelated subsystem rewrite, global defaults change, unauthorized external mutation or silent capability fallback. This change does not implement sibling change responsibilities. See design.md for exact boundary and approval gate.

## Outcome
Local event replay/reorder/concurrent delivery with actual runner admission and resource-denied case; selected external event source separately verified.

## Promotion
Follow `../prd-execution-map/design.md` CI protocol. This change and its round cannot promote on stale/partial/missing checks. Approval of the PRD is not blanket implementation or delivery authorization.
