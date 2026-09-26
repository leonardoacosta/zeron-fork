# Approved proposal implementation and verification stages

## ADDED Requirements

### Requirement: Bounded approved proposal implementation and verification stages
The system SHALL satisfy the following behavior for ZF-05, ZF-14, ZF-15:

Extend the bounded investigation runner to Understand, Investigate, Propose, Implement and Verify transitions under a pinned workflow. A proposal must pass its configured gate before any implementation dispatch. Bind exact approved scope, engineer, repository, baseline and resource policy; ordinary implementation uses that engineer once. Produce a new revision-bound candidate from observed working-tree changes, then run independent configured verification. Deliver and Confirm outcome invoke their separately gated contracts, not implicit inline side effects.

#### Scenario: C01
- **GIVEN / WHEN / THEN** Investigation suggests code changes before proposal acceptance: no implementation launch.

#### Scenario: C02
- **GIVEN / WHEN / THEN** Accepted proposal changes repository or allowed actions: implementation refuses stale scope and requests new gate.

#### Scenario: C03
- **GIVEN / WHEN / THEN** Engineer finishes with uncommitted changes: candidate binds exact dirty tree, not just HEAD.

#### Scenario: C04
- **GIVEN / WHEN / THEN** Verification fails: preserve candidate/evidence and follow configured retry or hold policy within original budget, no automatic delivery.

#### Scenario: C05
- **GIVEN / WHEN / THEN** Workflow marks a stage optional: skip only by recorded policy, not agent improvisation.

### Requirement: No silent authority expansion
The implementation SHALL reject or explicitly hold unsupported, unauthorized or uncertain operations. It SHALL preserve existing data and unrelated direct-session behavior.

#### Scenario: Unknown prerequisite
- **WHEN** a prerequisite capability or required acceptance result is unknown
- **THEN** affected work is blocked with a reason, not reported successful or rerouted silently.
