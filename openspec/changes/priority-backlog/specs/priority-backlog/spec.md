# Priority, blockers and non-preemptive urgent work

## ADDED Requirements

### Requirement: Bounded priority, blockers and non-preemptive urgent work
The system SHALL satisfy the following behavior for ZF-10, ZF-09:

Queue conflicted proposals with blocker type/reason and explicit priority. Among eligible work sort priority then oldest admission; Leo override recorded. Observer recommendations never silently change priority. Reassess on blocker resolution. Urgent conflicting work waits unless Leo explicitly requests interruption and actual stop is confirmed. Dependency-wait and conflict-wait are different states.

#### Scenario: C01
- **GIVEN / WHEN / THEN** Old blocked high-priority item does not stall lower-priority unrelated eligible work.

#### Scenario: C02
- **GIVEN / WHEN / THEN** Equal-priority eligible items retain oldest-first order across restart.

#### Scenario: C03
- **GIVEN / WHEN / THEN** Urgent conflict cannot launch on mere cancellation acknowledgment.

#### Scenario: C04
- **GIVEN / WHEN / THEN** Priority update racing admission produces one auditable order, not duplicate dispatch.

### Requirement: No silent authority expansion
The implementation SHALL reject or explicitly hold unsupported, unauthorized or uncertain operations. It SHALL preserve existing data and unrelated direct-session behavior.

#### Scenario: Unknown prerequisite
- **WHEN** a prerequisite capability or required acceptance result is unknown
- **THEN** affected work is blocked with a reason, not reported successful or rerouted silently.
