# JVC-OAI host adaptation R1 contract — 2026-09-05

Read-only architect `01a07103-0063-7d61-bc2e-878a696d7061` completed preparation. This freezes source scope, not production permission. Execution remains in the sole runtime ledger.

## Inputs and ownership

- API34b67fed96061bf9c3132106ca219fc6f5f6ba05 / treefb42c46c1f63299a37b44d7e55c6a303ddf016f1.
- Web6d88a3419d894c0abd0c9c3e96ea2e732890922b / treec2a6a192199c702ef3be9d48c8c4b4f4c86e51ba, retaining voice, landscape and archive changes. ce45 is ancestry only.
- Canonical installed source `/usr/local/sbin/cyf-api-kit` SHA25656537824cd33f6333f199ea1cebda90b127b39c079e08daad6d164607f788ef5; read source only, never execute during implementation.
- Dedicated Writer worktree `.worktrees/jvc-oai-host-adapt-r1`. Primary untracked `ops/release` is baseline input only: capture its exact bytes into isolated baseline, never change primary files. Independent review distinguishes baseline from implementation.

Modify only `ops/release/{common.sh,build-api.sh,verify-release.sh,deploy-api.sh,rollback-api.sh,tests/test-common.sh}` and worktree `docs/DEPLOYMENT.md`.
Add only `ops/release/host/cyf-api-kit`, `ops/release/{install-api-lifecycle.sh,activate-api-voice.sh,jvc-oai-r1-input.json}`, `ops/release/nginx/juyiting-voice-{http,server,deny}.conf`, `ops/release/tests/test-api-host-adaptation.sh`. A small shared host transaction/parser module under `ops/release/lib/` may be added if needed to avoid duplicated unsafe shell transactions; report exact paths before editing it.

## Canonical contract

One account `cyf-api`, one regular JAR `/opt/cyf/service/api/cyf-api-kit.jar` (0640 root:isp, nlink1), state `/run/cyf-api`, unchanged existing `.jasypt-password`, sole lifecycle `/usr/local/sbin/cyf-api-kit`. No old cyfapi/systemd/current.jar/symlink layout.

Lock order release FD8 (`/tmp/cyf-release-api.lock`,0660 root:isp,nlink1), lifecycle FD9 (`/tmp/cyf-api-lifecycle.lock`,0600 root:root,nlink1). Driver holds release lock across complete transaction. Canonical accepts only exact `CYF_RELEASE_LOCK_INHERITED_FD=8` with descriptor/path device+inode and held flock proof. Invalid/partial inheritance fails closed; absent marker acquires directly. Never reopen and deadlock the inherited lock, and never release between selection and health. Java closes FD8+FD9.

Artifact transaction stable-opens/verifies candidate and trusted path chains, copies to same-filesystem exclusive hidden regular staging, sets ownership/mode, fsyncs file+directory and makes byte-exact durable prior backup before stop. Persist PREPARED→STOPPED→CANDIDATE_INSTALLED→STARTED_HEALTHY→COMMITTED. Only canonical stop/start controls processes. Failure restores prior artifact via same transaction; record ROLLED_BACK_HEALTHY or FAILED_MANUAL_RECOVERY_REQUIRED. Explicit rollback retains current rescue artifact, may restore it if old version fails. No process scan/signal/argv capture/replay/direct Java/PID writes in deploy or rollback.

Lifecycle installer requires exact prior SHA, reviewed candidate digest, trusted path/inode checks and atomic durable replacement under lock order. Do not install during source work. Candidate binds127.0.0.1; installation requires local-consumer proof or independently accepted network ACL exception.

Build invokes absolute `/home/isp/wsps/cyf/ops/orchestration/cyf_orchestrator.py gradle`, valid ledger/exact tree/selector/fixture; no direct or nested Gradle flock.

## Voice activation separate from artifact release

API default-off remains unchanged. Optional root0600 regular nlink1 `/opt/cyf/service/api/.voice-runtime.env`: absent means all flags false; exact NAME=value allowlist parser, no source/eval/command substitution/value logging, sanitize ambient environment. Use standard shared Spring-AI variables and optional audio-specific overrides, no custom OPENAI_API_KEY. Preserve Jasypt source; require independent identity/cache keys according to accepted validator. No live secrets may be read during implementation.

Activation transaction keeps release FD8 across prior-config backup, canonical stop, atomic config replacement, canonical start, authenticated STT/TTS smoke and durable terminal receipt. Failure restores prior config using canonical. Credentials must not appear in argv/stdout/records. Exact voice Nginx routes, closed fallback and deny closure required. Live gateway audio capability remains unproven; text compatibility is insufficient.

## Offline tests and gates

Use fixture paths and fake lifecycle, no Java/namespace/production. Test valid inherited lock and contention; wrong FD/inode/path replacement/unlocked/partial marker; lock order; successful durable stop/swap/start; stop/rename/start/rollback faults; unsafe symlink/hardlink/mode/owner/cross-device rejection; absence of process controls in deploy/rollback; installer SHA precondition; strict config unknown/duplicate rejection and sentinel-secret non-disclosure; exact Nginx routes and deny closure; orchestrator build delegation. Separate independent reviewer0/0/0, then verifier executes tests once.

Old OPS first-checkpoint diagnosis is independent source work, not a reason to delay this worktree. Its old-layout tests cannot attest this new host path. Release guard must explicitly map applicable old security invariants to new-host tests rather than silently treating old131 as proof for a different lifecycle.

Release order after actual acceptance: canonical candidate install; immutable API build+verify; API flags-off deploy; Nginx closure; secure gateway/voice configuration+authenticated smoke; enabled Web artifact from current accepted baseline deployed last. No activation/deployment approval is implied by this contract.
