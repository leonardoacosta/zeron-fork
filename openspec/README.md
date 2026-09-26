# Fork change workflow

Adopted with user approval on 2026-09-26. Product requirements remain in
[`docs/fork-prd.md`](../docs/fork-prd.md). The roadmap below sequences work, not execution authorization.

Use `feature` to author `changes/<slug>/proposal.md`, `design.md`, `specs/<capability>/spec.md`,
and `tasks.md`. Review the written artifacts before using `apply` for a named change.
Use `apply:all` only for an explicitly selected ordered queue. Do not maintain a second task ledger.
No deployment, external write, credential provisioning, or spend follows from this workflow binding.

## Approved roadmap boundaries

Detailed decomposition proposed on 2026-09-26: [PRD execution map](changes/prd-execution-map/design.md).
It maps all 19 requirements into 35 bounded new change contracts plus existing assignment-record,
with ten integration rounds and mandatory CI before every iteration/round promotion.
Child contracts are discovery/refinement-ready, not blanket implementation approval.
Start with `ci-promotion-gates`; exact implementation tasks must pass refinement and review before `apply`.
The phase table and baseline classifications below are historical context, not current readiness claims.

Each row contains multiple separately designed changes. Only assignment-record has a detailed design.

| Phase | Feature boundaries and dependency order | Requirements | Exit evidence |
| --- | --- | --- | --- |
| Safe investigations | Assignment records without execution; profile and access enforcement; harness capability/preflight and confirmed stopping/recovery; manually launched investigations with versioned findings and configured acceptance | ZF-01–04, ZF-14–15; investigation subset of ZF-05–06 | Real investigation survives restart and agent replacement, obeys access limits, confirms stopping, and ends with checked findings rather than an unsupported completion claim |
| Verified engineering | Versioned configurable workflows and selection; revision-bound candidates; separate verification and acceptance; independently callable authorized delivery actions | ZF-05–07, ZF-14–15 | Changed revisions invalidate dependent evidence/approval; delivery reconciles uncertain external effects before retry; acceptance never implies blanket delivery authority |
| Coordinated work | Conflict observer and prioritized backlog including direct sessions; accepted-output dependencies; repository-scoped children and combined outcomes | ZF-09–13 | Unrelated work continues, conflicts wait, urgent priority does not preempt, and exact delivered child versions satisfy parent checks |
| Later capabilities | Opt-in triggers after admission controls; explicit comparisons after isolation/budgets; scoped browser integration; grouped alerts and configurable briefings | ZF-08, ZF-16–18 | Duplicate triggers do not duplicate launches; comparisons never change routing or deliver automatically; browser authentication grants no mutation authority; alerts grant no resume authority |

ZF-19 integration research runs alongside these phases. Each adapter ships only with capability,
authorization, version, and real-workflow evidence. GitHub/ADO/MCP/Aperture availability is not authority.
Jcode/Herdr and SystemOne remain distinct integration investigations. Unknown APIs, browser provider,
full release lifecycle, and attribution remain scoped research gaps, not assumed implementations.
Safety-critical exception reporting belongs with the feature that needs it, not only the later briefing feature.
No numeric targets or calendar estimates have been approved.

## Baseline and reuse

Static inspection baseline: `03b67be`, shallow checkout. No builds or runtime acceptance performed
during planning. Preserve Rust engine, typed RPC, GPUI desktop, Swift iOS, session Loro documents,
and current registry transport. The registry is a current-state LWW index, not an assignment history store
(`docs/registry-sync.md:16–28`). Existing Local/Synced/Development scopes are not the requested work profiles.

| Requirements | Baseline classification | Evidence and missing behavior |
| --- | --- | --- |
| ZF-01 | Partial | `ARCHITECTURE.md`, `crates/proto/src/workspace.rs:44–61`, `apps/ios/`: multi-device foundation exists; delegation does not |
| ZF-02 | Partial | `crates/engine/src/lib.rs:221–283`: profile-scoped store/journals, device-scoped repos/accounts; no full work-context boundary |
| ZF-03 | Missing | Existing session/registry model has no persistent delegated objective; assignment-record is the first change |
| ZF-04 | Partial | `crates/engine/src/lib.rs:247–252`: stale recovery exists; continuing authorization and actual-stop proof need separate work |
| ZF-05–06 | Missing | No approved versioned workflow/selection model identified |
| ZF-07 | Partial | `crates/engine/src/change_requests.rs:87–148`, `source_control.rs:1492–1511`: PR status is not authorized delivery orchestration |
| ZF-08 | Partial | `crates/mcp/src/tools.rs:57–189,530–686`: chat lifecycle entry points, not provenance-bound workflow triggers |
| ZF-09–13 | Missing | No assignment conflict observer, priority backlog, accepted-output dependency graph, or parent outcome model identified |
| ZF-14 | Partial | Existing run journals/transcripts provide raw material, not revision-bound evidence and acceptance |
| ZF-15 | Partial | `crates/harness/`: adapters exist; preferred integrations, frozen resource bindings, and stop guarantees need verification |
| ZF-16 | Missing | Git diff/compare is not an isolated engineering comparison |
| ZF-17 | Unknown | `crates/ui/src/browser/` exists; assignment/profile-scoped isolation and authorization not established |
| ZF-18 | Partial | `crates/ui/src/notify.rs:33–48,87–126`: notifications exist; grouped exceptions and profile briefing schedules missing |
| ZF-19 | Partial | GitHub status and `crates/mcp/` exist; exact ADO/Aperture and other integration readiness unverified |

These are source-based planning classifications, not exhaustive absence proofs or runtime acceptance.
The baseline map is preliminary: missing-feature classifications identify gaps in inspected surfaces,
not an exhaustive repository audit. Per-requirement test coverage mapping remains to be completed in
each feature's discovery. Existing tests were inspected or located, not executed for this roadmap.

## Current change

[`assignment-record`](changes/assignment-record/proposal.md): written specification approved for execution
on 2026-09-26 at 08:29 UTC. Later phases require their own feature design and approval.
