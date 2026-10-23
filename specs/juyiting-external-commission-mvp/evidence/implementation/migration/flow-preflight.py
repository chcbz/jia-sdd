#!/usr/bin/env python3
"""D31 read-only pre-expansion gate, not a deployment/migration executor.
Exit 0 means pinned inputs and data preconditions pass, NOT that cutover happened.
Exit 2 blocks changed inputs, unproven rows, or partial schema requiring catalog recovery.
"""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent

def reasons_for(report, pins):
    rows = report['observations']
    reasons = []
    def one(section):
        found = [r for r in rows if r['section'] == section]
        if len(found) != 1:
            raise ValueError('missing/duplicate audit section')
        return found[0]
    target = one('target')
    if target['database'] != pins['target']['schema'] or target['serverUuidSha256'] != pins['target']['serverUuidSha256'] or target['mysqlVersion'] != pins['target']['mysqlVersionObserved']:
        reasons.append('TARGET_CHANGED')
    binding = one('migrationBindingFreeze')
    if binding['grants'] != binding['proven']:
        reasons.append('UNPROVEN_MIGRATION_BINDING')
    proof = one('chatProof')
    if proof['bountyDispatches'] != proof['provenDispatches'] or proof['ambiguousDispatches']:
        reasons.append('UNPROVEN_CHAT_REFERENCE')
    if one('invalidDispatchJson')['count']:
        reasons.append('INVALID_DISPATCH_JSON')
    if any(r['section'] in ('unresolvedMigrationFreeze','unresolvedChat') for r in rows):
        reasons.append('UNRESOLVED_ROWS')
    # Once-only expansion inputs must never be replayed against partial/complete schema.
    # Resume uses exact catalog comparison and explicit phase postchecks from README.
    if any(r['section'] in ('schema','indexes') for r in rows):
        reasons.append('EXPANSION_ALREADY_STARTED_USE_PHASE_RESUME')
    if any(r['section']=='engine' and r['engine']!='InnoDB' for r in rows):
        reasons.append('NON_TRANSACTIONAL_TABLE')
    return reasons

def main():
    if len(sys.argv) != 1:
        raise SystemExit('No apply/force arguments are supported.')
    pins = json.loads((HERE/'candidate-pins.json').read_text())
    for item in pins['inputs']:
        p = HERE/item['file']
        if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest() != item['sha256']:
            print(json.dumps({'status':'BLOCKED','reason':'CANDIDATE_INPUT_HASH_CHANGED','file':item['file']}))
            return 2
    for name, expected in pins['installedHelpers'].items():
        p = Path(name)
        if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest() != expected:
            print(json.dumps({'status':'BLOCKED','reason':'DEPLOY_HELPER_CHANGED','file':name}))
            return 2
    result = subprocess.run([sys.executable,'-B',str(HERE/'inspect.py')],stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True)
    if result.returncode:
        print(json.dumps({'status':'BLOCKED','reason':'READONLY_AUDIT_FAILED'}))
        return 2
    try:
        report = json.loads(result.stdout)
        reasons = reasons_for(report, pins)
    except (ValueError, KeyError, TypeError):
        print(json.dumps({'status':'BLOCKED','reason':'INVALID_AUDIT'}))
        return 2
    print(json.dumps({'status':'BLOCKED' if reasons else 'PREFLIGHT_PASS', 'reasons':reasons,
        'scope':'pre-expansion data/catalog only; no writes or deploy', 'audit':report,
        'nextAction':'Parent Flow wrapper: own locks, stop all writers, backup and repeat gate, apply pinned phases with postchecks before installer startup.'},indent=2))
    return 2 if reasons else 0

if __name__ == '__main__':
    sys.exit(main())
