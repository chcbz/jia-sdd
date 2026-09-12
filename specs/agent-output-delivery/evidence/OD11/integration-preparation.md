# OD11 integration preparation

Preparation only; OD11 is not started. Reuse the exact accepted R1 fixtures/tooling and close ../OD06/r1-release-gates.md alongside the new R2 submission/review/rework matrix. Freeze product candidates before live operation; one operator owns fixture mutations, API configuration and synthetic client processes. Do not touch the original checkout or user Agent.

Known UI seams, paths relative to the Web repository:

- `src/components/juyiting/BountyPanel.vue`: click the actual `.task-card` matching the fixture task, inspect `.bounty-modal .modal-task-info` and its shared OutputList. `detailTask` comes from local modal state; merely selecting a task elsewhere does not establish modal navigation coverage.
- `src/components/juyiting/ChatPanel.vue`: OutputList is rendered when conversationId exists. Navigate the Hall panel/history through actual controls and verify source changes. Keep `/agent/map` and `/agent/roster` distinct.
- `src/components/chat/Chat.vue`: ordinary output display requires Juyiting conversation+conversationId; an exact output resource query also opens the shared list. Existing resource-route smoke proves the latter, not historical conversation navigation.
- `src/components/world/JuyiHall.vue`: panel overlay is keyed by panelSessionGeneration. Verify closing/reopening and switching sources through pointer actions rather than assigning internal Vue state. Read docs/juyiting-runbook.md before Hall changes.
- `src/composables/useOutputs.js`: real >100-item fixture must exercise nextCursor and source/identity-bound resets; do not substitute local mock pages for end-to-end evidence.

Existing Root browser tool `../../tools/smoke-output-browser.mjs` supports only exact `/chat` resource routes. Extend with a separate bounded navigation flow if needed, preserving origin restrictions, no credential logs, actual hit-tested clicks, screenshots, content/hash assertions and tracked Chromium cleanup. Existing JWT bootstrap does not test OAuth UI; mobile viewport is not WeChat. No navigation probe has been newly run for this preparation.

Known failure configuration: API `agent/jia-agent-service/src/main/java/cn/jia/agent/config/OutputDeliveryProperties.java` constructor binds `agent.output-delivery.writes-paused`; service constructors capture the value. A real pause probe needs controlled task-API configuration/restart, not editing an unrelated live bean or asserting a property file alone. Bundle this with the necessary next frozen package startup. Keep `enabled=true` when evaluating paused writes/retained reads, otherwise the scenario changes. Use prior retained TASK3 files for read/hash proof and a new disposable binding for writes; the old binding was intentionally revoked.

The isolated API package at10018 already has exact Vite15173 CORS and all25 starter resource URI patterns. Preserve them when generating the next task-only config; omitted phrase URI previously caused normal Web JWT removal/navigation. Do not copy unrelated production connections/secrets or loosen ACL. Root disk had1.3GiB free and /tmp1.5GiB at OD07 start, so retain necessary immutable packages and archive small original reports instead of repeating aggregate builds.

Keep the outage cases distinct: paused writes and unavailable scanner should not prevent previously READY objects being downloaded from healthy storage. If object storage itself is unavailable, fetching its bytes can fail explicitly/retryably; verify metadata/authorization persist and the same hash is downloadable after restoration. Do not promise bytes from an unavailable store or turn failed verification into READY to satisfy the probe.

R2 evidence must separate owner-share from formal delivery: create through authenticated entry, valid run-bound lease, freeze exact versions, atomic submit, accept/change-request, explicit new-run rework, conflicts and receipt recovery. Include funded-route negative checks without enabling deferred settlement integration. Trace actual HTTP bodies/versions to database delivery pins and ordered events; only record safe identifiers and hashes.
