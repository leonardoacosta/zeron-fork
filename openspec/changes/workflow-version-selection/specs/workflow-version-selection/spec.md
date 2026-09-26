# Versioned workflow definitions and selection

## ADDED Requirements

### Requirement: Bounded versioned workflow definitions and selection
The system SHALL satisfy the following behavior for ZF-05, ZF-06:

Define independently versioned workflows with stages, agent choices, checks, failure policy, gates and autonomy. Ship the PRD starting sequence without forcing investigation-only work to produce code. Select explicit assignment override, else repository default, else profile default; if none exists hold with a clear configuration error. Persist selected version and explanation before launch. Suggestions create optional updates; active definitions never mutate silently.

#### Scenario: C01
- **GIVEN / WHEN / THEN** Repository and profile defaults differ: repository wins and reason is visible.

#### Scenario: C02
- **GIVEN / WHEN / THEN** Assignment override selects inaccessible workflow: reject rather than bypass profile policy.

#### Scenario: C03
- **GIVEN / WHEN / THEN** Workflow updated while assignment runs: old version remains bound unless explicitly changed and revalidated.

#### Scenario: C04
- **GIVEN / WHEN / THEN** An investigation-only workflow ends with findings and no candidate/delivery stage.

### Requirement: No silent authority expansion
The implementation SHALL reject or explicitly hold unsupported, unauthorized or uncertain operations. It SHALL preserve existing data and unrelated direct-session behavior.

#### Scenario: Unknown prerequisite
- **WHEN** a prerequisite capability or required acceptance result is unknown
- **THEN** affected work is blocked with a reason, not reported successful or rerouted silently.
