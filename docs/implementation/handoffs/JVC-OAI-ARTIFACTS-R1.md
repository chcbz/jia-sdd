# JVC-OAI immutable build artifacts R1 — 2026-09-05

Both builds accepted, **NOT DEPLOYED**. No production key/config/flag/service/Nginx/database change has occurred in this thread.

## API

- Source34b67fed96061bf9c3132106ca219fc6f5f6ba05 / treefb42c46c1f63299a37b44d7e55c6a303ddf016f1; clean and independently accepted.
- Original one controller bootJar invocation succeeded in45m18s,179tasks(1executed/178uptodate). No tests, clean or publish tasks rerun. Cache4e635e021c3431279fb3e501fa0477e5b8d5c6dae2d31cd6b68dd3f4c4835ef4, selector`JVC-OAI-HOST-ADAPT-api-bootJar`, fixture`N/A`.
- OriginalJAR`.worktrees/juyiting-voice-release-api/starter/build/libs/starter-1.1.2-SNAPSHOT.jar`.
- Immutable0444copy`/tmp/jvc-oai-api-artifact-r1.pExH8j/evidence/starter-1.1.2-SNAPSHOT.jar`,217605642bytes, SHA256fa808e633e985551e66168b1d70c488d8cf01361662f630e9f48ccab265038d5.
- Full sealedlogsameevidence/gradle.log SHA2562de52870c7c887c039b8707df3c24dbb76d88edbe4e2756f3367e4a094c5558b; metadata.txt SHA2560cff69a5f36bafa662d9b7c3a4f98540b63ecb58c1d8960f2ffc94b0ad19698c.
- Main recomputedhashes and inspected nestedjia-chat-service JAR:90voiceclasses; actual SpringAI facade, activationvalidator and bothvoicecontrollers present. StandardBootJarLauncher manifest.
- Any later reviewed build-api metadata packaging must use same cache, valid verifiergate and exactsource/JAR; controller gatecheck precedescachelookup. Do not rebuild or relabel oldtests.

## Web

- Source6d88a3419d894c0abd0c9c3e96ea2e732890922b / treec2a6a192199c702ef3be9d48c8c4b4f4c86e51ba; clean, source review0/0/0 and94/94voice/experience/archive tests.
- One build with`VITE_JUYITING_VOICE_ENABLED=true`,512MiBNodeheap, existingexactlockdeps; no npm/testrepeats.
- Immutable0444archive`/tmp/jvc-oai-web-artifact-r1.B9dEVE/jvc-oai-web-dist.tar.gz`, SHA25686d3fd759cdf95050ff7520c4bdccf762eaca1f0be2a58c03f5a9970914df93f.
- Full build.log SHA256205d5a64b506129e99ee226bc5ed9b25119247c851e17000456223650899afad; dist.manifest.sha256 SHA2567b8f5240ac0c4cf7cbc69e1a8bb73df6951ea5b97f48ad857e79f62304b15a98; metadata.txt SHA25694a7dcb6a723565409bac80e81e2f56f6ebf847ea9ba51c48c452a6b1394f73a.
- Mainrecomputedhashes; index/voicecodepresent,nosymlinks; generatedcomponents.d.tsrestoredexactprebuild. Cachec1ef9c3fe2b6254c81555a6eb53df779fe9778936464762130decdf9bcb5dffd; fixturelockSHA0b73dab31d80a337585c5b8cb6e1de0dbc9183fc717aef1b3b9de92de244927e.
- A compilerflag in an isolated artifact is not liveactivation. Recheck remotes beforefinalpromotion, preserve neweracceptedchanges. NewhostAPI-onlyinput/verifierdoesnotyetbridgelegacyWebdeployment; separateadaptationtaskfrozenfromreviewfindings.

## Remaining release gates

HOSTR1 rejected0/5/0; R2sameWriter fixes actualsmokeschema, truthfulrecoveryreceipts, privatesafe fixtures, realcanonicalvalidationcoverage andprivilegedinterpreterstartup. Selector`all` wasunsafeandNOTRUN. Webdeploymentcompatibilitybridge is separatelyprepared. Freshindependentreview, actualofflineverification, perimeter/consumerproof, secureproviderconfigurationandrealSTT/TTSsmoke, thenfinalreleaseguard+explicitruntimeownerare stillrequired. Oldpacket131remainsNOTPASSEDanddeferred, neverwaivedorinstalled.
