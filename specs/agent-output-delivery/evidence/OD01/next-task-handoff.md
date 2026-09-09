# OD02 launch handoff — pending OD01 acceptance

Preparation only: OD02 is not started. Start after the OD01 candidate commit, required tests and independent final review pass. Record that exact commit as the OD02 base; retain one API writer in `/home/chc/wsps/cyf-worktrees/output-api`.

## Reuse before adding infrastructure

- Canonical behavior: `../../detailed-design.md` sections 6–7, `../../openapi.yaml` upload routes, `../../schema-contract.yaml`, and `../../fixtures.json`.
- OD01 source/run/ticket authorization and strict source SPI remain the write boundary. Use `repeatable-read-review.md` for current reads, lock order and original-POST terminal receipt lookup.
- Existing local MySQL, private MinIO and ClamAV probes are documented in `../OD00/prerequisites.md`; do not reinstall or restart working services. Installer reference remains the isolated `output-client` checkout of `isp-install`.
- Repository lookup found no existing MinIO/S3 client dependency in module `build.gradle` files. API path `isp/jia-isp-service/src/main/java/cn/jia/isp/service/impl/FileServiceImpl.java` stores ISP metadata and downloads URL content into a byte array/local path; it is not the private streaming output-storage adapter. Keep new storage dependencies in the Agent implementation module and the storage interface in Agent API as designed. Dependency catalogs originate in the included `plugin` build, not a root `gradle/libs.versions.toml`.
- Production HTTP security integration and deployment-only gates are in `../OD00/downstream-gates.md`. Endpoint/controller tests alone do not prove the filter chain.
- Copy applicable canonical fixtures into API test resources with their source and digest; tests must run without an absolute root-repository dependency.

## Implementation order within the single task

1. Add the remaining OD02 schema, quota/object/upload/job/receipt DAOs and exact upload-route authentication. Reuse OD01 identity tables and opt-in migration conventions.
2. Implement the fixture upload end to end: initialize → stream immutable staging bytes → complete → durable verification → READY. Keep network/storage/scanner calls outside SQL transactions.
3. Complete the same path's negative/recovery behavior: writer epoch fencing, quota reservation/release, bounded staging cleanup, scanner outage retry and object GC. Do not replace persisted recovery with process-local queues.
4. Run targeted real-dependency and actual HTTP filter-chain verification, archive reports, commit and pause for independent review. OD03 publication/download starts only after this task passes.

## Required evidence, grouped to reduce repeated setup

| Verification group | Observable result |
| --- | --- |
| HTTP boundary and receipt | Exact method/path ticket authentication; forged or revoked scope denied; user JWT routes preserved; same POST/key/body returns original receipt; conflict rejected; terminal status-only request cannot create a receipt or mutate |
| Real bytes and scanner | Fixture size/hash matches private object; type/hash/size failures rejected; clean scan reaches READY; EICAR rejected; unavailable scanner stays VERIFYING and recovers through persisted retry |
| Real MySQL concurrency | Reservation and rollback preserve quota; old writer epoch cannot finalize; binding/run revocation during streaming denies finalization; cleanup cannot delete a pinned/referenced object |
| Recovery and bounds | Restart can resume verification/cleanup; staged object limits and upload deadlines enforced; deletion failure retains retry state and does not release quota prematurely |

Use the existing local development dependency init only with its recorded limitation; keep every Gradle command under `/tmp/cyf-gradle.lock`. Reuse passing evidence until a change or unresolved concern justifies rerunning it. This handoff adds no acceptance criteria beyond the frozen contracts.
