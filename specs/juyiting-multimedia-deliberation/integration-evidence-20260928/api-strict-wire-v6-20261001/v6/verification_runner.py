#!/usr/bin/env python3
from __future__ import print_function

import datetime
import hashlib
import json
import os
import pathlib
import shutil
import socket
import stat
import subprocess
import sys
import threading
import time
import traceback
import xml.etree.ElementTree as ET

EVIDENCE = pathlib.Path('/var/tmp/cyf-mmd-api-a213-normal-terra-verification-v6-20261001')
PLAN_PATH = EVIDENCE / 'verification-plan.json'
BINDINGS_PATH = EVIDENCE / 'preexec-bindings.json'


def now():
    return datetime.datetime.now().astimezone().isoformat()


def sha256(path):
    h = hashlib.sha256()
    with pathlib.Path(path).open('rb') as handle:
        while True:
            block = handle.read(1024 * 1024)
            if not block:
                break
            h.update(block)
    return h.hexdigest()


def write_json(path, value):
    pathlib.Path(path).write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


def process_start_ticks(pid):
    raw = pathlib.Path('/proc/{}/stat'.format(pid)).read_text()
    tail = raw[raw.rfind(')') + 2:].split()
    return tail[19]


def process_cmdline(pid):
    return pathlib.Path('/proc/{}/cmdline'.format(pid)).read_bytes().replace(b'\0', b' ').decode('utf-8')


def git_value(worktree, *args):
    return subprocess.check_output(['git'] + list(args), cwd=worktree,
                                   universal_newlines=True).strip()


class VerificationFailure(Exception):
    def __init__(self, category, message, details=None):
        Exception.__init__(self, message)
        self.category = category
        self.details = details or {}


class OwnedTcpUnixAdapter(object):
    def __init__(self, host, port, unix_socket):
        self.host = host
        self.port = port
        self.unix_socket = unix_socket
        self.listener = None
        self.stop_event = threading.Event()
        self.accept_thread = None
        self.connection_threads = []
        self.connection_lock = threading.Lock()
        self.errors = []
        self.accepted_connections = 0

    def start(self):
        probe = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        probe.settimeout(0.25)
        try:
            result = probe.connect_ex((self.host, self.port))
        finally:
            probe.close()
        if result == 0:
            raise VerificationFailure('adapter_port_occupied',
                                      'TCP endpoint is already accepting connections; no takeover allowed',
                                      {'endpoint': '{}:{}'.format(self.host, self.port)})
        mode = os.stat(self.unix_socket).st_mode
        if not stat.S_ISSOCK(mode):
            raise VerificationFailure('adapter_unix_target_invalid',
                                      'Authorized Unix target is not a socket',
                                      {'unix_socket': self.unix_socket})
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Deliberately do not set SO_REUSEADDR or SO_REUSEPORT.
        try:
            listener.bind((self.host, self.port))
            listener.listen(32)
            listener.settimeout(0.5)
        except Exception:
            listener.close()
            raise
        self.listener = listener
        self.accept_thread = threading.Thread(target=self._accept_loop,
                                              name='cyf-owned-mysql-tcp-adapter-accept')
        self.accept_thread.daemon = False
        self.accept_thread.start()

    def _accept_loop(self):
        while not self.stop_event.is_set():
            try:
                client, address = self.listener.accept()
            except socket.timeout:
                continue
            except OSError:
                if self.stop_event.is_set():
                    return
                self.errors.append({'at': now(), 'stage': 'accept', 'trace': traceback.format_exc()})
                return
            self.accepted_connections += 1
            worker = threading.Thread(target=self._handle_connection, args=(client, address),
                                      name='cyf-owned-mysql-tcp-adapter-connection-{}'.format(
                                          self.accepted_connections))
            worker.daemon = False
            with self.connection_lock:
                self.connection_threads.append(worker)
            worker.start()

    def _pump(self, source, target):
        try:
            while True:
                data = source.recv(65536)
                if not data:
                    try:
                        target.shutdown(socket.SHUT_WR)
                    except OSError:
                        pass
                    return
                target.sendall(data)
        except OSError:
            return

    def _handle_connection(self, client, address):
        upstream = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        try:
            upstream.connect(self.unix_socket)
            forward = threading.Thread(target=self._pump, args=(client, upstream),
                                       name='cyf-owned-mysql-tcp-adapter-c2u')
            reverse = threading.Thread(target=self._pump, args=(upstream, client),
                                       name='cyf-owned-mysql-tcp-adapter-u2c')
            forward.daemon = False
            reverse.daemon = False
            forward.start()
            reverse.start()
            forward.join()
            reverse.join()
        except Exception:
            self.errors.append({'at': now(), 'stage': 'connection', 'peer': repr(address),
                                'trace': traceback.format_exc()})
        finally:
            try:
                client.close()
            except Exception:
                pass
            try:
                upstream.close()
            except Exception:
                pass

    def receipt(self):
        listener_open = self.listener is not None and self.listener.fileno() >= 0
        reuse_addr = None
        reuse_port = None
        if listener_open:
            reuse_addr = self.listener.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR)
            if hasattr(socket, 'SO_REUSEPORT'):
                reuse_port = self.listener.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT)
        return {
            'runner_pid': os.getpid(),
            'runner_start_ticks': process_start_ticks(os.getpid()),
            'listener': '{}:{}'.format(self.host, self.port),
            'listener_open': listener_open,
            'unix_target': self.unix_socket,
            'so_reuseaddr': reuse_addr,
            'so_reuseport': reuse_port,
            'accept_thread_name': self.accept_thread.name if self.accept_thread else None,
            'accept_thread_daemon': self.accept_thread.daemon if self.accept_thread else None,
            'accepted_connections': self.accepted_connections,
            'errors': list(self.errors),
        }

    def stop(self):
        self.stop_event.set()
        if self.listener is not None:
            try:
                self.listener.close()
            except Exception:
                pass
        if self.accept_thread is not None:
            self.accept_thread.join(3.0)
        with self.connection_lock:
            workers = list(self.connection_threads)
        for worker in workers:
            worker.join(3.0)


