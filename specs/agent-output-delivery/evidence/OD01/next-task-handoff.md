# OD02 launch handoff — activated after OD01 acceptance

Activated after independent OD01 APPROVE on `c5330dd50da6c03e55edca0744485a1b95385552`; see `accepted-review-c5330dd5.md`. OD02 is in progress with that base and one API writer in `/home/chc/wsps/cyf-worktrees/output-api`; the active ownership record is `../OD02/claim.md`.

## Reuse before adding infrastructure

- Canonical behavior: `../../detailed-design.md` sections 6–7, `../../openapi.yaml` upload routes, `../../schema-contract.yaml`, and `../../fixtures.json`.
- OD01 source/run/ticket authorization and strict source SPI remain the write boundary. Use `repeatable-read-review.md` for current reads, lock order and original-POST terminal receipt lookup.
- Existing local MySQL, private MinIO and ClamAV probes are documented in `../OD00/prerequisites.md`; do not reinstall or restart working services. Installer reference remains the isolated `output-client` checkout of `isp-install`.
- Repository lookup found no existing MinIO/S3 client dependency in module `build.gradle` files. API path `isp/jia-isp-service/src/main/java/cn/jia/isp/service/impl/FileServiceImpl.java` stores ISP metadata and downloads URL content into a byte array/local path; it is not the private streaming output-storage adapter. Keep new storage dependencies in the Agent implementation module and the storage interface in Agent API as designed. Dependency catalogs originate in the included `plugin` build, not a root `gradle/libs.versions.toml`.
- Production HTTP security integration and deployment-only gates are in `../OD00/downstream-gates.md`. Endpoint/controller tests alone do not prove the filter chain.
- Existing test scaffolding: API `oauth/jia-oauth-resource/src/test/java/cn/jia/oauth/api/SessionRevocationResourceSecurityTest.java` builds an `AnnotationConfigWebApplicationContext` with production `ResourceServerConfig` and explicitly installs `FilterChainProxy` in MockMvc. Reuse that pattern for output-route verification, extending the imported chains to include the relevant session/API-key fallbacks; copying its resource-only setup does not prove the complete output route boundary.
- Existing stateless configuration example: API `chat/jia-chat-service/src/main/java/cn/jia/chat/voice/config/VoiceSecurityConfiguration.java` uses a dedicated early chain, no session security context, no request cache and JSON authentication failures. Output needs its own exact method/path matcher: upload `GET` is ticket-authenticated, while task/chat user list/download methods must retain user JWT authorization.
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

For frozen-candidate source correspondence, root can run `python3 specs/agent-output-delivery/tools/verify-test-evidence.py --repo <worktree> --candidate <commit> <observation.json> ...`. It checks archived report hashes/counters and recorded source hashes against Git objects without running Gradle or changing the worktree. A successful check proves that correspondence only; reviewers still assess coverage and recorded test/dependency limits.
