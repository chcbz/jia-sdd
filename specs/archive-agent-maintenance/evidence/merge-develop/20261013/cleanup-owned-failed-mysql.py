import pathlib,shutil,json,os
root=pathlib.Path('/tmp/cyf-aam-merge-develop-20261013')
target=root/'mysql-data-attempt1'
assert root.resolve()==root and target.resolve()==target and not target.is_symlink()
assert target.parent==root and target.name=='mysql-data-attempt1'
active=[]
for process in pathlib.Path('/proc').glob('[0-9]*'):
 try:
  cmd=(process/'cmdline').read_bytes()
  if ('--datadir='+str(target)).encode() in cmd: active.append(process.name)
 except (OSError,IOError): pass
assert not active,active
bytes_before=sum(p.stat().st_size for p in target.rglob('*') if p.is_file() and not p.is_symlink())
shutil.rmtree(str(target))
result={'removed_only':str(target),'exact_path_verified':True,'active_own_mysql_processes':active,'bytes_before':bytes_before,'removed':not target.exists(),'logs_preserved':True,'tests_started':False,'cause':'MySQL initialization failed; contemporaneous filesystem exhaustion observed; no blind retry or foreign cleanup.'}
(root/'evidence/api-attempt1/environment-failure-and-cleanup.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