def run_mysql(plan, protocol, prefixes, raw_path):
    query = ('SELECT @@version,@@server_uuid,@@datadir,@@port,CURRENT_USER(),USER(); '
             "SELECT SCHEMA_NAME FROM information_schema.SCHEMATA WHERE SCHEMA_NAME REGEXP '^({})';"
             .format('|'.join(prefixes)))
    if protocol == 'SOCKET':
        command = ['mysql', '--protocol=SOCKET', '--socket=' + plan['mysql']['socket'], '-uroot']
    elif protocol == 'TCP':
        command = ['mysql', '--protocol=TCP', '-h127.0.0.1', '-P46139', '-uroot']
    else:
        raise ValueError(protocol)
    command += ['--batch', '--raw', '--skip-column-names', '-e', query]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                               universal_newlines=True)
    output, unused = process.communicate()
    pathlib.Path(raw_path).write_text(output)
    if process.returncode != 0:
        raise VerificationFailure('mysql_identity_preflight',
                                  '{} MySQL identity query failed'.format(protocol),
                                  {'returncode': process.returncode, 'raw': str(raw_path),
                                   'raw_sha256': sha256(raw_path)})
    lines = output.splitlines()
    if not lines:
        raise VerificationFailure('mysql_identity_preflight', 'MySQL identity query returned no rows')
    fields = lines[0].split('\t')
    if len(fields) != 6:
        raise VerificationFailure('mysql_identity_preflight', 'Unexpected identity field count',
                                  {'fields': fields})
    identity = {'version': fields[0], 'uuid': fields[1], 'datadir': fields[2],
                'reported_server_port': fields[3], 'current_user': fields[4], 'user': fields[5]}
    expected = plan['mysql']['expected_identity']
    for key in ['version', 'uuid', 'datadir']:
        if identity[key] != expected[key]:
            raise VerificationFailure('mysql_identity_mismatch',
                                      '{} identity mismatch for {}'.format(protocol, key),
                                      {'actual': identity, 'expected': expected})
    schemas = lines[1:]
    return {'at_actual_system_clock': now(), 'protocol': protocol, 'identity': identity,
            'matching_schemas': schemas, 'prefixes': prefixes, 'raw': str(raw_path),
            'raw_sha256': sha256(raw_path)}


