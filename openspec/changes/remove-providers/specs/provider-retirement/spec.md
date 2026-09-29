## ADDED Requirements

### Requirement: Retired providers are not offered for new work
The application MUST NOT present Devin, Grok, or Antigravity as supported options for creating a session, installing a harness, authenticating, checking readiness, or selecting a provider on any supported desktop or mobile surface.

#### Scenario: User opens a provider picker
- **WHEN** the user opens any new-session or provider selection surface
- **THEN** Devin, Grok, and Antigravity are absent
- **AND** supported providers remain selectable

#### Scenario: User opens provider setup or authentication
- **WHEN** the user views installation, sign-in, sign-out, or readiness actions
- **THEN** no supported action is offered for Devin, Grok, or Antigravity
- **AND** existing credential material is not deleted or changed by viewing those surfaces

#### Scenario: Related model is supplied by another harness
- **WHEN** a supported harness exposes a model whose name is also associated with a retired provider
- **THEN** that model remains available through the supported harness
- **AND** retirement filtering applies to harness identity, not the model name

#### Scenario: Stale client or queued request names a retired provider
- **WHEN** a stale client sends a direct RPC request or a queued new-session request using Devin, Grok, or Antigravity
- **THEN** the request is rejected as an unavailable/retired provider before any process spawn, installation, or authentication side effect
- **AND** no alternate harness is selected implicitly

### Requirement: Historical retired-provider sessions remain readable
The application MUST decode and render historical sessions that store a retired provider identity without rewriting the identity or requiring its executable.

#### Scenario: Open a historical session
- **WHEN** a user opens a stored conversation whose harness ID is Devin, Grok, or Antigravity
- **THEN** the application displays its stored history
- **AND** the persisted harness ID remains unchanged

#### Scenario: Resume a historical session
- **WHEN** a user attempts to resume a session assigned to a retired provider
- **THEN** the operation fails with a clear unavailable/retired-provider explanation and a supported next step
- **AND** the application does not launch or silently substitute another harness

#### Scenario: Retired provider credentials exist
- **WHEN** provider retirement code enumerates providers or rejects a resume
- **THEN** it does not delete, overwrite, or revoke existing credentials

## Verification anchors

Focused verification MUST cover serialized legacy decode, rendering without an installed executable, explicit resume failure with no substitute launch, desktop and mobile provider/setup/auth surfaces, credential preservation, and related model availability through another harness. Exact existing test names must be identified during implementation inventory; do not invent tests or claim coverage before they run.
