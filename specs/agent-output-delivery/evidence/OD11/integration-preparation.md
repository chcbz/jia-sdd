# OD11 integration preparation

Preparation only; OD11 is not started. Reuse the exact accepted R1 fixtures/tooling and close ../OD06/r1-release-gates.md alongside the new R2 submission/review/rework matrix. Freeze product candidates before live operation; one operator owns fixture mutations, API configuration and synthetic client processes. Do not touch the original checkout or user Agent.

Known UI seams, paths relative to the Web repository:

- `src/components/juyiting/BountyPanel.vue`: click the actual `.task-card` matching the fixture task, inspect `.bounty-modal .modal-task-info` and its shared OutputList. `detailTask` comes from local modal state; merely selecting a task elsewhere does not establish modal navigation coverage.
- `src/components/juyiting/ChatPanel.vue`: OutputList is rendered when conversationId exists. Navigate the Hall panel/history through actual controls and verify source changes. Keep `/agent/map` and `/agent/roster` distinct.
- `src/components/chat/Chat.vue`: ordinary output display requires Juyiting conversation+conversationId; an exact output resource query also opens the shared list. Existing resource-route smoke proves the latter, not historical conversation navigation.
- `src/components/world/JuyiHall.vue`: panel overlay is keyed by panelSessionGeneration. Verify closing/reopening and switching sources through pointer actions rather than assigning internal Vue state. Read docs/juyiting-runbook.md before Hall changes.
- `src/composables/useOutputs.js`: real >100-item fixture must exercise nextCursor and source/identity-bound resets; do not substitute local mock pages for end-to-end evidence.

Root browser tool `../../tools/smoke-output-browser.mjs` preserves exact `/chat` resource routes and now supports `entryMode: hall-bounty` with actual desktop map pointer navigation or mobile task controls. Live desktop r3 reached completed task3 and loaded three output cards, then failed because the nested bounty detail was clipped and could not be closed through hit testing. See `hall-bounty-navigation-r3/`; OD10 owns the layout repair before rerunning this mode. The new mode has no passing live evidence yet. Existing JWT bootstrap does not test OAuth UI; mobile viewport is not WeChat.

Known failure configuration: API `agent/jia-agent-service/src/main/java/cn/jia/agent/config/OutputDeliveryProperties.java` constructor binds `agent.output-delivery.writes-paused`; service constructors capture the value. A real pause probe needs controlled task-API configuration/restart, not editing an unrelated live bean or asserting a property file alone. Bundle this with the necessary next frozen package startup. Keep `enabled=true` when evaluating paused writes/retained reads, otherwise the scenario changes. Use prior retained TASK3 files for read/hash proof and a new disposable binding for writes; the old binding was intentionally revoked.

The isolated API package at10018 already has exact Vite15173 CORS and all25 starter resource URI patterns. Preserve them when generating the next task-only config; omitted phrase URI previously caused normal Web JWT removal/navigation. Do not copy unrelated production connections/secrets or loosen ACL. Root disk had1.3GiB free and /tmp1.5GiB at OD07 start, so retain necessary immutable packages and archive small original reports instead of repeating aggregate builds.

Keep the outage cases distinct: paused writes and unavailable scanner should not prevent previously READY objects being downloaded from healthy storage. If object storage itself is unavailable, fetching its bytes can fail explicitly/retryably; verify metadata/authorization persist and the same hash is downloadable after restoration. Do not promise bytes from an unavailable store or turn failed verification into READY to satisfy the probe.

R2 evidence must separate owner-share from formal delivery: create through authenticated entry, valid run-bound lease, freeze exact versions, atomic submit, accept/change-request, explicit new-run rework, conflicts and receipt recovery. Include funded-route negative checks without enabling deferred settlement integration. Trace actual HTTP bodies/versions to database delivery pins and ordered events; only record safe identifiers and hashes.

## Frozen OD07 runtime and release selector checkpoint (2026-09-13)

`0771f107` full starter now starts successfully on isolated port10018; real login/OAuth and all3 retained TASK3 downloads pass after Agent unbind/workspace removal. Evidence: ../OD07/full-starter-0771f107/. This development package still uses the recorded OpenCV/JAI substitutions.

The integrated API already contains `ops/ci/aliyun-flow/cold-init.gradle`, which resolves the original pinned OpenCV4.5.5 from its provenance repository and verifies size722802/SHA323d4011… before consumption. Do not replace this with the development substitution for release. The prior private artifact403 is still the last direct probe; no repeated credential probe was performed here.

`ops/orchestration/flow_remote.py` currently fixes tasks to common-core/test (SensitiveDataSanitizerTest), common-service/test (CorsConfigTest), validateLayering and starter/bootJar. It cannot currently claim the OD agent/chat/MySQL/Rabbit suite. The final CI plan must explicitly add a reviewed OD selector or attach separately attributable required verification; a successful existing ticket alone is inadequate. Preserve existing ticket hash/source/nonce and credential-isolation controls when extending it.

## Reusable real paging fixture

Conversation4 on isolatedAPI0771f107 contains120 actual published outputs from two authenticated chat dispatches (runs5b766db8e4a94bbba77b7a650241a152 and94cff4dc6fe04f19abf032e01af5dd97). Same owner login as prior TASK3; all server-created runs, no synthetic source/run database rows. Six real API pages and six boundary downloads pass; see paging-120-api-0771f107/. The new dedicated Agent is stopped, with server records and source snapshots retained. OD10/OD11 must still exercise actual browser pointer paging/source/history reset on the final UI candidate. Do not rebind the old TASK3 Agent.