def verify_mysqld_process(plan):
    expected = plan['mysql']['owned_mysqld']
    pid = int(expected['pid'])
    actual = {'pid': pid, 'start_ticks': process_start_ticks(pid),
              'cmdline': process_cmdline(pid)}
    if actual['start_ticks'] != expected['start_ticks'] or actual['cmdline'] != expected['cmdline']:
        raise VerificationFailure('owned_mysqld_identity_mismatch',
                                  'Owned mysqld process identity changed; no process control attempted',
                                  {'actual': actual, 'expected': expected})
    socket_stat = os.stat(plan['mysql']['socket'])
    if not stat.S_ISSOCK(socket_stat.st_mode):
        raise VerificationFailure('owned_mysqld_socket_missing', 'Owned Unix socket is unavailable')
    actual['socket_inode'] = socket_stat.st_ino
    actual['socket_mode'] = oct(stat.S_IMODE(socket_stat.st_mode))
    return actual


def verify_stable_inputs(plan, bindings, phase, adapter):
    worktree = plan['candidate']['worktree']
    actual = {
        'at_actual_system_clock': now(),
        'phase': phase['name'],
        'head': git_value(worktree, 'rev-parse', 'HEAD'),
        'tree': git_value(worktree, 'rev-parse', 'HEAD^{tree}'),
        'status_porcelain': git_value(worktree, 'status', '--porcelain'),
        'init_sha256': sha256(plan['normal_graph']['init']),
        'runner_sha256': sha256(__file__),
        'fixtures': {name: sha256(value['path']) for name, value in plan['fixtures'].items()},
        'phase_inputs_sha256': sha256(phase['inputs_path']),
        'phase_argv_sha256': sha256(phase['argv_path']),
        'phase_matrix_sha256': sha256(phase['matrix_path']),
        'owned_mysqld': verify_mysqld_process(plan),
        'adapter': adapter.receipt(),
    }
    expected_phase = bindings['phases'][phase['name']]
    checks = [
        actual['head'] == plan['candidate']['commit'],
        actual['tree'] == plan['candidate']['tree'],
        actual['status_porcelain'] == '',
        actual['init_sha256'] == plan['normal_graph']['sha256'],
        actual['runner_sha256'] == plan['runner_script_sha256'],
        actual['phase_inputs_sha256'] == expected_phase['inputs_sha256'],
        actual['phase_argv_sha256'] == expected_phase['argv_sha256'],
        actual['phase_matrix_sha256'] == expected_phase['matrix_sha256'],
    ]
    for name, value in plan['fixtures'].items():
        checks.append(actual['fixtures'][name] == value['sha256'])
    if adapter.errors:
        checks.append(False)
    actual['result'] = 'PASS' if all(checks) else 'FAIL'
    write_json(EVIDENCE / (phase['name'] + '-stable-input.json'), actual)
    if actual['result'] != 'PASS':
        raise VerificationFailure('stable_input_drift',
                                  'Stable verification input changed before {}'.format(phase['name']), actual)


