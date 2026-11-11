# UR05 published snapshot verifier slice — 2026-10-08 23:56 +08

Owner: Knuth / 01a1195e-e058-7ea2-bfc2-1a0e4736cdd4. Real ledger task UR-05-20261008, writer implementing; no Reviewer.

Read current /home/isp/wsps/cyf/AGENTS.md and /home/isp/wsps/cyf/ops/orchestration/README.md, and confirm read in handoff. Rules applied at this natural continuation, no production authorization expansion.

Repo/worktree: /home/isp/wsps/worktrees/ur05-local-backend-package-20261008. Base b2ac616353dba632e5c42ed4c189c0155d1b9a69 / tree 924a44f5d3331bbc77a77cee496fb8e7fcb5fa09, initially clean. Readonly report /var/tmp/ur05-helper-contract-diagnosis-20261008/report.json accepted after independent report artifact SHA and 15-file SHA/mode/ownership readback.

## Exactly two allowed source paths
- /home/isp/wsps/worktrees/ur05-local-backend-package-20261008/ops/ci/aliyun-flow/auto/admit-api-local.py
- /home/isp/wsps/worktrees/ur05-local-backend-package-20261008/ops/ci/aliyun-flow/tests/test_api_local_admission.py

## Goal/non-goals
Add the proposed read-only verifier to the existing helper so the future UNIQUE installer can validate already published copied snapshots without reopening any original builder/controller paths. No installer integration, new installation approval or schema authority in this slice. Do not edit five helpers, kit/wrappers, producer, installed files, root dirty source, ledger/docs, credentials, live92814 or its processes/targets; no Gradle/MySQL/pip/install/deploy.

## Frozen CLI/semantics
Additional explicit mode: --verify-published --trusted-root ABS --admission ABS --admission-sha256 HEX64. Strict exact flags; no automatic mode fallback or fabricated Flow Run. Existing admit and --describe semantics preserved; describe may add explicit verifier interface metadata without changing any old fields.

Root-required, stdlib-only read-only. Admission lives under the original protected trusted-root/admitted output tree; externally pinned admission file SHA is required. Reuse protected ancestry, regular-file/no-link/ownership/permissions, stable-read/recheck and safe-error protections. Verify strict published admitted schema, kind=local-build-v1, exact identity, scope=artifact-admission-only and productionAuthorized=false. Recheck every referenced copied authority/payload/package/evidence byte and complete independent batch authority/controller/trusted-record proof closure, as original admission does. Old originalPath values are labels only: bijectively map original trusted record/reference identities to protected copied snapshot bytes; never read original external paths. Exact five package members unchanged, actual package/payload/evidence consistency and raw-authority projection must all match; don't trust self-asserted admitted status.

Success emits canonical JSON format cyf-api-local-published-verification-v1, status=verified, scope=artifact-admission-only, productionAuthorized=false, admission={path,sha256,size}, source={kind,identity}. No installAllowed or production flag elevation. Failure same result format, status=rejected, existing safe code, exit1; no raw secret/path exceptions. No file publication, state mutation, consumption, auth issuance or service operation. Execution under future protected isolated interpreter is NOT_RUN; installed helper remains unchanged.

## Minimum earliest verification
Keep all original60 private admission tests intact; add private successful published-snapshot revalidation after ORIGINAL builder/controller paths are deleted, with no evidence reads outside protected copies. Negative tests: admission tamper/external pin mismatch, copied authority/controller/trusted-record/payload/package/evidence tamper, raw-authority or identity projection mismatch, duplicate/missing/extra refs and members, symlink/hardlink/unsafe ancestry/type/permission, producer self-approval or productionAuthorized=true, malformed CLI, and read-only filesystem preservation. New private fixtures only, not real build authority claims. Reuse current helper's full validation rather than creating a second business/trust implementation. No deadlines/kill/quotas.

Self-check, exact scoped commit/push/readback to existing task branch; publish code/log/source hashes plus old/new tests counts, no skips, clean HEAD/tree. Earliest compile is Python grammar + private tests, not Gradle. Stop with source handoff after this slice; main will freeze the larger installation decision/typed record/recovery/schema contracts separately. Overall actual build/admission/install/schema/recovery/production remains NOT_RUN.
