# PERF-01 offline inventory

`inventory.py` is a dependency-free Python 3.6+ offline scanner. It never starts the API or contacts a runtime.

## Commands

```sh
python3 ops/performance/inventory.py scan \
  --source-root /path/to/api \
  --profile grey --api-commit SHA --api-tree TREE \
  --framework-manifest framework-grey.json --output inventory-grey.json
python3 ops/performance/inventory.py reconcile \
  --inventory inventory-grey.json --runtime actuator-mappings-grey.json --profile grey
```

The scanner supports literal `@RequestMapping` and composed `@GetMapping`/`@PostMapping`/`@PutMapping`/`@DeleteMapping`/`@PatchMapping`/`@HeadMapping`/`@OptionsMapping`, literal string or string-array paths, and `RequestMethod` arrays. A mapping without `method` is represented as `ANY`, not guessed into HTTP verbs. Inheritance, conditional Java expressions, aliases, custom composed annotations, non-literal expressions, and ambiguous class-path arrays are explicit fatal diagnostics; callers must supply those routes in the framework manifest. Comments are lexically removed without interpreting arbitrary Java.

The framework manifest is JSON and is a separate declared fact. It may contain `profile`, `api_commit`, `api_tree`, and `routes`/`mappings` records. The runtime input is exported actuator mappings JSON; both directions are compared by method/path. Missing, unknown, profile/binding mismatches, dirty source checkouts, and unsupported mappings return nonzero. Static and runtime lists remain separate in output.

Source binding includes the current git commit/tree, a deterministic SHA-256 over sorted Java source paths and bytes, and a dirty-check. This v1 does not claim to parse the repository's YAML registry: provide a normalized JSON registry in a later validation step, or use a documented narrow parser before making registry-validity claims.

## Trusted runtime envelope

A raw actuator export is intentionally **not** accepted as runtime evidence. The capture owner must wrap it with an externally trusted envelope containing non-empty `profile`, `api_commit`, `api_tree`, and `capture_content_sha256`, plus the export under `mappings` (the export itself may use Spring's `contexts`/`predicate` shape). The framework manifest likewise requires `profile`, `api_commit`, and `api_tree`. Missing or mismatched bindings are nonzero; a framework manifest never suppresses unresolved/unsupported controller diagnostics. This slice provides no live capture and does not certify runtime equality without that envelope.
