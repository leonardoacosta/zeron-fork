# Initiative execution contracts

## ADDED Requirements

### Requirement: Exhaustive bounded decomposition
The plan SHALL map each ZF-01 through ZF-19 clause to named change boundaries, preserve approved behavior, and separate unresolved research from implementation-ready tasks.

#### Scenario: Unknown provider
- **WHEN** an external API is not verified
- **THEN** its change remains implementation-blocked with a named research prerequisite, not an invented adapter.

### Requirement: CI before promotion
Every iteration and integrated round SHALL complete its required CI phase on the exact promoted revision before any dependent next stage is admitted.

#### Scenario: Partial green
- **WHEN** component checks pass but combined checks fail or required platform evidence is missing
- **THEN** the round does not promote.

### Requirement: Delegable contracts
Each change SHALL define scope, prerequisites, existing file anchors, observable edge cases, prohibited interpretations, verification and rollback; product code SHALL wait for code-complete tasks and named approval.

#### Scenario: Low-context executor
- **WHEN** an executor finds an undefined type or missing API in an implementation step
- **THEN** refinement resumes before implementation, without guessing or dropping a requirement.
