# UR05 producer first checkpoint — SOURCE ONLY, fields proposed for main freeze

Base 2690fbbf040017083c6783a3cc65ce2eb631e136/tree5ca30834e19b11ddb457f3231546175e83bf1e55. Three newly authorized source paths only. No Gradle/install/Flow/production execution.

## Proposed CLI (no build invocation)
`package-api-local.py --opt-in --source-root ABS --commit HEX40 --tree HEX40 --version TOKEN --build-id TOKEN --build-root ABS --evidence ABS --evidence-sha256 HEX64 --output ABS.tgz`
source-root = actual API Git top-level; build-root = externally configured build output root, separate from source and output; evidence is inside build-root; output parent is a physical private directory, output must not exist, no overwrite. Evidence SHA pin is a controller consistency input, NOT build authentication. No Flow env or numericRun aliases.

## Proposed local build-evidence v1
Exact keys:
```
format: cyf-api-local-build-evidence-v1
identity: {version,buildId,commit,tree}
sourceRoot: absolute canonical API Git top-level
buildRoot: absolute canonical external build root
sourceBefore: {commit,tree,clean:true}
sourceAfter:  {commit,tree,clean:true}
invocation: {
  argv: [actual Gradle argv, public arguments only],
  exitCode:0, cacheHit:false,
  log:{path:absolute physical file under buildRoot,sha256,size},
  selector:public token,fixtureSha256:hex64,
  inputs:[{path:absolute physical source/init/settings input,sha256,size}]
}
tests: [{task:exact :path,selector:public token,fixtureSha256:hex64,
         reports:[{path:absolute physical XML under buildRoot,sha256,size}]}]
validateLayering: {task:':validateLayering'}
bootJar: {task:':starter:bootJar',proof:{path,sha256,size}}
opencv: {path,sha256,size}
```
Producer cross-checks paths/hash/byte size, actual XML counts and testcases, task-executed log lines (not UP-TO-DATE/FROM-CACHE/SKIPPED/NO-SOURCE), real orchestrator lock/no EVIDENCE_HIT, exact argv inclusion and no exclusions/secret args, identity/readback, and init proof BEGIN/END hash markers. Required test task set comes from explicit controller evidence (nonempty + starter publicArtifactVerifierTest and poiProductionRuntimeClasspathTest), not an invented whole-suite gate. Log/input/XML proof files remain controller-owned outside package; package records their digests. SourceBefore/After JSON alone is not proof: init executes its own Git checks before/after fresh bootJar, producer rechecks current Git before/after export. Exact selector/fixture remain separate from a successful exit.

## BootJar init
Opt-in env `CYF_LOCAL_RELEASE_OPT_IN=1`; required public inputs `CYF_LOCAL_RELEASE_SOURCE_ROOT`, `BUILD_ROOT`, `VERSION`, `COMMIT`, `TREE`, `BUILD_ID` (each suffix under CYF_LOCAL_RELEASE_). Only canonical matching API settings root/root name jia and :starter:bootJar of real BootJar ancestry, no included-build/Test/default task changes. Four frozen CYF-* attributes declared as task inputs and set at configuration; actual Implementation-Version untouched. BootJar-specific up-to-date/cache disabled; reject existing target jar/proof, alias paths, source mismatch/dirty source. External build routing, private dependency resolution/pre-consumption OpenCV verification and build sequencing stay controller prerequisites, not fake Flow init calls.

Fresh doFirst/doLast proof after original bootJar publicArtifactVerifier action:
```
format:cyf-api-local-bootjar-proof-v1
identity:{version,buildId,commit,tree}
sourceRoot,buildRoot,sourceBefore,sourceAfter
 task:':starter:bootJar'
 metadata:{CYF-Release-Version,CYF-Source-Commit,CYF-Source-Tree,CYF-Local-Build-Id}
 moduleVersion:actual project.version
 implementationVersion:actual manifest attribute or null
 jar:{path,sha256,size}
 publicArtifactVerifier:'bootJar-original-doLast-completed'
```
Exclusive `buildRoot/local-bootjar-proof.json`, actual jar opened/hash read, original public verification never replaced by Python scanning. Init does not rewrite JAR after build. Proof/log checks remain consistency checks; malicious builder can forge them, later trusted root admission MUST independently authenticate expected source/build/evidence/package.

## Five-payload receipt and external result
Receipt exact keys:
```
format:cyf-api-local-release-receipt-v1
status:packaged
producer:{kind:local-build-v1}
identity:{version,buildId,commit,tree}
source:{commit,tree,cleanBefore:true,cleanAfter:true}
evidence:{sha256,invocationLogSha256,selector,fixtureSha256,inputs,tests,bootJarProofSha256}
applicationJar:{path:application.jar,sha256,size}
dependencyProvenance:{path:dependency.provenance.json,sha256,size}
verification:{mailRuntimeClasses:[...],publicArtifactVerifier:'bootJar-original-doLast-completed'}
```
Metadata and sidecar format names are `cyf-api-local-application-metadata-v1` and `cyf-api-local-application-sidecar-v1`; both bind identity, receipt SHA, JAR and dependency provenance; metadata additionally records actual moduleVersion and nullable Implementation-Version. No package hash inside five payloads.

Stdout external proof: `{format:'cyf-api-local-package-v1',identity,package:{path,sha256,size},receiptSha256,applicationJarSha256,dependencyProvenanceSha256,buildEvidenceSha256,productionAuthorized:false}`. Producer success = packaged, NOT installed/released/actual tests authenticated. Exact five members retain original names. Atomically publish no-overwrite to external output, source clean readback before publication, cleanup only exclusive stage.

Safe failure output: fixed codes only (INPUT_INVALID, PATH_UNSAFE, SOURCE_MISMATCH, SOURCE_DIRTY, EVIDENCE_INVALID, EVIDENCE_TAMPERED, BUILD_NOT_FRESH, TEST_EVIDENCE_INVALID, JAR_INVALID, MAIL_RUNTIME_INVALID, PROVENANCE_INVALID, OUTPUT_EXISTS, IO_FAILURE); no argv/env/log/XML contents or original exception messages.

## Current prerequisite gaps
Actual local repository/OpenCV resolution/external build routing is controller-owned and must be supplied explicitly; cold-init.gradle is Flow-gated and cannot be used with fabricated Flow env. Actual Gradle/test/public verifier/bootJar integration NOT_RUN. No assumed module Implementation-Version (source only sets project.version); preserve actual manifest result. Root admission/install/transaction/schema/maintenance/cutover/three-Agent proof remain future slices.
