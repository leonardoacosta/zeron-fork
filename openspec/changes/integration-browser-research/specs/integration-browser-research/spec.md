# Browser provider isolation research

## ADDED Requirements

### Requirement: Bounded browser provider isolation research
The system SHALL satisfy the following behavior for ZF-17, ZF-19:

Compare existing embedded browser capability and candidate automation providers against required profile/session isolation, explicit signed-in scope, stopping and redacted evidence. Record API/version and credential handling, select only after reviewed decision. Browser choice is a genuine open decision, not a reason to reopen approved isolation rules.

#### Scenario: C01
- **GIVEN / WHEN / THEN** Provider supports screenshots but cannot isolate storage: does not satisfy session isolation.

#### Scenario: C02
- **GIVEN / WHEN / THEN** Provider close command returns before tool action stops: cancellation remains unverified.

#### Scenario: C03
- **GIVEN / WHEN / THEN** Provider needs cloud data upload: disclose data boundary before any private page use.

### Requirement: No silent authority expansion
The implementation SHALL reject or explicitly hold unsupported, unauthorized or uncertain operations. It SHALL preserve existing data and unrelated direct-session behavior.

#### Scenario: Unknown prerequisite
- **WHEN** a prerequisite capability or required acceptance result is unknown
- **THEN** affected work is blocked with a reason, not reported successful or rerouted silently.
