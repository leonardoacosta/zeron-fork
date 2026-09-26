# Desktop assignment and intervention surface

## ADDED Requirements

### Requirement: Bounded desktop assignment and intervention surface
The system SHALL satisfy the following behavior for ZF-01, ZF-02, ZF-03, ZF-04, ZF-05, ZF-06, ZF-14, ZF-18:

Add explicit create/promote/read/history/launch controls alongside direct sessions. Before launch show profile, selected workflow/version/reason, permissions, resources and unavailable capabilities. Show stopping versus confirmed stop, takeover/handback, evidence class and blocked reasons. UI location must be reviewed using existing navigation conventions before implementation; preserve keyboard and screen-reader operation.

#### Scenario: C01
- **GIVEN / WHEN / THEN** Open ordinary conversation: no forced assignment administration.

#### Scenario: C02
- **GIVEN / WHEN / THEN** Promote requires explicit action and preserves transcript.

#### Scenario: C03
- **GIVEN / WHEN / THEN** Disconnected owner or old capability: show unavailable/unsupported, never local duplicate.

#### Scenario: C04
- **GIVEN / WHEN / THEN** Screen-reader/keyboard user can inspect workflow reason and stop uncertainty without relying on color.

### Requirement: No silent authority expansion
The implementation SHALL reject or explicitly hold unsupported, unauthorized or uncertain operations. It SHALL preserve existing data and unrelated direct-session behavior.

#### Scenario: Unknown prerequisite
- **WHEN** a prerequisite capability or required acceptance result is unknown
- **THEN** affected work is blocked with a reason, not reported successful or rerouted silently.
