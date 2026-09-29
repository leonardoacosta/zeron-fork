# Design: verified Jcode ACP integration

## Decision

Represent Jcode with a stable harness identity and route it through the existing ACP client. Do not create a parallel runner. Jcode readiness, catalog, and available operations must be based on behavior verified for a pinned CLI version, not assumptions imported from another ACP agent.

## Bounded capability verification gate

Local evidence is limited to `jcode --version` reporting `v0.88.146-dev (f92c40053)` and successful `jcode acp --help`, which describes a daemon-backed ACP adapter and `--provider`. This does not establish wire compatibility, negotiated version, launch arguments, authentication, permission semantics, cancellation, or session behavior.

Before implementing the harness, perform a bounded, read-only verification against that exact CLI build using current Jcode documentation and an authorized harmless handshake in a disposable session. Record invocation, negotiation, readiness/auth behavior, session-new and session-load behavior, streaming, cancellation, permission request/response behavior, and relevant advertised capabilities. Do not configure MCP servers or invoke side-effecting tools. Bound timeouts and ensure child processes terminate.

If handshake or any required behavior is unavailable or ambiguous, stop Jcode implementation and return for design refinement. Do not infer compatibility from help text. A passing check applies only to the pinned version; future versions require re-verification.

After the gate, implement deterministic executable detection and truthful not-installed, unauthenticated, and ready states. Catalog/model selection must reflect verified options. New and resumed sessions use the same verified configuration. Resume failure remains an error and must not silently start a new session. Cancellation surfaces the observed result. Permission requests retain existing authority checks and never auto-approve unknown operations. Desktop and mobile expose equivalent identity and readiness.

## Coordination boundary

Provider retirement, a dedicated skills viewer, and Omni integration/metrics have separately owned sibling proposals. This change may coordinate at shared integration surfaces, but does not own those behaviors and must not impose hard dependencies on those sibling changes. No MCP functionality or dependency is part of this proposal.

## Surfaces to revalidate before implementation

Inspect the existing harness identity enum and serialization, ACP transport, harness catalog/detection/auth paths, engine readiness/RPC, desktop and mobile selectors, and the relevant ACP and migration tests. Keep implementation within the Jcode ownership boundary and avoid modifying another proposal's task ledger.
