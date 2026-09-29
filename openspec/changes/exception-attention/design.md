# Exception attention: durable state before notification

Status: proposed integration contract, exact implementation tasks still required. Source fact: `crates/ui/src/notify.rs` post returns unit, disabled/unavailable delivery is a no-op, and errors are logged/swallowed. Therefore calling post cannot establish notification delivery or acknowledgment.

## Existing anchors
- `crates/ui/src/notify.rs`: best-effort native presentation only; never acceptance/stop/resume authority.
- `crates/ui/src/state.rs`: native state subscriptions and event handling. Add profile-bound exception projection here after engine persistence.
- `crates/engine/src/rpc.rs`: typed owner boundary for list/watch/acknowledge; no client-supplied profile store selector.
- `crates/sync/src/store.rs`: authoritative durable exception record/update transaction, not registry LWW replacement.

## Proposed record contract
Exception key is `(work_profile_id, affected_work_id, run_generation, exception_kind)`. A repeated observation updates the same active incident but appends observation provenance. Distinct run generation or profile cannot coalesce. `exception_kind` is a closed enum: StopUncertain, AuthorityRevoked, DependencyInvalidated, ConflictUnresolved, ExternalEffectUncertain, RequiredCheckFailed. Routine progress is not an exception kind.

Record includes stable incident ID, first/last observation sequence, current blocker evidence references, redacted summary, affected exact binding, resolution state and acknowledgment state. `Acknowledged` means user saw/dismissed it, never resolved. Resolution requires owner-observed corrected condition with evidence; UI click cannot set it. Action labels are explicit safe navigation/review actions, not generic resume buttons.

Deliver notification only after record commits. Notifications are advisory projection; failures leave incident active and visible in in-product activity. Restart lists active incidents before attempting delivery. If runtime cannot determine delivered status, store attempted/unknown, not delivered. Do not retrofit fake receipts onto current notify::post. Windows no-op remains explicit unsupported native delivery, with in-product exception visibility required.

## Exact acceptance boundaries
1. Repeated same-key stop uncertainty creates one active incident and multiple retained observations. Different profile/run generation creates separate incident.
2. Inject SQLite write failure: no notification attempted before durable record; caller retains stop hold and reports record persistence failure safely.
3. Disable native notifications via existing environment flag: incident remains retrievable after owner restart; no assertion of native delivery.
4. Acknowledge/dismiss through owner RPC: acknowledgment recorded, unresolved blocker remains, no Harness::run or handback event.
5. Resolve stale generation: reject, current incident unaffected. Redacted summary cannot contain provider tokens or unrelated private content.
6. Native Mac/Linux delivery test observes actual banner/activity when available; receipt absence is unknown. Do not call screenshot evidence proof of human acknowledgment.

7. C04 isolation: create an active redacted incident under profile A with a destination bound to profile A; attempt list/watch/ack via profile B's owner context and deliver/project the event through profile B's native notifier and in-product activity feed. Assert profile B receives no incident ID, summary, source, destination, notification, activity row or acknowledgment side effect; profile A can still retrieve its record. Include identical affected-work/run IDs in both profiles to prove profile binding, not key coincidence, enforces isolation.

## Canonical scenarios
- C01: Repeated same stop uncertainty creates one grouped alert with updated observations, not an alert storm.
- C02: Notification delivery fails: blocked state remains durable and visible after restart.
- C03: User dismisses alert: execution remains held.
- C04: Profile-private alert must not leak into another profile destination.

## Rollback
Keep durable incident history and blocked owner state. Disable presentation safely without discarding exceptions. No rollback automatically resumes work. Provider/channel settings remain the later briefing unit's responsibility; this unit needs only existing in-product activity and native best-effort notification adapter.
