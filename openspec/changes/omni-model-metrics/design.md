# Design: Omni-backed model metrics

## Decision

Treat Omni as the authoritative read-only metrics source only after its actual deployed API is verified. This change does not prescribe endpoint paths, payload fields, authentication, or storage schema. No Omni API contract is evidenced locally; those are hard prerequisites, not implementation guesses.

## Metric contract

Each displayed result must carry enough context to interpret it:

- **Source:** Omni and verified instance/environment identity, without exposing credentials.
- **Coverage:** queried interval, retrieval time, completeness/partial status, and any supported filters. Never imply full coverage without source evidence.
- **Identity:** provider and model as reported/correlated for the measured call. Do not substitute the currently selected chat model. Unknown identity is grouped as unknown, not guessed.
- **Measures:** inventory request/attempt counts, token usage, cost, latency/duration, errors, and other metrics the verified Omni contract exposes. Include a metric only with established source semantics, provenance, units, interval, and aggregation. Latency is only labeled as such when Omni's definition supports it; do not relabel wall-clock duration as provider latency.
- **Missingness:** unavailable, unsupported, partial, stale, empty/zero, and failed are distinct states. Never coerce absent usage into zero.
- **Time:** explicit interval boundaries, timezone, and timestamp precision from verified API contract.

Inventory every metric exposed by the verified Omni contract, including request/attempt counts, tokens, cost, latency/duration, and errors where present. Include source-reported metrics only when provenance, semantics, units, interval, and aggregation are established. Never estimate/fabricate unsupported metrics; mark each metric supported, unsupported, or unknown, and show unsupported data as unavailable. Quota is not request usage. The exact metric set remains contingent on evidence.

## Retrieval and correctness

Use only a documented read-only Omni operation and least-privilege authorization. The exact query shape, pagination, and consistency guarantees are unverified. Once evidence exists, use the source's stable record/correlation identifiers to deduplicate pages and retries. Do not claim exactly-once behavior without source guarantees. Distinguish request attempts, retries, continuations, cancellations, and failures according to verified source semantics. If those cannot be distinguished, report the limitation and avoid a misleading aggregate.

Do not collect request bodies, prompts, tool inputs/outputs, or unrelated headers. Keep credentials in the approved secret mechanism, redact them from logs/errors, and never persist them with metrics. Limit access and retention to the minimum required; exact retention policy must be verified before collecting data.

## Failure and freshness behavior

A refresh failure must not replace a valid result with zero or silently present cached data as current. Show the last successful retrieval time and stale status when retaining a prior result; otherwise show unavailable/error. Retry only transient read failures with bounded backoff after the real API's rate-limit and retry guidance is verified. Avoid multiplying counts on retries. Do not retry authentication/authorization or schema errors as if transient. No polling cadence is set until rate limits and freshness expectations are documented.

## Evidence gate

Before implementation, attach current sanitized evidence for the deployed Omni API: endpoint and API/version, read-only scope, credential source/rotation handling, full metric inventory and each field's provenance/semantics/units, timestamp/time-zone behavior, filtering/pagination, data coverage/retention, stable IDs and retry semantics, model identity provenance, rate limits, and representative success/partial/empty/error fixtures. Verify no write operation is used. If evidence is unavailable, this feature remains blocked pending user/provider clarification.

## Validation boundary

Local tests can validate rendering/aggregation against sanitized fixtures after the contract is established. They cannot prove Omni compatibility. Final acceptance requires an authorized, read-only test against the intended Omni instance, validating each supported metric's provenance and units alongside identity, interval, freshness, errors, partial/missing handling, deduplication/retries, and secret/body redaction. Do not claim end-to-end integration before that test passes.
