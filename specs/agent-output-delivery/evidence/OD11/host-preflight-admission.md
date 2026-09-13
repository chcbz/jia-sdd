# Proposed manual Flow host preflight

Preparation only. No new pipeline has been created or started. The user's instruction to continue through release covers deployment preparation; this is a bounded alternative using the existing Flow host channel, not a request for broader credentials or RAM permissions. The earlier ECS DescribeCloudAssistantStatus denial remains in effect and will not be retried. If Flow itself denies the required operation/target, stop this approach without changing permissions.

Purpose: establish existing production directories, helper identity/mode, free disk, known binary/socket paths, local port availability and narrowly identified CYF Java processes. No configuration file contents or process environments are read. The probe reads each numeric PID comm (at most 17 bytes), then inspects bounded cmdline only for processes named java; unrelated Java command lines may be encountered in memory. Only canonical absolute CYF jar paths without dot segments are exported. This limited in-memory inspection is part of the approved scope; no raw command lines are logged. Helper hashing reads at most 1 MiB plus one overflow byte and exports only the digest. Six loopback TCP connections may increment service counters or logs; no application payload is sent. No SQL, storage write, source pull, build, service execution, install, process signal or restart is in the probe. A TCP connect proves no service identity or readiness. This does not close migration/backup/scan/storage/application release gates.

Frozen preparation:

- Probe: `../../tools/preflight-output-host.py`, SHA256 `648f412bfca4a56bb9e14eecb9307740873c23756503d4ada5cd043d8f2658b0`.
- Flow: `host-preflight-flow.yaml`, SHA256 `de186306c542fe1a16468e9ae7055d501d8f7e67a081fb0e4c281abacbb5bbe2`.
- Organization `5fb7d76ee6f9d07f148529c7`.
- Existing Flow machine group `yjctjhskhk1ti9t4`, host group28833. Recheck it still contains only ECS `i-wz9j3ip2unzhwij0bs30` in cn-shenzhen both immediately before creation and immediately before start. Require exactly that one ECS ID, region cn-shenzhen, and no other member; stop on drift. Bind observed output to the deployment-order target metadata, not to a self-reported hostname.
- One VMDeploy metadata probe job as root, matching the existing deployment channel. Artifact download is false; there are zero sources, build/deploy helper calls, source triggers and credential variables. Python executes with `-I -S` from `/usr/bin/python3`. The original API/Web/legacy pipelines are not edited or run.
- Proposed task-owned pipeline name: `cyf-output-host-preflight-20260913-648f412b`. Creation is only a reversible Flow configuration write. Start is a separate action after reading back and verifying the exact approved script/target/no-source structure.

Local syntax and one local invocation of the probe passed on the development host: expected production paths were absent, only local10018 was open, and no CYF production-path Java process was returned. This is tool execution evidence, not production inspection. A YAML generation command initially had a local Python syntax error; the corrected generation parsed back to the exact intended one-job/no-source structure. No remote operation occurred in either case.

Execution sequence after independent read-only admission:

1. Recheck local hashes and exact host-group membership; read existing pipelines for the proposed unique name before creation. Preserve any unknown API result and stop rather than creating duplicates.
2. Create only this pipeline with the public reviewed YAML using SDK CreatePipelineRequest content/name. Record returned pipelinId and request time. Fetch it back and compare the parsed full intended configuration, exact run script and empty source set before starting.
3. List existing runs, record IDs and requestStartedAt, then request exactly one manual run with empty params. Record returned run ID; an uncertain response is resolved only through subsequent read-only queries using request time, context and actual job evidence, never a blind second start.
4. Check job/deployment order, membership/count and the bounded probe JSON. Keep configuration/hash, run/order/result and limitations as evidence. Do not interpret the VMDeploy job name or green job alone as a feature deployment or functional readiness.

This inspection uses Flow permissions already exercised for this project's deployed host. It does not install an access agent, change IAM/SSH, execute the forbidden ECS API, or create a general command execution service. Any future setup/migration action requires its own concrete reviewed script and candidate-bound release evidence within the user's existing release authorization.

Revision verification: Python syntax and six canonical-path acceptance/rejection cases passed locally; YAML was regenerated from and parsed back to the exact probe source. This only admits bounded metadata collection. Disk thresholds, memory capacity, backup and all functional release checks remain separate outstanding gates.
