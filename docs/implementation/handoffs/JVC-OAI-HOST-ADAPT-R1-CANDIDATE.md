# JVC-OAI canonical-host R1 candidate — 2026-09-05

Source only, not deployed. Worktree `.worktrees/jvc-oai-host-adapt-r1`, branch `codex/jvc-oai-host-adapt-r1`.

- Baseline3eb06c589334977ac914b433423b6d23887abfea / tree8546163d32b71c8f01cb3dbef89e5ff03c2500c9 captures legacy release source and current deployment documentation from primary workspace without changing it.
- Candidate83e32efe31efdf592388f8e7a2c8b31aecd8943c / tree74fe56cebc8d234027e58b2e774c9898e8d50717; clean,14paths,+2248/-702.
- Writer01a07121-a86e-7e13-bd4e-611c33076550 reports bash-n9, embeddedPython3.6AST33, JSON/pin/candidate SHA consistency, scoped20unrelated files byte-preserved, diff-check and no pycache. No runtime selectors run.
- Scope matches `JVC-OAI-HOST-ADAPT-R1-CONTRACT.md`; single added helper `ops/release/lib/api-host-transaction.sh`. Current installed canonical source hash rechecked56537824cd33f6333f199ea1cebda90b127b39c079e08daad6d164607f788ef5; it has not been installed/changed/executed by this task.
- Concrete build-script hazards found during preparation (task-before-orchestrator-options; mktemp followed by open-x) corrected before candidate. No failed build of those scripts occurred.

Independent reviewer01a0715e-24b1-7001-917c-f8bf252eaca7 reviews exact candidate and determines safety of one offline `bash ops/release/tests/test-api-host-adaptation.sh --selector all` invocation. Source and actual offline verification remain pending. Earlier review-binding capacity rejection made no ledger change; own Web build subsequently completed and freed admission, without preempting another task.

No old current.jar/systemd packet is promoted. Final independent release guard must map applicable old semantic security invariants to new actual host-path proof. Source implementation includes canonical FD8→FD9 inheritance, regular-JAR transaction/recovery, strict secret/env handling, installer and activation/Nginx clauses, but these are implementation claims awaiting independent acceptance.

## Build inputs, not deployment status

API34b67/treefb42 source acceptance remains separate from `JVC-OAI-ARTIFACT-API` bootJar verification. The artifact task owns original build; never rerun broad tests or control another daemon.

Web6d88/treec2a6a192:94 focused tests and one **voice-enabled** Vite build passed. Artifact `/tmp/jvc-oai-web-artifact-r1.B9dEVE/jvc-oai-web-dist.tar.gz`, SHA25686d3fd759cdf95050ff7520c4bdccf762eaca1f0be2a58c03f5a9970914df93f, mode0444. Full build logSHA205d5a64b506129e99ee226bc5ed9b25119247c851e17000456223650899afad; dist-manifestSHA7b8f5240ac0c4cf7cbc69e1a8bb73df6951ea5b97f48ad857e79f62304b15a98; metadataSHA94a7dcb6a723565409bac80e81e2f56f6ebf847ea9ba51c48c452a6b1394f73a. Hashes independently recomputed by main; source clean after own generated component declarations restored byte-exact. Cachec1ef9c3fe2b6254c81555a6eb53df779fe9778936464762130decdf9bcb5dffd. No production flag is enabled by this isolated compiler input.

O01 newer candidate has no accepted runtime artifact and has not been substituted into this input. Recheck remote ancestry at final promotion and preserve any newly promoted changes; no global waiting on its independent unfinished R3 task.
