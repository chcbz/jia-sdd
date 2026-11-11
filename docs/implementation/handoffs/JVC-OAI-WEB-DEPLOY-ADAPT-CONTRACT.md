# JVC-OAI Web deployment bridge contract — 2026-09-05

Read-only design by independent reviewer01a0715e, frozen from HOST83e32/tree74fe. Source task only, no runtime approval. OriginalHOSTR2 Writer owns its14paths. Newbridge Writer owns an isolated root worktree `.worktrees/jvc-oai-web-deploy-adapt-r1` from83e32, branch`codex/jvc-oai-web-deploy-adapt-r1`.

## Disjoint scope

Add only`ops/release/lib/web-deploy-adapter.sh`, `ops/release/verify-web-deploy-adapter.sh`, `ops/release/jvc-oai-web-deploy-r1-input.json`, `ops/release/tests/test-web-deploy-adaptation.sh`.
Narrowly modify only`ops/release/deploy-web.sh`, `ops/release/rollback-web.sh`.
No common.sh/build-web.sh/HOST/APIhelper/input/verifier/lifecycle/deploy/rollback/activate/installer; noAPI/Webapplication source; no primaryquickscript. Main alone writes docs/implementation.

## Immutable input

Dedicatedschema`cyf-jvc-oai-web-deploy-adapter-v1`; releaseID, exactWebhead/tree/ref, archivepath/SHA, compileVoiceEnabled=true, live/backup/recordroots, HTTPShealthURLs/timeouts, expectedAPIhead/tree, externalactivationproofschema/root, deterministicWebguardroot. No dummyAPIartifacts or fakelegacyjointrecord.

SourceWeb6d88a3419d894c0abd0c9c3e96ea2e732890922b / treec2a6a192199c702ef3be9d48c8c4b4f4c86e51ba; existingacceptedarchive`/tmp/jvc-oai-web-artifact-r1.B9dEVE/jvc-oai-web-dist.tar.gz`, SHA25686d3fd759cdf95050ff7520c4bdccf762eaca1f0be2a58c03f5a9970914df93f. ExpectedAPI34b67fed96061bf9c3132106ca219fc6f5f6ba05 / treefb42c46c1f63299a37b44d7e55c6a303ddf016f1, actualacceptedJARSHAfa808e633e985551e66168b1d70c488d8cf01361662f630e9f48ccab265038d5. No builds/npm/retest94.

StableopenarchiveO_NOFOLLOW, regularnlink1, hashhelddescriptor, rejectmutationduringread, extractverifiedprivatecopyorstablefd. Reject traversal/duplicate-normalizedpath/symlink/hardlink/device/FIFO/missingrootindex.html. DeriveextractedtreeSHA. Do nottrust repeated/tmp pathname reads.

## External activation gate

Adapter **consumes, never creates**, independentlyproducedimmutableAPIactivationproof. Freeze schema`cyf-jvc-oai-api-activation-proof-v1`, trustedroot`/var/lib/cyf-jvc-release-controller`(root0700), regularroot0400nlink1proof. Requiredfacts: finalacceptedHOSTidentity/lifecycleSHA, expectedAPIhead/tree/deployedJARSHA, statusACTIVATED_HEALTHY, authenticatedSTTandTTSPASS, exactNginxroutes/denyclosedPASS, loopbackbinding, activationrecorddigest. No credentials, envvalues,tokens orlogs. ConcretefinalHOSTproofdoesnotexistyet; missingproofMUSTfailclosed, nevergenerateaPASSplaceholder. Finalruntimecontroller/releaseguardmustproducefromactualruntimeevidence, notcompilerflagorunittestreceipt.

VerifierwritesimmutableWebguard+sidecarbindinginputSHA, adaptertoolSHA, archivepath/SHA/extractedtreeSHA, Webhead/tree, activationproofSHA/APIhead/tree, verificationPASS/deploymentNOT_PERFORMED. No activationproofcreation orarbitraryexternalcommand executionfrominput.

## Preserve retained Web mechanics

Replace legacyloader/jointrecord calls withWebadapterloader/guard, preserveWebexecutionflock, samefilesystemhiddenstage, exacttreeproof, byteexactcurrentbackupbeforecutover, renamecutover/health/automaticrestoreonanypostbackupfailure/immutabledeployrecord. Addguard/proof/input/toolSHAs todeploymentreceipt.
Rollbackvalidatesrecordbindings, approvalID andexacttrees; preservescurrentrescuebackupandcandidaterestoration. Emergencyrollbackvalidatesrecordedproofdigest butdoesnotdependontheexternalprooffile still existing.

Approvalbindings: existingID/APIhead/tree/Webhead/tree plus exactartifactSHA/WebguardSHA/activationproofSHA. Rootentrypoints`/bin/bash -p`, fixedPATH/LC_ALL, umask077 beforetools. Nosource/evalofinputcontent; noshell-startupenvinjection. This remainsartifactdeployment, notprocess/servicecontrol.

## Offline verification contract

One privateexclusivemktemp root; fakehealth only, no/dev/shm/hostpaths/network/npm/build/processcontrol/outsidefixturewrites. Coverexactartifact/identity; hash/symlink/hardlink/mutation/unsafearchives; missing/wrong/unhealthyproof; API/STT/TTS/Nginx/loopbackmismatch; compilerflagwithoutprooffails; immutablecompleteguard; everyapprovalbinding; actualretaineddeploysuccess; injectedrename/backup/extraction/tree/health/recordwritefaultrecovery; actualrollback/rescueandIDbinding. Tests must exerciseactualentrypoint/helperlogic ratherthan duplicating it infakes. Static-only firstcandidate, independentreview/safetyadmission, thenoneofflineverification.

NoAPIorWebproductionreleasebeforeacceptedHOSTR2+offlineproof, actualAPIactivation/perimeterproof andfinalreleaseguard. Nolegacy131waiver. IndependentWebsourcewritingcanproceedwhileHOSTR2fixes5P1s; mergeonlyconflict-freeacceptedexactcommits.
