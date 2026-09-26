# Versioned outputs and evidence provenance

Status: proposed; discovery/refinement contract only. Implementation gate CLOSED.

**PRD:** ZF-14, ZF-03
**Round:** 2
**Hard prerequisites:** `work-profile-catalog`, `assignment-record`

## Scope
Introduce immutable output/candidate identities bound to exact assignment revision, source revision and dirty-tree content, frozen input/configuration/authorization/resource bindings, environment and native sessions. Evidence records check command, observations, outcome, limitations, timestamps and redacted artifacts. Separate structural, synthetic and real-workflow evidence. Editing inputs creates a new binding; it does not transfer approval.

## Non-scope
No unrelated subsystem rewrite, global defaults change, unauthorized external mutation or silent capability fallback. This change does not implement sibling change responsibilities. See design.md for exact boundary and approval gate.

## Outcome
Real create/edit/restart/read workflow proving stale invalidation and exact evidence retrieval, with synthetic fixtures separately tagged.

## Promotion
Follow `../prd-execution-map/design.md` CI protocol. This change and its round cannot promote on stale/partial/missing checks. Approval of the PRD is not blanket implementation or delivery authorization.
