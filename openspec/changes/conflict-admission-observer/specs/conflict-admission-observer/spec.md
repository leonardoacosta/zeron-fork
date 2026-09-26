# Conflict admission for assignments and direct sessions

## ADDED Requirements

### Requirement: Bounded conflict admission for assignments and direct sessions
The system SHALL satisfy the following behavior for ZF-09, ZF-02, ZF-18:

At proposal admission inspect overlapping changes, incompatible assumptions, shared resources and unmet dependencies. Include direct sessions without converting them into assignments. Represent limited outside-Zeron visibility. Different files can conflict; independent work proceeds. Recheck scope changes and shared-action boundaries. Uncertain conflicts require another reviewer; unresolved uncertainty holds affected work and alerts. System One is observer, not execution authority; unverified adapter can only return unknown.

#### Scenario: C01
- **GIVEN / WHEN / THEN** Disjoint files share one database migration invariant: identify conflict or uncertainty, not automatic independence.

#### Scenario: C02
- **GIVEN / WHEN / THEN** Two proposals race admission: no overlapping exclusive lease granted twice.

#### Scenario: C03
- **GIVEN / WHEN / THEN** One uncertain conflict holds only affected work, not all queues.

#### Scenario: C04
- **GIVEN / WHEN / THEN** Reviewer unavailable or external work invisible: expose unknown and hold affected scope.

### Requirement: No silent authority expansion
The implementation SHALL reject or explicitly hold unsupported, unauthorized or uncertain operations. It SHALL preserve existing data and unrelated direct-session behavior.

#### Scenario: Unknown prerequisite
- **WHEN** a prerequisite capability or required acceptance result is unknown
- **THEN** affected work is blocked with a reason, not reported successful or rerouted silently.
