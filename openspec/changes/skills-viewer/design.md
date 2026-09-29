# Design: host-scoped skills viewer

## Context

The harness already discovers provider, user/global, and project skills. The engine exposes `ListSkills` for the composer catalog, whose effective result may hide shadowed entries. A viewer needs inventory provenance that the current response may not preserve. Native host-advertised skills may not have readable local files. A displayed path alone is not proof that a local file belongs to the selected host or an approved discovery root.

## Design decisions

### Discovery and context

Reuse the current engine discovery implementation and its root/precedence rules. Add or extend an inventory response only as needed to preserve all discovered entries and their explicit metadata: stable identity, display name, scope, origin/provenance, effective/shadowed state, description, content availability, and host identity. Do not infer these fields from a path in the UI.

Every view is bound to a selected host and harness. The global view has no project-directory requirement. The project view requires an explicit current project context, displays that context, and does not silently fall back to an arbitrary working directory. A context change refreshes discovery and invalidates prior selection/content state. Surface partial discovery errors without hiding successful independent scopes.

Jcode-specific discovery is enabled only if host capabilities and discovery behavior are verified. Other hosts remain usable without Jcode installed or selected.

### Safe content read

Expose content reads only for entries whose content is available through the selected host's supported RPC or local boundary. Validate identity and host binding server-side. For remote hosts, send reads through that host's RPC boundary and never pass its path to local filesystem APIs. For local hosts, canonicalize the target and approved discovery roots; reject paths outside those roots and symlinks that resolve outside them. Hosts without a supported read boundary report metadata-only availability.

Bound bytes read, scan/traversal work, and response size. On limit, permission denial, disappearance, stale identity, unsupported read, or unsafe path, return a typed result that the UI can explain. Do not return partial content as if complete. Markdown is untrusted text: render as inert, escaped text, not executable HTML or instructions.

### User interface

Provide a dedicated, read-only viewer on desktop and mobile. Show host and harness selectors/context, global and project scope selection, project context when applicable, and a filterable skill list. Each list entry shows name, description, provenance, and effective/shadowed status. Details show content or a reason it is unavailable. Loading, empty, partial-error, permission, remote, stale, and size-limit states are distinct.

Keyboard navigation and screen-reader labels cover context controls, list selection, status, and content. Focus moves predictably when scope or selected skill changes. Mobile uses the same information hierarchy with compact navigation and a back path from detail to list.

### Compatibility and safety

Do not change the composer completion catalog or dispatch semantics. Add an explicit regression check that completion still lists and delivers existing discovered commands/skills independently. Do not add MCP behavior. Do not require Jcode for build, tests, startup, or the baseline viewer.

## Candidate implementation surfaces

- `crates/harness/src/skills.rs`: discovery roots, precedence, and inventory metadata.
- `crates/engine/src/rpc.rs`: skill RPC surface and authorization/context binding.
- `crates/engine/src/lib.rs` and engine host/discovery modules: host-aware request flow, only where the existing boundary requires it.
- `crates/proto`: typed inventory and bounded-read request/results if wire types are needed.
- `crates/ui`: desktop viewer and UI state/accessibility.
- Mobile UI crate and its navigation/tests: corresponding initial mobile surface.
- `crates/harness/src/skills.rs` tests around lines 699-916 and `crates/engine/tests/rich_composer_delivery.rs` around lines 415-474 are regression anchors from exploration; revalidate before implementation.

Exact ownership and mobile module paths must be confirmed during implementation discovery before source edits. Do not broaden the change into unrelated provider, ACP/Jcode, or Omni surfaces.

## Risks and mitigations

- Effective-only discovery can erase shadowed entries. Preserve an inventory distinct from the completion list.
- A path can be stale or forged. Resolve from server-owned discovered identity and revalidate at read time.
- Host confusion can expose unrelated local content. Bind every request to host identity and authorization; use selected-host RPC for supported remote reads and never pass a remote path to local file APIs.
- Large or changing files can exhaust resources or mislead. Bound reads and return typed stale/limit failures without partial preview.
- Markdown can carry hostile markup or prompt text. Display as inert escaped text and do not treat it as trusted instructions.
- Jcode APIs may differ. Gate Jcode-specific behavior on verification while keeping the viewer host-agnostic.

## Verification approach

Unit tests for scope/provenance/precedence and read boundary; RPC tests for host authorization, remote/absence/permission/stale/limit outcomes; UI tests for desktop/mobile states and accessibility semantics; regression tests for unchanged completion. Run focused crate tests and repository-required checks for touched Rust crates. No implementation or runtime claim is made by this proposal.