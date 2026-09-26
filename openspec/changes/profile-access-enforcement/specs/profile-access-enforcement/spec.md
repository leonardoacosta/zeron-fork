# Execution-time profile and resource authorization

## ADDED Requirements

### Requirement: Bounded execution-time profile and resource authorization
The system SHALL satisfy the following behavior for ZF-02, ZF-15, ZF-19:

Validate work-profile policy at every engine entry point that reads protected content or launches tools: direct sessions, assignment operations, MCP, terminal, repository and credential selection. Bind allowed repositories, account references, tools, environments and action scope explicitly. Revalidate at launch and external-effect boundaries; policy revocation blocks new effects and enters the configured stop/hold path. Never serialize secret values into authority snapshots.

#### Scenario: C01
- **GIVEN / WHEN / THEN** A trusted remote device supplies a foreign profile/account/repository ID: reject before any read or child process starts.

#### Scenario: C02
- **GIVEN / WHEN / THEN** A symlink or renamed checkout escapes the approved repository root: reject the resolved target.

#### Scenario: C03
- **GIVEN / WHEN / THEN** Policy changes after preflight but before dispatch: dispatch rechecks and denies stale authority.

#### Scenario: C04
- **GIVEN / WHEN / THEN** An unavailable requested account/tool must report unavailable, not fall back to a global default.

#### Scenario: C05
- **GIVEN / WHEN / THEN** Direct session and assignment invoking the same protected operation receive equivalent authorization decisions.

### Requirement: No silent authority expansion
The implementation SHALL reject or explicitly hold unsupported, unauthorized or uncertain operations. It SHALL preserve existing data and unrelated direct-session behavior.

#### Scenario: Unknown prerequisite
- **WHEN** a prerequisite capability or required acceptance result is unknown
- **THEN** affected work is blocked with a reason, not reported successful or rerouted silently.