def run_gradle_phase(plan, phase):
    argv_record = json.loads(pathlib.Path(phase['argv_path']).read_text())
    command = argv_record['orchestrator_argv']
    environment = os.environ.copy()
    environment.update(argv_record['environment'])
    environment['JAVA_TOOL_OPTIONS'] = plan['java_tool_options']
    start_epoch = time.time()
    start = {'phase': phase['name'], 'at_actual_system_clock': now(),
             'start_epoch': start_epoch, 'command': command,
             'environment_names': sorted(argv_record['environment'].keys()),
             'java_tool_options': plan['java_tool_options']}
    write_json(EVIDENCE / (phase['name'] + '-start.json'), start)
    raw_path = pathlib.Path(phase['raw_artifact'])
    with raw_path.open('w') as raw:
        process = subprocess.Popen(command, cwd=plan['candidate']['worktree'], env=environment,
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                   universal_newlines=True, bufsize=1)
        for line in iter(process.stdout.readline, ''):
            sys.stdout.write(line)
            sys.stdout.flush()
            raw.write(line)
            raw.flush()
        process.stdout.close()
        returncode = process.wait()
    return returncode, start_epoch


def collect_fresh_xml(phase, start_epoch):
    destination = pathlib.Path(phase['xml_destination'])
    destination.mkdir(parents=True, exist_ok=True)
    actual_classes = set()
    stale = []
    copied = []
    counts = {'tests': 0, 'failures': 0, 'errors': 0, 'skipped': 0}
    per_file = []
    for directory in phase['result_dirs']:
        result_dir = pathlib.Path(directory)
        for source in sorted(result_dir.glob('TEST-*.xml')) if result_dir.exists() else []:
            class_name = source.name[len('TEST-'):-len('.xml')]
            if source.stat().st_mtime + 0.001 < start_epoch:
                stale.append({'path': str(source), 'mtime': source.stat().st_mtime})
                continue
            actual_classes.add(class_name)
            target = destination / source.name
            shutil.copy2(str(source), str(target))
            root = ET.parse(str(source)).getroot()
            values = {key: int(root.attrib.get(key, '0')) for key in counts.keys()}
            for key in counts.keys():
                counts[key] += values[key]
            record = {'class_name': class_name, 'source': str(source), 'copy': str(target),
                      'source_mtime': source.stat().st_mtime, 'sha256': sha256(target)}
            record.update(values)
            per_file.append(record)
            copied.append(str(target))
    expected = set(phase['expected_classes'])
    summary = {'at_actual_system_clock': now(), 'phase': phase['name'], 'counts': counts,
               'expected_classes': sorted(expected), 'actual_fresh_classes': sorted(actual_classes),
               'missing_classes': sorted(expected - actual_classes),
               'unexpected_classes': sorted(actual_classes - expected),
               'stale_ignored': stale, 'files': per_file, 'copied': copied}
    summary['result'] = ('PASS' if actual_classes == expected and counts['failures'] == 0
                         and counts['errors'] == 0 and counts['skipped'] == 0 else 'FAIL')
    write_json(EVIDENCE / (phase['name'] + '-fresh-xml.json'), summary)
    return summary


def collect_class_provenance(plan, phase):
    records = []
    missing = []
    for class_name in phase['expected_classes']:
        relative = pathlib.Path(*class_name.split('.'))
        sources = []
        classes = []
        for root in phase['source_roots']:
            candidate = pathlib.Path(root) / relative.with_suffix('.java')
            if candidate.is_file():
                sources.append({'path': str(candidate), 'sha256': sha256(candidate), 'mtime': candidate.stat().st_mtime})
        for root in phase['class_roots']:
            candidate = pathlib.Path(root) / relative.with_suffix('.class')
            if candidate.is_file():
                classes.append({'path': str(candidate), 'sha256': sha256(candidate), 'mtime': candidate.stat().st_mtime})
        if len(sources) != 1 or len(classes) != 1:
            missing.append({'class_name': class_name, 'source_matches': len(sources), 'class_matches': len(classes)})
        records.append({'class_name': class_name, 'sources': sources, 'classes': classes})
    result = {'at_actual_system_clock': now(), 'phase': phase['name'], 'records': records, 'missing_or_ambiguous': missing, 'result': 'PASS' if not missing else 'FAIL', 'contract': 'exact source path/hash plus normal-graph Gradle class output path/hash; no loaned/manual classes'}
    write_json(EVIDENCE / (phase['name'] + '-class-provenance.json'), result)
    return result

