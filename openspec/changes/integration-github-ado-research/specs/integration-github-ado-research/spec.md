# GitHub, ADO, MCP and Aperture boundary research

## ADDED Requirements

### Requirement: Bounded github, ado, mcp and aperture boundary research
The system SHALL satisfy the following behavior for ZF-19, ZF-07:

Map current GitHub read/status and MCP behavior; verify exact ADO and Tailscale Aperture identities, versions, APIs and authority boundaries. Record external planning/review/specification systems as authoritative. Determine remote-only repository support separately from local storage convenience. Produce independently scoped adapter follow-ups per verified system, never a blanket integration permission.

#### Scenario: C01
- **GIVEN / WHEN / THEN** MCP tool available but action outside profile/workflow scope: unavailable for that action.

#### Scenario: C02
- **GIVEN / WHEN / THEN** External issue says Done while local output unverified: no acceptance transition.

#### Scenario: C03
- **GIVEN / WHEN / THEN** Remote repository cannot be materialized locally: report capability limitation, not require local storage as product policy.

#### Scenario: C04
- **GIVEN / WHEN / THEN** ADO/Brown endpoint discovered: no access attempt solely because Brown profile exists.

### Requirement: No silent authority expansion
The implementation SHALL reject or explicitly hold unsupported, unauthorized or uncertain operations. It SHALL preserve existing data and unrelated direct-session behavior.

#### Scenario: Unknown prerequisite
- **WHEN** a prerequisite capability or required acceptance result is unknown
- **THEN** affected work is blocked with a reason, not reported successful or rerouted silently.
