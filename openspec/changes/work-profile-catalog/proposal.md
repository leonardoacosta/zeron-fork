# Validated profile identity and owner catalog

Status: proposed; Implementation gate CLOSED pending named review/approval.

**PRD:** ZF-02
**Round:** 1
**Hard prerequisites:** `ci-promotion-gates`

## Scope
Define validated opaque profile identity, display metadata and revision types plus owner-local principal-scoped catalog persistence. Create/rename use atomic per-profile CAS and actor/principal-scoped exact replay receipts. This foundation provides no runtime authority, no daemon attachment, no sync namespace, and no legacy execution permission.

## Acceptance
Exact proto/catalog production tests plus real SQLite concurrent CAS, trigger rollback/reopen, poison/future-schema negatives. No runtime isolation claim.

## Non-scope
No sibling runtime/provider behavior, external access or silent authority expansion.
