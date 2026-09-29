# Add Jcode as a first-class ACP agent

Status: proposed; approval pending. Implementation must not start until this change is approved and the Jcode verification gate passes.

## Why

Users need Jcode available as a first-class coding agent without creating a second agent transport or claiming ACP behavior that has not been verified. The existing ACP path is the intended integration point, but the installed CLI help alone does not establish wire compatibility.

## What Changes

- Add a stable Jcode harness identity through the existing ACP transport.
- Expose truthful executable, authentication, readiness, catalog/model, session, streaming, cancellation, permission, skill-integration, desktop, and mobile behavior, limited to verified capabilities.
- Preserve existing serialized identities, settings, and behavior for other agents.
- Make ACP protocol verification a blocking gate before implementation.

Provider retirement, dedicated skill browsing, and Omni integration/metrics are independently owned sibling proposals. Coordinate at shared surfaces without hard dependencies or claiming ownership here.

## Impact

- **Compatibility:** Existing provider identities and persisted records must continue to decode; no existing agent defaults or skill completion behavior may regress.
- **Interfaces:** Adds Jcode to existing harness selection/readiness surfaces on desktop and mobile. It adds no second transport or new MCP interface.
- **Dependencies:** No new dependency. MCP behavior and dependencies remain untouched.
- **Risk boundary:** The local `jcode acp --help` evidence is insufficient to assert protocol behavior. Unsupported or unverified Jcode remains unavailable.

## Approval and sequencing

This proposal is not approval to implement. First complete the read-only ACP capability verification task. Stop and return for design refinement if the installed/pinned Jcode cannot establish the required handshake, authentication, lifecycle, cancellation, and permission semantics. Only then implement the dependent Jcode work. Sibling proposals remain independently owned, with coordination at shared surfaces and no hard dependency.
