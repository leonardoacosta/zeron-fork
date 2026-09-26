# PRD decomposition execution contract

**Goal:** canonical coverage and reviewable change units for all19 requirements, not implementation of them.
**Architecture:** OpenSpec proposals/specs/design and per-change tasks; one index, no duplicate lifecycle.
**Tech stack:** Markdown/JSON with a Python stdlib validator.

- [x] Read PRD, current code graph, assignment implementation and actual CI definitions.
- [x] Author bounded child proposal/design/spec/tasks and round dependency map.
- [x] Define mandatory iteration and integrated-round CI promotion contract.
- [x] Run complete self-review for clause coverage, no guessed interfaces, explicit blockers, rollback and consistent dependency metadata.
- [x] Obtain independent review, repair concrete omissions and contradictory authority/CI claims.
- [x] Run `python3 openspec/changes/prd-execution-map/validate.py` and `git diff --check`; expected exit0 with all19 mapped, all child artifacts present and acyclic dependencies.
- [x] Commit only requested planning artifacts and unchanged PRD baseline; report discovery-ready versus implementation-blocked status accurately. Initial package committed as `c3a04c0`; no product implementation or push.

## Handoff
First named refinement: `ci-promotion-gates`. R0 blocks later implementation promotion until clean enforceable CI baseline exists. Then follow design.md dependency rounds; no blanket `apply:all` authorization supplied by plan authoring.

## Overnight execution-readiness refinement (current, not completed decomposition counts)
- [x] Re-audit actual tasks:27 of original33 units still generic; do not count structural validation as readiness.
- [x] Cold-extract CI/catalog/pure-core proposals, execute actual commands, repair iOS skip-test and lint failures.
- [x] Split hidden profile runtime/access cycles into catalog, policy-core, runtime enforcement, runtime activation and migration responsibilities. Current inventory36 units; earlier33-unit review is historical only.
- [ ] Complete durable policy and exact engine binding/dispatch integration code and tests, not just pure evaluator source.
- [ ] Complete all remaining schema/RPC/native/provider/UI task contracts with exact code or bounded research outcomes; no undefined future APIs.
- [ ] Run cross-unit contract agreement and new cold executor trials on the final inventory, including CI after each refinement round.
- [ ] Record per-unit readiness and genuine external decision/access gates, obtain final review, and commit tested final handoff.

## Review evidence
Self-review found missing explicit engineering execution beyond investigation; added engineering-stage-runner before final validation. Independent reviewer butterfly returned Approved after reviewing all33 units against PRD and dependency/readiness/CI boundaries. Validator passed33 units, all19 requirements,10 round barriers,130 explicit cases. This is a reviewed decomposition/refinement handoff, not code-complete implementation approval.

## Delegation trial
On 2026-09-26 19:08 UTC the coordinator extracted and executed the exact first D1 shell block from all33 committed child tasks. All33 exited0 and resolved their existing source anchors. Cold low-context executor badger independently executed the first CI change's D1 command and validator, both exit0, inspected actual CI files, and correctly selected R0 refinement rather than implementation. Its verdict: useful decomposition, NOT implementation-ready; D2 refinement and written review/approval required. This establishes usable discovery entry points and understandable stop rules, not implementation sufficiency. Remaining interface/code-task refinement is real work, not a CI pass or approved product implementation. The writing-plans code-complete handoff criterion is not yet met for child implementation.

## Refinement iteration19:21 UTC
CI contract now includes exact native needs-summary YAML and proposed test source; predicate controls15/15 and synthetic structural red/green8 tests passed. Foundation handoff exact commands selected and passed5 tests. Research checker6 self-tests and attribution inventory1295 rows with missing-notice negative control passed. Corrected discovered weak-agent errors: corrupted shell quoting, short --exact filters/argument arity, missing YAML colons, inherited Windows shell, path-filtered aggregator deadlock and empty evidence acceptance. Provider/API and later product-unit design remains blocked for exact refinement. No claim that33 child implementations are code-complete.
