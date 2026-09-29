# Design: retired harness compatibility

## Decision

Treat retirement as removal from the supported harness lifecycle, not deletion of the historical identity. The serialized identity remains decodable for persisted sessions, while new selection and execution paths no longer advertise or launch it.

## Compatibility behavior

- Keep legacy string decoding for `devin`, `grok`, and `antigravity` where persisted data needs it. Decoding alone does not make an ID launchable.
- Historical session rendering must not require a live harness executable or catalog entry.
- Resume must fail at the harness boundary with an unavailable/retired error that names the selected harness and gives a next step (choose a supported agent for a new session). No fallback launch or implicit ID rewrite.
- Do not remove, migrate, or overwrite provider credential material. Auth screens and status should no longer present these providers as supported actions.

## Surface and dependency boundary

Inventory every consumer of the harness identity before removing executable behavior: protocol serialization, engine session creation/resume, provider catalog and account/auth surfaces, install/readiness code, desktop and mobile pickers/settings, and user-facing docs. Remove only the retired harness support. A model ID is not a harness ID; preserve it when another supported harness exposes it.

This change does not absorb the open provider-adapter discovery contract or authorize its implementation. Resolve collisions with in-flight prerequisite work through review before implementation rather than silently taking over its tasks. Approval applies only to this retirement boundary.

## Risks and mitigations

- **Old sessions stop rendering:** retain legacy decode and test persisted-session rendering without the retired executable.
- **Resume silently switches agent:** assert explicit error and absence of a start request to any replacement harness.
- **Credential loss:** assert retirement paths perform no credential delete/sign-out operation and preserve fixture bytes.
- **Over-broad model deletion:** test a related model through a different supported harness and scope catalog filtering to harness identity.
- **Platform mismatch:** cover desktop and mobile lists and their action handlers, not only shared catalog code.

## Unresolved implementation evidence

The exploration note did not enumerate all call sites or establish exact mobile test names. Implementation must discover those surfaces and pin focused tests before deleting support. No runtime integration or execution approval is implied by this design.
