# Named work profiles and explicit bindings

Status: proposed; discovery/refinement contract only. Implementation gate CLOSED.

**PRD:** ZF-02
**Round:** 1
**Hard prerequisites:** `ci-promotion-gates`

## Scope
Introduce extensible work-profile identity/configuration separate from Local/Synced/Development transport scope. Personal/Priceless/Brown are named work contexts, not hardcoded three-case permissions. Bind direct sessions and assignments to a stable work-profile ID and revision. Existing data must have an explicit migration/binding rule; ambiguous legacy ownership remains read-only/held rather than assigned by guess.

## Non-scope
No unrelated subsystem rewrite, global defaults change, unauthorized external mutation or silent capability fallback. This change does not implement sibling change responsibilities. See design.md for exact boundary and approval gate.

## Outcome
Real two-profile owner/client reads and restart, plus legacy-store fixture migration and denied cross-profile access.

## Promotion
Follow `../prd-execution-map/design.md` CI protocol. This change and its round cannot promote on stale/partial/missing checks. Approval of the PRD is not blanket implementation or delivery authorization.
