#!/usr/bin/env python3
"""Offline, fail-closed Spring MVC inventory scanner and reconciler (Python 3.6+)."""
from __future__ import print_function
import argparse, hashlib, json, os, re, subprocess, sys

MAPPING_ANN = {"GetMapping":"GET", "PostMapping":"POST", "PutMapping":"PUT", "DeleteMapping":"DELETE", "PatchMapping":"PATCH", "HeadMapping":"HEAD", "OptionsMapping":"OPTIONS"}
METHODS = set(["GET","POST","PUT","DELETE","PATCH","HEAD","OPTIONS","TRACE"])

class InventoryError(Exception): pass

def _diag(code, message, file=None, line=None, fatal=True):
    d = {"code": code, "message": message, "fatal": bool(fatal)}
    if file: d["file"] = file
    if line: d["line"] = line
    return d

def _strip_comments(s):
    # A lexical comment stripper: strings and chars are retained; comment-like text in literals is not removed.
    out=[]; i=0; state="code"
    while i < len(s):
        c=s[i]; n=s[i+1] if i+1 < len(s) else ""
        if state == "code":
            if c == '"': state="string"; out.append(c)
            elif c == "'": state="char"; out.append(c)
            elif c == '/' and n == '/': out.extend('  '); i += 1; state="line"
            elif c == '/' and n == '*': out.extend('  '); i += 1; state="block"
            else: out.append(c)
        elif state == "line":
            if c == '\n': state="code"; out.append(c)
            else: out.append(' ')
        elif state == "block":
            if c == '*' and n == '/': out.extend('  '); i += 1; state="code"
            else: out.append('\n' if c == '\n' else ' ')
        else:
            out.append(c)
            if c == '\\' and i+1 < len(s): out.append(s[i+1]); i += 1
            elif (state == "string" and c == '"') or (state == "char" and c == "'"): state="code"
        i += 1
    return ''.join(out)

def _balanced(text, start):
    if start >= len(text) or text[start] != '(':
        return "", start
    depth=0; quote=None; esc=False
    for i in range(start, len(text)):
        c=text[i]
        if quote:
            if esc: esc=False
            elif c == '\\': esc=True
            elif c == quote: quote=None
            continue
        if c in ('"', "'"): quote=c
        elif c == '(': depth += 1
        elif c == ')':
            depth -= 1
            if depth == 0: return text[start+1:i], i+1
    raise ValueError("unclosed annotation arguments")

def _split_top(s, sep=','):
    parts=[]; start=0; depth=0; quote=None; esc=False
    for i,c in enumerate(s):
        if quote:
            if esc: esc=False
            elif c == '\\': esc=True
            elif c == quote: quote=None
        elif c in ('"', "'"): quote=c
        elif c in '({[': depth += 1
        elif c in ')}]': depth -= 1
        elif c == sep and depth == 0: parts.append(s[start:i].strip()); start=i+1
    parts.append(s[start:].strip())
    return [p for p in parts if p]

def _strings(expr):
    vals=[]
    for m in re.finditer(r'"((?:\\.|[^"\\])*)"', expr):
        vals.append(bytes(m.group(1), 'utf8').decode('unicode_escape'))
    residue=re.sub(r'"(?:\\.|[^"\\])*"', '', expr).strip()
    if residue and not re.match(r'^(?:\{\s*\})?$', residue):
        # only literals or literal arrays are accepted
        if not re.match(r'^\{\s*(?:,?\s*)\}$', residue):
            return None
    return vals

def _arg_map(args):
    result={}
    for part in _split_top(args):
        if '=' in part:
            k,v=part.split('=',1); result[k.strip()] = v.strip()
        else:
            result.setdefault("value", part.strip())
    return result

def _paths(args):
    a=_arg_map(args); expr=a.get('path', a.get('value', '""'))
    vals=_strings(expr)
    return vals

def _methods(args, annotation):
    if annotation in MAPPING_ANN: return [MAPPING_ANN[annotation]]
    a=_arg_map(args)
    if 'method' not in a: return ['ANY']
    expr=a['method']; vals=re.findall(r'RequestMethod\.([A-Z]+)', expr)
    if not vals:
        vals=_strings(expr) or []
    if not vals or any(v not in METHODS for v in vals): return None
    return vals

