# Omni-backed model metrics

## Status

Pending review and approval. This proposal defines a read-only integration contract. Implementation is blocked until the Omni API and authorization prerequisites below are verified.

## What Changes

- Add an evidence-gated, read-only Omni metric inventory and presentation contract.
- Include only metrics whose source provenance, semantics, units, coverage, and aggregation are verified.
- Keep unsupported or unknown metrics explicitly unavailable.

## Why

Users need trustworthy usage and performance information for model calls routed through the confirmed Omni gateway. Existing account quota information is not a request ledger, and chat-turn duration is not upstream provider latency. The product must distinguish observed facts from absent or unverified data.

## Scope

- Read-only retrieval of Omni-sourced metrics for Omni-backed model calls.
- An inventory of metrics Omni actually exposes. Any source-reported request, token, cost, latency, duration, or error metrics may be included only when the verified contract establishes their meaning, units, and provenance.
- Model grouping only from immutable provider/model identity captured for the measured call, never the current chat selection.
- Explicit source, time window, units, coverage, missing-data, error, and staleness semantics.
- Secure handling of credentials and metric data, and resilient retry/deduplication behavior.

## Not in scope

- A generic gateway dashboard, gateway deployment/configuration, or write/control operations against Omni.
- Inferring or estimating request metrics, billable usage, tokens, cost, latency, or errors when Omni does not report them with verified semantics.
- Treating optional assistant-turn duration as provider latency, or missing measurements as zero.
- Prompt, tool, or message-body collection for aggregate metrics.
- MCP integration or any unrelated provider/integration changes.

## API evidence boundary and prerequisite

No verified Omni endpoint, deployment/version contract, authentication mechanism, metric schema, request/attempt correlation key, or coverage guarantee is established by repository evidence. Do not guess or hard-code one. Before implementation, obtain current, authorized evidence for the deployed Omni instance: documented/read-only endpoint and scope, supported authentication and secret source, response schema and units, time/filter semantics, pagination, timestamp timezone/precision, completeness and retention, model identity meaning, retry/continuation aggregation, and failure behavior. Record safe sanitized fixtures and prove the access is read-only. If those facts cannot be established, keep collection blocked and revise this proposal rather than inventing API behavior.

## Acceptance outcomes

- The dashboard labels metrics as Omni-sourced and distinguishes measured facts from unavailable or unsupported quantities.
- Counts and durations have explicit time range, units, source, coverage, and freshness.
- Missing, partial, stale, and errored results remain visibly distinct from zero.
- Retries and duplicate pages/polls do not inflate request/turn counts; aggregation follows the verified Omni contract.
- No secret, prompt, tool body, or raw credential is persisted or rendered.
- A source inventory explicitly marks each considered metric supported, unsupported, or unknown. Unsupported metrics are visibly unavailable, never estimated or fabricated. A later authorized read-only acceptance test against the verified Omni environment proves the contract end to end before the feature is called integrated.
