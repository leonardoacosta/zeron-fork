# Jcode, Herdr and observer capability research

Status: proposed; discovery/refinement contract only. Implementation gate CLOSED.

**PRD:** ZF-15, ZF-09, ZF-19
**Round:** 1
**Hard prerequisites:** `ci-promotion-gates`

## Scope
Produce versioned evidence for Jcode environment-local swarm integration and Herdr attachment, and separately SystemOne observer, Jev, Laya and empryo identity/capabilities. Identify native IDs, start/stop proof, status, configuration, usage and isolation contracts. Unknown products/APIs remain unknown and cannot become executable adapters. Keep SystemOne distinct from engineering harness.

## Non-scope
No unrelated subsystem rewrite, global defaults change, unauthorized external mutation or silent capability fallback. This change does not implement sibling change responsibilities. See design.md for exact boundary and approval gate.

## Outcome
Pinned official source/API references plus read-only local version/capability probes when authorized; output exact adapter contracts or explicit blocked decisions.

## Promotion
Follow `../prd-execution-map/design.md` CI protocol. This change and its round cannot promote on stale/partial/missing checks. Approval of the PRD is not blanket implementation or delivery authorization.
