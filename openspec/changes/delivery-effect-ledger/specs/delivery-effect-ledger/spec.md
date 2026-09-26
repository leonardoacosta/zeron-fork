# Independent delivery authorization and effect reconciliation

## ADDED Requirements

### Requirement: Bounded independent delivery authorization and effect reconciliation
The system SHALL satisfy the following behavior for ZF-07, ZF-04, ZF-14:

Define independently callable push/create-PR/merge/release/deploy/publish intents, each bound to exact candidate, destination, account reference and workflow action policy. Persist planned/dispatched/observed/uncertain/reconciled outcome states. An ambiguous effect is queried/reconciled before another dispatch; dedupe keys are not exactly-once claims. This unit defines the contract, not every provider adapter.

#### Scenario: C01
- **GIVEN / WHEN / THEN** Accepted candidate without deploy permission cannot deploy.

#### Scenario: C02
- **GIVEN / WHEN / THEN** Autonomous action policy may authorize one action without universal per-action dialog.

#### Scenario: C03
- **GIVEN / WHEN / THEN** Crash after provider mutation before acknowledgment: uncertain record, query existing effect before retry.

#### Scenario: C04
- **GIVEN / WHEN / THEN** Destination/account changes after approval: new authorization binding required.

### Requirement: No silent authority expansion
The implementation SHALL reject or explicitly hold unsupported, unauthorized or uncertain operations. It SHALL preserve existing data and unrelated direct-session behavior.

#### Scenario: Unknown prerequisite
- **WHEN** a prerequisite capability or required acceptance result is unknown
- **THEN** affected work is blocked with a reason, not reported successful or rerouted silently.
