# Configured verification and acceptance transitions

## ADDED Requirements

### Requirement: Bounded configured verification and acceptance transitions
The system SHALL satisfy the following behavior for ZF-05, ZF-14, ZF-11:

Keep agent-finished, verified, accepted, delivered and outcome-confirmed separate. Evaluate configured checks against exact bound output versions. Human or autonomous acceptance is allowed only as workflow policy specifies. Preserve external reviewer/OpenSpec/planning authority; in-product status cannot overwrite it. Missing/stale/contradictory evidence holds dependent transitions.

#### Scenario: C01
- **GIVEN / WHEN / THEN** Agent reports success while required check fails: verified/accepted stay false.

#### Scenario: C02
- **GIVEN / WHEN / THEN** Autonomous gate with all required checks and valid policy accepts without inventing a universal manual approval.

#### Scenario: C03
- **GIVEN / WHEN / THEN** Human approval for output A cannot apply to changed output B.

#### Scenario: C04
- **GIVEN / WHEN / THEN** External reviewer rejects a required review while internal tests pass: gate remains held.

### Requirement: No silent authority expansion
The implementation SHALL reject or explicitly hold unsupported, unauthorized or uncertain operations. It SHALL preserve existing data and unrelated direct-session behavior.

#### Scenario: Unknown prerequisite
- **WHEN** a prerequisite capability or required acceptance result is unknown
- **THEN** affected work is blocked with a reason, not reported successful or rerouted silently.
