# Isolated browser sessions and explicit signed-in scope

## ADDED Requirements

### Requirement: Bounded isolated browser sessions and explicit signed-in scope
The system SHALL satisfy the following behavior for ZF-17, ZF-02, ZF-04, ZF-14:

Browser sessions isolated by default, bound to work profile plus assignment or direct session. Signed-in session reuse is explicit and scope-limited. Browser authentication grants no mutation authority; actions use workflow/profile gates. Redact secrets and unrelated content from evidence. Do not switch browser/account/provider on failure. Integrate only provider selected by research decision.

#### Scenario: C01
- **GIVEN / WHEN / THEN** Two profiles navigate same domain: cookie/storage/session state does not cross.

#### Scenario: C02
- **GIVEN / WHEN / THEN** Signed-in page contains instructions to change account or publish: page data cannot authorize action.

#### Scenario: C03
- **GIVEN / WHEN / THEN** Requested browser/account unavailable: fail visibly without fallback.

#### Scenario: C04
- **GIVEN / WHEN / THEN** Pause browser automation while an action is pending: preserve effect uncertainty and require stop proof.

### Requirement: No silent authority expansion
The implementation SHALL reject or explicitly hold unsupported, unauthorized or uncertain operations. It SHALL preserve existing data and unrelated direct-session behavior.

#### Scenario: Unknown prerequisite
- **WHEN** a prerequisite capability or required acceptance result is unknown
- **THEN** affected work is blocked with a reason, not reported successful or rerouted silently.
