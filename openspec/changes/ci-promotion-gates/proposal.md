# CI admission and round promotion

Status: implemented locally, not promoted. Workflow edits and the structural test are committed at `1631379`; hosted enforcement remains blocked.

**PRD:** ZF-01, ZF-14
**Round:** 0
**Hard prerequisites:** none

## Scope
Extend existing CI, not a separate build system. Every change iteration must pass its declared checks; every integrated round must pass the union of affected checks on one exact commit. Persist requirement-to-check results, platform, toolchain, skipped tests and artifact references in the change tasks. A failed, missing, cancelled or stale required check blocks promotion. Newly discovered prerequisite failures become bounded repair changes, not permanent waivers.

## Non-scope
No unrelated subsystem rewrite, global defaults change, unauthorized external mutation or silent capability fallback. This change does not implement sibling change responsibilities. See design.md for exact boundary and approval gate.

## Outcome
Run documented quality/test commands locally without release or deployment. Hosted enforcement acceptance additionally needs authorized repository ruleset configuration and a disposable failing PR; those are external mutations and remain separately blocked until explicitly authorized. Do not claim the local plan tests prove merge protection. Recorded 2026-09-29: the active ruleset on `zeronsh/zeron` has no required status checks, and this account cannot change it (pull-only access).

## Promotion
Follow `../prd-execution-map/design.md` CI protocol. This change and its round cannot promote on stale/partial/missing checks. Approval of the PRD is not blanket implementation or delivery authorization.
