# Dispatcher repair accepted for continued development integration

Candidate: `f6d7e2780a26090e4ecd8b3f0e218b4c669a7f97`, parent `52cc2aae1d9a685295e5b25e1347557e0b3ca407`.

Independent read-only reviewer `/root/od06_dispatcher_review_fallback` returned **APPROVE**, with no P0/P1/P2 findings. The configured adversarial reviewer failed before review with its provider's `reasoning_content` API error; it supplied no review. The fallback independently inspected the complete diff, security chains, handshake interceptor, error handlers, actual configuration test, report and package. No Gradle rerun or product writes were performed by the reviewer.

The repair permits container `DispatcherType.ERROR` in the default security chain, preserving authentication on ordinary `/error` and private requests. External HTTP headers or parameters cannot select the servlet dispatcher type. Higher-priority chains retain their scoped matchers; Agent handshake key and ownership checks remain active.

Root verified clean candidate source, commit/file correspondence, scoped **2/2** report, package SHA-256 `ec2b87ca92e17bd0997a97a6c40bf660de64ba62f4a68364a32b2d93c0053033`, and packaged security class matching compiled output. API r12/PID714089 runs that jar; temporary error-detail properties were removed. See [the association](api-dispatcher-f6d7e278/observation.json).

Normal-configuration handshake results: missing/invalid key401, valid key without Agent400, valid key with an unowned Agent403, valid key with owned Agent101. The earlier true500 came from the isolated database missing exact-case `CORE_LOG`; correcting that development fixture was not a product/production migration. See [diagnosis and evidence limits](live-ws-diagnosis/README.md).

Limitations: the MockMvc test sets ERROR explicitly; the handshake file is a redacted result summary, not a complete raw capture. Original Gradle stdout and a pre/post-test source manifest were not retained. The jar uses documented development dependency substitutions. This acceptance unlocks trusted conversation/client integration only; trusted runs, tickets, publication, offline downloads, full R1/R2, canonical packaging and release remain unaccepted.
