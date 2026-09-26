# Assignment record design

## Approved decisions

The engine owns assignment records in its existing profile-scoped SQLite store. Typed RPC routes reads
and mutations to that owner. Session transcripts remain separate, referenced by native IDs.
Persist before acknowledging mutations. Reject stale revisions. Preserve history and recorded permissions
when linking replacement sessions. Creation and promotion never launch work.

Alternatives considered: embedding records in session documents couples objectives to conversations;
registry LWW rows lose the history and transition checks assignments need. Neither is authoritative storage.

## Record and revision boundary

The details below refine the sectional design. Stable mutation identities, immutable owner/profile
bindings, and RPC-only initial exposure were approved with the written specification on
2026-09-26 at 08:29 UTC. They grant no authority for external execution.

An assignment has a stable ID, owning device, immutable profile binding, and monotonically increasing revision.
Its content contains objective, allowed actions, linked sessions, findings, evidence references, reviews,
and unresolved questions. Preserve previous versions instead of overwriting history. Store references and
redacted observations, not credentials or copied unrelated transcripts. A review identifies the version it concerns.
This revision is a record revision, not the later engineering candidate revision model.

For this slice, profile binding means the existing engine store identity and scope. It must not be presented
as completed Personal/Priceless/Brown isolation. References to sessions must resolve within that boundary.
Cross-device links need authoritative profile-membership validation; if unavailable, reject the link rather
than trusting a client-supplied profile label. Remote access to an owner is not assignment ownership transfer.

## Mutation flow

1. Caller addresses the owning device through existing RPC routing and checks the advertised capability.
2. Owner validates input, active profile, referenced session membership, and expected record revision.
3. Owner atomically persists the new revision and durable history before returning success.
4. Caller displays or reads confirmed state. Failed or ambiguous transport replies do not imply success.

Use stable mutation identity for safe retries of record writes: replaying the same identity and payload
returns the original result; conflicting reuse is rejected. This concerns database record effects only,
not exactly-once external execution. Validate bounded input at RPC boundaries using project conventions.
Do not add a generic event bus, scheduler, or replayable execution queue.

## Failure and compatibility behavior

- Stale expected revision: reject without overwriting the winning edit; caller rereads before retry.
- Disk or transaction failure: no success acknowledgment and no partial history/current-state update.
- Owner offline: explicit unavailable result, no substitute local record or execution.
- Missing capability: explicit unsupported result, no fallback to session metadata or an ordinary cwd.
- Invalid or cross-profile reference: reject without leaking another profile's record contents.
- Restart: recover committed records/history; do not launch, resume, or infer permission from their presence.
- Old clients: existing session paths remain usable; absent assignment support does not permit assignment mutation.

Additive schema initialization must preserve existing session snapshots and registry data. A reopened store
must preserve assignments. Downgrade compatibility must be tested or explicitly reported as unsupported,
never assumed. Profile isolation, typed protocol compatibility, and database migration are verification boundaries.

## Verification

Use the existing Rust test framework and temporary stores. Exercise the real engine/RPC/store interfaces,
not a copied implementation. Test creation, explicit promotion, replacement links, history, restart, stale
concurrent edits, failed persistence, duplicate requests, invalid references, remote routing, and old hosts.
Inspect Swift/desktop decoding behavior where shared wire changes could affect them.

Real acceptance requires two devices with an explicitly authorized existing sync setup: remotely create,
restart the owner, retrieve matching committed content/history, and prove no agent launched. If that setup is
unavailable, record acceptance as blocked, not passed. This task does not authorize provisioning or deployment.
Source review, synthetic tests, real interface integration tests, and real two-device results remain separately labeled.
