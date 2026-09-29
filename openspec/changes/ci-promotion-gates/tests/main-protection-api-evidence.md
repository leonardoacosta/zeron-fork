# `zeronsh/zeron` main protection API evidence

Captured 2026-09-29 20:43 UTC with authenticated `gh` as `leonardoacosta` (`gh auth status`; token scopes included `repo`). No token value recorded.

Independently re-confirmed 2026-09-29 21:09 UTC: `repos/zeronsh/zeron/branches/main` returns `protected: true`; ruleset `20150191` is `active`; its rule types are exactly `["deletion","non_fast_forward","pull_request"]`; repository permissions for this account are `{"admin": false, "maintain": false, "push": false, "pull": true}`.

## Branch

`gh api repos/zeronsh/zeron/branches/main --jq '{name, protected, protection_url}'`

```json
{"name":"main","protected":true,"protection_url":"https://api.github.com/repos/zeronsh/zeron/branches/main/protection"}
```

## Legacy branch-protection endpoint

`gh api repos/zeronsh/zeron/branches/main/protection`

```json
{"message":"Not Found","documentation_url":"https://docs.github.com/rest/branches/branch-protection#get-branch-protection","status":"404"}
```

Direct `.../protection/required_status_checks` also returned 404. The branch endpoint marks `main` protected, so the legacy endpoint does not disclose required checks here. Do not infer that main is unprotected from this 404.

## Active ruleset

`gh api repos/zeronsh/zeron/rulesets?includes_parents=true` listed ruleset `20150191`, `Protect main`, target `branch`, source type `Repository`, source `zeronsh/zeron`, enforcement `active`.

`gh api repos/zeronsh/zeron/rulesets/20150191` returned:

```json
{"id":20150191,"name":"Protect main","target":"branch","source_type":"Repository","source":"zeronsh/zeron","enforcement":"active","conditions":{"ref_name":{"exclude":[],"include":["~DEFAULT_BRANCH"]}},"rules":[{"type":"deletion"},{"type":"non_fast_forward"},{"type":"pull_request","parameters":{"required_approving_review_count":1,"dismiss_stale_reviews_on_push":false,"required_reviewers":[],"require_code_owner_review":false,"dismissal_restriction":{"enabled":false,"allowed_actors":[]},"require_last_push_approval":false,"required_review_thread_resolution":false,"require_extra_approval_for_unattributed_changes":true,"allowed_merge_methods":["merge","squash","rebase"]}}],"node_id":"RRS_lACqUmVwb3NpdG9yec5N4xT2zgEzd68","created_at":"2026-07-31T15:31:48.652-05:00","updated_at":"2026-07-31T15:31:48.690-05:00","current_user_can_bypass":"never"}
```

Ruleset has no `required_status_checks` rule. Its configured protections are deletion prevention, non-fast-forward prevention, and PR review requirements. Thus API evidence found **no required status-check contexts and no app/source associations** in the active main ruleset. This is not evidence about checks configured by any separate mechanism outside these returned endpoints.

## GraphQL cross-check

Authenticated GraphQL query for repository `branchProtectionRules(first:100)` returned:

```json
{"data":{"repository":{"branchProtectionRules":{"nodes":[]}}}}
```

No classic GraphQL branch-protection rules were returned. Combined with REST ruleset evidence, the checked APIs expose no required checks/apps for main; REST legacy protection details remained unavailable (404).
