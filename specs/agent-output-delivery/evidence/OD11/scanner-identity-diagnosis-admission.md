# Scanner bootstrap diagnosis admission

Unique immutable Flow identity: `cyf-output-scanner-identity-diagnosis-20260913-078f2bba`.

- Source: tools/diagnose-output-scanner-bootstrap.py; SHA-256 `078f2bba13f084874c6e45d6f7e9eb2578d0809cb9b4adfc7d222c2662faebf4`.
- Flow: scanner-identity-diagnosis-flow.yaml; SHA-256 `7145d00a3c2183a432cb1b4a74e2e0ef84076b52a7cc324a961d5d2131e47b84`.
- Organization `5fb7d76ee6f9d07f148529c7`, group `28833`, machine group `yjctjhskhk1ti9t4`; exactly one ECS `i-wz9j3ip2unzhwij0bs30`, `cn-shenzhen`.
- Controller `/tmp/od11-scanner-identity-diagnosis-078f2bba.cjs`; exclusive state directory `/tmp/od11-scanner-identity-diagnosis-078f2bba`.

Create only after paginated exact-name reconciliation finds zero matching pipelines and singleton-host verification succeeds. Persist exclusive create intent before calling the API. Read back all config keys (flow/settings/sources), require zero sources, structural equality to frozen YAML and settings equality to the accepted controller baseline. Bind compact JSON SHA before start. Require zero historical runs and no next page, unchanged name/config and singleton host again. Persist exclusive start intent, then request exactly one run with empty parameters `{}`. Unknown creation/start results permit read-only reconciliation, never blind repeat.

Read-only scope: fixed scanner unit state/journals, at most100 journal entries per unit (256KiB captured-output cap), at most32 database directory metadata entries, free disk and memory. No restart, stop, enable, install, file write, database contents, API configuration, or process environment access on the host. The scanner activation5264852/run1 is terminal FAIL with verified stop/disable compensation. This is a new read-only observation after a different failure phase; reuse the unchanged, independently reviewed diagnostic source and YAML to inspect actual scanner journal messages. This diagnostic approval does not permit reinstall or storage activation.

Purpose: diagnose scanner5264943 progress_process_identity after verified stop/disable compensation. Preserve original bounded read-only scope; add effective systemd User/Group/NRestarts, numeric journal _UID/_GID/_PID fields only, and dedicated cyf-output-scan pwd/grp numeric IDs. No command line, environment, file contents, account password fields or member lists exported. No restart/config mutation. Actual offending UID was not recorded by activation, so do not claim its cause is known. Resource numbers are refreshed incidentally; a passing read-only diagnostic is not permission to activate or install storage.
