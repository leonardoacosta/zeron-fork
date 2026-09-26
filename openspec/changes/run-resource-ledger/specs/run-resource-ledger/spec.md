# Durable resource budgets and usage

## ADDED Requirements

### Requirement: Bounded durable resource budgets and usage
The system SHALL satisfy the following behavior for ZF-15, ZF-12, ZF-16:

Persist reservations and observed usage bound to run/profile/resource policy. Unknown price or usage remains unknown. Parent and child runs draw from one authorized shared budget without double counting; reservation/launch is atomic or recoverably reconciled. Budget exhaustion holds new work and invokes safe stopping for active work according to policy. No invented universal numeric budget.

#### Scenario: C01
- **GIVEN / WHEN / THEN** Two concurrent runs race for the final reservation: at most one starts.

#### Scenario: C02
- **GIVEN / WHEN / THEN** Owner restarts with a reserved-but-unconfirmed run: reconcile rather than spend reservation twice or refund blindly.

#### Scenario: C03
- **GIVEN / WHEN / THEN** Provider omits cost: show unknown and enforce policy for unknown cost, never display zero.

#### Scenario: C04
- **GIVEN / WHEN / THEN** Child usage rolls up once despite repeated provider events.

### Requirement: No silent authority expansion
The implementation SHALL reject or explicitly hold unsupported, unauthorized or uncertain operations. It SHALL preserve existing data and unrelated direct-session behavior.

#### Scenario: Unknown prerequisite
- **WHEN** a prerequisite capability or required acceptance result is unknown
- **THEN** affected work is blocked with a reason, not reported successful or rerouted silently.
