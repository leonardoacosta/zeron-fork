# Release, deploy and publish adapters

## ADDED Requirements

### Requirement: Bounded release, deploy and publish adapters
The system SHALL satisfy the following behavior for ZF-07, ZF-19:

Implement individually callable release/deploy/publish against explicitly selected destinations and verified contracts. Preserve build artifact identity, target environment, authorization and post-delivery observation. Local installation is a valid deploy target; hosted replacement is never inferred. Full release-candidate management beyond these actions remains outside approved scope.

#### Scenario: C01
- **GIVEN / WHEN / THEN** Artifact built from revision A cannot be presented as delivery of B.

#### Scenario: C02
- **GIVEN / WHEN / THEN** Install fails after staging: retain previous executable/data and report rollback result.

#### Scenario: C03
- **GIVEN / WHEN / THEN** Publish returns success but target serves old content: delivered may be observed but outcome-confirmed fails.

#### Scenario: C04
- **GIVEN / WHEN / THEN** Unsupported signing/provider credentials: blocked acceptance, no disabling security or password resets.

### Requirement: No silent authority expansion
The implementation SHALL reject or explicitly hold unsupported, unauthorized or uncertain operations. It SHALL preserve existing data and unrelated direct-session behavior.

#### Scenario: Unknown prerequisite
- **WHEN** a prerequisite capability or required acceptance result is unknown
- **THEN** affected work is blocked with a reason, not reported successful or rerouted silently.
