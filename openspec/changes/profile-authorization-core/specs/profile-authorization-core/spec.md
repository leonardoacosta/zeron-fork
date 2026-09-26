# Owner authorization core

## ADDED Requirements

### Requirement: Fail-closed policy core
The system SHALL satisfy: Define owner-derived principal/resource/operation requests, private single-use permits and current policy revision/grants. Persist policy replacement with CAS; synchronous admission is serialized with revocation. This unit exposes no daemon profile selection or full runtime isolation claim.

#### Scenario: C01
- **GIVEN / WHEN / THEN** Missing or unavailable policy, unbound legacy and foreign binding deny without invoking effect closure.

#### Scenario: C02
- **GIVEN / WHEN / THEN** Permit bound to another evaluator, operation or resource cannot be consumed.

#### Scenario: C03
- **GIVEN / WHEN / THEN** Revocation before synchronous admission rejects stale permit and executes zero effects.

#### Scenario: C04
- **GIVEN / WHEN / THEN** Concurrent synchronous admission and policy replacement have a defined serialized order; poison denies.
