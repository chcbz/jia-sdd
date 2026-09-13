# Independent host metadata probe admission

Reviewer `/root/od11_host_preflight_review` (release_guard) accepted frozen Root commit `5794498f6a9b2ad9079b52d251400caa7d6062b0` for one manual, bounded read-only host probe. No P0/P1/P2 remains for that scope. This is not a feature release GO.

The reviewer independently verified all three tracked files, exact Python and YAML hashes from host-preflight-admission.md, byte-identical embedded Python, one job/zero sources/no downloads, canonical path cases and process-read restrictions. Creation/start must each recheck the one Shenzhen ECS, read back the complete configuration, and never blindly repeat an unknown write. Deployment order metadata must establish the execution target. Other operational and business release gates remain open.

The earlier missing-file finding was withdrawn: the reviewer initially searched the wrong repository-relative evidence directory. The files were already tracked under `specs/agent-output-delivery/evidence/OD11/`. The valid path-canonicalization finding was repaired before this acceptance. Bounded Java cmdline inspection, helper digest reads and six TCP connection side effects are explicitly documented in the admission.

After acceptance, Flow created task-owned pipeline `5264702`. Readback parsed flow equals the entire frozen YAML and has no sources. The platform also returned outer default concurrency/settings metadata; the independent follow-up accepted these exact defaults because they add no source/trigger/variables/mount/job and are included in the start-time full configuration hash. Run1 was then started once and completed the probe on the sole expected ECS; see host-preflight-5264702-run1/.
