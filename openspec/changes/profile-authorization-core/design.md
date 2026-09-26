# Owner authorization core

## Existing anchors
- `crates/engine/src/rpc.rs`
- `crates/engine/src/sessions.rs`
- `crates/engine/src/agent_accounts.rs`
- `crates/engine/src/repos.rs`
- `crates/engine/src/terminals.rs`
- `crates/harness/src/lib.rs`
- `crates/engine/tests/local_profiles.rs`

Define owner-derived principal/resource/operation requests, private single-use permits and current policy revision/grants. Persist policy replacement with CAS; synchronous admission is serialized with revocation. This unit exposes no daemon profile selection or full runtime isolation claim.

Core test construction may use owner-resolved fixture bindings. Production integration is in profile-access-enforcement, not a prerequisite to this core gate. Exact durable policy schema, atomic snapshot load, CAS/replay, validated grants and private publication coordinator are now specified in tasks.md. In-memory evaluator alone remains insufficient; implement A+B+C together with the exact narrow lib.rs reexports.

## Rollback
Roll back enforcement code only with execution disabled for newly bound profiles. Never turn unknown policy into allow to preserve compatibility.
