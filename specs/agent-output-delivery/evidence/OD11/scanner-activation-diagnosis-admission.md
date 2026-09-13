# Scanner bootstrap diagnosis admission

Unique immutable Flow identity: `cyf-output-scanner-activation-diagnosis-20260913-c5d63cf4`.

- Source: tools/diagnose-output-scanner-bootstrap.py; SHA-256 `c5d63cf4ceb60a97a0b80e78aacf74146064190ea67140fd3bb31a81cfe5a5e3`.
- Flow: scanner-bootstrap-diagnosis-flow.yaml; SHA-256 `021430e024e5b310aceb790ce8d1b7c250a6f85d82b7362e9da385e911067afa`.
- Organization `5fb7d76ee6f9d07f148529c7`, group `28833`, machine group `yjctjhskhk1ti9t4`; exactly one ECS `i-wz9j3ip2unzhwij0bs30`, `cn-shenzhen`.
- Controller `/tmp/od11-scanner-activation-diagnosis-c5d63cf4.cjs`; exclusive state directory `/tmp/od11-scanner-activation-diagnosis-c5d63cf4`.

Create only after paginated exact-name reconciliation finds zero matching pipelines and singleton-host verification succeeds. Persist exclusive create intent before calling the API. Read back all config keys (flow/settings/sources), require zero sources, structural equality to frozen YAML and settings equality to the accepted controller baseline. Bind compact JSON SHA before start. Require zero historical runs and no next page, unchanged name/config and singleton host again. Persist exclusive start intent, then request exactly one run with empty parameters `{}`. Unknown creation/start results permit read-only reconciliation, never blind repeat.

Read-only scope: fixed scanner unit state/journals, at most100 journal entries per unit (256KiB captured-output cap), at most32 database directory metadata entries, free disk and memory. No restart, stop, enable, install, file write, database contents, API configuration, or process environment access on the host. The scanner activation5264852/run1 is terminal FAIL with verified stop/disable compensation. This is a new read-only observation after a different failure phase; reuse the unchanged, independently reviewed diagnostic source and YAML to inspect actual scanner journal messages. This diagnostic approval does not permit reinstall or storage activation.
