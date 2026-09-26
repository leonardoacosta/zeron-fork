---
title: Zeron fork PRD seed for planning
status: planning-input
updated: 2026-09-26
source: approved product requirements gathered 2026-09-24 to 2026-09-25
---

# Zeron fork: product requirements and planning seed

> **Purpose:** carry the approved product direction into a fresh planning session inside the Zeron repository. This is a requirements baseline, not a technical design, work breakdown, implementation authorization, or claim that these features exist.

## Direction and operating boundary

Modify/fork **Zeron itself**. Preserve its multi-device coding-agent workspace and add investigations, delegated engineering, controlled comparisons, and verified outcomes across Personal, Priceless, and Brown contexts.

- Zeron is the product and repository target. Do not use or develop Factory as the product, architecture, design system, or planning authority.
- Do not assume every Zeron subsystem must be rebuilt. Reuse or change upstream components where they satisfy the requirements; verify behavior instead of assuming it.
- Keep direct sessions. Add delegated assignments alongside them.
- This document seeds a **fresh planning session**. The next session should inspect current Zeron code and native contribution practices, map approved requirements to existing capabilities, surface decisions that genuinely remain open, and propose a bounded plan for Leo's review before implementation.
- Do not push, publish, deploy, mutate external products, provision credentials, or incur spend without separate task-specific authorization.
- Research and source inspection do not establish runtime acceptance. Distinguish static source evidence, synthetic examples, and real workflow verification.

## Product goal

Leo can work directly with coding agents or delegate bounded objectives without losing context, access limits, history, evidence, or decisions across devices and agent replacement. Work can proceed concurrently when independent. Completion claims remain distinct from verification, acceptance, delivery, and confirmed outcomes.

No numeric performance, reliability, or cost targets have been approved.

## Terms

- **Profile:** a work context such as Personal, Priceless, or Brown, including access and configuration boundaries.
- **Direct session:** a conversation where Leo works directly with an agent, without mandatory assignment administration.
- **Assignment:** a persistent delegated objective linking allowed actions, agent sessions, outputs, evidence, reviews, and unresolved questions.
- **Workflow:** a versioned process defining stages, agents, checks, approval gates, autonomy, and failure behavior.
- **Stage output:** a version-specific result, such as findings or an accepted proposal.
- **Candidate:** a revision-bound engineering result. Further changes create a new revision.
- **Verification:** evidence-based checking of a specific output.
- **Acceptance:** accepting a specific output under configured gates. It may be autonomous or require human review.
- **Delivery action:** an individually callable operation such as push, create PR, merge, release, deploy, or publish.
- **Combined outcome:** the parent objective's result across required child outputs and exact delivered versions, not a count of finished children.

The `ZF-*` labels below are stable requirement references for this document only. They are not runtime IDs, routes, API names, or task numbers.

## Approved requirements

These sections consolidate decisions Leo approved during product discovery. They are requirements, not assertions about current implementation.

### ZF-01. Zeron foundation and multi-device experience

Preserve Zeron's multi-device coding-agent workspace. Add delegated work alongside direct sessions; do not replace direct interaction with mandatory task administration. Reuse, modify, or contain existing behavior as needed. No language, service layout, storage system, or hosting topology is selected here.

### ZF-02. Profiles and access

Support extensible Personal, Priceless, and Brown profiles. Direct sessions and assignments obey profile protections. Brown support grants no Brown-system access. Connectivity, SSH, a trusted device, parent assignment, or browser authentication grants no workflow or cross-profile authority. Never silently substitute an account, profile, tool, or environment. Preserve existing external reviewer, planning, and OpenSpec authorities.

### ZF-03. Direct sessions and persistent delegation

Users may interact directly or explicitly delegate. Promoting a conversation to an assignment is an explicit act. Each assignment independently records objective, allowed actions, linked sessions, findings, evidence, reviews, and questions. Replacing an agent preserves history and does not expand permissions. Investigations may end with findings, not a code candidate.

### ZF-04. Intervention and recovery

Default intervention: **pause → confirm actual stopping → human takeover → explicit handback**. A cancellation receipt alone does not prove the work stopped. Unrelated isolated work may continue. Resume only if continuation is safe and still authorized with recorded configuration and authorization preserved. Ambiguous execution or uncertain external effects hold for Leo, never blind replay. Command deduplication is not proof of exactly-once external effects.

### ZF-05. Main workflow and customization

