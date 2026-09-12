# Isolated Web readiness

Accepted Web212bfe4 is served at http://127.0.0.1:15173 with API and OAuth proxies fixed to the running local API10018. Startup overrides HTTPS only in an external development launch script; no Web source changed. Homepage HTTP200 and anonymous output-route proxy HTTP401 were observed. This is HTTP/proxy readiness, not browser UI or authenticated output acceptance. The existing production build/test evidence is retained without an unaffected rerun.

The synthetic OAuth client currently has CLI redirect http://127.0.0.1:18080/callback. Browser authentication requires a public PKCE S256 client and http://127.0.0.1:15173/oauth2/callback; registration and actual login are pending. No login attempt or credentials were placed in this archive. Use the recorded PID plus startTicks/executable when stopping only the task-owned Vite process.