def _join(base, path):
    if not base: base='/'
    if not path: path='/'
    x=(base.rstrip('/') + '/' + path.lstrip('/'))
    x=re.sub(r'/+', '/', x)
    return x if x.startswith('/') else '/'+x

def _annotation_records(clean, filename):
    found=[]; i=0
    names=list(MAPPING_ANN)+["RequestMapping"]
    pattern=re.compile(r'@(' + '|'.join(names) + r')\b')
    while True:
        m=pattern.search(clean,i)
        if not m: break
        end=m.end(); args=""
        j=end
        while j < len(clean) and clean[j].isspace(): j+=1
        if j < len(clean) and clean[j]=='(':
            try: args, j = _balanced(clean,j)
            except ValueError as e:
                found.append((None, None, clean.count('\n',0,m.start())+1, str(e))); break
        found.append((m.group(1),args,clean.count('\n',0,m.start())+1,j)); i=j
    return found

def scan_source(root):
    root=os.path.abspath(root)
    if not os.path.isdir(root): raise InventoryError("source root does not exist: %s" % root)
    records=[]; diagnostics=[]; files=[]
    for dp, dns, fns in os.walk(root):
        dns.sort(); fns.sort()
        for fn in fns:
            if fn.endswith('Controller.java'):
                files.append(os.path.join(dp,fn))
    for filename in sorted(files):
        with open(filename,'r',encoding='utf-8') as source_file: raw=source_file.read()
        clean=_strip_comments(raw)
        anns=_annotation_records(clean, filename); class_prefixes=['']
        for idx, item in enumerate(anns):
            name,args,line,end=item
            if name is None:
                diagnostics.append(_diag('unresolved_annotation', args, filename,line)); continue
            # Class-vs-method is deliberately narrow: look only at the next declaration.
            tail=clean[end:end+1200]
            decl=re.search(r'\b(class|interface|enum)\s+([A-Za-z_$][\w$]*)\b([^\{;]*)\{',tail)
            method=re.search(r'\b(?:public|protected|private|static|final|synchronized|native|abstract|default|\s)+[\w$<>\[\],.? ]+\s+([A-Za-z_$][\w$]*)\s*\([^;{}]*\)\s*(?:throws[^\{]+)?\{',tail)
            is_class=bool(decl and (not method or decl.start() < method.start()))
            try: ps=_paths(args); ms=_methods(args,name)
            except Exception as exc: ps=ms=None; diagnostics.append(_diag('unsupported_mapping', str(exc),filename,line))
            if ps is None or ms is None or not ps:
                diagnostics.append(_diag('unsupported_mapping', 'mapping requires string literal path(s) and supported method(s)',filename,line)); continue
            if is_class:
                class_prefixes=ps
                if len(ps)>1: diagnostics.append(_diag('class_path_array', 'class mapping path array expanded as a Cartesian product',filename,line,False))
                if 'extends ' in (decl.group(3) or '') or 'implements ' in (decl.group(3) or ''):
                    diagnostics.append(_diag('unsupported_inheritance', 'inheritance mappings are not inferred; provide explicit manifest',filename,line))
            else:
                if not class_prefixes:
                    diagnostics.append(_diag('unresolved_class_mapping', 'method mapping has no resolvable class path',filename,line)); continue
                if not method:
                    diagnostics.append(_diag('unresolved_mapping_owner', 'mapping is not attached to a narrow method declaration',filename,line)); continue
                method_name=method.group(1)
                for prefix in class_prefixes:
                    for p in ps:
                        for verb in ms:
                            records.append({'kind':'controller','method':verb,'path':_join(prefix,p),'handler':os.path.relpath(filename,root)+':'+method_name,'source':os.path.relpath(filename,root),'line':line})
    records.sort(key=lambda r:(r['method'],r['path'],r['handler']))
    return records, diagnostics, files

def sha256_files(root, files):
    h=hashlib.sha256()
    for f in sorted(files):
        rel=os.path.relpath(f,root).replace(os.sep,'/')
        with open(f,'rb') as source_file: b=source_file.read()
        h.update(rel.encode()); h.update(b'\0'); h.update(b)
    return h.hexdigest()

