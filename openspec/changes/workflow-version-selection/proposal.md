# Versioned workflow definitions and selection

Status: proposed; discovery/refinement contract only. Implementation gate CLOSED.

**PRD:** ZF-05, ZF-06
**Round:** 3
**Hard prerequisites:** `revision-evidence-bindings`, `work-profile-catalog`

## Scope
Define independently versioned workflows with stages, agent choices, checks, failure policy, gates and autonomy. Ship the PRD starting sequence without forcing investigation-only work to produce code. Select explicit assignment override, else repository default, else profile default; if none exists hold with a clear configuration error. Persist selected version and explanation before launch. Suggestions create optional updates; active definitions never mutate silently.

## Non-scope
No unrelated subsystem rewrite, global defaults change, unauthorized external mutation or silent capability fallback. This change does not implement sibling change responsibilities. See design.md for exact boundary and approval gate.

## Outcome
Precedence, version pinning, invalid override and restart tests through owner RPC; UI explanation delivered by presentation changes.

## Promotion
Follow `../prd-execution-map/design.md` CI protocol. This change and its round cannot promote on stale/partial/missing checks. Approval of the PRD is not blanket implementation or delivery authorization.
