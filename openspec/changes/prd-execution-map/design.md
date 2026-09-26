# PRD execution map and CI promotion protocol

## Readiness and authority

Baseline inspected: `1427da6`. Existing assignment code commits `1581575`, `8f301e1`, test reinforcement `34ea27b`. Local runtime/deployment evidence is recorded in `openspec/changes/assignment-record/tasks.md`; do not reproduce machine-specific evidence as universally available CI artifacts.

33 new change boundaries plus existing assignment-record cover19 PRD requirements. **No new child is implementation-ready yet.** Each has a fully bounded behavior contract and executable refinement steps. This prevents weak executors from inventing an interface for unresolved research. Refine one named change with `feature`, make its tasks code-complete under `writing-plans`, then approve/admit through `apply`. Only an explicitly selected queue can use `apply:all`.

`units.json` contains immutable planning metadata, not completion state. Child tasks.md files are the only execution checklists. This document is the dependency/coverage index. Updating a unit's contract requires updating its metadata and validating agreement.

## Evidence baseline, not completion percentages

- ZF01: native Mac/homelab owner routing and persistent local services exercised. Does not establish every desktop/mobile flow.
- ZF03: assignment records/history/replacement links implemented. No delegated workflow execution or assignment UI yet.
- ZF02: account/transport storage separation exists; full named work-profile authorization not established.
- ZF14: assignment revision/review fields exist, not complete evidence provenance or acceptance gating.
- Remaining requirements are existing partial primitives or proposed features. Read original PRD historical research caveats: Codex sandbox handling, Claude/ACP auto-approval, recovery authorization, device-level credential sharing and unknown usage need revalidation at exact current source.
- CI definition now requires fmt and clippy. Neither new checks' hosted success nor a clean all-platform baseline has been demonstrated here. R0 must make that fact explicit and resolve failures, not exempt them.

## Round dependency table

A round is an integration boundary, not an estimate or permission to run all changes concurrently. Units can refine in parallel, but implementation may overlap only with disjoint resources/interfaces or explicit coordinated ownership. Shared rpc.rs/store.rs/proto/UI edits demand one integration owner and combined checks. Later-round research can be read-only; no later-round implementation promotion before prerequisite and preceding-round CI.

| Round | Purpose | Changes | Promotion acceptance |
|---|---|---|---|
| R0 | CI and distribution baseline | [ci-promotion-gates](../ci-promotion-gates/proposal.md), [dependency-attribution](../dependency-attribution/proposal.md) | CI-R0: all unit acceptance + integrated union of checks on same commit; no unresolved prerequisite |
| R1 | Profile identity and verified research | [work-profile-boundary](../work-profile-boundary/proposal.md), [integration-harness-observer-research](../integration-harness-observer-research/proposal.md), [integration-github-ado-research](../integration-github-ado-research/proposal.md), [integration-browser-research](../integration-browser-research/proposal.md), [foundation-compatibility](../foundation-compatibility/proposal.md) | CI-R1: all unit acceptance + integrated union of checks on same commit; no unresolved prerequisite |
| R2 | Authority, preflight and evidence | [profile-access-enforcement](../profile-access-enforcement/proposal.md), [harness-preflight-binding](../harness-preflight-binding/proposal.md), [revision-evidence-bindings](../revision-evidence-bindings/proposal.md) | CI-R2: all unit acceptance + integrated union of checks on same commit; no unresolved prerequisite |
| R3 | Stop, budgets and workflow selection | [run-resource-ledger](../run-resource-ledger/proposal.md), [confirmed-stop-handoff](../confirmed-stop-handoff/proposal.md), [workflow-version-selection](../workflow-version-selection/proposal.md) | CI-R3: all unit acceptance + integrated union of checks on same commit; no unresolved prerequisite |
| R4 | Recovery, acceptance and safety exceptions | [safe-resume-reconciliation](../safe-resume-reconciliation/proposal.md), [verification-acceptance-gates](../verification-acceptance-gates/proposal.md), [exception-attention](../exception-attention/proposal.md) | CI-R4: all unit acceptance + integrated union of checks on same commit; no unresolved prerequisite |
| R5 | First bounded investigation and concrete adapters | [manual-investigation-runner](../manual-investigation-runner/proposal.md), [integration-provider-adapters](../integration-provider-adapters/proposal.md) | CI-R5: all unit acceptance + integrated union of checks on same commit; no unresolved prerequisite |
| R6 | Desktop use, delivery ledger and conflict admission | [assignment-desktop-surface](../assignment-desktop-surface/proposal.md), [delivery-effect-ledger](../delivery-effect-ledger/proposal.md), [conflict-admission-observer](../conflict-admission-observer/proposal.md), [engineering-stage-runner](../engineering-stage-runner/proposal.md) | CI-R6: all unit acceptance + integrated union of checks on same commit; no unresolved prerequisite |
| R7 | Mobile parity, actions, dependencies, backlog and browser | [assignment-mobile-parity](../assignment-mobile-parity/proposal.md), [git-delivery-actions](../git-delivery-actions/proposal.md), [release-deploy-publish-actions](../release-deploy-publish-actions/proposal.md), [priority-backlog](../priority-backlog/proposal.md), [accepted-output-dependencies](../accepted-output-dependencies/proposal.md), [scoped-browser-capability](../scoped-browser-capability/proposal.md) | CI-R7: all unit acceptance + integrated union of checks on same commit; no unresolved prerequisite |
| R8 | Multi-repo children, triggers, comparisons and briefings | [multi-repository-breakdown](../multi-repository-breakdown/proposal.md), [opt-in-trigger-launch](../opt-in-trigger-launch/proposal.md), [engineering-comparisons](../engineering-comparisons/proposal.md), [profile-briefings](../profile-briefings/proposal.md) | CI-R8: all unit acceptance + integrated union of checks on same commit; no unresolved prerequisite |
| R9 | Combined outcome | [combined-outcome-checks](../combined-outcome-checks/proposal.md) | CI-R9: all unit acceptance + integrated union of checks on same commit; no unresolved prerequisite |