def git_binding(root):
    def run(*args):
        try: return subprocess.check_output(['git','-C',root]+list(args),stderr=subprocess.STDOUT).decode().strip()
        except Exception: return None
    commit=run('rev-parse','HEAD'); tree=run('rev-parse','HEAD^{tree}')
    dirty=bool(run('status','--porcelain','--untracked-files=all'))
    return {'commit':commit,'tree':tree,'dirty':dirty}

def load_json(path):
    with open(path,encoding='utf-8') as f: return json.load(f)

def _runtime_routes(obj):
    out=[]
    def add(method,path,extra=None):
        if not path: return
        if isinstance(method,list): methods=method or ['ANY']
        elif method in (None,''): methods=['ANY']
        else: methods=[str(method).upper()]
        for m in methods:
            out.append({'kind':'runtime','method':m,'path':str(path), 'handler': (extra or '')})
    def walk(x):
        if isinstance(x,list):
            for y in x: walk(y)
        elif isinstance(x,dict):
            if 'path' in x or 'pattern' in x:
                p=x.get('path',x.get('pattern')); add(x.get('method',x.get('methods')),p,x.get('handler'))
            pred=x.get('predicate')
            if isinstance(pred,str):
                m=re.match(r'^\{\s*(?:(GET|POST|PUT|DELETE|PATCH|HEAD|OPTIONS|TRACE)\s+)?\[([^]]+)\]',pred)
                if m: add(m.group(1),m.group(2),x.get('handler'))
            for k,v in x.items():
                if k not in ('path','pattern','method','methods','handler','predicate'): walk(v)
    walk(obj)
    unique={(r['method'],r['path'],r.get('handler','')):r for r in out}
    return sorted(unique.values(),key=lambda r:(r['method'],r['path'],r.get('handler','')))

def _keys(routes): return {(r['method'],r['path']) for r in routes}

def validate_registry(registry, routes):
    """Validate only the documented normalized JSON shape; this is not YAML parsing."""
    diags=[]
    if not isinstance(registry, dict) or not isinstance(registry.get('routes'), list):
        return [_diag('registry_shape', 'normalized registry JSON must contain a routes array')]
    actual=_keys(routes); declared=set()
    for item in registry['routes']:
        if not isinstance(item, dict) or not isinstance(item.get('method'), str) or not isinstance(item.get('path'), str):
            diags.append(_diag('registry_shape','each registry route requires string method and path')); continue
        method=item['method'].upper(); path=item['path']
        if '*' in path or '{*' in path:
            diags.append(_diag('registry_wildcard','wildcard registry routes are forbidden: %s %s'%(method,path)))
        declared.add((method,path))
    for key in sorted(actual-declared): diags.append(_diag('registry_missing','route missing from normalized registry: %s %s'%key))
    for key in sorted(declared-actual): diags.append(_diag('registry_unknown','normalized registry contains unknown route: %s %s'%key))
    return diags

def reconcile(static, manifest, runtime, expected, profile, inventory_diagnostics=None):
    diags=list(inventory_diagnostics or [])
    if not isinstance(manifest,dict): diags.append(_diag('invalid_manifest','framework manifest must be an object')); manifest={}
    for key in ('profile','api_commit','api_tree'):
        if not manifest.get(key): diags.append(_diag('binding_missing','framework manifest requires %s from the trusted capture envelope' % key))
    if manifest.get('profile') != profile: diags.append(_diag('profile_mismatch','framework manifest profile is missing or does not match requested profile'))
    if not expected.get('commit') or manifest.get('api_commit') != expected.get('commit'): diags.append(_diag('binding_mismatch','framework manifest API commit is missing or mismatched'))
    if not expected.get('tree') or manifest.get('api_tree') != expected.get('tree'): diags.append(_diag('binding_mismatch','framework manifest API tree is missing or mismatched'))
    if not isinstance(runtime,dict): runtime={}; diags.append(_diag('invalid_runtime','runtime capture must be an object'))
    for key in ('profile','api_commit','api_tree','capture_content_sha256'):
        if not runtime.get(key): diags.append(_diag('binding_missing','runtime capture requires %s from the trusted capture envelope' % key))
    if runtime.get('profile') != profile: diags.append(_diag('profile_mismatch','runtime profile is missing or does not match requested profile'))
    if runtime.get('api_commit') != expected.get('commit'): diags.append(_diag('binding_mismatch','runtime API commit is missing or mismatched'))
    if runtime.get('api_tree') != expected.get('tree'): diags.append(_diag('binding_mismatch','runtime API tree is missing or mismatched'))
    fw=_runtime_routes(manifest.get('routes',manifest.get('mappings',[])))
    rt=_runtime_routes(runtime.get('mappings', runtime))
    sk=_keys(static+fw); rk=_keys(rt)
    for m,p in sorted(sk-rk): diags.append(_diag('runtime_missing','declared route missing from runtime: %s %s'%(m,p)))
    for m,p in sorted(rk-sk): diags.append(_diag('runtime_unknown','runtime route not declared by static/framework inventory: %s %s'%(m,p)))
    return {'static':static,'framework':fw,'runtime':rt,'diagnostics':diags,'ok':not diags}

