# Git push and change-request create/merge actions

## ADDED Requirements

### Requirement: Bounded git push and change-request create/merge actions
The system SHALL satisfy the following behavior for ZF-07, ZF-19:

Implement push, create change request and merge as independently authorized actions using verified provider methods. Freeze remote/ref/repository/account/candidate; observe exact delivered commit. Support required GitHub/ADO providers only when their research and native acceptance are complete; unsupported remains explicit. Respect protected branches and external review authority.

#### Scenario: C01
- **GIVEN / WHEN / THEN** Remote URL changes between proposal and push: block and reauthorize.

#### Scenario: C02
- **GIVEN / WHEN / THEN** PR creation times out after successful creation: discover matching external identity, do not create duplicate.

#### Scenario: C03
- **GIVEN / WHEN / THEN** Merge observes newer head than accepted candidate: reject stale candidate.

#### Scenario: C04
- **GIVEN / WHEN / THEN** Branch protection rejects merge: surface provider decision; never bypass or force push.

### Requirement: No silent authority expansion
The implementation SHALL reject or explicitly hold unsupported, unauthorized or uncertain operations. It SHALL preserve existing data and unrelated direct-session behavior.

#### Scenario: Unknown prerequisite
- **WHEN** a prerequisite capability or required acceptance result is unknown
- **THEN** affected work is blocked with a reason, not reported successful or rerouted silently.
