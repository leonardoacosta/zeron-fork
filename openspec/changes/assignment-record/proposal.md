# Persistent assignment records

Status: written specification approved by the user on 2026-09-26 at 08:29 UTC. Execution authorized for this change only.

Execution owner: Jcode coordinator with sole code implementation worker
`session_calf_1790411391294_fb7a07dbe0864861`. Other roadmap changes and external actions remain unauthorized.

## Why

ZF-03 needs delegated objectives to outlive individual agents and sessions. Start with a durable record,
not an executor. This is the first bounded feature in the investigation-first roadmap.

## Scope

- Explicit creation or promotion of an existing session into an assignment.
- Objective, profile binding, recorded allowed actions, linked native sessions, findings, evidence references,
  reviews, and unresolved questions, with preserved revision history.
- Owning-engine validation, profile-scoped SQLite persistence, typed RPC, stale-write rejection,
  and remote access through the existing owning-device transport.
- Agent replacement represented by an additional linked session, preserving prior links and permissions.
- Additive capability negotiation and unchanged direct-session behavior.

Recorded allowed actions describe the assignment boundary. They do not authorize execution in this change.
Evidence and review records do not automatically establish correctness or acceptance.

## Non-scope

No agent launch, cancellation, resumption, workflow executor, delivery, automatic acceptance, full named-profile
isolation, conflict scheduler, browser integration, trigger, comparison, or multi-repository orchestration.
No desktop/iOS navigation redesign. The first interface is typed RPC; user-facing placement is a separate change.
No replication of authoritative assignment history through registry LWW rows, owner migration, or offline edits.

## Preconditions for later execution

Investigations cannot launch until profile/access enforcement, harness preflight, confirmed stopping,
and safe recovery have passed their own acceptance gates. A stored assignment is not evidence those gates exist.

## Impact

Expected surfaces: `crates/proto`, `crates/sync/src/store.rs`, `crates/engine`, `crates/rpc` and native tests.
Keep storage mechanics beside the existing SQLite owner and domain validation in the engine.
Do not expose raw SQL connections across crates or add a new service/dependency for this feature.

Acceptance is defined in [the capability specification](specs/assignment-record/spec.md).
Architecture is in [design.md](design.md). Execution work exists only in [tasks.md](tasks.md).
