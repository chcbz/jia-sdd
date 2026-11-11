# Collector preparation failures — bounded remediation matrix

Native unique Godel01a07767 completed COLLECTOR_REJECT on collector d971642dd8605e78d3a4dd57b4241dfa9af226a725a52c6a5c144ea36410485d / inner b8f0f02d4ede7c71ff714dba08f012c0393d0b12678a89d982037928df1e518f, P0/P1/P2=0/3/1. Summary below, not verbatim transcript. Product8bf22/a6c8 SOURCE/TEST_DELTA acceptance and13fresh+73reuse remain unchanged. Build invocations=0; preparation failures are not build/test failures.

First preparation gate: coordinator static rejection a821 collector, matrix /tmp/jy-live-preview-8bf22-collector-static-findings.md SHA1296e2814f2548a4ffb9192b12508e380d724d8cc2693565f8364d65156121a8. Retrospectively record as preparation rejection only, not independent review. Second preparation gate: authoritative d971 collector review rejected as above. Stop blind preparation loop, allow only this completed bounded matrix.

1 P1 collector40-42,112-123,379,423-425: inner hash only observed not pinned. Hardcode approved inner SHA; check admission and immediately predispatch; main ledger binds collector+inner/manifest.
2 P1 collector329-358,452-456: dist root symlink accepted and full-env-file scan misses individual private values. Anchored/lstat containment for root/all descendants; reject symlink/hardlink/special types. Classify nonpublic env values and scan individually; explicit approved public VITE allowlist, no dumping secrets.
3 P1 collector376-384,427-433,459-485 and inner31-54: initialization outside finalization, invocation increment before spawn, unsealed receipt. Structured terminal fallback includes initialization failure even when no file can be created; Popen successful creation before invocation increment; atomic/fsync readonly final receipt and stdout final SHA. Preserve once-only latch/native-vs-outer statuses, no retries.
4 P2 collector280-304: os.open mode filtered by umask and single os.write may be short. Write all bytes, fchmod original mode, fsync before atomicrename, cleanup only own temporary entry on error.

Already closed, do not rewrite: inner argv/syntax, writable native receipt, verifying/verifier/exact source+collector admission, actual snapshot comparison, donor full fingerprint/toolpins, native/outer statuses, one-shot latch.

Original Terra authors new immutable own script package only, preserving both old packages. No source/test/donor/snapshot/native/browser/production operations; same Godel reviews consolidated delta before native GO. Keep production voicefalse/512MiB/1200s+30s/readonly donor/user resource waiver.

Retrieved/recorded at 2026-09-07T11:18:37+08:00; original review completion time not supplied.
