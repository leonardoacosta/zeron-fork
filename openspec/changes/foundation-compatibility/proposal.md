# Preserve direct sessions and two-device baseline

Status: proposed; discovery/refinement contract only. Implementation gate CLOSED.

**PRD:** ZF-01, ZF-03
**Round:** 1
**Hard prerequisites:** `ci-promotion-gates`, `assignment-record`

## Scope
Codify current successful assignment persistence and ordinary-session behavior as regression gates. Preserve explicit null RPC successes, unsupported owner rejection, no local substitutes and no implicit delegation. Keep local private deployment distinct from hosted authentication acceptance. Verify exact installed artifacts rather than version string alone.

## Non-scope
No unrelated subsystem rewrite, global defaults change, unauthorized external mutation or silent capability fallback. This change does not implement sibling change responsibilities. See design.md for exact boundary and approval gate.

## Outcome
Existing native suites plus installed Mac/homelab test evidence reconciled to commit/binary identity; lifecycle caveats explicit.

## Promotion
Follow `../prd-execution-map/design.md` CI protocol. This change and its round cannot promote on stale/partial/missing checks. Approval of the PRD is not blanket implementation or delivery authorization.
