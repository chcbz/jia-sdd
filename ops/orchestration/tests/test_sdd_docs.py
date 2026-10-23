import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location('sdd_docs', Path(__file__).resolve().parents[1] / 'sdd_docs.py')
D = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(D)


class DocumentNavigationTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix='cyf-sdd-docs-')
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.put('docs/sdd-document-map.json', json.dumps({'removed': {}, 'feature_dispositions': {}}))
        self.folder = self.root / 'specs/example'
        for name in D.REQUIRED:
            self.put('specs/example/' + name, '# Example\n' if name.endswith('.md') else
                     'feature_id: example\nstatus: draft\npinned_revisions:\n  api_commit: null\n')

    def put(self, path, text):
        p = self.root / path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)
        return p

    def run_check(self):
        return D.check(self.root, 'example')

    def test_unpinned_draft_is_document_only_pass_without_git(self):
        result = self.run_check()
        self.assertEqual(result['result'], 'DOCUMENT_NAVIGATION_PASS')
        self.assertIn('not YAML schema', result['scope'])

    def test_missing_artifact_fails(self):
        (self.folder / 'tasks.md').unlink()
        self.assertTrue(self.run_check()['errors'])

    def test_query_and_fragment_do_not_become_filename(self):
        self.put('specs/example/page.html', '<html></html>')
        self.put('specs/example/spec.md', '[page](page.html?scenario=results#chat)')
        self.assertFalse(self.run_check()['errors'])

    def test_remote_links_and_code_examples_are_not_local_targets(self):
        self.put('specs/example/spec.md', '[remote](https://example.invalid/a)\n```md\n[x](missing.md)\n```\n')
        self.assertFalse(self.run_check()['errors'])

    def test_missing_link_fails(self):
        self.put('specs/example/spec.md', '[x](missing.md)')
        self.assertTrue(self.run_check()['errors'])

    def test_current_navigation_is_checked(self):
        self.put('specs/example/integration.yaml', 'current_design: "absent.md"\n')
        self.assertTrue(self.run_check()['errors'])

    def test_unsupported_navigation_scalar_fails(self):
        self.put('specs/example/integration.yaml', 'current_design: [design.md]\n')
        self.assertTrue(self.run_check()['errors'])

    def test_navigation_fragment_and_comment(self):
        self.put('specs/example/integration.yaml', 'clarifications: design.md#details # source\n')
        self.assertFalse(self.run_check()['errors'])

    def test_missing_mapping_successor_fails(self):
        self.put('docs/sdd-document-map.json', json.dumps({'removed': {'specs/example/old.md': 'specs/example/missing.md'}}))
        self.assertTrue(self.run_check()['errors'])

    def test_deleted_inline_reference_fails(self):
        self.put('docs/sdd-document-map.json', json.dumps({'removed': {'specs/example/old.md': 'specs/example/design.md'}}))
        self.put('specs/example/spec.md', '`specs/example/old.md`')
        self.assertTrue(self.run_check()['errors'])

    def test_historical_snapshot_and_pin_unchanged(self):
        p = self.put('specs/example/evidence/before/spec.md', '[old](missing.md)')
        original = (self.folder / 'integration.yaml').read_bytes()
        self.assertFalse(self.run_check()['errors'])
        self.assertEqual((self.folder / 'integration.yaml').read_bytes(), original)
        self.assertEqual(p.read_text(), '[old](missing.md)')

    def test_source_summary_is_explicit_exception(self):
        self.put('docs/sdd-document-map.json', json.dumps({'removed': {}, 'feature_dispositions': {'example': {'category': '历史来源'}}}, ensure_ascii=False))
        for name in D.REQUIRED[1:]:
            (self.folder / name).unlink()
        result = self.run_check()
        self.assertFalse(result['errors'])
        self.assertEqual(len(result['exceptions']), 1)

    def test_invalid_and_unknown_ids_rejected(self):
        for name in ('../example', 'unknown', '/tmp'):
            with self.assertRaises(ValueError):
                D.check(self.root, name)


if __name__ == '__main__':
    unittest.main()
