# Profile-configurable routine briefings

## ADDED Requirements

### Requirement: Bounded profile-configurable routine briefings
The system SHALL satisfy the following behavior for ZF-18:

Provide morning/routine briefing schedule and destinations per profile with explicit configuration. Summarize progress, blockers, uncertainty and accepted/delivered/outcome states distinctly. Delivery provider/channel selection must be recorded before adapter implementation. Missed schedule, timezone/DST and duplicate delivery are explicit policies; no guessed universal morning time.

#### Scenario: C01
- **GIVEN / WHEN / THEN** Clock crosses DST or device was offline: apply configured missed-run policy once, not duplicate delivery.

#### Scenario: C02
- **GIVEN / WHEN / THEN** Destination revoked: retain failed-delivery state without sending to a fallback account.

#### Scenario: C03
- **GIVEN / WHEN / THEN** Briefing reports agent-finished but unverified output as unverified.

#### Scenario: C04
- **GIVEN / WHEN / THEN** Routine progress stays activity while urgent exception still alerts immediately.

### Requirement: No silent authority expansion
The implementation SHALL reject or explicitly hold unsupported, unauthorized or uncertain operations. It SHALL preserve existing data and unrelated direct-session behavior.

#### Scenario: Unknown prerequisite
- **WHEN** a prerequisite capability or required acceptance result is unknown
- **THEN** affected work is blocked with a reason, not reported successful or rerouted silently.
