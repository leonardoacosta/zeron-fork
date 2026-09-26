# Named work profiles and explicit bindings

Status: proposed; discovery/refinement contract only. Implementation gate CLOSED.

**PRD:** ZF-02
**Round:** 3
**Hard prerequisites:** `work-profile-catalog`, `profile-access-enforcement`

## Scope
Bind engine runtime, daemon attachment, direct sessions and assignments to the validated work-profile catalog identity and current authority. Reject wrong/old daemon identity before protected reads. Legacy roots without explicit binding remain inspection-only with no recovery or execution. Do not migrate/copy data here; work-profile-legacy-migration owns that separate protocol.

## Non-scope
No unrelated subsystem rewrite, global defaults change, unauthorized external mutation or silent capability fallback. This change does not implement sibling change responsibilities. See design.md for exact boundary and approval gate.

## Outcome
Two-profile runtime owner/client and exact daemon binding checks; legacy roots held read-only. Import execution belongs to work-profile-legacy-migration.

## Promotion
Follow `../prd-execution-map/design.md` CI protocol. This change and its round cannot promote on stale/partial/missing checks. Approval of the PRD is not blanket implementation or delivery authorization.
