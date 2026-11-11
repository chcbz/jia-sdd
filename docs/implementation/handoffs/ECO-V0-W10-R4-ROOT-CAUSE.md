# W10 corrected-tree Node verification / stopped second failure

Exact source `3b337d22ee4ec543b7223d45131bcbf8ee38d41d`, tree `3302bf9f6bbba665f8cd7c96fd9fa50346a1ea24`. Verifier `01a0718b-c0a9-7fe1-8427-4a7461c8b34c`, session 21973 naturally exited 1; owned TMPDIR/HOME empty and removed, logs preserved. No Gradle, live installer or production action.

| Selector | Actual result | Evidence |
| --- | --- | --- |
| `node --test test/skill-install-manager.test.mjs` | PASS 47/47, no fail/skip | `ad4ad6569ef449753cc0e184e676eca9dee9f16d18f53f8c40dceb1471cf0453` |
| `node --test --test-name-pattern=installer test/workspace-manager.test.mjs` | 41 total, 4 pass, 1 fail, 36 skipped | failed `e4e5bae2f1dac5992d9ac573eab730f63652b96964f505a764fcbfd13a0100fc` |

Fixture digest `85f0550f17035d2206b5b703719c535d8d2d98a5a1fb4d3db54e462226e4ff76`. Logs `/var/tmp/eco-w10-r4-node-adbiDh/eco-w10-r4-node-{installer,packaging}.log`, respective SHA256 `60e77bf3620d87f30ccdfc2a3430e467613b66821cc87076e9e99e0a79c2f9d0`, `fd933d4f879b6a5416b6f5cef6da56398f5bbc533e216dc1865146e789ccb4e6`. Cleanup `/var/tmp/eco-w10-r4-verifier-2h0A0J/postflight.log`.

## Root-cause matrix / bounded remediation

1. Earlier production Stats `.st_dev` defect is closed by the actual 47-case PASS; preserve that evidence, do not claim the entire W10 accepted.
2. New packaging failure `workspace-manager.test.mjs:1408–1421`: wrapper `umask 077` means fixture `writeFileSync(mode:0644)` creates 0600. Later fixed-0644 assertion therefore fails without any installer mutation. Explicitly establish/assert the intended starting referent mode or compare a verified pre-execution snapshot, independent of ambient umask. Preserve symlink refusal/content/mode/atomicity checks. This is a fixture failure, not evidence of a live chmod vulnerability. Test correction source needs independent review; retain restrictive evidence-directory permissions.
3. R01 runner `af40adbe` requires `managed-host.mjs` added to the install script's explicit staging list. Complete this separately scoped packaging integration in a new tree based on that runner candidate, preserving original W10 tree. Include a staged-module assertion and immutable parent/tree manifests. No host provision/runtime/socket operations.

Stop at second consecutive failed verification. No blind retry. After original installer writer admission and approved bounded remediation, fix (2)/(3), independent review, then targeted packaging verification plus changed-runtime selectors as needed. Full installer evidence is tied to its original tree; cross-tree reuse requires byte-exact runtime/test proof, not relabeling.

Additional bounded integration requirement found 2026-09-06: supported skill frontmatter allows `metadata.version`, not top-level `version`. W08 is correcting six packages to name/description/metadata.version. Existing W10 `parseSkillIdentity` lines655–675 reads only top-level version; next installer owner must support canonical metadata.version, preserve strict exact identity and reject duplicate/conflicting identities. Add matching actual package install regression fixtures (including valid required description), no generic YAML execution or new signature platform. Original 47-case pass remains true only for original source/fixtures and does not prove new metadata compatibility. Combine this narrow parser/test fix with already authorized pending umask fixture + managed-host stage-list integration in `eco-v0-agent-integrated`, under one admitted source owner.
