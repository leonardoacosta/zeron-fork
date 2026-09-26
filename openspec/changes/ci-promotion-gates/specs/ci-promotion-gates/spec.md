# CI admission and round promotion

## ADDED Requirements

### Requirement: Bounded ci admission and round promotion
The system SHALL satisfy the following behavior for ZF-01, ZF-14:

Extend existing CI, not a separate build system. Every change iteration must pass its declared checks; every integrated round must pass the union of affected checks on one exact commit. Persist requirement-to-check results, platform, toolchain, skipped tests and artifact references in the change tasks. A failed, missing, cancelled or stale required check blocks promotion. Newly discovered prerequisite failures become bounded repair changes, not permanent waivers.

#### Scenario: C01
- **GIVEN / WHEN / THEN** Given two independently green changes with conflicting combined behavior, when integrated CI fails, then neither combined round nor its dependents promote.

#### Scenario: C02
- **GIVEN / WHEN / THEN** Given CI success for commit A, when source/config/lockfile changes to B, then A evidence cannot promote B.

#### Scenario: C03
- **GIVEN / WHEN / THEN** Given a filter selects zero tests or an ignored external test never runs, then it is not coverage.

#### Scenario: C04
- **GIVEN / WHEN / THEN** Given native platform/auth credentials are unavailable, record blocked evidence and hold the affected acceptance, without disabling a job to manufacture green.

### Requirement: No silent authority expansion
The implementation SHALL reject or explicitly hold unsupported, unauthorized or uncertain operations. It SHALL preserve existing data and unrelated direct-session behavior.

#### Scenario: Unknown prerequisite
- **WHEN** a prerequisite capability or required acceptance result is unknown
- **THEN** affected work is blocked with a reason, not reported successful or rerouted silently.
