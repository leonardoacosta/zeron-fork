# Explicit isolated engineering comparisons

Status: proposed; discovery/refinement contract only. Implementation gate CLOSED.

**PRD:** ZF-16, ZF-15, ZF-14
**Round:** 8
**Hard prerequisites:** `run-resource-ledger`, `verification-acceptance-gates`, `safe-resume-reconciliation`, `integration-harness-observer-research`

## Scope
Only user-launched comparisons with task, entrants and budget. Freeze identical baseline/input/configuration bindings and isolate each attempt. Report disclosed configurations, cost unknowns, independent correctness results and infrastructure failures separately. Comparison recommends; Leo alone approves routing/default changes. No automatic delivery or winning-run adoption.

## Non-scope
No unrelated subsystem rewrite, global defaults change, unauthorized external mutation or silent capability fallback. This change does not implement sibling change responsibilities. See design.md for exact boundary and approval gate.

## Outcome
Two bounded harmless local entrants on identical baseline, actual isolation tests, independent verifier and no-default-change assertions.

## Promotion
Follow `../prd-execution-map/design.md` CI protocol. This change and its round cannot promote on stale/partial/missing checks. Approval of the PRD is not blanket implementation or delivery authorization.