Offer one starting workflow: **Understand → Investigate → Propose → Implement → Verify → Deliver → Confirm outcome.** Each workflow independently customizes stages, agents, checks, failure behavior, gates, and autonomy. Investigation-only work may end early with findings. Agent-suggested changes never silently modify enabled workflows. Main-workflow improvements arrive as optional updates. Running assignments keep their selected workflow version unless explicitly changed.

### ZF-06. Workflow selection

Use repository default when configured, otherwise profile default. Allow an explicit per-assignment override without bypassing profile access. Show the selected workflow and why before launch. Automatic triggers name the workflow rather than guessing.

### ZF-07. Individually callable delivery actions

Support push, PR creation, merge, release, deploy, and publish individually, not only as steps in one rigid pipeline. Workflow/stage policy determines whether human review is required or autonomous execution is authorized. Do not require universal per-action confirmation. Candidate acceptance is not blanket delivery authority, but an enabled autonomous workflow may authorize later actions under its conditions. Full release-management scope and release-candidate lifecycle remain open beyond these approved actions.

### ZF-08. Manual launch and opt-in triggers

Support manual launch and opt-in automatic starts. Triggers may prepare work for approval or launch an authorized workflow within profile, access, and resource limits. Explain trigger provenance and deduplicate repeated events. Comparisons remain explicitly user-launched, never background-triggered.

### ZF-09. Concurrent work and conflict observer

Run concurrent workloads when they do not conflict and have no unmet dependencies. Do not globally serialize unrelated work. A System One observer checks proposals at queue admission for overlapping changes, incompatible assumptions, shared resources, and unmet dependencies. Different files can conflict. Keep dependency waiting distinct from conflict waiting. Include direct sessions without converting them into assignments. Disclose limited visibility outside Zeron. Recheck at scope changes and shared-action boundaries. Uncertain conflicts get another agent's review; unresolved uncertainty holds affected work and alerts Leo. Observer grants no authority.

### ZF-10. Prioritized backlog and urgent work

Conflicting proposals enter a prioritized backlog with blocker and reason, then are reassessed when blockers resolve. Eligible order is assigned priority, then oldest first within equal priority. Leo may override. Observer suggestions do not silently change priority. Blocked work does not block unrelated eligible work. Urgent conflicting work waits by default. Leo decides interruption; higher priority does not authorize preemption. Conflicting work starts only after actual stop confirmation. Applies to direct sessions too.

### ZF-11. Dependencies on accepted outputs

Dependencies may target specific accepted stage outputs, not only completed assignments. Downstream work binds to the exact output version that passed configured checks and gates, which may be autonomous. Upstream changes trigger downstream reassessment. Independent work may overlap when its dependencies are satisfied.

### ZF-12. Multi-repository objectives and breakdown

One parent assignment represents a multi-repository objective with linked repository-scoped children. Each child retains workflow, permissions, revision-bound candidate, evidence, and delivery status. Independent children run concurrently; dependencies connect outputs as needed. Agents may propose breakdown and dependencies under workflow gates. Review-gated workflows wait for approval; autonomous workflows may create children only within authorized scope. Leo can inspect and edit the breakdown. Children remain inside the objective, authorized repositories, and shared resource budget. Discovering broader scope/access does not grant it. Grouping grants no cross-profile access and does not require simultaneous deployment.

### ZF-13. Combined-outcome verification

The parent checks the combined outcome across required children and exact delivered versions before presenting the objective as complete. Finished children alone are insufficient. Parent workflow defines combined checks and human/autonomous acceptance gates. Partial delivery remains visible. If a child fails, unrelated children may continue while dependent work waits. Do not silently use superseded child outputs.

### ZF-14. Revision-bound candidates and evidence

Separate agent completion, verification, and acceptance. Engineering results use revision-bound candidates; new changes create new revisions without transferring previous evidence or approval. Evidence records stable identities, objective, frozen input/configuration/authorization/resource bindings, environment, revision and working tree, native sessions, observations, checks, results, limitations, redacted artifacts, and blockers. Binding identifies what evidence concerns; it does not prove correctness. **Artifact presence and binding ≠ correctness ≠ reviewer approval.** Missing, stale, or contradictory evidence blocks dependent advancement. Plane Done is not verification. Label structural, synthetic, and real-workflow evidence separately. Never describe synthetic hashes/results as live evidence.

### ZF-15. Harnesses, capabilities, resources

Jcode remains a preferred candidate for environment-local specialist swarms, with Herdr attachment. SystemOne remains distinct from engineering harnesses. These are preferences, not verified integration readiness. Provide comparable capability/preflight information, frozen configuration and resource limits, status/native IDs, confirmed cancellation, evidence, and usage. Identify unsupported capability and unknown cost; unknown is not zero. No silent tool/environment substitution or isolation downgrade. Ordinary delivery uses its configured engineer once.

