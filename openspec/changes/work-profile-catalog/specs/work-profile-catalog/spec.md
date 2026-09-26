# Validated profile identity and owner catalog

## ADDED Requirements

### Requirement: Bounded profile change
The system SHALL satisfy: Define validated opaque profile identity, display metadata and revision types plus owner-local principal-scoped catalog persistence. Create/rename use atomic per-profile CAS and actor/principal-scoped exact replay receipts. This foundation provides no runtime authority, no daemon attachment, no sync namespace, and no legacy execution permission.

#### Scenario: C01
- **GIVEN / WHEN / THEN** Invalid UUID/revision/name rejects during wire decoding before catalog write.

#### Scenario: C02
- **GIVEN / WHEN / THEN** Same operation identity and payload replays exact result; changed payload conflicts without mutation.

#### Scenario: C03
- **GIVEN / WHEN / THEN** Two connections rename the same revision: exactly one wins, history of receipts survives reopen.

#### Scenario: C04
- **GIVEN / WHEN / THEN** Late SQL failure rolls back row and receipt; future schema rejected without modifying database.
