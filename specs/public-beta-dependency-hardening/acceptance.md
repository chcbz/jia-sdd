# Public beta dependency hardening acceptance

- [ ] The production lockfile has no unresolved DOMPurify, PostCSS or nanoid advisory covered by the 2026-08-24 exception.
- [ ] Untrusted Markdown/Chat content remains sanitized against script, event-handler, URL and custom-element bypasses.
- [ ] Build tooling does not read attacker-controlled source maps or execute in the deployed browser artifact.
- [ ] Exact Web/root revisions, audit output, build hashes and independent review are recorded.
