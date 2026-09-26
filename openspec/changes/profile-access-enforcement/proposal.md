# Execution-time profile and resource authorization

Status: proposed; discovery/refinement contract only. Implementation gate CLOSED.

**PRD:** ZF-02, ZF-15, ZF-19
**Round:** 2
**Hard prerequisites:** `work-profile-catalog`

## Scope
Validate work-profile policy at every engine entry point that reads protected content or launches tools: direct sessions, assignment operations, MCP, terminal, repository and credential selection. Bind allowed repositories, account references, tools, environments and action scope explicitly. Revalidate at launch and external-effect boundaries; policy revocation blocks new effects and enters the configured stop/hold path. Never serialize secret values into authority snapshots.

## Non-scope
No unrelated subsystem rewrite, global defaults change, unauthorized external mutation or silent capability fallback. This change does not implement sibling change responsibilities. See design.md for exact boundary and approval gate.

## Outcome
Instrument real engine dispatch boundaries and prove unauthorized paths perform zero protected reads/effects; approved isolated account succeeds.

## Promotion
Follow `../prd-execution-map/design.md` CI protocol. This change and its round cannot promote on stale/partial/missing checks. Approval of the PRD is not blanket implementation or delivery authorization.
