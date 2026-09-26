# Capability preflight and frozen run configuration

Status: proposed; discovery/refinement contract only. Implementation gate CLOSED.

**PRD:** ZF-15, ZF-02
**Round:** 2
**Hard prerequisites:** `work-profile-boundary`

## Scope
Produce comparable per-harness capability results with supported/unsupported/unknown distinctions and observed version. Freeze requested harness/model/account reference/environment/sandbox/resource configuration for a run. Inspect actual adapter behavior, especially Codex sandbox overrides and Claude/ACP auto-approval, before claiming enforcement. Unsupported requested isolation blocks dispatch. Configuration changes require explicit new run binding.

## Non-scope
No unrelated subsystem rewrite, global defaults change, unauthorized external mutation or silent capability fallback. This change does not implement sibling change responsibilities. See design.md for exact boundary and approval gate.

## Outcome
Adapter argument/protocol tests plus one authorized native harness preflight; token-spending execution requires separate bounded budget.

## Promotion
Follow `../prd-execution-map/design.md` CI protocol. This change and its round cannot promote on stale/partial/missing checks. Approval of the PRD is not blanket implementation or delivery authorization.
