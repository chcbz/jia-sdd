#!/usr/bin/env python3
"""Offline, fail-closed Spring MVC inventory scanner and reconciler (Python 3.6+)."""
from __future__ import print_function

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys

MAPPING_ANN = {
    "GetMapping": "GET",
    "PostMapping": "POST",
    "PutMapping": "PUT",
    "DeleteMapping": "DELETE",
    "PatchMapping": "PATCH",
    "HeadMapping": "HEAD",
    "OptionsMapping": "OPTIONS",
}
METHODS = set(["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS", "TRACE"])

# Exact names only. Unknown annotations on relevant controller/type/method declarations
# are fatal because they may be mapping aliases or composed mappings.
KNOWN_NON_MAPPING_ANNOTATIONS = set(
    "AliasFor AllowSensitiveOutput Async Autowired Bean ConditionalOnBean ConditionalOnClass ConditionalOnExpression "
    "ConditionalOnMissingBean ConditionalOnMissingClass ConditionalOnProperty Configuration "
    "ConstructorBinding Controller ControllerAdvice CookieValue CrossOrigin Deprecated ExceptionHandler "
    "Documented Generated Inject InitBinder JsonCreator JsonIgnore JsonProperty Lazy ModelAttribute Nullable Operation "
    "Override Parameter PathVariable Retention Target PermitAll PreAuthorize Primary Profile Qualifier Repository RequestBody "
    "RequestHeader RequestParam RequestPart Resource ResponseBody ResponseStatus RestController "
    "RestControllerAdvice RegisteredOAuth2AuthorizedClient Scheduled Secured Service SessionAttributes SuppressWarnings SysPermission Tag Transactional Valid Validated Value "
    "VisibleForTesting AllArgsConstructor Builder Data EqualsAndHashCode Getter NoArgsConstructor NonNull "
    "RequiredArgsConstructor Setter Slf4j ToString".split()
)
KNOWN_MAPPING_NAMES = set(MAPPING_ANN) | set(["RequestMapping"])
KNOWN_RUNTIME_MAPPING_SECTIONS = set(["dispatcherServlets", "servletFilters", "servlets"])
HEX_SHA256 = re.compile(r"^[0-9a-f]{64}$")
GIT_OBJECT_ID = re.compile(r"^[0-9a-f]{40}$")


class InventoryError(Exception):
    pass


def _diag(code, message, file=None, line=None, fatal=True):
    d = {"code": code, "message": message, "fatal": bool(fatal)}
    if file:
        d["file"] = file
    if line:
        d["line"] = line
    return d


def _strip_comments(s):
    # A lexical comment stripper: strings and chars are retained; comment-like text in literals is not removed.
    out = []
    i = 0
    state = "code"
    while i < len(s):
        c = s[i]
        n = s[i + 1] if i + 1 < len(s) else ""
        if state == "code":
            if c == '"':
                state = "string"
                out.append(c)
            elif c == "'":
                state = "char"
                out.append(c)
            elif c == "/" and n == "/":
                out.extend("  ")
                i += 1
                state = "line"
            elif c == "/" and n == "*":
                out.extend("  ")
                i += 1
                state = "block"
            else:
                out.append(c)
        elif state == "line":
            if c == "\n":
                state = "code"
                out.append(c)
            else:
                out.append(" ")
        elif state == "block":
            if c == "*" and n == "/":
                out.extend("  ")
                i += 1
                state = "code"
            else:
                out.append("\n" if c == "\n" else " ")
        else:
            out.append(c)
            if c == "\\" and i + 1 < len(s):
                out.append(s[i + 1])
                i += 1
            elif (state == "string" and c == '"') or (state == "char" and c == "'"):
                state = "code"
        i += 1
    return "".join(out)


def _balanced(text, start):
    if start >= len(text) or text[start] != "(":
        return "", start
    depth = 0
    quote = None
    esc = False
    for i in range(start, len(text)):
        c = text[i]
        if quote:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == quote:
                quote = None
            continue
        if c in ('"', "'"):
            quote = c
        elif c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
            if depth == 0:
                return text[start + 1 : i], i + 1
    raise ValueError("unclosed annotation arguments")


