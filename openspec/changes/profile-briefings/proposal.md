# Profile-configurable routine briefings

Status: proposed; discovery/refinement contract only. Implementation gate CLOSED.

**PRD:** ZF-18
**Round:** 8
**Hard prerequisites:** `exception-attention`, `workflow-version-selection`

## Scope
Provide morning/routine briefing schedule and destinations per profile with explicit configuration. Summarize progress, blockers, uncertainty and accepted/delivered/outcome states distinctly. Delivery provider/channel selection must be recorded before adapter implementation. Missed schedule, timezone/DST and duplicate delivery are explicit policies; no guessed universal morning time.

## Non-scope
No unrelated subsystem rewrite, global defaults change, unauthorized external mutation or silent capability fallback. This change does not implement sibling change responsibilities. See design.md for exact boundary and approval gate.

## Outcome
Deterministic clock/scheduler tests plus actual authorized local notification destination; external email/chat destination separately authorized.

## Promotion
Follow `../prd-execution-map/design.md` CI protocol. This change and its round cannot promote on stale/partial/missing checks. Approval of the PRD is not blanket implementation or delivery authorization.
