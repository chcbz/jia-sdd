# Read-only deployment capacity diagnosis

The identity diagnostic at1789304438 reports only2717790208bytes free, below MinIO's2862452920byte initial gate. This probe discovers fixed CYF deployment-directory allocation before proposing any cleanup. No file is deleted or changed.

Source `tools/preflight-output-capacity.py` SHA0fdb025677f9d3b17c2c596422f6659fa9e6f324ce5d7f262702d2abee3e6fd7. Flow `capacity-allocation-flow.yaml` SHA4e70ca8ffc9d15c5360459b573b05d7eea6dd5a31075c45d3c7091274ec77add. Controller `/tmp/od11-capacity-allocation-0fdb0256.cjs` SHA2518a283a69f9e8085543ec97b523c4257a016a0ccc1a13b2f067c908c452ca8. Unique name cyf-output-capacity-20260913-0fdb0256.

Reuses task-owned diagnostic5264938 only with exact current name/configd38d2429, exactly successful runs1+2 and no next page. New exclusive update/start intents; new name must be absent; preserve before-config and history; full readback before run3. No create/delete. Ambiguous writes reconcile read-only.

Existing OS/memory/helper-hash/allowlisted Java jar metadata behavior retained. New fixed directory size inspection has30second cooperative traversal budget checked before each root/entry/stack iteration, at most80 visible top-level children per root and50000 entries per subtree, lstat and no symlink traversal or cross-device recursion. Only safe non-sensitive names, size/allocation/uid/mode/time are emitted; no file contents, configs, environment or arbitrary command lines exported. Missing/partial traversal is marked. Hardlinks may make per-child allocated totals overlap; these counts are diagnosis, not guaranteed cleanup yield. No service/resource gate closes, and concurrent deploy changes make this a timestamped snapshot only.

Any actual cleanup must be a separately concrete, reviewed operation which protects active/recovery deployments and validates fresh identity. This probe grants no cleanup scope.

The traversal budget is not a hard real-time guarantee on an individual kernel metadata call. Flow timeout bounds the overall command. Budget exhaustion emits explicit incomplete/truncated metadata; there is no cleanup decision based on a partial sum. Old600389ad candidate was never updated/started.