def _split_top(s, sep=","):
    parts = []
    start = 0
    depth = 0
    quote = None
    esc = False
    for i, c in enumerate(s):
        if quote:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == quote:
                quote = None
        elif c in ('"', "'"):
            quote = c
        elif c in "({[":
            depth += 1
        elif c in ")}]":
            depth -= 1
        elif c == sep and depth == 0:
            parts.append(s[start:i].strip())
            start = i + 1
    parts.append(s[start:].strip())
    return [p for p in parts if p]


def _strings(expr):
    vals = []
    for m in re.finditer(r'"((?:\\.|[^"\\])*)"', expr):
        vals.append(bytes(m.group(1), "utf8").decode("unicode_escape"))
    residue = re.sub(r'"(?:\\.|[^"\\])*"', "", expr).strip()
    if residue and not re.match(r"^(?:\{\s*\})?$", residue):
        if not re.match(r"^\{\s*(?:,?\s*)\}$", residue):
            return None
    return vals


def _arg_map(args):
    result = {}
    for part in _split_top(args):
        if "=" in part:
            k, v = part.split("=", 1)
            result[k.strip()] = v.strip()
        else:
            result.setdefault("value", part.strip())
    return result


def _paths(args):
    a = _arg_map(args)
    present = [key for key in ("path", "value") if key in a]
    if len(present) > 1:
        return None
    expr = a.get(present[0], '""') if present else '""'
    return _strings(expr)


def _methods(args, annotation):
    if annotation in MAPPING_ANN:
        return [MAPPING_ANN[annotation]]
    a = _arg_map(args)
    if "method" not in a:
        return ["ANY"]
    expr = a["method"]
    vals = re.findall(r"RequestMethod\.([A-Z]+)", expr)
    if not vals:
        vals = _strings(expr) or []
    if not vals or any(v not in METHODS for v in vals):
        return None
    return vals


def _join(base, path):
    if not base:
        base = "/"
    if not path:
        path = "/"
    x = base.rstrip("/") + "/" + path.lstrip("/")
    x = re.sub(r"/+", "/", x)
    return x if x.startswith("/") else "/" + x


def _annotation_records(clean):
    found = []
    pattern = re.compile(r"@(?!interface\b)([A-Za-z_$][\w$]*(?:\.[A-Za-z_$][\w$]*)*)")
    i = 0
    while True:
        m = pattern.search(clean, i)
        if not m:
            break
        end = m.end()
        args = ""
        j = end
        while j < len(clean) and clean[j].isspace():
            j += 1
        if j < len(clean) and clean[j] == "(":
            try:
                args, j = _balanced(clean, j)
            except ValueError as exc:
                found.append((None, None, clean.count("\n", 0, m.start()) + 1, str(exc), m.start(), end))
                i = end
                continue
        found.append((m.group(1).split(".")[-1], args, clean.count("\n", 0, m.start()) + 1, j, m.start(), end))
        i = j
    return found


_TYPE_DECL = re.compile(r"@interface\s+[A-Za-z_$][\w$]*|\b(?:class|interface|enum|record)\s+[A-Za-z_$][\w$]*")
_METHOD_DECL = re.compile(
    r"\b(?:public|protected|private|static|final|synchronized|native|abstract|default|strictfp|\s)+"
    r"[\w$<>\[\],.? ]+\s+([A-Za-z_$][\w$]*)\s*\([^;{}]*\)\s*(?:throws[^\{;]+)?[\{;]"
)


def _annotation_target(clean, annotation_end):
    candidates = []
    tm = _TYPE_DECL.search(clean, annotation_end)
    mm = _METHOD_DECL.search(clean, annotation_end)
    if tm:
        candidates.append((tm.start(), "annotation" if clean.startswith("@interface", tm.start()) else "type", tm))
    if mm:
        candidates.append((mm.start(), "method", mm))
    if not candidates:
        return None, None
    start, kind, match = min(candidates, key=lambda item: item[0])
    gap = clean[annotation_end:start]
    if any(ch in gap for ch in ";{}"):
        return None, None
    return kind, match


