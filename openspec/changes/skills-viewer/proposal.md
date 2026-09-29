# Host-scoped skills viewer

Status: proposed; approval pending. This proposal authorizes planning only. Do not begin implementation before approval.

## Why

Users need to inspect discovered skills and understand their origin, precedence, and content availability. The composer catalog is not a dedicated scoped browser and may omit shadowed entries. Host context matters because an advertised path may belong to a remote machine.

## What Changes

Add a read-only viewer for discovered skills at global/user and project scope. It uses the existing engine discovery path and makes the selected host, harness, and project context explicit. Show each skill's scope, provenance, effective or shadowed status, description, and content availability. Provide bounded content reads through the selected host's supported RPC boundary when available. Never interpret a remote-host path as a local-machine path.

Cover desktop and mobile surfaces in the initial delivery. Keep Jcode integration conditional on independently verified Jcode host discovery support. The viewer must also work with existing supported hosts and must not make Jcode a hidden dependency.

Preserve current skill discovery and composer completion behavior.

## Impact

Expected impact is limited to the existing harness discovery, engine/protocol RPC, desktop UI, and mobile UI/test surfaces, confirmed during implementation discovery. Remote content is permitted only through a selected-host RPC boundary with host-bound identity, authorization, path/root policy, and bounded reads. Hosts without a supported read boundary show metadata and an explicit unavailable state.

## Out of scope

No skill creation, editing, deletion, enabling, installation, execution, synchronization, or changes to completion semantics. No remote filesystem reads through local paths. No arbitrary filesystem browsing. No MCP work or MCP dependency. No change to provider support, Jcode harness onboarding, Omni metrics, or unrelated active changes.

## Outcome

Users can inspect global skills without an invented project directory, switch to a specific project context, understand discovery source and shadowing, and read eligible content safely. Remote, missing, unreadable, stale, oversized, or unsafe content produces an explicit state instead of a misleading preview. Existing completion remains unchanged.

## Approval boundary

This change remains pending approval. Implementation depends on verifying the current discovery response shape and identifying the host-aware content-read boundary. Jcode-specific coverage is conditional; failure to verify Jcode does not block viewer delivery for other supported hosts.

## Acceptance evidence

- Automated tests cover provenance, effective/shadowed entries, global versus project scope, bounded safe reads, remote and error states, and completion regression.
- Desktop and mobile tests or equivalent UI coverage show explicit scope/context and accessible navigation and content states.
- Existing skill-discovery and completion regression suites pass.