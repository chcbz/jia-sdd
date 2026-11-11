# JVC-OAI host R1 independent review remediation — 2026-09-05

Reviewer01a0715e-24b1-7001-917c-f8bf252eaca7 REJECT0/5/0 on83e32efe31efdf592388f8e7a2c8b31aecd8943c / tree74fe56cebc8d234027e58b2e774c9898e8d50717. Offline selector is NOT SAFE and has not run. No production permitted.

| Finding | Exact cause/boundary | Required bounded correction/proof |
|---|---|---|
| P1 real voice smoke contract | activate-api-voice.sh106–117 checksdata.transcript instead of accepteddata.text and omits mandatory synthesisrequestId; fakecurl259–269 masks errors | Use accepted API schema, valid independent requestId for requests, strict fake validates actual transmitted fields and returnsdata.text; assert actual synthesisMIME/body validity |
| P1 false health/commit records | deploy49–87,rollback73–106,activate66–122; helper427–458. Stop can change runtime then fail while PHASE stillPREPARED; recovery claimshealthy without proving it. Post-start receipt/finalize failure can restore oldselection while record remainsSTARTED_HEALTHY/COMMITTED | Represent stop-attempt/state-unknown before call. Recover via canonicalstop/restore/start and health proof. Durable journal/PHASE/terminal transitions must remain truthful for receiptwrite/fsync/finalization failures; never rollback leaving a stale committed record. Test partial-stop and all terminal write/finalize faults, not only earlyfakefailure |
| P1 unsafe offline selector | predictable `/dev/shm/cyf-host-cross-device-stage.$$` ordinary redirection in test229–232 can followprecreatedsymlink and is outsideowned fixture | Exclusivemktemp0700owned directory/file on secondfilesystem; exact bounded cleanup. No sharedpredictablepath or broad deletion. Fresh independent safety admission before any selector |
| P1 semantic test gap | locks158–190 exercisefakecanonical; realcanonical onlygrep191. Installer312–313 skips trustedchain, Nginx292–295 stringchecks only | Exercise production validation function bytes/logic from canonical candidate under ownedfixtures (not reimplement same semantics in fake). Cover inheritedFD/path/inode/heldflock/partialmarker/no-reopen/order/trustedchain and JavaFDclosure sourcebinding. Exact parsed Nginxroutes/upstreams/POSTrestrictions/authforwarding/denyclosure assertions |
| P1 pre-script environment injection | deploy/rollback/activate/install use`#!/usr/bin/env bash`, permittingPATH/BASH_ENV before code | Absolute privileged interpreter `/bin/bash -p`, fixed PATH/environment before tools; fixture verifieshostilePATH/BASH_ENV can'texecute payload, with no production paths |

## Web compatibility gap (separate bounded slice permitted)

Newjsonschema`cyf-jvc-oai-host-release-v1` plus API-onlyverify-release are incompatible with retainedWebloader/record. common.sh142–217 onlylegacy`cyf-m2-c08-release-input-v1`; build-web27/deploy-web26–31/rollback-web25–35 stilluselegacyloader+jointrecord. Accepted6d88 voice-enabledartifact cannot be deployed through newinput. Need narrowly scoped adapter or genuinely compatible jointrecord path, no bypass throughdirtyprimaryquickscript and no rebuild of acceptedunchanged artifact.

## Reuse and scope

Keep baseline/current canonical source positives: FD8→FD9order, inheritedinode/descriptorproof/no-reopen, JavaFDclosure, canonical-onlysignals, strictallowlist/defaultoff/Jasyptunchanged, installeroldSHA, stablecopy/fsync. Preserve existing14path implementation except boundedfindings; no API/Websource, production, keys, DB, Gradle or namespace. OriginalWriter may add focusedtests/sharedpure validation extraction if necessary, listpaths; staticchecks+cleanR2candidate first, fresh independent source/safetyreview then oneoffline test run.

Old131 is stillNOTPASSED and notsemanticallyreplaced until realcanonical/transaction/config/Nginxproof passes. API/Webartifact builds remain independent and reusable, notdeploymentapproval.