### ZF-16. Explicit engineering comparisons

Comparisons are user-launched and specify task, entrants, and budget. Isolate attempts on identical frozen baselines, disclose full configurations with secrets redacted, verify correctness independently, and distinguish infrastructure failure from engineering failure. Comparisons recommend only. Leo approves routing/default changes. A winner neither replaces ordinary routing nor authorizes delivery.

### ZF-17. Browser work

Isolated browser sessions by default. Signed-in access is explicit and scoped to profile plus assignment/direct session. Authentication does not authorize external mutation; workflow gates still apply. Evidence excludes secrets and unrelated private content. Never silently switch account, tool, or environment. Provider selection remains open.

### ZF-18. Attention and briefings

Group immediate exception alerts. Routine progress goes to activity. Provide a morning briefing with profile-configurable timing and destinations. Alerts state blockers/uncertainty and do not imply acceptance or authority to resume. Provider/channel/schedule details are not selected.

### ZF-19. External systems and ownership

GitHub, Azure DevOps (ADO), MCP, and Tailscale Aperture are important integration needs; local repository storage is optional. External planning, review, and product-specification systems remain authoritative for their responsibilities. Integration availability does not authorize every action. Exact APIs, versions, capabilities, and acceptance require evidence.

## Research baseline and limitations

A static Zeron source assessment inspected commit `87ef6c8ff05629d2629133fa417e9f04c9348827`. It was not a Zeron installation, build, test run, or runtime acceptance. The detailed evidence is in Recon:

- Source: `git-github-com-zeronsh-zeron-9a8b1a114e9d`
- Record: `run-20260924T195506Z-2b0cde48199c`
- Artifact: `.mx/evidence/sources/git-github-com-zeronsh-zeron-9a8b1a114e9d/recon/run-20260924T195506Z-2b0cde48199c/artifacts/report.md` relative to configured Recon vault

Findings to verify/change in the fork: ordinary Codex paths override requested sandbox restrictions; Claude/ACP permissions auto-allow tools; stale-session recovery does not establish continuing authorization or effect safety; command dedupe is not exactly-once effect handling; trusted-device profiles do not establish cross-profile credential/repository isolation; older hosts may fall back from worktree to ordinary cwd; usage is not durably persisted in inspected contract. Root license is MIT, but selected dependencies/assets need separate review.

The recommendation in that historical report to build an independent Factory core is superseded by the approved Zeron-fork direction. Do not import its Factory milestones or architecture as requirements. A separate Jcode runtime audit (baseline `b659310328b345442226dcdc860527a7e0f2f4b7`) is prior art, not Zeron runtime acceptance. Exact SystemOne/Jev/Laya APIs, `empryo` identity/capabilities, browser-provider selection, and fuller release lifecycle remain research gaps.

## Planning handoff for the fresh session

Use this file as the product requirements baseline. Start by inspecting the current Zeron repository, its native tests/build/docs, and current branch/worktree state. Then:

1. Map each `ZF-01`…`ZF-19` to current Zeron code and tests, classifying **already supported**, **partially supported**, **missing**, or **unknown** with source evidence.
2. Identify integration and compatibility boundaries, especially workspace persistence/sync, desktop/mobile clients, harness permissions, recovery, delivery effects, and old-client behavior.
3. Propose a small, dependency-aware first slice and an overall feature plan. Keep product planning in Zeron-owned docs/issues; do not use Factory artifacts as the product plan.
4. State open user decisions separately from facts discoverable in source. Do not silently choose UI navigation or autonomy policy where this PRD leaves it open.
5. Establish tests and acceptance criteria before implementation. Label source inspection, synthetic tests, and real workflow acceptance distinctly.
6. Present the plan for Leo's review before making product-code changes. No push, external write, deployment, credential provisioning, or spending is authorized by this seed.

## Explicit unresolved decisions

- Exact APIs/capabilities for SystemOne, Jev, Laya, and the identity of `empryo`.
- Browser-provider selection/compatibility.
- Full release-management scope and release-candidate lifecycle.
- Exact integrations/versions and real-workflow readiness.
- Dependency/asset attribution for the exact upstream components selected for reuse.
- UI placement/details where not already defined by Zeron's current conventions and the approved behavior.

Do not reopen the approved product behaviors as unresolved. Plan how to satisfy them; ask Leo only for genuine new product judgments.
