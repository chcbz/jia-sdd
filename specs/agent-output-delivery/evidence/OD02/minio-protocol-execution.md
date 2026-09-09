# Real MinIO single-PUT fence probe

Executed successfully on 2026-09-09 at 21:32 UTC, exit 0. This root-operated protocol probe used a dedicated new local bucket and did not run Gradle, mutate the API worktree or touch application objects.

```bash
PYTHONPATH=/home/chc/.local/share/cyf-output-tools/python \
python3 specs/agent-output-delivery/tools/probe-minio-storage-fence.py \
  --credentials /home/chc/.local/share/cyf-output-tools/services/minio-state/credentials.json \
  --output specs/agent-output-delivery/evidence/OD02/minio-protocol-probe.json
```

The credential file was read only in-process; no values or signed URLs were recorded. Python MinIO client version: 7.2.20. The observed MinIO process PID 44100 uses `/home/chc/.local/share/cyf-output-tools/services/minio`; that binary reports `RELEASE.2025-09-07T16-13-09Z`, commit `07c3a429bfed433e49018cb0f78a52145d4bedeb`, Go 1.24.6 linux/arm64.

| Executed artifact | SHA-256 |
| --- | --- |
| `../../tools/probe-minio-storage-fence.py` | `cbbff54ee87627ba3eeaa58d5d1d37989f45f12bb8412826db1fca07008e087b` |
| `minio-protocol-probe.json` | `1debd5c87110a25e59fd8b2f5a6697ef75e2e3cb4a855d6134c1cbc7c4033fa1` |

Observed behavior:

- The probe received HTTP 100 Continue from the actual MinIO server, sent 64 KiB of the old PUT body, then attempted the same-key tombstone on another connection. The tombstone did not finish within the two-second paused-body interval. After the probe sent the remaining body, the old PUT returned 200 and the tombstone completed; HEAD showed zero length and the exact cleanup token. This observed ordering is old PUT then tombstone, not a claim that the tombstone committed before the old body resumed.
- Replaying the same still-valid signed conditional PUT after the fence returned 412.
- A separately completed data PUT followed by repeated tombstone installation remained zero length; later conditional data PUT was rejected.

The isolated bucket was newly created without versioning. Its zero-byte test tombstones were retained. The two-second observation interval only classifies the observed ordering; it is not a production cleanup timeout or safety assumption.

Limits: this probes the storage protocol, not `S3OutputObjectStorage`, application HTTP authentication, quota transactions, retry scheduling, antivirus or READY. It does not inject an actually lost tombstone response, prove all scheduling interleavings or validate enabled/Suspended bucket rejection in the application. Those application checks remain OD02 work. No OD01 JUnit counts are changed by these three protocol scenarios.

Independent read-only architect review found this sufficient to resolve the design uncertainty about single-PUT feasibility on the tested MinIO. Marker concurrency is inferred from the future timeout and observed ordering rather than a server trace, so this is not an exhaustive concurrency proof. The probe's presigned URL does not demonstrate that `If-None-Match` is a signed header: the URL remains internal and the trusted probe always sets it. A production presigned URL exposed outside the process would have to bind that condition in SignedHeaders; the current Java implementation instead uses a direct, service-controlled signed PutObject request. No secret or signed URL serialization was found in the probe. Production adapter/versioning checks and SQL quota evidence remain required.
