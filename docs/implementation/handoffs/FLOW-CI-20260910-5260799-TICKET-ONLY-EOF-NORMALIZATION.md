# Flow 5260799 ticket-only YAML readback normalization

**At:** 2026-09-10 Asia/Shanghai  
**Pipeline:** `5260799` / `cyf-api-kit-ci`  
**No run, deploy, or local Gradle/npm build was performed.**

The guarded configuration update returned a nonzero controller result because Flow persisted the reviewed YAML with the final newline removed:

- submitted candidate: 8,540 bytes, SHA-256 `4dd36471dbb8cabed32b3e7c9fe0efa53c25dd56db844fc4d39bd3e2949d749d`, ending `PYCLOUD\n`;
- saved Flow readback: 8,539 bytes, SHA-256 `3c0e04e2cde3fb5ccb71698ae3a49aa841cdfcd22f7fbf5cc5cda24a23baaa4c`, ending `PYCLOUD`.

This is EOF-only normalization. Readback semantic checks are positive: one `JavaBuild`; no `SetupJava`/`Command`; `develop` source and filter; `triggerEvents: []`; ticket SHA `4b787e71673996880a0d45362d8769d4f79fe86fb2f8a8181a40222e892baf6a`; compressed-ticket transport; no old bundled payload; no deploy/upload step; no credential literal. Encrypted variable group `44254` remains related to pipeline `5260799` and contains only encrypted `CYF_MAVEN_USERNAME`/`CYF_MAVEN_PASSWORD` variable metadata.

This is a controller comparison defect, not an unpersisted Flow configuration. Do not resubmit the same update. Continue only with the saved readback, fresh-ticket validity check, and one new manual run.
