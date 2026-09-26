# Verified provider adapters and authority preservation

## ADDED Requirements

### Requirement: Bounded verified provider adapters and authority preservation
The system SHALL satisfy the following behavior for ZF-19, ZF-15:

Instantiate one child adapter change per researched concrete provider and action set before implementation. Each child freezes documented API/version, maps native identity/status/stop/effect semantics, honors profile and external authority, and has real authorized acceptance. This boundary is a fan-out contract, not permission to implement all adapters in one patch. MCP exposure must reuse engine authorization, not bypass it.

#### Scenario: C01
- **GIVEN / WHEN / THEN** Adapter returns unsupported for missing stop/isolation instead of claiming a generic interface makes it safe.

#### Scenario: C02
- **GIVEN / WHEN / THEN** External planning/review status changes: preserve source provenance and never overwrite from local completion.

#### Scenario: C03
- **GIVEN / WHEN / THEN** Provider upgrade changes contract: capability evidence invalidated and affected launches held.

### Requirement: No silent authority expansion
The implementation SHALL reject or explicitly hold unsupported, unauthorized or uncertain operations. It SHALL preserve existing data and unrelated direct-session behavior.

#### Scenario: Unknown prerequisite
- **WHEN** a prerequisite capability or required acceptance result is unknown
- **THEN** affected work is blocked with a reason, not reported successful or rerouted silently.
