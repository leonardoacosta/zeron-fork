# Specification: Omni model metrics

## ADDED Requirements

### Requirement: Omni metrics remain read-only and source-bound
The system SHALL inventory metric types exposed by the verified, read-only Omni contract, including request/attempt counts, tokens, cost, latency/duration, and errors when present. It SHALL identify Omni as the source. A source-reported metric may be included only when its provenance, semantics, units, interval, and aggregation are established. Unsupported or unknown metrics SHALL be marked unavailable, not estimated or fabricated. It SHALL NOT infer metrics from account quota or present generic gateway data as Omni data.

#### Scenario: API evidence is not established
- **WHEN** endpoint, authentication, schema, or read-only authorization has not been verified for the target Omni instance
- **THEN** metric collection remains unavailable/blocked
- **AND** the system does not guess an endpoint, schema, credential, or source

#### Scenario: Read-only query succeeds
- **WHEN** a user requests a metrics interval through an authorized read-only Omni integration
- **THEN** the result identifies Omni as its source and reports only measures supported by the verified contract
- **AND** no Omni write/control operation is issued

#### Scenario: Only account quota is available
- **WHEN** account quota data exists without per-call metrics provenance
- **THEN** the system does not count it as model requests, tokens, or cost

#### Scenario: Optional metric is unsupported or unverified
- **WHEN** a metric such as tokens, cost, latency, or errors is absent or its semantics/provenance are unverified
- **THEN** that metric is marked unsupported or unknown and unavailable
- **AND** no estimated or fabricated value is shown

### Requirement: Metrics preserve identity, time, units, and coverage
The system SHALL associate a measure with the provider/model identity and time interval reported for the measured call, plus source-defined units and observed coverage. It SHALL NOT use today's selected chat model as a substitute for historical routed identity. Unsupported or unknown identity SHALL remain explicitly unknown.

#### Scenario: Historical identity is available
- **WHEN** Omni supplies a verified immutable provider/model identity for a measured call
- **THEN** that identity is used for grouping the measure
- **AND** current chat selection does not rewrite the historical identity

#### Scenario: Identity or coverage is absent
- **WHEN** source evidence does not establish identity or complete coverage
- **THEN** results mark identity unknown or coverage partial/unknown as appropriate
- **AND** do not imply complete per-model totals

#### Scenario: Interval is shown
- **WHEN** metrics are displayed
- **THEN** the interval boundaries, timezone/precision as supported, measure definition, and units are visible or directly available with the result

### Requirement: Missing, stale, partial, and failed data are not zero
The system SHALL distinguish a genuine empty/zero result from unsupported, missing, partial, stale, and failed data. It SHALL label successful results with retrieval freshness and SHALL NOT silently replace failures with zeros or imply stale cached data is current.

#### Scenario: Source reports no events
- **WHEN** a successful, complete query returns no events for an interval
- **THEN** the system may report zero for that interval and measure
- **AND** identifies the source, interval, units, and complete coverage basis

#### Scenario: Optional measure is absent
- **WHEN** usage or another optional measure is missing from a source record
- **THEN** it remains unavailable rather than being coerced to zero

#### Scenario: Refresh fails with prior data
- **WHEN** refresh fails after a previous successful result exists
- **THEN** the prior result may remain visible with its last-success time and an explicit stale/error state
- **AND** it is not presented as current

#### Scenario: Refresh fails without prior data
- **WHEN** refresh fails and no successful result exists
- **THEN** the result is unavailable/error, not an empty or zero result

### Requirement: Aggregation resists retry and duplicate inflation
The system SHALL define counted entities and aggregate retries, continuations, cancellations, and failures only according to verified Omni semantics. It SHALL use source-backed stable identifiers for deduplication where available and SHALL disclose limitations where exactly-once accounting cannot be established.

#### Scenario: A read is retried or page repeats
- **WHEN** a retry or repeated page returns a record already observed
- **THEN** a stable source identity prevents duplicate counting where the contract supports it
- **AND** retries do not silently inflate totals

#### Scenario: Source cannot distinguish attempts
- **WHEN** Omni does not expose sufficient semantics or identifiers to distinguish attempts from completed turns
- **THEN** the system avoids labeling an attempt count as a turn/request count
- **AND** exposes the limitation or blocks that aggregate

### Requirement: Metrics do not expose secrets or conversation content
The system SHALL keep credentials out of metric records, UI, and logs, and SHALL NOT collect prompt, message, or tool bodies for aggregate metrics. Access to credentials SHALL follow the verified least-privilege read-only mechanism.

#### Scenario: Error includes sensitive response data
- **WHEN** an Omni response or request error includes credential material
- **THEN** logs and user-visible errors redact it
- **AND** credentials are not persisted with metric data

#### Scenario: Aggregate metrics are collected
- **WHEN** metrics are queried or stored
- **THEN** prompt, message, and tool bodies are not collected solely for metrics

## Non-functional acceptance

An authorized read-only integration acceptance test against the intended Omni instance is required after the API evidence gate passes. Fixture tests alone do not establish Omni compatibility. An authorized read-only integration acceptance test against the intended Omni instance is required after the API evidence gate passes. It verifies all supported metric categories and provenance/units; fixture tests alone do not establish Omni compatibility. Unsupported metrics remain explicitly unavailable. No metric may be inferred from quota or fabricated.
