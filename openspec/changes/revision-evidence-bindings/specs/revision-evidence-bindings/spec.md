# Versioned outputs and evidence provenance

## ADDED Requirements

### Requirement: Bounded versioned outputs and evidence provenance
The system SHALL satisfy the following behavior for ZF-14, ZF-03:

Introduce immutable output/candidate identities bound to exact assignment revision, source revision and dirty-tree content, frozen input/configuration/authorization/resource bindings, environment and native sessions. Evidence records check command, observations, outcome, limitations, timestamps and redacted artifacts. Separate structural, synthetic and real-workflow evidence. Editing inputs creates a new binding; it does not transfer approval.

#### Scenario: C01
- **GIVEN / WHEN / THEN** Same Git commit with changed uncommitted content produces a different binding and stale prior evidence.

#### Scenario: C02
- **GIVEN / WHEN / THEN** A candidate has artifacts but no passed check: show unverified, never accepted.

#### Scenario: C03
- **GIVEN / WHEN / THEN** An artifact contains a secret or unrelated private content: reject/redact before persistence and alert safely.

#### Scenario: C04
- **GIVEN / WHEN / THEN** Conflicting or missing evidence blocks dependent advancement rather than choosing the optimistic entry.

### Requirement: No silent authority expansion
The implementation SHALL reject or explicitly hold unsupported, unauthorized or uncertain operations. It SHALL preserve existing data and unrelated direct-session behavior.

#### Scenario: Unknown prerequisite
- **WHEN** a prerequisite capability or required acceptance result is unknown
- **THEN** affected work is blocked with a reason, not reported successful or rerouted silently.
