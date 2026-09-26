# Assignment record tasks

Status: pending written-specification review. These tasks are not implementation authorization.
Run through `apply` only after approval of this named change. No external mutation, deployment, or spend.

- [ ] 1. Confirm baseline and define failing contract tests. Recheck repository instructions and current source,
  inspect DocsStore ownership, profile identity, RPC forwarding, capability decoding, and session lookup.
  Add tests for the spec scenarios before behavior implementation. Freeze concrete DTO names and input limits
  using existing conventions. Do not weaken approved invariants to fit old protocol behavior.
- [ ] 2. Implement profile-store assignment persistence. Depends on 1. Add minimal additive schema/storage methods
  beside existing SQLite ownership, atomic revision/history writes, stale-write checks and mutation replay handling.
  Test new/existing-store initialization, reopen durability, rollback, concurrent writes, duplicate identity and
  conflicting identity reuse. Preserve snapshots and registry state. Do not expose the raw connection publicly.
- [ ] 3. Implement engine validation and typed owner-routed RPC. Depends on 2. Add explicit create/promote,
  read/history and revision-checked record updates. Validate membership and payloads, retain native session IDs,
  preserve permission records on replacement, and advertise additive capability. Test unavailable owners,
  unsupported hosts, invalid/cross-profile references, and rejection without information leakage.
- [ ] 4. Run regression and integration gates. Depends on 3. Run `cargo fmt --all -- --check`,
  `cargo test --locked -p zeron-proto`, `cargo test --locked -p zeron-sync --lib`,
  `cargo test --locked -p zeron-rpc`, and relevant new engine tests plus
  `cargo test --locked -p zeron-engine --lib --test local_profiles --test restart_resume --test session_publication`.
  Confirm actual test target names before execution. Cover direct sessions, no implicit assignment creation,
  no agent launch, lost replies and owner restart through real interfaces. Record failures or unavailable build
  dependencies honestly. Run native client checks if shared decoding changes affect those clients.
- [ ] 5. Perform real two-device acceptance. Depends on 4 and an existing explicitly authorized test setup.
  Create remotely, restart owner, retrieve record/history, verify profile rejection and no launched agent.
  Record exact build, environment, observations and limitations without credentials. If unavailable, report
  blocked acceptance. Do not provision, deploy, sign in elsewhere, or substitute synthetic evidence.
- [ ] 6. Review and close only with accurate evidence. Depends on 4–5. Compare every spec scenario to results,
  label source/synthetic/integration/real-workflow evidence, document compatibility limits, and preserve unresolved
  acceptance blockers. Commit only this change's files. No push or downstream feature execution is authorized.
