# Remove retired agent providers

Status: approved by the user on 2026-09-29 at 22:38:57 UTC. Implementation has not started.

## Why

Devin, Grok, and Antigravity remain selectable or discoverable as supported coding-agent harnesses. Retiring their harness support must not make existing conversations unreadable, erase credentials, or prevent a model with a similar name from being used through a different agent.

## Outcome

Remove Devin, Grok, and Antigravity from supported launch, installation, authentication, readiness, and provider-catalog surfaces. Keep legacy serialized identities readable and report an actionable unavailable-provider error when a user tries to resume one. Preserve stored credentials and unrelated model access.

## What Changes

- Remove the three harnesses from new-session selection, supported-provider catalogs, executable/install flows, login/logout/auth status, readiness checks, and platform-specific provider surfaces.
- Preserve decoding and display of historical conversations carrying their existing serialized harness identifiers. Do not rewrite persisted records.
- Reject attempts to resume a retired harness explicitly. Never silently substitute another harness.
- Leave credentials untouched. Do not treat retirement as sign-out or credential cleanup.
- Audit desktop and mobile entry points, docs, and tests for supported-provider claims and choices.
- Distinguish harness retirement from model availability: models exposed by another supported agent remain available there.

## Impact

Affected capability: provider-retirement. Expected surfaces include harness identity decoding, engine execution guards, provider catalogs and setup, desktop/mobile controls, and compatibility tests. No credential deletion, document rewrite, or new runtime dependency.

## Out of scope

Adding Jcode as a harness, adding a skill viewer, all MCP work (explicitly skipped), gateway/model metrics, deleting credentials, migrating historical records, and unrelated provider-adapter work. User approval authorizes this bounded scope subject to its prerequisite tasks. Existing prerequisite changes and their approval gates remain independent; do not import unrelated roadmap gates into this bounded change.

## Acceptance

1. Neither retired provider appears in any supported launch, install, auth, readiness, or catalog choice on desktop or mobile.
2. A stored conversation using a retired ID loads and displays its history without changing the stored ID.
3. Resuming such a conversation returns a clear retired/unavailable error and does not start a different agent.
4. Existing credential files remain unchanged by enumeration, selection, and failed resume.
5. A same-named or related model remains selectable through any other supported harness that provides it.
6. Focused regression tests and repository-required Rust formatting/Clippy checks pass.

## Approval boundary

User approval is recorded above. Existing prerequisite and verification gates remain in force. Approval authorizes only this proposal's scope, not the neighboring integrations in the exploration note.