def main(argv=None):
    ap=argparse.ArgumentParser(description='Offline Spring MVC inventory scanner/reconciler')
    sub=ap.add_subparsers(dest='command')
    s=sub.add_parser('scan'); s.add_argument('--source-root',required=True); s.add_argument('--profile',required=True); s.add_argument('--api-commit'); s.add_argument('--api-tree'); s.add_argument('--framework-manifest'); s.add_argument('--registry-json'); s.add_argument('--output',required=True)
    r=sub.add_parser('reconcile'); r.add_argument('--inventory',required=True); r.add_argument('--runtime',required=True); r.add_argument('--profile',required=True); r.add_argument('--runtime-sha256')
    a=ap.parse_args(argv)
    try:
        if a.command=='scan':
            routes, diags, files=scan_source(a.source_root); binding=git_binding(os.path.abspath(a.source_root))
            if a.api_commit and binding['commit'] != a.api_commit: diags.append(_diag('source_binding_mismatch','source HEAD does not match --api-commit'))
            if a.api_tree and binding['tree'] != a.api_tree: diags.append(_diag('source_binding_mismatch','source tree does not match --api-tree'))
            if binding['dirty']: diags.append(_diag('source_dirty','source checkout is dirty'))
            manifest=load_json(a.framework_manifest) if a.framework_manifest else {}
            if not manifest: diags.append(_diag('framework_manifest_missing','explicit framework surface JSON manifest is required'))
            if manifest and manifest.get('profile') != a.profile: diags.append(_diag('profile_mismatch','manifest profile missing or mismatched'))
            if a.registry_json:
                diags.extend(validate_registry(load_json(a.registry_json), routes))
            result={'schema_version':1,'profile':a.profile,'source':{'root':os.path.abspath(a.source_root),'api_commit':binding['commit'],'api_tree':binding['tree'],'dirty':binding['dirty'],'java_content_sha256':sha256_files(a.source_root,files),'framework_manifest_sha256': (hashlib.sha256(open(a.framework_manifest,'rb').read()).hexdigest() if a.framework_manifest else None)},'routes':routes,'framework_manifest':manifest,'diagnostics':diags,'ok':not diags}
            with open(a.output,'w',encoding='utf-8') as f: json.dump(result,f,sort_keys=True,indent=2); f.write('\n')
            return 0 if result['ok'] else 2
        if a.command=='reconcile':
            inv=load_json(a.inventory); runtime=load_json(a.runtime)
            if inv.get('profile') != a.profile: raise InventoryError('profile mismatch')
            expected=inv.get('source',{}); result=reconcile(inv.get('routes',[]),inv.get('framework_manifest',{}),runtime,expected,a.profile,inv.get('diagnostics'))
            with open(a.runtime,'rb') as runtime_file: runtime_hash=hashlib.sha256(runtime_file.read()).hexdigest()
            result['runtime_content_sha256']=runtime_hash
            if a.runtime_sha256 and runtime_hash != a.runtime_sha256:
                result['diagnostics'].append(_diag('content_hash_mismatch','runtime JSON content hash mismatch')); result['ok']=False
            print(json.dumps(result,sort_keys=True,indent=2)); return 0 if result['ok'] else 2
        ap.error('a command is required')
    except (OSError,ValueError,InventoryError, json.JSONDecodeError) as exc:
        print('inventory: ERROR: %s' % exc, file=sys.stderr); return 2

if __name__=='__main__': sys.exit(main())
