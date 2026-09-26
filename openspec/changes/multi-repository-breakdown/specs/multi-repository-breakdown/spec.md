# Bounded parent/child repository objectives

## ADDED Requirements

### Requirement: Bounded bounded parent/child repository objectives
The system SHALL satisfy the following behavior for ZF-12, ZF-02, ZF-15:

Parent objective groups linked repository-scoped children with independent workflow, permissions, candidate/evidence and delivery status. Agent breakdown is proposal until its workflow gate authorizes creation. Leo can inspect/edit. Children stay inside parent objective, approved repositories/profile and shared budget. Grouping neither grants cross-profile access nor requires simultaneous deployment.

#### Scenario: C01
- **GIVEN / WHEN / THEN** Agent proposes an extra unapproved repository: retain proposal but do not create executable child.

#### Scenario: C02
- **GIVEN / WHEN / THEN** Autonomous breakdown within configured scope can create children without imposing universal human confirmation.

#### Scenario: C03
- **GIVEN / WHEN / THEN** Concurrent child reservations cannot exceed parent budget.

#### Scenario: C04
- **GIVEN / WHEN / THEN** Editing breakdown after a child starts preserves prior evidence/effects and revalidates changed dependencies.

### Requirement: No silent authority expansion
The implementation SHALL reject or explicitly hold unsupported, unauthorized or uncertain operations. It SHALL preserve existing data and unrelated direct-session behavior.

#### Scenario: Unknown prerequisite
- **WHEN** a prerequisite capability or required acceptance result is unknown
- **THEN** affected work is blocked with a reason, not reported successful or rerouted silently.
