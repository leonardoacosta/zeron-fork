# Immediate grouped safety exceptions

## ADDED Requirements

### Requirement: Bounded immediate grouped safety exceptions
The system SHALL satisfy the following behavior for ZF-18, ZF-04, ZF-09:

Persist and group actionable exceptions with source, profile, affected work, blocker/uncertainty and safe next action. Routine progress goes to activity, not urgent alerts. Notification delivery/acknowledgment does not accept work, grant authority or resume execution. Safety features cannot defer essential alerts until morning briefings ship.

#### Scenario: C01
- **GIVEN / WHEN / THEN** Repeated same stop uncertainty creates one grouped alert with updated observations, not an alert storm.

#### Scenario: C02
- **GIVEN / WHEN / THEN** Notification delivery fails: blocked state remains durable and visible after restart.

#### Scenario: C03
- **GIVEN / WHEN / THEN** User dismisses alert: execution remains held.

#### Scenario: C04
- **GIVEN / WHEN / THEN** Profile-private alert must not leak into another profile destination.

### Requirement: No silent authority expansion
The implementation SHALL reject or explicitly hold unsupported, unauthorized or uncertain operations. It SHALL preserve existing data and unrelated direct-session behavior.

#### Scenario: Unknown prerequisite
- **WHEN** a prerequisite capability or required acceptance result is unknown
- **THEN** affected work is blocked with a reason, not reported successful or rerouted silently.
