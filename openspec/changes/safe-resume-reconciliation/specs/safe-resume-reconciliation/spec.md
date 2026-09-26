# Recovery with continuing authority and effect reconciliation

## ADDED Requirements

### Requirement: Bounded recovery with continuing authority and effect reconciliation
The system SHALL satisfy the following behavior for ZF-04, ZF-14:

On crash/reconnect reconstruct frozen configuration, authorization, native session identity and effect uncertainty. Resume only a known-safe still-authorized continuation. Unknown external effects hold for Leo with evidence and reconciliation options. Keep interrupted, stopped, failed and outcome-confirmed distinct. Direct-session recovery must obey the same boundary.

#### Scenario: C01
- **GIVEN / WHEN / THEN** Crash after dispatch but before receipt: no blind resend of an external mutation.

#### Scenario: C02
- **GIVEN / WHEN / THEN** Profile permission revoked while owner is down: restart cannot auto-resume old authority.

#### Scenario: C03
- **GIVEN / WHEN / THEN** Journal has torn final entry: recover known prefix and mark missing effects uncertain.

#### Scenario: C04
- **GIVEN / WHEN / THEN** Native session unavailable: do not substitute a new account/environment or claim continuation.

### Requirement: No silent authority expansion
The implementation SHALL reject or explicitly hold unsupported, unauthorized or uncertain operations. It SHALL preserve existing data and unrelated direct-session behavior.

#### Scenario: Unknown prerequisite
- **WHEN** a prerequisite capability or required acceptance result is unknown
- **THEN** affected work is blocked with a reason, not reported successful or rerouted silently.
