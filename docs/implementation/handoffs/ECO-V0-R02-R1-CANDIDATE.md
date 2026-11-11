# R02 rental Web source candidate — 2026-09-06

Terra owner recovered from one capacity exception and committed clean `53e12c87c03b14f2562f4fbd7ea1a131698db28a`, tree `9b4c58d408638bc068c493154dd2525ac7a981a4`, parent combined Web R4 `06875878bd21760ae172bf578afb1ee3889aa923`, in `eco-v0-rent-web`. Main verified Git identity and clean state.

Source adds explicit server quote/confirmation/cancel, wallet/period/expiry/token-cost distinction, immutable reservation and free-reprovision receipt handling, canonical lease/refund recovery, manual paid renewal, free reprovision, exact scoped persisted replay and monotonic identity/version fencing. Local path preserved, no legacy free-server fallback. These are writer claims pending independent review and execution.

Changed source: `src/components/juyiting/{PersonaCatalogPanel,HostingRentPanel}.vue`, `src/components/world/JuyiHall.vue`, `src/composables/juyiting/{useHallData,useHostingRent,hostingRentContract}.js`.

Tests: `tests/hosting-rent.test.js`, `tests/hosting-rent-ui.test.js`, `tests/juyiting-component-behavior.test.js`; fixture `tests/hosting-rent-fixtures.js`. Syntax and whitespace only so far; no npm tests/build/deployment. Review must also consume the unaccepted combined R2–R4 wallet/bounty/skill Web corrections, not assume the parent accepted. Server capability/fingerprint/wallet and actual R01 adapter remain integration dependencies.
