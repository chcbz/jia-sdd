# CYF online functionality audit — 2026-09-14

## Scope and evidence

Read-only online audit performed on 2026-09-14 Asia/Shanghai. Evidence combines the active nginx configuration, local service health, recent API access/application logs, installed web bundle, and Alibaba Cloud Flow run details. No production data writes, deployments, restarts, or configuration changes were made.

## Current release and baseline

- API: Flow `5260799`, Run `56`, `SUCCESS`; exact source `9fdd2e6a3a8d6e4f53ab2d26be7af1122eeca3ce`; artifact SHA-256 `da623f9da64cf266a11a2c8008a7283cc4b247079f6c46c7f3cc6172987cce5f` is installed.
- Web: Flow `4403172`, Run `102`, `SUCCESS`; exact source `c3aa00c9dcd5a9f2b8df52cdb998ee639410f453` is installed.
- The API process is healthy on loopback (`/actuator/health` returns `UP`). No API 5xx was observed in the access log after the instance became ready at approximately 10:54 CST.

## Confirmed functional failures

### P0 — API proxy omissions make browser requests fail at transport level

The deployed web bundle has `VITE_API_BASE_URL=https://api.chaoyoufan.cn` and actively defines/uses `/economy`, `/msg`, and `/tip` clients. The active `api.chaoyoufan.cn` nginx vhost has no proxy location for any of those three prefixes; its fallback is `return 444`.

A real browser-style `fetch` to each of the following rejects with `TypeError: fetch failed`, rather than receiving an HTTP API error:

- `/economy/capabilities`
- `/msg/list`
- `/tip/list`

There is also live production evidence: at `2026-09-14 12:33:18 CST`, a WeChat mini-program attempted `OPTIONS /economy/capabilities` and nginx returned `444`.

Impact:

- Juyi Hall/profile/economy-capability loading can surface `Failed to fetch` after authentication.
- Message Center requests (`/msg/list`, read/read-all/recycle) are unreachable.
- Phrase tipping (`/tip/create`) is unreachable.
- This explains the reported mini-program `Failed to fetch`; it is a routing failure, not a 3-second performance refusal.

### P1 — one user’s listed chat conversation cannot be opened

At `2026-09-14 12:18:27 CST`, the user successfully listed conversations (`POST /chat/conversation/list` = 200) but `GET /chat/conversation/content` returned 404. The running service logged that the conversation messages contain rows outside the authenticated owner scope and denied the entire read.

The exact service code intentionally fails closed on that condition. The safety behavior is appropriate; the data/query invariant is not. The affected conversation is unusable until ownership/data consistency is repaired or the retrieval path can safely ignore/report unrelated rows.

### P1 — persona catalog is partially denied during normal Juyi Hall use

At `12:18` and repeatedly after `12:33 CST`, `/agent/personas/catalog` returned HTTP 200 but the service logged `AGENT_FORBIDDEN: Persona catalog runtime escaped the byte-exact requested scope`. The app continues enough to load roster/task data, but the persona catalogue response is not cleanly successful and may cause missing/incomplete persona UI for the affected account.

## Functions verified working now

- Public web entry and guest-demo shell load in headless Chromium without page-level `Failed to load`/JavaScript errors.
- API CORS preflight is correct for `/oauth2/token`, `/oauth2/authorize`, and `/agent/map` from `https://kit.chaoyoufan.cn`.
- Two real WeChat third-party login sequences completed on 2026-09-14 (11:12–11:14 and 12:17–12:18 CST): authorize → login page → `/oauth/third-party/wxmp` → token → `/user/my` → `/agent/map`, with the latter application requests returning 200.
- Juyi Hall roster and task search/status calls returned 200 for a real authenticated mini-program session.

## Not proven by this audit

The audit did not replay a credentialed password login. However, production access logs show `POST /login` returning 302 followed by `POST /oauth2/token` returning 200 at 06:50 and 09:34 CST on September 14, which is positive evidence that form-login completions were occurring. A disposable authorized account is still needed for a controlled end-to-end acceptance case.

## Availability history

Current service is healthy, but the access log records deployment-related 502 windows before readiness on September 14, including 10:04–10:10, 10:26–10:53 CST. The active API JVM started at 10:47:18 and Run 56 measured roughly 418 seconds to application readiness. These are historical outages, not current 5xxs. They reinforce the release-schedule requirement to avoid daytime backend deployment; the installed 00:00 policy has not yet had its first scheduled execution.

## Recommended repair order

1. Restore proxy coverage for `/economy`, `/msg`, and `/tip`, with an exact nginx config readback and a live CORS/browser-fetch probe.
2. Diagnose and repair the scoped chat-message data/query invariant using a controlled fixture first; do not weaken the owner-scope denial.
3. Diagnose the persona-catalog scope rejection and make the frontend show a deterministic recoverable state if data is not eligible.
4. Run a password-login acceptance flow with an authorized disposable account, then bind results to the exact Flow source/run.
