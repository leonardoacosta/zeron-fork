# Mobile compatible assignment control/read surface

## ADDED Requirements

### Requirement: Bounded mobile compatible assignment control/read surface
The system SHALL satisfy the following behavior for ZF-01, ZF-03, ZF-04, ZF-06, ZF-14:

Add reviewed mobile parity for the accepted desktop assignment contract, with explicit capability negotiation and owner routing. Preserve direct sessions and display profile/workflow/evidence/stop state correctly. Mobile reconnect must not repeat launches or delivery. Define supported controls explicitly in design rather than silently treating unsupported controls as success.

#### Scenario: C01
- **GIVEN / WHEN / THEN** Old owner lacks assignment capability: ordinary session still works, assignment operation reports unsupported.

#### Scenario: C02
- **GIVEN / WHEN / THEN** Phone loses connection after launch request: reconcile run identity, no duplicate launch.

#### Scenario: C03
- **GIVEN / WHEN / THEN** Stale phone view submits old revision: conflict and refresh, no overwrite.

#### Scenario: C04
- **GIVEN / WHEN / THEN** Stop receipt remains stopping until owner confirms cessation.

### Requirement: No silent authority expansion
The implementation SHALL reject or explicitly hold unsupported, unauthorized or uncertain operations. It SHALL preserve existing data and unrelated direct-session behavior.

#### Scenario: Unknown prerequisite
- **WHEN** a prerequisite capability or required acceptance result is unknown
- **THEN** affected work is blocked with a reason, not reported successful or rerouted silently.
