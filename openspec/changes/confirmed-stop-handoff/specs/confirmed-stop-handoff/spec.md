# Confirmed stopping and explicit human handoff

## ADDED Requirements

### Requirement: Bounded confirmed stopping and explicit human handoff
The system SHALL satisfy the following behavior for ZF-04, ZF-15, ZF-10:

Define pause-requested, stopping, stopped-confirmed, human-owned, handback-requested and resumable states with guarded transitions. Stop receipts are observations, not proof. Track native process/session and descendant/tool activity for supported harnesses. Hand takeover only after stop proof; unknown remote/process status remains held. Human handback is explicit and revalidates authority/configuration.

#### Scenario: C01
- **GIVEN / WHEN / THEN** Cancel RPC acknowledges while a spawned child continues writing: status stays stopping and takeover is refused.

#### Scenario: C02
- **GIVEN / WHEN / THEN** Network disappears during stop: mark uncertain, block conflicting work, keep unrelated isolated work running.

#### Scenario: C03
- **GIVEN / WHEN / THEN** Repeated pause/handback commands are idempotent without duplicate launches.

#### Scenario: C04
- **GIVEN / WHEN / THEN** A stale handback for an older run generation cannot resume the replacement run.

### Requirement: No silent authority expansion
The implementation SHALL reject or explicitly hold unsupported, unauthorized or uncertain operations. It SHALL preserve existing data and unrelated direct-session behavior.

#### Scenario: Unknown prerequisite
- **WHEN** a prerequisite capability or required acceptance result is unknown
- **THEN** affected work is blocked with a reason, not reported successful or rerouted silently.
