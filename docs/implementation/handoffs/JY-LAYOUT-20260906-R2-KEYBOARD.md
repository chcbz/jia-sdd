# JY-LAYOUT keyboard regression — 2026-09-06

Independent Sol Godel exact94f75555/tree08b43439 SOURCE REJECT P0/P1/P2=0/1/0. Legacy no-has fallback and stale test findings closed, but full-height chat overrides live visual height and places composer below visible viewport on visualViewport-only keyboard shrink (physical landscape layout/root390, visual220).

Bounded correction: only chat overlay vertical bounds should follow live available Hall visual viewport, top anchored so bottom alignment cannot move the whole short dialog below visibility. Preserve no-keyboard edge-to-edge, explicit no-has class, normal other panels, source orientation/canvas/reader unchanged. No speculative native host bridge. Add matching focused contract coverage, retain full mode25/selected11 prior evidence as scoped only; real keyboard simulation viewport-only geometry handled by verifier.

Old worktree jy-layout-20260906 is running exact94f7555 build and immutable until verifier natural completion/decl restoration. New sole-Owner source worktree jy-layout-keyboard-20260906 starts exact94f7555. Do not mutate old build source or terminate verifier. New scoped commit will be fast-forward integrated only after old build source released; the old dist is superseded and cannot be deployed as corrected candidate. Final exact new source needs its own required production build and geometry checks.
