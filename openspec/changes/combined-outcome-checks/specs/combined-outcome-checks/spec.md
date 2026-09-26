# Parent outcome verification over delivered versions

## ADDED Requirements

### Requirement: Bounded parent outcome verification over delivered versions
The system SHALL satisfy the following behavior for ZF-13, ZF-12, ZF-14:

Parent workflow evaluates combined checks across exact required child output and delivered versions before objective completion. Finished children are insufficient. Partial delivery visible; failed child blocks dependents only. Configured human/autonomous outcome gates apply. Superseded child outputs cannot silently count.

#### Scenario: C01
- **GIVEN / WHEN / THEN** All child tasks done but integration endpoint fails: parent outcome remains unconfirmed.

#### Scenario: C02
- **GIVEN / WHEN / THEN** One child delivered old accepted revision while another expects new API: combined check fails with exact mismatch.

#### Scenario: C03
- **GIVEN / WHEN / THEN** Optional independent child failure does not automatically stop unrelated required work; requiredness is explicit.

#### Scenario: C04
- **GIVEN / WHEN / THEN** Partial deployment survives restart and remains visible with reconciliation options.

### Requirement: No silent authority expansion
The implementation SHALL reject or explicitly hold unsupported, unauthorized or uncertain operations. It SHALL preserve existing data and unrelated direct-session behavior.

#### Scenario: Unknown prerequisite
- **WHEN** a prerequisite capability or required acceptance result is unknown
- **THEN** affected work is blocked with a reason, not reported successful or rerouted silently.
