# Jcode ACP requirement delta

## ADDED Requirements

### Requirement: Jcode is a first-class verified ACP agent
The application MUST represent Jcode with a stable identity and MUST use the existing ACP transport. It MUST expose only launch, authentication, model, and ACP capabilities verified for the pinned Jcode version. Jcode MUST NOT be offered as ready when executable detection, authentication, or handshake fails.

#### Scenario: Jcode is available and authenticated
- **WHEN** the pinned Jcode executable is detected, authentication succeeds, and the ACP handshake passes the approved verification contract
- **THEN** the application reports Jcode ready and allows selection of verified catalog/model choices
- **AND** it uses the existing ACP session path

#### Scenario: Jcode executable or authentication is unavailable
- **WHEN** executable detection or authentication fails
- **THEN** the application reports the specific not-installed or unauthenticated state
- **AND** it does not launch a session or claim readiness

#### Scenario: ACP negotiation is unsupported or unknown
- **WHEN** the handshake or a required capability is unsupported, times out, or is not verified for the pinned version
- **THEN** Jcode remains unavailable with an actionable reason
- **AND** the application does not guess a command, capability, or fallback agent

### Requirement: Jcode session lifecycle preserves ACP outcomes
The application MUST use the verified Jcode contract for new and resumed sessions. It MUST surface streamed output and cancellation outcomes, preserve existing permission authority checks, and MUST NOT silently replace a failed resume with a new session.

#### Scenario: Create and resume sessions
- **WHEN** a user creates or resumes a Jcode session
- **THEN** the application uses the same verified configuration and reports the actual session result

#### Scenario: Resume fails
- **WHEN** Jcode rejects or cannot load a saved session
- **THEN** the application reports resume failure
- **AND** it does not silently start a fresh session

#### Scenario: Cancel an active operation
- **WHEN** a user cancels an active Jcode operation
- **THEN** the ACP operation is cancelled using the verified protocol behavior
- **AND** the UI reflects the observed cancellation result

#### Scenario: Permission request is received
- **WHEN** Jcode requests permission for an operation
- **THEN** the application presents the request through existing authority controls
- **AND** unknown requests are not auto-approved

#### Scenario: Desktop and mobile readiness
- **WHEN** a user opens an agent selector on desktop or mobile
- **THEN** both surfaces expose the same Jcode identity and truthful readiness state

### Requirement: Jcode preserves existing skill behavior
Jcode MUST use the existing skill integration path, with only capabilities and command bindings verified for its pinned ACP version. This requirement does not add a dedicated skills browser.

#### Scenario: Verified skill support
- **WHEN** the pinned Jcode ACP advertises a skill-related capability supported by the existing integration
- **THEN** the application exposes that verified integration for Jcode

#### Scenario: Skill capability is absent or unverified
- **WHEN** skill support or command binding is absent or unverified
- **THEN** the application does not claim that Jcode supports it
- **AND** existing skill behavior for other agents remains unchanged
