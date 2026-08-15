# Juyiting E18 Temporary Dependency Security Exception

## Decision state

- Status: `accepted`
- Scope: CYF `web/` release candidate `4127e7af8fe5c5325d0715fbfc826937f48f41bb`
- Recorded: 2026-08-14
- Owner: CYF web maintainers
- Expiry: 2026-09-14
- Accepted by: E18 GPT-5.6 Sol High Release Guard on 2026-08-14
- Required follow-up: upgrade and independently verify the affected dependency chain before expiry; this exception must not be silently renewed.

## Audit result

`npm audit --omit=dev` reports 0 critical, 2 high and 1 moderate vulnerable packages:

| Package | Installed | Direct | Audit severity | Release-path assessment |
| --- | ---: | --- | --- | --- |
| `dompurify` | 3.4.11 | yes | moderate | The application calls default `DOMPurify.sanitize(marked(...))`; it does not configure `CUSTOM_ELEMENT_HANDLING`, `IN_PLACE`, hooks, or `afterSanitizeElements`, which are required by the reported bypass conditions. |
| `postcss` | 8.5.16 | transitive | high | Used by the trusted local Vite/build toolchain. This release does not process attacker-controlled CSS or `sourceMappingURL` input on the server or in a production runtime build service. |
| `nanoid` | 3.3.15 | transitive | high | Used through the build dependency graph. No application runtime path calls Nano ID custom generators with attacker-controlled zero/negative sizes. |

Verified source searches:

```text
src/components/juyiting/ChatPanel.vue
src/components/chat/ChatMessage.vue
```

contain the only application `DOMPurify` calls. Searches of `src/`, `tests/`, `scripts/`, Vite config and package metadata found no application import/call of `postcss` or `nanoid`, and no use of the affected DOMPurify options/hooks.

## Risk acceptance rationale

The advisories are real dependency debt, but their published trigger conditions are not exposed by the E18 frontend release path. Upgrading the dependency tree at this point would change the already frozen and fully reverified release candidate, requiring the complete functional, visual and performance gate set to be rerun. The bounded exception is therefore lower release risk than an unreviewed dependency upgrade immediately before deployment.

This is not a claim that the packages are generally safe. It is a time-limited acceptance for this exact commit and deployment path only.

## Compensating controls

1. Deploy only the exact clean commit through `/home/isp/bin/cyf_web_kit_release_pinned.sh` with `CYF_RELEASE_HEAD` pinned.
2. Do not add DOMPurify custom-element handling, in-place sanitization, or hooks while this exception is active.
3. Do not introduce a production service that compiles attacker-controlled CSS/source maps.
4. Do not expose Nano ID custom generator size parameters to untrusted input.
5. Keep CSP/input-validation and existing DOMPurify default sanitization behavior unchanged for this release.
6. Roll back immediately if production smoke finds unexpected script execution, resource substitution, or build artifact drift.

## Closure criteria

Close this exception by upgrading to non-vulnerable versions, reviewing lockfile changes, and rerunning at minimum:

- `npm audit --omit=dev`
- chat/Juyiting markdown rendering tests
- `npm run test:game`
- `npm run test`
- `npm run typecheck:game`
- `npm run build`
- the E14 performance freshness gate
- the V5 visual release sample if production assets or bundle behavior change
