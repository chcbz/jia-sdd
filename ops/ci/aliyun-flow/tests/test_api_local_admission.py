#!/usr/bin/env python3
"""Private SYNTHETIC units only. No actual batch/build/package/install proof.

Root-only admission is exercised under an exclusively owned temporary home
anchor, NEVER actual /var/lib admission roots. Test-only OpenCV bytes/pin mocks
cannot be enabled by the production CLI. No Gradle, process/service or network.
"""
import argparse
import ast
import contextlib
import copy
import importlib.machinery
import importlib.util
import io
import json
import os
from pathlib import Path
import stat
import tarfile
import tempfile
import unittest
from unittest import mock
import zipfile

BASE = Path(__file__).resolve().parents[1]
HELPER = BASE / 'auto/admit-api-local.py'
WRAPPER = BASE / 'host/cyf-api-local-admit'
PRODUCER = BASE / 'auto/package-api-local.py'


def load(name, path):
    loader = importlib.machinery.SourceFileLoader(name, str(path))
    spec = importlib.util.spec_from_loader(name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


m = load('ur05_admission_private_unit', HELPER)
w = load('ur05_wrapper_private_unit', WRAPPER)


class Fixture:
    """All observations and materials below are explicitly synthetic unit input."""
    def __init__(self, root):
        self.root = root
        self.trusted = root / 'trusted'
        self.authority = root / 'authority'
        self.ingress = root / 'ingress'
        for p in (self.trusted, self.authority, self.ingress):
            p.mkdir(mode=0o700)
        for name in ('admitted', 'proofs', 'records'):
            (self.trusted / name).mkdir(mode=0o700)
        self.ident = {'version': '0.1.0-synthetic', 'buildId': 'unit-only-not-a-build', 'commit': 'c'*40, 'tree': 'd'*40}
        self.batch = 'synthetic-unit-batch'
        self.dependency = b'UNIT SYNTHETIC OpenCV replacement; NOT production artifact'
        self.data = {}
        self.roles = {}
        self.source = '/synthetic/source'
        self.build = '/synthetic/build'
        self.evpath = self.build + '/build-evidence.json'
        self.proofpath = self.build + '/local-bootjar-proof.json'
        self.logpath = self.build + '/invocation.log'
        self.provpath = self.build + '/opencv-resolved.json'
        self.deppath = '/synthetic/cache/opencv.jar'
        self.initpath = '/synthetic/control/local-release-metadata.init.gradle'
        self.jarpath = self.build + '/boot.jar'
        self.jar = self.make_jar()
        self.tasks = (':starter:publicArtifactVerifierTest', ':starter:poiProductionRuntimeClasspathTest', ':agent:test')
        self.clean = {'commit': self.ident['commit'], 'tree': self.ident['tree'], 'clean': True}
        self.proof = {'format': 'cyf-api-local-bootjar-proof-v1', 'identity': self.ident,
            'sourceRoot': self.source, 'buildRoot': self.build, 'sourceBefore': self.clean, 'sourceAfter': self.clean,
            'task': ':starter:bootJar', 'metadata': self.metadata(), 'moduleVersion': '1.1.2-SNAPSHOT',
            'implementationVersion': None, 'jar': {'path': self.jarpath, **m.binding(self.jar)},
            'publicArtifactVerifier': 'bootJar-original-doLast-completed'}
        self.ev = {'format': 'cyf-api-local-build-evidence-v1', 'identity': self.ident,
            'sourceRoot': self.source, 'buildRoot': self.build, 'sourceBefore': self.clean, 'sourceAfter': self.clean,
            'invocation': {'argv': ['./gradlew', '--console=plain', '--no-daemon', '--no-build-cache',
                '-I', self.initpath, *self.tasks, ':validateLayering', ':starter:bootJar'],
                'exitCode': 0, 'cacheHit': False, 'log': {}, 'selector': 'synthetic-unit-selector',
                'fixtureSha256': 'f'*64, 'inputs': []}, 'tests': [],
            'validateLayering': {'task': ':validateLayering'}, 'bootJar': {'task': ':starter:bootJar', 'proof': {}}, 'opencv': {}}
        self.put(self.source + '/settings.gradle', b'// UNIT SYNTHETIC settings\n', 'input')
        self.put(self.source + '/starter/build.gradle', b'// UNIT SYNTHETIC build\n', 'input')
        self.put(self.initpath, b'// UNIT SYNTHETIC init never executed\n', 'input')
        for i, task in enumerate(self.tasks):
            path = self.build + '/TEST-unit-%d.xml' % i
            self.put(path, b'<testsuite tests="1" failures="0" errors="0" skipped="0"><testcase classname="UnitSynthetic" name="only"/></testsuite>', 'test-report')
            self.ev['tests'].append({'task': task, 'selector': 'synthetic-selector-%d' % i,
                'fixtureSha256': 'a'*64, 'reports': [self.ref(path)]})
        self.auth = None
        self.verification = None
        self.record = None
        self.rebuild()

    def put(self, path, data, role):
        self.data[path] = data
        self.roles[path] = role

    def ref(self, path):
        return {'path': path, **m.binding(self.data[path])}

    def metadata(self):
        return dict(zip(m.META_KEYS, (self.ident[k] for k in ('version', 'commit', 'tree', 'buildId'))))

    def make_jar(self, mail=True, changes=None, implementation=None, duplicate=False):
        out = io.BytesIO()
        attrs = {'Manifest-Version': '1.0', 'Main-Class': 'org.springframework.boot.loader.launch.JarLauncher',
                 'Start-Class': 'cn.jia.JiaApplication', **self.metadata()}
        attrs.update(changes or {})
        if implementation is not None:
            attrs['Implementation-Version'] = implementation
        text = ''.join('%s: %s\r\n' % v for v in attrs.items()) + '\r\n'
        with zipfile.ZipFile(out, 'w') as boot:
            boot.writestr('META-INF/MANIFEST.MF', text)
            if mail:
                dep = io.BytesIO()
                with zipfile.ZipFile(dep, 'w') as nested:
                    for name in sorted(m.MAIL_CLASSES):
                        nested.writestr(name, b'UNIT SYNTHETIC CLASS, NEVER JVM execution')
                boot.writestr('BOOT-INF/lib/unit-synthetic-mail.jar', dep.getvalue())
            if duplicate:
                # Negative input deliberately includes a duplicate ZIP name.
                import warnings
                with warnings.catch_warnings():
                    warnings.simplefilter('ignore')
                    boot.writestr('META-INF/MANIFEST.MF', text)
        return out.getvalue()

    def write(self, path, data):
        path.write_bytes(data)
        path.chmod(0o600)

    def rebuild(self, log_suffix='', omitted_task=None, extra_log=''):
        self.put(self.deppath, self.dependency, 'opencv-jar')
        self.put(self.provpath, m.canonical({'coordinate': 'org.opencv:opencv:4.5.5',
            'jar_sha256': m.sha(self.dependency), 'jar_size': len(self.dependency), 'resolved_file': self.deppath}), 'input')
        self.ev['opencv'] = self.ref(self.provpath)
        self.proof['jar'] = {'path': self.jarpath, **m.binding(self.jar)}
        self.put(self.proofpath, m.canonical(self.proof), 'bootjar-proof')
        self.ev['bootJar']['proof'] = self.ref(self.proofpath)
        lines = ['GRADLE_LOCK_ACQUIRED task=synthetic-unit pid=0']
        lines += ['> Task ' + task + log_suffix for task in (*self.tasks, ':validateLayering', ':starter:bootJar') if task != omitted_task]
        lines += ['CYF_LOCAL_BOOTJAR_BEGIN ' + self.ident['buildId'],
                  'CYF_LOCAL_BOOTJAR_END ' + m.sha(self.data[self.proofpath]), 'BUILD SUCCESSFUL in UNIT-SYNTHETIC', extra_log]
        self.put(self.logpath, ('\n'.join(lines)+'\n').encode(), 'invocation-log')
        self.ev['invocation']['log'] = self.ref(self.logpath)
        self.ev['invocation']['inputs'] = [self.ref(p) for p in (self.source+'/settings.gradle', self.source+'/starter/build.gradle', self.initpath)]
        for test in self.ev['tests']:
            test['reports'] = [self.ref(r['path']) for r in test['reports']]
        self.put(self.evpath, m.canonical(self.ev), 'build-evidence')
        self.tests = [dict({k: t[k] for k in ('task', 'selector', 'fixtureSha256')}, reports=[
            {**m.binding(self.data[r['path']]), **m.xml_summary(self.data[r['path']])} for r in t['reports']]) for t in self.ev['tests']]
        jar_ref = {'path': 'application.jar', **m.binding(self.jar)}
        prov_ref = {'path': 'dependency.provenance.json', **m.binding(self.data[self.provpath])}
        receipt = {'format': 'cyf-api-local-release-receipt-v1', 'status': 'packaged', 'producer': {'kind': 'local-build-v1'},
            'identity': self.ident, 'source': {'commit': self.ident['commit'], 'tree': self.ident['tree'], 'cleanBefore': True, 'cleanAfter': True},
            'evidence': {'sha256': m.sha(self.data[self.evpath]), 'invocationLogSha256': m.sha(self.data[self.logpath]),
                'selector': self.ev['invocation']['selector'], 'fixtureSha256': self.ev['invocation']['fixtureSha256'],
                'inputs': self.ev['invocation']['inputs'], 'tests': self.tests, 'bootJarProofSha256': m.sha(self.data[self.proofpath])},
            'applicationJar': jar_ref, 'dependencyProvenance': prov_ref,
            'verification': {'mailRuntimeClasses': sorted(m.MAIL_CLASSES), 'publicArtifactVerifier': 'bootJar-original-doLast-completed'}}
        receipt_data = m.canonical(receipt)
        base = {'identity': self.ident, 'receiptSha256': m.sha(receipt_data), 'applicationJar': jar_ref, 'dependencyProvenance': prov_ref}
        self.payloads = {'application.jar': self.jar, 'dependency.provenance.json': self.data[self.provpath],
            'receipt.json': receipt_data,
            'application.metadata.json': m.canonical({'format': 'cyf-api-local-application-metadata-v1', **base,
                'moduleVersion': self.proof['moduleVersion'], 'implementationVersion': self.proof['implementationVersion']}),
            'application.sidecar.json': m.canonical({'format': 'cyf-api-local-application-sidecar-v1', **base})}
        snapshots = []
        for i, (p, data) in enumerate(self.data.items()):
            target = self.trusted / 'proofs' / ('unit-%d.bin' % i)
            self.write(target, data)
            snapshots.append({'role': self.roles[p], 'originalPath': p, 'file': {'path': str(target), **m.binding(data)}})
        self.record = {'format': 'cyf-api-local-trusted-record-v1', 'scope': m.SCOPE, 'batchId': self.batch, 'identity': self.ident,
            'package': {}, 'payloads': {}, 'buildEvidence': next(x['file'] for x in snapshots if x['role']=='build-evidence'),
            'snapshots': snapshots, 'installPrecondition': {'canonicalJarSha256': 'e'*64}}
        self.verification = {'format': 'cyf-api-local-controller-verification-v1', 'authorityId': m.AUTHORITY_ID,
            'batchId': self.batch, 'identity': self.ident, 'buildEvidenceSha256': m.sha(self.data[self.evpath]),
            'package': {}, 'payloads': {}, 'invocationLogSha256': m.sha(self.data[self.logpath]),
            'bootJarProofSha256': m.sha(self.data[self.proofpath]), 'requiredTests': self.tests,
            'observations': dict(m.OBSERVATIONS)}
        self.auth = {'format': 'cyf-api-local-batch-authority-v1', 'authorityId': m.AUTHORITY_ID, 'scope': m.SCOPE,
            'batchId': self.batch, 'identity': self.ident, 'trustedRecordSha256': '', 'verificationRecord': {}}
        self.repack()

    def archive(self, extra=None, omitted=None, duplicate=None):
        out = io.BytesIO()
        with tarfile.open(fileobj=out, mode='w:gz', format=tarfile.USTAR_FORMAT) as archive:
            for name, data in self.payloads.items():
                if name == omitted:
                    continue
                item = tarfile.TarInfo(name)
                item.mode, item.size = 0o600, len(data)
                archive.addfile(item, io.BytesIO(data))
                if name == duplicate:
                    archive.addfile(item, io.BytesIO(data))
            if extra:
                item, data = extra
                archive.addfile(item, io.BytesIO(data) if data else None)
        return out.getvalue()

    def repack(self, **kwargs):
        self.package = self.ingress / 'unit-synthetic-package.tgz'
        self.package_data = self.archive(**kwargs)
        self.write(self.package, self.package_data)
        self.record['package'] = m.binding(self.package_data)
        self.record['payloads'] = {k: m.binding(v) for k, v in self.payloads.items()}
        self.verification['package'] = copy.deepcopy(self.record['package'])
        self.verification['payloads'] = copy.deepcopy(self.record['payloads'])
        self.save_records()

    def save_records(self):
        self.verification_path = self.authority / 'unit-controller-verification.json'
        self.record_path = self.trusted / 'records' / 'unit-trusted-record.json'
        self.auth_path = self.authority / 'unit-batch-authority.json'
        self.write(self.verification_path, m.canonical(self.verification))
        self.write(self.record_path, m.canonical(self.record))
        self.auth['verificationRecord'] = {'path': str(self.verification_path), **m.binding(self.verification_path.read_bytes())}
        self.auth['trustedRecordSha256'] = m.sha(self.record_path.read_bytes())
        self.write(self.auth_path, m.canonical(self.auth))

    def args(self):
        return argparse.Namespace(opt_in=True, trusted_root=str(self.trusted), authority_root=str(self.authority),
            trusted_record=str(self.record_path), trusted_record_sha256=m.sha(self.record_path.read_bytes()),
            batch_authority=str(self.auth_path), batch_authority_sha256=m.sha(self.auth_path.read_bytes()),
            package=str(self.package), output=str(self.trusted / 'admitted' / 'unit-admitted'))

    def pins(self):
        # Test-only. NOT a real OpenCV/bootJar/build/authority proof.
        return mock.patch.multiple(m, OPENCV_SHA=m.sha(self.dependency), OPENCV_SIZE=len(self.dependency))


class AdmissionTest(unittest.TestCase):
    def setUp(self):
        # Use only an exclusive private scratch, not actual host admission roots.
        self.temp = tempfile.TemporaryDirectory(prefix='.ur05-private-synthetic-', dir=str(Path.home()))
        self.root = Path(self.temp.name)
        self.addCleanup(self.temp.cleanup)
        self.f = Fixture(self.root)
        self.addCleanup(mock.patch.stopall)
        mock.patch.dict(os.environ, {'PIPELINE_ID':'', 'BUILD_NUMBER':'', 'CYF_FLOW_GRADLE_ACTIVE':''}).start()

    def run_admission(self, args=None):
        with self.f.pins():
            return m.admit(args or self.f.args())

    def reject(self, code=None, args=None):
        with self.assertRaises(m.Rejected) as error:
            self.run_admission(args)
        if code:
            self.assertEqual(error.exception.code, code)
        self.assertFalse(Path((args or self.f.args()).output).exists())
        self.assertEqual(list((self.f.trusted/'admitted').iterdir()), [])
        return error.exception.code

    def change_payload(self, name, change):
        obj = json.loads(self.f.payloads[name])
        change(obj)
        self.f.payloads[name] = m.canonical(obj)
        self.f.repack()

    def test_synthetic_full_consistency_external_digest_and_inventory(self):
        result = self.run_admission()
        self.assertEqual(result['status'], 'admitted')
        self.assertIs(result['productionAuthorized'], False)
        admitted_path = Path(result['admission']['path'])
        self.assertEqual(m.binding(admitted_path.read_bytes()), {k:result['admission'][k] for k in ('sha256','size')})
        admitted = json.loads(admitted_path.read_bytes())
        self.assertEqual(admitted['source'], {'kind':'local-build-v1','identity':self.f.ident})
        self.assertEqual(set(admitted['payloads']), set(m.MEMBERS))
        self.assertEqual(admitted['scope'], 'artifact-admission-only')
        self.assertNotIn('consumed', admitted)
        self.assertNotIn('run_id', admitted)
        self.assertNotIn('admissionSha256', admitted)
        refs = [admitted['package'], *admitted['payloads'].values(), *[admitted['authority'][k] for k in ('batchAuthority','trustedRecord','verificationRecord')]]
        refs += [s['file'] for s in admitted['evidence']['snapshots']]
        for ref in refs:
            file = Path(ref['path'])
            self.assertEqual(m.binding(file.read_bytes()), {k:ref[k] for k in ('sha256','size')})
            self.assertEqual(stat.S_IMODE(file.stat().st_mode), 0o600)
            self.assertEqual(file.stat().st_nlink, 1)
        self.assertEqual(set(Path(self.f.args().output).iterdir()), {Path(self.f.args().output)/x for x in ('package.tgz','payload','authority','evidence','admission.json')})
        self.assertEqual(self.f.package.read_bytes(), self.f.package_data)

    def test_consistent_producer_without_independent_authority_is_rejected(self):
        args = self.f.args()
        self.f.auth_path.unlink()
        with self.assertRaises(m.Rejected) as error:
            self.run_admission(args)
        self.assertEqual(error.exception.code, 'AUTHORITY_INVALID')
        self.assertFalse(Path(args.output).exists())

    def test_controller_observations_missing_or_false_or_type_confused(self):
        original = copy.deepcopy(self.f.verification)
        for key in m.OBSERVATIONS:
            for value in (None, False, 'PASS'):
                with self.subTest(key=key, value=value):
                    self.f.verification = copy.deepcopy(original)
                    self.f.verification['observations'][key] = value
                    self.f.save_records()
                    self.reject('AUTHORITY_INVALID')
        self.f.verification = copy.deepcopy(original)
        del self.f.verification['observations']
        self.f.save_records()
        self.reject('AUTHORITY_INVALID')

    def test_foreign_authority_id_or_scope_or_batch_or_identity(self):
        original = copy.deepcopy(self.f.auth)
        for key, value in (('authorityId','producer-self-approval'),('scope','production'),('batchId','foreign'),('identity',dict(self.f.ident,commit='a'*40))):
            with self.subTest(key=key):
                self.f.auth = copy.deepcopy(original)
                self.f.auth[key] = value
                self.f.save_records()
                self.reject('AUTHORITY_INVALID')

    def test_authority_and_record_independent_digest_pins(self):
        for key in ('batch_authority_sha256','trusted_record_sha256'):
            with self.subTest(key=key):
                args=self.f.args(); setattr(args,key,'0'*64)
                self.reject('AUTHORITY_INVALID', args)

    def test_producer_receipt_cannot_be_batch_authority(self):
        self.f.write(self.f.auth_path,self.f.payloads['receipt.json'])
        self.reject('AUTHORITY_INVALID')

    def test_root_record_foreign_identity(self):
        self.f.record['identity'] = dict(self.f.ident,tree='a'*40)
        self.f.save_records()
        self.reject('IDENTITY_MISMATCH')

    def test_record_extra_flow_or_secret_keys(self):
        for key in ('flow','token','password','run_id'):
            with self.subTest(key=key):
                self.f.record[key] = 'SYNTHETIC SECRET MUST NEVER BE PRINTED'
                self.f.save_records()
                self.reject('EVIDENCE_INVALID')
                del self.f.record[key]

    def test_duplicate_json_and_nan(self):
        for data in (b'{"a":1,"a":2}', b'{"a":NaN}', b'{"a":Infinity}'):
            with self.subTest(data=data), self.assertRaises(m.Rejected):
                m.strict_json(data)

    def test_frozen_json_has_no_float_fields_or_exponent_overflow(self):
        for data in (b'{"size":1.0}', b'{"nested":{"size":1e9999}}',
                     b'{"nested":[-Infinity]}'):
            for code in ('EVIDENCE_INVALID', 'AUTHORITY_INVALID'):
                with self.subTest(data=data, code=code), self.assertRaises(m.Rejected) as error:
                    m.strict_json(data, code)
                self.assertEqual(error.exception.code, code)

    def test_controller_exact_payload_map_and_digest_types(self):
        original = copy.deepcopy(self.f.verification)
        for key, value in (('size', True), ('sha256', 'not-a-digest')):
            with self.subTest(key=key):
                self.f.verification = copy.deepcopy(original)
                self.f.verification['payloads']['application.jar'][key] = value
                self.f.save_records()
                self.reject('AUTHORITY_INVALID')
        self.f.verification = copy.deepcopy(original)
        self.f.verification['payloads']['foreign'] = dict(original['payloads']['application.jar'])
        self.f.save_records()
        self.reject('AUTHORITY_INVALID')

    def test_file_integer_bool_rejected(self):
        with self.assertRaises(m.Rejected):
            m.file_ref({'path':'/synthetic/file','sha256':'a'*64,'size':True})

    def test_ingress_package_tampered(self):
        self.f.package.write_bytes(b'TAMPERED SYNTHETIC')
        self.reject('DIGEST_MISMATCH')

    def test_exact_archive_catalog_rejects_missing_duplicate_extra_links_and_traversal(self):
        for args in ({'omitted':'receipt.json'}, {'duplicate':'receipt.json'}):
            with self.subTest(args=args):
                self.f.repack(**args);self.reject('PACKAGE_INVALID')
        for name, kind in (('../escape',tarfile.REGTYPE),('/absolute',tarfile.REGTYPE),('extra',tarfile.REGTYPE),
                           ('extra',tarfile.SYMTYPE),('extra',tarfile.LNKTYPE),('extra',tarfile.DIRTYPE),('extra',tarfile.FIFOTYPE)):
            with self.subTest(name=name, kind=kind):
                item=tarfile.TarInfo(name);item.type=kind
                item.linkname='receipt.json' if kind in (tarfile.SYMTYPE,tarfile.LNKTYPE) else ''
                item.size=1 if kind==tarfile.REGTYPE else 0
                self.f.repack(extra=(item,b'x' if item.size else None));self.reject('PACKAGE_INVALID')

    def test_payload_actual_digest_mismatch(self):
        self.f.record['payloads']['receipt.json']['sha256']='0'*64
        self.f.verification['payloads']=copy.deepcopy(self.f.record['payloads'])
        self.f.save_records();self.reject('DIGEST_MISMATCH')

    def test_receipt_metadata_sidecar_identity_and_receipt_binding(self):
        for name in ('receipt.json','application.metadata.json','application.sidecar.json'):
            with self.subTest(name=name):
                self.f.rebuild()
                self.change_payload(name,lambda obj:obj.update(identity=dict(self.f.ident,buildId='foreign')))
                self.reject('EVIDENCE_INVALID')
        self.f.rebuild()
        self.change_payload('application.sidecar.json',lambda obj:obj.update(receiptSha256='0'*64))
        self.reject('EVIDENCE_INVALID')

    def test_receipt_boolean_clean_required(self):
        self.change_payload('receipt.json',lambda obj:obj['source'].update(cleanAfter=1))
        self.reject('EVIDENCE_INVALID')

    def test_implementation_version_preserved_and_mismatch_rejected(self):
        self.f.jar=self.f.make_jar(implementation='1.1.2-SNAPSHOT')
        self.f.proof['implementationVersion']='1.1.2-SNAPSHOT'
        self.f.rebuild()
        self.assertEqual(self.run_admission()['status'],'admitted')

    def test_wrong_jar_manifest_identity(self):
        self.f.jar=self.f.make_jar(changes={'CYF-Source-Tree':'0'*40});self.f.rebuild()
        self.reject('JAR_INVALID')

    def test_missing_actual_nested_mail_runtime(self):
        self.f.jar=self.f.make_jar(mail=False);self.f.rebuild()
        self.reject('MAIL_RUNTIME_INVALID')

    def test_duplicate_zip_entries_rejected(self):
        self.f.jar=self.f.make_jar(duplicate=True);self.f.rebuild()
        self.reject('JAR_INVALID')

    def test_unmodified_actual_opencv_pin(self):
        self.assertEqual(m.OPENCV_SHA,'323d40119548134b0966d3735e97a78d1edbc79bd91e7fb1074e5152392095f4')
        self.assertEqual(m.OPENCV_SIZE,722802)
        # Synthetic dependency never passes an unmocked production verifier.
        with self.assertRaises(m.Rejected):m.admit(self.f.args())
        self.assertFalse(Path(self.f.args().output).exists())

    def test_provenance_coordinate_mismatch(self):
        self.change_payload('dependency.provenance.json',lambda obj:obj.update(coordinate='org.opencv:opencv:other'))
        self.reject('EVIDENCE_INVALID')

    def test_proof_snapshots_must_be_actual_matching_bytes(self):
        path=Path(self.f.record['snapshots'][0]['file']['path'])
        path.write_bytes(b'TAMPERED SYNTHETIC PROOF')
        self.reject('DIGEST_MISMATCH')

    def test_complete_snapshot_closure_no_missing_extra_duplicate_or_wrong_roles(self):
        original=copy.deepcopy(self.f.record['snapshots'])
        variations=[original[:-1], original+[dict(original[0],originalPath='/synthetic/extra')], original+[original[0]],
                    [dict(x,role='test-report') if x['role']=='invocation-log' else x for x in original]]
        for snapshots in variations:
            with self.subTest(count=len(snapshots)):
                self.f.record['snapshots']=snapshots;self.f.save_records();self.reject()

    def test_snapshot_originals_never_read_from_builder_paths(self):
        with mock.patch.object(m,'open_directory', wraps=m.open_directory) as opened:
            self.run_admission()
        self.assertTrue(all(not str(call[0][0]).startswith('/synthetic/') for call in opened.call_args_list))

    def test_failed_exit_cache_and_dirty_source_are_not_valid(self):
        for section,key,value in (('invocation','exitCode',1),('invocation','cacheHit',True),
                                  ('sourceAfter','clean',False),('sourceBefore','clean',1)):
            with self.subTest(section=section,key=key):
                old=copy.deepcopy(self.f.ev)
                self.f.ev[section][key]=value;self.f.rebuild();self.reject('EVIDENCE_INVALID')
                self.f.ev=old;self.f.rebuild()

    def test_exact_task_execution_allows_testclasses_siblings(self):
        siblings = '\n'.join('> Task ' + task + 'Classes' for task in self.f.tasks)
        self.f.rebuild(extra_log=siblings)
        self.assertEqual(self.run_admission()['status'], 'admitted')

    def test_exact_task_token_rejects_prefix_only_status_and_duplicates(self):
        task = self.f.tasks[0]
        for extra in ('> Task ' + task + 'Classes', '> Task ' + task + 'Extra',
                      '> Task ' + task + ':child', '> Task ' + task + '-sibling',
                      '> Task ' + task + ' UP-TO-DATE', '> Task ' + task + ' FROM-CACHE',
                      '> Task ' + task + ' SKIPPED', '> Task ' + task + ' NO-SOURCE'):
            with self.subTest(extra=extra):
                self.f.rebuild(omitted_task=task, extra_log=extra)
                self.reject('EVIDENCE_INVALID')
        self.f.rebuild(extra_log='> Task ' + task)
        self.reject('EVIDENCE_INVALID')

    def test_cached_or_missing_tasks_and_evidence_hit_rejected(self):
        for kwargs in ({'log_suffix':' UP-TO-DATE'},{'omitted_task':':starter:bootJar'},{'extra_log':'EVIDENCE_HIT selector=unit'}):
            with self.subTest(kwargs=kwargs):
                self.f.rebuild(**kwargs);self.reject('EVIDENCE_INVALID')

    def test_public_verifier_completion_proof_required(self):
        self.f.proof['publicArtifactVerifier']='SKIPPED';self.f.rebuild();self.reject('EVIDENCE_INVALID')

    def test_required_scope_selectors_and_fixtures_match_controller(self):
        for key,value in (('selector','foreign-selector'),('fixtureSha256','0'*64),('task',':other:test')):
            with self.subTest(key=key):
                self.f.verification['requiredTests']=copy.deepcopy(self.f.tests)
                self.f.verification['requiredTests'][0][key]=value
                # Missing a controller-required starter task invalidates the
                # authority itself, before comparing producer evidence. A valid
                # scope with mismatched selector/fixture remains evidence-invalid.
                self.f.save_records()
                self.reject('AUTHORITY_INVALID' if key == 'task' else 'EVIDENCE_INVALID')

    def test_controller_count_boolean_not_an_int(self):
        self.f.verification['requiredTests']=copy.deepcopy(self.f.tests)
        self.f.verification['requiredTests'][0]['reports'][0]['tests']=True
        self.f.save_records();self.reject('AUTHORITY_INVALID')

    def test_xml_failure_skipped_all_duplicate_and_dtd(self):
        for xml in (b'<testsuite tests="1"><testcase classname="X" name="Y"><failure/></testcase></testsuite>',
                    b'<testsuite tests="2"><testcase classname="X" name="Y"/><testcase classname="X" name="Y"/></testsuite>',
                    b'<!DOCTYPE test><testsuite tests="0"/>'):
            with self.subTest(xml=xml),self.assertRaises(m.Rejected):m.xml_summary(xml)
        summary=m.xml_summary(b'<testsuite tests="1" skipped="1"><testcase classname="X" name="Y"><skipped/></testcase></testsuite>')
        self.assertEqual(summary['tests']-summary['skipped'],0)

    def test_encoded_xml_dtd_and_entity_do_not_bypass_safe_parser(self):
        # Byte substring screening alone misses UTF-16/32. Parser must reject
        # the DTD before expansion and must never resolve external material.
        document = '<!DOCTYPE testsuite [<!ENTITY x "synthetic">]><testsuite tests="1"><testcase classname="X" name="&x;"/></testsuite>'
        for encoding in ('utf-8', 'utf-16', 'utf-32'):
            with self.subTest(encoding=encoding), self.assertRaises(m.Rejected) as error:
                m.xml_summary(document.encode(encoding))
            self.assertEqual(error.exception.code, 'EVIDENCE_INVALID')

    def test_argv_cannot_load_secret_or_arbitrary_command(self):
        self.f.ev['invocation']['argv']+=['-Ppassword=SYNTHETIC-SECRET']
        self.f.rebuild();self.reject('EVIDENCE_INVALID')

    def test_trust_root_owner_mode_ancestry_and_nested_anchors(self):
        self.f.trusted.chmod(0o755)
        self.reject('PATH_UNSAFE')
        self.f.trusted.chmod(0o700)
        self.root.chmod(0o777)
        self.reject('PATH_UNSAFE')
        self.root.chmod(0o700)
        args=self.f.args();args.authority_root=str(self.f.trusted/'proofs')
        self.reject('PATH_UNSAFE',args)

    def test_unprotected_authority_file_and_verification_file(self):
        for path in (self.f.auth_path,self.f.verification_path,self.f.record_path):
            with self.subTest(path=path):
                path.chmod(0o644);self.reject('PATH_UNSAFE');path.chmod(0o600)

    def test_nonroot_file_owner_rejected(self):
        os.chown(self.f.auth_path,12345,12345)
        try:self.reject('PATH_UNSAFE')
        finally:os.chown(self.f.auth_path,0,0)

    def test_hardlinks_rejected_for_ingress_and_proof(self):
        for path in (self.f.package,self.f.auth_path):
            with self.subTest(path=path):
                alias=self.root/'hardlink';os.link(path,alias)
                try:self.reject('PATH_UNSAFE')
                finally:alias.unlink()

    def test_symlink_component_and_final_leaf(self):
        alias=self.root/'symlink';alias.symlink_to(self.f.trusted,target_is_directory=True)
        args=self.f.args();args.trusted_root=str(alias);args.output=str(alias/'admitted'/'unit-admitted')
        with self.assertRaises(OSError):self.run_admission(args)
        self.f.package.unlink();self.f.package.symlink_to(self.f.record_path)
        with self.assertRaises(OSError):self.run_admission()

    def test_noncanonical_paths_and_unsafe_output(self):
        for key,value in (('package',str(self.f.package.parent)+'/../ingress/'+self.f.package.name),
                          ('output',str(self.root/'outside')),('trusted_root',str(self.f.trusted)+'/')):
            with self.subTest(key=key):
                args=self.f.args();setattr(args,key,value);self.reject('PATH_UNSAFE',args)

    def test_ingress_may_not_overlap_trust_or_authority(self):
        args=self.f.args();args.package=str(self.f.trusted/'records'/'unit-trusted-record.json')
        self.reject('PATH_UNSAFE',args)

    def test_opt_in_and_root_before_any_write(self):
        args=self.f.args();args.opt_in=False;self.reject('INPUT_INVALID',args)
        with mock.patch.object(os,'geteuid',return_value=12345):self.reject('ROOT_REQUIRED')

    def test_flow_environment_is_not_a_local_authority(self):
        for key in ('PIPELINE_ID','BUILD_NUMBER','CYF_FLOW_GRADLE_ACTIVE'):
            with self.subTest(key=key),mock.patch.dict(os.environ,{key:'1'}):self.reject('INPUT_INVALID')

    def test_source_tamper_during_staging_fails_and_exact_stage_removed(self):
        original=m.OwnedStage.write
        def tamper(stage,name,data):
            result=original(stage,name,data)
            if name=='admission.json':self.f.package.write_bytes(self.f.package_data+b'TAMPER')
            return result
        with mock.patch.object(m.OwnedStage,'write',tamper):self.reject('DIGEST_MISMATCH')
        self.assertTrue(self.f.package.exists())
        self.assertTrue(self.f.auth_path.exists())

    def test_same_bytes_but_replaced_input_inode_fails(self):
        original=m.OwnedStage.write
        def tamper(stage,name,data):
            result=original(stage,name,data)
            if name=='admission.json':
                old=self.f.package.read_bytes();self.f.package.unlink();self.f.write(self.f.package,old)
            return result
        with mock.patch.object(m.OwnedStage,'write',tamper):self.reject('DIGEST_MISMATCH')

    def test_staged_bytes_tamper_is_not_published(self):
        original=m.OwnedStage.write
        def tamper(stage,name,data):
            result=original(stage,name,data)
            if name=='admission.json':
                fd=os.open('application.jar',os.O_WRONLY|os.O_TRUNC,dir_fd=stage.dirs['payload'])
                os.write(fd,b'UNIT-TAMPER');os.close(fd)
            return result
        with mock.patch.object(m.OwnedStage,'write',tamper):self.reject('DIGEST_MISMATCH')

    def test_no_overwrite_existing_output(self):
        self.run_admission();old=Path(self.f.args().output)/'admission.json';data=old.read_bytes()
        with self.assertRaises(m.Rejected) as e:self.run_admission()
        self.assertEqual(e.exception.code,'OUTPUT_EXISTS');self.assertEqual(old.read_bytes(),data)

    def test_atomic_publication_race_does_not_replace_foreign_directory(self):
        original=m.rename_no_replace
        def race(fd,old,new):
            os.mkdir(new,mode=0o700,dir_fd=fd)
            f=os.open(new,os.O_RDONLY|os.O_DIRECTORY,dir_fd=fd)
            try:
                child=os.open('foreign',os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600,dir_fd=f)
                os.write(child,b'foreign-synthetic');os.close(child)
            finally:os.close(f)
            return original(fd,old,new)
        with mock.patch.object(m,'rename_no_replace',race),self.assertRaises(m.Rejected) as e:self.run_admission()
        self.assertEqual(e.exception.code,'OUTPUT_EXISTS')
        output=Path(self.f.args().output)
        self.assertEqual((output/'foreign').read_bytes(),b'foreign-synthetic')
        self.assertEqual(list(output.parent.iterdir()),[output])

    def test_no_renameat2_fallback(self):
        with mock.patch.object(m.ctypes,'CDLL',return_value=object()):self.reject('IO_FAILURE')

    def test_publication_failure_cleanup_only_owned_stage(self):
        unrelated=self.f.trusted/'admitted'/'unrelated';unrelated.mkdir(mode=0o700)
        (unrelated/'sentinel').write_bytes(b'do-not-delete')
        with mock.patch.object(m,'rename_no_replace',side_effect=m.Rejected('IO_FAILURE')),self.assertRaises(m.Rejected):self.run_admission()
        self.assertEqual((unrelated/'sentinel').read_bytes(),b'do-not-delete')
        self.assertEqual(list(unrelated.parent.iterdir()),[unrelated])

    def test_prepublication_file_fsync_failure_removes_only_owned_stage(self):
        original = m.os.fsync
        failed = []
        def fail_once(fd):
            if not failed and stat.S_ISREG(os.fstat(fd).st_mode):
                failed.append(True)
                raise OSError('SYNTHETIC PRIVATE fsync detail')
            return original(fd)
        with mock.patch.object(m.os, 'fsync', fail_once), self.assertRaises(OSError):
            self.run_admission()
        self.assertTrue(failed)
        self.assertEqual(list((self.f.trusted / 'admitted').iterdir()), [])
        self.assertEqual(self.f.package.read_bytes(), self.f.package_data)
        self.assertTrue(self.f.auth_path.is_file())

    def test_foreign_staged_inode_is_never_deleted_or_published(self):
        original = m.OwnedStage.write
        # Simulate a root-side replacement; unprivileged producers cannot access
        # the protected stage. Never recursively erase an unrecognized inode.
        def replace(stage, name, data):
            result = original(stage, name, data)
            if name == 'admission.json':
                fd = stage.dirs['payload']
                os.rename('application.jar', 'foreign-retained', src_dir_fd=fd, dst_dir_fd=fd)
                leaf = os.open('application.jar', os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600, dir_fd=fd)
                with os.fdopen(leaf, 'wb') as handle:
                    handle.write(b'FOREIGN PRIVATE SYNTHETIC')
            return result
        with mock.patch.object(m.OwnedStage, 'write', replace), self.assertRaises(m.Rejected) as error:
            self.run_admission()
        self.assertEqual(error.exception.code, 'PATH_UNSAFE')
        self.assertFalse(Path(self.f.args().output).exists())
        stages = list((self.f.trusted / 'admitted').iterdir())
        self.assertEqual(len(stages), 1)
        self.assertTrue(stages[0].name.startswith('.admit-'))
        self.assertEqual((stages[0] / 'payload/application.jar').read_bytes(), b'FOREIGN PRIVATE SYNTHETIC')
        self.assertEqual((stages[0] / 'payload/foreign-retained').read_bytes(), self.f.jar)
        # Only TemporaryDirectory's exclusive unit root removes these materials.

    def test_post_publish_fsync_failure_not_reported_as_success_or_deleted(self):
        original=m.rename_no_replace
        def rename_then_fsync_fail(fd,old,new):
            result=original(fd,old,new)
            mock.patch.object(m.os,'fsync',side_effect=OSError('SYNTHETIC PRIVATE detail')).start()
            return result
        with mock.patch.object(m,'rename_no_replace',rename_then_fsync_fail),self.assertRaises(OSError):self.run_admission()
        self.assertTrue((Path(self.f.args().output)/'admission.json').is_file())

    def test_parser_describe_and_safe_failures_no_secret_or_paths(self):
        for argv in ([],['--opt-in'],['--describe','--opt-in'],['--password','SYNTHETIC PRIVATE']):
            out=io.StringIO()
            with contextlib.redirect_stdout(out):self.assertEqual(m.main(argv),1)
            self.assertEqual(json.loads(out.getvalue()),{'format':'cyf-api-local-admission-result-v1','status':'rejected','code':'INPUT_INVALID'})
            self.assertNotIn('SYNTHETIC PRIVATE',out.getvalue())
        with mock.patch.object(m,'admit',side_effect=OSError('SYNTHETIC PRIVATE SECRET')):
            args=self.f.args();argv=['--opt-in']
            for key,value in vars(args).items():
                if key!='opt_in':argv+=['--'+key.replace('_','-'),value]
            out=io.StringIO()
            with contextlib.redirect_stdout(out):self.assertEqual(m.main(argv),1)
            self.assertEqual(json.loads(out.getvalue())['code'],'IO_FAILURE')
            self.assertNotIn('SYNTHETIC PRIVATE',out.getvalue())
        with mock.patch.object(m,'admit',side_effect=AssertionError('must not run')):
            out=io.StringIO()
            with contextlib.redirect_stdout(out):self.assertEqual(m.main(['--describe']),0)
            self.assertIs(json.loads(out.getvalue())['productionAuthorized'],False)

    def test_unexpected_fault_is_safe_code_not_raw_traceback(self):
        args = self.f.args()
        argv = ['--opt-in']
        for key, value in vars(args).items():
            if key != 'opt_in':
                argv += ['--' + key.replace('_', '-'), value]
        with mock.patch.object(m, 'admit', side_effect=RuntimeError('SYNTHETIC SECRET /private/path')):
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                self.assertEqual(m.main(argv), 1)
        self.assertEqual(json.loads(out.getvalue()), {
            'format': 'cyf-api-local-admission-result-v1', 'status': 'rejected', 'code': 'IO_FAILURE'})
        self.assertNotIn('SYNTHETIC SECRET', out.getvalue())
        self.assertEqual(list((self.f.trusted / 'admitted').iterdir()), [])

    def test_repeated_and_abbreviated_cli_options_rejected(self):
        args=self.f.args();argv=['--opt-in']
        for k,v in vars(args).items():
            if k!='opt_in':argv+=['--'+k.replace('_','-'),v]
        with self.assertRaises(m.Rejected):m.parse(argv+['--package',args.package])
        abbreviated=argv[:];abbreviated[abbreviated.index('--package')]='--pack'
        with self.assertRaises(m.Rejected):m.parse(abbreviated)

    def test_wrapper_fixed_anchors_isolated_fd_exec_and_safe_describe(self):
        self.assertEqual(w.HELPER,'/usr/local/libexec/cyf-api-local/admit-api-local.py')
        self.assertEqual(w.TRUSTED_ROOT,'/var/lib/cyf-api-local-admission')
        self.assertEqual(w.AUTHORITY_ROOT,'/var/lib/cyf-api-local-authority')
        out=io.StringIO()
        with contextlib.redirect_stdout(out):self.assertEqual(w.main(['--describe']),0)
        self.assertFalse(json.loads(out.getvalue())['productionAuthorized'])
        args=self.f.args();argv=['--opt-in']
        for k in w.OPTIONS:argv+=['--'+k,getattr(args,k.replace('-','_'))]
        fd=os.open(self.f.auth_path,os.O_RDONLY)
        # Only exec interception: never execute an actual installed/root helper.
        with mock.patch.object(w,'__file__',w.SELF),mock.patch.object(w,'protected_file',side_effect=lambda path, **kwargs:os.dup(fd)),mock.patch.object(w.os,'execve',side_effect=RuntimeError('unit-exec-intercept')) as execute:
            with self.assertRaisesRegex(RuntimeError,'unit-exec-intercept'):w.main(argv)
        os.close(fd)
        python,command,env=execute.call_args[0]
        self.assertEqual(python,'/usr/bin/python3')
        self.assertEqual(command[:3],['/usr/bin/python3','-I','-B'])
        self.assertTrue(command[3].startswith('/proc/self/fd/'))
        self.assertEqual(env,{'PATH':'/usr/sbin:/usr/bin:/sbin:/bin','LC_ALL':'C'})
        self.assertIn(w.TRUSTED_ROOT,command);self.assertIn(w.AUTHORITY_ROOT,command)

    def test_wrapper_rejects_source_execution_unknown_flags_and_root_overrides(self):
        args=self.f.args();argv=['--opt-in']
        for k in w.OPTIONS:argv+=['--'+k,getattr(args,k.replace('-','_'))]
        for extra in ([],['--trusted-root','/synthetic'],['--helper','/synthetic'],['--install']):
            out=io.StringIO()
            with contextlib.redirect_stdout(out):self.assertEqual(w.main(argv+extra),1)
            self.assertEqual(json.loads(out.getvalue())['code'],'PATH_UNSAFE' if not extra else 'INPUT_INVALID')

    def test_wrapper_protected_file_rejects_mode_links_and_untrusted_ancestry(self):
        fd=w.protected_file(str(self.f.auth_path));os.close(fd)
        self.f.auth_path.chmod(0o666)
        with self.assertRaises(w.Refused):w.protected_file(str(self.f.auth_path))
        self.f.auth_path.chmod(0o600);self.root.chmod(0o777)
        with self.assertRaises(w.Refused):w.protected_file(str(self.f.auth_path))
        self.root.chmod(0o700)

    def test_wrapper_distro_interpreter_hardlinks_keep_helper_single_link_rule(self):
        interpreter=self.root/'synthetic-distro-python'
        interpreter.write_bytes(b'synthetic executable, never invoked')
        interpreter.chmod(0o755)
        alias=self.root/'synthetic-distro-python-m'
        os.link(str(interpreter),str(alias))
        self.assertEqual(interpreter.stat().st_nlink,2)
        with self.assertRaises(w.Refused):w.protected_file(str(interpreter))
        fd=w.protected_file(str(interpreter),interpreter=True);os.close(fd)
        interpreter.chmod(0o775)
        with self.assertRaises(w.Refused):w.protected_file(str(interpreter),interpreter=True)
        interpreter.chmod(0o644)
        with self.assertRaises(w.Refused):w.protected_file(str(interpreter),interpreter=True)
        interpreter.chmod(0o755)
        self.root.chmod(0o777)
        with self.assertRaises(w.Refused):w.protected_file(str(interpreter),interpreter=True)
        self.root.chmod(0o700)

    def test_owned_source_only_and_no_original_mutation_or_commands(self):
        for path in (HELPER,WRAPPER):ast.parse(path.read_text())
        source=HELPER.read_text()
        self.assertNotIn('subprocess',source)
        self.assertNotIn('flock(',source)
        self.assertNotIn('importlib',source)
        self.assertNotIn('CYF_RELEASE_OFFLINE_TEST',source)
        self.assertNotIn('os.replace(',source)
        # Read-only producer still contains its original format/pin/fresh binding.
        self.assertIn('cyf-api-local-release-receipt-v1',PRODUCER.read_text())
        self.assertIn(m.OPENCV_SHA,PRODUCER.read_text())


class PublishedVerificationTest(unittest.TestCase):
    """Private synthetic copies only; no installed helper or real batch authority."""
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='.ur05-published-private-', dir=str(Path.home()))
        self.root = Path(self.temp.name)
        self.addCleanup(self.temp.cleanup)
        self.f = Fixture(self.root)
        self.addCleanup(mock.patch.stopall)
        mock.patch.dict(os.environ, {'PIPELINE_ID': '', 'BUILD_NUMBER': '', 'CYF_FLOW_GRADLE_ACTIVE': ''}).start()
        with self.f.pins():
            result = m.admit(self.f.args())
        self.admission = Path(result['admission']['path'])
        self.output = self.admission.parent
        self.admitted = json.loads(self.admission.read_bytes())
        self.pinned_sha = result['admission']['sha256']

    def args(self):
        return argparse.Namespace(verify_published=True, trusted_root=str(self.f.trusted),
                                  admission=str(self.admission), admission_sha256=self.pinned_sha)

    def argv(self, args=None):
        args = args or self.args()
        return ['--verify-published', '--trusted-root', args.trusted_root,
                '--admission', args.admission, '--admission-sha256', args.admission_sha256]

    def rebind_admitted(self):
        self.f.write(self.admission, m.canonical(self.admitted))
        # A synthetic caller deliberately supplies the new pin, to prove that
        # projection claims alone cannot bypass ORIGINAL raw trust checks.
        self.pinned_sha = m.sha(self.admission.read_bytes())

    def copied_json(self, ref, change):
        path = Path(ref['path'])
        obj = json.loads(path.read_bytes())
        change(obj)
        data = m.canonical(obj)
        self.f.write(path, data)
        ref.update(m.binding(data))
        self.rebind_admitted()
        return obj

    def raw_record_change(self, change):
        ref = self.admitted['authority']['trustedRecord']
        record = self.copied_json(ref, change)
        self.copied_json(self.admitted['authority']['batchAuthority'],
                         lambda auth: auth.update(trustedRecordSha256=ref['sha256']))
        return record

    def inventory(self):
        # Omit atime: reads may update it. Observe bytes/inodes/modes/mtime/ctime,
        # not just a self-reported no-write flag. Only this unit's exclusive root.
        result = {}
        for path in [self.root] + sorted(self.root.rglob('*')):
            s = path.lstat()
            result[str(path.relative_to(self.root))] = (
                s.st_dev, s.st_ino, s.st_uid, s.st_gid, s.st_mode, s.st_nlink,
                s.st_size, s.st_mtime_ns, s.st_ctime_ns,
                m.sha(path.read_bytes()) if stat.S_ISREG(s.st_mode) else None)
        return result

    def verify(self, args=None):
        with self.f.pins():
            return m.verify_published(args or self.args())

    def reject(self, code=None, argv=None):
        before = self.inventory()
        out = io.StringIO()
        with self.f.pins(), contextlib.redirect_stdout(out):
            self.assertEqual(m.main(argv or self.argv()), 1)
        response = json.loads(out.getvalue())
        self.assertEqual(response['format'], 'cyf-api-local-published-verification-v1')
        self.assertEqual(response['status'], 'rejected')
        self.assertEqual(set(response), {'format', 'status', 'code'})
        self.assertIn(response['code'], m.SAFE_CODES)
        if code:
            self.assertEqual(response['code'], code)
        self.assertEqual(self.inventory(), before)
        self.assertNotIn(str(self.root), out.getvalue())
        self.assertFalse(any(p.name.startswith('.admit-') for p in self.output.parent.iterdir()))
        return response

    def test_original_paths_deleted_success_without_external_reads(self):
        import shutil
        for path in (self.f.authority, self.f.ingress,
                     self.f.trusted / 'proofs', self.f.trusted / 'records'):
            shutil.rmtree(str(path))  # ONLY this unit's synthetic original paths
        original_read = m.StableReader.read
        reads = []
        def copied_read(reader, path, anchor=None):
            path = Path(path)
            self.assertIn(self.output, path.parents)
            reads.append(path)
            return original_read(reader, path, anchor)
        before = self.inventory()
        with mock.patch.object(m.StableReader, 'read', copied_read):
            result = self.verify()
        self.assertEqual(result, {
            'format': 'cyf-api-local-published-verification-v1', 'status': 'verified',
            'scope': 'artifact-admission-only', 'productionAuthorized': False,
            'admission': {'path': str(self.admission), **m.binding(self.admission.read_bytes())},
            'source': {'kind': 'local-build-v1', 'identity': self.f.ident}})
        self.assertTrue(reads)
        self.assertEqual(self.inventory(), before)

    def test_readonly_open_flags_no_umask_publish_or_state_mutation(self):
        original_open = m.os.open
        def readonly_open(path, flags, *args, **kwargs):
            self.assertFalse(flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND))
            return original_open(path, flags, *args, **kwargs)
        before = self.inventory()
        out = io.StringIO()
        with self.f.pins(), mock.patch.object(m.os, 'open', readonly_open), \
                mock.patch.object(m.os, 'umask', side_effect=AssertionError('verifier must not set umask')), \
                mock.patch.object(m, 'admit', side_effect=AssertionError('not ingress admission')), \
                mock.patch.object(m, 'publish', side_effect=AssertionError('must not publish')), \
                mock.patch.object(m, 'OwnedStage', side_effect=AssertionError('must not stage')), \
                contextlib.redirect_stdout(out):
            self.assertEqual(m.main(self.argv()), 0)
        response = json.loads(out.getvalue())
        self.assertFalse(response['productionAuthorized'])
        self.assertNotIn('installAllowed', response)
        self.assertEqual(m.canonical(response).decode(), out.getvalue())
        self.assertEqual(self.inventory(), before)

    def test_admission_tamper_and_external_pin_mismatch(self):
        self.f.write(self.admission, self.admission.read_bytes() + b' ')
        self.reject('DIGEST_MISMATCH')
        args = self.args()
        args.admission_sha256 = '0' * 64
        self.reject('DIGEST_MISMATCH', self.argv(args))

    def test_every_copied_authority_package_payload_and_evidence_tamper(self):
        refs = [self.admitted['authority'][k] for k in ('batchAuthority', 'trustedRecord', 'verificationRecord')]
        refs += [self.admitted['package']] + list(self.admitted['payloads'].values())
        refs += [s['file'] for s in self.admitted['evidence']['snapshots']]
        for ref in refs:
            with self.subTest(path=ref['path']):
                path = Path(ref['path'])
                original = path.read_bytes()
                self.f.write(path, original + b' UNIT TAMPER')
                self.reject()
                self.f.write(path, original)

    def test_raw_authority_projection_mismatch(self):
        for key in ('authorityId', 'batchId'):
            with self.subTest(key=key):
                old = self.admitted['authority'][key]
                self.admitted['authority'][key] = 'foreign-projection'
                self.rebind_admitted()
                self.reject('AUTHORITY_INVALID')
                self.admitted['authority'][key] = old
                self.rebind_admitted()

    def test_raw_authority_pins_controller_bytes_not_projected_file_digest(self):
        ref = self.admitted['authority']['verificationRecord']
        path = Path(ref['path'])
        self.f.write(path, path.read_bytes() + b' ')
        ref.update(m.binding(path.read_bytes()))
        self.rebind_admitted()
        self.reject('AUTHORITY_INVALID')

    def test_raw_authority_pins_original_trusted_record_bytes(self):
        self.copied_json(self.admitted['authority']['trustedRecord'],
                         lambda record: record['identity'].update(buildId='foreign'))
        self.reject('AUTHORITY_INVALID')

    def test_identity_projection_all_four_fields_failclosed(self):
        for key, value in (('version', 'foreign'), ('buildId', 'foreign'),
                           ('commit', '0' * 40), ('tree', '0' * 40)):
            with self.subTest(key=key):
                old = self.admitted['source']['identity'][key]
                self.admitted['source']['identity'][key] = value
                self.rebind_admitted()
                self.reject('IDENTITY_MISMATCH')
                self.admitted['source']['identity'][key] = old
                self.rebind_admitted()

    def test_kind_scope_status_production_flag_and_extra_authority_fail(self):
        pristine = copy.deepcopy(self.admitted)
        for field, value in (('scope', 'install'), ('status', 'verified'),
                             ('productionAuthorized', True), ('productionAuthorized', 0)):
            with self.subTest(field=field, value=value):
                self.admitted = copy.deepcopy(pristine)
                self.admitted[field] = value
                self.rebind_admitted()
                self.reject('AUTHORITY_INVALID')
        self.admitted = copy.deepcopy(pristine)
        self.admitted['source']['kind'] = 'flow-build-v1'
        self.rebind_admitted()
        self.reject('IDENTITY_MISMATCH')
        self.admitted = copy.deepcopy(pristine)
        self.admitted['installAllowed'] = True
        self.rebind_admitted()
        self.reject('EVIDENCE_INVALID')

    def test_producer_receipt_cannot_replace_independent_authority(self):
        ref = self.admitted['authority']['batchAuthority']
        self.f.write(Path(ref['path']), self.f.payloads['receipt.json'])
        ref.update(m.binding(self.f.payloads['receipt.json']))
        self.rebind_admitted()
        self.reject('AUTHORITY_INVALID')

    def test_missing_independent_controller_observation_despite_consistent_producer(self):
        ref = self.admitted['authority']['verificationRecord']
        self.copied_json(ref, lambda verification: verification['observations'].update(freshBootJar=False))
        self.copied_json(self.admitted['authority']['batchAuthority'],
                         lambda auth: auth['verificationRecord'].update(sha256=ref['sha256'], size=ref['size']))
        self.reject('AUTHORITY_INVALID')

    def test_install_precondition_projection_mismatch(self):
        self.admitted['installPrecondition']['canonicalJarSha256'] = '0' * 64
        self.rebind_admitted()
        self.reject('EVIDENCE_INVALID')

    def test_missing_extra_payload_refs_and_actual_members(self):
        original = copy.deepcopy(self.admitted)
        del self.admitted['payloads']['receipt.json']
        self.rebind_admitted()
        self.reject('PACKAGE_INVALID')
        self.admitted = copy.deepcopy(original)
        self.admitted['payloads']['extra'] = dict(original['payloads']['receipt.json'])
        self.rebind_admitted()
        self.reject('PACKAGE_INVALID')
        self.admitted = copy.deepcopy(original)
        ref = self.admitted['package']
        item = tarfile.TarInfo('unexpected')
        item.size = 1
        data = self.f.archive(extra=(item, b'x'))
        self.f.write(Path(ref['path']), data)
        ref.update(m.binding(data))
        self.raw_record_change(lambda record: record.update(package=m.binding(data)))
        # Independently synthetic verifier record is also rebound to isolate the
        # archive member guard. It never grants real execution authorization.
        vref = self.admitted['authority']['verificationRecord']
        self.copied_json(vref, lambda v: v.update(package=m.binding(data)))
        self.copied_json(self.admitted['authority']['batchAuthority'],
                         lambda a: a['verificationRecord'].update(sha256=vref['sha256'], size=vref['size']))
        self.reject('PACKAGE_INVALID')

    def test_duplicate_missing_extra_or_reordered_snapshot_refs(self):
        pristine = copy.deepcopy(self.admitted)
        original = pristine['evidence']['snapshots']
        variants = [original[:-1], original + [original[0]],
                    [original[0], original[0]] + original[2:], list(reversed(original))]
        for snapshots in variants:
            with self.subTest(count=len(snapshots)):
                self.admitted = copy.deepcopy(pristine)
                self.admitted['evidence']['snapshots'] = copy.deepcopy(snapshots)
                self.rebind_admitted()
                self.reject('EVIDENCE_INVALID')

    def test_raw_proof_identity_bijection_rejects_duplicate_logical_files(self):
        self.raw_record_change(lambda r: r['snapshots'][1].update(file=dict(r['snapshots'][0]['file'])))
        snapshot = self.admitted['evidence']['snapshots'][1]
        data = Path(self.admitted['evidence']['snapshots'][0]['file']['path']).read_bytes()
        self.f.write(Path(snapshot['file']['path']), data)
        snapshot['file'].update(m.binding(data))
        self.rebind_admitted()
        self.reject('EVIDENCE_INVALID')

    def test_missing_raw_proof_closure_cannot_pass_projection_only(self):
        self.raw_record_change(lambda r: r['snapshots'].pop())
        self.admitted['evidence']['snapshots'].pop()
        self.rebind_admitted()
        self.reject('EVIDENCE_INVALID')

    def test_changed_original_path_role_or_build_evidence_projection(self):
        pristine = copy.deepcopy(self.admitted)
        for key, value in (('originalPath', '/synthetic/unknown'), ('role', 'unknown')):
            with self.subTest(key=key):
                self.admitted = copy.deepcopy(pristine)
                self.admitted['evidence']['snapshots'][0][key] = value
                self.rebind_admitted()
                self.reject('EVIDENCE_INVALID')
        self.admitted = copy.deepcopy(pristine)
        self.admitted['evidence']['buildEvidence'] = dict(self.admitted['payloads']['receipt.json'])
        self.rebind_admitted()
        self.reject('EVIDENCE_INVALID')

    def test_exact_published_inventory_rejects_extra_file_or_directory(self):
        for relative in ('foreign', 'authority/foreign', 'evidence/foreign'):
            with self.subTest(relative=relative):
                path = self.output / relative
                self.f.write(path, b'FOREIGN PRIVATE SYNTHETIC')
                self.reject('EVIDENCE_INVALID')
                path.unlink()
        directory = self.output / 'foreign-dir'
        directory.mkdir(mode=0o700)
        self.reject('EVIDENCE_INVALID')

    def test_projection_cannot_reference_original_or_outside_or_wrong_copied_path(self):
        pristine = copy.deepcopy(self.admitted)
        for value in (str(self.f.package), str(self.f.record_path),
                      str(self.output / 'payload/receipt.json'), str(self.output / 'payload/../package.tgz')):
            with self.subTest(value=value):
                self.admitted = copy.deepcopy(pristine)
                self.admitted['package']['path'] = value
                self.rebind_admitted()
                self.reject('PATH_UNSAFE')

    def test_symlink_leaf_or_component_and_hardlink_rejected(self):
        package = Path(self.admitted['package']['path'])
        data = package.read_bytes()
        package.unlink()
        package.symlink_to(self.f.package)
        self.reject()
        package.unlink()
        self.f.write(package, data)
        link = self.root / 'unit-only-hardlink'
        os.link(package, link)
        self.reject('PATH_UNSAFE')
        link.unlink()
        authority = self.output / 'authority'
        moved = self.output / 'private-moved-authority'
        authority.rename(moved)
        authority.symlink_to(moved, target_is_directory=True)
        self.reject()

    def test_unsafe_file_owner_mode_and_protected_directory_mode(self):
        file = Path(self.admitted['authority']['batchAuthority']['path'])
        file.chmod(0o644)
        self.reject('PATH_UNSAFE')
        file.chmod(0o600)
        os.chown(file, 12345, 12345)
        try:
            self.reject('PATH_UNSAFE')
        finally:
            os.chown(file, 0, 0)
        for directory in (self.root, self.output, self.output / 'evidence'):
            with self.subTest(directory=directory):
                directory.chmod(0o777)
                self.reject('PATH_UNSAFE')
                directory.chmod(0o700)

    def test_required_admission_location_and_noncanonical_cli_paths(self):
        for key, value in (('admission', str(self.f.record_path)),
                           ('trusted_root', str(self.f.trusted) + '/'),
                           ('admission', str(self.output) + '/../' + self.output.name + '/admission.json')):
            with self.subTest(key=key):
                args = self.args()
                setattr(args, key, value)
                self.reject('PATH_UNSAFE', self.argv(args))

    def test_strict_admitted_json_types_duplicate_keys_and_nonfinite(self):
        original = self.admission.read_bytes()
        for raw in (original[:-2] + b',"status":"admitted"}\n', b'{"x":NaN}', b'{"x":1e9999}'):
            with self.subTest(raw=raw[:16]):
                self.f.write(self.admission, raw)
                self.pinned_sha = m.sha(raw)
                self.reject('EVIDENCE_INVALID')
        self.admitted['package']['size'] = True
        self.rebind_admitted()
        self.reject('DIGEST_MISMATCH')

    def test_root_and_flow_input_guard_before_reads(self):
        with mock.patch.object(m.os, 'geteuid', return_value=12345), \
                mock.patch.object(m.StableReader, 'read', side_effect=AssertionError('must not read')):
            self.reject('ROOT_REQUIRED')
        with mock.patch.dict(os.environ, {'CYF_FLOW_GRADLE_ACTIVE': 'fake'}), \
                mock.patch.object(m.StableReader, 'read', side_effect=AssertionError('must not read')):
            self.reject('INPUT_INVALID')

    def test_malformed_cli_no_automatic_mode_fallback_and_safe_failure(self):
        variants = [self.argv() + ['--opt-in'], self.argv() + ['--install'],
                    self.argv() + ['--admission', str(self.admission)],
                    ['--verify-published'], ['--verify-published=1'] + self.argv()[1:],
                    ['--verify-published', '--describe'],
                    ['--verify-published', '--trusted-ro', str(self.f.trusted),
                     '--admission', str(self.admission), '--admission-sha256', self.pinned_sha]]
        for argv in variants:
            with self.subTest(argv=argv), mock.patch.object(m, 'admit', side_effect=AssertionError('no mode fallback')):
                self.reject('INPUT_INVALID', argv)
        with mock.patch.object(m, 'verify_published', side_effect=RuntimeError('SYNTHETIC SECRET /private/path')):
            result = self.reject('IO_FAILURE')
        self.assertEqual(set(result), {'format', 'status', 'code'})

    def test_final_recheck_detects_copied_tamper_without_cleanup_or_publish(self):
        original = m.CopiedProofReader.checked
        touched = []
        def tamper(reader, ref, anchor, code='DIGEST_MISMATCH'):
            result = original(reader, ref, anchor, code)
            if not touched:
                touched.append(True)
                package = Path(self.admitted['package']['path'])
                self.f.write(package, package.read_bytes() + b'PEER TAMPER')
            return result
        out = io.StringIO()
        with self.f.pins(), mock.patch.object(m.CopiedProofReader, 'checked', tamper), contextlib.redirect_stdout(out):
            self.assertEqual(m.main(self.argv()), 1)
        self.assertEqual(json.loads(out.getvalue())['code'], 'DIGEST_MISMATCH')
        self.assertTrue(self.admission.exists())
        self.assertFalse(any(p.name.startswith('.admit-') for p in self.output.parent.iterdir()))

    def test_final_inventory_detects_peer_extra_member(self):
        original = m.StableReader.recheck
        def extra_member(reader):
            result = original(reader)
            self.f.write(self.output / 'PEER-EXTRA', b'PRIVATE SYNTHETIC')
            return result
        out = io.StringIO()
        with self.f.pins(), mock.patch.object(m.StableReader, 'recheck', extra_member), contextlib.redirect_stdout(out):
            self.assertEqual(m.main(self.argv()), 1)
        self.assertEqual(json.loads(out.getvalue())['code'], 'EVIDENCE_INVALID')
        self.assertTrue((self.output / 'PEER-EXTRA').is_file())

    def test_describe_preserves_old_fields_and_only_adds_explicit_verifier(self):
        value = m.describe()
        self.assertEqual(value['format'], 'cyf-api-local-admission-interface-v1')
        self.assertEqual(value['result'], 'cyf-api-local-admission-result-v1')
        self.assertFalse(value['productionAuthorized'])
        self.assertEqual(value['publishedVerifier'], {
            'mode': '--verify-published',
            'flags': ['--verify-published', '--trusted-root', '--admission', '--admission-sha256'],
            'result': 'cyf-api-local-published-verification-v1', 'readOnly': True})
        # The remapping adapter has no filesystem capability, even a test-only one.
        node = next(n for n in ast.parse(HELPER.read_text()).body if isinstance(n, ast.ClassDef) and n.name == 'CopiedProofReader')
        self.assertFalse(any(isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and
                             n.func.attr in ('open', 'read_bytes', 'stat', 'resolve') for n in ast.walk(node)))


if __name__=='__main__':
    unittest.main(verbosity=2)