Research siblings do not select providers silently. `integration-provider-adapters` must fan out into reviewed provider-specific child changes before code. Those exact adapter dependencies must be added to consumers before they become ready; an umbrella research result is not an implemented provider.

Early runner acceptance before conflict admission exists is restricted to an explicitly isolated, single-run test scope. Do not advertise production concurrent admission from R5/R6 runner success. If an early runner can coexist with direct sessions on shared resources, it must enforce a conservative affected-resource hold or depend on `conflict-admission-observer`; it may not silently launch overlapping work. This restriction is not permission to globally serialize unrelated work in the final product.

## Complete requirement mapping

| PRD | Primary units | Must-not-lose clauses |
|---|---|---|
| ZF-01 | `ci-promotion-gates`, `dependency-attribution`, `foundation-compatibility`, `assignment-desktop-surface`, `assignment-mobile-parity` | Preserve direct sessions and multi-device clients; delegation additive |
| ZF-02 | `work-profile-boundary`, `profile-access-enforcement`, `harness-preflight-binding`, `assignment-desktop-surface`, `conflict-admission-observer`, `scoped-browser-capability`, `multi-repository-breakdown` | Extensible work profiles; no Brown access by label; no silent account/tool/environment substitution; external authority preserved |
| ZF-03 | `foundation-compatibility`, `revision-evidence-bindings`, `manual-investigation-runner`, `assignment-desktop-surface`, `assignment-mobile-parity` + existing `assignment-record` | Explicit promotion; objective/actions/sessions/findings/evidence/reviews/questions; replacement preserves history/permissions; findings-only outcome |
| ZF-04 | `confirmed-stop-handoff`, `safe-resume-reconciliation`, `exception-attention`, `assignment-desktop-surface`, `delivery-effect-ledger`, `assignment-mobile-parity`, `scoped-browser-capability` | Pause then actual stop then takeover then explicit handback; safe authorized recovery; uncertainty holds; unrelated work continues |
| ZF-05 | `workflow-version-selection`, `verification-acceptance-gates`, `manual-investigation-runner`, `assignment-desktop-surface`, `engineering-stage-runner` | Understand/Investigate/Propose/Implement/Verify/Deliver/Confirm outcome; independent customization; optional updates; pinned active version |
| ZF-06 | `workflow-version-selection`, `manual-investigation-runner`, `assignment-desktop-surface`, `assignment-mobile-parity`, `opt-in-trigger-launch` | Repository default before profile default; explicit override cannot bypass access; explain before launch; trigger explicit binding |
| ZF-07 | `integration-github-ado-research`, `delivery-effect-ledger`, `git-delivery-actions`, `release-deploy-publish-actions` | Push/PR/merge/release/deploy/publish independent; configured autonomy not universal confirmation; acceptance not delivery authority |
| ZF-08 | `manual-investigation-runner`, `opt-in-trigger-launch` | Manual and opt-in triggers; approval or authorized launch; provenance/dedupe; no auto comparisons |
| ZF-09 | `integration-harness-observer-research`, `exception-attention`, `conflict-admission-observer`, `priority-backlog`, `opt-in-trigger-launch` | Assumptions/resources/dependencies not just files; direct sessions; limited visibility; scope/boundary rechecks; uncertainty reviewer; observer no authority |
| ZF-10 | `confirmed-stop-handoff`, `priority-backlog`, `opt-in-trigger-launch` | Eligible priority then oldest; Leo override; no silent priority change/preemption; blocked item not global block; confirmed stop required |
| ZF-11 | `verification-acceptance-gates`, `accepted-output-dependencies` | Exact accepted stage-output versions; upstream changes invalidate/reassess; independent overlap |
| ZF-12 | `run-resource-ledger`, `multi-repository-breakdown`, `combined-outcome-checks` | Parent and repository children retain independent bindings; review/autonomy controlled breakdown; editable within scope/profile/budget; not simultaneous deploy |
| ZF-13 | `combined-outcome-checks` | Combined checks over exact delivered children; child done insufficient; partial delivery and independent continuation; no superseded substitution |
| ZF-14 | `ci-promotion-gates`, `revision-evidence-bindings`, `safe-resume-reconciliation`, `verification-acceptance-gates`, `assignment-desktop-surface`, `delivery-effect-ledger`, `engineering-stage-runner`, `assignment-mobile-parity`, `accepted-output-dependencies`, `scoped-browser-capability`, `engineering-comparisons`, `combined-outcome-checks` | Distinct completion/verification/acceptance/delivery; dirty tree/config/auth/resources/native IDs; redacted observations; stale/contradictory/missing evidence blocks; structural/synthetic/real labels |
| ZF-15 | `integration-harness-observer-research`, `profile-access-enforcement`, `harness-preflight-binding`, `run-resource-ledger`, `confirmed-stop-handoff`, `integration-provider-adapters`, `engineering-stage-runner`, `multi-repository-breakdown`, `engineering-comparisons` | Jcode/Herdr preferences not readiness; observer distinct; preflight, configuration, resources, native IDs, stop, evidence/usage; unknown cost not zero; ordinary single engineer |
| ZF-16 | `run-resource-ledger`, `engineering-comparisons` | Explicit task/entrants/budget; identical isolated baseline; independent correctness; infra failure distinct; recommend only; Leo changes routing; no automatic delivery |
| ZF-17 | `integration-browser-research`, `scoped-browser-capability` | Default isolation; explicit scoped signed-in access; auth not mutation authority; redaction; no provider/account fallback |
| ZF-18 | `exception-attention`, `assignment-desktop-surface`, `conflict-admission-observer`, `profile-briefings` | Grouped exceptions now, routine activity, profile schedule/destinations; alerts do not accept/resume |
| ZF-19 | `dependency-attribution`, `integration-harness-observer-research`, `integration-github-ado-research`, `integration-browser-research`, `profile-access-enforcement`, `integration-provider-adapters`, `git-delivery-actions`, `release-deploy-publish-actions` | GitHub/ADO/MCP/Aperture need exact evidence; external authority retained; local storage optional; availability not blanket permission |

