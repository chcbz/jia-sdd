# Output verification tools

These tools are development verification helpers, not implementation or release evidence by themselves. Python requires `PyYAML` and `jsonschema >= 4`. Run from the root repository.

- `verify-test-evidence.py` verifies archived JUnit report bytes and recorded source hashes against a named Git candidate. Passing establishes correspondence, not coverage; failed/skipped batches remain separate evidence.
- `verify-http-contract.py observations.json` checks a nonempty array of `{operationId,status,body}` against the frozen OpenAPI JSON response schema. It reports only hashes and validation keywords. `valid:true` covers only the supplied observations; it proves no route/status completeness, live HTTP execution, headers or ACL.
- `smoke-output-http.py` uploads the frozen 13-byte fixture, checks create/complete/publication receipt replay, publishes an explicit task owner share or conversation output, and reads/downloads version 1 as the user. It checks method/path against OpenAPI, JSON envelopes/cache policy, file metadata, binary headers and exact bytes. Only a numeric loopback origin without a path prefix is supported; redirects and proxies are disabled.

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

Use `CONVERSATION` for the chat endpoint. The read-only mode issues no mutations; a passing report cannot itself prove the Agent was stopped. Record that lifecycle observation separately. Wrong-user/role/scope, changed-body/cross-route idempotency conflicts, list/pagination/expiry, UI and deployment acceptance require their own evidence. An interrupted publish run is not resumable by this smoke helper; durable recovery belongs to the OD04 client.

`python3 specs/agent-output-delivery/tools/test-http-probe-controls.py` tests the helper with a synthetic transport, never the CYF API. Its three test methods cover task/chat publication, read-only GET behavior, status/bytes/metadata/cache faults and invalid origins. Real local synthetic HTTP controls also observed redirect rejection with zero requests at the redirect target; these are tool checks, not product acceptance.
