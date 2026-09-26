# Named work profiles and explicit bindings

## ADDED Requirements

### Requirement: Bounded named work profiles and explicit bindings
The system SHALL satisfy the following behavior for ZF-02:

Introduce extensible work-profile identity/configuration separate from Local/Synced/Development transport scope. Personal/Priceless/Brown are named work contexts, not hardcoded three-case permissions. Bind direct sessions and assignments to a stable work-profile ID and revision. Existing data must have an explicit migration/binding rule; ambiguous legacy ownership remains read-only/held rather than assigned by guess.

#### Scenario: C01
- **GIVEN / WHEN / THEN** Two profiles on one device cannot retrieve each other's assignment, transcript, upload or repository binding through local or remote RPC.

#### Scenario: C02
- **GIVEN / WHEN / THEN** Rename a profile while a session runs: identity stays stable and the frozen binding does not silently change.

#### Scenario: C03
- **GIVEN / WHEN / THEN** Open legacy data without an unambiguous work-profile binding: show migration-required state, retain original bytes and prohibit execution.

#### Scenario: C04
- **GIVEN / WHEN / THEN** Create a fourth profile without changing an enum or granting default access.

### Requirement: No silent authority expansion
The implementation SHALL reject or explicitly hold unsupported, unauthorized or uncertain operations. It SHALL preserve existing data and unrelated direct-session behavior.

#### Scenario: Unknown prerequisite
- **WHEN** a prerequisite capability or required acceptance result is unknown
- **THEN** affected work is blocked with a reason, not reported successful or rerouted silently.