## Mandatory CI phase: every iteration, then every integrated round

1. **Admission:** named change approved, exact prerequisites promoted, contract frozen, required tests/platforms listed in its tasks. Baseline commit and working tree recorded. Never inherit CI from another branch or from an older dependency version.
2. **Red/green development:** run the actual public-boundary failing test, show expected behavioral failure rather than compile error as sole red proof; implement minimum change; rerun relevant tests. Unsupported external capability is blocked, not mocked into a pass.
3. **Iteration CI:** execute core plus affected feature/platform checks on exact candidate. An iteration cannot promote to the next stage with a required failing, skipped, missing, cancelled or stale job. Fix the root cause or stop at the gate. Red-phase expected failure is not a promotion pass.
4. **Independent review:** compare every requirement clause to assertion and observed output. Review evidence for invented execution, copied-source harnesses, weak checks, wrong profile, authority widening, concurrency, retries, rollback and native compatibility.
5. **Integrated-round CI:** integrate authorized units, then rerun union of their checks against one revision. Individual green runs do not prove merged compatibility. Every edit, including integration/conflict resolution, invalidates affected prior evidence. No next round starts implementation until barrier CI-Rn passes.
6. **Persist result:** child tasks.md records commit/tree, command, platform, test selected/passed/ignored counts, exit status, environment, evidence path or CI run/job URL, requirement/scenario mapping, and blocked conditions. Never check a box from aggregate counts alone. No side completion ledger.
7. **Promotion:** reviewer verifies exact tested commit, all prerequisites and required native acceptance. CI green is necessary, not sufficient for product acceptance. After promotion, downstream may consume exact accepted outputs. New upstream changes require reassessment.

### Core local reproduction commands (repository root)

These mirror/extend current CI targets. They are commands to run during authorized implementation, not results claimed by this planning package. On Linux choose temporary storage outside any Git repository for plain-folder tests. `/var/tmp` is for small fixtures, not build artifacts. On native Windows use its native temp and shell; do not paste POSIX environment syntax into PowerShell.

