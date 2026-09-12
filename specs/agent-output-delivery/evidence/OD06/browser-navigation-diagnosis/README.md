# Browser probe investigation (not acceptance)

Credentialed r3 and r4 both timed out at `Page.navigate`, before API observations or output cards. r4 uses the same `ws` package as the existing Web smoke helper; this did not resolve the timeout. Both reported an unconfirmed CDP close; task-owned Chromium profiles/processes were cleaned up.

A separate credential-free probe reproduced HTTP navigation timeout with and without Fetch interception. A `data:text/html,hello` navigation succeeded. The localhost Vite URL returned HTTP 200 through a normal request. These facts do not yet identify a product defect or establish browser acceptance. Further network diagnosis is ongoing.

The Root probe now uses CDP mouse events after visibility and hit-target checks. Syntax checked only; this behavior still needs live verification. No OAuth headers or raw CDP event payloads are archived.
