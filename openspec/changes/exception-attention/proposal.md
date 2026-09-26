# Immediate grouped safety exceptions

Status: proposed; discovery/refinement contract only. Implementation gate CLOSED.

**PRD:** ZF-18, ZF-04, ZF-09
**Round:** 4
**Hard prerequisites:** `confirmed-stop-handoff`, `revision-evidence-bindings`

## Scope
Persist and group actionable exceptions with source, profile, affected work, blocker/uncertainty and safe next action. Routine progress goes to activity, not urgent alerts. Notification delivery/acknowledgment does not accept work, grant authority or resume execution. Safety features cannot defer essential alerts until morning briefings ship.

## Non-scope
No unrelated subsystem rewrite, global defaults change, unauthorized external mutation or silent capability fallback. This change does not implement sibling change responsibilities. See design.md for exact boundary and approval gate.

## Outcome
Native notification/activity integration plus delivery-failure/restart/grouping and cross-profile redaction assertions.

## Promotion
Follow `../prd-execution-map/design.md` CI protocol. This change and its round cannot promote on stale/partial/missing checks. Approval of the PRD is not blanket implementation or delivery authorization.
