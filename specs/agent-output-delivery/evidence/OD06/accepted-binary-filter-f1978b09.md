# Binary upload repair accepted for development integration

Candidate `f1978b09ac7d567a53923f7c7e5c1bc3667e6a13`, parent `43e6bb94`. Independent read-only reviewer `/root/od06_tenant_review`: **APPROVE**, no P0/P1/P2.

Exact upload PUT requests retain the original stream through metadata-only logging. The log service does not request body/servlet parameter parsing in that mode; query/header audit sanitization remains. Ordinary cached bodies preserve raw bytes and Chinese JSON audit compatibility. Upload controller/service authentication, size/hash verification and storage semantics are unchanged.

Root and reviewer verified affected30/30 tests, original r5 stdout, clean frozen source, the development bootJar and three packaged classes matching compiled output. See [observation.json](api-binary-filter-f1978b09/observation.json). Jar:228808922 bytes, SHA256 `1438fa8d59e8de9e1ab8ab65c5c19698725d5b59e1031b7654f8b232e6a71f6d`.

This permits the next isolated API restart and real binary HTTP validation. It does not claim that restarted HTTP/upload/scanner/browser tests have already passed. The reviewer noted that noncanonical paths, if admitted by the surrounding server, fall back to byte-exact buffering rather than the exact-route stream path. No common logging refactor or security allowance for such paths is introduced.

Only the isolated CORS property will also gain the exact Vite15173 origin at this necessary restart. Its previous omission was demonstrated by real no-Origin200 versus Vite-Origin403 comparisons; production CORS and ACL are unchanged. Canonical packaging, full R1/R2 and release gates remain separate.
