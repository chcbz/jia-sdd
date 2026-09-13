#!/usr/bin/env python3
"""Read-only pinned helper lock inspection; export only sanitized Python syntax."""
import ast
import copy
import hashlib
import json
import os
from pathlib import Path
import stat
import time

HELPER = Path('/usr/local/sbin/cyf-web-flow-deploy')
EXPECTED = '53070ba8cf924852744e38c232d0b5d5b3fd432e0d05c90b8f9a877af21b9bb6'
SAFE_STRINGS = {'/var/lib/cyf-web-flow', '/var/lib/cyf-web-flow/deploy.lock',
                'deploy.lock', 'a', 'a+', 'w', 'r', 'r+', 'rb', '__main__'}

class Redact(ast.NodeTransformer):
    def visit_Constant(self, node):
        if isinstance(node.value, str) and node.value not in SAFE_STRINGS:
            return ast.copy_location(ast.Constant('<redacted>'), node)
        return node


def main():
    fd = os.open(HELPER, os.O_RDONLY | os.O_NOFOLLOW)
    with os.fdopen(fd, 'rb') as stream:
        before = os.fstat(stream.fileno())
        data = stream.read(1024*1024+1)
        after = os.fstat(stream.fileno())
    assert stat.S_ISREG(before.st_mode) and before.st_uid == 0
    assert (before.st_dev,before.st_ino,before.st_size,before.st_mtime_ns) == (after.st_dev,after.st_ino,after.st_size,after.st_mtime_ns)
    assert len(data) <= 1024*1024 and hashlib.sha256(data).hexdigest() == EXPECTED
    tree = ast.parse(data.decode())
    statements = [n for n in ast.walk(tree) if isinstance(n, ast.stmt)]
    selected = []
    for node in statements:
        # Compound nodes contribute only their header, never whole function bodies.
        shallow = copy.deepcopy(node)
        for field in ('body','orelse','finalbody','handlers'):
            if hasattr(shallow,field):
                setattr(shallow,field,[ast.Pass()] if field == 'body' else [])
        rendered = ast.unparse(shallow)
        if any(word in rendered.lower() for word in ('lock','flock')):
            selected.append(node)
    names = {n.id for node in selected for n in ast.walk(node)
             if isinstance(n,ast.Name)}
    dependencies = [n for n in statements if isinstance(n,(ast.Assign,ast.AnnAssign))
                    and any(isinstance(x,ast.Name) and isinstance(x.ctx,ast.Store) and x.id in names for x in ast.walk(n))]
    exported=[]
    for node in sorted({n.lineno:n for n in selected+dependencies}.values(),key=lambda n:n.lineno):
        clone=copy.deepcopy(node)
        for field in ('body','orelse','finalbody','handlers'):
            if hasattr(clone,field):
                setattr(clone,field,[ast.Pass()] if field == 'body' else [])
        exported.append({'line':node.lineno,'endLine':node.end_lineno,
                         'syntax':ast.unparse(Redact().visit(clone))})
    info = Path('/var/lib/cyf-web-flow/deploy.lock').lstat()
    print(json.dumps({'observedAtEpoch':int(time.time()),'readOnly':True,
                      'helperSha256':EXPECTED,'lockSyntax':exported,
                      'lock':{'device':info.st_dev,'inode':info.st_ino,'uid':info.st_uid,
                              'gid':info.st_gid,'mode':oct(stat.S_IMODE(info.st_mode)),
                              'nlink':info.st_nlink,'regular':stat.S_ISREG(info.st_mode)}} ,sort_keys=True))

if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(json.dumps({'status':'INSPECTION_FAILED','errorType':type(exc).__name__}))
        raise SystemExit(1)