def collect_candidate_source_class_provenance(plan):
    records = []
    failures = []
    for item in plan['candidate_source_class_provenance']:
        source = pathlib.Path(plan['candidate']['worktree']) / item['source']
        class_file = pathlib.Path(item['class_file'])
        record = {'source': str(source), 'expected_source_sha256': item['source_sha256'], 'source_exists': source.is_file(), 'class_file': str(class_file), 'class_exists': class_file.is_file()}
        if source.is_file(): record['source_sha256'] = sha256(source)
        if class_file.is_file(): record.update({'class_sha256': sha256(class_file), 'class_mtime': class_file.stat().st_mtime})
        ok = record.get('source_sha256') == item['source_sha256'] and record['class_exists']
        record['result'] = 'PASS' if ok else 'FAIL'
        if not ok: failures.append(record)
        records.append(record)
    result = {'at_actual_system_clock': now(), 'records': records, 'failures': failures, 'result': 'PASS' if not failures else 'FAIL'}
    write_json(EVIDENCE / 'candidate-source-class-provenance.json', result)
    return result

def mark_not_run(plan, phase_summaries):
    completed = set(value['phase'] for value in phase_summaries)
    for phase in plan['phases']:
        if phase['name'] in completed: continue
        raw = pathlib.Path(phase['raw_artifact']); raw.touch(exist_ok=True)
        xml = {'at_actual_system_clock': now(), 'phase': phase['name'], 'result': 'NOT_RUN', 'counts': {'tests': 0, 'failures': 0, 'errors': 0, 'skipped': 0}, 'expected_classes': sorted(phase['expected_classes']), 'actual_fresh_classes': [], 'missing_classes': sorted(phase['expected_classes']), 'unexpected_classes': [], 'stale_ignored': [], 'files': [], 'copied': []}
        write_json(EVIDENCE / (phase['name'] + '-fresh-xml.json'), xml)
        result = {'phase': phase['name'], 'at_actual_system_clock': now(), 'result': 'NOT_RUN', 'reason': 'stopped after first actual failure', 'raw_artifact': str(raw), 'raw_sha256': sha256(raw), 'xml': xml, 'mysql_cleanup': None}
        write_json(EVIDENCE / (phase['name'] + '-result.json'), result); phase_summaries.append(result)


def write_index(name):
    files = sorted(p for p in EVIDENCE.rglob('*') if p.is_file() and p.name != name)
    lines = []
    for path in files:
        lines.append('{}  {}\n'.format(sha256(path), str(path.relative_to(EVIDENCE))))
    (EVIDENCE / name).write_text(''.join(lines))


