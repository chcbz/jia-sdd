# Proposed manual Flow host preflight

Preparation only. No new pipeline has been created or started. The user's instruction to continue through release covers deployment preparation; this is a bounded alternative using the existing Flow host channel, not a request for broader credentials or RAM permissions. The earlier ECS DescribeCloudAssistantStatus denial remains in effect and will not be retried. If Flow itself denies the required operation/target, stop this approach without changing permissions.

Purpose: establish existing production directories, helper identity/mode, free disk, known binary/socket paths, local port availability and narrowly identified CYF Java processes. No configuration file contents or process environments are read. Bounded command lines stay in memory except allowlisted absolute CYF jar paths. No SQL, storage write, source pull, build, service execution, install, process signal or restart is in the probe. A TCP connect proves no service identity or readiness. This does not close migration/backup/scan/storage/application release gates.

Frozen preparation:

- Probe: `../../tools/preflight-output-host.py`, SHA256 `ee64259a61c832fc33bfcf02e5fdeb47334e2a97706aec19d515fdba21164ca6`.
- Flow: `host-preflight-flow.yaml`, SHA256 `156a97d4d4f9fd7e1bf0ccdeb4a309c298fca612a3001d21c24f768cc3b1e406`.
- Organization `5fb7d76ee6f9d07f148529c7`.
- Existing Flow machine group `yjctjhskhk1ti9t4`, host group28833. Recheck it still contains only ECS `i-wz9j3ip2unzhwij0bs30` in cn-shenzhen before any start.
- One VMDeploy metadata probe job as root, matching the existing deployment channel. Artifact download is false; there are zero sources, build/deploy helper calls, source triggers and credential variables. Python executes with `-I -S` from `/usr/bin/python3`. The original API/Web/legacy pipelines are not edited or run.
- Proposed task-owned pipeline name: `cyf-output-host-preflight-20260913-ee64259a`. Creation is only a reversible Flow configuration write. Start is a separate action after reading back and verifying the exact approved script/target/no-source structure.

Local syntax and one local invocation of the probe passed on the development host: expected production paths were absent, only local10018 was open, and no CYF production-path Java process was returned. This is tool execution evidence, not production inspection. A YAML generation command initially had a local Python syntax error; the corrected generation parsed back to the exact intended one-job/no-source structure. No remote operation occurred in either case.

Execution sequence after independent read-only admission:

1. Recheck local hashes and exact host-group membership; read existing pipelines for the proposed unique name before creation. Preserve any unknown API result and stop rather than creating duplicates.
2. Create only this pipeline with the public reviewed YAML using SDK CreatePipelineRequest content/name. Record returned pipelinId and request time. Fetch it back and compare the parsed full intended configuration, exact run script and empty source set before starting.
3. List existing runs, record IDs and requestStartedAt, then request exactly one manual run with empty params. Record returned run ID; an uncertain response is resolved only through subsequent read-only queries using request time, context and actual job evidence, never a blind second start.
4. Check job/deployment order, membership/count and the bounded probe JSON. Keep configuration/hash, run/order/result and limitations as evidence. Do not interpret the VMDeploy job name or green job alone as a feature deployment or functional readiness.

This inspection uses Flow permissions already exercised for this project's deployed host. It does not install an access agent, change IAM/SSH, execute the forbidden ECS API, or create a general command execution service. Any future setup/migration action requires its own concrete reviewed script and candidate-bound release evidence within the user's existing release authorization.
