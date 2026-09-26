# Owner policy and synchronous admission core

Status: proposed; Implementation gate CLOSED pending review.

**PRD:** ZF-02, ZF-15, ZF-19
**Round:** 2
**Hard prerequisites:** `work-profile-catalog`

## Scope
Define owner-derived principal/resource/operation requests, private single-use permits and current policy revision/grants. Persist policy replacement with CAS; synchronous admission is serialized with revocation. This unit exposes no daemon profile selection or full runtime isolation claim.

## Acceptance
Exact core tests plus durable policy/CAS tests. No actual engine/harness/terminal enforcement claim.