def _looks_path_like(args):
    vals = _strings(args)
    return bool(vals and any(v.startswith("/") for v in vals))


def _is_relevant_source(filename, clean, annotations):
    if filename.endswith("Controller.java"):
        return True
    for name, args, _line, end, _start, _raw_end in annotations:
        if name is None:
            continue
        kind, _match = _annotation_target(clean, end)
        if name in KNOWN_MAPPING_NAMES or (name in ("Controller", "RestController") and kind == "type"):
            return True
        if kind in ("type", "method", "annotation") and name not in KNOWN_NON_MAPPING_ANNOTATIONS:
            if name.endswith("Mapping") or _looks_path_like(args):
                return True
    return False


def scan_source(root):
    root = os.path.abspath(root)
    if not os.path.isdir(root):
        raise InventoryError("source root does not exist: %s" % root)
    records = []
    diagnostics = []
    files = []
    sources = []
    for dp, dns, fns in os.walk(root):
        dns[:] = [d for d in sorted(dns) if d not in (".git", "build", ".gradle")]
        for fn in sorted(fns):
            if fn.endswith(".java"):
                candidate = os.path.join(dp, fn)
                rel = "/" + os.path.relpath(candidate, root).replace(os.sep, "/")
                if not any(marker in rel for marker in ("/src/test/", "/src/testFixtures/", "/src/integrationTest/")):
                    files.append(candidate)
    for filename in sorted(files):
        with open(filename, "r", encoding="utf-8") as source_file:
            clean = _strip_comments(source_file.read())
        annotations = _annotation_records(clean)
        if _is_relevant_source(filename, clean, annotations):
            sources.append((filename, clean, annotations))

    for filename, clean, annotations in sources:
        rel = os.path.relpath(filename, root).replace(os.sep, "/")
        class_prefixes = [""]
        for name, args, line, end, _start, _raw_end in annotations:
            if name is None:
                diagnostics.append(_diag("unresolved_annotation", end, rel, line))
                continue
            kind, decl = _annotation_target(clean, end)
            if kind not in ("type", "method", "annotation"):
                continue
            if name not in KNOWN_MAPPING_NAMES and name not in KNOWN_NON_MAPPING_ANNOTATIONS:
                diagnostics.append(
                    _diag(
                        "unknown_declaration_annotation",
                        "unknown annotation @%s may be an unsupported composed/aliased mapping" % name,
                        rel,
                        line,
                    )
                )
                continue
            if name not in KNOWN_MAPPING_NAMES:
                continue
            if kind == "annotation":
                diagnostics.append(
                    _diag(
                        "unsupported_composed_mapping",
                        "mapping annotation composes a custom annotation; aliases are not inferred",
                        rel,
                        line,
                    )
                )
                continue
            try:
                ps = _paths(args)
                ms = _methods(args, name)
            except Exception as exc:
                ps = ms = None
                diagnostics.append(_diag("unsupported_mapping", str(exc), rel, line))
            if ps is None or ms is None or not ps:
                diagnostics.append(
                    _diag(
                        "unsupported_mapping",
                        "mapping requires exactly one path/value alias with literal path(s) and supported method(s)",
                        rel,
                        line,
                    )
                )
                continue
            if kind == "type":
                class_prefixes = ps
                if len(ps) > 1:
                    diagnostics.append(
                        _diag("class_path_array", "class mapping path array expanded as a Cartesian product", rel, line, False)
                    )
                header = decl.group(0)
                tail = clean[decl.start() : clean.find("{", decl.start()) + 1]
                if " extends " in " " + tail or " implements " in " " + tail:
                    diagnostics.append(
                        _diag("unsupported_inheritance", "inheritance mappings are not inferred; provide explicit manifest", rel, line)
                    )
            else:
                if not class_prefixes:
                    diagnostics.append(
                        _diag("unresolved_class_mapping", "method mapping has no resolvable class path", rel, line)
                    )
                    continue
                method_name = decl.group(1)
                for prefix in class_prefixes:
                    for path in ps:
                        for verb in ms:
                            records.append(
                                {
                                    "kind": "controller",
                                    "method": verb,
                                    "path": _join(prefix, path),
                                    "handler": rel + ":" + method_name,
                                    "source": rel,
                                    "line": line,
                                }
                            )
    records.sort(key=lambda r: (r["method"], r["path"], r["handler"]))
    if not records:
        diagnostics.append(_diag("static_surface_empty", "no supported controller routes were enumerated"))
    return records, diagnostics, files