def main():
    plan = json.loads(PLAN_PATH.read_text())
    bindings = json.loads(BINDINGS_PATH.read_text())
    if sha256(__file__) != plan['runner_script_sha256']:
        raise VerificationFailure('runner_hash_mismatch', 'Verification runner hash drift')
    if plan.get('execution_authorization', {}).get('state') != 'GO':
        raise VerificationFailure('execution_not_authorized', 'Main ledger binding plus GO is required before any bridge, MySQL, or Gradle action', plan.get('execution_authorization', {}))
    runner_receipt = {'started_at_actual_system_clock': now(), 'pid': os.getpid(),
                      'start_ticks': process_start_ticks(os.getpid()),
                      'script': str(pathlib.Path(__file__).resolve()),
                      'script_sha256': sha256(__file__), 'python': sys.version,
                      'candidate': plan['candidate']}
    write_json(EVIDENCE / 'runner-receipt.json', runner_receipt)
    for phase in plan['phases']:
        pathlib.Path(phase['raw_artifact']).touch(exist_ok=True)
    adapter = OwnedTcpUnixAdapter('127.0.0.1', 46139, plan['mysql']['socket'])
    success = False
    phase_summaries = []
    try:
        mysqld_before = verify_mysqld_process(plan)
        write_json(EVIDENCE / 'owned-mysqld-process-before.json', mysqld_before)
        unix = run_mysql(plan, 'SOCKET', plan['mysql']['prefixes'],
                         EVIDENCE / 'mysql-unix-readonly-preflight.tsv')
        if unix['matching_schemas']:
            raise VerificationFailure('private_prefix_not_absent',
                                      'Private prefixes already exist before adapter start', unix)
        write_json(EVIDENCE / 'mysql-unix-readonly-preflight.json', unix)
        adapter.start()
        write_json(EVIDENCE / 'adapter-start.json', dict(adapter.receipt(),
                                                         started_at_actual_system_clock=now()))
        tcp = run_mysql(plan, 'TCP', plan['mysql']['prefixes'],
                        EVIDENCE / 'mysql-tcp-readonly-preflight.tsv')
        if tcp['matching_schemas']:
            raise VerificationFailure('private_prefix_not_absent',
                                      'Private prefixes already exist through owned TCP adapter', tcp)
        tcp['endpoint_proof'] = 'successful explicit TCP mysql client to owned adapter 127.0.0.1:46139'
        tcp['mysqld_reported_port_zero_expected_skip_networking'] = True
        write_json(EVIDENCE / 'mysql-tcp-readonly-preflight.json', tcp)
        for phase in plan['phases']:
            verify_stable_inputs(plan, bindings, phase, adapter)
            prefix = phase['private_prefix']
            before = run_mysql(plan, 'TCP', [prefix],
                               EVIDENCE / (phase['name'] + '-mysql-before.tsv'))
            if before['matching_schemas']:
                raise VerificationFailure('private_prefix_not_absent',
                                          'Phase prefix exists before {}'.format(phase['name']), before)
            write_json(EVIDENCE / (phase['name'] + '-mysql-before.json'), before)
            returncode, start_epoch = run_gradle_phase(plan, phase)
            try:
                xml = collect_fresh_xml(phase, start_epoch)
                provenance = collect_class_provenance(plan, phase)
                candidate_provenance = collect_candidate_source_class_provenance(plan) if phase['name'] == 'phase1-v3' else None
            except Exception as collection_error:
                collection_result = {'phase': phase['name'], 'at_actual_system_clock': now(),
                                     'result': 'COLLECTION_ERROR_AFTER_GRADLE',
                                     'gradle_returncode': returncode, 'raw_artifact': phase['raw_artifact'],
                                     'raw_sha256': sha256(phase['raw_artifact']),
                                     'collection_exception': repr(collection_error),
                                     'collection_traceback': traceback.format_exc(),
                                     'status_meaning': 'Gradle completed; XML/provenance collection failed. Not NOT_RUN.'}
                write_json(EVIDENCE / (phase['name'] + '-result.json'), collection_result)
                phase_summaries.append(collection_result)
                raise VerificationFailure('collection_error_after_gradle',
                                          '{} collection failed after Gradle completion'.format(phase['name']),
                                          collection_result)
            after = run_mysql(plan, 'TCP', [prefix],
                              EVIDENCE / (phase['name'] + '-mysql-after.tsv'))
            after['cleanup_result'] = 'PASS' if not after['matching_schemas'] else 'FAIL'
            write_json(EVIDENCE / (phase['name'] + '-mysql-after.json'), after)
            result = {'phase': phase['name'], 'at_actual_system_clock': now(),
                      'gradle_returncode': returncode, 'raw_artifact': phase['raw_artifact'],
                      'raw_sha256': sha256(phase['raw_artifact']), 'xml': xml,
                      'class_provenance': provenance, 'candidate_source_class_provenance': candidate_provenance,
                      'mysql_cleanup': after}
            result['result'] = ('PASS' if returncode == 0 and xml['result'] == 'PASS'
                                and after['cleanup_result'] == 'PASS' and provenance['result'] == 'PASS'
                                and (candidate_provenance is None or candidate_provenance['result'] == 'PASS')
                                and not adapter.errors else 'FAIL')
            write_json(EVIDENCE / (phase['name'] + '-result.json'), result)
            phase_summaries.append(result)
            if result['result'] != 'PASS':
                raise VerificationFailure('gradle_or_acceptance_failure',
                                          '{} failed; no later phase run'.format(phase['name']), result)
        final_tcp = run_mysql(plan, 'TCP', plan['mysql']['prefixes'],
                              EVIDENCE / 'mysql-final-cleanup.tsv')
        final_tcp['cleanup_result'] = 'PASS' if not final_tcp['matching_schemas'] else 'FAIL'
        write_json(EVIDENCE / 'mysql-final-cleanup.json', final_tcp)
        if final_tcp['cleanup_result'] != 'PASS':
            raise VerificationFailure('mysql_cleanup_failure', 'Owned private schemas remain', final_tcp)
        success = True
    except VerificationFailure as failure:
        record = {'at_actual_system_clock': now(), 'result': 'FAILED_STOP',
                  'category': failure.category, 'failure': str(failure),
                  'details': failure.details, 'candidate': plan['candidate'],
                  'completed_phases': [value['phase'] for value in phase_summaries if value.get('result') == 'PASS'],
                  'executed_or_recorded_phases': [value['phase'] for value in phase_summaries],
                  'retry': 'STOP; attribute through orchestrator; no retry without new GO'}
        write_json(EVIDENCE / 'failure-attribution.json', record)
        mark_not_run(plan, phase_summaries)
    except Exception as failure:
        record = {'at_actual_system_clock': now(), 'result': 'FAILED_STOP',
                  'category': 'verification_runner_internal', 'failure': repr(failure),
                  'traceback': traceback.format_exc(), 'candidate': plan['candidate'],
                  'completed_phases': [value['phase'] for value in phase_summaries if value.get('result') == 'PASS'],
                  'executed_or_recorded_phases': [value['phase'] for value in phase_summaries],
                  'retry': 'STOP; attribute through orchestrator; no retry without new GO'}
        write_json(EVIDENCE / 'failure-attribution.json', record)
        mark_not_run(plan, phase_summaries)
    finally:
        before_close = adapter.receipt()
        adapter.stop()
        probe = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        probe.settimeout(0.25)
        try:
            connect_ex_after_close = probe.connect_ex(('127.0.0.1', 46139))
        finally:
            probe.close()
        cleanup = {'at_actual_system_clock': now(), 'before_close': before_close,
                   'after_close': adapter.receipt(), 'tcp_connect_ex_after_close': connect_ex_after_close,
                   'owned_listener_closed': connect_ex_after_close != 0,
                   'owned_mysqld_after': verify_mysqld_process(plan),
                   'mysqld_action': 'NONE'}
        write_json(EVIDENCE / 'adapter-cleanup.json', cleanup)
    final = {'at_actual_system_clock': now(), 'result': 'PASS' if success else 'FAILED_STOP',
             'candidate': plan['candidate'], 'phase_results': [
                 {'phase': value['phase'], 'result': value['result'],
                  'counts': value.get('xml', {}).get('counts'), 'raw_sha256': value.get('raw_sha256'),
                  'mysql_cleanup': (value.get('mysql_cleanup') or {}).get('cleanup_result')}
                 for value in phase_summaries],
             'adapter_cleanup': json.loads((EVIDENCE / 'adapter-cleanup.json').read_text()),
             'worktree': {'head': git_value(plan['candidate']['worktree'], 'rev-parse', 'HEAD'),
                          'tree': git_value(plan['candidate']['worktree'], 'rev-parse', 'HEAD^{tree}'),
                          'status_porcelain': git_value(plan['candidate']['worktree'], 'status', '--porcelain')}}
    write_json(EVIDENCE / 'final-summary.json', final)
    write_index('FINAL-EVIDENCE.sha256')
    print('CYF_VERIFICATION_FINAL ' + json.dumps(final, sort_keys=True), flush=True)
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
