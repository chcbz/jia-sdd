# Candidate 683e8007 verification

API candidate: `683e8007dbbde98895d82a391fc7d2a4228f46fa`; worktree `/home/chc/wsps/cyf-worktrees/output-api` clean at handoff. Development dependency overrides remain those recorded in OD00; no deployment or production migration.

## Retained final reports

- Real-dependency MockMvc: recorded command in `command.txt`, exit 0, one test with task and conversation round trips. Root inspected XML and compared the test and OAuth production source blobs to the candidate. See `observation.json`. No live TCP or actual Agent shutdown was exercised.
- OAuth regression: writer executed `python3 /tmp/cyf-od02-evidence/run-gradle-with-od-env.py :oauth:jia-oauth-resource:test --tests 'cn.jia.oauth.api.AuthenticationResourceSecurityTest' --tests 'cn.jia.oauth.config.ResourceServerConfigTest'`, reporting exit 0. Root inspected both surviving XML files: 6 + 1 tests, no failures/errors/skips. See `oauth-observation.json`. No standalone command/exit log was retained. Source association is a post-run comparison; no full pre-run manifest exists.

Archived XML excludes captured logs/properties to avoid copying environment data; original report hashes are preserved. These are existing executions, not reruns by root.

## Writer execution transcript only

- `python3 /tmp/cyf-od02-evidence/run-gradle-with-od-env.py :chat:jia-chat-service:test --tests 'cn.jia.chat.output.OutputDeliveryMySqlIntegrationTest'`: reported exit 0, five MySQL service cases; final HTTP invocation overwrote the XML and no standalone log survives. Authorization/storage are mocked/in-memory in this suite.
- `python3 /tmp/cyf-od02-evidence/run-gradle-with-od-env.py validateLayering`: reported exit 0; no XML or saved log.
- `git diff --check`: reported exit 0.

Historical repaired H2 reports remain separate and are not relabeled as final-candidate runs. Independent review is pending.
