import json
import os
import shutil
import subprocess
import tempfile
import unittest

from ops.performance.inventory import canonical_sha256, main, reconcile, scan_source, _runtime_routes


COMMIT = "c" * 40
TREE = "d" * 40


def manifest(framework=None, management=None, profile="grey", commit=COMMIT, tree=TREE):
    if framework is None:
        framework = [{"method": "GET", "path": "/error", "handler": "error"}]
    if management is None:
        management = [{"method": "GET", "path": "/actuator/health", "handler": "health"}]
    return {
        "profile": profile,
        "api_commit": commit,
        "api_tree": tree,
        "framework_routes": framework,
        "management_routes": management,
    }


def actuator(records):
    return {
        "contexts": {
            "application": {
                "mappings": {
                    "dispatcherServlets": {"dispatcherServlet": records},
                    "servletFilters": [],
                    "servlets": {},
                },
                "parentId": None,
            }
        }
    }


def runtime(framework_records, management_records, profile="grey", commit=COMMIT, tree=TREE):
    payload = {
        "framework_mappings": actuator(framework_records),
        "management_mappings": actuator(management_records),
    }
    return {
        "profile": profile,
        "api_commit": commit,
        "api_tree": tree,
        "capture_content_sha256": canonical_sha256(payload),
        "payload": payload,
    }


def structured(methods, patterns, handler="Handler"):
    return {
        "handler": handler,
        "predicate": "ignored when Boot 4 structured details are present",
        "details": {
            "handlerMethod": {"className": "example.Handler", "name": "handle"},
            "requestMappingConditions": {
                "consumes": [],
                "headers": [],
                "methods": methods,
                "params": [],
                "patterns": patterns,
                "produces": [{"mediaType": "application/json", "negated": False}],
            },
        },
    }


