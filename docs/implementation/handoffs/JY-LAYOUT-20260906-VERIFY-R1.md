# Verification startup attribution — 2026-09-06

Final application source3c644af/tree055215 remains SOURCE ACCEPT. Final production build exit0 and source-clean restoration complete; do not rebuild unchanged source.

First final static-browser run failed before navigation: BROWSER_PARENT_PROFILE_UNPROVEN at sequential-layout.mjs:82. It spawned /usr/local/bin/chromium-headless-smoke, a shell exec wrapper; immediate ownBrowser.root() can observe the directly spawned wrapper before chromium exec exposes --user-data-dir. Cleanup subsequently recorded the same direct-child PPid/profile/startTime proof, browser natural exit0 and remaining[]. Thus this is harness startup ordering, not application behavior or browser inability; no geometry acceptance claim.

Bounded remediation proposal: preserve strict direct-child parent/profile/startTime ownership, but obtain proof by bounded wait within the existing 180s startup budget, checking early child exit and stderr milestones; do not relax identity or inspect/signal arbitrary foreign processes. Only after proof may CDP endpoint control proceed. Preserve failed artifacts, final source/build attestation and fixture digest; one new evidence directory/unique profile for the corrected harness run after main inspection. No application source change, no extra build.

## Corrected root cause from exact event evidence (supersedes initial startup-order hypothesis)

Verifier browser-first-failure-attribution.json and events.jsonl prove root ownership existed at 05:55:10Z. The same PID1538091/PPid1537956/startTime3024665072 later had Chromium's process title rewritten into one space-delimited cmdline string (05:55:26Z), so Array.includes(exact NUL argv token) returned false. This was not insufficient 180s readiness or merely proof before exec. Correct remediation is bounded exact profile argument parsing for both cmdline representations, preserving direct parent, PID/startTime and rejection of prefix/suffix/foreign identity. Test positive/negative parser cases offline before one controller-approved browser rerun; no rebuild or app changes.
