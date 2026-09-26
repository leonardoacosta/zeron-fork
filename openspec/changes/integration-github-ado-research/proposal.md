# GitHub, ADO, MCP and Aperture boundary research

Status: proposed; discovery/refinement contract only. Implementation gate CLOSED.

**PRD:** ZF-19, ZF-07
**Round:** 1
**Hard prerequisites:** `ci-promotion-gates`

## Scope
Map current GitHub read/status and MCP behavior; verify exact ADO and Tailscale Aperture identities, versions, APIs and authority boundaries. Record external planning/review/specification systems as authoritative. Determine remote-only repository support separately from local storage convenience. Produce independently scoped adapter follow-ups per verified system, never a blanket integration permission.

## Non-scope
No unrelated subsystem rewrite, global defaults change, unauthorized external mutation or silent capability fallback. This change does not implement sibling change responsibilities. See design.md for exact boundary and approval gate.

## Outcome
Exact provider/version capability matrix and authoritative-source mapping; write probes await named sandbox authorization.

## Promotion
Follow `../prd-execution-map/design.md` CI protocol. This change and its round cannot promote on stale/partial/missing checks. Approval of the PRD is not blanket implementation or delivery authorization.