class InventoryTest(unittest.TestCase):
    def setUp(self):
        self.roots = []

    def tearDown(self):
        for root in self.roots:
            shutil.rmtree(root, ignore_errors=True)

    def source(self, text, filename="DemoController.java"):
        root = tempfile.mkdtemp()
        self.roots.append(root)
        with open(os.path.join(root, filename), "w") as source_file:
            source_file.write(text)
        return root

    def test_arrays_and_comments(self):
        root = self.source(
            '''@RestController\n@RequestMapping(path={"/a", "/b"})\nclass DemoController {\n'''
            ''' // @GetMapping("/fake")\n'''
            ''' @RequestMapping(value={"/x", "/y"}, method={RequestMethod.PUT, RequestMethod.DELETE})\n'''
            ''' public String run() { return "// literal"; }\n}'''
        )
        routes, diagnostics, _ = scan_source(root)
        self.assertEqual([], [item for item in diagnostics if item["fatal"]])
        self.assertEqual(8, len(routes))
        self.assertIn(("PUT", "/a/x"), {(item["method"], item["path"]) for item in routes})

    def test_missing_method_is_any(self):
        root = self.source(
            '@RequestMapping("/root")\nclass DemoController { @RequestMapping("/x") public void x() {} }'
        )
        routes, diagnostics, _ = scan_source(root)
        self.assertFalse(diagnostics)
        self.assertEqual("ANY", routes[0]["method"])

    def test_nonliteral_and_path_value_alias_collision_fail_closed(self):
        root = self.source(
            '@RequestMapping(path="/root", value="/alias")\nclass DemoController { '
            '@GetMapping(PATH) public void x() {} }'
        )
        routes, diagnostics, _ = scan_source(root)
        self.assertTrue(any(item["code"] == "unsupported_mapping" for item in diagnostics))
        self.assertEqual([], routes)

    def test_inheritance_fails_closed(self):
        root = self.source(
            '@RequestMapping("/root")\nclass DemoController extends BaseController { '
            '@GetMapping("/x") public void x() {} }'
        )
        _routes, diagnostics, _ = scan_source(root)
        self.assertTrue(any(item["code"] == "unsupported_inheritance" for item in diagnostics))

    def test_custom_mapping_annotations_are_never_silent(self):
        for annotation in ("MyGetMapping", "GM"):
            root = self.source(
                '@RestController\nclass DemoController { @%s("/x") public void x() {} }' % annotation,
                filename=annotation + "Controller.java",
            )
            routes, diagnostics, _ = scan_source(root)
            self.assertEqual([], routes)
            self.assertTrue(any(item["code"] == "unknown_declaration_annotation" for item in diagnostics))

    def test_composed_annotation_definition_outside_controller_filename_is_detected(self):
        root = self.source(
            '@GetMapping("/x")\n@Target(ElementType.METHOD)\npublic @interface MyGetMapping {}',
            filename="MyGetMapping.java",
        )
        routes, diagnostics, files = scan_source(root)
        self.assertEqual([], routes)
        self.assertTrue(any(item["code"] == "unsupported_composed_mapping" for item in diagnostics))
        self.assertTrue(any(path.endswith("MyGetMapping.java") for path in files))

    def test_rest_controller_outside_controller_filename_is_scanned(self):
        root = self.source(
            '@RestController\n@RequestMapping("/odd")\nclass OddEndpoint { @GetMapping("/x") public void x() {} }',
            filename="OddEndpoint.java",
        )
        routes, diagnostics, _ = scan_source(root)
        self.assertFalse(diagnostics)
        self.assertIn(("GET", "/odd/x"), {(item["method"], item["path"]) for item in routes})

    def test_known_nonmapping_allowlist_does_not_hide_mapping(self):
        root = self.source(
            '@Deprecated\n@RestController\n@RequestMapping("/root")\nclass DemoController { '
            '@Override\n@GetMapping("/x") public void x() {} }'
        )
        routes, diagnostics, _ = scan_source(root)
        self.assertFalse(any(item["code"] == "unknown_declaration_annotation" for item in diagnostics))
        self.assertEqual([("GET", "/root/x")], [(item["method"], item["path"]) for item in routes])

    def test_boot4_plural_methods_patterns_expand_cartesian_product(self):
        routes = _runtime_routes(actuator([structured(["GET", "POST"], ["/a", "/b"])]))
        self.assertEqual(
            {("GET", "/a"), ("GET", "/b"), ("POST", "/a"), ("POST", "/b")},
            {(item["method"], item["path"]) for item in routes},
        )

    def test_direct_method_and_path_arrays_expand_without_stringification(self):
        routes = _runtime_routes([{"methods": ["PUT", "DELETE"], "paths": ["/a", "/b"]}])
        self.assertEqual(4, len(routes))
        with self.assertRaisesRegex(Exception, "entries must be non-empty strings"):
            _runtime_routes([{"methods": ["GET"], "paths": [["/not-string"]]}])

    def test_malformed_runtime_records_are_rejected_not_skipped(self):
        bad_records = [
            [{"handler": "missing route"}],
            [{"method": "GET", "path": "/ok"}, "bad"],
            [{"methods": ["BREW"], "paths": ["/coffee"]}],
            [{"method": "GET", "path": "relative"}],
            [{"method": "GET", "path": "/x", "mystery": 1}],
        ]
        for records in bad_records:
            with self.assertRaises(Exception):
                _runtime_routes(records)

    def test_empty_or_unknown_actuator_surface_is_rejected(self):
        with self.assertRaisesRegex(Exception, "zero routes"):
            _runtime_routes(actuator([]))
        bad = actuator([{"predicate": "{GET [/x]}"}])
        bad["contexts"]["application"]["mappings"]["unknownSection"] = []
        with self.assertRaisesRegex(Exception, "unknown sections"):
            _runtime_routes(bad)

    def test_forged_or_missing_canonical_capture_hash_rejected(self):
        static = [{"method": "GET", "path": "/x", "handler": "x"}]
        fw = [structured(["GET"], ["/x"]), structured(["GET"], ["/error"])]
        mgmt = [structured(["GET"], ["/actuator/health"])]
        for claimed in ("f" * 64, None, "not-a-hash"):
            capture = runtime(fw, mgmt)
            if claimed is None:
                capture.pop("capture_content_sha256")
            else:
                capture["capture_content_sha256"] = claimed
            result = reconcile(static, manifest(), capture, {"commit": COMMIT, "tree": TREE}, "grey")
            self.assertFalse(result["ok"])
            self.assertTrue(
                any(item["code"] in ("content_hash_missing", "content_hash_mismatch") for item in result["diagnostics"])
            )

    def test_canonical_payload_hash_is_format_independent_and_valid(self):
        static = [{"method": "GET", "path": "/x", "handler": "x"}]
        capture = runtime(
            [structured(["GET"], ["/x"]), structured(["GET"], ["/error"])],
            [structured(["GET"], ["/actuator/health"])],
        )
        reparsed = json.loads(json.dumps(capture, indent=4, sort_keys=False))
        result = reconcile(static, manifest(), reparsed, {"commit": COMMIT, "tree": TREE}, "grey")
        self.assertTrue(result["ok"], result["diagnostics"])

    def test_manifest_requires_exact_binding_and_nonempty_distinct_lists(self):
        static = [{"method": "GET", "path": "/x", "handler": "x"}]
        capture = runtime(
            [structured(["GET"], ["/x"]), structured(["GET"], ["/error"])],
            [structured(["GET"], ["/actuator/health"])],
        )
        invalid = [
            {"profile": "grey", "routes": []},
            manifest(framework=[], management=[]),
            manifest(commit="wrong"),
            manifest(framework=[{"method": "GET", "path": [["/bad"]]}]),
            dict(manifest(), mystery=[]),
        ]
        for declared in invalid:
            result = reconcile(static, declared, capture, {"commit": COMMIT, "tree": TREE}, "grey")
            self.assertFalse(result["ok"])
            self.assertTrue(any(item["code"] in ("binding_missing", "binding_mismatch", "manifest_shape") for item in result["diagnostics"]))

    def test_runtime_binding_and_nonempty_distinct_surfaces_required(self):
        static = [{"method": "GET", "path": "/x", "handler": "x"}]
        good_fw = [structured(["GET"], ["/x"]), structured(["GET"], ["/error"])]
        good_mgmt = [structured(["GET"], ["/actuator/health"])]
        captures = [
            runtime(good_fw, good_mgmt, profile="prod"),
            runtime(good_fw, good_mgmt, tree="wrong"),
            runtime([], good_mgmt),
            runtime(good_fw, []),
        ]
        for capture in captures:
            result = reconcile(static, manifest(), capture, {"commit": COMMIT, "tree": TREE}, "grey")
            self.assertFalse(result["ok"])

    def test_framework_and_management_surfaces_cannot_cross_cancel(self):
        static = [{"method": "GET", "path": "/x", "handler": "x"}]
        capture = runtime(
            [
                structured(["GET"], ["/x"]),
                structured(["GET"], ["/error"]),
                structured(["GET"], ["/actuator/health"]),
            ],
            [structured(["GET"], ["/management-other"])],
        )
        result = reconcile(static, manifest(), capture, {"commit": COMMIT, "tree": TREE}, "grey")
        self.assertFalse(result["ok"])
        messages = "\n".join(item["message"] for item in result["diagnostics"])
        self.assertIn("management declared route missing", messages)
        self.assertIn("framework runtime route not declared", messages)

    def test_scan_cli_rejects_unbound_empty_framework_manifest(self):
        root = self.source(
            '@RestController\n@RequestMapping("/root")\nclass DemoController { '
            '@GetMapping("/x") public void x() {} }'
        )
        subprocess.check_call(["git", "init", "-q", root])
        subprocess.check_call(["git", "-C", root, "add", "DemoController.java"])
        subprocess.check_call(
            ["git", "-C", root, "-c", "user.name=Inventory Test", "-c", "user.email=inventory@example.invalid", "commit", "-qm", "fixture"]
        )
        commit = subprocess.check_output(["git", "-C", root, "rev-parse", "HEAD"]).decode().strip()
        tree = subprocess.check_output(["git", "-C", root, "rev-parse", "HEAD^{tree}"]).decode().strip()
        fixture_dir = tempfile.mkdtemp()
        self.roots.append(fixture_dir)
        manifest_path = os.path.join(fixture_dir, "manifest.json")
        output_path = os.path.join(fixture_dir, "inventory.json")
        with open(manifest_path, "w") as output_file:
            json.dump({"profile": "grey", "routes": []}, output_file)
        rc = main(
            [
                "scan",
                "--source-root",
                root,
                "--profile",
                "grey",
                "--api-commit",
                commit,
                "--api-tree",
                tree,
                "--framework-manifest",
                manifest_path,
                "--output",
                output_path,
            ]
        )
        self.assertEqual(2, rc)
        with open(output_path) as input_file:
            result = json.load(input_file)
        self.assertFalse(result["ok"])
        self.assertTrue(any(item["code"] in ("binding_missing", "manifest_shape") for item in result["diagnostics"]))

    def test_json_media_is_not_stream_exemption(self):
        root = self.source(
            '@RequestMapping("/media/upload")\nclass DemoController { '
            '@PostMapping("/x") public void x() {} }'
        )
        routes, diagnostics, _ = scan_source(root)
        self.assertFalse(diagnostics)
        self.assertIn(("POST", "/media/upload/x"), {(item["method"], item["path"]) for item in routes})


if __name__ == "__main__":
    unittest.main()
