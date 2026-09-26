# Explicit non-destructive work-profile migration

Status: proposed; Implementation gate CLOSED pending named review/approval.

**PRD:** ZF-02
**Round:** 5
**Hard prerequisites:** `work-profile-boundary`, `safe-resume-reconciliation`

## Scope
Migrate only explicitly selected legacy source to a new named-profile target with verified identity, non-destructive staged copy, content manifest and atomic publication. Preserve original data; no credentials copied. Interrupted or ambiguous migration remains non-executable. Imported runs require safe resume authorization, never automatic journal replay.

## Acceptance
Real isolated old-store fixtures with source digest drift, partial-copy fault, target collision, atomic publish/reopen and zero harness starts.

## Non-scope
No sibling runtime/provider behavior, external access or silent authority expansion.