```bash
cargo fmt --all -- --check
cargo clippy --workspace --all-targets --all-features -- -D warnings
cargo test --locked -p zeron-proto
cargo test --locked -p zeron-sync --lib
cargo test --locked -p zeron-rpc
TMPDIR=/var/tmp cargo test --locked -p zeron-engine --lib --test local_profiles --test restart_resume --test session_publication --test device_routing --test workspace_files -- --test-threads=1
cargo test --locked -p zeron-harness --lib
cargo test --locked -p zeron-mcp
cargo build --locked -p zeron
git diff --check
```

Expected: every required command exit0, named tests actually run. Feature contracts add focused and adversarial tests, not replace this baseline. Never use `cargo fmt -- files` to limit formatting: it formatted unrelated workspace files in prior execution. For targeted formatting use `rustfmt --edition 2024 --config skip_children=true exact/file.rs`, then required whole-workspace check. Existing formatting/lint failures require the R0 repair contract before promotion.

### Affected-surface checks

- UI: `.github/workflows/ui-tests.yml` native GPUI release tests, Linux browser fixture and Mac frame/browser jobs. `cargo test --release --locked -p zeron-ui --lib -- --test-threads=1`. A screenshot is not a keyboard/accessibility test.
- macOS application/protocol: `cargo check --release --locked -p zeron` on Mac, native owner/client workflow; preserve user's app/profile, disk budget and rollback. No fabricated native success from cross-compilation alone.
- Windows shared Rust/harness/platform changes: `.github/workflows/windows.yml` including native harness isolation/quoting tests. Required unsupported environment blocks that platform gate; do not claim portable support from Linux.
- iOS DTO/routing/state changes: `.github/workflows/ui-tests.yml` iOS simulator job. Existing path filter only watches apps/ios/workflow: R0 must ensure shared contract changes trigger required compatibility jobs. Exact xcodebuild command remains the existing workflow's simulator-selected invocation, not a hardcoded unavailable device.
- Edge/transport changes: `npm ci --prefix edge`; `npm run typecheck --prefix edge`; `npm test --prefix edge`; `cargo test --locked -p zeron-preview` where preview boundary changes. Use local workerd, not production deployment.
- Harness changes: affected existing native adapter tests under crates/harness/tests plus approved real provider probes. Ignored authenticated/token-spending tests need explicit bounded authorization; do not unignore globally or label mocks real.
- Schema/migration: real SQLite old-store/reopen/rollback fault tests through production APIs, concurrent revision race, no cross-profile read, downgrade/backup behavior.
- Deployment changes: artifact identity/signature/local installed launch/private listener/reconnect/rollback checks. Full host reboot or logout requires interruption window, not inferred permission to disrupt work.

### CI implementation boundary

R0 `ci-promotion-gates` extends actual existing workflows and defines a machine-readable required gate/status contract before later code. This planning package does not install a fake workflow or claim branch protection is configured. GitHub required-check/merge protection is external repository administration: if unavailable, mark automatic enforcement blocked and retain manual no-promotion gate, never assert repository enforcement exists. Documentation-only plan validation is also CI input; it does not validate product behavior.

## Delegation protocol for low-context executors

- Read one named change's proposal/design/spec/tasks plus prerequisite interfaces and this CI section; do not absorb the entire initiative and invent a broader rewrite.
- Refresh source anchors because downstream code does not yet exist. Existing graph cards are entry points, not a license to rely on stale line numbers.
- Claim exactly bounded ownership, never stage all files or reset another agent's changes. Scoped commit after relevant verification; no pushes by default.
- If a step depends on an undefined API/type, stop implementation and return to refinement. Do not supply a plausible API from memory.
- Do not drop edge cases, shrink scope, skip real acceptance or weaken assertions to match a small context window. Split the change further, preserve dependency edges and review.
- If test shows zero selected tests, wrong temporary root, or environment failure, diagnose it before inferring product behavior. Prior watcher60/60 passes did not prove earlier flakiness impossible; keep failing evidence.
- No hidden autonomy escalation: profile/account/network/browser/parent relationship never grants action authority. Authorization is rechecked at side-effect boundaries.
- On interruption, read current tasks and git diff, verify actual service/process/state. Do not blindly replay uncertain commands. Record blocked evidence rather than asking for broad new authority.

## Unresolved decisions with explicit holding boundaries

Provider identities/APIs (SystemOne/Jev/Laya/empryo, Jcode/Herdr, ADO/Aperture) belong to named research units. Browser provider belongs to integration-browser-research. Native UI placement belongs to reviewed assignment-desktop-surface design. Briefing destination/time policy belongs to profile-briefings. Full release-candidate lifecycle beyond independent actions is excluded. Exact default budgets/performance thresholds are not approved; no invented numbers. Dependency attribution gates distribution separately. These are genuine design/research holds, not placeholders an implementer may fill arbitrarily.
