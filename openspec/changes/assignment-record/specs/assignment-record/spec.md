# Assignment records

## ADDED Requirements

### Requirement: Explicit persistent objective
The system SHALL create assignments only through an explicit create or promote operation, recording objective,
profile, allowed actions, linked sessions, findings, evidence references, reviews, and unresolved questions.

#### Scenario: Create without execution
- **WHEN** a valid create request succeeds
- **THEN** the record is committed before acknowledgment and no agent or external action starts.

#### Scenario: Promote an existing session
- **WHEN** the user explicitly promotes a valid session in the active profile
- **THEN** the assignment links that session without rewriting its transcript or changing its direct-session behavior.

### Requirement: Owner and profile boundaries
The owning engine SHALL validate every assignment operation against its active profile store and reject
invalid session links. Client labels, device connectivity, and authentication SHALL NOT create workflow authority.

#### Scenario: Foreign session reference
- **WHEN** an operation references a session outside the assignment profile or membership cannot be established
- **THEN** the engine rejects the operation without exposing foreign content or modifying the record.

#### Scenario: Remote owner unavailable
- **WHEN** the selected owning device is unavailable
- **THEN** the request reports unavailability without creating a local substitute or executing work.

### Requirement: Revision history and safe writes
The system SHALL preserve committed assignment versions and reject writes against stale revisions.
Current content and history SHALL commit atomically. Repeated identical mutation identities SHALL NOT create
duplicate assignments or revisions, and conflicting identity reuse SHALL be rejected.

#### Scenario: Concurrent edits
- **WHEN** two edits name the same expected revision and one commits
- **THEN** the other is rejected as stale and the committed history remains intact.

#### Scenario: Lost acknowledgment
- **WHEN** a committed mutation is retried with the same identity and payload after a lost reply
- **THEN** the owner returns its original result without a second mutation.

#### Scenario: Failed persistence
- **WHEN** persistence fails before commit
- **THEN** no success is returned and neither partial record content nor partial history becomes committed.

#### Scenario: Restart
- **WHEN** the owner restarts after an acknowledged write
- **THEN** the same committed record and history are retrievable without launching or resuming work.

### Requirement: Agent replacement preserves the objective
The system SHALL represent a replacement agent by linking its session without deleting prior links,
findings, evidence, questions, reviews, or recorded allowed actions.

#### Scenario: Link replacement
- **WHEN** a valid replacement session is linked
- **THEN** prior history remains available and allowed actions do not expand as a side effect.

### Requirement: Evidence is not acceptance
The system SHALL retain evidence and revision-specific reviews without inferring verification, acceptance,
delivery, or confirmed outcomes from record presence, agent completion, or a linked artifact.

#### Scenario: Findings recorded
- **WHEN** findings and an evidence reference are added
- **THEN** they are retrievable with their record version and no execution or automatic acceptance occurs.

### Requirement: Additive protocol and unchanged sessions
Assignment access SHALL use typed owner-routed RPC with explicit capability support. Unsupported hosts SHALL
fail explicitly. Existing direct sessions SHALL remain usable without assignment administration.

#### Scenario: Old host
- **WHEN** the target does not advertise assignment support
- **THEN** assignment access reports unsupported without silently substituting session metadata or another owner.

#### Scenario: Ordinary session
- **WHEN** a user opens or uses a session without promoting it
- **THEN** no assignment is required or implicitly created.

#### Scenario: Two-device acceptance
- **WHEN** a second authorized device creates an assignment on the owner, the owner restarts, and the second device reads it
- **THEN** the committed content and history match, the owner remains unchanged, and no agent execution occurred.
