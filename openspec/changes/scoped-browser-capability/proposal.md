# Isolated browser sessions and explicit signed-in scope

Status: proposed; discovery/refinement contract only. Implementation gate CLOSED.

**PRD:** ZF-17, ZF-02, ZF-04, ZF-14
**Round:** 7
**Hard prerequisites:** `profile-access-enforcement`, `confirmed-stop-handoff`, `revision-evidence-bindings`, `integration-browser-research`

## Scope
Browser sessions isolated by default, bound to work profile plus assignment or direct session. Signed-in session reuse is explicit and scope-limited. Browser authentication grants no mutation authority; actions use workflow/profile gates. Redact secrets and unrelated content from evidence. Do not switch browser/account/provider on failure. Integrate only provider selected by research decision.

## Non-scope
No unrelated subsystem rewrite, global defaults change, unauthorized external mutation or silent capability fallback. This change does not implement sibling change responsibilities. See design.md for exact boundary and approval gate.

## Outcome
Actual chosen provider with two isolated browser profiles and harmless local authenticated fixture; external mutation needs separate scoped authorization.

## Promotion
Follow `../prd-execution-map/design.md` CI protocol. This change and its round cannot promote on stale/partial/missing checks. Approval of the PRD is not blanket implementation or delivery authorization.
