# CI admission and round promotion

Status: proposed; discovery/refinement contract only. Implementation gate CLOSED.

**PRD:** ZF-01, ZF-14
**Round:** 0
**Hard prerequisites:** none

## Scope
Extend existing CI, not a separate build system. Every change iteration must pass its declared checks; every integrated round must pass the union of affected checks on one exact commit. Persist requirement-to-check results, platform, toolchain, skipped tests and artifact references in the change tasks. A failed, missing, cancelled or stale required check blocks promotion. Newly discovered prerequisite failures become bounded repair changes, not permanent waivers.

## Non-scope
No unrelated subsystem rewrite, global defaults change, unauthorized external mutation or silent capability fallback. This change does not implement sibling change responsibilities. See design.md for exact boundary and approval gate.

## Outcome
Run documented quality/test commands and demonstrate an intentionally failing disposable branch cannot promote; no real release or hosted mutation is needed.

## Promotion
Follow `../prd-execution-map/design.md` CI protocol. This change and its round cannot promote on stale/partial/missing checks. Approval of the PRD is not blanket implementation or delivery authorization.
