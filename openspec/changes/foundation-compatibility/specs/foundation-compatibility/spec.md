# Preserve direct sessions and two-device baseline

## ADDED Requirements

### Requirement: Bounded preserve direct sessions and two-device baseline
The system SHALL satisfy the following behavior for ZF-01, ZF-03:

Codify current successful assignment persistence and ordinary-session behavior as regression gates. Preserve explicit null RPC successes, unsupported owner rejection, no local substitutes and no implicit delegation. Keep local private deployment distinct from hosted authentication acceptance. Verify exact installed artifacts rather than version string alone.

#### Scenario: C01
- **GIVEN / WHEN / THEN** Owner restarts after acknowledged assignment: native second-device read/history match and owner unchanged.

#### Scenario: C02
- **GIVEN / WHEN / THEN** Old owner lacks capability: assignment rejected explicitly, ordinary session unaffected.

#### Scenario: C03
- **GIVEN / WHEN / THEN** Successful null response completes RPC rather than hanging.

#### Scenario: C04
- **GIVEN / WHEN / THEN** Direct session opens without an assignment or hidden workflow launch.

### Requirement: No silent authority expansion
The implementation SHALL reject or explicitly hold unsupported, unauthorized or uncertain operations. It SHALL preserve existing data and unrelated direct-session behavior.

#### Scenario: Unknown prerequisite
- **WHEN** a prerequisite capability or required acceptance result is unknown
- **THEN** affected work is blocked with a reason, not reported successful or rerouted silently.
