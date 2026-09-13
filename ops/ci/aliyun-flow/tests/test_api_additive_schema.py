"""Offline-only adversarial tests for the exact F06 additive schema runner."""
import fcntl
import hashlib
import importlib.machinery
import io
import json
import os
from pathlib import Path
import subprocess
import tarfile
import tempfile
import time
import unittest
import zipfile


ROOT = Path(__file__).resolve().parents[4]
RUNNER = ROOT / 'ops/ci/aliyun-flow/host/cyf-api-additive-schema'
loader = importlib.machinery.SourceFileLoader('cyf_f06_schema_runner_test_module', str(RUNNER))
f06 = loader.load_module()


def encoded(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':')) + '\n').encode('utf-8')


def digest(value):
    return hashlib.sha256(value).hexdigest()


def hx(value):
    return value.encode('utf-8').hex().upper()


def optional(value):
    return '-' if value is None else '+' + hx(str(value))


def expected_rows(table, collation):
    spec = f06.EXPECTED_TABLES[table]
    rows = {
        'TABLES': [[hx(table), hx('InnoDB'), hx(collation)]],
        'COLUMNS': [],
        'STATISTICS': [],
        'CONSTRAINTS': [],
        'CHECKS': [],
    }
    for ordinal, value in enumerate(spec['columns'], 1):
        name, sql_type, nullable, default, extra = value
        string_type = sql_type.startswith('varchar(') or sql_type.startswith('char(')
        rows['COLUMNS'].append([
            hx(table), str(ordinal), hx(name), hx(sql_type), hx(nullable),
            optional(default), hx(extra), optional('utf8mb4' if string_type else None),
            optional(collation if string_type else None),
        ])
    for name, non_unique, columns, index_type in sorted(spec['indexes'], key=lambda value: value[0]):
        for sequence, column_name in enumerate(columns, 1):
            rows['STATISTICS'].append([
                hx(table), hx(name), str(non_unique), str(sequence), hx(column_name), '-',
                hx(index_type), hx('A'), hx('YES'),
            ])
    constraints = {}
    for name in spec['unique_constraints']:
        constraints[name] = ('PRIMARY KEY' if name == 'PRIMARY' else 'UNIQUE', 'YES')
    for name in spec['checks']:
        constraints[name] = ('CHECK', 'YES')
    for name, (kind, enforced) in sorted(constraints.items()):
        rows['CONSTRAINTS'].append([hx(table), hx(name), hx(kind), hx(enforced)])
    for name, clause in sorted(spec['checks'].items()):
        # Exercise the parser against normal MySQL quoting/charset decoration.
        mysql_clause = clause.replace('outcome_state', '`outcome_state`')
        mysql_clause = mysql_clause.replace("'accepted'", "_utf8mb4'accepted'")
        mysql_clause = mysql_clause.replace("'superseded'", "_utf8mb4'superseded'")
        rows['CHECKS'].append([hx(table), hx(name), hx(mysql_clause)])
    return rows


