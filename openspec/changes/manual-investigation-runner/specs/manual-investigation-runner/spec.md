# Manual bounded investigation workflow

## ADDED Requirements

### Requirement: Bounded manual bounded investigation workflow
The system SHALL satisfy the following behavior for ZF-03, ZF-05, ZF-06, ZF-08:

Explicitly launch one configured investigation for an assignment after profile/preflight/resource/selection gates. Bind native session IDs and observations; findings can be the terminal output. Preserve objective and permissions through replacement, with stop proof for affected old execution. Keep direct sessions runnable without implicit assignments. No coding/delivery authorization inferred from investigation.

#### Scenario: C01
- **GIVEN / WHEN / THEN** Double-click/retried launch yields one run identity and one resource reservation.

#### Scenario: C02
- **GIVEN / WHEN / THEN** Replacement adds linked session while preserving findings/history and allowed actions.

#### Scenario: C03
- **GIVEN / WHEN / THEN** Investigation ends with checked findings and unresolved questions, without requiring code changes.

#### Scenario: C04
- **GIVEN / WHEN / THEN** Direct session opens normally without automatic assignment creation.

### Requirement: No silent authority expansion
The implementation SHALL reject or explicitly hold unsupported, unauthorized or uncertain operations. It SHALL preserve existing data and unrelated direct-session behavior.

#### Scenario: Unknown prerequisite
- **WHEN** a prerequisite capability or required acceptance result is unknown
- **THEN** affected work is blocked with a reason, not reported successful or rerouted silently.
