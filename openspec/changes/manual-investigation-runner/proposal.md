# Manual bounded investigation workflow

Status: proposed; discovery/refinement contract only. Implementation gate CLOSED.

**PRD:** ZF-03, ZF-05, ZF-06, ZF-08
**Round:** 5
**Hard prerequisites:** `safe-resume-reconciliation`, `verification-acceptance-gates`, `run-resource-ledger`, `work-profile-boundary`

## Scope
Explicitly launch one configured investigation for an assignment after profile/preflight/resource/selection gates. Bind native session IDs and observations; findings can be the terminal output. Preserve objective and permissions through replacement, with stop proof for affected old execution. Keep direct sessions runnable without implicit assignments. No coding/delivery authorization inferred from investigation.

## Non-scope
No unrelated subsystem rewrite, global defaults change, unauthorized external mutation or silent capability fallback. This change does not implement sibling change responsibilities. See design.md for exact boundary and approval gate.

## Outcome
First real end-to-end investigation on harmless local repository: launch, stop, replace, restart, accepted findings; bounded authorized harness budget.

## Promotion
Follow `../prd-execution-map/design.md` CI protocol. This change and its round cannot promote on stale/partial/missing checks. Approval of the PRD is not blanket implementation or delivery authorization.
