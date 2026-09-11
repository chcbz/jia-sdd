#!/usr/bin/env python3
"""Validate saved JSON response bodies against the frozen OpenAPI contract.

Input is an array of {operationId, status, body} observations. This is an offline
shape check, not proof that an HTTP request ran, ACL passed, or headers are safe.
It never prints response bodies. Requires PyYAML and jsonschema >= 4.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys

import yaml
from jsonschema import Draft202012Validator


def require_local_refs(value):
    if isinstance(value, dict):
        if "$ref" in value and not value["$ref"].startswith("#/"):
            raise ValueError("Only local schema references are supported")
        for child in value.values():
            require_local_refs(child)
    elif isinstance(value, list):
        for child in value:
            require_local_refs(child)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("observations", type=Path)
    parser.add_argument("--contract", type=Path,
                        default=Path(__file__).resolve().parents[1] / "openapi.yaml")
    args = parser.parse_args()
    contract_bytes = args.contract.read_bytes()
    document = yaml.safe_load(contract_bytes)
    require_local_refs(document)
    operations = {}
    for path in document["paths"].values():
        for method, operation in path.items():
            if method not in {"get", "post", "put", "patch", "delete", "head", "options", "trace"}:
                continue
            name = operation["operationId"]
            if name in operations:
                raise ValueError("Duplicate operation ID")
            operations[name] = operation
    raw = args.observations.read_bytes()
    captures = json.loads(raw)
    if not isinstance(captures, list) or not captures:
        raise ValueError("A nonempty observation array is required")
    results = []
    for index, capture in enumerate(captures):
        result = {"index": index, "valid": False}
        if not isinstance(capture, dict) or set(capture) != {"operationId", "status", "body"}:
            result["error"] = "observation_fields"
        elif not isinstance(capture["operationId"], str) or capture["operationId"] not in operations:
            result["error"] = "unknown_operation"
        elif type(capture["status"]) is not int or str(capture["status"]) not in operations[capture["operationId"]]["responses"]:
            result["error"] = "undocumented_http_status"
        else:
            operation = operations[capture["operationId"]]
            response = operation["responses"][str(capture["status"]) ]
            media = response.get("content", {}).get("application/json")
            if media is None:
                result["error"] = "not_a_json_response"
            else:
                schema = dict(media["schema"], components=document["components"])
                Draft202012Validator.check_schema(schema)
                errors = list(Draft202012Validator(schema).iter_errors(capture["body"]))
                result.update(operationId=capture["operationId"], status=capture["status"],
                              valid=not errors, violations=[e.validator for e in errors])
        results.append(result)
    valid = all(r["valid"] for r in results)
    print(json.dumps({"contract_sha256": hashlib.sha256(contract_bytes).hexdigest(),
                      "observations_sha256": hashlib.sha256(raw).hexdigest(),
                      "valid": valid, "results": results,
                      "limit": "Offline JSON shape only; no live HTTP, header, authorization or release verdict."},
                     indent=2))
    return 0 if valid else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, KeyError, TypeError, yaml.YAMLError):
        print("Contract check could not read valid input/schema; response values omitted.", file=sys.stderr)
        sys.exit(2)
