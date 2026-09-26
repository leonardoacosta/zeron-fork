# Configured verification and acceptance transitions

Status: proposed; discovery/refinement contract only. Implementation gate CLOSED.

**PRD:** ZF-05, ZF-14, ZF-11
**Round:** 4
**Hard prerequisites:** `workflow-version-selection`, `revision-evidence-bindings`, `profile-access-enforcement`

## Scope
Keep agent-finished, verified, accepted, delivered and outcome-confirmed separate. Evaluate configured checks against exact bound output versions. Human or autonomous acceptance is allowed only as workflow policy specifies. Preserve external reviewer/OpenSpec/planning authority; in-product status cannot overwrite it. Missing/stale/contradictory evidence holds dependent transitions.

## Non-scope
No unrelated subsystem rewrite, global defaults change, unauthorized external mutation or silent capability fallback. This change does not implement sibling change responsibilities. See design.md for exact boundary and approval gate.

## Outcome
Owner RPC transitions with stale/revoked/external-rejection cases and restart at decision commit boundary.

## Promotion
Follow `../prd-execution-map/design.md` CI protocol. This change and its round cannot promote on stale/partial/missing checks. Approval of the PRD is not blanket implementation or delivery authorization.
