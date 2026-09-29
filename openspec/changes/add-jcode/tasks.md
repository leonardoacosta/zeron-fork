# Tasks: Add Jcode ACP

Status: approved by the user on 2026-09-29. Implementation has not started. Complete in order. Task 1.1 is a blocking verification gate, not an implementation task.

- [ ] 1.1 Verify pinned Jcode ACP contract (blocking gate)
  - **Scope:** Read current Jcode documentation and run a bounded, read-only harmless handshake against `v0.88.146-dev (f92c40053)` in a disposable session. Verify invocation and negotiated ACP version, auth/readiness, catalog/model discovery, new/load session behavior, streaming, cancellation, permission requests/responses, and skill-related capabilities. Do not configure MCP or invoke side-effecting tools.
  - **Check:** Record exact commands, outcomes, timeout/cleanup behavior, and verified/unverified capabilities. If handshake or required semantics cannot be verified, stop; revise proposal/design before implementation. No code changes in this task.
  - **Depends on:** None.

- [ ] 2.1 Add stable Jcode identity and preserve compatibility
  - **Scope:** Add Jcode to the existing harness identity/serialization and catalog plumbing only after Task 1.1 passes. Preserve old serialized identities, saved settings, and default behavior. Do not modify provider retirement behavior.
  - **Check:** Focused serialization/catalog tests prove Jcode round-trip and old-value decoding. Migration fixtures for existing settings/chats load unchanged; namesake models for other supported agents remain unaffected.
  - **Depends on:** 1.1 passes.

- [ ] 3.1 Integrate executable detection, authentication, and readiness
  - **Scope:** Implement verified command construction and truthful not-installed, unauthenticated, and ready states using the existing ACP adapter. Do not add a second runner or advertise unverified capabilities.
  - **Check:** Focused harness tests cover installed, missing executable, unauthenticated, handshake failure, and ready states. A harmless disposable real-CLI handshake passes the Task 1.1 contract.
  - **Depends on:** 2.1.

- [ ] 3.2 Integrate verified catalog and model selection
  - **Scope:** Present only catalog/model options confirmed for the pinned Jcode build through existing selection APIs.
  - **Check:** Catalog tests assert verified options are selectable and unknown/unsupported options are not advertised.
  - **Depends on:** 3.1.

- [ ] 4.1 Integrate ACP session lifecycle, streaming, cancellation, and permissions
  - **Scope:** Connect new/load, streamed events, cancellation, and permission decisions through existing ACP lifecycle and authority controls. A failed resume remains failed and never becomes an implicit new session. Do not relax permission policy.
  - **Check:** Focused ACP tests exercise a real harmless Jcode session workflow from creation through streamed response and clean termination; cover load failure without fallback, cancellation outcome, permission allow/deny, and unknown-request non-approval. Verify real-CLI cases only where Task 1.1 established support.
  - **Depends on:** 3.1, 3.2.

- [ ] 5.1 Expose Jcode availability and readiness on desktop and mobile
  - **Scope:** Add Jcode to existing agent selectors/readiness UI on both surfaces, with matching identity and truthful not-installed, unauthenticated, and ready states. Avoid edits owned by sibling proposals except minimal Jcode integration.
  - **Check:** Desktop and mobile UI tests assert Jcode's visible selection/readiness states match harness readiness and cannot select it when unavailable.
  - **Depends on:** 3.1, 4.1.

- [ ] 6.1 Integrate only verified Jcode skill capabilities
  - **Scope:** Reuse existing skill/command integration only where the pinned ACP build verified support. This does not create a dedicated skills viewer.
  - **Check:** Tests cover advertised and absent/unverified skill capability cases and confirm existing behavior for other agents is unchanged.
  - **Depends on:** 4.1.

- [ ] 7.1 Run acceptance checks and review change boundary
  - **Scope:** Run focused harness, engine, desktop, and mobile tests affected by the integration, plus required repository quality checks. Inspect the final diff; do not touch sibling proposal task ledgers.
  - **Check:** A harmless Jcode ACP workflow succeeds on the pinned build; compatibility fixtures pass; desktop/mobile readiness tests pass; diff contains no provider-retirement, dedicated skills-viewer, Omni, or MCP behavior/dependency changes. If the ACP gate fails, do not mark implementation complete.
  - **Depends on:** 5.1, 6.1.
