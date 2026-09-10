# Reader fixed actions — released

- **Web commit:** 88425bd5416388e86ff1c1420502c3b571c861f (ix(reader): keep navigation fixed and maximize portrait reading area), pushed to cyf-web-kit master.
- **Root pin:** 4b8edd1550bbd82526085c618f794c057e1a75d5 updates only the web gitlink. Existing pi worktree changes were not staged or included.
- **Flow:** organization 5fb7d76ee6f9d07f148529c7, frontend pipeline 4403172, Run **86: SUCCESS**. The run checked out the exact Web commit above; JavaScript scan, Node.js unit tests, Node.js build, and host deployment all succeeded.
- **Deployment:** deploy order 69337967, host group 28833, one batch / one host: Success, client healthy.
- **Artifact:** 102,878,602 bytes; MD5 24dbe1069f74e54e3637c0c0d730656f; SHA-256 499f33b52153e59acdb211b064c6be93fdb25a7509be0069fc8399dd800cc09.
- **Online verification:** at 2026-09-10T09:19:41.5581527Z, the production entry, main index chunk, and the JuyiHallEntry JS/CSS assets matched the Run 86 artifact byte-for-byte. The entry references the Juyi Hall lazy pair.
- **Reader rules in deployed CSS:** fixed four-column controls; 40px minimum touch height; portrait handnote drawer; compact portrait header; normal capsule right-edge and virtual-landscape left-edge reservation.
- **Not performed:** physical WeChat device acceptance. This deployment verification does not establish real-device behavior.

Machine-readable details and hashes: docs/releases/2026-09-10-reader-fixed-actions-flow86.json.
