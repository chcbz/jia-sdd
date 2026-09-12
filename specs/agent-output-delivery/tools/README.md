# Output verification tools

These tools are development verification helpers, not implementation or release evidence by themselves. Python requires `PyYAML` and `jsonschema >= 4`. Run from the root repository.

- `smoke-output-lease.py` is the OD07 lease probe, prepared but not yet live-validated or independently reviewed. It requires an already trusted READY policy1 work item and `OUTPUT_SMOKE_RUN_TICKET`. Only numeric loopback HTTP10018 is accepted. GET → claim/start/heartbeat/release uses returned string versions and exact receipt replays, with bounded/schema-checked responses and hash-only sensitive response evidence. Success releases the lease; a failure stops immediately and may leave an active lease for the operator to inspect/expire, without guessing new versions or automatically retrying another operation. It never creates tasks/runs, executes a model, submits a delivery or provides concurrency proof. `python3 specs/agent-output-delivery/tools/test-lease-probe-controls.py` passed six synthetic helper-control tests; these do not contact CYF and are not OD07 product test evidence.

- `verify-test-evidence.py` verifies archived JUnit report bytes and recorded source hashes against a named Git candidate. Passing establishes correspondence, not coverage; failed/skipped batches remain separate evidence.
- `verify-http-contract.py observations.json` checks a nonempty array of `{operationId,status,body}` against the frozen OpenAPI JSON response schema. It reports only hashes and validation keywords. `valid:true` covers only the supplied observations; it proves no route/status completeness, live HTTP execution, headers or ACL.
- `smoke-output-http.py` uploads the frozen 13-byte fixture, checks create/complete/publication receipt replay, publishes an explicit task owner share or conversation output, and lists/reads/downloads version 1 as the user. It checks method/path against OpenAPI, JSON envelopes/cache policy, source/version list boundaries, file metadata, binary headers and exact bytes. Only a numeric loopback origin without a path prefix is supported; redirects and proxies are disabled.

For the live probe, the execution harness supplies `OUTPUT_SMOKE_RUN_TICKET` and `OUTPUT_SMOKE_USER_TOKEN` through the process environment. Do not paste either into command arguments or evidence. The server-created source/run must already exist and be authorized; the tool does not fabricate a trusted run or mint credentials. Publication creates synthetic development records; the tool does not delete them.

Command templates only; no business endpoint has been exercised by preparing these tools:

```bash
python3 specs/agent-output-delivery/tools/smoke-output-http.py \
  --base-url http://127.0.0.1:18080 --source-type TASK \
  --source-id TASK_ID --run-id TRUSTED_RUN_ID --output-id UNIQUE_PROBE_OUTPUT_ID

# After independently stopping the Agent, use only the user token and prior ID.
python3 specs/agent-output-delivery/tools/smoke-output-http.py \
  --base-url http://127.0.0.1:18080 --source-type TASK \
  --source-id TASK_ID --output-id UNIQUE_PROBE_OUTPUT_ID --read-only
```

Use `CONVERSATION` for the chat endpoint. The read-only mode issues no mutations; a passing report cannot itself prove the Agent was stopped. Record that lifecycle observation separately. With `--check-other-user`, supply an authenticated unrelated user's `OUTPUT_SMOKE_OTHER_USER_TOKEN` through the environment. The helper requires its authenticated capabilities request to succeed, then requires all four list/version/detail/download read routes to return nonretryable 404 without resource details. It withholds credential and response-body values from evidence. New publication mode requires the synthetic version in both first-page lists; use an isolated synthetic source for deterministic ordering. Read-only mode validates list schemas and boundaries without claiming the older version is on the first page.

Private-role/scope, changed-body/cross-route idempotency conflicts, pagination beyond the first page, expiry, UI and deployment acceptance require their own evidence. An interrupted publish run is not resumable by this smoke helper; durable recovery belongs to the OD04 client.

`python3 specs/agent-output-delivery/tools/test-http-probe-controls.py` tests the helper with a synthetic transport, never the CYF API. Its four test methods (16 subcases) passed after the OD03 list/negative-read extension, covering task/chat publication, read-only GET behavior, status/bytes/metadata/cache/list faults, unauthorized/leaking cross-user responses and invalid origins. Earlier real local synthetic HTTP controls also observed redirect rejection with zero requests at the redirect target; these are tool checks, not product acceptance.