def sha256_files(root, files):
    h = hashlib.sha256()
    for filename in sorted(files):
        rel = os.path.relpath(filename, root).replace(os.sep, "/")
        with open(filename, "rb") as source_file:
            content = source_file.read()
        h.update(rel.encode("utf-8"))
        h.update(b"\0")
        h.update(content)
    return h.hexdigest()




def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as source_file:
        while True:
            chunk = source_file.read(1024 * 1024)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()

def canonical_sha256(value):
    try:
        encoded = json.dumps(
            value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise InventoryError("payload is not canonical JSON: %s" % exc)
    return hashlib.sha256(encoded).hexdigest()


def git_binding(root):
    def run(*args):
        try:
            return subprocess.check_output(
                ["git", "-C", root] + list(args), stderr=subprocess.STDOUT
            ).decode().strip()
        except Exception:
            return None

    commit = run("rev-parse", "HEAD")
    tree = run("rev-parse", "HEAD^{tree}")
    dirty = bool(run("status", "--porcelain", "--untracked-files=all"))
    return {"commit": commit, "tree": tree, "dirty": dirty}


def load_json(path):
    with open(path, encoding="utf-8") as source_file:
        return json.load(source_file)


def _string_list(value, label, allow_empty=False):
    if isinstance(value, str):
        values = [value]
    elif isinstance(value, list):
        values = value
    else:
        raise InventoryError("%s must be a string or string array" % label)
    if not values and not allow_empty:
        raise InventoryError("%s must be non-empty" % label)
    if any(not isinstance(item, str) or not item for item in values):
        raise InventoryError("%s entries must be non-empty strings" % label)
    return values


def _expand_route_record(record, kind, label, boot_conditions=False):
    if not isinstance(record, dict):
        raise InventoryError("%s must be an object" % label)
    handler = record.get("handler", "")
    if not isinstance(handler, str):
        raise InventoryError("%s handler must be a string" % label)
    if boot_conditions:
        unknown = set(record) - set(["methods", "patterns", "consumes", "headers", "params", "produces", "handler"])
        if unknown:
            raise InventoryError("%s has unknown requestMappingConditions fields: %s" % (label, sorted(unknown)))
        if "methods" not in record or "patterns" not in record:
            raise InventoryError("%s requires plural methods and patterns" % label)
        methods = _string_list(record["methods"], label + ".methods", allow_empty=True) or ["ANY"]
        paths = _string_list(record["patterns"], label + ".patterns")
    else:
        method_keys = [key for key in ("method", "methods") if key in record]
        path_keys = [key for key in ("path", "paths", "pattern", "patterns") if key in record]
        allowed = set(method_keys + path_keys + ["handler"])
        unknown = set(record) - allowed
        if unknown:
            raise InventoryError("%s has unknown route fields: %s" % (label, sorted(unknown)))
        if len(method_keys) != 1 or len(path_keys) != 1:
            raise InventoryError("%s requires exactly one method(s) field and one path/pattern(s) field" % label)
        methods = _string_list(record[method_keys[0]], label + "." + method_keys[0])
        paths = _string_list(record[path_keys[0]], label + "." + path_keys[0])
    methods = [method.upper() for method in methods]
    if any(method not in METHODS and method != "ANY" for method in methods):
        raise InventoryError("%s contains an unsupported HTTP method" % label)
    if any(not path.startswith("/") for path in paths):
        raise InventoryError("%s paths must be absolute normalized paths" % label)
    return [
        {"kind": kind, "method": method, "path": path, "handler": handler}
        for method in methods
        for path in paths
    ]


def _direct_route_list(value, kind, label):
    if not isinstance(value, list) or not value:
        raise InventoryError("%s must be a non-empty route array" % label)
    routes = []
    for index, record in enumerate(value):
        routes.extend(_expand_route_record(record, kind, "%s[%d]" % (label, index)))
    keys = [(route["method"], route["path"], route["handler"]) for route in routes]
    if len(keys) != len(set(keys)):
        raise InventoryError("%s contains duplicate route records" % label)
    return sorted(routes, key=lambda route: (route["method"], route["path"], route["handler"]))


def _predicate_routes(predicate, handler, kind, label):
    if not isinstance(predicate, str):
        raise InventoryError("%s predicate must be a string" % label)
    match = re.match(
        r"^\{\s*(?:(GET|POST|PUT|DELETE|PATCH|HEAD|OPTIONS|TRACE)\s+)?\[([^\]]+)\](?:,.*)?\}\s*$",
        predicate,
    )
    if not match:
        raise InventoryError("%s predicate is unsupported; structured conditions are required for ambiguous predicates" % label)
    method = match.group(1) or "ANY"
    raw_paths = re.split(r"\s*\|\|\s*|\s*,\s*", match.group(2).strip())
    return _expand_route_record(
        {"methods": [method], "paths": raw_paths, "handler": handler}, kind, label + ".predicate"
    )


def _boot_mapping_record(record, kind, label):
    if not isinstance(record, dict):
        raise InventoryError("%s must be an object" % label)
    allowed = set(["handler", "predicate", "details"])
    unknown = set(record) - allowed
    if unknown:
        raise InventoryError("%s has unknown mapping fields: %s" % (label, sorted(unknown)))
    handler = record.get("handler", "")
    if not isinstance(handler, str):
        raise InventoryError("%s handler must be a string" % label)
    details = record.get("details")
    if details is not None:
        if not isinstance(details, dict):
            raise InventoryError("%s.details must be an object" % label)
        unknown_details = set(details) - set(["handlerMethod", "requestMappingConditions"])
        if unknown_details:
            raise InventoryError("%s.details has unknown fields: %s" % (label, sorted(unknown_details)))
        conditions = details.get("requestMappingConditions")
        if conditions is not None:
            if not isinstance(conditions, dict):
                raise InventoryError("%s.details.requestMappingConditions must be an object" % label)
            enriched = dict(conditions)
            enriched["handler"] = handler
            return _expand_route_record(
                enriched, kind, label + ".details.requestMappingConditions", boot_conditions=True
            )
    if "predicate" in record:
        return _predicate_routes(record["predicate"], handler, kind, label)
    raise InventoryError("%s has neither structured requestMappingConditions nor a supported predicate" % label)


def _boot_routes(value, kind, label):
    if isinstance(value, list):
        return _direct_route_list(value, kind, label)
    if not isinstance(value, dict):
        raise InventoryError("%s must be an actuator mappings object or route array" % label)
    if set(value) != set(["contexts"]):
        raise InventoryError("%s actuator root must contain only contexts" % label)
    contexts = value.get("contexts")
    if not isinstance(contexts, dict) or not contexts:
        raise InventoryError("%s.contexts must be a non-empty object" % label)
    routes = []
    for context_name in sorted(contexts):
        context = contexts[context_name]
        context_label = "%s.contexts.%s" % (label, context_name)
        if not isinstance(context, dict):
            raise InventoryError("%s must be an object" % context_label)
        unknown_context = set(context) - set(["mappings", "parentId"])
        if unknown_context:
            raise InventoryError("%s has unknown fields: %s" % (context_label, sorted(unknown_context)))
        mappings = context.get("mappings")
        if not isinstance(mappings, dict):
            raise InventoryError("%s.mappings must be an object" % context_label)
        unknown_sections = set(mappings) - KNOWN_RUNTIME_MAPPING_SECTIONS
        if unknown_sections:
            raise InventoryError("%s.mappings has unknown sections: %s" % (context_label, sorted(unknown_sections)))
        dispatchers = mappings.get("dispatcherServlets")
        if not isinstance(dispatchers, dict) or not dispatchers:
            raise InventoryError("%s.mappings.dispatcherServlets must be a non-empty object" % context_label)
        for servlet_name in sorted(dispatchers):
            records = dispatchers[servlet_name]
            servlet_label = "%s.mappings.dispatcherServlets.%s" % (context_label, servlet_name)
            if not isinstance(records, list):
                raise InventoryError("%s must be an array" % servlet_label)
            for index, record in enumerate(records):
                routes.extend(_boot_mapping_record(record, kind, "%s[%d]" % (servlet_label, index)))
        for ignored in ("servletFilters", "servlets"):
            if ignored in mappings and not isinstance(mappings[ignored], (list, dict)):
                raise InventoryError("%s.mappings.%s has an invalid known non-route shape" % (context_label, ignored))
    if not routes:
        raise InventoryError("%s enumerated zero routes" % label)
    keys = [(route["method"], route["path"], route["handler"]) for route in routes]
    if len(keys) != len(set(keys)):
        raise InventoryError("%s contains duplicate runtime mapping records" % label)
    return sorted(routes, key=lambda route: (route["method"], route["path"], route["handler"]))


def _runtime_routes(obj, kind="runtime"):
    """Strict parser retained as a small public seam for unit tests."""
    return _boot_routes(obj, kind, kind)


def _keys(routes):
    return set((route["method"], route["path"]) for route in routes)


def _binding_diagnostics(envelope, expected, profile, label):
    diagnostics = []
    if not isinstance(envelope, dict):
        return [_diag("invalid_%s" % label, "%s must be an object" % label)]
    for key in ("profile", "api_commit", "api_tree"):
        value = envelope.get(key)
        if not isinstance(value, str) or not value:
            diagnostics.append(_diag("binding_missing", "%s requires non-empty %s" % (label, key)))
        elif key in ("api_commit", "api_tree") and not GIT_OBJECT_ID.match(value):
            diagnostics.append(_diag("binding_invalid", "%s %s must be a full lowercase Git object ID" % (label, key)))
    if envelope.get("profile") != profile:
        diagnostics.append(_diag("profile_mismatch", "%s profile does not match requested profile" % label))
    if not expected.get("commit") or envelope.get("api_commit") != expected.get("commit"):
        diagnostics.append(_diag("binding_mismatch", "%s API commit is missing or mismatched" % label))
    if not expected.get("tree") or envelope.get("api_tree") != expected.get("tree"):
        diagnostics.append(_diag("binding_mismatch", "%s API tree is missing or mismatched" % label))
    return diagnostics


def _declared_surfaces(manifest, expected, profile):
    diagnostics = _binding_diagnostics(manifest, expected, profile, "framework_manifest")
    framework = []
    management = []
    if isinstance(manifest, dict):
        unknown = set(manifest) - set(["profile", "api_commit", "api_tree", "framework_routes", "management_routes"])
        if unknown:
            diagnostics.append(
                _diag("manifest_shape", "framework manifest has unknown fields: %s" % sorted(unknown))
            )
        for key, kind in (("framework_routes", "framework"), ("management_routes", "management")):
            try:
                parsed = _direct_route_list(manifest.get(key), kind, "framework_manifest.%s" % key)
                if kind == "framework":
                    framework = parsed
                else:
                    management = parsed
            except InventoryError as exc:
                diagnostics.append(_diag("manifest_shape", str(exc)))
    return framework, management, diagnostics


def _runtime_surfaces(runtime, expected, profile):
    diagnostics = _binding_diagnostics(runtime, expected, profile, "runtime_capture")
    framework = []
    management = []
    if not isinstance(runtime, dict):
        return framework, management, diagnostics
    allowed = set(["profile", "api_commit", "api_tree", "capture_content_sha256", "payload"])
    unknown = set(runtime) - allowed
    if unknown:
        diagnostics.append(_diag("runtime_shape", "runtime capture has unknown envelope fields: %s" % sorted(unknown)))
    claimed = runtime.get("capture_content_sha256")
    if not isinstance(claimed, str) or not HEX_SHA256.match(claimed):
        diagnostics.append(_diag("content_hash_missing", "runtime capture requires a lowercase canonical SHA-256"))
    payload = runtime.get("payload")
    if not isinstance(payload, dict):
        diagnostics.append(_diag("runtime_shape", "runtime capture payload must be an object"))
        return framework, management, diagnostics
    if set(payload) != set(["framework_mappings", "management_mappings"]):
        diagnostics.append(
            _diag(
                "runtime_shape",
                "runtime payload must contain exactly framework_mappings and management_mappings",
            )
        )
    try:
        actual_hash = canonical_sha256(payload)
        if claimed != actual_hash:
            diagnostics.append(_diag("content_hash_mismatch", "runtime canonical payload SHA-256 mismatch"))
    except InventoryError as exc:
        diagnostics.append(_diag("runtime_shape", str(exc)))
    for key, kind in (("framework_mappings", "runtime_framework"), ("management_mappings", "runtime_management")):
        try:
            parsed = _boot_routes(payload.get(key), kind, "runtime.payload.%s" % key)
            if kind == "runtime_framework":
                framework = parsed
            else:
                management = parsed
        except InventoryError as exc:
            diagnostics.append(_diag("runtime_shape", str(exc)))
    return framework, management, diagnostics


def validate_registry(registry, routes):
    """Validate only the documented normalized JSON shape; this is not YAML parsing."""
    diagnostics = []
    if not isinstance(registry, dict) or not isinstance(registry.get("routes"), list):
        return [_diag("registry_shape", "normalized registry JSON must contain a routes array")]
    actual = _keys(routes)
    declared = set()
    for item in registry["routes"]:
        if not isinstance(item, dict) or not isinstance(item.get("method"), str) or not isinstance(item.get("path"), str):
            diagnostics.append(_diag("registry_shape", "each registry route requires string method and path"))
            continue
        method = item["method"].upper()
        path = item["path"]
        if "*" in path or "{*" in path:
            diagnostics.append(_diag("registry_wildcard", "wildcard registry routes are forbidden: %s %s" % (method, path)))
        declared.add((method, path))
    for key in sorted(actual - declared):
        diagnostics.append(_diag("registry_missing", "route missing from normalized registry: %s %s" % key))
    for key in sorted(declared - actual):
        diagnostics.append(_diag("registry_unknown", "normalized registry contains unknown route: %s %s" % key))
    return diagnostics


def reconcile(static, manifest, runtime, expected, profile, inventory_diagnostics=None):
    diagnostics = list(inventory_diagnostics or [])
    if not isinstance(static, list) or not static:
        diagnostics.append(_diag("static_surface_empty", "inventory requires a non-empty static controller route list"))
        static = []
    else:
        try:
            # Generated static records have additional source metadata; validate the route-bearing fields strictly.
            normalized_static = []
            for index, route in enumerate(static):
                if not isinstance(route, dict):
                    raise InventoryError("static[%d] must be an object" % index)
                normalized_static.extend(
                    _expand_route_record(
                        {"method": route.get("method"), "path": route.get("path"), "handler": route.get("handler", "")},
                        "controller",
                        "static[%d]" % index,
                    )
                )
            static = normalized_static
        except InventoryError as exc:
            diagnostics.append(_diag("static_shape", str(exc)))
            static = []
    framework, management, manifest_diags = _declared_surfaces(manifest, expected, profile)
    runtime_framework, runtime_management, runtime_diags = _runtime_surfaces(runtime, expected, profile)
    diagnostics.extend(manifest_diags)
    diagnostics.extend(runtime_diags)

    declared_framework = static + framework
    declared_keys = [(route["method"], route["path"]) for route in declared_framework + management]
    if len(declared_keys) != len(set(declared_keys)):
        diagnostics.append(_diag("declared_duplicate", "declared controller/framework/management surfaces overlap"))

    comparisons = (
        (declared_framework, runtime_framework, "framework"),
        (management, runtime_management, "management"),
    )
    for declared, actual, surface in comparisons:
        declared_set = _keys(declared)
        actual_set = _keys(actual)
        for method, path in sorted(declared_set - actual_set):
            diagnostics.append(
                _diag("runtime_missing", "%s declared route missing from runtime: %s %s" % (surface, method, path))
            )
        for method, path in sorted(actual_set - declared_set):
            diagnostics.append(
                _diag("runtime_unknown", "%s runtime route not declared: %s %s" % (surface, method, path))
            )
    return {
        "static": static,
        "framework": framework,
        "management": management,
        "runtime_framework": runtime_framework,
        "runtime_management": runtime_management,
        "diagnostics": diagnostics,
        "ok": not any(item.get("fatal", True) for item in diagnostics),
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description="Offline Spring MVC inventory scanner/reconciler")
    sub = parser.add_subparsers(dest="command")
    scan = sub.add_parser("scan")
    scan.add_argument("--source-root", required=True)
    scan.add_argument("--profile", required=True)
    scan.add_argument("--api-commit", required=True)
    scan.add_argument("--api-tree", required=True)
    scan.add_argument("--framework-manifest", required=True)
    scan.add_argument("--registry-json")
    scan.add_argument("--output", required=True)
    rec = sub.add_parser("reconcile")
    rec.add_argument("--inventory", required=True)
    rec.add_argument("--runtime", required=True)
    rec.add_argument("--profile", required=True)
    rec.add_argument("--runtime-sha256")
    args = parser.parse_args(argv)
    try:
        if args.command == "scan":
            routes, diagnostics, files = scan_source(args.source_root)
            binding = git_binding(os.path.abspath(args.source_root))
            expected = {"commit": args.api_commit, "tree": args.api_tree}
            if not binding["commit"] or not binding["tree"]:
                diagnostics.append(_diag("source_binding_missing", "source root must be an exact git checkout"))
            if binding["commit"] != args.api_commit:
                diagnostics.append(_diag("source_binding_mismatch", "source HEAD does not match --api-commit"))
            if binding["tree"] != args.api_tree:
                diagnostics.append(_diag("source_binding_mismatch", "source tree does not match --api-tree"))
            if binding["dirty"]:
                diagnostics.append(_diag("source_dirty", "source checkout is dirty"))
            manifest = load_json(args.framework_manifest)
            _framework, _management, manifest_diags = _declared_surfaces(manifest, expected, args.profile)
            diagnostics.extend(manifest_diags)
            if args.registry_json:
                diagnostics.extend(validate_registry(load_json(args.registry_json), routes))
            result = {
                "schema_version": 2,
                "profile": args.profile,
                "source": {
                    "root": os.path.abspath(args.source_root),
                    "api_commit": binding["commit"],
                    "api_tree": binding["tree"],
                    "dirty": binding["dirty"],
                    "java_content_sha256": sha256_files(args.source_root, files),
                    "framework_manifest_sha256": sha256_file(args.framework_manifest),
                },
                "routes": routes,
                "framework_manifest": manifest,
                "diagnostics": diagnostics,
                "ok": not any(item.get("fatal", True) for item in diagnostics),
            }
            with open(args.output, "w", encoding="utf-8") as output_file:
                json.dump(result, output_file, sort_keys=True, indent=2)
                output_file.write("\n")
            return 0 if result["ok"] else 2
        if args.command == "reconcile":
            inventory = load_json(args.inventory)
            runtime = load_json(args.runtime)
            if inventory.get("profile") != args.profile:
                raise InventoryError("inventory profile mismatch")
            source = inventory.get("source", {})
            expected = {"commit": source.get("api_commit"), "tree": source.get("api_tree")}
            result = reconcile(
                inventory.get("routes"),
                inventory.get("framework_manifest"),
                runtime,
                expected,
                args.profile,
                inventory.get("diagnostics"),
            )
            with open(args.runtime, "rb") as runtime_file:
                runtime_hash = hashlib.sha256(runtime_file.read()).hexdigest()
            result["runtime_file_sha256"] = runtime_hash
            if args.runtime_sha256 and runtime_hash != args.runtime_sha256:
                result["diagnostics"].append(_diag("file_hash_mismatch", "runtime JSON file SHA-256 mismatch"))
                result["ok"] = False
            print(json.dumps(result, sort_keys=True, indent=2))
            return 0 if result["ok"] else 2
        parser.error("a command is required")
    except (OSError, ValueError, InventoryError, json.JSONDecodeError) as exc:
        print("inventory: ERROR: %s" % exc, file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
