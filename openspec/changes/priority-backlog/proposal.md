# Priority, blockers and non-preemptive urgent work

Status: proposed; discovery/refinement contract only. Implementation gate CLOSED.

**PRD:** ZF-10, ZF-09
**Round:** 7
**Hard prerequisites:** `conflict-admission-observer`, `confirmed-stop-handoff`

## Scope
Queue conflicted proposals with blocker type/reason and explicit priority. Among eligible work sort priority then oldest admission; Leo override recorded. Observer recommendations never silently change priority. Reassess on blocker resolution. Urgent conflicting work waits unless Leo explicitly requests interruption and actual stop is confirmed. Dependency-wait and conflict-wait are different states.

## Non-scope
No unrelated subsystem rewrite, global defaults change, unauthorized external mutation or silent capability fallback. This change does not implement sibling change responsibilities. See design.md for exact boundary and approval gate.

## Outcome
Concurrent queue/restart integration and actual-stop boundary with direct sessions included.

## Promotion
Follow `../prd-execution-map/design.md` CI protocol. This change and its round cannot promote on stale/partial/missing checks. Approval of the PRD is not blanket implementation or delivery authorization.
