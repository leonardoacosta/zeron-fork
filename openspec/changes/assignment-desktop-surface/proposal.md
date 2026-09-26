# Desktop assignment and intervention surface

Status: proposed; discovery/refinement contract only. Implementation gate CLOSED.

**PRD:** ZF-01, ZF-02, ZF-03, ZF-04, ZF-05, ZF-06, ZF-14, ZF-18
**Round:** 6
**Hard prerequisites:** `manual-investigation-runner`

## Scope
Add explicit create/promote/read/history/launch controls alongside direct sessions. Before launch show profile, selected workflow/version/reason, permissions, resources and unavailable capabilities. Show stopping versus confirmed stop, takeover/handback, evidence class and blocked reasons. UI location must be reviewed using existing navigation conventions before implementation; preserve keyboard and screen-reader operation.

## Non-scope
No unrelated subsystem rewrite, global defaults change, unauthorized external mutation or silent capability fallback. This change does not implement sibling change responsibilities. See design.md for exact boundary and approval gate.

## Outcome
Native GPUI workflow with actual owner/client, keyboard/focus/accessibility checks and zero implicit assignments.

## Promotion
Follow `../prd-execution-map/design.md` CI protocol. This change and its round cannot promote on stale/partial/missing checks. Approval of the PRD is not blanket implementation or delivery authorization.
