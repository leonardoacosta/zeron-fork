# Jcode, Herdr and observer capability research

## ADDED Requirements

### Requirement: Bounded jcode, herdr and observer capability research
The system SHALL satisfy the following behavior for ZF-15, ZF-09, ZF-19:

Produce versioned evidence for Jcode environment-local swarm integration and Herdr attachment, and separately SystemOne observer, Jev, Laya and empryo identity/capabilities. Identify native IDs, start/stop proof, status, configuration, usage and isolation contracts. Unknown products/APIs remain unknown and cannot become executable adapters. Keep SystemOne distinct from engineering harness.

#### Scenario: C01
- **GIVEN / WHEN / THEN** A tool is installed but no stop proof/API exists: capability remains blocked.

#### Scenario: C02
- **GIVEN / WHEN / THEN** Documentation and observed version disagree: record mismatch and do not guess request shape.

#### Scenario: C03
- **GIVEN / WHEN / THEN** Jcode preferred but unavailable: ordinary configured engineer stays unchanged.

### Requirement: No silent authority expansion
The implementation SHALL reject or explicitly hold unsupported, unauthorized or uncertain operations. It SHALL preserve existing data and unrelated direct-session behavior.

#### Scenario: Unknown prerequisite
- **WHEN** a prerequisite capability or required acceptance result is unknown
- **THEN** affected work is blocked with a reason, not reported successful or rerouted silently.
