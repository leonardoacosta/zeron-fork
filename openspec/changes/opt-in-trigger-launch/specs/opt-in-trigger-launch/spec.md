# Provenance-bound automatic triggers

## ADDED Requirements

### Requirement: Bounded provenance-bound automatic triggers
The system SHALL satisfy the following behavior for ZF-08, ZF-06, ZF-09, ZF-10:

Add opt-in event triggers with provenance, explicit workflow binding and stable event identity. A trigger prepares approval or launches only within configured authority/profile/resources/admission. Duplicate/reordered events do not duplicate launch. Manual launch remains available. No comparisons may be triggered automatically.

#### Scenario: C01
- **GIVEN / WHEN / THEN** Same event delivered after restart yields one prepared/run identity.

#### Scenario: C02
- **GIVEN / WHEN / THEN** Trigger names missing workflow version: hold, do not infer current default.

#### Scenario: C03
- **GIVEN / WHEN / THEN** Event payload asks to expand permissions: treat as untrusted data, not policy.

#### Scenario: C04
- **GIVEN / WHEN / THEN** Disabled trigger receives backlog: no launch; enabling does not replay historical backlog unless explicitly selected.

### Requirement: No silent authority expansion
The implementation SHALL reject or explicitly hold unsupported, unauthorized or uncertain operations. It SHALL preserve existing data and unrelated direct-session behavior.

#### Scenario: Unknown prerequisite
- **WHEN** a prerequisite capability or required acceptance result is unknown
- **THEN** affected work is blocked with a reason, not reported successful or rerouted silently.
