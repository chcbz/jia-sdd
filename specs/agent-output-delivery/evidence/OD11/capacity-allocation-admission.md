# Read-only deployment capacity diagnosis

The identity diagnostic at1789304438 reports only2717790208bytes free, below MinIO's2862452920byte initial gate. This probe discovers fixed CYF deployment-directory allocation before proposing any cleanup. No file is deleted or changed.

Source `tools/preflight-output-capacity.py` SHA600389ad525bd5bbdf3513b122a31b6e4146317344f82518d3a120e5834acea6. Flow `capacity-allocation-flow.yaml` SHA61924420c0877288063a40069e494345b75916d64ca94f951ebd0de23c49d64a. Controller `/tmp/od11-capacity-allocation-600389ad.cjs` SHA830c0c3ce219eec7b39e945ad53d5a2ce9c8b88bcb086f1abf9a070a51351aa5. Unique name cyf-output-capacity-20260913-600389ad.

Reuses task-owned diagnostic5264938 only with exact current name/configd38d2429, exactly successful runs1+2 and no next page. New exclusive update/start intents; new name must be absent; preserve before-config and history; full readback before run3. No create/delete. Ambiguous writes reconcile read-only.

Existing OS/memory/helper-hash/allowlisted Java jar metadata behavior retained. New fixed directory size inspection has30second global scan budget, at most80 visible top-level children per root and50000 entries per subtree, lstat and no symlink traversal or cross-device recursion. Only safe non-sensitive names, size/allocation/uid/mode/time are emitted; no file contents, configs, environment or arbitrary command lines exported. Missing/partial traversal is marked. Hardlinks may make per-child allocated totals overlap; these counts are diagnosis, not guaranteed cleanup yield. No service/resource gate closes, and concurrent deploy changes make this a timestamped snapshot only.

Any actual cleanup must be a separately concrete, reviewed operation which protects active/recovery deployments and validates fresh identity. This probe grants no cleanup scope.
