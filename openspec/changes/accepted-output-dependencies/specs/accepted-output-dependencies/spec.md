# Exact-version output dependencies

## ADDED Requirements

### Requirement: Bounded exact-version output dependencies
The system SHALL satisfy the following behavior for ZF-11, ZF-14:

Bind dependency edges to accepted stage-output versions, not just whole assignment completion. Reject cycles and foreign-profile edges. Allow independent work to overlap. Upstream replacement/revocation triggers downstream reassessment before next dependent action; prior execution effects are preserved and never retroactively called safe.

#### Scenario: C01
- **GIVEN / WHEN / THEN** Investigation output accepted while parent assignment not done: authorized dependent stage may start.

#### Scenario: C02
- **GIVEN / WHEN / THEN** Upstream new revision cannot silently substitute into already-bound downstream run.

#### Scenario: C03
- **GIVEN / WHEN / THEN** Cycle or self-edge rejected atomically, no partial graph change.

#### Scenario: C04
- **GIVEN / WHEN / THEN** Accepted evidence later contradicted: affected downstream waits/reconciles, independent branch continues.

### Requirement: No silent authority expansion
The implementation SHALL reject or explicitly hold unsupported, unauthorized or uncertain operations. It SHALL preserve existing data and unrelated direct-session behavior.

#### Scenario: Unknown prerequisite
- **WHEN** a prerequisite capability or required acceptance result is unknown
- **THEN** affected work is blocked with a reason, not reported successful or rerouted silently.
