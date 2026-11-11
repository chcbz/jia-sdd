from pathlib import Path
import base64,hashlib,zipfile,json,subprocess,os
from cryptography.hazmat.primitives.ciphers import Cipher,algorithms,modes
from cryptography.hazmat.primitives.padding import PKCS7
root=Path('/var/tmp/cyf-voice-realtime-20260930')
# Exclusive marker prevents an accidental second billable attempt.
marker=root/'attempt-started'
with zipfile.ZipFile('/opt/cyf/service/api/cyf-api-kit.jar') as z:
 lines=z.read('BOOT-INF/classes/application-prod.properties').decode().splitlines()
props={k.strip():v.strip() for l in lines if '=' in l and not l.lstrip().startswith('#') for k,v in [l.split('=',1)]}
base=props['spring.ai.openai.base-url'].rstrip('/')
assert base=='https://codex.chcbz.net/v1'
enc=props['spring.ai.openai.api-key'];assert enc.startswith('ENC(')
raw=base64.b64decode(enc[4:-1],validate=True)
password=Path('/opt/cyf/service/api/.jasypt-password').read_bytes().splitlines()[0]
derived=hashlib.pbkdf2_hmac('sha512',password,raw[:16],1000,32)
dec=Cipher(algorithms.AES(derived),modes.CBC(raw[16:32])).decryptor(); padded=dec.update(raw[32:])+dec.finalize()
u=PKCS7(128).unpadder();key=(u.update(padded)+u.finalize()).decode()
assert key and '\n' not in key and '\r' not in key
config={'base':base,'key':key,'connectTimeoutMillis':25000}
# 25s is the existing voice provider transport timeout, not a total response/SLO deadline.
fd=os.open(str(marker),os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600);os.close(fd)
r=subprocess.run(['/usr/bin/node',str(root/'probe.cjs')],input=json.dumps(config).encode())
raise SystemExit(r.returncode)