FAKE_MYSQL = r'''#!/usr/bin/python3
import json
import os
from pathlib import Path
import re
import sys

root = Path(__file__).resolve().parents[1]
state_path = root / 'fake-state.json'
args_path = root / 'mysql-args.json'
args_path.write_text(json.dumps(sys.argv[1:], sort_keys=True))

def load():
    return json.loads(state_path.read_text())

def save(value):
    state_path.write_text(json.dumps(value, sort_keys=True))

def emit(rows):
    for row in rows:
        print('\t'.join(row), flush=True)

for raw in sys.stdin:
    statement = raw.strip()
    marker = re.match(r"SELECT '(_CYF_F06_[0-9]{4}_END_)';$", statement)
    if marker:
        print(marker.group(1), flush=True)
        continue
    state = load()
    if 'GET_LOCK(' in statement:
        print(str(state.get('db_lock_result', 1)), flush=True)
        continue
    if 'RELEASE_LOCK(' in statement:
        print('1', flush=True)
        continue
    tag_match = re.search(r'/\*CYF_F06:([A-Z]+)\*/', statement)
    if tag_match:
        tag = tag_match.group(1)
        if state.get('metadata_error_tag') == tag:
            print('fixture metadata failure', file=sys.stderr, flush=True)
            continue
        if tag == 'SCHEMA':
            emit(state['schema_rows'])
            continue
        rows = []
        for table in sorted(state['tables']):
            table_state = state['tables'][table]
            if table_state == 'absent':
                continue
            table_rows = [list(row) for row in state['expected'][table][tag]]
            if table_state == 'column_drift' and tag == 'COLUMNS':
                table_rows[0][3] = state['hex_int']
            if table_state == 'nullable_drift' and tag == 'COLUMNS':
                table_rows[1][4] = state['hex_yes']
            if table_state == 'default_drift' and tag == 'COLUMNS':
                table_rows[1][5] = '+31'
            if table_state == 'check_drift' and tag == 'CHECKS':
                table_rows[0][2] = state['hex_bad_check']
            if table_state == 'engine_drift' and tag == 'TABLES':
                table_rows[0][1] = state['hex_myisam']
            if table_state == 'collation_drift' and tag == 'TABLES':
                table_rows[0][2] = state['hex_other_collation']
            if table_state == 'index_drift' and tag == 'STATISTICS':
                table_rows = table_rows[:-1]
            if table_state == 'constraint_drift' and tag == 'CONSTRAINTS':
                table_rows[0][3] = state['hex_no']
            rows.extend(table_rows)
        emit(rows)
        continue
    create = re.match(r'CREATE TABLE IF NOT EXISTS ([a-z0-9_]+) ', statement, re.I)
    if create:
        table = create.group(1).lower()
        state['creates'].append(table)
        if state.get('create_fail_on') == table:
            print('fixture create failure', file=sys.stderr, flush=True)
        else:
            state['tables'][table] = ('check_drift' if state.get('create_drift_on') == table
                                      else 'equivalent')
        save(state)
        continue
    print('unexpected fixture SQL', file=sys.stderr, flush=True)
'''


class ApiAdditiveSchemaTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='cyf-f06-schema-', dir='/tmp')
        self.root = Path(self.tmp.name)
        self.root.chmod(0o700)
        for name in ('service', 'state/incoming', 'bin'):
            (self.root / name).mkdir(parents=True, mode=0o700)
        self.mysql = self.root / 'bin/mysql'
        self.mysql.write_text(FAKE_MYSQL)
        self.mysql.chmod(0o700)
        self.collation = 'utf8mb4_0900_ai_ci'
        expected = {table: expected_rows(table, self.collation) for table in f06.TABLE_ORDER}
        self.state = {
            'schema_rows': [[hx('utf8mb4'), hx(self.collation)]],
            'expected': expected,
            'tables': {table: 'absent' for table in f06.TABLE_ORDER},
            'creates': [],
            'hex_int': hx('int'),
            'hex_yes': hx('YES'),
            'hex_no': hx('NO'),
            'hex_myisam': hx('MyISAM'),
            'hex_other_collation': hx('utf8mb4_bin'),
            'hex_bad_check': hx('1 = 1'),
        }
        self.write_state()
        self.commit = 'a' * 40
        self.tree = 'b' * 40
        self.run_id = '39'
        self.resource = f06.F06_SQL_BYTES
        self.rebuild_release()
        self.secret = 'offline-only-secret-value'
        self.env = dict(os.environ)
        self.env.update(
            CYF_F06_SCHEMA_OFFLINE_TEST='YES',
            CYF_F06_SCHEMA_TEST_ROOT=str(self.root),
            CYF_F06_MYSQL_PASSWORD=self.secret,
            # These must not influence the fixed target catalog.
            CYF_F06_DATABASE='attacker_database',
            CYF_F06_SCHEMA='attacker_schema',
            MYSQL_PWD='inherited-wrong-secret',
        )

    def tearDown(self):
        self.tmp.cleanup()

    def write_state(self):
        path = self.root / 'fake-state.json'
        path.write_text(json.dumps(self.state, sort_keys=True))
        path.chmod(0o600)

    def read_state(self):
        return json.loads((self.root / 'fake-state.json').read_text())

    def build_jar(self, resource=None, nested_name=None, resource_name=None):
        resource = self.resource if resource is None else resource
        nested_name = f06.NESTED_MAPPER_JAR if nested_name is None else nested_name
        resource_name = f06.RESOURCE_PATH if resource_name is None else resource_name
        nested = io.BytesIO()
        with zipfile.ZipFile(nested, 'w', zipfile.ZIP_DEFLATED) as archive:
            archive.writestr(resource_name, resource)
        boot = io.BytesIO()
        with zipfile.ZipFile(boot, 'w', zipfile.ZIP_DEFLATED) as archive:
            archive.writestr('META-INF/MANIFEST.MF', 'Start-Class: fixture.Main\n')
            archive.writestr(nested_name, nested.getvalue())
        return boot.getvalue()

    def rebuild_release(self, resource=None, nested_name=None, resource_name=None,
                        record_overrides=None, receipt_overrides=None):
        jar = self.build_jar(resource, nested_name, resource_name)
        canonical = self.root / 'service/cyf-api-kit.jar'
        canonical.write_bytes(jar)
        canonical.chmod(0o600)
        provenance = encoded({'fixture': True})
        flow = {
            'organization_id': f06.EXPECTED_ORG,
            'pipeline_id': f06.EXPECTED_PIPELINE,
            'job_id': f06.EXPECTED_JOB,
            'run_id': self.run_id,
            'source_tip_sha': self.commit,
        }
        source = {
            'branch': 'develop', 'commit_sha': self.commit, 'tree_sha': self.tree,
            'clean_before': True, 'clean_after': True,
        }
        identity = digest(encoded({'flow': flow, 'source': source}))
        records = [
            {'kind': 'application_jar', 'path': 'application.jar',
             'sha256': digest(jar), 'size': len(jar)},
            {'kind': 'dependency_provenance', 'path': 'dependency.provenance.json',
             'sha256': digest(provenance), 'size': len(provenance)},
        ]
        receipt = {
            'schema_version': 1, 'status': 'success', 'gradle_exit_code': 0,
            'bridge_exit_code': 0, 'ticket_sha256': identity,
            'flow': flow, 'source': source, 'files': records,
        }
        if receipt_overrides:
            receipt.update(receipt_overrides)
        receipt_bytes = encoded(receipt)
        metadata = encoded({'fixture': 'metadata'})
        sidecar = encoded({'fixture': 'sidecar'})
        members = {
            'application.jar': jar,
            'application.metadata.json': metadata,
            'application.sidecar.json': sidecar,
            'dependency.provenance.json': provenance,
            'receipt.json': receipt_bytes,
        }
        package = self.root / 'state/incoming/package.tgz'
        with tarfile.open(str(package), 'w:gz') as archive:
            for name, value in members.items():
                info = tarfile.TarInfo(name)
                info.size = len(value)
                archive.addfile(info, io.BytesIO(value))
        package.chmod(0o600)
        record = {
            'schema_version': 2, 'status': 'installed', 'phase': 'installed',
            'recovery': 'not_required', 'ticket_sha256': identity,
            'source_commit_sha': self.commit, 'source_tree_sha': self.tree,
            'run_id': self.run_id, 'receipt_sha256': digest(receipt_bytes),
            'candidate_sha256': digest(jar), 'previous_sha256': 'c' * 64,
            'backup': '/var/lib/cyf-api-flow/backups/fixture.jar',
            'candidate_stop_rc': 0, 'timestamp': '20260913T000000Z',
        }
        if record_overrides:
            record.update(record_overrides)
        record_path = self.root / 'state/record.json'
        record_path.write_bytes(encoded(record))
        record_path.chmod(0o600)

    def execute(self, *args):
        result = subprocess.run(
            [str(RUNNER)] + list(args), env=self.env,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            universal_newlines=True, timeout=20,
        )
        self.assertTrue(result.stdout.strip(), result.stderr)
        return result, json.loads(result.stdout)

    def assert_no_secret_disclosure(self, result, payload):
        combined = result.stdout + result.stderr + json.dumps(payload)
        self.assertNotIn(self.secret, combined)
        args_path = self.root / 'mysql-args.json'
        if args_path.exists():
            args_text = args_path.read_text()
            self.assertNotIn(self.secret, args_text)
            args = json.loads(args_text)
            self.assertIn('--database=jia', args)
            self.assertIn('--user=cyf_f06_schema_runner', args)
            self.assertNotIn('--database=attacker_database', args)
            self.assertFalse(any('password' in value.lower() for value in args))
        self.assertNotIn(self.secret, (self.root / 'fake-state.json').read_text())

    def test_default_plan_is_read_only_and_binds_exact_nested_resource(self):
        result, payload = self.execute()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(payload['status'], 'pass')
        self.assertEqual(payload['operation'], 'plan')
        self.assertEqual(payload['candidate']['resource_outer'], f06.NESTED_MAPPER_JAR)
        self.assertEqual(payload['candidate']['resource_inner'], f06.RESOURCE_PATH)
        self.assertEqual(payload['candidate']['sql_sha256'], f06.RESOURCE_SHA256)
        self.assertEqual(payload['binding']['run'], self.run_id)
        self.assertEqual(self.read_state()['creates'], [])
        self.assertTrue(all(value['status'] == 'planned_create'
                            for value in payload['tables'].values()))
        self.assert_no_secret_disclosure(result, payload)

    def test_apply_creates_only_the_two_exact_tables_and_verifies_equivalence(self):
        result, payload = self.execute('--apply')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(payload['status'], 'pass')
        self.assertEqual(self.read_state()['creates'], list(f06.TABLE_ORDER))
        self.assertTrue(all(value['status'] == 'created_equivalent'
                            for value in payload['tables'].values()))
        self.assert_no_secret_disclosure(result, payload)

    def test_equivalent_existing_tables_are_not_blindly_repeated(self):
        self.state['tables'] = {table: 'equivalent' for table in f06.TABLE_ORDER}
        self.write_state()
        result, payload = self.execute('--apply')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.read_state()['creates'], [])
        self.assertTrue(all(value['status'] == 'existing_equivalent'
                            for value in payload['tables'].values()))


    def test_all_requested_schema_facets_are_fail_closed(self):
        cases = {
            'nullable_drift': 'columns',
            'default_drift': 'columns',
            'engine_drift': 'engine',
            'collation_drift': 'table_collation',
            'index_drift': 'indexes',
            'constraint_drift': 'constraints',
        }
        for state_name, mismatch in cases.items():
            with self.subTest(state=state_name):
                self.state['tables'] = {table: 'absent' for table in f06.TABLE_ORDER}
                self.state['tables'][f06.TABLE_ORDER[0]] = state_name
                self.state['creates'] = []
                self.write_state()
                result, payload = self.execute('--apply')
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(payload['error'], 'existing_schema_drift')
                self.assertIn(mismatch, payload['tables'][f06.TABLE_ORDER[0]]['mismatches'])
                self.assertEqual(self.read_state()['creates'], [])

    def test_runner_file_lock_waits_without_backend_or_schema_mutation(self):
        lock_path = self.root / 'f06-runner.lock'
        lock_path.touch(mode=0o600)
        with lock_path.open('r+') as held:
            fcntl.flock(held, fcntl.LOCK_EX)
            process = subprocess.Popen(
                [str(RUNNER)], env=self.env, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                universal_newlines=True,
            )
            try:
                time.sleep(0.25)
                self.assertIsNone(process.poll())
                self.assertFalse((self.root / 'mysql-args.json').exists())
                self.assertEqual(self.read_state()['creates'], [])
            finally:
                fcntl.flock(held, fcntl.LOCK_UN)
            out, err = process.communicate(timeout=20)
        self.assertEqual(process.returncode, 0, out + err)
        self.assertEqual(json.loads(out)['status'], 'pass')

    def test_database_named_lock_denial_stops_before_metadata_or_ddl(self):
        self.state['db_lock_result'] = 0
        self.write_state()
        result, payload = self.execute('--apply')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(payload['error'], 'database_lock_acquire_failed')
        self.assertEqual(self.read_state()['creates'], [])

    def test_source_contains_no_lifecycle_or_foreign_release_lock_control(self):
        source = RUNNER.read_text()
        self.assertNotIn('/usr/local/sbin/cyf-api-kit', source)
        self.assertNotIn('/tmp/cyf-release-api.lock', source)
        statements = f06.split_exact_statements(f06.F06_SQL_BYTES)
        self.assertEqual(set(statements), set(f06.TABLE_ORDER))
        for statement in statements.values():
            self.assertRegex(statement, r'^CREATE TABLE IF NOT EXISTS ')
            for forbidden in (' ALTER ', ' DROP ', ' INSERT ', ' UPDATE ', ' DELETE ', ' REPLACE '):
                self.assertNotIn(forbidden, ' ' + statement.upper() + ' ')

    def test_existing_column_drift_fails_before_any_create(self):
        self.state['tables'][f06.TABLE_ORDER[0]] = 'column_drift'
        self.write_state()
        result, payload = self.execute('--apply')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(payload['error'], 'existing_schema_drift')
        self.assertIn('columns', payload['tables'][f06.TABLE_ORDER[0]]['mismatches'])
        self.assertEqual(self.read_state()['creates'], [])

    def test_check_constraint_drift_fails_closed(self):
        self.state['tables'][f06.TABLE_ORDER[0]] = 'check_drift'
        self.write_state()
        result, payload = self.execute()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(payload['error'], 'existing_schema_drift')
        self.assertTrue(any(value.startswith('check_clause:')
                            for value in payload['tables'][f06.TABLE_ORDER[0]]['mismatches']))
        self.assertEqual(self.read_state()['creates'], [])

    def test_partial_autocommit_is_preserved_and_retry_verifies_before_continuing(self):
        second = f06.TABLE_ORDER[1]
        self.state['create_fail_on'] = second
        self.write_state()
        first_result, first_payload = self.execute('--apply')
        self.assertNotEqual(first_result.returncode, 0)
        self.assertEqual(first_payload['failed_table'], second)
        self.assertEqual(first_payload['tables'][f06.TABLE_ORDER[0]]['status'], 'created_equivalent')
        after_first = self.read_state()
        self.assertEqual(after_first['tables'][f06.TABLE_ORDER[0]], 'equivalent')
        self.assertEqual(after_first['tables'][second], 'absent')
        self.assertEqual(after_first['creates'], list(f06.TABLE_ORDER))

        after_first.pop('create_fail_on')
        after_first['creates'] = []
        self.state = after_first
        self.write_state()
        second_result, second_payload = self.execute('--apply')
        self.assertEqual(second_result.returncode, 0, second_result.stderr)
        self.assertEqual(self.read_state()['creates'], [second])
        self.assertEqual(second_payload['tables'][f06.TABLE_ORDER[0]]['status'],
                         'existing_equivalent')
        self.assertEqual(second_payload['tables'][second]['status'], 'created_equivalent')

    def test_post_create_drift_is_not_dropped_or_followed_by_second_create(self):
        first = f06.TABLE_ORDER[0]
        self.state['create_drift_on'] = first
        self.write_state()
        result, payload = self.execute('--apply')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(payload['failed_table'], first)
        state = self.read_state()
        self.assertEqual(state['tables'][first], 'check_drift')
        self.assertEqual(state['tables'][f06.TABLE_ORDER[1]], 'absent')
        self.assertEqual(state['creates'], [first])

    def test_metadata_query_error_stops_before_ddl(self):
        self.state['metadata_error_tag'] = 'COLUMNS'
        self.write_state()
        result, payload = self.execute('--apply')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(payload['error'], 'metadata_query_failed')
        self.assertEqual(self.read_state()['creates'], [])

    def test_resource_with_extra_drop_is_rejected_even_when_receipt_matches_jar(self):
        self.rebuild_release(resource=self.resource + b'\nDROP TABLE forbidden;\n')
        result, payload = self.execute('--apply')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(payload['error'], 'f06_resource_digest_mismatch')
        self.assertFalse((self.root / 'mysql-args.json').exists())
        self.assertEqual(self.read_state()['creates'], [])

    def test_wrong_nested_module_location_is_rejected(self):
        self.rebuild_release(nested_name='BOOT-INF/lib/not-the-mapper.jar')
        result, payload = self.execute()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(payload['error'], 'mapper_jar_location_invalid')
        self.assertFalse((self.root / 'mysql-args.json').exists())

    def test_record_receipt_source_run_mismatch_is_rejected(self):
        self.rebuild_release(record_overrides={'run_id': '40'})
        result, payload = self.execute()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(payload['error'], 'receipt_release_identity_mismatch')
        self.assertFalse((self.root / 'mysql-args.json').exists())

    def test_arbitrary_cli_payload_is_rejected_without_touching_backend(self):
        result, payload = self.execute('--apply', '--database=evil')
        self.assertEqual(result.returncode, 2)
        self.assertEqual(payload['error'], 'arguments_rejected')
        self.assertFalse((self.root / 'mysql-args.json').exists())
        self.assertEqual(self.read_state()['creates'], [])

    def test_missing_password_fails_without_starting_mysql(self):
        del self.env['CYF_F06_MYSQL_PASSWORD']
        result, payload = self.execute()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(payload['error'], 'mysql_password_environment_missing')
        self.assertFalse((self.root / 'mysql-args.json').exists())


if __name__ == '__main__':
    unittest.main()
