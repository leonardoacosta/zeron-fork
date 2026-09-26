# Explicit isolated engineering comparisons

## ADDED Requirements

### Requirement: Bounded explicit isolated engineering comparisons
The system SHALL satisfy the following behavior for ZF-16, ZF-15, ZF-14:

Only user-launched comparisons with task, entrants and budget. Freeze identical baseline/input/configuration bindings and isolate each attempt. Report disclosed configurations, cost unknowns, independent correctness results and infrastructure failures separately. Comparison recommends; Leo alone approves routing/default changes. No automatic delivery or winning-run adoption.

#### Scenario: C01
- **GIVEN / WHEN / THEN** Entrants start from different dirty trees: admission fails before spending.

#### Scenario: C02
- **GIVEN / WHEN / THEN** One entrant infrastructure fails: do not rank it as engineering incorrectness without evidence.

#### Scenario: C03
- **GIVEN / WHEN / THEN** Fast candidate fails independent correctness check: cannot win by speed alone.

#### Scenario: C04
- **GIVEN / WHEN / THEN** Winner selected: defaults unchanged and delivery not triggered.

### Requirement: No silent authority expansion
The implementation SHALL reject or explicitly hold unsupported, unauthorized or uncertain operations. It SHALL preserve existing data and unrelated direct-session behavior.

#### Scenario: Unknown prerequisite
- **WHEN** a prerequisite capability or required acceptance result is unknown
- **THEN** affected work is blocked with a reason, not reported successful or rerouted silently.
