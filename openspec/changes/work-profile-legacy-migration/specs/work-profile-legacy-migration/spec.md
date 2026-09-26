# Explicit non-destructive work-profile migration

## ADDED Requirements

### Requirement: Bounded profile change
The system SHALL satisfy: Migrate only explicitly selected legacy source to a new named-profile target with verified identity, non-destructive staged copy, content manifest and atomic publication. Preserve original data; no credentials copied. Interrupted or ambiguous migration remains non-executable. Imported runs require safe resume authorization, never automatic journal replay.

#### Scenario: C01
- **GIVEN / WHEN / THEN** No explicit source/target binding: legacy source stays unchanged and execution held.

#### Scenario: C02
- **GIVEN / WHEN / THEN** Crash during staged copy: destination is not published ready and source remains intact.

#### Scenario: C03
- **GIVEN / WHEN / THEN** Source changes or target already exists: reject without overwrite or merging profiles.

#### Scenario: C04
- **GIVEN / WHEN / THEN** Verified copied data is published atomically, but copied run journals do not auto-resume.
