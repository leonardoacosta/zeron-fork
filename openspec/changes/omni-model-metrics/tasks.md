# Tasks: Omni-backed model metrics

Tasks are dependency ordered. All implementation tasks are blocked until Task 1 records sufficient authorized API evidence and Task 2 translates that evidence into an agreed contract. Keep this change proposal pending review/approval; planning this sequence is not implementation authorization.

- [ ] 1. Verify Omni read-only API evidence (BLOCKING)

- **Scope:** Identify the intended Omni instance/version and obtain current, authorized documentation or equivalent evidence for endpoint, read-only permission, authentication/secret source, schema, timestamps/timezone, units, supported measures, filters/pagination, completeness/retention, stable IDs, model identity, retry/continuation/failure semantics, rate limits, and errors.
- **Verify:** Produce a sanitized evidence record and representative success, partial, empty, and error fixtures. Demonstrate the chosen operation is read-only without exposing credentials. If API access or evidence is unavailable, record the missing facts and stop downstream work for user/provider clarification.
- **Dependency:** None. This is a discovery gate, not permission to provision credentials or perform writes.

- [ ] 2. Resolve data contract and acceptance scope (BLOCKED by 1)

- **Scope:** Map only evidence-backed Omni fields to measures, identity, intervals, units, coverage, missingness, freshness, and aggregation behavior. Choose the first-release metric set from the Task 1 inventory and evidence-backed Task 2 contract; do not exclude metric categories in advance. For every considered metric, mark supported, unsupported, or unknown. Unsupported metrics are explicitly unavailable, not estimated. If no useful metric has verifiable provenance and semantics, stop for clarification rather than fabricate values.
- **Verify:** Review mapping against sanitized fixtures; ensure no unsupported endpoint/schema/auth assumptions remain and every metric has defined entity, source, unit, interval, and missing-data behavior.
- **Dependency:** Task 1 complete. API/schema/auth uncertainties must be resolved here, not guessed in code.

- [ ] 3. Implement authorized read-only retrieval and safe result states (BLOCKED by 2)

- **Scope:** Implement the evidence-backed read path and least-privilege credential handling. Preserve source, metric inventory/support status, coverage, interval, identity, units, freshness, partial/missing/error state. Do not collect conversation bodies or log credentials.
- **Verify:** Test each metric surfaced as supported against its documented provenance, units, interval, and semantics. Tests cover success, empty, partial, missing optional values, unsupported metrics, stale prior result, no-prior-result error, auth/schema failure, and redaction. Assert no write request is made.
- **Dependency:** Task 2 approved; no endpoint or auth implementation until verified contract exists.

- [ ] 4. Implement source-semantic aggregation and deduplication (BLOCKED by 2)

- **Scope:** Aggregate only verified entities and use verified stable IDs for retries/repeated pages. Correctly represent attempts, continuations, cancellations, and failures to the extent Omni evidence permits. Block or label aggregates when semantic distinction is unavailable.
- **Verify:** Fixture tests prove repeated pages/retries do not inflate supported counts and unknown semantics do not appear as precise totals.
- **Dependency:** Task 2. Do not invent exactly-once or per-request accounting guarantees.

- [ ] 5. Present Omni metrics with truthful context (BLOCKED by 3 and 4)

- **Scope:** Present the evidence-backed metric inventory and each metric's supported/unsupported/unknown state. Expose supported measures with Omni source, model identity provenance, interval, units, coverage, freshness, and explicit unavailable/partial/error states. Do not build generic gateway controls or MCP integration.
- **Verify:** UI tests demonstrate unknown identity, missing values, zero versus unavailable, partial coverage, and stale/error distinction; no provider latency, token, or cost claim exceeds verified evidence.
- **Dependency:** Tasks 3 and 4.

- [ ] 6. Run end-to-end read-only Omni acceptance (BLOCKED by 1–5)

- **Scope:** Exercise the implemented flow against the intended, authorized Omni instance using approved read-only access.
- **Verify:** Validate each supported metric's provenance, units, and totals alongside source, identity, interval, timezone, coverage, freshness, partial/empty/error behavior, retry/deduplication, and secret/body redaction. Unsupported metrics remain unavailable. If external access is unavailable, report acceptance blocked; fixture success is not a substitute.
- **Dependency:** Tasks 1–5 and approval of the change. Do not claim integration is complete before this check passes.
