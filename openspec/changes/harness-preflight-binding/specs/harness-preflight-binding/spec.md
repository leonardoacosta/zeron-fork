# Capability preflight and frozen run configuration

## ADDED Requirements

### Requirement: Bounded capability preflight and frozen run configuration
The system SHALL satisfy the following behavior for ZF-15, ZF-02:

Produce comparable per-harness capability results with supported/unsupported/unknown distinctions and observed version. Freeze requested harness/model/account reference/environment/sandbox/resource configuration for a run. Inspect actual adapter behavior, especially Codex sandbox overrides and Claude/ACP auto-approval, before claiming enforcement. Unsupported requested isolation blocks dispatch. Configuration changes require explicit new run binding.

#### Scenario: C01
- **GIVEN / WHEN / THEN** A harness advertises cancellation but cannot prove descendant stopping: report that capability as unverified, not supported.

#### Scenario: C02
- **GIVEN / WHEN / THEN** Requested sandbox differs from actual process arguments: preflight fails and no agent starts.

#### Scenario: C03
- **GIVEN / WHEN / THEN** Missing model/account/executable cannot silently route to another engineer.

#### Scenario: C04
- **GIVEN / WHEN / THEN** A model or adapter version changes between preflight and launch: invalidate/recheck binding.

### Requirement: No silent authority expansion
The implementation SHALL reject or explicitly hold unsupported, unauthorized or uncertain operations. It SHALL preserve existing data and unrelated direct-session behavior.

#### Scenario: Unknown prerequisite
- **WHEN** a prerequisite capability or required acceptance result is unknown
- **THEN** affected work is blocked with a reason, not reported successful or rerouted silently.
