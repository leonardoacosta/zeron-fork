# Dependency and asset attribution for fork distribution

## ADDED Requirements

### Requirement: Bounded dependency and asset attribution for fork distribution
The system SHALL satisfy the following behavior for ZF-01, ZF-19:

Inventory exact selected dependency/asset licenses and required attribution for distributed local builds, including pinned GPUI/component forks, fonts and browser/platform components. Root MIT alone does not settle asset/dependency terms. Record evidence and package required notices without claiming legal review beyond verified facts.

#### Scenario: C01
- **GIVEN / WHEN / THEN** Pinned dependency revision changes: attribution evidence invalidated for that package.

#### Scenario: C02
- **GIVEN / WHEN / THEN** Binary package omits required font notice: packaging gate fails.

#### Scenario: C03
- **GIVEN / WHEN / THEN** License unresolved: affected distribution held, no assumption from repository root license.

### Requirement: No silent authority expansion
The implementation SHALL reject or explicitly hold unsupported, unauthorized or uncertain operations. It SHALL preserve existing data and unrelated direct-session behavior.

#### Scenario: Unknown prerequisite
- **WHEN** a prerequisite capability or required acceptance result is unknown
- **THEN** affected work is blocked with a reason, not reported successful or rerouted silently.
