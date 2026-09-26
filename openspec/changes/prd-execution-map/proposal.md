# PRD execution map

Status: proposed planning package, authored at user request on 2026-09-26. Approval to author this package is not approval to implement every child change. Local deployment authorization from the preceding session remains scoped to that deployment.

## Goal
Turn every clause of `docs/fork-prd.md` ZF-01 through ZF-19 into a named, bounded change with dependencies, observable acceptance, explicit non-goals and mandatory CI before promotion. Make delegation safe for an executor with no conversation history.

## Authority
The PRD defines product behavior. Each child proposal/spec defines its bounded behavior. Its `tasks.md` is the only executable checklist. This change's `design.md` is the coverage/dependency index, not a second completion ledger. Existing `assignment-record` remains authoritative for its implemented slice. Do not overwrite its history or count deployment as a workflow executor.

## Deliverables
- Separate child changes for independently testable safety, orchestration, delivery, integration and presentation boundaries.
- Explicit rounds with a CI barrier after every iteration and after integrating each round.
- Adversarial scenarios and prohibited interpretations in every child contract.
- A readiness distinction: discovery/refinement can proceed on a named authorized change; implementation cannot proceed until that change has exact approved interfaces, runnable failing tests and code-level tasks.

## Non-goals
No product code, external integration, CI workflow implementation, dependency installation, deployment, push, schema migration or agent launch is authorized by this planning package. No guessed SDKs or undocumented provider methods. No universal confirmation policy that contradicts workflow-configured autonomy.

## Why contracts are staged
The PRD approves behavior but leaves provider selection and several API contracts unresolved. Writing invented Rust APIs or full implementation snippets for those decisions would mislead the very executors this package protects. Every child therefore has a concrete executable discovery/refinement contract, a complete bounded behavior/acceptance specification, and an explicit implementation gate. The gate requires replacing refinement-only instructions with code-complete tasks before `apply` can implement. These are not claims that all future code is already designed.

## Acceptance of this planning change
Every ZF requirement maps to one or more changes; dependency graph is acyclic; each change has proposal/design/spec/tasks; existing source anchors resolve; each round ends in CI on its integrated commit; blocked external evidence never becomes a pass; an independent review challenges clause coverage and weaker-agent misinterpretations. Planning checks are not product acceptance.
