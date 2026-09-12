# Browser probe investigation (not acceptance)

Credentialed r3 and r4 both timed out at `Page.navigate`, before API observations or output cards. r4 uses the same `ws` package as the existing Web smoke helper; this did not resolve the timeout. Both reported an unconfirmed CDP close; task-owned Chromium profiles/processes were cleaned up.

A separate credential-free probe reproduced HTTP navigation timeout with and without Fetch interception. A `data:text/html,hello` navigation succeeded. The localhost Vite URL returned HTTP 200 through a normal request. These facts do not yet identify a product defect or establish browser acceptance. A subsequent credential-free probe with `--password-store=basic` returned Page.navigate and loaded Vite HTTP responses. This narrows the hang to headless password-store/keyring initialization; no product source changed. That diagnostic later reported a pending Fetch command during cleanup, so it is only navigation evidence. Task Chromium processes/profiles were absent afterward.

The Root probe now uses CDP mouse events after visibility and hit-target checks. Syntax checked only; this behavior still needs live verification. No OAuth headers or raw CDP event payloads are archived.

A credential-free real Chromium data-URL probe observed a clean local close response with code1000 and empty reason. The shared helper rejects it because the generated reason was not echoed. `chromium-close-observation.json` preserves the exact safe fields. Task process/profile cleanup succeeded. Root is reviewing a probe-only compatibility adjustment; the original r5 result remains failed overall.
