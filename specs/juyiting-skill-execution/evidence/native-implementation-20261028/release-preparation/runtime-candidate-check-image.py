import hashlib, json, os, pathlib, stat, subprocess, zipfile
root=pathlib.Path('conf/skills/native-image').resolve()
out=pathlib.Path('_runtime_export').resolve()
raw=subprocess.check_output(['git','ls-files','-z','--','SKILL.md','scripts','vendor'],cwd=root)
names=sorted(os.fsdecode(x) for x in raw.split(b'\0') if x)
assert names and 'SKILL.md' in names and len(names)==len(set(names))
assert all(n=='SKILL.md' or n.startswith(('scripts/','vendor/')) for n in names)
for name in names:
    p=pathlib.PurePosixPath(name)
    assert not p.is_absolute() and '..' not in p.parts and not any(c in name for c in ('\n','\r','\x00'))
    q=root
    for part in p.parts:
        q=q/part
        st=q.lstat()
        assert not stat.S_ISLNK(st.st_mode)
    assert stat.S_ISREG(st.st_mode) and st.st_nlink==1
archive=out/'native-image.zip'
with zipfile.ZipFile(archive,'x',compression=zipfile.ZIP_DEFLATED) as z:
    for name in names: z.write(root/name,arcname=name)
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None and sorted(z.namelist())==names
    assert all(not stat.S_ISLNK(i.external_attr >> 16) for i in z.infolist())
size=archive.stat().st_size
h=hashlib.sha256()
with archive.open('rb') as f:
    for block in iter(lambda:f.read(1024*1024),b''): h.update(block)
meta={'commit':os.environ['CI_COMMIT_SHA'],'tree':subprocess.check_output(['git','rev-parse','HEAD^{tree}'],universal_newlines=True).strip(),'pipeline':os.environ['PIPELINE_ID'],'run':os.environ['BUILD_NUMBER'],'file':'native-image.zip','sha256':h.hexdigest(),'byteLength':size,'entries':names}
(out/'native-image-package.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
print('NATIVE_IMAGE_PACKAGE_SHA256='+h.hexdigest(),'BYTES='+str(size))
