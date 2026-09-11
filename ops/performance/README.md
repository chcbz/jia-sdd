# PERF-01 offline inventory

`inventory.py` is a dependency-free Python 3.6+ offline scanner/reconciler. It never starts the API or contacts a runtime.

## Commands

```sh
python3 ops/performance/inventory.py scan \
  --source-root /path/to/api \
  --profile grey --api-commit SHA --api-tree TREE \
  --framework-manifest framework-grey.json --output inventory-grey.json
python3 ops/performance/inventory.py reconcile \
  --inventory inventory-grey.json --runtime runtime-grey.json --profile grey
```

The scanner supports only literal `@RequestMapping` and Spring's verb mappings, literal `path` **or** `value`, literal string/string-array paths, and `RequestMethod` arrays. A mapping without a method is `ANY`. It scans production Java sources (excluding standard test-source roots) so controllers not named `*Controller.java` and custom annotation declarations cannot disappear solely because of filenames. Unknown annotations on relevant type/method declarations, custom composed mappings, aliases, inheritance, conditional expressions, and unsupported grammar are fatal diagnostics; they are never inferred.

The explicit non-mapping annotation allowlist is `KNOWN_NON_MAPPING_ANNOTATIONS` in `inventory.py`. Extending it is a source-reviewed change: an unrecognized annotation may be a composed route mapping and therefore fails closed.

## Declared surfaces

The framework manifest is strict JSON bound to the exact profile/API commit/tree. Both route arrays are mandatory, non-empty, well formed, and independently reconciled:

```json
{
  "profile": "grey",
  "api_commit": "...",
  "api_tree": "...",
  "framework_routes": [{"method": "GET", "path": "/error", "handler": "error"}],
  "management_routes": [{"method": "GET", "path": "/actuator/health", "handler": "health"}]
}
```

Legacy `routes`/`mappings`, empty arrays, unknown fields, malformed records, dirty source checkouts, and missing/mismatched bindings are nonzero. Static/controller, framework, and management lists remain separate in output.

## Trusted runtime envelope

A raw actuator export is not runtime evidence. The capture owner must provide an externally trusted envelope:

```json
{
  "profile": "grey",
  "api_commit": "...",
  "api_tree": "...",
  "capture_content_sha256": "lowercase SHA-256 of canonical payload JSON",
  "payload": {
    "framework_mappings": {"contexts": {}},
    "management_mappings": {"contexts": {}}
  }
}
```

The hash is mandatory and verified over UTF-8 JSON serialized with sorted keys and compact separators. Both payload surfaces must enumerate at least one route. Direct strict route arrays and Actuator mappings are supported. Spring Boot 4 `details.requestMappingConditions.methods` plus `patterns` are expanded as a Cartesian product; malformed methods, paths, records, sections, or unknown shapes are rejected rather than skipped. Application/framework and management surfaces are compared independently, so moving a route between lists cannot conceal a mismatch.

An optional CLI `--runtime-sha256` checks the transport file bytes separately from the mandatory canonical payload hash. This slice provides no live capture, no YAML parser, and no claim that any real grey/prod runtime has passed reconciliation.
