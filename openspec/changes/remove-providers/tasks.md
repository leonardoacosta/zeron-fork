# Tasks: Remove retired providers

Status: approval pending. Do not start implementation tasks until explicit approval. Each task is limited to the retirement scope in proposal.md.

- [ ] **T1. Inventory retired-provider lifecycle and test anchors**
  - Depends on: none
  - Scope: Trace Devin, Grok, and Antigravity IDs through serialization, new-session selection, catalogs, launch/install/readiness, auth/account flows, session resume, desktop/mobile UI, docs, and tests. Separate harness IDs from model IDs. Identify overlaps with active changes, especially `integration-provider-adapters`, and record the exact focused test commands/files before editing.
  - Verify: Inventory accounts for every consumer and both platforms; confirms legacy decode/display and credential storage boundaries; lists concrete tests and any ownership conflict for review. No code changes in this task.

- [ ] **T2. Remove retired providers from supported actions and choices**
  - Depends on: T1
  - Scope: Remove only the three harnesses from new-session/provider catalogs and supported install, auth, readiness, launch, desktop, mobile, and documentation surfaces. Preserve unrelated provider and model offerings.
  - Verify: Focused catalog/UI/auth/install tests show all three absent on desktop and mobile; direct RPC and queued-new-session tests reject each retired ID before spawn/install/auth side effects; regression test confirms a related model remains available through another supported harness.

- [ ] **T3. Preserve legacy history and reject retired resume**
  - Depends on: T1
  - Scope: Keep legacy persisted-ID decoding and history rendering. Reject new, resumed, direct-RPC, stale-client, and queued execution at the engine boundary before spawn/install/auth with a clear retired/unavailable message and no fallback harness selection. Do not rewrite session records.
  - Verify: Focused serialization and engine/session tests open historical fixtures without the provider executable, retain the stored ID, and assert retired new/resume/direct-RPC/queued requests issue no spawn, install, authentication, or replacement launch.

- [ ] **T4. Prove credentials are untouched and run bounded regression suite**
  - Depends on: T2, T3
  - Scope: Add or update regression coverage for credential preservation across provider listing, setup/auth surfaces, and failed resume; complete cross-platform and docs audit within this proposal.
  - Verify: Credential fixture bytes and auth state remain unchanged; run focused tests identified in T1, workspace Rust formatting and Clippy commands from README, and applicable desktop/mobile checks. Report each command/result and any unavailable platform runner. Fix failures within scope and rerun.

## Completion boundary

All scenarios in `specs/provider-retirement/spec.md` need a mapped verification result. Do not add Jcode, skills, MCP, metrics, unrelated roadmap gates, or implementation tasks for neighboring proposals. Completion does not imply GitHub Actions passed unless that workflow ran.
