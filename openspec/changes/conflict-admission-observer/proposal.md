# Conflict admission for assignments and direct sessions

Status: proposed; discovery/refinement contract only. Implementation gate CLOSED.

**PRD:** ZF-09, ZF-02, ZF-18
**Round:** 6
**Hard prerequisites:** `manual-investigation-runner`, `revision-evidence-bindings`

## Scope
At proposal admission inspect overlapping changes, incompatible assumptions, shared resources and unmet dependencies. Include direct sessions without converting them into assignments. Represent limited outside-Zeron visibility. Different files can conflict; independent work proceeds. Recheck scope changes and shared-action boundaries. Uncertain conflicts require another reviewer; unresolved uncertainty holds affected work and alerts. System One is observer, not execution authority; unverified adapter can only return unknown.

## Non-scope
No unrelated subsystem rewrite, global defaults change, unauthorized external mutation or silent capability fallback. This change does not implement sibling change responsibilities. See design.md for exact boundary and approval gate.

## Outcome
Concurrent direct-session plus assignment admission with resource conflicts, unknown observer and changed-scope checks; provider-specific SystemOne evidence separately required.

## Promotion
Follow `../prd-execution-map/design.md` CI protocol. This change and its round cannot promote on stale/partial/missing checks. Approval of the PRD is not blanket implementation or delivery authorization.
