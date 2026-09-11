#!/usr/bin/env python3
import json,os,sys
from pathlib import Path
mysql=json.loads(Path('/home/chc/.local/share/cyf-output-tools/services/mysql/state/credentials.json').read_text())
minio=json.loads(Path('/home/chc/.local/share/cyf-output-tools/services/minio-state/credentials.json').read_text())
env=os.environ.copy()
env.update({
 'JAVA_HOME':'/home/chc/.local/share/cyf-output-tools/java',
 'PATH':'/home/chc/.local/share/cyf-output-tools/java/bin:'+env.get('PATH',''),
 'OD01_MYSQL_URL':'jdbc:mysql://127.0.0.1:13306/?useSSL=false&allowPublicKeyRetrieval=true&serverTimezone=UTC',
 'OD01_MYSQL_USER':mysql['user'],'OD01_MYSQL_PASSWORD':mysql['password'],
 'OD02_MYSQL_URL':'jdbc:mysql://127.0.0.1:13306/?useSSL=false&allowPublicKeyRetrieval=true&serverTimezone=UTC',
 'OD02_MYSQL_USER':mysql['user'],'OD02_MYSQL_PASSWORD':mysql['password'],
 'OD02_S3_ENDPOINT':'http://127.0.0.1:19000','OD02_S3_ACCESS_KEY':minio['access_key'],'OD02_S3_SECRET_KEY':minio['secret_key'],
 'OD02_CLAM_HOST':'127.0.0.1','OD02_CLAM_PORT':'13310'
})
command=['flock','/tmp/cyf-gradle.lock','./gradlew','--include-build','plugin','--init-script','/home/chc/.local/share/cyf-output-tools/od00-development-opencv-substitution.init.gradle','--no-daemon','--max-workers=1','-Dorg.gradle.jvmargs=-Xmx512m -XX:MaxMetaspaceSize=256m',*sys.argv[1:]]
os.execvpe(command[0],command,env)
